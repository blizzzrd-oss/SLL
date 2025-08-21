"""
Player entity and logic.
"""

import pygame
import os
import json
from skills.base import Skill
from audio.sound_manager import SoundManager
from config import (
    WORLD_SIZE, PLAYER_START_HEALTH, PLAYER_START_BARRIER, PLAYER_BARRIER_DECAY_PERCENT_PER_SEC, PLAYER_BARRIER_REGEN,
    PLAYER_START_EXP, PLAYER_START_LEVEL, PLAYER_BASE_EXP_REQUIREMENT, PLAYER_EXP_REQUIREMENT_BONUS, PLAYER_MAX_LEVEL,
    PLAYER_SIZE, PLAYER_MOVEMENT_SPEED, PLAYER_DAMAGE_REDUCTION, PLAYER_COOLDOWN, PLAYER_ATTACK_SPEED, 
    PLAYER_CRIT_CHANCE, PLAYER_CRIT_DAMAGE, PLAYER_START_SKILL_POINTS, PLAYER_PASSIVE_SKILLS, PLAYER_ACTIVE_SKILLS,
    PLAYER_AUTO_AIM, PLAYER_AUTO_ATTACK
)
from utils.player_damage_log import PlayerDamageLog
from utils.player_received_log import PlayerReceivedLog
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
        # Start in the middle of a large world
        self.x = WORLD_SIZE // 2
        self.y = WORLD_SIZE // 2
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
        self.max_health = PLAYER_START_HEALTH  # Add max_health attribute
        self.barrier = PLAYER_START_BARRIER
        self.barrier_decay_percent_per_sec = PLAYER_BARRIER_DECAY_PERCENT_PER_SEC
        self.barrier_regen = PLAYER_BARRIER_REGEN
        
        # Experience and Leveling System (Additive)
        self.exp = PLAYER_START_EXP
        self.level = PLAYER_START_LEVEL
        self.max_level = PLAYER_MAX_LEVEL
        
        # Other stats
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
        self.position = [self.x, self.y]  # Make this a mutable list
        self.damage_log = PlayerDamageLog()
        self.received_log = PlayerReceivedLog()
        self.last_move = (1, 0)


        # Animation state
        self.anim_state = self.ANIM_IDLE
        self.anim_timer = 0.0  # Time since animation started
        self.anim_lock = False  # If True, animation cannot be interrupted

        # Settings checkboxes (auto aim, auto attack) - sync with menu if possible
        try:
            settings_path = os.path.join(os.path.dirname(__file__), '..', 'settings.json')
            with open(settings_path, 'r') as f:
                data = json.load(f)
            self.checkbox_options = [
                {"label": "Auto Aim", "checked": bool(data.get('auto_aim', PLAYER_AUTO_AIM))},
                {"label": "Auto Attack", "checked": bool(data.get('auto_attack', PLAYER_AUTO_ATTACK))},
            ]
        except Exception:
            self.checkbox_options = [
                {"label": "Auto Aim", "checked": PLAYER_AUTO_AIM},
                {"label": "Auto Attack", "checked": PLAYER_AUTO_ATTACK},
            ]


    def take_damage(self, amount, source=None, barrier_damage=False):
        # Barrier absorbs damage first unless barrier_damage is True
        damage_to_health = amount
        # Use actual skill name for damage logging
        if source and hasattr(source, 'name') and isinstance(source.name, str):
            skill_name = source.name
        elif isinstance(source, str):
            skill_name = source
        else:
            skill_name = 'Unknown'
        # Track barrier damage
        if not barrier_damage and self.barrier > 0:
            absorbed = min(self.barrier, amount)
            self.barrier -= absorbed
            damage_to_health -= absorbed
            if absorbed > 0 and not self.anim_lock:
                self.anim_state = self.ANIM_HURT_BARRIER
                self.anim_timer = 0.0
                self.anim_lock = True
                # Play hit sound for barrier damage
                SoundManager.play_hit_sound('player')
            # Log barrier reduction
            self.received_log.add_entry(-absorbed, skill_name, 'damage', health=self.health, barrier=self.barrier)
        if damage_to_health > 0:
            if not self.anim_lock:
                self.anim_state = self.ANIM_HURT_HP
                self.anim_timer = 0.0
                self.anim_lock = True
                # Play hit sound for health damage
                SoundManager.play_hit_sound('player')
            self.health -= damage_to_health
            # Log health reduction
            self.received_log.add_entry(-damage_to_health, skill_name, 'damage', health=self.health, barrier=self.barrier)
        # Log outgoing damage (only if source is a Skill instance)
        if isinstance(source, Skill):
            self.damage_log.add_entry(amount, skill_name, 'Enemy')
        # ...handle death, clear recent_damage, etc...
    def heal(self, amount, source=None):
        if source and hasattr(source, 'name') and isinstance(source.name, str):
            skill_name = source.name
        elif isinstance(source, str):
            skill_name = source
        else:
            skill_name = 'Unknown'
        self.health = min(self.max_health, self.health + amount)
        self.received_log.add_entry(amount, skill_name, 'heal', health=self.health, barrier=self.barrier)

    def get_exp_to_next_level(self):
        """Calculate XP required for next level using additive bonus system."""
        if self.level >= self.max_level:
            return 0  # Max level reached
        
        # Calculate additive bonus: each level adds 10% to the base requirement
        level_bonus = (self.level - 1) * PLAYER_EXP_REQUIREMENT_BONUS  # -1 because level 1->2 has no bonus
        total_requirement = PLAYER_BASE_EXP_REQUIREMENT * (1.0 + level_bonus)
        return int(total_requirement)
    
    def add_experience(self, amount):
        """Add experience and handle level ups."""
        if self.level >= self.max_level:
            return False  # No more leveling possible
        
        self.exp += amount
        leveled_up = False
        
        # Check for level ups (can level multiple times with large XP gains)
        while self.level < self.max_level and self.exp >= self.get_exp_to_next_level():
            self.exp -= self.get_exp_to_next_level()
            self.level += 1
            leveled_up = True
            
            # Gain skill point on level up
            self.skill_points += 1
            
            print(f"[PLAYER] Level up! Now level {self.level}")
            
            # Optional: Add level up bonuses (health, damage, etc.)
            self._apply_level_up_bonuses()
        
        return leveled_up
    
    def _apply_level_up_bonuses(self):
        """Apply stat bonuses when leveling up."""
        # Small health increase per level (additive)
        health_bonus = 5  # +5 HP per level
        self.max_health += health_bonus
        self.health += health_bonus  # Also heal the player
        
        # Small damage increase per level (additive)
        damage_bonus = 0.02  # +2% damage per level
        self.crit_damage += damage_bonus
        
        print(f"[PLAYER] Level {self.level}: +{health_bonus} HP, +{damage_bonus*100:.0f}% crit damage")
    
    def get_experience_progress(self):
        """Get current XP progress as percentage (0.0 to 1.0)."""
        if self.level >= self.max_level:
            return 1.0
        
        exp_needed = self.get_exp_to_next_level()
        if exp_needed <= 0:
            return 1.0
        
        return min(self.exp / exp_needed, 1.0)
