

import random
import time
from config import (
    SPAWNER_DEFAULT_INTERVAL, SPAWNER_ENEMY_WEIGHTS, SPAWNER_TIME_WEIGHT_EVENTS, 
    WINDOW_WIDTH, WINDOW_HEIGHT, SPAWNER_RATE_INCREASE_ENABLED, 
    SPAWNER_RATE_INCREASE_INTERVAL, SPAWNER_RATE_INCREASE_FACTOR, SPAWNER_MIN_INTERVAL
)
from entities.enemy import PlantType, EnemyType, Enemy


class EnemySpawner:
    def __init__(self, enemy_types, get_game_time_fn=None, screen=None, game=None):
        """
        enemy_types: list of EnemyType
        get_game_time_fn: function returning current run time in seconds (optional)
        screen: pygame display surface (optional, for dynamic size)
        game: Game instance (for mode multipliers)
        """
        self.enemy_types = enemy_types
        self.get_game_time = get_game_time_fn or (lambda: 0)
        self.last_spawn_time = 0
        self.spawn_interval = SPAWNER_DEFAULT_INTERVAL
        self.screen = screen
        self.game = game  # Store game instance for mode multipliers

    def choose_enemy_type(self):
        t = self.get_game_time()
        weights = []
        for etype in self.enemy_types:
            weight = SPAWNER_ENEMY_WEIGHTS.get(etype.name, 1.0)
            for event in SPAWNER_TIME_WEIGHT_EVENTS:
                enemy_name, time_threshold, multiplier = event
                if etype.name == enemy_name and t > time_threshold:
                    weight *= multiplier
            weights.append(weight)
        total = sum(weights)
        r = random.uniform(0, total)
        upto = 0
        for etype, w in zip(self.enemy_types, weights):
            if upto + w >= r:
                return etype
            upto += w
        return self.enemy_types[0]  # fallback

    def get_current_spawn_interval(self):
        """Calculate the current spawn interval based on game time."""
        if not SPAWNER_RATE_INCREASE_ENABLED:
            return self.spawn_interval
            
        game_time = self.get_game_time()
        
        # Calculate how many rate increases should have occurred
        rate_increases = int(game_time // SPAWNER_RATE_INCREASE_INTERVAL)
        
        # Apply the rate increase factor for each interval
        current_interval = self.spawn_interval
        for _ in range(rate_increases):
            current_interval *= SPAWNER_RATE_INCREASE_FACTOR
            
        # Ensure we don't go below minimum interval
        return max(current_interval, SPAWNER_MIN_INTERVAL)

    def can_spawn(self):
        now = time.time()
        current_interval = self.get_current_spawn_interval()
        return (now - self.last_spawn_time) >= current_interval


    def random_edge_position(self):
        # Spawn enemies around the player's world position, not screen edges
        if self.game and hasattr(self.game, 'player'):
            player_x = self.game.player.x
            player_y = self.game.player.y
            
            # Use screen dimensions to determine spawn distance from player
            if self.screen:
                width, height = self.screen.get_width(), self.screen.get_height()
            else:
                width, height = WINDOW_WIDTH, WINDOW_HEIGHT
            
            # Spawn slightly outside the visible area around the player
            spawn_distance = max(width, height) // 2 + 100  # A bit beyond screen edge
            
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top':
                return (player_x + random.randint(-width//2, width//2), player_y - spawn_distance)
            elif edge == 'bottom':
                return (player_x + random.randint(-width//2, width//2), player_y + spawn_distance)
            elif edge == 'left':
                return (player_x - spawn_distance, player_y + random.randint(-height//2, height//2))
            else:  # right
                return (player_x + spawn_distance, player_y + random.randint(-height//2, height//2))
        else:
            # Fallback to old method if no game/player reference
            if self.screen:
                width, height = self.screen.get_width(), self.screen.get_height()
            else:
                width, height = WINDOW_WIDTH, WINDOW_HEIGHT
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top':
                return (random.randint(0, width), 0)
            elif edge == 'bottom':
                return (random.randint(0, width), height)
            elif edge == 'left':
                return (0, random.randint(0, height))
            else:
                return (width, random.randint(0, height))

    def spawn_if_ready(self):
        if not self.can_spawn():
            return None
        etype = self.choose_enemy_type()
        self.last_spawn_time = time.time()
        pos = self.random_edge_position()
        enemy = Enemy(etype, position=pos)
        
        # Apply game mode multipliers if game instance is available
        if self.game and hasattr(self.game, 'mode_config'):
            self._apply_mode_multipliers(enemy)
        
        return enemy
    
    def _apply_mode_multipliers(self, enemy):
        """Apply game mode multipliers to a spawned enemy"""
        config = self.game.mode_config
        
        # Apply health multiplier
        original_health = enemy.type.max_health
        enemy.health = int(original_health * config['enemy_health_multiplier'])
        enemy.max_health = enemy.health  # Store modified max health
        
        # Store multipliers for damage and speed (applied during gameplay)
        enemy.mode_damage_multiplier = config['enemy_damage_multiplier']
        enemy.mode_speed_multiplier = config['enemy_speed_multiplier']
        
        # Apply speed multiplier to the enemy's type speed
        if hasattr(enemy, 'logic') and enemy.logic:
            # Speed will be applied in the logic update methods
            pass

# Example usage:
# from entities.enemy import PlantType
# spawner = EnemySpawner([PlantType])
# enemy = spawner.spawn((x, y))
