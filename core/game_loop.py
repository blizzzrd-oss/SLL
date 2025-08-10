
"""
Game main loop and event handling.
"""
import pygame
import time
import json
#import os
from core.player_movement import handle_player_movement, get_movement_vector
from core.init import initialize_game_state
#from rendering.player_render import draw_player_idle, draw_player_walk, draw_player_run, draw_player_hurt
from rendering.game_render import draw_game
from core.game import Game
#from config import (PLAYER_HURT_ANIMATION_FPS, PLAYER_SPRITE_FRAME_WIDTH, GAME_BG_COLOR, GAME_OVERLAY_COLOR, PAUSE_OVERLAY_COLOR, GAME_OVER_FONT_SIZE, PAUSE_FONT_SIZE, MENU_FONT_SIZE, PAUSE_MENU_HIGHLIGHT_COLOR, PAUSE_MENU_TEXT_COLOR, PAUSE_MENU_OPTIONS, HUD_TOGGLE_KEY)
from config import (HUD_TOGGLE_KEY)
from rendering.menu import Menu
#from rendering.ui import draw_hud

def run_game(screen, slot, mode):
    (
        game, running, should_exit, last_move, time_accum, clock, paused, pause_menu_selected,
        pause_menu_options, pause_menu_rects, in_settings_menu, settings_menu, hud_visible, settings_path
    ) = initialize_game_state(screen, slot, mode)

    def handle_events():
        nonlocal running, should_exit, paused, pause_menu_selected, in_settings_menu, settings_menu, hud_visible
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                should_exit = True
            elif game.game_over:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    should_exit = True
            elif event.type == pygame.KEYDOWN and event.key == HUD_TOGGLE_KEY:
                hud_visible = not hud_visible
            elif not in_settings_menu and not game.game_over:
                # Player skill input (slash on LMB)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Use slash skill toward mouse position
                    if 'slash' in game.player.skills:
                        mouse_pos = pygame.mouse.get_pos()
                        game.player.skills['slash'].use(target_pos=mouse_pos)
                # Player skill input (dash on SPACE)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if 'dash' in game.player.skills:
                        mouse_pos = pygame.mouse.get_pos()
                        game.player.skills['dash'].use(target_pos=mouse_pos)
                handle_pause_menu_events(event, mouse_pos)
            elif in_settings_menu:
                handle_settings_menu_events(event)

    def handle_pause_menu_events(event, mouse_pos):
        nonlocal paused, pause_menu_selected, in_settings_menu, settings_menu, should_exit
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused = not paused
        if paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pause_menu_selected = (pause_menu_selected - 1) % len(pause_menu_options)
                elif event.key == pygame.K_DOWN:
                    pause_menu_selected = (pause_menu_selected + 1) % len(pause_menu_options)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    option = pause_menu_options[pause_menu_selected]
                    process_pause_menu_option(option)
            elif event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(pause_menu_rects):
                    if rect.collidepoint(mouse_pos):
                        pause_menu_selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(pause_menu_rects):
                    if rect.collidepoint(mouse_pos):
                        option = pause_menu_options[i]
                        process_pause_menu_option(option)

    def process_pause_menu_option(option):
        nonlocal paused, in_settings_menu, settings_menu, should_exit
        if option == "Resume":
            paused = False
        elif option == "Surrender":
            should_exit = True
        elif option == "Settings":
            in_settings_menu = True
            if settings_menu is None:
                settings_menu = Menu(screen)
                settings_menu.state = 'settings'
        elif option == "Quit":
            pygame.quit()
            exit()


    def handle_settings_menu_events(event):
        nonlocal in_settings_menu, settings_menu
        if settings_menu is None:
            settings_menu = Menu(screen)
            settings_menu.state = 'settings'
        if settings_menu.handle_event(event):
            in_settings_menu = False
            settings_menu = None

    def show_settings_menu_if_active():
        nonlocal settings_menu
        if in_settings_menu:
            if settings_menu is None:
                settings_menu = Menu(screen)
                settings_menu.state = 'settings'
            settings_menu.draw()
            pygame.display.flip()
            return True
        return False

    def get_frame_timing(clock, settings_path, time_accum):
        """Load FPS from settings, advance clock, and update time accumulator. Returns (dt, time_accum, fps)."""
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
            fps = int(settings.get('fps', 60))
        except Exception:
            fps = 60
        dt = clock.tick(fps) / 1000.0
        time_accum += dt
        return dt, time_accum, fps




    ###### MAIN GAME LOOP ######
    while running:
        # profiling if needed
        #frame_start = time.perf_counter()
        dt, time_accum, fps = get_frame_timing(clock, settings_path, time_accum)
        move_dx, move_dy = 0, 0

        handle_events()

        # Draw settings menu if active
        if show_settings_menu_if_active():
            continue

        # Game logic and movement
        if not game.game_over and not paused:
            move_dx, move_dy = get_movement_vector()
            # If there is movement, update last_move on the player
            if (move_dx, move_dy) != (0, 0):
                game.player.last_move = (move_dx, move_dy)
            last_move = (move_dx, move_dy)
            handle_player_movement(game.player, dt)
        if not paused:
            game.update(dt)
            # Update all player skills
            for skill in game.player.skills.values():
                skill.update(dt, [])  # TODO: pass list of entities for hit detection
        if game.player.anim_lock:
            game.player.anim_timer += dt

        # Draw game and all player skills (skills now drawn inside draw_game)
        draw_game(screen, game, last_move, time_accum, paused, pause_menu_selected, pause_menu_options, pause_menu_rects, hud_visible, clock.get_fps())
        if should_exit:
            break
        # Simple profiling: print frame time in ms
        #frame_end = time.perf_counter()
        #print(f"Frame time: {(frame_end - frame_start) * 1000:.2f} ms")

