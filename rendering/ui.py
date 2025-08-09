"""
User interface rendering logic.
"""
def draw_hud(screen, player):
    import pygame
    from config import (
        HUD_TOP_HEIGHT, HUD_BOTTOM_HEIGHT, HUD_LEFT_WIDTH, HUD_RIGHT_WIDTH,
        HUD_ALPHA, HUD_COLOR, HUD_LABEL_COLOR, HUD_LABEL_FONT_SIZE
    )
    width, height = screen.get_size()

    # Top HUD (full width, HUD_TOP_HEIGHT)
    top_hud = pygame.Surface((width, HUD_TOP_HEIGHT), pygame.SRCALPHA)
    top_hud.fill(HUD_COLOR)
    screen.blit(top_hud, (0, 0))

    # Bottom HUD (full width, HUD_BOTTOM_HEIGHT)
    bottom_hud = pygame.Surface((width, HUD_BOTTOM_HEIGHT), pygame.SRCALPHA)
    bottom_hud.fill(HUD_COLOR)
    screen.blit(bottom_hud, (0, height - HUD_BOTTOM_HEIGHT))

    # Left HUD (HUD_LEFT_WIDTH wide, full height minus top/bottom)
    left_hud = pygame.Surface((HUD_LEFT_WIDTH, height - HUD_TOP_HEIGHT - HUD_BOTTOM_HEIGHT), pygame.SRCALPHA)
    left_hud.fill(HUD_COLOR)
    screen.blit(left_hud, (0, HUD_TOP_HEIGHT))

    # Right HUD (HUD_RIGHT_WIDTH wide, full height minus top/bottom)
    right_hud = pygame.Surface((HUD_RIGHT_WIDTH, height - HUD_TOP_HEIGHT - HUD_BOTTOM_HEIGHT), pygame.SRCALPHA)
    right_hud.fill(HUD_COLOR)
    screen.blit(right_hud, (width - HUD_RIGHT_WIDTH, HUD_TOP_HEIGHT))

    # Optionally, add labels for clarity
    font = pygame.font.SysFont(None, HUD_LABEL_FONT_SIZE)
    screen.blit(font.render("TOP HUD", True, HUD_LABEL_COLOR), (width//2 - 60, 20))
    screen.blit(font.render("BOTTOM HUD", True, HUD_LABEL_COLOR), (width//2 - 80, height - HUD_BOTTOM_HEIGHT + 20))
    screen.blit(font.render("LEFT HUD", True, HUD_LABEL_COLOR), (10, height//2 - 20))
    screen.blit(font.render("RIGHT HUD", True, HUD_LABEL_COLOR), (width - HUD_RIGHT_WIDTH + 10, height//2 - 20))

def draw_menu(screen):
    # Draw game menu
    pass
