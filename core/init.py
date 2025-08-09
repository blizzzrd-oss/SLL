"""
Pygame and audio initialization logic.
"""
import pygame
from config import BG_MUSIC_PATH, MUSIC_VOLUME, WINDOW_WIDTH, WINDOW_HEIGHT
from rendering.menu import resource_path

def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("SLL")
    # Load and play background music
    pygame.mixer.init()
    music_path = resource_path(BG_MUSIC_PATH)
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1)  # Loop forever
    return screen
