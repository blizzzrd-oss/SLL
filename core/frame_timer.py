"""
Frame timing and performance utilities.
Handles FPS control and timing calculations.
"""

import json
import pygame


class FrameTimer:
    """Manages frame timing, FPS control, and time accumulation."""
    
    def __init__(self, settings_path):
        self.settings_path = settings_path
        self.clock = pygame.time.Clock()
        self.time_accum = 0.0
        self.target_fps = 60  # Default FPS
        
    def tick(self):
        """Advance one frame and return timing information."""
        # Load current FPS setting
        self.target_fps = self._load_fps_setting()
        
        # Calculate frame delta time
        dt = self.clock.tick(self.target_fps) / 1000.0
        self.time_accum += dt
        
        return dt, self.time_accum, self.clock.get_fps()
    
    def _load_fps_setting(self):
        """Load FPS setting from configuration file."""
        try:
            with open(self.settings_path, 'r') as f:
                settings = json.load(f)
            return int(settings.get('fps', 60))
        except Exception:
            return 60  # Fallback to 60 FPS
            
    def get_accumulated_time(self):
        """Get total accumulated game time."""
        return self.time_accum
