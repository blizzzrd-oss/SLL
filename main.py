from core.init import init_pygame
from rendering.menu import Menu
from core.game import Game
from core.game_loop import run_game

def main():
    screen = init_pygame()

    def start_game(slot, mode):
        run_game(screen, slot, mode)

    menu = Menu(screen, start_game_callback=start_game)
    menu.run()  # Handles menu loop and transitions

if __name__ == "__main__":
    main()