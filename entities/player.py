"""
Player entity and logic.
"""

import pygame
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    PLAYER_START_HEALTH, PLAYER_START_BARRIER, PLAYER_BARRIER_DECAY_PERCENT_PER_SEC, PLAYER_BARRIER_REGEN,
    PLAYER_START_EXP, PLAYER_EXP_TO_NEXT_LEVEL_MULT, PLAYER_START_LEVEL, PLAYER_SIZE, PLAYER_MOVEMENT_SPEED,
    PLAYER_DAMAGE_REDUCTION, PLAYER_COOLDOWN, PLAYER_ATTACK_SPEED, PLAYER_CRIT_CHANCE, PLAYER_CRIT_DAMAGE,
    PLAYER_START_SKILL_POINTS, PLAYER_PASSIVE_SKILLS, PLAYER_ACTIVE_SKILLS
)

class Player:
    def __init__(self):
        # Start in the middle of the game window
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.size = PLAYER_SIZE
        self.health = PLAYER_START_HEALTH
        self.barrier = PLAYER_START_BARRIER
        self.barrier_decay_percent_per_sec = PLAYER_BARRIER_DECAY_PERCENT_PER_SEC
        self.barrier_regen = PLAYER_BARRIER_REGEN
        self.exp = PLAYER_START_EXP
        self.exp_to_next_level_mult = PLAYER_EXP_TO_NEXT_LEVEL_MULT
        self.level = PLAYER_START_LEVEL
        self.movement_speed = PLAYER_MOVEMENT_SPEED
        self.buffs = []  # List of current temporary positive effects
        self.debuffs = []  # List of current temporary negative effects
        self.skill_points = PLAYER_START_SKILL_POINTS
        self.passive_skills = PLAYER_PASSIVE_SKILLS.copy()
        self.active_skills = PLAYER_ACTIVE_SKILLS.copy()
        self.damage_reduction = PLAYER_DAMAGE_REDUCTION
        self.cooldown = PLAYER_COOLDOWN
        self.attack_speed = PLAYER_ATTACK_SPEED
        self.crit_chance = PLAYER_CRIT_CHANCE
        self.crit_damage = PLAYER_CRIT_DAMAGE
        # For compatibility with old code
        self.position = (self.x, self.y)
        self.damage_log = []
        self.recent_damage = []

    def take_damage(self, amount, source):
        self.health -= amount
        self.damage_log.append((amount, source))
        self.recent_damage.append((amount, source))
        # ...handle death, clear recent_damage, etc...
