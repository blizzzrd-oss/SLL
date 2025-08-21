from config import PLAYER_SIZE, SLASH_COOLDOWN, SLASH_DAMAGE, SLASH_ARC_DEGREES, SLASH_DURATION, SLASH_SHEET_PATH, SLASH_FRAME_COUNT, SKILL_SLASH_SOUND_PATH, SFX_VOLUME
import pygame
import math
import os
from skills.base import Skill
from utils.resource_path import resource_path

class SlashSkill(Skill):
    # Class-level cache for frames and sound
    _cached_frames = None
    _cached_sound = None

    def __init__(self, user, cooldown=SLASH_COOLDOWN, damage=SLASH_DAMAGE, arc_deg=SLASH_ARC_DEGREES, duration=SLASH_DURATION):
        super().__init__(user, cooldown, name="Slash")
        self.damage = damage
        self.arc_deg = arc_deg
        self.duration = duration
        # Use class-level cache for frames
        if SlashSkill._cached_frames is None:
            SlashSkill._cached_frames = self._load_frames()
        self.frames = SlashSkill._cached_frames
        
        # Load sound effect (use class cache to avoid loading multiple times)
        if SlashSkill._cached_sound is None:
            try:
                sound_path = resource_path(SKILL_SLASH_SOUND_PATH)
                if os.path.exists(sound_path):
                    SlashSkill._cached_sound = pygame.mixer.Sound(sound_path)
                    SlashSkill._cached_sound.set_volume(SFX_VOLUME)
                else:
                    print(f"[WARNING] Slash sound file not found: {sound_path}")
                    SlashSkill._cached_sound = None
            except Exception as e:
                print(f"[WARNING] Failed to load slash sound: {e}")
                SlashSkill._cached_sound = None
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
            
        # Play slash sound effect
        if SlashSkill._cached_sound is not None:
            try:
                SlashSkill._cached_sound.play()
            except Exception as e:
                print(f"[WARNING] Failed to play slash sound: {e}")
                
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
                entity.take_damage(self.damage, source=self, attacker=self.user)
                self.hit_entities.add(entity)

    def draw(self, surface, last_move=(1,0), camera=None):
        if not self.active or not self.frames:
            return
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
        # Removed yellow hitbox debug visualization

    def _in_slash_arc(self, entity):
        # Use the current slash sprite's rect as the hitbox, placed by target_pos
        frame_idx = min(int(self.animation_frame), self.total_frames - 1)
        frame = self.frames[frame_idx]
        if not hasattr(self, 'target_pos') or self.target_pos is None:
            self.target_pos = pygame.mouse.get_pos()
        if hasattr(self.user, 'x') and hasattr(self.user, 'y'):
            px, py = int(self.user.x), int(self.user.y)
        else:
            px, py = self.user.rect.center
        dx, dy = self.target_pos[0] - px, self.target_pos[1] - py
        offset_dist = PLAYER_SIZE // 2 + 4
        norm = math.hypot(dx, dy)
        if norm == 0:
            norm = 1
        dir_x, dir_y = dx / norm, dy / norm
        offset_x = int(px + dir_x * offset_dist)
        offset_y = int(py + dir_y * offset_dist)
        angle = math.degrees(math.atan2(dy, dx)) % 360
        draw_frame = pygame.transform.rotate(frame, -angle)
        rect = draw_frame.get_rect(center=(offset_x, offset_y))
        hit = rect.colliderect(entity.rect)
        return hit
