 

from core.init import init_pygame
from rendering.menu import Menu

def main():
    screen = init_pygame()
    menu = Menu(screen)
    menu.run()  # Handles menu loop and transitions

if __name__ == "__main__":
    main()
