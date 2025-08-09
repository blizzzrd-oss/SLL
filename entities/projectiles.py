"""
Projectile logic for both player and enemy projectiles.
"""
class Projectile:
    def __init__(self, position, direction, speed, damage, owner_type):
        self.position = position
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.owner_type = owner_type  # 'player' or 'enemy'
