"""
Camera system for following the player and translating world coordinates to screen coordinates.
"""
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, CAMERA_FOLLOW_SPEED, CAMERA_DEADZONE


class Camera:
    """Simple camera that follows the player."""
    
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0
        
    def update(self, player, dt):
        """Update camera position to follow player."""
        # Calculate target position (center player on screen)
        self.target_x = player.x - WINDOW_WIDTH // 2
        self.target_y = player.y - WINDOW_HEIGHT // 2
        
        # Smooth camera movement
        if CAMERA_FOLLOW_SPEED >= 1.0:
            # Instant follow
            self.x = self.target_x
            self.y = self.target_y
        else:
            # Smooth follow
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            self.x += dx * CAMERA_FOLLOW_SPEED * dt * 60  # 60 FPS baseline
            self.y += dy * CAMERA_FOLLOW_SPEED * dt * 60
    
    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates."""
        screen_x = world_x - self.x
        screen_y = world_y - self.y
        return int(screen_x), int(screen_y)
    
    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates."""
        world_x = screen_x + self.x
        world_y = screen_y + self.y
        return world_x, world_y
