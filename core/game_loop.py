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
    last_move = (0, 0)
    time_accum = 0.0
    clock = pygame.time.Clock()
    while running:
        dt = clock.tick(60) / 1000.0
        time_accum += dt
        move_dx, move_dy = 0, 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle game over input
            if game.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        game.reset()
                        return  # Return to main menu (handled by caller)
            # TODO: Handle input, skills, inventory, etc.
        if not game.game_over:
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
        game.update(dt)
        # Update animation timer if locked
        if game.player.anim_lock:
            game.player.anim_timer += dt
        draw_game(screen, game, last_move, time_accum)


def draw_game(screen, game, last_move, time_accum):
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

    pygame.display.flip()
