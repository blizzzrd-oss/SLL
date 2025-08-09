"""
Game logic for the roguelike hack and slash.
Handles player, monsters, loot, skills, and inventory.
"""

import pygame
from entities.player import Player
from rendering.player_render import draw_player_idle, draw_player_walk
from core.player_movement import handle_player_movement

class Game:
    def __init__(self, screen, slot, mode):
        self.screen = screen
        self.slot = slot  # Save slot index
        self.mode = mode  # 'Easy', 'Normal', 'Hard'
        self.player = Player()
        self.game_over = False
        # TODO: Initialize monsters, loot, map, etc.

    def reset(self):
        """Reset the game state except for settings."""
        self.player = Player()
        self.game_over = False
        # TODO: Reset monsters, loot, map, etc.

    def update(self, dt):
        if not self.game_over:
            self.player.update(dt)
            # Check for player death
            if self.player.health <= 0:
                self.game_over = True
        # TODO: Update monsters, loot, etc.
