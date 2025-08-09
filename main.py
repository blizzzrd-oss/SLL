 


from core.init import init_pygame
from rendering.menu import Menu
from core.game import Game

def main():
    screen = init_pygame()

    def start_game(slot, mode):
        game = Game(screen, slot, mode)
        game.run()

    menu = Menu(screen, start_game_callback=start_game)
    menu.run()  # Handles menu loop and transitions

if __name__ == "__main__":
    main()
