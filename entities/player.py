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



from skills.registry import get_skill


class Player:

    def update(self, dt):
        # Barrier decay (float, smooth)
        if not hasattr(self, '_barrier_decay_accum'):
            self._barrier_decay_accum = 0.0
        if self.barrier > 0:
            decay = self.barrier * (self.barrier_decay_percent_per_sec / 100) * dt
            self._barrier_decay_accum += decay
            if self._barrier_decay_accum >= 1.0:
                to_sub = int(self._barrier_decay_accum)
                self.barrier = max(0, self.barrier - to_sub)
                self._barrier_decay_accum -= to_sub
        # TODO: barrier regen, buffs, debuffs, etc.
    # Animation states
    ANIM_IDLE = 'idle'
    ANIM_WALK = 'walk'
    ANIM_RUN = 'run'
    ANIM_HURT_HP = 'hurt_hp'
    ANIM_HURT_BARRIER = 'hurt_barrier'


    def __init__(self):
        # Start in the middle of the game window
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.size = PLAYER_SIZE
        self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
        self.facing_angle = 0  # Degrees, 0 = right

        # Skills config (must be set before registering skills)
        self.passive_skills = PLAYER_PASSIVE_SKILLS.copy()
        self.active_skills = PLAYER_ACTIVE_SKILLS.copy()
        # Skills system
        self.skills = {}
        for skill_name in self.active_skills:
            skill_cls = get_skill(skill_name)
            if skill_cls:
                self.skills[skill_name] = skill_cls(self)

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
        self.damage_reduction = PLAYER_DAMAGE_REDUCTION
        self.cooldown = PLAYER_COOLDOWN
        self.attack_speed = PLAYER_ATTACK_SPEED
        self.crit_chance = PLAYER_CRIT_CHANCE
        self.crit_damage = PLAYER_CRIT_DAMAGE

        # For compatibility with old code
        self.position = (self.x, self.y)
        self.damage_log = []
        self.recent_damage = []
        # Track last nonzero movement vector for dash direction
        self.last_move = (1, 0)


        # Animation state
        self.anim_state = self.ANIM_IDLE
        self.anim_timer = 0.0  # Time since animation started
        self.anim_lock = False  # If True, animation cannot be interrupted

        # Settings checkboxes (auto aim, auto attack) - sync with menu if possible
        try:
            import os, json
            settings_path = os.path.join(os.path.dirname(__file__), '..', 'settings.json')
            with open(settings_path, 'r') as f:
                data = json.load(f)
            self.checkbox_options = [
                {"label": "Auto Aim", "checked": bool(data.get('auto_aim', True))},
                {"label": "Auto Attack", "checked": bool(data.get('auto_attack', True))},
            ]
        except Exception:
            self.checkbox_options = [
                {"label": "Auto Aim", "checked": True},
                {"label": "Auto Attack", "checked": True},
            ]


    def take_damage(self, amount, source=None, barrier_damage=False):
        # Barrier absorbs damage first unless barrier_damage is True
        damage_to_health = amount
        if not barrier_damage and self.barrier > 0:
            absorbed = min(self.barrier, amount)
            self.barrier -= absorbed
            damage_to_health -= absorbed
            if absorbed > 0 and not self.anim_lock:
                self.anim_state = self.ANIM_HURT_BARRIER
                self.anim_timer = 0.0
                self.anim_lock = True
        if damage_to_health > 0:
            if not self.anim_lock:
                self.anim_state = self.ANIM_HURT_HP
                self.anim_timer = 0.0
                self.anim_lock = True
            self.health -= damage_to_health
        self.damage_log.append((amount, source))
        self.recent_damage.append((amount, source))
        # ...handle death, clear recent_damage, etc...
