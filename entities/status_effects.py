"""
Enemy Status Effects System
Manages temporary effects applied to enemies (stun, knockback, etc.)
"""

import time


class StatusEffect:
    """Base class for status effects."""
    
    def __init__(self, duration):
        self.duration = duration
        self.start_time = time.time()
        self.active = True
    
    def is_expired(self):
        """Check if the status effect has expired."""
        return time.time() - self.start_time >= self.duration
    
    def apply(self, enemy):
        """Apply the status effect to an enemy."""
        pass
    
    def remove(self, enemy):
        """Remove the status effect from an enemy."""
        pass


class StunEffect(StatusEffect):
    """Stun effect that prevents enemy movement."""
    
    def __init__(self, duration=1.0):
        super().__init__(duration)
        self.original_speed = None
        self.applied = False
    
    def apply(self, enemy):
        """Apply stun to enemy."""
        if not self.applied:
            # Store original speed only once
            self.original_speed = getattr(enemy, 'movement_speed', 1.0)
            self.applied = True
            
        enemy.movement_speed = 0
        enemy.is_stunned = True
        # If the enemy has a logic object with an ongoing attack, cancel it so
        # the stun immediately prevents any pending damage from completing.
        # This covers cases where an enemy was mid-attack when stunned.
        if hasattr(enemy, 'logic') and enemy.logic:
            logic = enemy.logic
            # Safely reset animation/attack state if present
            # If the enemy is currently playing its death animation, do not
            # override the death state or reset its animation counters. Stun
            # should prevent behavior but must not interrupt death visuals.
            if hasattr(logic, 'state') and getattr(logic, 'state') == 'death':
                # Leave death animation/state untouched
                pass
            else:
                if hasattr(logic, 'state'):
                    try:
                        # Move enemy back to a non-attacking movement state
                        logic.state = 'run' if getattr(enemy, 'movement_speed', 0) > 4 else 'walk'
                    except Exception:
                        pass
                if hasattr(logic, 'anim_frame'):
                    try:
                        logic.anim_frame = 0
                    except Exception:
                        pass
                if hasattr(logic, 'anim_timer'):
                    try:
                        logic.anim_timer = 0.0
                    except Exception:
                        pass
                # Clear any damage-dealt flag used to prevent double-hits
                if hasattr(logic, '_damage_dealt'):
                    try:
                        logic._damage_dealt = False
                    except Exception:
                        pass
    
    def remove(self, enemy):
        """Remove stun from enemy."""
        if self.original_speed is not None:
            enemy.movement_speed = self.original_speed
        enemy.is_stunned = False


class KnockbackEffect(StatusEffect):
    """Knockback effect that pushes enemy away."""
    
    def __init__(self, force, direction, duration=0.3):
        super().__init__(duration)
        self.force = force
        self.direction = direction  # (dx, dy) normalized
        self.applied = False
    
    def apply(self, enemy):
        """Apply knockback to enemy."""
        if not self.applied:
            # Apply immediate position change
            enemy.x += self.direction[0] * self.force
            enemy.y += self.direction[1] * self.force
            
            # Update enemy rect if it exists
            if hasattr(enemy, 'rect'):
                enemy.rect.centerx = enemy.x
                enemy.rect.centery = enemy.y
            
            self.applied = True
    
    def remove(self, enemy):
        """Knockback removal doesn't need special handling."""
        pass


class EnemyStatusManager:
    """Manages status effects for enemies."""
    
    def __init__(self):
        self.effects = []
    
    def add_effect(self, effect):
        """Add a status effect."""
        self.effects.append(effect)
    
    def update(self, dt, enemy):
        """Update all status effects."""
        # Apply active effects
        for effect in self.effects:
            if effect.active:
                effect.apply(enemy)
        
        # Remove expired effects
        expired_effects = []
        for effect in self.effects:
            if effect.is_expired():
                effect.remove(enemy)
                expired_effects.append(effect)
        
        # Clean up expired effects
        for effect in expired_effects:
            self.effects.remove(effect)
    
    def has_effect_type(self, effect_class):
        """Check if enemy has a specific type of effect."""
        return any(isinstance(effect, effect_class) for effect in self.effects)
    
    def clear_all_effects(self, enemy):
        """Remove all status effects."""
        for effect in self.effects:
            effect.remove(enemy)
        self.effects.clear()
