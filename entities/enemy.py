"""
Enemy entity and logic.
"""
import pygame

class Enemy:
    def __init__(self):
        self.health = 50
        self.position = (0, 0)
        self.size = 48
        self.rect = pygame.Rect(self.position[0] - self.size // 2, self.position[1] - self.size // 2, self.size, self.size)
        self.facing_angle = 0
        self.skills = {}
        # ...other attributes...
