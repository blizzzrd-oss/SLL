import pygame
import os

# =============================================================================
# CAMERA AND WORLD CONFIGURATION
# =============================================================================
WORLD_SIZE = 10000  # Large world size
CAMERA_BUFFER_TILES = 2  # Extra tiles to render outside camera view
TILE_SIZE = 16  # Standard tile size
BACKGROUND_TILE_BUFFER = 5  # Extra tiles for background rendering

# Camera System
CAMERA_FOLLOW_SPEED = 1.0  # 1.0 = instant, lower = smoother
CAMERA_DEADZONE = 50  # Pixel deadzone around center before camera moves

# Background Biome Configuration
BIOME_TILES = {
    'grass': [
        ('resources/images/Tiles/bg/tile_grass1.jpg', 10),  # (path, weight%)
        ('resources/images/Tiles/bg/tile_grass2.jpg', 60),
        ('resources/images/Tiles/bg/tile_grass3.jpg', 10),
        ('resources/images/Tiles/bg/tile_grass4.jpg', 18),
        ('resources/images/Tiles/bg/grass_stone_5.jpg', 0.2),
        ('resources/images/Tiles/bg/tile_grass_wood1.jpg', 0.2),
        ('resources/images/Tiles/bg/tile_grass_wood2.jpg', 0.2),
        ('resources/images/Tiles/bg/tile_grass_wood3.jpg', 0.2),
    ],
    'grass_plant_yellow': [
        ('resources/images/Tiles/bg/tile_grass2.jpg', 70),
        ('resources/images/Tiles/bg/tile_grass4.jpg', 5),
        ('resources/images/Tiles/bg/tile_plant_y_1.jpg', 10),
        ('resources/images/Tiles/bg/tile_plant_y_2.jpg', 10),
        ('resources/images/Tiles/bg/tile_plant_y_3.jpg', 5),
        ('resources/images/Tiles/bg/grass_stone_1.jpg', 0.2),
		('resources/images/Tiles/bg/grass_stone_2.jpg', 0.2),
    ],
    'grass_plant_red': [
        ('resources/images/Tiles/bg/tile_grass2.jpg', 70),
        ('resources/images/Tiles/bg/tile_grass4.jpg', 5),
        ('resources/images/Tiles/bg/tile_plant_r_1.jpg', 10),
        ('resources/images/Tiles/bg/tile_plant_r_2.jpg', 10),
        ('resources/images/Tiles/bg/tile_plant_r_3.jpg', 5),
        ('resources/images/Tiles/bg/grass_stone_4.jpg', 0.2),
        ('resources/images/Tiles/bg/grass_stone_3.jpg', 0.2),
    ]
}

# Fallback colors if images don't exist
BIOME_FALLBACK_COLORS = {
    'grass': (60, 140, 40),
    'grass_plant_yellow': (101, 67, 33),
    'grass_plant_red': (140, 40, 40)
}

# =============================================================================
# ENEMY CONFIGURATION
# =============================================================================
ENEMY_TYPE_CONFIG = {
	'Plant': {
		'max_health': 25,
		'size': 48,
		'speed': 75,
		'color': (80, 200, 80),
		'attack_range': 32,
		'attack_damage': 5,
		'attack_cooldown': 1.0,
	},
}

# =============================================================================
# WAVE SYSTEM CONFIGURATION
# =============================================================================

# Comprehensive Wave System Configuration (Primary) - ADDITIVE BONUSES
WAVE_SYSTEM_CONFIGURATION = {
    # Core wave timing
    'WAVE_DURATION': 30.0,  # Duration of each wave in seconds
    
    # Spawn rate bonuses per wave (additive percentages)
    'WAVE_SPAWN_RATE_BONUSES': {
        1: 0.0,   # Wave 1: +0% spawn rate (normal)
        2: 0.2,   # Wave 2: +20% spawn rate
        3: 0.4,   # Wave 3: +40% spawn rate  
        4: 0.7,   # Wave 4: +70% spawn rate
        5: 1.0,   # Wave 5+: +100% spawn rate (continues)
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

# Core Wave Settings (Legacy - kept for backward compatibility)
WAVE_DURATION = 30.0  # Duration of each wave in seconds (central config)
WAVE_SCALING_ENABLED = True  # Enable wave-based progression

# Wave Progression Multipliers (applied per wave)
WAVE_SPAWN_RATE_MULTIPLIER = 1.15     # 15% faster spawning each wave
WAVE_ENEMY_HEALTH_MULTIPLIER = 1.08   # 8% more enemy health each wave
WAVE_ENEMY_DAMAGE_MULTIPLIER = 1.05   # 5% more enemy damage each wave
WAVE_ENEMY_SPEED_MULTIPLIER = 1.03    # 3% faster enemy movement each wave
WAVE_ENEMY_COOLDOWN_MULTIPLIER = 0.98 # 2% faster enemy attack cooldowns each wave
WAVE_EXP_GAIN_MULTIPLIER = 1.04       # 4% more experience each wave
WAVE_MAGIC_FIND_MULTIPLIER = 1.02     # 2% better loot quality each wave

# Special Wave Types
BOSS_WAVE_INTERVAL = 10      # Every 10th wave is a boss wave
ELITE_WAVE_INTERVAL = 5      # Every 5th wave is an elite wave
BOSS_WAVE_HEALTH_BONUS = 2.0 # Boss waves: 2x enemy health
BOSS_WAVE_DAMAGE_BONUS = 1.5 # Boss waves: 1.5x enemy damage
ELITE_WAVE_HEALTH_BONUS = 1.5 # Elite waves: 1.5x enemy health
ELITE_WAVE_SPEED_BONUS = 1.3  # Elite waves: 1.3x enemy speed

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
    'loot_blessing': {
        'unlock_wave': 3,
        'base_chance': 0.25,
        'mode_multipliers': {
            'Easy': 1.2,
            'Normal': 1.0,
            'Hard': 1.3,     # More loot events in hard mode as reward
        }
    },
    'enemy_weakness': {
        'unlock_wave': 5,
        'base_chance': 0.2,
        'mode_multipliers': {
            'Easy': 1.4,
            'Normal': 1.0,
            'Hard': 0.8,
        }
    },
    'boss_swarm': {
        'unlock_wave': 4,
        'base_chance': 0.15,
        'mode_multipliers': {
            'Easy': 0.5,
            'Normal': 1.0,
            'Hard': 1.5,     # More challenging events in hard mode
        }
    }
}

# Enemy Spawner Configuration
SPAWNER_DEFAULT_INTERVAL = 0.5  # seconds between spawns
SPAWNER_SPAWN_BUFFER = 100  # Distance outside camera view to spawn enemies
SPAWNER_ENEMY_WEIGHTS = {
	'Plant': 1.0,
}

# Wave-based Enemy Scaling (replaces time-based scaling)
SPAWNER_WAVE_WEIGHT_EVENTS = [
	('Plant', 3, 1.5),   # Starting from wave 3, increase plant spawn chance by 50%
	('Plant', 5, 2.0),   # Starting from wave 5, double plant spawn chance
	('Plant', 10, 3.0),  # Starting from wave 10, triple plant spawn chance
]

# Spawn Rate Limits
SPAWNER_MIN_INTERVAL = 0.1           # Minimum spawn interval (maximum spawn rate)
SPAWNER_MAX_SPAWN_MULTIPLIER = 10.0  # Maximum spawn rate multiplier (caps at 10x)

# Legacy time-based scaling (kept for fallback when no wave manager is available)
SPAWNER_TIME_WEIGHT_EVENTS = [
	('Plant', 60, 2.0),  # After 60s, double plant spawn chance (fallback only)
]
SPAWNER_RATE_INCREASE_ENABLED = True  # Enable spawn rate increases over time (fallback)
SPAWNER_RATE_INCREASE_INTERVAL = 30.0  # Every 30 seconds, increase spawn rate (fallback) 
SPAWNER_RATE_INCREASE_FACTOR = 0.9    # Multiply interval by 0.9 (10% faster spawning) (fallback)

# =============================================================================
# ENEMY LOGIC CONFIGURATION
# =============================================================================
# Plant Enemy Configuration
PLANT_ATTACK_TRIGGER_RANGE = 40
PLANT_ATTACK_DAMAGE_RANGE = 25
PLANT_ATTACK_IMPACT_FRAME_RATIO = 0.5  # Impact happens at half animation
PLANT_HURT_OVERLAY_DURATION = 0.5  # 500ms red tint
PLANT_SPRITE_STANDARD_WIDTH = 64
PLANT_SPRITE_STANDARD_HEIGHT = 64

# =============================================================================
# SKILL CONFIGURATION
# =============================================================================
SKILL_COOLDOWN = 0.5  # Default cooldown for skills (seconds)

# Slash Skill Configuration
SLASH_DEFAULT_COOLDOWN = 1.0
SLASH_DEFAULT_DAMAGE = 10
SLASH_DEFAULT_ARC_DEGREES = 190
SLASH_DEFAULT_DURATION = 0.25
SLASH_FRAME_COUNT = 5
SLASH_SHEET_PATH = 'resources/images/player_melee/slash/player_melee_slash.png'

# Dash Skill Configuration
DASH_RANGE = 100
DASH_COOLDOWN = 2.0
DASH_DURATION = 0.15  # seconds
DASH_DEFAULT_DAMAGE = 10

# =============================================================================
# PLAYER CONFIGURATION
# =============================================================================
PLAYER_START_HEALTH = 100
PLAYER_START_BARRIER = 100
PLAYER_BARRIER_DECAY_PERCENT_PER_SEC = 10
PLAYER_BARRIER_REGEN = 0
PLAYER_START_EXP = 0
PLAYER_EXP_TO_NEXT_LEVEL_MULT = 1.02
PLAYER_START_LEVEL = 1
PLAYER_SIZE = 48
PLAYER_MOVEMENT_SPEED = 2
PLAYER_DAMAGE_REDUCTION = 0.0
PLAYER_COOLDOWN = 1.0
PLAYER_ATTACK_SPEED = 1.0
PLAYER_CRIT_CHANCE = 0.05
PLAYER_CRIT_DAMAGE = 1.5
PLAYER_START_SKILL_POINTS = 0

# Player Combat Settings
PLAYER_AUTO_AIM = True  # Default auto-aim setting
PLAYER_AUTO_ATTACK = True  # Default auto-attack setting

# Player Skills Configuration
PLAYER_PASSIVE_SKILLS = {
	'toughness': 0,
	'regeneration': 0,
	'barrier_boost': 0,
}
PLAYER_ACTIVE_SKILLS = {
	'slash': 0,
	'dash': 0,
	'barrier_burst': 0,
}

# Skill System Configuration
# Dash Skill
DASH_RANGE = 100
DASH_COOLDOWN = 2.0
DASH_DURATION = 0.15
DASH_DAMAGE = 10

# Slash Skill
SLASH_COOLDOWN = 1.0
SLASH_DAMAGE = 10
SLASH_ARC_DEGREES = 190
SLASH_DURATION = 0.25
SLASH_SHEET_PATH = os.path.join('resources', 'images', 'player_melee', 'slash', 'player_melee_slash.png')
SLASH_FRAME_COUNT = 5

# Player Sprite Configuration
PLAYER_IDLE_SPRITE = 'resources/images/player/Idle/Slime1_Idle_full.png'
PLAYER_WALK_SPRITE = 'resources/images/player/Walk/Slime1_Walk_full.png'
PLAYER_RUN_SPRITE = 'resources/images/player/Run/Slime1_Run_full.png'
PLAYER_HURT_HP_SPRITE = 'resources/images/player/Hurt/Slime1_Hurt_full_hp.png'
PLAYER_HURT_BARRIER_SPRITE = 'resources/images/player/Hurt/Slime1_Hurt_full_barrier.png'

# Player Animation Configuration
PLAYER_SPRITE_FRAME_WIDTH = 64
PLAYER_SPRITE_FRAME_HEIGHT = 64
PLAYER_IDLE_ANIMATION_FPS = 6
PLAYER_WALK_ANIMATION_FPS = 10
PLAYER_RUN_ANIMATION_FPS = 14
PLAYER_HURT_ANIMATION_FPS = 12

# =============================================================================
# UI AND RENDERING CONFIGURATION
# =============================================================================
# Window Configuration
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# Color Definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_GRAY = (128, 128, 128)

# UI Color Scheme
COLOR_BG = (30, 30, 30)
COLOR_TEXT = (200, 200, 200)
COLOR_HIGHLIGHT = (200, 200, 50)
COLOR_SLIDER_MUSIC = (100, 100, 255)
COLOR_SLIDER_SFX = (100, 255, 100)
COLOR_BACK = (180, 180, 180)

# Font Sizes
FONT_SIZE_LARGE = 48
FONT_SIZE_SMALL = 32

# Game UI Configuration
GAME_BG_COLOR = (20, 20, 20)
GAME_OVERLAY_COLOR = (0, 0, 0, 180)
PAUSE_OVERLAY_COLOR = (0, 0, 0, 140)
GAME_OVER_FONT_SIZE = 120
PAUSE_FONT_SIZE = 80
MENU_FONT_SIZE = 48
PAUSE_MENU_HIGHLIGHT_COLOR = (255, 255, 0)
PAUSE_MENU_TEXT_COLOR = (255, 255, 255)
PAUSE_MENU_OPTIONS = ["Resume", "Surrender", "Settings", "Quit"]

# HUD Configuration
HUD_TOGGLE_KEY = pygame.K_TAB
HUD_TOP_HEIGHT = 80
HUD_BOTTOM_HEIGHT = 100
HUD_LEFT_WIDTH = 300
HUD_RIGHT_WIDTH = 300
HUD_ALPHA = 120
HUD_COLOR = (40, 40, 40, HUD_ALPHA)
HUD_LABEL_COLOR = (200, 200, 200)
HUD_LABEL_FONT_SIZE = 32

# Health and Barrier Bar Colors
COLOR_HEALTH_BAR_BG = (135, 45, 40)
COLOR_HEALTH_BAR_FILL = (175, 60, 55)
COLOR_BARRIER_BAR_BG = (130, 110, 50)
COLOR_BARRIER_BAR_FILL = (180, 150, 35)

# =============================================================================
# PERFORMANCE AND SYSTEM CONFIGURATION
# =============================================================================
GAME_FPS_OPTIONS = [60, 120, 240]
GAME_DEFAULT_FPS = 120

# =============================================================================
# LOGGING AND DEBUGGING CONFIGURATION
# =============================================================================
DAMAGE_LOG_MAX_ENTRIES = 10
RECEIVED_LOG_MAX_ENTRIES = 50

# =============================================================================
# AUDIO CONFIGURATION
# =============================================================================
MUSIC_VOLUME = 0.02  # 2%
SFX_VOLUME = 0.1    # 10%
BG_MUSIC_PATH = "resources/sounds/bg_music01.mp3"

# Audio Performance Settings
AUDIO_CHANNELS = 64  # Number of audio channels (increased for better performance)
AUDIO_FORCE_PLAY_MAX_CHANNELS_TO_STOP = 3  # Max channels to stop when force-playing important sounds

# Skill Sound Effects
SKILL_DASH_SOUND_PATH = "resources/sounds/skill_dash.mp3"
SKILL_SLASH_SOUND_PATHS = [
    "resources/sounds/skill_slash01.wav",
    "resources/sounds/skill_slash02.wav",
    "resources/sounds/skill_slash03.mp3"
]

# Hit Sound Effects
HIT_ENEMY_SOUND_PATH = "resources/sounds/hit_enemy.mp3"
HIT_PLAYER_SOUND_PATH = "resources/sounds/hit_player.wav"

# Enemy Sound Effects
ENEMY_PLANT_DEATH_SOUND_PATHS = [
    "resources/sounds/death_enemy_plant01.wav",
    "resources/sounds/death_enemy_plant02.wav", 
    "resources/sounds/death_enemy_plant03.wav"
]

# =============================================================================
# LOGGING AND DEBUGGING CONFIGURATION  
# =============================================================================
PLAYER_DAMAGE_LOG_MAX_ENTRIES = 10
PLAYER_RECEIVED_LOG_MAX_ENTRIES = 10  # Death log shows last 10 events before death

# =============================================================================
# FILE PATHS AND RESOURCES
# =============================================================================
SAVEGAME_PATH = "savegame.sav"
SETTINGS_FILE_NAME = "settings.json"

# Grass tile directory
GRASS_TILES_PATH = "resources/images/Tiles/grass"

# Menu button images
MENU_BUTTON_IMAGE_PATH = r'C:\Repos\SLL\resources\images\UI\menu\buttons\slime_button_292x145.png'
MENU_BUTTON_WIDTH = 292
MENU_BUTTON_HEIGHT = 145

# Game mode selection image
GAMEMODE_SELECT_IMAGE_PATH = r'C:\Repos\SLL\resources\images\UI\menu\buttons\slect_game_mode.png'
