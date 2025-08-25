"""
Skill Enhancement Configuration
Defines all available skill enhancements and their parameters.
"""

# General Enhancement Types (applicable to all skills)
GENERAL_ENHANCEMENTS = {
    'cooldown_reduction': {
        'name': 'Cooldown Reduction',
        'description': 'Reduces skill cooldown time',
        'base_value': 0.15,  # 15% reduction per level
        'max_level': 5,
        'value_per_level': 0.05,  # Additional 5% per level
    },
    'increased_aoe': {
        'name': 'Increased AOE',
        'description': 'Increases skill area of effect',
        'base_value': 0.25,  # 25% size increase per level
        'max_level': 4,
        'value_per_level': 0.15,  # Additional 15% per level
    },
    'cooldown_reset_chance': {
        'name': 'Cooldown Reset',
        'description': 'Chance to reset cooldown on use',
        'base_value': 0.05,  # 5% chance per level
        'max_level': 3,
        'value_per_level': 0.03,  # Additional 3% per level
    },
    'double_damage_chance': {
        'name': 'Critical Strike',
        'description': 'Chance to deal double damage',
        'base_value': 0.05,  # 5% chance per level
        'max_level': 4,
        'value_per_level': 0.04,  # Additional 4% per level
    }
}

# Skill-Specific Enhancements
SKILL_SPECIFIC_ENHANCEMENTS = {
    'slash': {
        'stun_chance': {
            'name': 'Stunning Strike',
            'description': 'Chance to stun enemies for 1 second',
            'base_value': 0.10,  # 10% chance per level
            'max_level': 3,
            'value_per_level': 0.05,  # Additional 5% per level
            'stun_duration': 1.0,  # seconds
        },
        'knockback': {
            'name': 'Knockback Force',
            'description': 'Pushes enemies away on hit',
            'base_value': 50.0,  # pixels per level
            'max_level': 4,
            'value_per_level': 25.0,  # Additional 25 pixels per level
        }
    },
    'dash': {
        'increased_range': {
            'name': 'Extended Dash',
            'description': 'Increases dash distance',
            'base_value': 0.50,  # 50% increase per level
            'max_level': 3,
            'value_per_level': 0.25,  # Additional 25% per level
        },
        'double_dash': {
            'name': 'Double Dash',
            'description': 'Allows two consecutive dashes',
            'base_value': 1,  # Number of additional dashes
            'max_level': 2,
            'value_per_level': 1,  # One more dash per level
            'charge_regen_time': 2.0,  # seconds to regen one charge
        }
    }
}

# Enhancement Selection Configuration
ENHANCEMENT_SELECTION = {
    'choices_per_level': 3,  # Number of enhancement options to show
    'general_chance': 0.6,   # 60% chance for general enhancements
    'specific_chance': 0.4,  # 40% chance for skill-specific enhancements
    'avoid_duplicates': True,  # Don't show same enhancement twice in one selection
    'respect_max_levels': True,  # Don't show maxed enhancements
}

# UI Configuration for Enhancement Selection
ENHANCEMENT_UI = {
    'background_color': (20, 20, 30, 180),  # Semi-transparent dark
    'panel_color': (40, 40, 50),
    'border_color': (100, 100, 120),
    'text_color': (255, 255, 255),
    'highlight_color': (100, 150, 255),
    'button_color': (60, 60, 80),
    'button_hover_color': (80, 80, 100),
    'panel_width': 600,
    'panel_height': 400,
    'button_width': 180,
    'button_height': 100,
    'button_spacing': 20,
}
