from config import PLAYER_SIZE, SLASH_COOLDOWN, SLASH_DAMAGE, SLASH_ARC_DEGREES, SLASH_DURATION, SLASH_SHEET_PATH, SLASH_FRAME_COUNT
import pygame
import math
import os
from skills.base import Skill
from utils.resource_path import resource_path
from audio.sound_manager import SoundManager

class SlashSkill(Skill):
    # Class-level cache for frames
    _cached_frames = None

    def __init__(self, user, cooldown=SLASH_COOLDOWN, damage=SLASH_DAMAGE, arc_deg=SLASH_ARC_DEGREES, duration=SLASH_DURATION):
        super().__init__(user, cooldown, name="Slash")
        self.base_damage = damage
        self.damage = damage
        self.arc_deg = arc_deg
        self.duration = duration
        # Use class-level cache for frames
        if SlashSkill._cached_frames is None:
            SlashSkill._cached_frames = self._load_frames()
        self.frames = SlashSkill._cached_frames
        self.total_frames = len(self.frames)
        self.frame_time = duration / max(1, self.total_frames)
        self.active = False
        self.animation_frame = 0
        self.hit_entities = set()
        self.start_angle = None
        self.end_angle = None
        self.center = None

    def _load_frames(self):
        frames = []
        slash_path = resource_path(SLASH_SHEET_PATH)
        if not os.path.exists(slash_path):
            return frames
        sheet = pygame.image.load(slash_path).convert_alpha()
        sheet_width, sheet_height = sheet.get_width(), sheet.get_height()
        frame_width = sheet_width // SLASH_FRAME_COUNT
        for i in range(SLASH_FRAME_COUNT):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))
            frames.append(frame)
        return frames

    def use(self, target_pos=None):
        now = pygame.time.get_ticks() / 1000
        if not self.can_use(now):
            return False
            
        # Apply general enhancements
        self._apply_general_enhancements()
        
        # Play slash sound effect using sound manager
        SoundManager.play_skill_sound('slash')
                
        self.last_used = now
        self.active = True
        self.animation_frame = 0
        self.hit_entities.clear()
        # Calculate arc center and angles
        self.center = self.user.rect.center
        self.target_pos = target_pos if target_pos else pygame.mouse.get_pos()
        dx, dy = self.target_pos[0] - self.center[0], self.target_pos[1] - self.center[1]
        angle = math.degrees(math.atan2(dy, dx)) % 360
        self.start_angle = (angle - self.arc_deg / 2) % 360
        self.end_angle = (angle + self.arc_deg / 2) % 360
        return True

    def update(self, dt, entities):
        if not self.active:
            return
        self.animation_frame += dt / self.frame_time
        if self.animation_frame >= self.total_frames:
            self.active = False
            return
        # Hit detection
        for entity in entities:
            if entity is self.user or entity in self.hit_entities:
                continue
            if self._in_slash_arc(entity):
                # Apply damage with enhancements
                damage = self._check_double_damage(self.base_damage)
                entity.take_damage(damage, source=self, attacker=self.user)
                self.hit_entities.add(entity)
                
                # Apply skill-specific enhancements
                self._apply_slash_enhancements(entity)

    def draw(self, surface, last_move=(1,0), camera=None):
        if not self.active or not self.frames:
            return
        
        # Store camera reference for collision detection
        self.camera = camera
        
        # Calculate current frame index
        frame_idx = min(int(self.animation_frame), self.total_frames - 1)
        frame = self.frames[frame_idx]
        # Always face the target_pos direction and rotate the sprite
        if not hasattr(self, 'target_pos') or self.target_pos is None:
            mouse_screen = pygame.mouse.get_pos()
            # Convert mouse screen position to world coordinates if camera is available
            if camera:
                self.target_pos = camera.screen_to_world(mouse_screen[0], mouse_screen[1])
            else:
                self.target_pos = mouse_screen
        if hasattr(self.user, 'x') and hasattr(self.user, 'y'):
            world_px, world_py = self.user.x, self.user.y
        else:
            world_px, world_py = self.user.rect.center
            
        # Apply camera transformation to player position
        if camera:
            px, py = camera.world_to_screen(world_px, world_py)
        else:
            px, py = int(world_px), int(world_py)
            
        # For world coordinate calculations, use world positions
        if camera and hasattr(self, 'target_pos'):
            target_world_x, target_world_y = self.target_pos
            dx, dy = target_world_x - world_px, target_world_y - world_py
        else:
            dx, dy = self.target_pos[0] - px, self.target_pos[1] - py
        angle = math.degrees(math.atan2(dy, dx)) % 360
        # Sprite faces right (0°) by default, so rotate by -angle
        draw_frame = pygame.transform.rotate(frame, -angle)
        # Scale sprite 20% bigger for better visual impact
        sprite_scale = 1.5
        scaled_width = int(draw_frame.get_width() * sprite_scale)
        scaled_height = int(draw_frame.get_height() * sprite_scale)
        draw_frame = pygame.transform.scale(draw_frame, (scaled_width, scaled_height))
        # Offset: place slash just next to player in target direction
        offset_dist = PLAYER_SIZE // 2 + 4
        norm = math.hypot(dx, dy)
        if norm == 0:
            norm = 1
        dir_x, dir_y = dx / norm, dy / norm
        offset_x = int(px + dir_x * offset_dist)
        offset_y = int(py + dir_y * offset_dist)
        rect = draw_frame.get_rect(center=(offset_x, offset_y))
        surface.blit(draw_frame, rect)
        
        # Calculate and draw debug hitbox visualization
        # Get the base frame for hitbox calculation
        frame_idx = min(int(self.animation_frame), self.total_frames - 1)
        base_frame = self.frames[frame_idx]
        
        # Apply size enhancement
        if self.size_multiplier != 1.0:
            enhanced_width = int(base_frame.get_width() * self.size_multiplier)
            enhanced_height = int(base_frame.get_height() * self.size_multiplier)
            base_frame = pygame.transform.scale(base_frame, (enhanced_width, enhanced_height))
        
        # Define hitbox dimensions - make it longer in the slash direction
        # The sprite is naturally oriented to slash horizontally (right-facing)
        # So width is the slash length, height is the slash width
        hitbox_width = base_frame.get_width()  # Keep original length
        hitbox_height = base_frame.get_height() * 1.5  # Make it wider perpendicular to slash
        
        # Create the four corners of the unrotated rectangle centered at origin
        half_w, half_h = hitbox_width / 2, hitbox_height / 2
        corners = [
            (-half_w, -half_h),  # top-left
            (half_w, -half_h),   # top-right
            (half_w, half_h),    # bottom-right
            (-half_w, half_h)    # bottom-left
        ]
        
        # Use the SAME angle calculation as the sprite rotation above
        debug_angle = math.degrees(math.atan2(dy, dx)) % 360
        angle_rad = math.radians(-debug_angle)  # negative because sprite rotates opposite
        cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
        rotated_corners = []
        for x, y in corners:
            rot_x = x * cos_a - y * sin_a + offset_x
            rot_y = x * sin_a + y * cos_a + offset_y
            rotated_corners.append((rot_x, rot_y))
        
        # Draw the yellow debug hitbox polygon
        pygame.draw.polygon(surface, (255, 255, 0), rotated_corners, 2)

    def _in_slash_arc(self, entity):
        # Use the same coordinate calculation as the draw method
        frame_idx = min(int(self.animation_frame), self.total_frames - 1)
        frame = self.frames[frame_idx]
        
        # Always face the target_pos direction and rotate the sprite
        if not hasattr(self, 'target_pos') or self.target_pos is None:
            mouse_screen = pygame.mouse.get_pos()
            # Convert mouse screen position to world coordinates if camera is available
            if hasattr(self, 'camera') and self.camera:
                self.target_pos = self.camera.screen_to_world(mouse_screen[0], mouse_screen[1])
            else:
                self.target_pos = mouse_screen
                
        if hasattr(self.user, 'x') and hasattr(self.user, 'y'):
            world_px, world_py = self.user.x, self.user.y
        else:
            world_px, world_py = self.user.rect.center
            
        # For world coordinate calculations, use world positions
        if hasattr(self, 'camera') and self.camera and hasattr(self, 'target_pos'):
            target_world_x, target_world_y = self.target_pos
            dx, dy = target_world_x - world_px, target_world_y - world_py
        else:
            # Convert to screen coordinates for calculation
            if hasattr(self, 'camera') and self.camera:
                px, py = self.camera.world_to_screen(world_px, world_py)
            else:
                px, py = int(world_px), int(world_py)
            dx, dy = self.target_pos[0] - px, self.target_pos[1] - py
            
        offset_dist = PLAYER_SIZE // 2 + 4
        norm = math.hypot(dx, dy)
        if norm == 0:
            norm = 1
        dir_x, dir_y = dx / norm, dy / norm
        
        # Use world coordinates for collision detection
        offset_x = world_px + dir_x * offset_dist
        offset_y = world_py + dir_y * offset_dist
        angle = math.degrees(math.atan2(dy, dx)) % 360
        
        # Create hitbox as a rotated rectangle with consistent dimensions
        base_frame = frame.copy()
        # Apply size enhancement first
        if self.size_multiplier != 1.0:
            enhanced_width = int(base_frame.get_width() * self.size_multiplier)
            enhanced_height = int(base_frame.get_height() * self.size_multiplier)
            base_frame = pygame.transform.scale(base_frame, (enhanced_width, enhanced_height))
        
        # Define hitbox dimensions - make it longer in the slash direction
        # The sprite is naturally oriented to slash horizontally (right-facing)
        # So width is the slash length, height is the slash width
        hitbox_width = base_frame.get_width()  # Keep original length
        hitbox_height = base_frame.get_height() * 1.5  # Make it wider perpendicular to slash
        
        # Create the four corners of the unrotated rectangle centered at origin
        half_w, half_h = hitbox_width / 2, hitbox_height / 2
        corners = [
            (-half_w, -half_h),  # top-left
            (half_w, -half_h),   # top-right
            (half_w, half_h),    # bottom-right
            (-half_w, half_h)    # bottom-left
        ]
        
        # Rotate corners and translate to final position
        angle_rad = math.radians(-angle)  # negative because sprite rotates opposite
        cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
        rotated_corners = []
        for x, y in corners:
            rot_x = x * cos_a - y * sin_a + offset_x
            rot_y = x * sin_a + y * cos_a + offset_y
            rotated_corners.append((rot_x, rot_y))
        
        # Check collision using polygon collision with world coordinates
        # Get entity position in world coordinates
        if hasattr(entity, 'x') and hasattr(entity, 'y'):
            entity_center = (entity.x, entity.y)
            entity_corners = [
                (entity.x - entity.rect.width//2, entity.y - entity.rect.height//2),  # topleft
                (entity.x + entity.rect.width//2, entity.y - entity.rect.height//2),  # topright
                (entity.x + entity.rect.width//2, entity.y + entity.rect.height//2),  # bottomright
                (entity.x - entity.rect.width//2, entity.y + entity.rect.height//2)   # bottomleft
            ]
        else:
            entity_center = entity.rect.center
            entity_corners = [
                entity.rect.topleft, entity.rect.topright, 
                entity.rect.bottomright, entity.rect.bottomleft
            ]
        
        hit = self._point_in_rotated_rect(entity_center, rotated_corners) or \
              any(self._point_in_rotated_rect(corner, rotated_corners) for corner in entity_corners)
        
        # Store corners for debug visualization
        self._debug_hitbox_corners = rotated_corners
        
        return hit
    
    def _point_in_rotated_rect(self, point, corners):
        """Check if a point is inside a rotated rectangle defined by corners."""
        x, y = point
        # Use cross product method to check if point is inside polygon
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        # Check if point is on the same side of all edges
        signs = []
        for i in range(4):
            next_i = (i + 1) % 4
            signs.append(sign(point, corners[i], corners[next_i]))
        
        # Point is inside if all signs are the same (all positive or all negative)
        return all(s >= 0 for s in signs) or all(s <= 0 for s in signs)
    
    def _apply_slash_enhancements(self, entity):
        """Apply slash-specific enhancements to hit entity."""
        import random
        import math
        from entities.status_effects import StunEffect, KnockbackEffect
        
        # Stun enhancement
        stun_chance = self.user.get_enhancement_value('stun_chance', 'slash')
        if stun_chance > 0 and random.random() < stun_chance:
            from config_enhancements import SKILL_SPECIFIC_ENHANCEMENTS
            stun_duration = SKILL_SPECIFIC_ENHANCEMENTS['slash']['stun_chance']['stun_duration']
            stun_effect = StunEffect(stun_duration)
            entity.status_manager.add_effect(stun_effect)
            print(f"[SLASH] Stunned enemy for {stun_duration}s!")
        
        # Knockback enhancement
        knockback_force = self.user.get_enhancement_value('knockback', 'slash')
        if knockback_force > 0:
            # Calculate knockback direction (away from player)
            if hasattr(self.user, 'x') and hasattr(self.user, 'y'):
                player_x, player_y = self.user.x, self.user.y
            else:
                player_x, player_y = self.user.rect.center
            
            if hasattr(entity, 'x') and hasattr(entity, 'y'):
                entity_x, entity_y = entity.x, entity.y
            else:
                entity_x, entity_y = entity.rect.center
            
            dx = entity_x - player_x
            dy = entity_y - player_y
            distance = math.hypot(dx, dy)
            
            if distance > 0:
                # Normalize direction
                direction = (dx / distance, dy / distance)
                knockback_effect = KnockbackEffect(knockback_force, direction)
                entity.status_manager.add_effect(knockback_effect)
                print(f"[SLASH] Knocked back enemy with force {knockback_force}!")
        
        # Check for cooldown reset
        self._check_cooldown_reset()
