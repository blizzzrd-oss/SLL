"""
Pickable System
Base classes and implementations for collectible items.
"""

import pygame
import math
import os
from abc import ABC, abstractmethod
from config import (
    REROLL_DICE_SPRITE, REROLL_DICE_FRAME_SIZE, REROLL_DICE_FRAME_COUNT,
    REROLL_DICE_ANIMATION_FPS, REROLL_DICE_REROLL_CHARGES,
    XP_GREEN_SPRITE, XP_GREEN_FRAME_SIZE, XP_GREEN_FRAME_COUNT, 
    XP_GREEN_ANIMATION_FPS, XP_GREEN_XP_VALUE,
    PICKABLE_DESPAWN_TIME, PICKABLE_FLOAT_HEIGHT, PICKABLE_FLOAT_SPEED
)
from utils.resource_path import resource_path
from audio.sound_manager import SoundManager


class Pickable(ABC):
    """Base class for all pickable items."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x - 8, y - 8, 16, 16)  # Default 16x16 collision
        self.spawn_time = pygame.time.get_ticks() / 1000
        self.float_timer = 0.0
        self.collected = False
        
    def update(self, dt):
        """Update pickable state (floating animation, despawn timer)."""
        self.float_timer += dt
        
        # Check if expired
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.spawn_time > PICKABLE_DESPAWN_TIME:
            return False  # Signal for removal
            
        return True  # Continue existing
        
    def get_render_position(self):
        """Get the floating render position."""
        float_offset = math.sin(self.float_timer * PICKABLE_FLOAT_SPEED) * PICKABLE_FLOAT_HEIGHT
        return (self.x, self.y - float_offset)
        
    def is_in_collection_range(self, player):
        """Check if player is close enough to collect this pickable."""
        player_center = (player.x, player.y)
        pickable_center = (self.x, self.y)
        distance = math.hypot(
            player_center[0] - pickable_center[0],
            player_center[1] - pickable_center[1]
        )
        # Use player's pickup range (includes enhancements)
        player_pickup_range = player.get_pickup_range()
        return distance <= player_pickup_range
        
    @abstractmethod
    def collect(self, player):
        """Apply the pickable's effect to the player."""
        pass
        
    @abstractmethod
    def draw(self, surface, camera=None):
        """Draw the pickable."""
        pass


class RerollDicePickable(Pickable):
    """Pickable that grants enhancement reroll charges."""
    
    # Class-level sprite cache
    _frames = None
    _loaded = False
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.animation_timer = 0.0
        self._load_sprites()
        
    @classmethod
    def _load_sprites(cls):
        """Load and cache sprite frames."""
        if cls._loaded:
            return
            
        try:
            sprite_path = resource_path(REROLL_DICE_SPRITE)
            if os.path.exists(sprite_path):
                sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
                cls._frames = []
                
                # Extract frames (assuming horizontal layout)
                for i in range(REROLL_DICE_FRAME_COUNT):
                    frame_x = i * REROLL_DICE_FRAME_SIZE
                    frame_rect = (frame_x, 0, REROLL_DICE_FRAME_SIZE, REROLL_DICE_FRAME_SIZE)
                    frame = sprite_sheet.subsurface(frame_rect)
                    cls._frames.append(frame)
                    
                print(f"[PICKABLES] Loaded {len(cls._frames)} reroll dice frames")
            else:
                print(f"[PICKABLES] Sprite not found: {sprite_path}")
                # Create placeholder frames
                cls._frames = []
                for i in range(REROLL_DICE_FRAME_COUNT):
                    placeholder = pygame.Surface((REROLL_DICE_FRAME_SIZE, REROLL_DICE_FRAME_SIZE))
                    placeholder.fill((100 + i * 20, 50, 200))  # Different colors for each frame
                    cls._frames.append(placeholder)
                    
        except Exception as e:
            print(f"[PICKABLES] Error loading reroll dice sprite: {e}")
            # Create placeholder frames
            cls._frames = []
            for i in range(REROLL_DICE_FRAME_COUNT):
                placeholder = pygame.Surface((REROLL_DICE_FRAME_SIZE, REROLL_DICE_FRAME_SIZE))
                placeholder.fill((100 + i * 20, 50, 200))
                cls._frames.append(placeholder)
                
        cls._loaded = True
        
    def update(self, dt):
        """Update animation and base pickable behavior."""
        if not super().update(dt):
            return False
            
        self.animation_timer += dt
        return True
        
    def collect(self, player):
        """Grant reroll charges to the player."""
        if hasattr(player, 'enhancement_ui') and player.enhancement_ui:
            player.enhancement_ui.add_reroll_charges(REROLL_DICE_REROLL_CHARGES)
        
        # Play collection sound
        try:
            SoundManager.play_pickable_collect_sound()
        except Exception as e:
            print(f"[PICKABLES] Failed to play collection sound: {e}")
            
        print(f"[PICKABLES] Player collected reroll dice! Gained {REROLL_DICE_REROLL_CHARGES} reroll charge(s)")
        self.collected = True
        
    def draw(self, surface, camera=None):
        """Draw the animated reroll dice."""
        if not self._frames:
            return
            
        # Calculate current frame
        frame_index = int(self.animation_timer * REROLL_DICE_ANIMATION_FPS) % len(self._frames)
        current_frame = self._frames[frame_index]
        
        # Get floating position
        render_x, render_y = self.get_render_position()
        
        # Apply camera transformation
        if camera:
            screen_x, screen_y = camera.world_to_screen(render_x, render_y)
        else:
            screen_x, screen_y = int(render_x), int(render_y)
            
        # Center the sprite
        rect = current_frame.get_rect(center=(screen_x, screen_y))
        surface.blit(current_frame, rect)


class XpPickable(Pickable):
    """XP crystal pickable that grants experience points."""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self._frames = []
        self.animation_timer = 0.0  # Added missing animation timer
        self.xp_value = XP_GREEN_XP_VALUE
        self._load_sprite_frames()
    
    def _load_sprite_frames(self):
        """Load and split the animated XP crystal sprite."""
        try:
            full_path = resource_path(XP_GREEN_SPRITE)
            if os.path.exists(full_path):
                sprite_sheet = pygame.image.load(full_path).convert_alpha()
                
                # Split sprite sheet into individual frames
                frame_width, frame_height = XP_GREEN_FRAME_SIZE
                for i in range(XP_GREEN_FRAME_COUNT):
                    frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
                    frame = sprite_sheet.subsurface(frame_rect).copy()
                    self._frames.append(frame)
                
                print(f"[PICKABLES] Loaded {len(self._frames)} XP crystal frames")
            else:
                print(f"[WARNING] XP crystal sprite not found: {full_path}")
                self._create_fallback_frames()
        except Exception as e:
            print(f"[WARNING] Failed to load XP crystal sprite: {e}")
            self._create_fallback_frames()
    
    def _create_fallback_frames(self):
        """Create fallback green frames if sprite loading fails."""
        frame_width, frame_height = XP_GREEN_FRAME_SIZE
        for i in range(XP_GREEN_FRAME_COUNT):
            frame = pygame.Surface((frame_width, frame_height))
            # Create slightly different shades of green for animation effect
            green_value = 200 + (i * 10)  # Vary brightness
            frame.fill((0, min(255, green_value), 0))
            self._frames.append(frame)
    
    def update(self, dt):
        """Update animation and base pickable behavior."""
        if not super().update(dt):
            return False
            
        self.animation_timer += dt
        return True
    
    def collect(self, player):
        """Grant XP to the player."""
        # Give XP directly to player
        player.add_experience(self.xp_value)
        
        # Play collection sound
        try:
            SoundManager.play_pickable_collect_sound()
        except Exception as e:
            print(f"[PICKABLES] Failed to play collection sound: {e}")
            
        print(f"[PICKABLES] Player collected XP crystal! Gained {self.xp_value} XP")
        self.collected = True
        
    def draw(self, surface, camera=None):
        """Draw the animated XP crystal."""
        if not self._frames:
            return
            
        # Calculate current frame
        frame_index = int(self.animation_timer * XP_GREEN_ANIMATION_FPS) % len(self._frames)
        current_frame = self._frames[frame_index]
        
        # Get floating position
        render_x, render_y = self.get_render_position()
        
        # Apply camera transformation
        if camera:
            screen_x, screen_y = camera.world_to_screen(render_x, render_y)
        else:
            screen_x, screen_y = int(render_x), int(render_y)
            
        # Center the sprite
        rect = current_frame.get_rect(center=(screen_x, screen_y))
        surface.blit(current_frame, rect)


class PickableManager:
    """Manages all pickables in the game."""
    
    def __init__(self):
        self.pickables = []
        
    def add_pickable(self, pickable):
        """Add a pickable to the manager."""
        self.pickables.append(pickable)
        
    def create_reroll_dice(self, x, y):
        """Create a reroll dice pickable at the specified position."""
        dice = RerollDicePickable(x, y)
        self.add_pickable(dice)
        
        # Play drop sound
        try:
            SoundManager.play_pickable_drop_sound()
        except Exception as e:
            print(f"[PICKABLES] Failed to play drop sound: {e}")
            
        return dice
        
    def create_xp_pickable(self, x, y):
        """Create an XP crystal pickable at the specified position."""
        xp_crystal = XpPickable(x, y)
        self.add_pickable(xp_crystal)
        
        # Play drop sound
        try:
            SoundManager.play_pickable_drop_sound()
        except Exception as e:
            print(f"[PICKABLES] Failed to play drop sound: {e}")
            
        return xp_crystal
        
    def update(self, dt, player):
        """Update all pickables and handle collection."""
        pickables_to_remove = []
        
        for pickable in self.pickables:
            # Update pickable
            if not pickable.update(dt):
                pickables_to_remove.append(pickable)
                continue
                
            # Check for collection
            if not pickable.collected and pickable.is_in_collection_range(player):
                pickable.collect(player)
                pickables_to_remove.append(pickable)
                
        # Remove collected/expired pickables
        for pickable in pickables_to_remove:
            if pickable in self.pickables:
                self.pickables.remove(pickable)
                
    def draw(self, surface, camera=None):
        """Draw all pickables."""
        for pickable in self.pickables:
            if not pickable.collected:
                pickable.draw(surface, camera)
                
    def clear_all(self):
        """Clear all pickables (useful for game reset)."""
        self.pickables.clear()
