"""
Player movement logic (input and movement updates).
"""
import pygame

def get_movement_vector():
    """Return (dx, dy) movement vector based on WASD keys, normalized for diagonal movement."""
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
    if dx != 0 and dy != 0:
        dx *= 0.7071
        dy *= 0.7071
    return dx, dy

def handle_player_movement(player, dt):
    """Handle WASD movement input for the player. dt is delta time in seconds."""
    dx, dy = get_movement_vector()
    # Update last_move if there is movement
    if (dx, dy) != (0, 0):
        player.last_move = (dx, dy)
    player.x += dx * player.movement_speed * dt * 60
    player.y += dy * player.movement_speed * dt * 60
    player.position = (player.x, player.y)
