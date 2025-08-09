"""
Game main loop and event handling.
"""
import pygame
from core.player_movement import handle_player_movement
from rendering.player_render import draw_player_idle, draw_player_walk, draw_player_run, draw_player_hurt
from .game import Game
from config import PLAYER_HURT_ANIMATION_FPS, PLAYER_SPRITE_FRAME_WIDTH

def run_game(screen, slot, mode):
    game = Game(screen, slot, mode)
    running = True
    should_exit = False
    last_move = (0, 0)
    time_accum = 0.0
    clock = pygame.time.Clock()
    paused = False
    pause_menu_selected = 0
    pause_menu_options = ["Resume", "Surrender", "Settings", "Quit"]
    pause_menu_rects = []
    in_settings_menu = False
    # Always reset player state on new game
    game.reset()
    while running:
        dt = clock.tick(60) / 1000.0
        time_accum += dt
        move_dx, move_dy = 0, 0
        mouse_pos = pygame.mouse.get_pos()
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                should_exit = True
            # Game over input
            if game.game_over:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    should_exit = True
            # Pause menu logic
            elif not in_settings_menu and not game.game_over:
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
                            if option == "Resume":
                                paused = False
                            elif option == "Surrender":
                                should_exit = True
                            elif option == "Settings":
                                in_settings_menu = True
                            elif option == "Quit":
                                pygame.quit()
                                exit()
                    elif event.type == pygame.MOUSEMOTION:
                        for i, rect in enumerate(pause_menu_rects):
                            if rect.collidepoint(mouse_pos):
                                pause_menu_selected = i
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for i, rect in enumerate(pause_menu_rects):
                            if rect.collidepoint(mouse_pos):
                                option = pause_menu_options[i]
                                if option == "Resume":
                                    paused = False
                                elif option == "Surrender":
                                    should_exit = True
                                elif option == "Settings":
                                    in_settings_menu = True
                                elif option == "Quit":
                                    pygame.quit()
                                    exit()
            # Settings menu logic (modal, but non-blocking)
            elif in_settings_menu:
                from rendering.menu import Menu
                menu = Menu(screen)
                menu.state = 'settings'
                if menu.handle_event(event):
                    in_settings_menu = False
        # Draw settings menu if active
        if in_settings_menu:
            from rendering.menu import Menu
            menu = Menu(screen)
            menu.state = 'settings'
            menu.draw()
            pygame.display.flip()
            continue
        # Game logic and movement
        if not game.game_over and not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                move_dy -= 1
            if keys[pygame.K_s]:
                move_dy += 1
            if keys[pygame.K_a]:
                move_dx -= 1
            if keys[pygame.K_d]:
                move_dx += 1
            if move_dx != 0 and move_dy != 0:
                move_dx *= 0.7071
                move_dy *= 0.7071
            last_move = (move_dx, move_dy)
            handle_player_movement(game.player, dt)
        if not paused:
            game.update(dt)
        if game.player.anim_lock:
            game.player.anim_timer += dt
        draw_game(screen, game, last_move, time_accum, paused, pause_menu_selected, pause_menu_options, pause_menu_rects)
        if should_exit:
            break


def draw_game(screen, game, last_move, time_accum, paused=False, pause_menu_selected=0, pause_menu_options=None, pause_menu_rects=None):
    screen.fill((20, 20, 20))
    player = game.player
    # Handle hurt animation (non-interruptible)
    if player.anim_state in ('hurt_hp', 'hurt_barrier'):
        # Determine number of frames for current hurt animation
        if player.anim_state == 'hurt_hp':
            img = pygame.image.load('resources/images/player/Hurt/Slime1_Hurt_full_hp.png').convert_alpha()
        else:
            img = pygame.image.load('resources/images/player/Hurt/Slime1_Hurt_full_barrier.png').convert_alpha()
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
    # TODO: Draw monsters, loot, UI, etc.

    # Draw GAME OVER overlay if needed
    if getattr(game, 'game_over', False):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # 180/255 alpha for half transparency
        screen.blit(overlay, (0, 0))
        font = pygame.font.SysFont(None, 120)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        font2 = pygame.font.SysFont(None, 48)
        tip = font2.render("Press ESC or Enter to return to menu", True, (255, 255, 255))
        tip_rect = tip.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
        screen.blit(tip, tip_rect)

    # Draw pause menu overlay if paused
    if paused and not getattr(game, 'game_over', False):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))
        font = pygame.font.SysFont(None, 80)
        text = font.render("Paused", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 120))
        screen.blit(text, text_rect)
        font2 = pygame.font.SysFont(None, 48)
        rects = []
        for i, option in enumerate(pause_menu_options or []):
            color = (255, 255, 0) if i == pause_menu_selected else (255, 255, 255)
            opt_text = font2.render(option, True, color)
            opt_rect = opt_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 30 + i * 60))
            screen.blit(opt_text, opt_rect)
            # Add a slightly larger rect for mouse hitbox
            rects.append(opt_rect.inflate(40, 20))
        if pause_menu_rects is not None:
            pause_menu_rects.clear()
            pause_menu_rects.extend(rects)

    pygame.display.flip()
