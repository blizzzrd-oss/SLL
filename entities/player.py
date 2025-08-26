"""
Player entity and logic.
"""

import pygame
import os
import json
from skills.base import Skill
from skills.enhancements import SkillEnhancementManager
from audio.sound_manager import SoundManager
from config import (
    WORLD_SIZE, PLAYER_START_HEALTH, PLAYER_START_BARRIER, PLAYER_BARRIER_DECAY_PERCENT_PER_SEC, PLAYER_BARRIER_REGEN,
    PLAYER_START_EXP, PLAYER_START_LEVEL, PLAYER_BASE_EXP_REQUIREMENT, PLAYER_EXP_REQUIREMENT_BONUS, PLAYER_MAX_LEVEL,
    PLAYER_SIZE, PLAYER_MOVEMENT_SPEED, PLAYER_PICKUP_RANGE, PLAYER_DAMAGE_REDUCTION, PLAYER_COOLDOWN, PLAYER_ATTACK_SPEED, 
    PLAYER_CRIT_CHANCE, PLAYER_CRIT_DAMAGE, PLAYER_START_SKILL_POINTS, PLAYER_PASSIVE_SKILLS, PLAYER_ACTIVE_SKILLS,
    PLAYER_AUTO_AIM, PLAYER_AUTO_ATTACK
)
from utils.player_damage_log import PlayerDamageLog
from utils.player_received_log import PlayerReceivedLog
from skills.registry import get_skill


class Player:

    def update(self, dt):
        # Apply movement speed enhancement
        base_movement_speed = PLAYER_MOVEMENT_SPEED
        movement_speed_bonus = self.enhancement_manager.get_enhancement_value('movement_speed')
        self.movement_speed = base_movement_speed * (1.0 + movement_speed_bonus)
        
        # Apply life regeneration enhancement
        life_regen = self.enhancement_manager.get_enhancement_value('life_regeneration')
        if life_regen > 0 and self.health < self.max_health:
            self.health = min(self.max_health, self.health + life_regen * dt)
        
        # Apply barrier regeneration enhancement
        barrier_regen = self.enhancement_manager.get_enhancement_value('barrier_regeneration')
        if barrier_regen > 0 and self.barrier < self.max_barrier:
            self.barrier = min(self.max_barrier, self.barrier + barrier_regen * dt)
        
        # Update immunity timer
        if self.is_immune and self.immunity_timer > 0:
            self.immunity_timer -= dt
            if self.immunity_timer <= 0:
                self.is_immune = False
                self.immunity_timer = 0.0
        
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
        
        # Handle delayed enhancement selection
        if (self.enhancement_delay_time > 0 and not self.pending_enhancement_selection):
            import pygame
            current_time = pygame.time.get_ticks() / 1000
            if current_time - self.enhancement_delay_time >= self.enhancement_delay_duration:
                # Check if movement skills are still active
                movement_skills_active = any(
                    getattr(skill, 'active', False) for skill in self.skills.values()
                    if getattr(skill, 'is_movement_skill', False)
                )
                
                if not movement_skills_active:
                    # Safe to show enhancement selection now
                    self.pending_enhancement_selection = True
                    self.enhancement_delay_time = 0  # Clear the delay
                else:
                    # Extend delay until movement skills finish
                    self.enhancement_delay_time = current_time
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

        # Enhancement system
        self.enhancement_manager = SkillEnhancementManager(self)
        self.pending_enhancement_selection = False
        self.last_enhancement_time = 0  # Track when enhancements were applied
        self.enhancement_delay_time = 0  # Time when enhancement was requested
        self.enhancement_delay_duration = 0.5  # Wait 0.5 seconds before showing enhancement

        self.health = PLAYER_START_HEALTH
        self.max_health = PLAYER_START_HEALTH  # Add max_health attribute
        self.barrier = PLAYER_START_BARRIER
        self.max_barrier = PLAYER_START_BARRIER  # Add max_barrier attribute
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
        
        # Immunity system
        self.is_immune = False
        self.immunity_timer = 0.0


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
        # Check immunity first
        # Debug: log incoming damage attempts for troubleshooting
        try:
            src_name = source.name if (source and hasattr(source, 'name')) else str(source)
        except Exception:
            src_name = str(source)
        print(f"[PLAYER DAMAGE DEBUG] Incoming {amount} from {src_name}; is_immune={self.is_immune}, immunity_timer={getattr(self, 'immunity_timer', 0):.2f}, barrier={getattr(self, 'barrier', 0)}")

        if self.is_immune:
            print(f"[PLAYER DAMAGE DEBUG] Damage blocked by immunity: {amount} from {src_name}")
            return  # Immune to all damage
            
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
            self.received_log.add_entry(-absorbed, skill_name, 'damage', 
                                        health=self.health, barrier=self.barrier,
                                        max_health=self.max_health, max_barrier=self.max_barrier)
        if damage_to_health > 0:
            if not self.anim_lock:
                self.anim_state = self.ANIM_HURT_HP
                self.anim_timer = 0.0
                self.anim_lock = True
                # Play hit sound for health damage
                SoundManager.play_hit_sound('player')
            self.health -= damage_to_health
            # Log health reduction
            self.received_log.add_entry(-damage_to_health, skill_name, 'damage', 
                                        health=self.health, barrier=self.barrier,
                                        max_health=self.max_health, max_barrier=self.max_barrier)
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
        self.received_log.add_entry(amount, skill_name, 'heal', 
                                    health=self.health, barrier=self.barrier,
                                    max_health=self.max_health, max_barrier=self.max_barrier)
    
    def grant_immunity(self, duration):
        """Grant damage immunity for the specified duration in seconds."""
        self.is_immune = True
        self.immunity_timer = max(self.immunity_timer, duration)  # Don't reduce existing immunity time

    def get_exp_to_next_level(self):
        """Calculate XP required for next level using progressive additive bonus system."""
        if self.level >= self.max_level:
            return 0  # Max level reached
        
        # Progressive XP requirement: 25% base + 1% increase per level
        # Each previous level contributes its own escalating bonus
        total_bonus = 0.0
        for prev_level in range(1, self.level):  # For each previous level
            level_bonus_rate = PLAYER_EXP_REQUIREMENT_BONUS + (prev_level - 1) * 0.01
            total_bonus += level_bonus_rate
        
        total_requirement = PLAYER_BASE_EXP_REQUIREMENT * (1.0 + total_bonus)
        return int(total_requirement)
    
    def add_experience(self, amount):
        """Add experience and handle level ups."""
        if self.level >= self.max_level:
            return False  # No more leveling possible
        
        # Apply XP enhancement bonus
        xp_bonus = self.enhancement_manager.get_enhancement_value('increased_xp')
        enhanced_amount = amount * (1.0 + xp_bonus)
        
        self.exp += enhanced_amount
        leveled_up = False
        
        # Check for level ups (can level multiple times with large XP gains)
        while self.level < self.max_level and self.exp >= self.get_exp_to_next_level():
            self.exp -= self.get_exp_to_next_level()
            self.level += 1
            leveled_up = True
            
            # Gain skill point on level up
            self.skill_points += 1
            
            print(f"[PLAYER] Level up! Now level {self.level}")
            
            # Play level up sound
            try:
                SoundManager.play_player_level_up_sound()
            except Exception as e:
                print(f"[WARNING] Failed to play level up sound: {e}")
            
            # Optional: Add level up bonuses (health, damage, etc.)
            self._apply_level_up_bonuses()
            
            # Schedule enhancement selection with delay
            import pygame
            self.enhancement_delay_time = pygame.time.get_ticks() / 1000
        
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
    
    def has_pending_enhancement_selection(self):
        """Check if player has pending enhancement selection."""
        return self.pending_enhancement_selection
    
    def get_enhancement_choices(self):
        """Get available enhancement choices for level up."""
        return self.enhancement_manager.generate_enhancement_choices()
    
    def apply_enhancement_choice(self, enhancement_id):
        """Apply selected enhancement and clear pending selection."""
        success = self.enhancement_manager.apply_enhancement(enhancement_id)
        if success:
            self.pending_enhancement_selection = False
            self.last_enhancement_time = pygame.time.get_ticks() / 1000  # Record enhancement time
            print(f"[PLAYER] Applied enhancement: {enhancement_id}")
        return success
    
    def get_enhancement_value(self, enhancement_type, skill_name=None):
        """Get current value of an enhancement."""
        return self.enhancement_manager.get_enhancement_value(enhancement_type, skill_name)
    
    def get_enhancement_level(self, enhancement_type, skill_name=None):
        """Get current level of an enhancement."""
        return self.enhancement_manager.get_enhancement_level(enhancement_type, skill_name)
    
    def get_pickup_range(self):
        """Get current pickup range including enhancements."""
        base_range = PLAYER_PICKUP_RANGE
        pickup_enhancement = self.enhancement_manager.get_enhancement_value('pickup_range')
        enhanced_range = base_range * (1.0 + pickup_enhancement)
        return enhanced_range
