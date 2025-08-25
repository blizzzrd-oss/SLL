"""
Projectile system for enemies and other entities.
"""

import pygame
import math
from audio.sound_manager import SoundManager


class Projectile:
    """Base class for all projectiles."""
    
    def __init__(self, start_pos, target_pos, speed, damage, owner=None, sprite_path=None):
        self.x, self.y = start_pos
        self.target_x, self.target_y = target_pos
        self.speed = speed
        self.damage = damage
        self.owner = owner  # Entity that fired this projectile
        self.active = True
        
        # Calculate direction vector
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        
        if distance > 0:
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0
        
        # Create collision rect - smaller for more precise collision
        self.rect = pygame.Rect(int(self.x), int(self.y), 4, 4)  # Very small collision box for precise hits
        
        # Load sprite if provided
        self.sprite = None
        if sprite_path:
            try:
                self.sprite = pygame.image.load(sprite_path).convert_alpha()
            except pygame.error:
                print(f"[WARNING] Could not load projectile sprite: {sprite_path}")
    
    def update(self, dt):
        """Update projectile position and check for expiration."""
        if not self.active:
            return
        
        # Move projectile
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.rect.center = (int(self.x), int(self.y))
        
        # Check if projectile has traveled too far (cleanup)
        start_distance = math.hypot(self.x - self.target_x, self.y - self.target_y)
        if start_distance > 1000:  # Remove if too far from target
            self.active = False
    
    def check_collision(self, target):
        """Check collision with a target entity."""
        if not self.active or not hasattr(target, 'rect'):
            return False
        
        return self.rect.colliderect(target.rect)
    
    def hit_target(self, target):
        """Handle hitting a target."""
        if hasattr(target, 'take_damage'):
            # Check if target supports 'attacker' parameter (enemies) or not (player)
            import inspect
            sig = inspect.signature(target.take_damage)
            if 'attacker' in sig.parameters:
                # Enemy-style take_damage method
                target.take_damage(self.damage, source=self, attacker=self.owner)
            else:
                # Player-style take_damage method - provide descriptive source
                source_name = "Unknown Projectile"
                if self.owner and hasattr(self.owner, 'type') and hasattr(self.owner.type, 'name'):
                    source_name = f"{self.owner.type.name} Projectile"
                elif isinstance(self, EnemyProjectile):
                    source_name = "Enemy Projectile"
                target.take_damage(self.damage, source=source_name)
        self.active = False
    
    def draw(self, surface, camera=None):
        """Draw the projectile."""
        if not self.active:
            return
        
        if camera:
            screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        else:
            screen_x, screen_y = int(self.x), int(self.y)
        
        if self.sprite:
            # Center the sprite on the projectile position
            sprite_rect = self.sprite.get_rect(center=(screen_x, screen_y))
            surface.blit(self.sprite, sprite_rect)
        else:
            # Draw a simple red circle if no sprite
            pygame.draw.circle(surface, (255, 100, 100), (screen_x, screen_y), 4)


class EnemyProjectile(Projectile):
    """Projectile fired by enemies at the player."""
    
    def __init__(self, start_pos, target_pos, speed=150, damage=5, owner=None):
        super().__init__(start_pos, target_pos, speed, damage, owner)
        # Enemy projectiles could have different properties than player projectiles
        self.rect = pygame.Rect(int(self.x), int(self.y), 6, 6)  # Slightly smaller


class ProjectileManager:
    """Manages all projectiles in the game."""
    
    def __init__(self):
        self.projectiles = []
    
    def add_projectile(self, projectile):
        """Add a projectile to be managed."""
        self.projectiles.append(projectile)
    
    def update(self, dt, player):
        """Update all projectiles and handle collisions."""
        for projectile in self.projectiles[:]:
            projectile.update(dt)
            
            # Remove inactive projectiles
            if not projectile.active:
                self.projectiles.remove(projectile)
                continue
            
            # Check collision with player (for enemy projectiles)
            if isinstance(projectile, EnemyProjectile) and projectile.check_collision(player):
                projectile.hit_target(player)
                self.projectiles.remove(projectile)
    
    def draw(self, surface, camera=None):
        """Draw all active projectiles."""
        for projectile in self.projectiles:
            projectile.draw(surface, camera)
    
    def clear(self):
        """Clear all projectiles."""
        self.projectiles.clear()
