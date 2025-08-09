"""
Player movement logic (input and movement updates).
"""
import pygame

def handle_player_movement(player, dt):
    """Handle WASD movement input for the player. dt is delta time in seconds."""
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_w]:
        dy -= 1
    if keys[pygame.K_s]:
        dy += 1
    if keys[pygame.K_a]:
        dx -= 1
    if keys[pygame.K_d]:
        dx += 1
    # Normalize diagonal movement
    if dx != 0 and dy != 0:
        dx *= 0.7071
        dy *= 0.7071
    player.x += dx * player.movement_speed * dt * 60
    player.y += dy * player.movement_speed * dt * 60
    player.position = (player.x, player.y)
