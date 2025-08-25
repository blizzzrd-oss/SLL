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
    XP_YELLOW_SPRITE, XP_YELLOW_FRAME_SIZE, XP_YELLOW_FRAME_COUNT,
    XP_YELLOW_ANIMATION_FPS, XP_YELLOW_XP_VALUE,
    XP_LIGHT_BLUE_SPRITE, XP_LIGHT_BLUE_FRAME_SIZE, XP_LIGHT_BLUE_FRAME_COUNT,
    XP_LIGHT_BLUE_ANIMATION_FPS, XP_LIGHT_BLUE_XP_VALUE,
    XP_BLUE_SPRITE, XP_BLUE_FRAME_SIZE, XP_BLUE_FRAME_COUNT,
    XP_BLUE_ANIMATION_FPS, XP_BLUE_XP_VALUE,
    XP_RED_SPRITE, XP_RED_FRAME_SIZE, XP_RED_FRAME_COUNT,
    XP_RED_ANIMATION_FPS, XP_RED_XP_VALUE,
    XP_PURPLE_SPRITE, XP_PURPLE_FRAME_SIZE, XP_PURPLE_FRAME_COUNT,
    XP_PURPLE_ANIMATION_FPS, XP_PURPLE_XP_VALUE,
    XP_PLANT_GREEN_CHANCE, XP_PLANT_YELLOW_CHANCE,
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
    
    # Crystal type configurations
    CRYSTAL_TYPES = {
        'green': {
            'sprite': XP_GREEN_SPRITE,
            'frame_size': XP_GREEN_FRAME_SIZE,
            'frame_count': XP_GREEN_FRAME_COUNT,
            'animation_fps': XP_GREEN_ANIMATION_FPS,
            'xp_value': XP_GREEN_XP_VALUE
        },
        'yellow': {
            'sprite': XP_YELLOW_SPRITE,
            'frame_size': XP_YELLOW_FRAME_SIZE,
            'frame_count': XP_YELLOW_FRAME_COUNT,
            'animation_fps': XP_YELLOW_ANIMATION_FPS,
            'xp_value': XP_YELLOW_XP_VALUE
        },
        'light_blue': {
            'sprite': XP_LIGHT_BLUE_SPRITE,
            'frame_size': XP_LIGHT_BLUE_FRAME_SIZE,
            'frame_count': XP_LIGHT_BLUE_FRAME_COUNT,
            'animation_fps': XP_LIGHT_BLUE_ANIMATION_FPS,
            'xp_value': XP_LIGHT_BLUE_XP_VALUE
        },
        'blue': {
            'sprite': XP_BLUE_SPRITE,
            'frame_size': XP_BLUE_FRAME_SIZE,
            'frame_count': XP_BLUE_FRAME_COUNT,
            'animation_fps': XP_BLUE_ANIMATION_FPS,
            'xp_value': XP_BLUE_XP_VALUE
        },
        'red': {
            'sprite': XP_RED_SPRITE,
            'frame_size': XP_RED_FRAME_SIZE,
            'frame_count': XP_RED_FRAME_COUNT,
            'animation_fps': XP_RED_ANIMATION_FPS,
            'xp_value': XP_RED_XP_VALUE
        },
        'purple': {
            'sprite': XP_PURPLE_SPRITE,
            'frame_size': XP_PURPLE_FRAME_SIZE,
            'frame_count': XP_PURPLE_FRAME_COUNT,
            'animation_fps': XP_PURPLE_ANIMATION_FPS,
            'xp_value': XP_PURPLE_XP_VALUE
        }
    }
    
    def __init__(self, x, y, crystal_type='green'):
        super().__init__(x, y)
        self._frames = []
        self.animation_timer = 0.0
        self.crystal_type = crystal_type
        self.config = self.CRYSTAL_TYPES.get(crystal_type, self.CRYSTAL_TYPES['green'])
        self.xp_value = self.config['xp_value']
        self._load_sprite_frames()
    
    def _load_sprite_frames(self):
        """Load and split the animated XP crystal sprite."""
        try:
            full_path = resource_path(self.config['sprite'])
            if os.path.exists(full_path):
                sprite_sheet = pygame.image.load(full_path).convert_alpha()
                
                # Split sprite sheet into individual frames
                frame_width, frame_height = self.config['frame_size']
                for i in range(self.config['frame_count']):
                    frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
                    frame = sprite_sheet.subsurface(frame_rect).copy()
                    self._frames.append(frame)
                
                print(f"[PICKABLES] Loaded {len(self._frames)} {self.crystal_type} XP crystal frames")
            else:
                print(f"[WARNING] {self.crystal_type} XP crystal sprite not found: {full_path}")
                self._create_fallback_frames()
        except Exception as e:
            print(f"[WARNING] Failed to load {self.crystal_type} XP crystal sprite: {e}")
            self._create_fallback_frames()
    
    def _create_fallback_frames(self):
        """Create fallback colored frames if sprite loading fails."""
        frame_width, frame_height = self.config['frame_size']
        
        # Define fallback colors for each crystal type
        fallback_colors = {
            'green': (0, 255, 0),
            'yellow': (255, 255, 0),
            'light_blue': (173, 216, 230),
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'purple': (128, 0, 128)
        }
        
        base_color = fallback_colors.get(self.crystal_type, (0, 255, 0))
        
        for i in range(self.config['frame_count']):
            frame = pygame.Surface((frame_width, frame_height))
            # Create slightly different brightness for animation effect
            brightness_mod = 200 + (i * 10)
            color = tuple(min(255, int(c * brightness_mod / 255)) for c in base_color)
            frame.fill(color)
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
            
        print(f"[PICKABLES] Player collected {self.crystal_type} XP crystal! Gained {self.xp_value} XP")
        self.collected = True
        
    def draw(self, surface, camera=None):
        """Draw the animated XP crystal."""
        if not self._frames:
            return
            
        # Calculate current frame using this crystal's animation speed
        frame_index = int(self.animation_timer * self.config['animation_fps']) % len(self._frames)
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
        
    def create_xp_pickable(self, x, y, crystal_type='green'):
        """Create an XP crystal pickable at the specified position."""
        xp_crystal = XpPickable(x, y, crystal_type)
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
