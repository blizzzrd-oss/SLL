import pygame
import os
from config import BG_MUSIC_PATH, MUSIC_VOLUME, WINDOW_WIDTH, WINDOW_HEIGHT, PAUSE_MENU_OPTIONS
from rendering.menu import resource_path, Menu
from core.game import Game

def initialize_game_state(screen, slot, mode):
    game = Game(screen, slot, mode)
    running = True
    should_exit = False
    last_move = (0, 0)
    time_accum = 0.0
    clock = pygame.time.Clock()
    paused = False
    pause_menu_selected = 0
    pause_menu_options = PAUSE_MENU_OPTIONS
    pause_menu_rects = []
    in_settings_menu = False
    settings_menu = None
    game.reset()
    hud_visible = True
    settings_path = os.path.join(os.path.dirname(__file__), '..', 'settings.json')
    return (game, running, should_exit, last_move, time_accum, clock, paused, pause_menu_selected, pause_menu_options, pause_menu_rects, in_settings_menu, settings_menu, hud_visible, settings_path)

"""
Pygame and audio initialization logic.
"""
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
