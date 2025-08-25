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
from utils.resource_path import resource_path

# Cache for HUD surfaces and font
_hud_cache = {
    'size': None,
    'top': None,
    'bottom': None,
    'left': None,
    'right': None,
    'font': None,
    'fps_text': None,
    'fps_value': None
}

def draw_hud(screen, player, fps=None, game_mode=None, active_events=None, event_notifications=None, game_time=None, wave_info=None):
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
        slash_img_path = resource_path('resources/images/UI/hud/skill_bar/skill_slash.jpg')
        if os.path.exists(slash_img_path):
            img = pygame.image.load(slash_img_path).convert_alpha()
            draw_hud._slash_img = pygame.transform.smoothscale(img, (SKILL_BOX_SIZE, SKILL_BOX_SIZE))
        else:
            draw_hud._slash_img = None
    if not hasattr(draw_hud, '_dash_img'):
        dash_img_path = resource_path('resources/images/UI/hud/skill_bar/skill_dash.jpg')
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
            
            # Check if skill has charge system
            has_charges = hasattr(skill, 'max_charges') and skill.max_charges > 1
            
            if has_charges:
                # For charge-based skills, show charges and regeneration progress
                current_charges = getattr(skill, 'current_charges', 1)
                max_charges = getattr(skill, 'max_charges', 1)
                
                # Draw charge counter above cooldown bar
                charge_text = f"{current_charges}/{max_charges}"
                charge_font = pygame.font.SysFont(None, 20)
                charge_surf = charge_font.render(charge_text, True, (255, 255, 255))
                charge_rect = charge_surf.get_rect(center=(box_x + SKILL_BOX_SIZE // 2, box_y - 25))
                screen.blit(charge_surf, charge_rect)
                
                # Calculate regeneration progress for cooldown bar
                if current_charges < max_charges:
                    # Show progress toward next charge
                    last_charge_regen = getattr(skill, 'last_charge_regen', 0)
                    charge_regen_time = getattr(skill, 'charge_regen_time', 2.0)
                    time_since_regen = now - last_charge_regen
                    regen_progress = min(time_since_regen / charge_regen_time, 1.0) if charge_regen_time > 0 else 0
                    cd_frac = 1.0 - regen_progress  # Invert so bar empties as charge regenerates
                else:
                    # At max charges, no cooldown
                    cd_frac = 0
            else:
                # For normal skills, use regular cooldown
                cd = max(0, skill.cooldown - (now - skill.last_used)) if not getattr(skill, 'active', False) else skill.cooldown
                cd_frac = min(cd / skill.cooldown, 1.0) if skill.cooldown > 0 else 0
            
            # Draw cooldown bar
            bar_w = SKILL_BOX_SIZE
            bar_h = 8
            bar_x = box_x
            bar_y = box_y - bar_h - 4
            
            # Draw background
            pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
            
            # Draw filled portion if on cooldown/regenerating
            if cd_frac > 0:
                fill_w = int(bar_w * cd_frac)
                if has_charges:
                    # Use different color for charge regeneration
                    pygame.draw.rect(screen, (255, 180, 120), (bar_x, bar_y, fill_w, bar_h), border_radius=4)
                else:
                    # Regular cooldown color
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
    max_health = getattr(player, 'max_health', 100)
    health_val = max(0, int(round(player.health)))
    health_frac = min(health_val / max_health, 1.0) if max_health > 0 else 0
    pygame.draw.rect(screen, COLOR_HEALTH_BAR_BG, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), border_radius=8)
    pygame.draw.rect(screen, COLOR_HEALTH_BAR_FILL, (BAR_X, BAR_Y, int(BAR_WIDTH * health_frac), BAR_HEIGHT), border_radius=8)
    health_text = f"{health_val}/{max_health}"
    health_label = font.render(health_text, True, (255,255,255))
    health_label_rect = health_label.get_rect(center=(BAR_X + BAR_WIDTH // 2, BAR_Y + BAR_HEIGHT // 2))
    screen.blit(health_label, health_label_rect)
    # Shield bar (blue), below health
    max_shield = getattr(player, 'max_barrier', 100)  # Use player's actual max barrier
    shield_val = max(0, int(round(player.barrier)))
    shield_frac = min(shield_val / max_shield, 1.0) if max_shield > 0 else 0
    shield_y = BAR_Y + BAR_HEIGHT + BAR_GAP
    pygame.draw.rect(screen, COLOR_BARRIER_BAR_BG, (BAR_X, shield_y, BAR_WIDTH, BAR_HEIGHT), border_radius=8)
    pygame.draw.rect(screen, COLOR_BARRIER_BAR_FILL, (BAR_X, shield_y, int(BAR_WIDTH * shield_frac), BAR_HEIGHT), border_radius=8)
    shield_text = f"{shield_val}/{max_shield}"
    shield_label = font.render(shield_text, True, (255,255,255))
    shield_label_rect = shield_label.get_rect(center=(BAR_X + BAR_WIDTH // 2, shield_y + BAR_HEIGHT // 2))
    screen.blit(shield_label, shield_label_rect)
    
    # Experience bar (purple), below shield
    exp_val = int(player.exp)  # Convert to integer for display
    exp_needed = int(player.get_exp_to_next_level())  # Convert to integer for display
    exp_frac = player.get_experience_progress()
    exp_y = shield_y + BAR_HEIGHT + BAR_GAP
    
    # XP bar colors (purple theme)
    EXP_BAR_BG = (60, 30, 80)    # Dark purple background
    EXP_BAR_FILL = (120, 60, 160) # Bright purple fill
    
    pygame.draw.rect(screen, EXP_BAR_BG, (BAR_X, exp_y, BAR_WIDTH, BAR_HEIGHT), border_radius=8)
    pygame.draw.rect(screen, EXP_BAR_FILL, (BAR_X, exp_y, int(BAR_WIDTH * exp_frac), BAR_HEIGHT), border_radius=8)
    
    # Display level and XP text
    if player.level >= player.max_level:
        exp_text = f"Level {player.level} (MAX)"
    else:
        exp_text = f"Level {player.level} - {exp_val}/{exp_needed} XP"
    
    exp_label = font.render(exp_text, True, (255,255,255))
    exp_label_rect = exp_label.get_rect(center=(BAR_X + BAR_WIDTH // 2, exp_y + BAR_HEIGHT // 2))
    screen.blit(exp_label, exp_label_rect)

    # Remove debug labels for cleaner look
    # screen.blit(font.render("TOP HUD", True, HUD_LABEL_COLOR), (width//2 - 60, 20))
    # screen.blit(font.render("LEFT HUD", True, HUD_LABEL_COLOR), (10, height//2 - 20))
    # screen.blit(font.render("RIGHT HUD", True, HUD_LABEL_COLOR), (width - HUD_RIGHT_WIDTH + 10, height//2 - 20))

    # --- Right HUD Display (FPS and Game Mode) ---
    # Show FPS in the top right corner with caching
    if fps is not None:
        fps_int = int(fps)
        # Only re-render FPS text if the value changed
        if _hud_cache['fps_value'] != fps_int:
            _hud_cache['fps_value'] = fps_int
            _hud_cache['fps_text'] = font.render(f"FPS: {fps_int}", True, HUD_LABEL_COLOR)
        
        if _hud_cache['fps_text'] is not None:
            text_rect = _hud_cache['fps_text'].get_rect(topright=(width - 20, 10))
            screen.blit(_hud_cache['fps_text'], text_rect)

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

    # --- Game Time Display (Top HUD, Right) ---
    if game_time is not None:
        # Format time as MM:SS
        minutes = int(game_time // 60)
        seconds = int(game_time % 60)
        time_str = f"Time: {minutes:02d}:{seconds:02d}"
        
        time_text = font.render(time_str, True, (255, 255, 255))
        time_rect = time_text.get_rect(topright=(width - 20, 65))  # Below mode display
        screen.blit(time_text, time_rect)

    # --- Wave Information Display (Top HUD, Right) ---
    if wave_info is not None:
        # Wave number and description
        wave_text = font.render(f"Wave {wave_info['number']}", True, (255, 255, 100))
        wave_rect = wave_text.get_rect(topright=(width - 20, 95))  # Below time display
        screen.blit(wave_text, wave_rect)
        
        # Wave progress bar
        if wave_info.get('progress', 0) < 1.0:
            bar_width = 120
            bar_height = 8
            bar_x = width - 20 - bar_width
            bar_y = 115
            
            # Background bar
            pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
            
            # Progress bar
            progress_width = int(bar_width * wave_info['progress'])
            color = (255, 100, 100) if wave_info.get('is_boss_wave', False) else (100, 150, 255)
            pygame.draw.rect(screen, color, (bar_x, bar_y, progress_width, bar_height))
            
            # Time remaining
            time_remaining = int(wave_info.get('time_remaining', 0))
            remaining_text = font.render(f"{time_remaining}s", True, (200, 200, 200))
            remaining_rect = remaining_text.get_rect(topright=(width - 20, 125))
            screen.blit(remaining_text, remaining_rect)

    # --- Active Events Display (Top HUD, Center) ---
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
            # Center the text horizontally
            text_rect = event_text.get_rect(centerx=width // 2, y=event_y)
            screen.blit(event_text, text_rect)
            event_y += 25

    # --- Event Notifications (Center-right, fade in/out) ---
    if event_notifications:
        notification_x = width - 300
        notification_y = height // 2 - 100
        
        for notification in event_notifications:
            # Handle both string and dict notification formats
            if isinstance(notification, str):
                # Simple string notification - show for 2 seconds
                notification_text = notification
                alpha = 255  # Full opacity for string notifications
            else:
                # Dictionary notification with age tracking
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
                notification_text = notification.get('text', str(notification))
            
            if alpha > 0:
                # Use default color for string notifications
                event_color = (255, 255, 100)  # Yellow default
                
                # If we can determine event type, use specific colors
                if 'HEALING' in notification_text.upper():
                    event_color = (100, 255, 150)
                elif 'LOOT' in notification_text.upper():
                    event_color = (255, 215, 0)
                elif 'ENEMIES' in notification_text.upper() or 'WEAKNESS' in notification_text.upper():
                    event_color = (255, 100, 255)
                
                # Render with alpha
                notification_font = pygame.font.SysFont(None, 36)
                text_surface = notification_font.render(notification_text, True, event_color)
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
