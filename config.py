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
        ('resources/images/Tiles/bg/tile_grass1.jpg', 35),  # (path, weight%)
        ('resources/images/Tiles/bg/tile_grass2.jpg', 30),
        ('resources/images/Tiles/bg/tile_grass3.jpg', 35)
    ],
    'grass_plant_yellow': [
        ('resources/images/Tiles/bg/tile_plant_y_1.jpg', 40),
        ('resources/images/Tiles/bg/tile_plant_y_2.jpg', 40),
        ('resources/images/Tiles/bg/tile_plant_y_3.jpg', 20),
    ],
    'grass_plant_red': [
        ('resources/images/Tiles/bg/tile_plant_r_1.jpg', 40),
        ('resources/images/Tiles/bg/tile_plant_r_2.jpg', 40),
        ('resources/images/Tiles/bg/tile_plant_r_3.jpg', 20),
    ],
    'stone': [
        ('resources/images/Tiles/bg/tile_stone1.jpg', 40),
        ('resources/images/Tiles/bg/tile_stone2.jpg', 40),
        ('resources/images/Tiles/bg/tile_stone3.jpg', 20)
    ]
}

# Fallback colors if images don't exist
BIOME_FALLBACK_COLORS = {
    'grass': (60, 140, 40),
    'grass_plant_yellow': (101, 67, 33),
    'grass_plant_red': (140, 40, 40),
    'stone': (120, 120, 120)
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

# Enemy Spawner Configuration
SPAWNER_DEFAULT_INTERVAL = 1.0  # seconds between spawns
SPAWNER_SPAWN_BUFFER = 100  # Distance outside camera view to spawn enemies
SPAWNER_ENEMY_WEIGHTS = {
	'Plant': 1.0,
}
SPAWNER_TIME_WEIGHT_EVENTS = [
	('Plant', 60, 2.0),  # After 60s, double plant spawn chance
]

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
PLAYER_START_HEALTH = 50
PLAYER_START_BARRIER = 0
PLAYER_BARRIER_DECAY_PERCENT_PER_SEC = 10
PLAYER_BARRIER_REGEN = 0
PLAYER_START_EXP = 0
PLAYER_EXP_TO_NEXT_LEVEL_MULT = 1.02
PLAYER_START_LEVEL = 1
PLAYER_SIZE = 48
PLAYER_MOVEMENT_SPEED = 3
PLAYER_DAMAGE_REDUCTION = 0.0
PLAYER_COOLDOWN = 1.0
PLAYER_ATTACK_SPEED = 1.0
PLAYER_CRIT_CHANCE = 0.05
PLAYER_CRIT_DAMAGE = 1.5
PLAYER_START_SKILL_POINTS = 0

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
GAME_DEFAULT_FPS = 60

# =============================================================================
# LOGGING AND DEBUGGING CONFIGURATION
# =============================================================================
DAMAGE_LOG_MAX_ENTRIES = 10
RECEIVED_LOG_MAX_ENTRIES = 50

# =============================================================================
# AUDIO CONFIGURATION
# =============================================================================
MUSIC_VOLUME = 0.05  # 5%
SFX_VOLUME = 0.1    # 10%
BG_MUSIC_PATH = "resources/sounds/bg_music01.mp3"

# =============================================================================
# LOGGING AND DEBUGGING CONFIGURATION  
# =============================================================================
PLAYER_DAMAGE_LOG_MAX_ENTRIES = 50
PLAYER_RECEIVED_LOG_MAX_ENTRIES = 50

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
