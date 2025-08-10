import pygame
import os


class PlantEnemyLogic:
    """
    Handles movement, animation, and attack logic for Plant enemies.
    """
    SPRITE_PATH = os.path.join('resources', 'images', 'enemies', 'Plant')
    ANIMATIONS = {
        'idle': 'Plant_Idle_full.png',
        'walk': 'Plant_Walk_full.png',
        'run': 'Plant_Run_full.png',
        'death': 'Plant_Death_full.png',
        'attack': 'Plant_Attack_full.png',
    }
    FRAME_COUNTS = {
        'idle': 8,  # 256px / 8 = 32px per frame
        'walk': 6,  # Updated: 6 frames per direction
        'run': 8,
        'death': 10,  # Updated: 10 frames per direction
        'attack': 7,  # 448px / 7 = 64px per frame
    }
    # Class-level sprite cache
    _sprite_cache = None

    def __init__(self, enemy):
        self.enemy = enemy
        self.state = 'idle'
        self.anim_frame = 0
        self.anim_timer = 0.0
        if PlantEnemyLogic._sprite_cache is None:
            PlantEnemyLogic._sprite_cache = self._load_sprites()
        self.sprites = PlantEnemyLogic._sprite_cache
        # Use attack_cooldown from type if available, else default
        self.attack_cooldown = getattr(self.enemy.type, 'attack_cooldown', 1.0)
        self.last_attack = -float('inf')
        
        # Store fixed position during hurt/death animations to prevent jitter
        self.fixed_draw_pos = None
        
        # Hurt overlay system (instead of hurt state)
        self.hurt_overlay_timer = 0.0
        self.hurt_overlay_duration = 0.5  # 500ms red tint

    def _load_sprites(self):
        sprites = {}
        directions = 4  # Down, Up, Left, Right (top to bottom in image)
        
        # Use a fixed standard frame size for ALL animations
        STANDARD_FRAME_WIDTH = 64
        STANDARD_FRAME_HEIGHT = 64
        
        for state, fname in self.ANIMATIONS.items():
            path = os.path.join(self.SPRITE_PATH, fname)
            
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                frame_count = self.FRAME_COUNTS[state]
                img_w, img_h = img.get_width(), img.get_height()
                
                if img_w % frame_count == 0 and img_h % directions == 0:
                    w = img_w // frame_count
                    h = img_h // directions
                    
                    # 2D list: sprites[state][direction][frame]
                    sprites[state] = []
                    
                    for d in range(directions):
                        row = []
                        for i in range(frame_count):
                            left = i * w
                            top = d * h
                            
                            if left + w <= img_w and top + h <= img_h:
                                # Extract the original frame
                                original_frame = img.subsurface((left, top, w, h))
                                
                                # Create a standardized surface
                                standard_surface = pygame.Surface((STANDARD_FRAME_WIDTH, STANDARD_FRAME_HEIGHT), pygame.SRCALPHA)
                                
                                # Center the original frame in the standard surface
                                offset_x = (STANDARD_FRAME_WIDTH - w) // 2
                                offset_y = STANDARD_FRAME_HEIGHT - h  # Bottom align
                                standard_surface.blit(original_frame, (offset_x, offset_y))
                                
                                row.append(standard_surface)
                        sprites[state].append(row)
                else:
                    print(f"[SPRITE ERROR] {state}: Invalid dimensions {img_w}x{img_h}, frames={frame_count}, dirs={directions}")
                    sprites[state] = [[] for _ in range(directions)]
            else:
                print(f"[SPRITE ERROR] {state}: File not found: {path}")
                sprites[state] = [[] for _ in range(directions)]
        
        return sprites

    def update(self, dt, player):
        # Movement towards player
        dx = player.position[0] - self.enemy.position[0]
        dy = player.position[1] - self.enemy.position[1]
        dist = (dx**2 + dy**2) ** 0.5
        speed = self.enemy.type.speed
        # Map movement to sprite row: 0=down, 1=up, 2=left, 3=right
        if abs(dx) > abs(dy):
            if dx > 0:
                direction = 3  # right
            else:
                direction = 2  # left
        else:
            if dy > 0:
                direction = 0  # down
            else:
                direction = 1  # up
        self.direction = direction
        now = pygame.time.get_ticks() / 1000
        attack_trigger_range = 40
        attack_damage_range = 25
        attack_frames = self.FRAME_COUNTS['attack']
        impact_frame = attack_frames // 2

        # Check for death first - death overrides everything
        if self.enemy.health <= 0 and self.state != 'death':
            self.state = 'death'
            self.anim_frame = 0
            self.anim_timer = 0.0
            # Fix position for death animation to prevent jitter
            self.fixed_draw_pos = (int(self.enemy.position[0]), int(self.enemy.position[1]))

        # Handle death animation - cannot be interrupted
        if self.state == 'death':
            self.anim_timer += dt
            if self.anim_timer > 0.1:
                self.anim_frame += 1
                self.anim_timer = 0.0
                if self.anim_frame >= self.FRAME_COUNTS['death']:
                    # Death animation complete, mark for removal
                    self.enemy.dead = True
            return  # Don't process any other logic during death

        # Update hurt overlay timer
        if self.hurt_overlay_timer > 0:
            self.hurt_overlay_timer -= dt

        # Normal movement and attack logic - only when not hurt or dead
        prev_state = self.state
        # Always move toward player unless dead or hurt
        min_dist = attack_damage_range
        if dist > min_dist:
            move_x = dx / dist
            move_y = dy / dist
            self.enemy.position = (
                self.enemy.position[0] + move_x * speed * dt,
                self.enemy.position[1] + move_y * speed * dt
            )
            self.enemy.rect.center = (int(self.enemy.position[0]), int(self.enemy.position[1]))
        
        # Set movement state unless attacking
        if self.state != 'attack':
            new_state = 'run' if speed > 4 else 'walk'
            if self.state != new_state:
                self.state = new_state
        
        # Only reset animation if state actually changed
        if self.state != prev_state:
            self.anim_frame = 0
            self.anim_timer = 0.0

        # Attack logic
        if self.state == 'attack':
            # On impact frame, deal damage if player is in range and not already hit
            impact_frame = 3
            if self.anim_frame == impact_frame and not getattr(self, '_damage_dealt', False):
                if dist < attack_damage_range:
                    player.take_damage(5, source=self.enemy)
                self._damage_dealt = True
            # After animation, return to movement and set cooldown
            if self.anim_frame >= attack_frames - 1:
                self.state = 'run' if speed > 4 else 'walk'
                self._damage_dealt = False
                self.last_attack = now
                self.anim_frame = 0
                self.anim_timer = 0.0
        elif self.state != 'attack' and dist < attack_trigger_range and (now - self.last_attack > self.attack_cooldown):
            # Start attack animation
            self.state = 'attack'
            self.anim_frame = 0
            self.anim_timer = 0.0
            self._damage_dealt = False
        
        # Animation update for normal states (walk/run/attack)
        if self.state in ['walk', 'run', 'attack']:
            self.anim_timer += dt
            frames = self.FRAME_COUNTS[self.state]
            if self.anim_timer > 0.1:
                if self.state == 'attack':
                    # Attack animation doesn't loop
                    if self.anim_frame < frames - 1:
                        self.anim_frame += 1
                else:
                    # Movement animations loop
                    self.anim_frame = (self.anim_frame + 1) % frames
                self.anim_timer = 0.0

    def draw(self, surface):
        # Use direction-aware sprites
        state_sprites = self.sprites.get(self.state, [[] for _ in range(4)])
        direction = getattr(self, 'direction', 0)
        frame_list = state_sprites[direction] if direction < len(state_sprites) else []
        
        if frame_list:
            frame_idx = min(self.anim_frame, len(frame_list) - 1)
            frame = frame_list[frame_idx]
            
            # Use fixed position during death animations to prevent jitter
            if self.fixed_draw_pos is not None:
                enemy_center_x, enemy_center_y = self.fixed_draw_pos
            else:
                enemy_center_x = int(self.enemy.position[0])
                enemy_center_y = int(self.enemy.position[1])
            
            # Since all frames are now 64x64 and bottom-aligned, positioning is consistent
            rect = frame.get_rect()
            rect.centerx = enemy_center_x
            rect.bottom = enemy_center_y + (self.enemy.size // 2)
            
            # Apply hurt overlay if active
            if self.hurt_overlay_timer > 0:
                # Create a red-tinted version of the frame
                hurt_frame = frame.copy()
                # Create red overlay surface
                red_overlay = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
                red_overlay.fill((255, 100, 100, 128))  # Red with transparency
                hurt_frame.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                surface.blit(hurt_frame, rect)
            else:
                surface.blit(frame, rect)
