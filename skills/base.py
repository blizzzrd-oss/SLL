

import pygame
from abc import ABC, abstractmethod
from config import SKILL_COOLDOWN

class Skill(ABC):
    def __init__(self, user, cooldown=None):
        self.user = user
        self.cooldown = SKILL_COOLDOWN if cooldown is None else cooldown
        self.last_used = -float('inf')
        self.active = False
        self.animation_frame = 0

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
        return (now - self.last_used) >= self.cooldown
