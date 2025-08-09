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
        # TODO: Initialize monsters, loot, map, etc.

    def update(self, dt):
        self.player.update(dt)
        # TODO: Update monsters, loot, etc.
