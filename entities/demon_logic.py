"""
Demon Enemy Logic
Handles AI, movement, and combat behavior for demon enemies.
"""

import pygame
import math
import os
from entities.projectiles import EnemyProjectile
from utils.resource_path import resource_path
from config_images import DEMON_SPRITE_FILES, DEMON_SPRITES_BASE_PATH


class DemonEnemyLogic:
    """AI and logic for demon enemies with flying movement and projectile attacks."""
    
    FRAME_COUNTS = {
        'idle': 4,
        'flying': 4,
        'attack': 8,
        'hurt': 4,
        'death': 6,
    }
    # Frame dimensions for demon sprites
    FRAME_WIDTH = 81
    FRAME_HEIGHT = 71  # Updated to match actual sprite height
    
    # Special dimensions for death animation
    DEATH_FRAME_WIDTH = 67  # 404 / 6 frames = ~67.33, round down to 67
    DEATH_FRAME_HEIGHT = 66
    
    # Class-level sprite cache
    _sprite_cache = None

    def __init__(self, enemy):
        self.enemy = enemy
        self.state = 'idle'
        self.anim_frame = 0
        self.anim_timer = 0.0
        if DemonEnemyLogic._sprite_cache is None:
            DemonEnemyLogic._sprite_cache = self._load_sprites()
        self.sprites = DemonEnemyLogic._sprite_cache
        
        # Use attack_cooldown from type if available, else default
        self.attack_cooldown = getattr(self.enemy.type, 'attack_cooldown', 2.0)
        self.last_attack = -float('inf')
        
        # Separate cooldowns for melee and ranged attacks
        self.melee_cooldown = 1.0  # Melee attack every 1 second
        self.last_melee_attack = -float('inf')
        
        # Store fixed position during hurt/death animations to prevent jitter
        self.fixed_draw_pos = None
        
        # Hurt animation system
        self.hurt_timer = 0.0
        self.hurt_duration = 0.4  # 400ms hurt animation for demons
        
        # Track XP drop timing
        self.death_timer = 0.0
        self.xp_dropped = False
        
        # Flying movement properties
        self.hover_offset = 0.0
        self.hover_speed = 2.0  # Speed of hover oscillation
        self.base_y = enemy.position[1]  # Store original Y position
        
        # Direction tracking for sprite flipping
        self.facing_direction = 'left'  # 'left' or 'right'
        self.last_move_direction = (0, 0)  # Track last movement for direction

    def trigger_hurt_animation(self):
        """Trigger the hurt animation when the demon takes damage."""
        if self.state != 'death':  # Can't interrupt death animation
            self.state = 'hurt'
            self.anim_frame = 0
            self.anim_timer = 0.0
            self.hurt_timer = 0.0

    def _load_sprites(self):
        """Load all sprite sheets for demon animations."""
        sprites = {}
        
        for state, filename in DEMON_SPRITE_FILES.items():
            relative_path = os.path.join(DEMON_SPRITES_BASE_PATH, filename)
            full_path = resource_path(relative_path)
            if os.path.exists(full_path):
                try:
                    sprite_sheet = pygame.image.load(full_path).convert_alpha()
                    # Load both left (original) and right (flipped) versions
                    sprites[state] = {
                        'left': self._extract_frames(sprite_sheet, state),
                        'right': self._extract_frames_flipped(sprite_sheet, state)
                    }
                    print(f"[DEMON] Loaded {state} sprite: {filename}")
                except pygame.error as e:
                    print(f"[WARNING] Failed to load demon sprite {filename}: {e}")
                    sprites[state] = {'left': [], 'right': []}
            else:
                print(f"[WARNING] Demon sprite not found: {full_path}")
                sprites[state] = {'left': [], 'right': []}
        
        return sprites

    def _extract_frames(self, sprite_sheet, state):
        """Extract individual frames from a sprite sheet (left-facing, original)."""
        frames = []
        frame_count = self.FRAME_COUNTS[state]
        
        # Use special dimensions for death animation
        if state == 'death':
            frame_width = self.DEATH_FRAME_WIDTH
            frame_height = self.DEATH_FRAME_HEIGHT
        else:
            frame_width = self.FRAME_WIDTH
            frame_height = self.FRAME_HEIGHT
        
        for i in range(frame_count):
            x = i * frame_width
            y = 0
            frame_rect = pygame.Rect(x, y, frame_width, frame_height)
            
            # Check if the frame rectangle is within the sprite sheet bounds
            if (x + frame_width <= sprite_sheet.get_width() and 
                y + frame_height <= sprite_sheet.get_height()):
                frame = sprite_sheet.subsurface(frame_rect).copy()
                frames.append(frame)
            else:
                print(f"[WARNING] Frame {i} for {state} exceeds sprite sheet bounds")
                break
        
        return frames
    
    def _extract_frames_flipped(self, sprite_sheet, state):
        """Extract individual frames from a sprite sheet and flip them horizontally (right-facing)."""
        frames = []
        frame_count = self.FRAME_COUNTS[state]
        
        # Use special dimensions for death animation
        if state == 'death':
            frame_width = self.DEATH_FRAME_WIDTH
            frame_height = self.DEATH_FRAME_HEIGHT
        else:
            frame_width = self.FRAME_WIDTH
            frame_height = self.FRAME_HEIGHT
        
        for i in range(frame_count):
            x = i * frame_width
            y = 0
            frame_rect = pygame.Rect(x, y, frame_width, frame_height)
            
            # Check if the frame rectangle is within the sprite sheet bounds
            if (x + frame_width <= sprite_sheet.get_width() and 
                y + frame_height <= sprite_sheet.get_height()):
                frame = sprite_sheet.subsurface(frame_rect).copy()
                # Flip the frame horizontally for right-facing direction
                flipped_frame = pygame.transform.flip(frame, True, False)
                frames.append(flipped_frame)
            else:
                print(f"[WARNING] Frame {i} for {state} (flipped) exceeds sprite sheet bounds")
                break
        
        return frames

    def update(self, dt, player):
        """Update demon AI, movement, and combat logic."""
        now = pygame.time.get_ticks() / 1000
        
        # Update hover animation
        self.hover_offset += self.hover_speed * dt
        
        # Enemy-specific logic for attack ranges and combat
        attack_trigger_range = getattr(self.enemy.type, 'attack_range', 200)
        attack_damage = getattr(self.enemy.type, 'attack_damage', 8)

        # Check for death first - death overrides everything
        if self.enemy.health <= 0 and self.state != 'death':
            self.state = 'death'
            self.anim_frame = 0
            self.anim_timer = 0.0
            self.death_timer = 0.0  # Start death timer for XP drop
            # Fix position for death animation to prevent jitter
            self.fixed_draw_pos = (int(self.enemy.position[0]), int(self.enemy.position[1]))

        # Handle death animation - cannot be interrupted
        if self.state == 'death':
            self.death_timer += dt  # Track time since death started
            self.anim_timer += dt
            if self.anim_timer > 0.15:  # Slightly slower death animation
                self.anim_frame += 1
                self.anim_timer = 0.0
                if self.anim_frame >= self.FRAME_COUNTS['death']:
                    # Death animation complete, mark for removal
                    self.enemy.dead = True
            return  # Don't process any other logic during death

        # Handle hurt animation - can be interrupted by death
        if self.state == 'hurt':
            self.hurt_timer += dt
            self.anim_timer += dt
            if self.anim_timer > 0.1:  # Hurt animation speed
                self.anim_frame += 1
                self.anim_timer = 0.0
                if self.anim_frame >= self.FRAME_COUNTS['hurt'] or self.hurt_timer >= self.hurt_duration:
                    # Hurt animation complete, return to appropriate state
                    px, py = player.rect.center if hasattr(player, 'rect') else (player.x, player.y)
                    ex, ey = self.enemy.position
                    distance = math.hypot(px - ex, py - ey)
                    attack_trigger_range = getattr(self.enemy.type, 'attack_range', 200)
                    
                    if distance <= attack_trigger_range:
                        self.state = 'idle'
                    else:
                        self.state = 'flying'
                    self.anim_frame = 0
                    self.anim_timer = 0.0
            return  # Don't process movement logic during hurt animation

        # Normal movement and attack logic - only when not hurt or dead
        prev_state = self.state
        
        # Check if stunned - if so, don't process movement or attack logic
        if getattr(self.enemy, 'is_stunned', False):
            # When stunned, force idle state and don't process any other logic
            if self.state not in ['hurt']:  # Don't interrupt ongoing hurt animation
                self.state = 'idle'
            return  # Skip all movement and attack logic when stunned
        
        # Calculate distance to player
        px, py = player.rect.center if hasattr(player, 'rect') else (player.x, player.y)
        ex, ey = self.enemy.position
        distance = math.hypot(px - ex, py - ey)

        # Check for collision (melee range) - highest priority
        player_collision = False
        if hasattr(player, 'rect') and hasattr(self.enemy, 'rect'):
            player_collision = self.enemy.rect.colliderect(player.rect)
        
        # Attack logic - prioritize melee when colliding, then ranged
        if player_collision and now - self.last_melee_attack >= self.melee_cooldown:
            # Melee attack when colliding
            self.state = 'attack'
            self.anim_frame = 0
            self.anim_timer = 0.0
            self.last_melee_attack = now
            self._perform_melee_attack(player)
        elif distance <= attack_trigger_range and now - self.last_attack >= self.attack_cooldown and not player_collision:
            # Ranged attack when in range but not colliding
            self.state = 'attack'
            self.anim_frame = 0
            self.anim_timer = 0.0
            self.last_attack = now
            self._shoot_projectile_at_player(player)
        elif distance > attack_trigger_range:
            # Move toward player when out of attack range
            self.state = 'flying'
            self._move_toward_player(player, dt)
        else:
            # In range but on cooldown - hover in place
            self.state = 'idle'

        # Update animation frame
        self.anim_timer += dt
        if self.anim_timer > 0.12:  # Animation speed
            self.anim_frame += 1
            self.anim_timer = 0.0
            if self.state in self.FRAME_COUNTS:
                frame_count = self.FRAME_COUNTS[self.state]
                if self.anim_frame >= frame_count:
                    if self.state == 'attack':
                        # Return to appropriate state after attack
                        if distance <= attack_trigger_range:
                            self.state = 'idle'
                        else:
                            self.state = 'flying'
                    self.anim_frame = 0

    def _move_toward_player(self, player, dt):
        """Move demon toward player with flying movement."""
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
            
            # Update facing direction based on movement
            # For north/south movement, keep current facing direction
            if abs(dx) > abs(dy):  # More horizontal movement
                if dx > 0:
                    self.facing_direction = 'right'
                else:
                    self.facing_direction = 'left'
            # For vertical movement, don't change facing direction
            
            # Store last move direction
            self.last_move_direction = (nx, ny)
            
            # Apply movement with flying behavior
            speed = getattr(self.enemy, 'movement_speed', self.enemy.type.speed)
            
            # Add hovering motion (vertical oscillation)
            hover_amplitude = 10  # Pixels of hover
            hover_y = math.sin(self.hover_offset) * hover_amplitude
            
            # Move toward player
            new_x = ex + nx * speed * dt
            new_y = ey + ny * speed * dt + hover_y * dt
            
            self.enemy.position = (new_x, new_y)
            self.enemy.x = new_x
            self.enemy.y = new_y
            self.enemy.rect.center = (int(new_x), int(new_y))

    def _shoot_projectile_at_player(self, player):
        """Fire a projectile at the player."""
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
            
            # Get game instance to access projectile manager
            # We need to find a way to access the game's projectile manager
            # For now, we'll add a reference to the enemy
            if hasattr(self.enemy, 'game') and hasattr(self.enemy.game, 'projectile_manager'):
                # Calculate target position
                start_pos = self.enemy.position
                target_pos = (px, py)
                
                # Create projectile
                projectile_speed = getattr(self.enemy.type, 'projectile_speed', 150)
                projectile_damage = getattr(self.enemy.type, 'projectile_damage', 8)
                
                projectile = EnemyProjectile(start_pos, target_pos, projectile_speed, projectile_damage, self.enemy)
                self.enemy.game.projectile_manager.add_projectile(projectile)
                
                print(f"[DEMON] Fired projectile at player")
        except Exception as e:
            print(f"[WARNING] Failed to shoot projectile: {e}")

    def _perform_melee_attack(self, player):
        """Perform a melee attack on the player when colliding."""
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
            
            # Deal direct damage to player (melee attack)
            melee_damage = getattr(self.enemy.type, 'attack_damage', 8)
            if hasattr(player, 'take_damage'):
                player.take_damage(melee_damage, source="Demon Melee")
                print(f"[DEMON] Melee attack hit player for {melee_damage} damage")
        except Exception as e:
            print(f"[WARNING] Failed to perform melee attack: {e}")

    def get_current_sprite(self):
        """Get the current sprite frame for rendering."""
        if self.state not in self.sprites:
            return None
        
        direction_sprites = self.sprites[self.state]
        if self.facing_direction not in direction_sprites or not direction_sprites[self.facing_direction]:
            return None
        
        frames = direction_sprites[self.facing_direction]
        if not frames:
            return None
        
        frame_index = min(self.anim_frame, len(frames) - 1)
        return frames[frame_index]

    def get_draw_position(self):
        """Get position for drawing (fixed during death/hurt animations)."""
        if self.fixed_draw_pos:
            # Use fixed position during death animations to prevent jitter
            return self.fixed_draw_pos
        else:
            # Use current position
            return (int(self.enemy.position[0]), int(self.enemy.position[1]))

    def draw(self, surface, camera=None):
        """Draw the demon with proper directional sprites."""
        sprite = self.get_current_sprite()
        if not sprite:
            # Fallback to debug circle if no sprite available
            if camera:
                screen_x, screen_y = camera.world_to_screen(self.enemy.position[0], self.enemy.position[1])
            else:
                screen_x, screen_y = int(self.enemy.position[0]), int(self.enemy.position[1])
            pygame.draw.circle(surface, self.enemy.color, (screen_x, screen_y), 35)
            return
        
        # Get position (use fixed position during death animations)
        draw_x, draw_y = self.get_draw_position()
        
        # Apply camera transformation
        if camera:
            screen_x, screen_y = camera.world_to_screen(draw_x, draw_y)
        else:
            screen_x, screen_y = draw_x, draw_y
        
        # Draw the sprite centered on the demon position
        sprite_rect = sprite.get_rect(center=(screen_x, screen_y))
        surface.blit(sprite, sprite_rect)
