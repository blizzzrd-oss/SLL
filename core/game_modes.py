"""
Game Mode Configuration
Defines different gameplay modifiers and events for each game mode.
"""

# Game Mode Configurations
GAME_MODES = {
    'Easy': {
        'display_name': 'Easy Mode',
        'description': 'Relaxed gameplay for beginners',
        
        # Difficulty Multipliers
        'enemy_health_multiplier': 0.7,      # Enemies have 70% health
        'enemy_damage_multiplier': 0.8,      # Enemies deal 80% damage
        'enemy_speed_multiplier': 0.9,       # Enemies move at 90% speed
        'enemy_spawn_rate_multiplier': 0.8,  # 80% spawn rate
        
        # Player Bonuses
        'player_health_multiplier': 1.2,     # Player has 120% health
        'player_damage_multiplier': 1.1,     # Player deals 110% damage
        'player_speed_multiplier': 1.0,      # Normal player speed
        'experience_multiplier': 1.0,        # Normal XP gain
        
        # Resource Multipliers
        'loot_drop_rate_multiplier': 1.3,    # 130% loot drop rate
        'gold_multiplier': 1.2,              # 120% gold drops
        
        # Special Events (probability per minute)
        'healing_shrine_chance': 0.15,       # 15% chance per minute
        'bonus_loot_event_chance': 0.10,     # 10% chance per minute
        'enemy_weakness_event_chance': 0.08, # 8% chance per minute
        
        # UI Color Theme
        'theme_color': (100, 255, 100),      # Green theme
    },
    
    'Normal': {
        'display_name': 'Normal Mode',
        'description': 'Balanced gameplay experience',
        
        # Difficulty Multipliers (baseline)
        'enemy_health_multiplier': 1.0,
        'enemy_damage_multiplier': 1.0,
        'enemy_speed_multiplier': 1.0,
        'enemy_spawn_rate_multiplier': 1.0,
        
        # Player Stats (baseline)
        'player_health_multiplier': 1.0,
        'player_damage_multiplier': 1.0,
        'player_speed_multiplier': 1.0,
        'experience_multiplier': 1.0,
        
        # Resource Multipliers (baseline)
        'loot_drop_rate_multiplier': 1.0,
        'gold_multiplier': 1.0,
        
        # Special Events
        'healing_shrine_chance': 0.08,
        'bonus_loot_event_chance': 0.06,
        'enemy_weakness_event_chance': 0.04,
        
        # UI Color Theme
        'theme_color': (100, 150, 255),      # Blue theme
    },
    
    'Hard': {
        'display_name': 'Hard Mode',
        'description': 'Challenging gameplay for veterans',
        
        # Difficulty Multipliers
        'enemy_health_multiplier': 1.4,      # Enemies have 140% health
        'enemy_damage_multiplier': 1.3,      # Enemies deal 130% damage
        'enemy_speed_multiplier': 1.2,       # Enemies move at 120% speed
        'enemy_spawn_rate_multiplier': 1.5,  # 150% spawn rate
        
        # Player Stats
        'player_health_multiplier': 0.8,     # Player has 80% health
        'player_damage_multiplier': 0.9,     # Player deals 90% damage
        'player_speed_multiplier': 1.0,      # Normal player speed
        'experience_multiplier': 1.5,        # 150% XP gain (reward for difficulty)
        
        # Resource Multipliers
        'loot_drop_rate_multiplier': 0.8,    # 80% loot drop rate
        'gold_multiplier': 1.3,              # 130% gold drops (quality over quantity)
        
        # Special Events
        'healing_shrine_chance': 0.05,       # 5% chance per minute
        'bonus_loot_event_chance': 0.12,     # 12% chance per minute (rare but valuable)
        'enemy_weakness_event_chance': 0.02, # 2% chance per minute
        'boss_swarm_event_chance': 0.08,     # 8% chance for elite enemy spawns
        
        # UI Color Theme
        'theme_color': (255, 100, 100),      # Red theme
    }
}

# Event Definitions
GAME_EVENTS = {
    'healing_shrine': {
        'name': 'Healing Shrine',
        'description': 'A magical shrine appears, restoring health over time',
        'duration': 30.0,  # seconds
        'effect_type': 'heal_over_time',
        'effect_value': 2,  # HP per second
    },
    
    'bonus_loot_event': {
        'name': 'Loot Blessing',
        'description': 'Enemies drop extra loot for a short time',
        'duration': 45.0,
        'effect_type': 'loot_multiplier',
        'effect_value': 2.0,  # Double loot drops
    },
    
    'enemy_weakness_event': {
        'name': 'Enemy Weakness',
        'description': 'Enemies are weakened and take extra damage',
        'duration': 60.0,
        'effect_type': 'damage_multiplier',
        'effect_value': 1.5,  # 150% damage to enemies
    },
    
    'boss_swarm_event': {
        'name': 'Elite Invasion',
        'description': 'Powerful elite enemies spawn more frequently',
        'duration': 90.0,
        'effect_type': 'elite_spawn_rate',
        'effect_value': 3.0,  # 300% elite spawn rate
    }
}

def get_game_mode_config(mode):
    """Get configuration for a specific game mode"""
    return GAME_MODES.get(mode, GAME_MODES['Normal'])

def get_all_game_modes():
    """Get list of all available game modes"""
    return list(GAME_MODES.keys())
