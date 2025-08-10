import pygame
from config import (
    PLAYER_HURT_ANIMATION_FPS, PLAYER_SPRITE_FRAME_WIDTH, GAME_BG_COLOR, GAME_OVERLAY_COLOR, PAUSE_OVERLAY_COLOR, GAME_OVER_FONT_SIZE, PAUSE_FONT_SIZE, MENU_FONT_SIZE, PAUSE_MENU_HIGHLIGHT_COLOR, PAUSE_MENU_TEXT_COLOR
)
from rendering.player_render import draw_player_idle, draw_player_walk, draw_player_run, draw_player_hurt
from rendering.ui import draw_hud


# --- Resource cache ---
_game_render_cache = {
    'hurt_hp_img': None,
    'hurt_barrier_img': None,
    'game_over_font': None,
    'menu_font': None,
    'pause_font': None
}

def draw_game(screen, game, last_move, time_accum, paused=False, pause_menu_selected=0, pause_menu_options=None, pause_menu_rects=None, hud_visible=True, fps=None):
    screen.fill(GAME_BG_COLOR)
    player = game.player
    global _game_render_cache
    if _game_render_cache['hurt_hp_img'] is None:
        _game_render_cache['hurt_hp_img'] = pygame.image.load('resources/images/player/Hurt/Slime1_Hurt_full_hp.png').convert_alpha()
    if _game_render_cache['hurt_barrier_img'] is None:
        _game_render_cache['hurt_barrier_img'] = pygame.image.load('resources/images/player/Hurt/Slime1_Hurt_full_barrier.png').convert_alpha()
    if _game_render_cache['game_over_font'] is None:
        _game_render_cache['game_over_font'] = pygame.font.SysFont(None, GAME_OVER_FONT_SIZE)
    if _game_render_cache['menu_font'] is None:
        _game_render_cache['menu_font'] = pygame.font.SysFont(None, MENU_FONT_SIZE)
    if _game_render_cache['pause_font'] is None:
        _game_render_cache['pause_font'] = pygame.font.SysFont(None, PAUSE_FONT_SIZE)

    if hud_visible:
        game_mode = game.mode
        active_events = game.get_active_events_for_display()
        event_notifications = game.get_event_notifications()
        draw_hud(screen, player, fps=fps, game_mode=game_mode, active_events=active_events, event_notifications=event_notifications)
    # Handle hurt animation (non-interruptible)
    if player.anim_state in ('hurt_hp', 'hurt_barrier'):
        # Determine number of frames for current hurt animation
        if player.anim_state == 'hurt_hp':
            img = _game_render_cache['hurt_hp_img']
        else:
            img = _game_render_cache['hurt_barrier_img']
        num_frames = img.get_width() // PLAYER_SPRITE_FRAME_WIDTH
        duration = num_frames / PLAYER_HURT_ANIMATION_FPS
        draw_player_hurt(screen, player, player.anim_timer, barrier_damage=(player.anim_state=='hurt_barrier'))
        # Unlock animation if finished
        if player.anim_timer >= duration:
            player.anim_lock = False
            player.anim_state = 'idle'
            player.anim_timer = 0.0
    else:
        if last_move != (0, 0):
            if getattr(player, 'movement_speed', 0) >= 5:
                draw_player_run(screen, player, time_accum)
            else:
                draw_player_walk(screen, player, time_accum)
        else:
            draw_player_idle(screen, player, time_accum)

    # Draw all player skills (e.g., slash animation), pass last_move for direction
    for skill in player.skills.values():
        if hasattr(skill, 'draw'):
            skill.draw(screen, last_move=last_move)
    # Draw enemies and debug overlays
    if hasattr(game, 'enemies'):
        enemies = game.enemies
    else:
        enemies = []
    for enemy in getattr(game, 'enemies', []):
        enemy.draw(screen)
    # ...removed enemy count and player position debug overlays...

    # Draw GAME OVER overlay if needed
    if getattr(game, 'game_over', False):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill(GAME_OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))
        font = _game_render_cache['game_over_font']
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        font2 = _game_render_cache['menu_font']
        tip = font2.render("Press ESC or Enter to return to menu", True, (255, 255, 255))
        tip_rect = tip.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
        screen.blit(tip, tip_rect)

    # Draw pause menu overlay if paused
    if paused and not getattr(game, 'game_over', False):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill(PAUSE_OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))
        font = _game_render_cache['pause_font']
        text = font.render("Paused", True, PAUSE_MENU_TEXT_COLOR)
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 120))
        screen.blit(text, text_rect)
        font2 = _game_render_cache['menu_font']
        rects = []
        for i, option in enumerate(pause_menu_options or []):
            color = PAUSE_MENU_HIGHLIGHT_COLOR if i == pause_menu_selected else PAUSE_MENU_TEXT_COLOR
            opt_text = font2.render(option, True, color)
            opt_rect = opt_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 30 + i * 60))
            screen.blit(opt_text, opt_rect)
            # Add a slightly larger rect for mouse hitbox
            rects.append(opt_rect.inflate(40, 20))
        if pause_menu_rects is not None:
            pause_menu_rects.clear()
            pause_menu_rects.extend(rects)

    pygame.display.flip()
