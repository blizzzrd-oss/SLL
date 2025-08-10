"""
User interface rendering logic.
"""
import pygame
import os
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
    # --- Skill Bar ---
    # Skill bar config
    SKILL_BOX_SIZE = 64
    SKILL_BOX_GAP = 16
    SKILL_BOX_COUNT = 7
    SKILL_BOX_ALPHA = int(0.8 * 255)
    SKILL_BAR_Y = height - HUD_BOTTOM_HEIGHT + 10
    SKILL_BAR_WIDTH = SKILL_BOX_COUNT * SKILL_BOX_SIZE + (SKILL_BOX_COUNT - 1) * SKILL_BOX_GAP
    SKILL_BAR_X = (width - SKILL_BAR_WIDTH) // 2
    # Key labels for each skill slot (first is SPACE, rest empty)
    SKILL_KEYS = ["SPACE"] + ["" for _ in range(SKILL_BOX_COUNT - 1)]
    # Load slash skill image (cache it)
    if not hasattr(draw_hud, '_slash_img'):
        slash_img_path = r'C:\Repos\SLL\resources\images\UI\hud\skill_bar\skill_slash.jpg'
        if os.path.exists(slash_img_path):
            img = pygame.image.load(slash_img_path).convert_alpha()
            draw_hud._slash_img = pygame.transform.smoothscale(img, (SKILL_BOX_SIZE, SKILL_BOX_SIZE))
        else:
            draw_hud._slash_img = None
    # Draw skill boxes
    for i in range(SKILL_BOX_COUNT):
        box_x = SKILL_BAR_X + i * (SKILL_BOX_SIZE + SKILL_BOX_GAP)
        box_y = SKILL_BAR_Y
        box_rect = pygame.Rect(box_x, box_y, SKILL_BOX_SIZE, SKILL_BOX_SIZE)
        # Draw semi-transparent box
        box_surface = pygame.Surface((SKILL_BOX_SIZE, SKILL_BOX_SIZE), pygame.SRCALPHA)
        box_surface.fill((80, 80, 80, SKILL_BOX_ALPHA))
        screen.blit(box_surface, (box_x, box_y))
        # Draw slash skill image in first box
        if i == 0 and draw_hud._slash_img:
            screen.blit(draw_hud._slash_img, (box_x, box_y))
        # Draw border
        pygame.draw.rect(screen, (200, 200, 200), box_rect, 2)
        # Draw key label below box (no visual box, move text up)
        key_label = SKILL_KEYS[i]
        if key_label:
            key_font = pygame.font.SysFont(None, 24)
            label_surf = key_font.render(key_label, True, (220, 220, 220))
            label_rect = label_surf.get_rect(center=(box_x + SKILL_BOX_SIZE // 2, box_y + SKILL_BOX_SIZE + 10))
            screen.blit(label_surf, label_rect)
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
    # Removed bottom HUD background for a cleaner look
    screen.blit(_hud_cache['left'], (0, HUD_TOP_HEIGHT))
    screen.blit(_hud_cache['right'], (width - HUD_RIGHT_WIDTH, HUD_TOP_HEIGHT))

    # Optionally, add labels for clarity
    screen.blit(font.render("TOP HUD", True, HUD_LABEL_COLOR), (width//2 - 60, 20))
    # Removed 'BOTTOM HUD' label for a cleaner look
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
