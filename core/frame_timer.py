"""
Frame timing and performance utilities.
Handles FPS control and timing calculations.
"""

import json
import pygame
from config import GAME_DEFAULT_FPS


class FrameTimer:
    """Manages frame timing, FPS control, and time accumulation."""
    
    def __init__(self, settings_path):
        self.settings_path = settings_path
        self.clock = pygame.time.Clock()
        self.time_accum = 0.0
        self.target_fps = GAME_DEFAULT_FPS  # Default FPS from config
        
        # FPS calculation optimization
        self.fps_update_timer = 0.0
        self.fps_update_interval = 0.5  # Update FPS twice per second
        self.cached_fps = 60.0  # Start with reasonable default
        
        # Settings caching
        self.settings_update_timer = 0.0
        self.settings_update_interval = 1.0  # Check settings once per second
        
    def tick(self):
        """Advance one frame and return timing information."""
        # Calculate frame delta time
        dt = self.clock.tick(self.target_fps) / 1000.0
        self.time_accum += dt
        
        # Update FPS calculation only twice per second
        self.fps_update_timer += dt
        if self.fps_update_timer >= self.fps_update_interval:
            self.cached_fps = self.clock.get_fps()
            self.fps_update_timer = 0.0
        
        # Update settings cache only once per second
        self.settings_update_timer += dt
        if self.settings_update_timer >= self.settings_update_interval:
            self.target_fps = self._load_fps_setting()
            self.settings_update_timer = 0.0
        
        return dt, self.time_accum, self.cached_fps
    
    def _load_fps_setting(self):
        """Load FPS setting from configuration file."""
        try:
            with open(self.settings_path, 'r') as f:
                settings = json.load(f)
            return int(settings.get('fps', GAME_DEFAULT_FPS))
        except Exception:
            return GAME_DEFAULT_FPS  # Fallback to config default
    
    def force_fps_update(self):
        """Force an immediate FPS setting update (for settings menu)."""
        self.target_fps = self._load_fps_setting()
        self.settings_update_timer = 0.0
            
    def get_accumulated_time(self):
        """Get total accumulated game time."""
        return self.time_accum
    
    def get_current_fps(self):
        """Get the current cached FPS value."""
        return self.cached_fps
