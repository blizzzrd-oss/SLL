"""
Skill Enhancement System
Manages player skill enhancements and upgrades.
"""

import random
from config_enhancements import (
    GENERAL_ENHANCEMENTS, SKILL_SPECIFIC_ENHANCEMENTS, 
    ENHANCEMENT_SELECTION
)


class Enhancement:
    """Represents a single enhancement for a skill."""
    
    def __init__(self, enhancement_type, skill_name=None, enhancement_key=None):
        self.enhancement_type = enhancement_type  # 'general' or 'specific'
        self.skill_name = skill_name  # None for general, skill name for specific
        self.enhancement_key = enhancement_key
        self.level = 0
        self.max_level = self._get_config()['max_level']
    
    def _get_config(self):
        """Get configuration for this enhancement."""
        if self.enhancement_type == 'general':
            return GENERAL_ENHANCEMENTS[self.enhancement_key]
        else:
            return SKILL_SPECIFIC_ENHANCEMENTS[self.skill_name][self.enhancement_key]
    
    def get_current_value(self):
        """Calculate current enhancement value based on level."""
        config = self._get_config()
        if self.level == 0:
            return 0
        
        base_value = config['base_value']
        value_per_level = config['value_per_level']
        return base_value + (self.level - 1) * value_per_level
    
    def can_upgrade(self):
        """Check if this enhancement can be upgraded further."""
        return self.level < self.max_level
    
    def upgrade(self):
        """Upgrade this enhancement by one level."""
        if self.can_upgrade():
            self.level += 1
            return True
        return False
    
    def get_display_info(self):
        """Get information for UI display."""
        config = self._get_config()
        name = config['name']
        description = config['description']
        current_value = self.get_current_value()
        
        if self.skill_name:
            name = f"{self.skill_name.title()} - {name}"
        
        level_text = f"Level {self.level}/{self.max_level}"
        
        return {
            'name': name,
            'description': description,
            'level_text': level_text,
            'current_value': current_value,
            'can_upgrade': self.can_upgrade()
        }


class SkillEnhancementManager:
    """Manages all skill enhancements for a player."""
    
    def __init__(self, player):
        self.player = player
        self.enhancements = {}  # key: enhancement_id, value: Enhancement
        self._initialize_enhancements()
    
    def _initialize_enhancements(self):
        """Initialize all possible enhancements."""
        # General enhancements (apply to all skills)
        for enhancement_key in GENERAL_ENHANCEMENTS:
            enhancement_id = f"general_{enhancement_key}"
            self.enhancements[enhancement_id] = Enhancement(
                'general', None, enhancement_key
            )
        
        # Skill-specific enhancements
        for skill_name in self.player.active_skills:
            if skill_name in SKILL_SPECIFIC_ENHANCEMENTS:
                for enhancement_key in SKILL_SPECIFIC_ENHANCEMENTS[skill_name]:
                    enhancement_id = f"{skill_name}_{enhancement_key}"
                    self.enhancements[enhancement_id] = Enhancement(
                        'specific', skill_name, enhancement_key
                    )
    
    def get_available_enhancements(self):
        """Get list of enhancements that can still be upgraded."""
        available = []
        for enhancement_id, enhancement in self.enhancements.items():
            if enhancement.can_upgrade():
                available.append((enhancement_id, enhancement))
        return available
    
    def generate_enhancement_choices(self):
        """Generate enhancement choices for level up."""
        available = self.get_available_enhancements()
        if not available:
            return []
        
        choices_count = min(ENHANCEMENT_SELECTION['choices_per_level'], len(available))
        choices = []
        
        # Separate general and specific enhancements
        general_enhancements = [(eid, enh) for eid, enh in available if enh.enhancement_type == 'general']
        specific_enhancements = [(eid, enh) for eid, enh in available if enh.enhancement_type == 'specific']
        
        # Generate choices based on configured probabilities
        for _ in range(choices_count):
            if not available:
                break
                
            # Choose type based on probability
            if (general_enhancements and specific_enhancements and 
                random.random() < ENHANCEMENT_SELECTION['general_chance']):
                pool = general_enhancements
            elif specific_enhancements:
                pool = specific_enhancements
            elif general_enhancements:
                pool = general_enhancements
            else:
                break
            
            # Select random enhancement from pool
            choice = random.choice(pool)
            choices.append(choice)
            
            # Remove from available if avoiding duplicates
            if ENHANCEMENT_SELECTION['avoid_duplicates']:
                available.remove(choice)
                if choice in general_enhancements:
                    general_enhancements.remove(choice)
                if choice in specific_enhancements:
                    specific_enhancements.remove(choice)
        
        return choices
    
    def apply_enhancement(self, enhancement_id):
        """Apply an enhancement upgrade."""
        if enhancement_id in self.enhancements:
            enhancement = self.enhancements[enhancement_id]
            if enhancement.upgrade():
                self._update_skill_stats(enhancement)
                return True
        return False
    
    def _update_skill_stats(self, enhancement):
        """Update skill statistics based on enhancement."""
        # This will be called when skills are used to apply enhancement effects
        # The actual application happens in the skill classes
        pass
    
    def get_enhancement_value(self, enhancement_type, skill_name=None):
        """Get the current value of a specific enhancement."""
        if enhancement_type in GENERAL_ENHANCEMENTS:
            enhancement_id = f"general_{enhancement_type}"
        else:
            enhancement_id = f"{skill_name}_{enhancement_type}"
        
        if enhancement_id in self.enhancements:
            return self.enhancements[enhancement_id].get_current_value()
        return 0
    
    def get_enhancement_level(self, enhancement_type, skill_name=None):
        """Get the current level of a specific enhancement."""
        if enhancement_type in GENERAL_ENHANCEMENTS:
            enhancement_id = f"general_{enhancement_type}"
        else:
            enhancement_id = f"{skill_name}_{enhancement_type}"
        
        if enhancement_id in self.enhancements:
            return self.enhancements[enhancement_id].level
        return 0
