"""
User interface rendering logic.
"""
import pygame
from config import (
    HUD_TOP_HEIGHT, HUD_BOTTOM_HEIGHT, HUD_LEFT_WIDTH, HUD_RIGHT_WIDTH,
    HUD_ALPHA, HUD_COLOR, HUD_LABEL_COLOR, HUD_LABEL_FONT_SIZE
)

# Cache for HUD surfaces and font
_hud_cache = {
    'size': None,
    'top': None,
    'bottom': None,
    'left': None,
    'right': None,
    'font': None
}

def draw_hud(screen, player, fps=None):
    width, height = screen.get_size()
    global _hud_cache
    # Recreate surfaces only if size changed
    if _hud_cache['size'] != (width, height):
        _hud_cache['top'] = pygame.Surface((width, HUD_TOP_HEIGHT), pygame.SRCALPHA)
        _hud_cache['top'].fill(HUD_COLOR)
        _hud_cache['bottom'] = pygame.Surface((width, HUD_BOTTOM_HEIGHT), pygame.SRCALPHA)
        _hud_cache['bottom'].fill(HUD_COLOR)
        _hud_cache['left'] = pygame.Surface((HUD_LEFT_WIDTH, height - HUD_TOP_HEIGHT - HUD_BOTTOM_HEIGHT), pygame.SRCALPHA)
        _hud_cache['left'].fill(HUD_COLOR)
        _hud_cache['right'] = pygame.Surface((HUD_RIGHT_WIDTH, height - HUD_TOP_HEIGHT - HUD_BOTTOM_HEIGHT), pygame.SRCALPHA)
        _hud_cache['right'].fill(HUD_COLOR)
        _hud_cache['size'] = (width, height)
    if _hud_cache['font'] is None:
        _hud_cache['font'] = pygame.font.SysFont(None, HUD_LABEL_FONT_SIZE)
    font = _hud_cache['font']

    # Blit cached surfaces
    screen.blit(_hud_cache['top'], (0, 0))
    screen.blit(_hud_cache['bottom'], (0, height - HUD_BOTTOM_HEIGHT))
    screen.blit(_hud_cache['left'], (0, HUD_TOP_HEIGHT))
    screen.blit(_hud_cache['right'], (width - HUD_RIGHT_WIDTH, HUD_TOP_HEIGHT))

    # Optionally, add labels for clarity
    screen.blit(font.render("TOP HUD", True, HUD_LABEL_COLOR), (width//2 - 60, 20))
    screen.blit(font.render("BOTTOM HUD", True, HUD_LABEL_COLOR), (width//2 - 80, height - HUD_BOTTOM_HEIGHT + 20))
    screen.blit(font.render("LEFT HUD", True, HUD_LABEL_COLOR), (10, height//2 - 20))
    screen.blit(font.render("RIGHT HUD", True, HUD_LABEL_COLOR), (width - HUD_RIGHT_WIDTH + 10, height//2 - 20))

    # Show FPS in the top right corner
    if fps is not None:
        fps_text = font.render(f"FPS: {int(fps)}", True, HUD_LABEL_COLOR)
        text_rect = fps_text.get_rect(topright=(width - 20, 10))
        screen.blit(fps_text, text_rect)

def draw_menu(screen):
    # Draw game menu
    pass
