"""
Game logic for the roguelike hack and slash.
Handles player, monsters, loot, skills, and inventory.
"""
import pygame

class Game:
    def __init__(self, screen, slot, mode):
        self.screen = screen
        self.slot = slot  # Save slot index
        self.mode = mode  # 'Easy', 'Normal', 'Hard'
        self.running = True
        # TODO: Initialize player, monsters, loot, map, etc.

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # TODO: Handle input, skills, inventory, etc.
            self.update()
            self.draw()
            clock.tick(60)

    def update(self):
        # TODO: Update player, monsters, loot, etc.
        pass

    def draw(self):
        self.screen.fill((20, 20, 20))
        # TODO: Draw player, monsters, loot, UI, etc.
        pygame.display.flip()
