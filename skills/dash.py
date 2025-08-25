import pygame
import math
import os
from skills.base import Skill
from config import DASH_RANGE, DASH_COOLDOWN, DASH_DURATION, DASH_DAMAGE
from audio.sound_manager import SoundManager

class DashSkill(Skill):
    is_movement_skill = True
    
    def __init__(self, user, cooldown=DASH_COOLDOWN, dash_range=DASH_RANGE, duration=DASH_DURATION, dash_damage=DASH_DAMAGE):
        super().__init__(user, cooldown, name="Dash")
        self.base_dash_range = dash_range
        self.dash_range = dash_range
        self.duration = duration
        self.dash_damage = dash_damage
        self.active = False
        self.dash_vector = (0, 0)
        self.dash_start = None
        self.dash_end = None
        self.elapsed = 0.0
        
        # Double dash enhancement
        self.max_charges = 1
        self.current_charges = 1
        self.charge_regen_time = 0
        self.last_charge_regen = 0

    def use(self, target_pos=None):
        now = pygame.time.get_ticks() / 1000
        
        # Check if we can use dash
        if not self.can_use(now):
            print(f"[DASH] Cannot use - active: {self.active}, charges: {self.current_charges}/{self.max_charges}")
            return False
            
        # Apply general enhancements
        self._apply_general_enhancements()
        
        # Apply dash range enhancement
        range_bonus = self.user.get_enhancement_value('increased_range', 'dash')
        effective_range = self.base_dash_range * (1.0 + range_bonus)
        
        # Play dash sound effect using sound manager
        SoundManager.play_skill_sound('dash')
        
        print(f"[DASH] Using dash - charges before: {self.current_charges}/{self.max_charges}")
                
        # Consume charge safely (prevent going negative)
        if self.current_charges > 0:
            self.current_charges = max(0, self.current_charges - 1)
        
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
        self.dash_end = (self.user.x + norm_dx * effective_range, self.user.y + norm_dy * effective_range)
        
        # Check for cooldown reset
        self._check_cooldown_reset()
        
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
        # Modular damage logic: deal damage to entities collided with during dash
        self.deal_damage(entities)
        if t >= 1.0:
            self.active = False

    def deal_damage(self, entities):
        # Deal damage to entities collided with during dash
        for entity in entities:
            if entity is self.user:
                continue
            # Simple collision: check rect overlap
            if hasattr(entity, 'rect') and self.user.rect.colliderect(entity.rect):
                if hasattr(entity, 'take_damage'):
                    damage = self._check_double_damage(self.dash_damage)
                    entity.take_damage(damage, source=self, attacker=self.user)

    def draw(self, surface, last_move=(1,0), camera=None):
        # Optionally, draw a dash effect (e.g., a trail or afterimage)
        pass

    def can_use(self, now):
        # Don't allow dashing while already dashing
        if self.active:
            return False
            
        # Update charges first
        self._update_charges(now)
        
        # Check if we have charges available
        if self.current_charges > 0:
            return True
        
        # If no charges, check normal cooldown
        return super().can_use(now)
    
    def _update_charges(self, now):
        """Update charge system for double dash enhancement."""
        # Update max charges based on enhancement
        double_dash_level = self.user.get_enhancement_level('double_dash', 'dash')
        self.max_charges = 1 + double_dash_level
        
        # Ensure current charges don't exceed max
        self.current_charges = min(self.current_charges, self.max_charges)
        
        if double_dash_level > 0:
            from config_enhancements import SKILL_SPECIFIC_ENHANCEMENTS
            self.charge_regen_time = SKILL_SPECIFIC_ENHANCEMENTS['dash']['double_dash']['charge_regen_time']
            
            # Regenerate charges over time
            if self.current_charges < self.max_charges:
                if self.last_charge_regen == 0:
                    self.last_charge_regen = now
                elif now - self.last_charge_regen >= self.charge_regen_time:
                    self.current_charges = min(self.max_charges, self.current_charges + 1)
                    self.last_charge_regen = now
                    print(f"[DASH] Regenerated charge: {self.current_charges}/{self.max_charges}")
