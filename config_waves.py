"""
Wave System Configuration
All wave-related settings including progression, bonuses, and events.
"""

# =============================================================================
# WAVE SYSTEM CONFIGURATION
# =============================================================================

# Comprehensive Wave System Configuration (Primary) - ADDITIVE BONUSES
WAVE_SYSTEM_CONFIGURATION = {
    # Core wave timing
    'WAVE_DURATION': 60.0,  # Duration of each wave in seconds
    
    # Spawn rate bonuses per wave (additive percentages)
    'WAVE_SPAWN_RATE_BONUSES': {
        1: 0.0,   # Wave 1: +0% spawn rate (normal)
        2: 0.1,   # Wave 2: +10% spawn rate
        3: 0.2,   # Wave 3: +20% spawn rate  
        4: 0.3,   # Wave 4: +30% spawn rate
        5: 0.4,   # Wave 5+: +40% spawn rate (continues)
    },
    
    # XP gain bonuses per wave (additive percentages)
    'WAVE_XP_GAIN_BONUSES': {
        1: 0.0,   # Wave 1: +0% XP (normal)
        2: 0.1,   # Wave 2: +10% XP
        3: 0.2,   # Wave 3: +20% XP
        4: 0.4,   # Wave 4: +40% XP
        5: 0.6,   # Wave 5+: +60% XP (continues)
    },
    
    # Enemy stat bonuses per wave (additive percentages)
    'WAVE_ENEMY_BONUSES': {
        'health': {
            1: 0.0,   # Wave 1: +0% health (normal)
            2: 0.2,   # Wave 2: +20% health
            3: 0.4,   # Wave 3: +40% health
            4: 0.7,   # Wave 4: +70% health
            5: 1.0,   # Wave 5+: +100% health (continues)
        },
        'damage': {
            1: 0.0,   # Wave 1: +0% damage (normal)
            2: 0.1,   # Wave 2: +10% damage
            3: 0.2,   # Wave 3: +20% damage
            4: 0.4,   # Wave 4: +40% damage
            5: 0.6,   # Wave 5+: +60% damage (continues)
        },
        'speed': {
            1: 0.0,   # Wave 1: +0% speed (normal)
            2: 0.05,  # Wave 2: +5% speed
            3: 0.1,   # Wave 3: +10% speed
            4: 0.15,  # Wave 4: +15% speed
            5: 0.2,   # Wave 5+: +20% speed (continues)
        },
    },
    
    # Player progression bonuses per wave (additive percentages)
    'WAVE_PLAYER_BONUSES': {
        'cooldown_reduction': {
            1: 0.0,   # Wave 1: +0% cooldown reduction (normal)
            2: 0.05,  # Wave 2: +5% cooldown reduction
            3: 0.1,   # Wave 3: +10% cooldown reduction
            4: 0.15,  # Wave 4: +15% cooldown reduction
            5: 0.2,   # Wave 5+: +20% cooldown reduction (continues)
        },
        'magic_find': {
            1: 0.0,   # Wave 1: +0% magic find (normal)
            2: 0.1,   # Wave 2: +10% magic find
            3: 0.2,   # Wave 3: +20% magic find
            4: 0.3,   # Wave 4: +30% magic find
            5: 0.5,   # Wave 5+: +50% magic find (continues)
        },
    },
}

# Core Wave Settings
WAVE_DURATION = 60.0  # Duration of each wave in seconds (central config)
WAVE_SCALING_ENABLED = True  # Enable wave-based progression

# Special Wave Types - ADDITIVE BONUSES
BOSS_WAVE_INTERVAL = 10      # Every 10th wave is a boss wave
ELITE_WAVE_INTERVAL = 5      # Every 5th wave is an elite wave
BOSS_WAVE_HEALTH_BONUS = 1.0 # Boss waves: +100% enemy health (additive bonus)
BOSS_WAVE_DAMAGE_BONUS = 0.5 # Boss waves: +50% enemy damage (additive bonus)
ELITE_WAVE_HEALTH_BONUS = 0.5 # Elite waves: +50% enemy health (additive bonus)
ELITE_WAVE_SPEED_BONUS = 0.3  # Elite waves: +30% enemy speed (additive bonus)

# Wave Event Configuration
WAVE_EVENT_CHANCES = {
    # Event chances per wave (0.0 to 1.0)
    'healing_shrine': {
        'unlock_wave': 2,    # Available starting from wave 2
        'base_chance': 0.3,  # 30% chance per wave
        'mode_multipliers': {
            'Easy': 1.5,     # 45% chance in Easy mode
            'Normal': 1.0,   # 30% chance in Normal mode
            'Hard': 0.7,     # 21% chance in Hard mode
        }
    },
    'bonus_loot_event': {
        'unlock_wave': 3,
        'base_chance': 0.25,
    'multiplier': 2.0,  # Loot blessing doubles non-XP pickable drop chances
        'mode_multipliers': {
            'Easy': 1.2,
            'Normal': 1.0,
            'Hard': 1.3,     # More loot events in hard mode as reward
        }
    },
    'enemy_weakness_event': {
        'unlock_wave': 5,
        'base_chance': 0.2,
        'mode_multipliers': {
            'Easy': 1.4,
            'Normal': 1.0,
            'Hard': 0.8,
        }
    },
    'boss_swarm_event': {
        'unlock_wave': 4,
        'base_chance': 0.15,
        'mode_multipliers': {
            'Easy': 0.5,
            'Normal': 1.0,
            'Hard': 1.5,     # More challenging events in hard mode
        }
    }
}
