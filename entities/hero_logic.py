"""
Hero Enemy Logic
Handles AI, movement, and combat behavior for hero enemies.
Features melee combat with blocking mechanics.
"""

import pygame
import math
import os
import random
from utils.resource_path import resource_path
from config_images import HERO_SPRITE_FILES, HERO_SPRITES_BASE_PATH, HERO_FRAME_COUNTS


class HeroEnemyLogic:
    """AI and logic for hero enemies with melee combat and blocking mechanics."""
    
    # Frame dimensions for hero sprites
    FRAME_WIDTH = 56
    FRAME_HEIGHT = 56
    
    # Class-level sprite cache
    _sprite_cache = None

    def __init__(self, enemy):
        self.enemy = enemy
        self.state = 'idle'
        self.anim_frame = 0
        self.anim_timer = 0.0
        if HeroEnemyLogic._sprite_cache is None:
            HeroEnemyLogic._sprite_cache = self._load_sprites()
        self.sprites = HeroEnemyLogic._sprite_cache
        
        # Combat properties
        self.attack_cooldown = 1.5  # Melee attack every 1.5 seconds
        self.last_attack = -float('inf')
        self.attack_range = 40  # Close melee range
        
        # Blocking system
        self.block_chance = getattr(self.enemy.type, 'block_chance', 0.3)  # 30% block chance
        self.blocking = False
        self.block_timer = 0.0
        self.block_duration = 0.5  # Hold block animation for 0.5 seconds
        
        # Store fixed position during hurt/death animations to prevent jitter
        self.fixed_draw_pos = None
        
        # Hurt animation system
        self.hurt_timer = 0.0
        self.hurt_duration = 0.4  # 400ms hurt animation
        
        # Track XP drop timing
        self.death_timer = 0.0
        self.xp_dropped = False
        
        # Direction tracking for sprite flipping
        self.facing_direction = 'left'  # 'left' or 'right'
        self.last_move_direction = (0, 0)  # Track last movement for direction

    def trigger_hurt_animation(self):
        """Trigger the hurt animation when the hero takes damage."""
        # Cannot block while attacking
        if self.state == 'attack':
            # Cannot block during attack animation - take damage normally
            if self.state != 'death':
                self.state = 'hurt'
                self.anim_frame = 0
                self.anim_timer = 0.0
                self.hurt_timer = 0.0
                self.blocking = False
            return False  # Damage was not blocked
        
        # Check if blocking - 30% chance to block damage (only when not attacking)
        if not self.blocking and random.random() < self.block_chance:
            self.blocking = True
            self.state = 'block'
            self.anim_frame = 0
            self.anim_timer = 0.0
            self.block_timer = 0.0
            print(f"[HERO] Blocked attack!")
            return True  # Indicate damage was blocked
        elif self.state != 'death':  # Can't interrupt death animation
            self.state = 'hurt'
            self.anim_frame = 0
            self.anim_timer = 0.0
            self.hurt_timer = 0.0
            self.blocking = False
            return False  # Damage was not blocked

    def _load_sprites(self):
        """Load all sprite sheets for hero animations."""
        sprites = {}
        
        for state, filename in HERO_SPRITE_FILES.items():
            relative_path = os.path.join(HERO_SPRITES_BASE_PATH, filename)
            full_path = resource_path(relative_path)
            if os.path.exists(full_path):
                try:
                    sprite_sheet = pygame.image.load(full_path).convert_alpha()
                    # Load both left (flipped) and right (original) versions
                    # Hero sprites are originally right-facing, so we flip for left
                    sprites[state] = {
                        'left': self._extract_frames_flipped(sprite_sheet, state),
                        'right': self._extract_frames(sprite_sheet, state)
                    }
                    print(f"[HERO] Loaded {state} sprite: {filename}")
                except pygame.error as e:
                    print(f"[WARNING] Failed to load hero sprite {filename}: {e}")
                    sprites[state] = {'left': [], 'right': []}
            else:
                print(f"[WARNING] Hero sprite not found: {full_path}")
                sprites[state] = {'left': [], 'right': []}
        
        return sprites

    def _extract_frames(self, sprite_sheet, state):
        """Extract individual frames from a sprite sheet (left-facing, original)."""
        frames = []
        frame_count = HERO_FRAME_COUNTS[state]
        
        for i in range(frame_count):
            x = i * self.FRAME_WIDTH
            y = 0
            frame_rect = pygame.Rect(x, y, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            
            # Check if the frame rectangle is within the sprite sheet bounds
            if (x + self.FRAME_WIDTH <= sprite_sheet.get_width() and 
                y + self.FRAME_HEIGHT <= sprite_sheet.get_height()):
                frame = sprite_sheet.subsurface(frame_rect).copy()
                frames.append(frame)
            else:
                print(f"[WARNING] Frame {i} for {state} exceeds sprite sheet bounds")
                break
        
        return frames
    
    def _extract_frames_flipped(self, sprite_sheet, state):
        """Extract individual frames from a sprite sheet and flip them horizontally (right-facing)."""
        frames = []
        frame_count = HERO_FRAME_COUNTS[state]
        
        for i in range(frame_count):
            x = i * self.FRAME_WIDTH
            y = 0
            frame_rect = pygame.Rect(x, y, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            
            # Check if the frame rectangle is within the sprite sheet bounds
            if (x + self.FRAME_WIDTH <= sprite_sheet.get_width() and 
                y + self.FRAME_HEIGHT <= sprite_sheet.get_height()):
                frame = sprite_sheet.subsurface(frame_rect).copy()
                # Flip the frame horizontally for right-facing direction
                flipped_frame = pygame.transform.flip(frame, True, False)
                frames.append(flipped_frame)
            else:
                print(f"[WARNING] Frame {i} for {state} (flipped) exceeds sprite sheet bounds")
                break
        
        return frames

    def update(self, dt, player):
        """Update hero AI, movement, and combat logic."""
        now = pygame.time.get_ticks() / 1000
        
        # Check for death first - death overrides everything
        if self.enemy.health <= 0 and self.state != 'death':
            self.state = 'death'
            self.anim_frame = 0
            self.anim_timer = 0.0
            self.death_timer = 0.0  # Start death timer for XP drop
            self.blocking = False
            # Fix position for death animation to prevent jitter
            self.fixed_draw_pos = (int(self.enemy.position[0]), int(self.enemy.position[1]))

        # Handle death animation - cannot be interrupted
        if self.state == 'death':
            self.death_timer += dt  # Track time since death started
            self.anim_timer += dt
            if self.anim_timer > 0.1:  # 100ms animation speed
                self.anim_frame += 1
                self.anim_timer = 0.0
                if self.anim_frame >= HERO_FRAME_COUNTS['death']:
                    # Death animation complete, mark for removal
                    self.enemy.dead = True
            return  # Don't process any other logic during death

        # Handle blocking animation
        if self.state == 'block':
            self.block_timer += dt
            self.anim_timer += dt
            if self.anim_timer > 0.1:  # 100ms animation speed
                self.anim_frame += 1
                self.anim_timer = 0.0
                if self.anim_frame >= HERO_FRAME_COUNTS['block'] or self.block_timer >= self.block_duration:
                    # Block animation complete, return to appropriate state
                    self.blocking = False
                    px, py = player.rect.center if hasattr(player, 'rect') else (player.x, player.y)
                    ex, ey = self.enemy.position
                    distance = math.hypot(px - ex, py - ey)
                    
                    if distance <= self.attack_range:
                        self.state = 'idle'
                    else:
                        self.state = 'walk'
                    self.anim_frame = 0
                    self.anim_timer = 0.0
            return  # Don't process movement logic during block animation

        # Handle hurt animation - can be interrupted by death
        if self.state == 'hurt':
            self.hurt_timer += dt
            self.anim_timer += dt
            if self.anim_timer > 0.1:  # 100ms animation speed
                self.anim_frame += 1
                self.anim_timer = 0.0
                if self.anim_frame >= HERO_FRAME_COUNTS['hurt'] or self.hurt_timer >= self.hurt_duration:
                    # Hurt animation complete, return to appropriate state
                    px, py = player.rect.center if hasattr(player, 'rect') else (player.x, player.y)
                    ex, ey = self.enemy.position
                    distance = math.hypot(px - ex, py - ey)
                    
                    if distance <= self.attack_range:
                        self.state = 'idle'
                    else:
                        self.state = 'walk'
                    self.anim_frame = 0
                    self.anim_timer = 0.0
            return  # Don't process movement logic during hurt animation

        # Handle attack animation - cannot be interrupted by blocking
        if self.state == 'attack':
            self.anim_timer += dt
            if self.anim_timer > 0.1:  # 100ms animation speed
                self.anim_frame += 1
                self.anim_timer = 0.0
                if self.anim_frame >= HERO_FRAME_COUNTS['attack']:
                    # Attack animation complete, return to appropriate state
                    px, py = player.rect.center if hasattr(player, 'rect') else (player.x, player.y)
                    ex, ey = self.enemy.position
                    distance = math.hypot(px - ex, py - ey)
                    
                    if distance <= self.attack_range:
                        self.state = 'idle'
                    else:
                        self.state = 'walk'
                    self.anim_frame = 0
                    self.anim_timer = 0.0
            return  # Don't process movement or blocking logic during attack animation

        # Normal movement and attack logic - only when not in special states
        prev_state = self.state
        
        # Calculate distance to player
        px, py = player.rect.center if hasattr(player, 'rect') else (player.x, player.y)
        ex, ey = self.enemy.position
        distance = math.hypot(px - ex, py - ey)

        # Attack logic - melee attack when in range (but not when blocking)
        if (distance <= self.attack_range and 
            now - self.last_attack >= self.attack_cooldown and 
            not self.blocking and 
            self.state != 'block'):
            # Melee attack when in range and not blocking
            self.state = 'attack'
            self.anim_frame = 0
            self.anim_timer = 0.0
            self.last_attack = now
            self._perform_melee_attack(player)
        elif distance > self.attack_range and not self.blocking:
            # Move toward player when out of attack range and not blocking
            self.state = 'walk'
            self._move_toward_player(player, dt)
        elif not self.blocking:
            # In range but on cooldown or other reason - stay idle (but not blocking)
            self.state = 'idle'

        # Update animation frame for idle and walk states
        if self.state in ['idle', 'walk']:
            self.anim_timer += dt
            if self.anim_timer > 0.1:  # 100ms animation speed
                self.anim_frame += 1
                self.anim_timer = 0.0
                if self.state in HERO_FRAME_COUNTS:
                    frame_count = HERO_FRAME_COUNTS[self.state]
                    if self.anim_frame >= frame_count:
                        self.anim_frame = 0

    def _move_toward_player(self, player, dt):
        """Move hero toward player with ground movement."""
        px, py = player.rect.center if hasattr(player, 'rect') else (player.x, player.y)
        ex, ey = self.enemy.position
        
        # Calculate direction to player
        dx = px - ex
        dy = py - ey
        distance = math.hypot(dx, dy)
        
        if distance > 0:
            # Normalize direction
            nx = dx / distance
            ny = dy / distance
            
            # Update facing direction based on horizontal movement direction
            # Always update if there's any horizontal movement
            if dx > 0:
                self.facing_direction = 'right'
            elif dx < 0:
                self.facing_direction = 'left'
            # If dx == 0 (purely vertical movement), keep current facing direction
            
            # Store last move direction
            self.last_move_direction = (nx, ny)
            
            # Apply movement (ground-based, no hovering)
            speed = getattr(self.enemy, 'movement_speed', self.enemy.type.speed)
            
            # Move toward player
            new_x = ex + nx * speed * dt
            new_y = ey + ny * speed * dt
            
            self.enemy.position = (new_x, new_y)
            self.enemy.x = new_x
            self.enemy.y = new_y
            self.enemy.rect.center = (int(new_x), int(new_y))

    def _perform_melee_attack(self, player):
        """Perform a melee attack on the player when in range."""
        try:
            # Update facing direction when attacking
            px, py = player.rect.center if hasattr(player, 'rect') else (player.x, player.y)
            ex, ey = self.enemy.position
            dx = px - ex
            
            # Set facing direction based on target
            if dx > 0:
                self.facing_direction = 'right'
            else:
                self.facing_direction = 'left'
            
            # Deal damage to player
            damage = getattr(self.enemy.type, 'attack_damage', 10)
            if hasattr(player, 'take_damage'):
                player.take_damage(damage, source='Hero Melee')
                print(f"[HERO] Performed melee attack for {damage} damage")
        except Exception as e:
            print(f"[WARNING] Failed to perform melee attack: {e}")

    def draw(self, surface, camera=None):
        """Draw the hero enemy sprite."""
        try:
            # Use fixed position during death animation, otherwise current position
            if self.fixed_draw_pos:
                draw_x, draw_y = self.fixed_draw_pos
            else:
                draw_x, draw_y = int(self.enemy.position[0]), int(self.enemy.position[1])
            
            # Apply camera transformation
            if camera:
                screen_x, screen_y = camera.world_to_screen(draw_x, draw_y)
            else:
                screen_x, screen_y = draw_x, draw_y
            
            # Get current animation state and frame
            current_state = self.state if self.state in self.sprites else 'idle'
            direction = self.facing_direction
            
            if (current_state in self.sprites and 
                direction in self.sprites[current_state] and 
                self.sprites[current_state][direction]):
                
                frames = self.sprites[current_state][direction]
                if frames and self.anim_frame < len(frames):
                    frame = frames[self.anim_frame]
                    # Center the sprite on the enemy position
                    rect = frame.get_rect(center=(screen_x, screen_y))
                    surface.blit(frame, rect)
                else:
                    # Fallback to first frame if animation frame is out of bounds
                    if frames:
                        frame = frames[0]
                        rect = frame.get_rect(center=(screen_x, screen_y))
                        surface.blit(frame, rect)
            else:
                # Fallback to debug circle if sprites not available
                pygame.draw.circle(surface, (100, 100, 255), (screen_x, screen_y), 20)
        except Exception as e:
            print(f"[WARNING] Failed to draw hero sprite: {e}")
            # Emergency fallback
            if camera:
                screen_x, screen_y = camera.world_to_screen(self.enemy.position[0], self.enemy.position[1])
            else:
                screen_x, screen_y = int(self.enemy.position[0]), int(self.enemy.position[1])
            pygame.draw.circle(surface, (100, 100, 255), (screen_x, screen_y), 20)
