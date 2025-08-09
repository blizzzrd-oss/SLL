"""
Game main loop and event handling.
"""
import pygame
from core.player_movement import handle_player_movement
from rendering.player_render import draw_player_idle, draw_player_walk, draw_player_run
from .game import Game

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
            # TODO: Handle input, skills, inventory, etc.
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
        draw_game(screen, game, last_move, time_accum)


def draw_game(screen, game, last_move, time_accum):
    screen.fill((20, 20, 20))
    if last_move != (0, 0):
        if getattr(game.player, 'movement_speed', 0) >= 5:
            draw_player_run(screen, game.player, time_accum)
        else:
            draw_player_walk(screen, game.player, time_accum)
    else:
        draw_player_idle(screen, game.player, time_accum)
    # TODO: Draw monsters, loot, UI, etc.
    pygame.display.flip()
