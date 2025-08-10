

import random
import time
from config import SPAWNER_DEFAULT_INTERVAL, SPAWNER_ENEMY_WEIGHTS, SPAWNER_TIME_WEIGHT_EVENTS, WINDOW_WIDTH, WINDOW_HEIGHT
from entities.enemy import PlantType, EnemyType, Enemy


class EnemySpawner:
    def __init__(self, enemy_types, get_game_time_fn=None, screen=None):
        """
        enemy_types: list of EnemyType
        get_game_time_fn: function returning current run time in seconds (optional)
        screen: pygame display surface (optional, for dynamic size)
        """
        self.enemy_types = enemy_types
        self.get_game_time = get_game_time_fn or (lambda: 0)
        self.last_spawn_time = 0
        self.spawn_interval = SPAWNER_DEFAULT_INTERVAL
        self.screen = screen

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

    def can_spawn(self):
        now = time.time()
        return (now - self.last_spawn_time) >= self.spawn_interval


    def random_edge_position(self):
        # Use actual window size if screen is available
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
        return Enemy(etype, position=pos)

# Example usage:
# from entities.enemy import PlantType
# spawner = EnemySpawner([PlantType])
# enemy = spawner.spawn((x, y))
