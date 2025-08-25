
import pygame
import random
from abc import ABC, abstractmethod
from config import SKILL_COOLDOWN

class Skill(ABC):
    def __init__(self, user, cooldown=None, name=None):
        self.user = user
        self.base_cooldown = SKILL_COOLDOWN if cooldown is None else cooldown
        self.cooldown = self.base_cooldown
        self.last_used = -float('inf')
        self.active = False
        self.animation_frame = 0
        self.name = name if name is not None else self.__class__.__name__
        
        # Enhancement-related attributes
        self.base_size = 1.0  # Base size multiplier
        self.size_multiplier = 1.0  # Current size including enhancements

    @abstractmethod
    def use(self, target_pos=None):
        pass

    @abstractmethod
    def update(self, dt, entities):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    def can_use(self, now):
        # Apply cooldown reduction enhancement
        effective_cooldown = self._get_effective_cooldown()
        return (now - self.last_used) >= effective_cooldown
    
    def _get_effective_cooldown(self):
        """Calculate effective cooldown with enhancements."""
        cooldown_reduction = self.user.get_enhancement_value('cooldown_reduction')
        return self.base_cooldown * (1.0 - cooldown_reduction)
    
    def _apply_general_enhancements(self):
        """Apply general enhancements that affect all skills."""
        # Update size multiplier
        aoe_bonus = self.user.get_enhancement_value('increased_aoe')
        self.size_multiplier = self.base_size * (1.0 + aoe_bonus)
    
    def _check_cooldown_reset(self):
        """Check if cooldown should be reset due to enhancement."""
        reset_chance = self.user.get_enhancement_value('cooldown_reset_chance')
        if reset_chance > 0 and random.random() < reset_chance:
            self.last_used = -float('inf')  # Reset cooldown immediately
            return True
        return False
    
    def _check_double_damage(self, base_damage):
        """Check if damage should be doubled due to enhancement."""
        double_chance = self.user.get_enhancement_value('double_damage_chance')
        if double_chance > 0 and random.random() < double_chance:
            return base_damage * 2
        return base_damage
    
    def _apply_skill_specific_enhancements(self):
        """Apply skill-specific enhancements. Override in subclasses."""
        pass
