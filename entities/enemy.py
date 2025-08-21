# Import plant logic
from entities.plant_logic import PlantEnemyLogic
from config import ENEMY_TYPE_CONFIG
import pygame
"""
Enemy entity and logic.
"""



# EnemyType: defines archetype attributes and skills for enemies
class EnemyType:
    def __init__(self, name, max_health, size, skills=None, speed=1.0, color=(255,0,0), logic_cls=None, attack_range=32, attack_damage=5):
        self.name = name
        self.max_health = max_health
        self.size = size
        self.skills = skills or []
        self.speed = speed
        self.color = color
        self.logic_cls = logic_cls
        self.attack_range = attack_range
        self.attack_damage = attack_damage

# Enemy: instance of an enemy in the game, based on EnemyType
class Enemy:
    def take_damage(self, amount, source=None, attacker=None):
        # If already dead or in death animation, ignore further damage
        if self.dead or (self.logic and hasattr(self.logic, 'state') and self.logic.state == 'death'):
            return

        self.health -= amount

        # Log outgoing damage for player stats if attacker is a Player
        if attacker and hasattr(attacker, 'damage_log'):
            attacker.damage_log.add_entry(amount, source, self.__class__.__name__)

        # Handle death or hurt visual feedback
        if self.logic and hasattr(self.logic, 'state'):
            if self.health <= 0:
                # Death overrides everything
                prev_state = self.logic.state
                self.logic.state = 'death'
                self.logic.anim_frame = 0
                self.logic.anim_timer = 0.0
                
                # Play death sound if state changed to death (only once)
                if prev_state != 'death' and hasattr(self.logic, '_death_sounds_cache'):
                    if self.logic._death_sounds_cache is not None and len(self.logic._death_sounds_cache) > 0:
                        try:
                            # Randomly select one of the death sounds
                            import random
                            random_sound = random.choice(self.logic._death_sounds_cache)
                            random_sound.play()
                        except Exception as e:
                            print(f"[WARNING] Failed to play enemy death sound: {e}")
                
                # Fix position for death animation to prevent jitter
                if hasattr(self.logic, 'fixed_draw_pos'):
                    self.logic.fixed_draw_pos = (int(self.position[0]), int(self.position[1]))
            else:
                # Trigger hurt overlay without changing state
                if hasattr(self.logic, 'hurt_overlay_timer') and hasattr(self.logic, 'hurt_overlay_duration'):
                    self.logic.hurt_overlay_timer = self.logic.hurt_overlay_duration
        # Don't set dead = True here, let the death animation complete first
    def __init__(self, enemy_type, position=(0, 0)):
        self.type = enemy_type
        self.health = enemy_type.max_health
        self.position = position
        self.size = enemy_type.size
        self.rect = pygame.Rect(self.position[0] - self.size // 2, self.position[1] - self.size // 2, self.size, self.size)
        self.facing_angle = 0
        self.skills = {name: skill for name, skill in (enemy_type.skills or [])}
        self.speed = enemy_type.speed
        self.color = enemy_type.color
        self.logic = enemy_type.logic_cls(self) if enemy_type.logic_cls else None
        self.dead = False
        # ...other attributes...

    def update(self, dt, player):
        if self.logic:
            self.logic.update(dt, player)
        # Don't automatically set dead = True here, let the logic handle it
        # after death animation completes

    def draw(self, surface, camera=None):
        # Use sprite logic if available, else fallback to debug circle
        if self.logic and hasattr(self.logic, 'draw'):
            self.logic.draw(surface, camera=camera)
        else:
            # Apply camera transformation for fallback circle
            if camera:
                screen_x, screen_y = camera.world_to_screen(self.position[0], self.position[1])
            else:
                screen_x, screen_y = int(self.position[0]), int(self.position[1])
            pygame.draw.circle(surface, (220, 40, 40), (screen_x, screen_y), self.size // 2)

# Register the Plant enemy type using config
plant_cfg = ENEMY_TYPE_CONFIG['Plant']
PlantType = EnemyType(
    name='Plant',
    max_health=plant_cfg['max_health'],
    size=plant_cfg['size'],
    speed=plant_cfg['speed'],
    color=plant_cfg['color'],
    logic_cls=PlantEnemyLogic,
    attack_range=plant_cfg.get('attack_range', 32),
    attack_damage=plant_cfg.get('attack_damage', 5)
)
