"""
Enemy Configuration
All enemy-related settings including types, spawning, and AI behavior.
"""

# =============================================================================
# ENEMY TYPE CONFIGURATION
# =============================================================================
ENEMY_TYPE_CONFIG = {
	'Plant': {
		'max_health': 20,
		'size': 48,
		'speed': 50,
		'color': (80, 200, 80),
		'attack_range': 32,
		'attack_damage': 5,
		'attack_cooldown': 1.0,
	},
	'Demon': {
		'max_health': 35,
		'size': (81, 70),  # Width x Height
		'speed': 35,  # Slower than plants
		'color': (150, 50, 50),
		'attack_range': 200,  # Long range for projectiles
		'attack_damage': 10,
		'attack_cooldown': 2.0,
		'projectile_speed': 150,
		'projectile_damage': 8,
	},
	'Hero': {
		'max_health': 40,
		'size': (32, 32),  # Width x Height - reduced hitbox for small sprite
		'speed': 45,  # Moderate speed - between plants and demons
		'color': (200, 100, 100),
		'attack_range': 20,  # Melee range
		'attack_damage': 18,
		'attack_cooldown': 1.5,
		'block_chance': 0.3,  # 30% chance to block attacks
	},
}

# =============================================================================
# ENEMY SPAWNER CONFIGURATION
# =============================================================================
SPAWNER_DEFAULT_INTERVAL = 0.5  # seconds between spawns
SPAWNER_SPAWN_BUFFER = 100  # Distance outside camera view to spawn enemies
SPAWNER_ENEMY_WEIGHTS = {
	'Plant': 1.0,
	'Demon': 0.3,  # Lower spawn weight - demons are more dangerous
	'Hero': 0.5,   # Moderate spawn weight - Heroes are tankier than plants
}

# Minimum wave requirements for enemy types
SPAWNER_ENEMY_MIN_WAVES = {
	'Plant': 1,   # Plants can spawn from wave 1
	'Demon': 2,   # Demons only start spawning from wave 2
	'Hero': 1,    # Heroes can spawn from wave 1
}

# Wave-based Enemy Scaling (replaces time-based scaling)
SPAWNER_WAVE_WEIGHT_EVENTS = [
	('Plant', 3, 1.5),   # Starting from wave 3, increase plant spawn chance by 50%
	('Plant', 5, 2.0),   # Starting from wave 5, double plant spawn chance
	('Plant', 10, 3.0),  # Starting from wave 10, triple plant spawn chance
	('Demon', 2, 0.5),   # Starting from wave 2, demons begin spawning
	('Demon', 5, 1.0),   # Starting from wave 5, normal demon spawn rate
	('Demon', 10, 1.5),  # Starting from wave 10, increase demon spawn rate
	('Hero', 1, 0.8),    # Heroes start spawning from wave 1
	('Hero', 3, 1.2),    # Starting from wave 3, increase hero spawn rate
	('Hero', 7, 1.8),    # Starting from wave 7, increase hero spawn rate more
]

# Spawn Rate Limits
SPAWNER_MIN_INTERVAL = 0.1           # Minimum spawn interval (maximum spawn rate)
SPAWNER_MAX_SPAWN_MULTIPLIER = 10.0  # Maximum spawn rate multiplier (caps at 10x)

# Legacy time-based scaling (fallback when no wave manager is available)
SPAWNER_RATE_INCREASE_ENABLED = True  # Enable spawn rate increases over time (fallback)
SPAWNER_RATE_INCREASE_INTERVAL = 30.0  # Every 30 seconds, increase spawn rate (fallback) 
SPAWNER_RATE_INCREASE_FACTOR = 0.9    # Multiply interval by 0.9 (10% faster spawning) (fallback)

# =============================================================================
# ENEMY AI AND BEHAVIOR CONFIGURATION
# =============================================================================
# Plant Enemy Configuration
PLANT_ATTACK_TRIGGER_RANGE = 40
PLANT_ATTACK_DAMAGE_RANGE = 25
PLANT_ATTACK_IMPACT_FRAME_RATIO = 0.5  # Impact happens at half animation
PLANT_HURT_OVERLAY_DURATION = 0.5  # 500ms red tint
PLANT_SPRITE_STANDARD_WIDTH = 64
PLANT_SPRITE_STANDARD_HEIGHT = 64

# Enemy Sound Effects
ENEMY_PLANT_DEATH_SOUND_PATHS = [
    "resources/sounds/death_enemy_plant01.wav",
    "resources/sounds/death_enemy_plant02.wav", 
    "resources/sounds/death_enemy_plant03.wav"
]
