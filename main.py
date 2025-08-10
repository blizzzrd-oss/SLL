
import pygame
from core.init import init_pygame
from rendering.menu import Menu
from core.game import Game
from core.game_loop import run_game

def main():
    screen = init_pygame()

    def start_game(slot, mode):
        run_game(screen, slot, mode)

    while True:
        menu = Menu(screen, start_game_callback=start_game)
        menu.run()  # Handles menu loop and transitions
        # If the user closed the window or chose Quit, pygame.get_init() will be False
        if not pygame.get_init():
            break

if __name__ == "__main__":
    main()