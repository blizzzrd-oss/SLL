import pygame
import math
import os
from skills.base import Skill

DASH_RANGE = 100
DASH_COOLDOWN = 2.0
DASH_DURATION = 0.15  # seconds

class DashSkill(Skill):
    is_movement_skill = True
    def __init__(self, user, cooldown=DASH_COOLDOWN, dash_range=DASH_RANGE, duration=DASH_DURATION):
        super().__init__(user, cooldown)
        self.dash_range = dash_range
        self.duration = duration
        self.active = False
        self.dash_vector = (0, 0)
        self.dash_start = None
        self.dash_end = None
        self.elapsed = 0.0

    def use(self, target_pos=None):
        now = pygame.time.get_ticks() / 1000
        if not self.can_use(now):
            return False
        self.last_used = now
        self.active = True
        self.elapsed = 0.0
        # Use WASD movement direction for dash
        move_vec = getattr(self.user, 'last_move', (1, 0))
        dx, dy = move_vec
        dist = math.hypot(dx, dy)
        if dist == 0:
            norm_dx, norm_dy = 1, 0
        else:
            norm_dx, norm_dy = dx / dist, dy / dist
        self.dash_vector = (norm_dx, norm_dy)
        self.dash_start = (self.user.x, self.user.y)
        self.dash_end = (self.user.x + norm_dx * self.dash_range, self.user.y + norm_dy * self.dash_range)
        return True

    def update(self, dt, entities):
        if not self.active:
            return
        self.elapsed += dt
        t = min(self.elapsed / self.duration, 1.0)
        # Linear interpolation from start to end
        new_x = self.dash_start[0] + (self.dash_end[0] - self.dash_start[0]) * t
        new_y = self.dash_start[1] + (self.dash_end[1] - self.dash_start[1]) * t
        self.user.x = new_x
        self.user.y = new_y
        self.user.position = (new_x, new_y)
        self.user.rect.center = (int(new_x), int(new_y))
        if t >= 1.0:
            self.active = False

    def draw(self, surface, last_move=(1,0)):
        # Optionally, draw a dash effect (e.g., a trail or afterimage)
        pass

    def can_use(self, now):
        # Prevent dashing while already dashing
        return super().can_use(now) and not self.active
