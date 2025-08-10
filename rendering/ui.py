"""
User interface rendering logic.
"""
import pygame
import os
from config import (
    HUD_TOP_HEIGHT, HUD_BOTTOM_HEIGHT, HUD_LEFT_WIDTH, HUD_RIGHT_WIDTH,
    HUD_ALPHA, HUD_COLOR, HUD_LABEL_COLOR, HUD_LABEL_FONT_SIZE,
    COLOR_HEALTH_BAR_BG, COLOR_HEALTH_BAR_FILL, COLOR_BARRIER_BAR_BG, COLOR_BARRIER_BAR_FILL
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

def draw_hud(screen, player, fps=None, game_mode=None, active_events=None, event_notifications=None):
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
    SKILL_KEYS = ["LMB", "RMB", "SPACE", "1", "2", "3", "4"]
    # Load slash and dash skill images (cache them)
    if not hasattr(draw_hud, '_slash_img'):
        slash_img_path = r'C:\Repos\SLL\resources\images\UI\hud\skill_bar\skill_slash.jpg'
        if os.path.exists(slash_img_path):
            img = pygame.image.load(slash_img_path).convert_alpha()
            draw_hud._slash_img = pygame.transform.smoothscale(img, (SKILL_BOX_SIZE, SKILL_BOX_SIZE))
        else:
            draw_hud._slash_img = None
    if not hasattr(draw_hud, '_dash_img'):
        dash_img_path = r'C:\Repos\SLL\resources\images\UI\hud\skill_bar\skill_dash.jpg'
        if os.path.exists(dash_img_path):
            img = pygame.image.load(dash_img_path).convert_alpha()
            draw_hud._dash_img = pygame.transform.smoothscale(img, (SKILL_BOX_SIZE, SKILL_BOX_SIZE))
        else:
            draw_hud._dash_img = None
    # Draw skill boxes and cooldown bars
    skill_names = ["slash", None, "dash", None, None, None, None]
    for i in range(SKILL_BOX_COUNT):
        box_x = SKILL_BAR_X + i * (SKILL_BOX_SIZE + SKILL_BOX_GAP)
        box_y = SKILL_BAR_Y
        box_rect = pygame.Rect(box_x, box_y, SKILL_BOX_SIZE, SKILL_BOX_SIZE)
        # Draw cooldown bar above box if skill exists
        skill_name = skill_names[i]
        if skill_name and skill_name in player.skills:
            skill = player.skills[skill_name]
            now = pygame.time.get_ticks() / 1000
            cd = max(0, skill.cooldown - (now - skill.last_used)) if not getattr(skill, 'active', False) else skill.cooldown
            cd_frac = min(cd / skill.cooldown, 1.0) if skill.cooldown > 0 else 0
            bar_w = SKILL_BOX_SIZE
            bar_h = 8
            bar_x = box_x
            bar_y = box_y - bar_h - 4
            # Draw background
            pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
            # Draw filled portion if on cooldown
            if cd_frac > 0:
                fill_w = int(bar_w * cd_frac)
                pygame.draw.rect(screen, (120, 180, 255), (bar_x, bar_y, fill_w, bar_h), border_radius=4)
        # Draw semi-transparent box
        box_surface = pygame.Surface((SKILL_BOX_SIZE, SKILL_BOX_SIZE), pygame.SRCALPHA)
        box_surface.fill((80, 80, 80, SKILL_BOX_ALPHA))
        screen.blit(box_surface, (box_x, box_y))
        # Draw slash skill image in first box, dash skill image in third box
        if i == 0 and draw_hud._slash_img:
            screen.blit(draw_hud._slash_img, (box_x, box_y))
        if i == 2 and draw_hud._dash_img:
            screen.blit(draw_hud._dash_img, (box_x, box_y))
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
    # Remove HUD backgrounds for a cleaner look
    if _hud_cache['size'] != (width, height):
        _hud_cache['size'] = (width, height)
    if _hud_cache['font'] is None:
        _hud_cache['font'] = pygame.font.SysFont(None, HUD_LABEL_FONT_SIZE)
    font = _hud_cache['font']

    # No HUD background surfaces blitted for cleaner appearance


    # --- Health and Shield Bars (Left HUD, Top) ---
    BAR_X = 24
    BAR_Y = 24
    BAR_WIDTH = HUD_LEFT_WIDTH - 48
    BAR_HEIGHT = 32
    BAR_GAP = 12
    # Health bar (red)
    max_health = 100
    health_val = max(0, int(round(player.health)))
    health_frac = min(health_val / max_health, 1.0)
    pygame.draw.rect(screen, COLOR_HEALTH_BAR_BG, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), border_radius=8)
    pygame.draw.rect(screen, COLOR_HEALTH_BAR_FILL, (BAR_X, BAR_Y, int(BAR_WIDTH * health_frac), BAR_HEIGHT), border_radius=8)
    health_text = f"{health_val}/{max_health}"
    health_label = font.render(health_text, True, (255,255,255))
    health_label_rect = health_label.get_rect(center=(BAR_X + BAR_WIDTH // 2, BAR_Y + BAR_HEIGHT // 2))
    screen.blit(health_label, health_label_rect)
    # Shield bar (blue), below health
    max_shield = 100  # For bar scaling; actual max is 100 for full bar
    shield_val = max(0, int(round(player.barrier)))
    shield_frac = min(shield_val / max_shield, 1.0)
    shield_y = BAR_Y + BAR_HEIGHT + BAR_GAP
    pygame.draw.rect(screen, COLOR_BARRIER_BAR_BG, (BAR_X, shield_y, BAR_WIDTH, BAR_HEIGHT), border_radius=8)
    pygame.draw.rect(screen, COLOR_BARRIER_BAR_FILL, (BAR_X, shield_y, int(BAR_WIDTH * shield_frac), BAR_HEIGHT), border_radius=8)
    shield_text = f"{shield_val}/{max_shield}"
    shield_label = font.render(shield_text, True, (255,255,255))
    shield_label_rect = shield_label.get_rect(center=(BAR_X + BAR_WIDTH // 2, shield_y + BAR_HEIGHT // 2))
    screen.blit(shield_label, shield_label_rect)

    # Remove debug labels for cleaner look
    # screen.blit(font.render("TOP HUD", True, HUD_LABEL_COLOR), (width//2 - 60, 20))
    # screen.blit(font.render("LEFT HUD", True, HUD_LABEL_COLOR), (10, height//2 - 20))
    # screen.blit(font.render("RIGHT HUD", True, HUD_LABEL_COLOR), (width - HUD_RIGHT_WIDTH + 10, height//2 - 20))

    # --- Right HUD Display (FPS and Game Mode) ---
    # Show FPS in the top right corner
    if fps is not None:
        fps_text = font.render(f"FPS: {int(fps)}", True, HUD_LABEL_COLOR)
        text_rect = fps_text.get_rect(topright=(width - 20, 10))
        screen.blit(fps_text, text_rect)

    # Show Game Mode under FPS in right HUD
    if game_mode:
        mode_color = {
            'Easy': (100, 255, 100),    # Green
            'Normal': (255, 255, 100),  # Yellow
            'Hard': (255, 100, 100)     # Red
        }.get(game_mode, (255, 255, 255))
        
        mode_text = font.render(f"Mode: {game_mode}", True, mode_color)
        mode_rect = mode_text.get_rect(topright=(width - 20, 35))
        screen.blit(mode_text, mode_rect)

    # --- Active Events Display (Top HUD, Left) ---
    if active_events:
        event_y = 50
        for event in active_events:
            event_color = {
                'healing_shrine': (100, 255, 150),    # Light green
                'loot_blessing': (255, 215, 0),       # Gold
                'enemy_weakness': (255, 100, 255)     # Magenta
            }.get(event['type'], (255, 255, 255))
            
            # Format remaining time
            remaining_time = max(0, event['remaining'])
            time_str = f"{remaining_time:.1f}s"
            
            event_name = {
                'healing_shrine': 'Healing Shrine',
                'loot_blessing': 'Loot Blessing',
                'enemy_weakness': 'Enemy Weakness'
            }.get(event['type'], event['type'].title())
            
            event_text = font.render(f"{event_name} ({time_str})", True, event_color)
            screen.blit(event_text, (20, event_y))
            event_y += 25

    # --- Event Notifications (Center-right, fade in/out) ---
    if event_notifications:
        notification_x = width - 300
        notification_y = height // 2 - 100
        
        for notification in event_notifications:
            # Calculate fade alpha based on time since notification
            age = notification.get('age', 0)
            max_age = 3.0  # 3 seconds total display time
            fade_time = 0.5  # Fade in/out duration
            
            if age < fade_time:
                alpha = int(255 * (age / fade_time))
            elif age > max_age - fade_time:
                alpha = int(255 * ((max_age - age) / fade_time))
            else:
                alpha = 255
            
            alpha = max(0, min(255, alpha))
            
            if alpha > 0:
                # Event type color
                event_color = {
                    'healing_shrine': (100, 255, 150),
                    'loot_blessing': (255, 215, 0),
                    'enemy_weakness': (255, 100, 255)
                }.get(notification['type'], (255, 255, 255))
                
                # Create notification text
                event_name = {
                    'healing_shrine': 'HEALING SHRINE ACTIVATED!',
                    'loot_blessing': 'LOOT BLESSING ACTIVE!',
                    'enemy_weakness': 'ENEMIES WEAKENED!'
                }.get(notification['type'], notification['type'].upper())
                
                # Render with alpha
                notification_font = pygame.font.SysFont(None, 36)
                text_surface = notification_font.render(event_name, True, event_color)
                text_surface.set_alpha(alpha)
                
                # Draw background with alpha
                bg_rect = text_surface.get_rect(center=(notification_x, notification_y))
                bg_rect.inflate_ip(20, 10)
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                bg_surface.fill((0, 0, 0, alpha // 3))
                screen.blit(bg_surface, bg_rect.topleft)
                
                # Draw text
                screen.blit(text_surface, text_surface.get_rect(center=(notification_x, notification_y)))
                notification_y += 50

def draw_menu(screen):
    # Draw game menu
    pass
