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
    },
    'movement_speed': {
        'name': 'Movement Speed',
        'description': 'Increases movement speed',
        'base_value': 0.10,  # 10% increase per level
        'max_level': 5,
        'value_per_level': 0.10,  # Additional 10% per level
    },
    'life_regeneration': {
        'name': 'Life Regeneration',
        'description': 'Regenerates health over time',
        'base_value': 1.0,   # +1 HP per second per level
        'max_level': 10,
        'value_per_level': 1.0,  # Additional +1 HP per second per level
    },
    'barrier_regeneration': {
        'name': 'Barrier Regeneration',
        'description': 'Regenerates barrier over time',
        'base_value': 2.0,   # +2 barrier per second per level
        'max_level': 10,
        'value_per_level': 2.0,  # Additional +2 barrier per second per level
    },
    'increased_xp': {
        'name': 'Increased XP',
        'description': 'Increases experience gain',
        'base_value': 0.02,  # 2% increase per level
        'max_level': 10,
        'value_per_level': 0.02,  # Additional 2% per level
    },
    'pickup_range': {
        'name': 'Pickup Range',
        'description': 'Increases item pickup range',
        'base_value': 0.10,  # 10% increase per level
        'max_level': 50,     # No max limit as requested
        'value_per_level': 0.20,  # Additional 10% per level
    },
    'increased_damage': {
        'name': 'Increased Damage',
        'description': 'Increases all skill damage',
        'base_value': 0.10,  # 10% increase per level
        'max_level': 10,
        'value_per_level': 0.10,  # Additional 10% per level
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
        },
        'double_slash': {
            'name': 'Double Slash',
            'description': 'Creates a second slash on the opposite side',
            'base_value': 1,  # Binary - either have it or not
            'max_level': 1,   # Can only be selected once
            'value_per_level': 0,  # No scaling
        },
        'triple_strike': {
            'name': 'Triple Strike',
            'description': 'Every third slash is 3x bigger',
            'base_value': 3.0,  # 3x size multiplier
            'max_level': 1,   # Can only be selected once
            'value_per_level': 0,  # No scaling
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
        },
        'immunity_on_dash': {
            'name': 'Dash Immunity',
            'description': 'Become immune to damage for 1 second when dashing',
            'base_value': 1.0,  # Duration in seconds
            'max_level': 1,
            'value_per_level': 1.0,  # Additional 1.0 seconds per level (1.0, 2.0)
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

# UI Configuration for Enhancement Selection (sizing only, colors in main config.py)
ENHANCEMENT_UI = {
    'panel_width': 700,
    'panel_height': 450,
    'button_width': 220,
    'button_height': 130,
    'button_spacing': 20,
}
