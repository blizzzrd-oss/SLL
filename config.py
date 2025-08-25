import pygame
import os

# Import configuration modules
from config_enemies import *
from config_waves import *
from config_pickables import *

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
        ('resources/images/Tiles/bg/tile_grass2.jpg', 68),
        ('resources/images/Tiles/bg/tile_grass4.jpg', 5),
        ('resources/images/Tiles/bg/tile_plant_y_1.jpg', 10),
        ('resources/images/Tiles/bg/tile_plant_y_2.jpg', 10),
        ('resources/images/Tiles/bg/tile_plant_y_3.jpg', 5),
        ('resources/images/Tiles/bg/grass_stone_1.jpg', 0.1),
		('resources/images/Tiles/bg/grass_stone_2.jpg', 1),
    ],
    'grass_plant_red': [
        ('resources/images/Tiles/bg/tile_grass2.jpg', 66),
        ('resources/images/Tiles/bg/tile_grass4.jpg', 5),
        ('resources/images/Tiles/bg/tile_plant_r_1.jpg', 10),
        ('resources/images/Tiles/bg/tile_plant_r_2.jpg', 10),
        ('resources/images/Tiles/bg/tile_plant_r_3.jpg', 5),
        ('resources/images/Tiles/bg/grass_stone_4.jpg', 1),
        ('resources/images/Tiles/bg/grass_stone_3.jpg', 1),
    ]
}

# Fallback colors if images don't exist
BIOME_FALLBACK_COLORS = {
    'grass': (60, 140, 40),
    'grass_plant_yellow': (101, 67, 33),
    'grass_plant_red': (140, 40, 40)
}

# =============================================================================
# SKILL CONFIGURATION
# =============================================================================
SKILL_COOLDOWN = 0.5  # Default cooldown for skills (seconds)

# Slash Skill Configuration
SLASH_FRAME_COUNT = 5
SLASH_SHEET_PATH = 'resources/images/player_melee/slash/player_melee_slash.png'

# Dash Skill Configuration
DASH_RANGE = 100

# =============================================================================
# PLAYER CONFIGURATION
# =============================================================================
PLAYER_START_HEALTH = 100
PLAYER_START_BARRIER = 100
PLAYER_BARRIER_DECAY_PERCENT_PER_SEC = 10
PLAYER_BARRIER_REGEN = 0

# Player Experience and Leveling System (Additive Scaling)
PLAYER_START_EXP = 0
PLAYER_START_LEVEL = 1
PLAYER_BASE_EXP_REQUIREMENT = 15     # XP needed for level 2 (first level up)
PLAYER_EXP_REQUIREMENT_BONUS = 0.10   # Base XP requirement bonus per level (increases by +1% per player level)
PLAYER_MAX_LEVEL = 100               # Maximum player level

# Player Stats
PLAYER_SIZE = 32  # Smaller hitbox for more precise collision detection
PLAYER_MOVEMENT_SPEED = 2
PLAYER_PICKUP_RANGE = 32  # Base pickup range in pixels
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

########### Skill System Configuration ###########
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
ENHANCEMENT_OVERLAY_COLOR = (0, 0, 0, 140)  # Same as pause menu for consistency
GAME_OVER_FONT_SIZE = 120
PAUSE_FONT_SIZE = 80
MENU_FONT_SIZE = 48
PAUSE_MENU_HIGHLIGHT_COLOR = (255, 255, 0)
PAUSE_MENU_TEXT_COLOR = (255, 255, 255)
PAUSE_MENU_OPTIONS = ["Resume", "Surrender", "Settings", "Quit"]

# Enhancement UI Colors
ENHANCEMENT_PANEL_COLOR = (40, 40, 50)
ENHANCEMENT_BORDER_COLOR = (100, 100, 120)
ENHANCEMENT_SKILL_SPECIFIC_BORDER_COLOR = (40, 120, 40)  # Dark green border for skill-specific enhancements
ENHANCEMENT_TEXT_COLOR = (255, 255, 255)
ENHANCEMENT_BUTTON_COLOR = (60, 60, 80)
ENHANCEMENT_BUTTON_HOVER_COLOR = (80, 80, 100)

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

# =============================================================================
# PICKABLE SYSTEM CONFIGURATION
# =============================================================================
# Reroll Dice Pickable
REROLL_DICE_SPRITE = "resources/images/pickabels/reroll_dice.png"
REROLL_DICE_FRAME_SIZE = 16  # 16x16 frames
REROLL_DICE_FRAME_COUNT = 6  # 6 different frames
REROLL_DICE_ANIMATION_FPS = 4  # Slow animation for visibility
REROLL_DICE_DROP_CHANCE = 0.008  # 0.8% chance to drop from plants
REROLL_DICE_REROLL_CHARGES = 1  # Grants 1 reroll charge

# XP Pickable Configuration
# Green Crystal (Base)
XP_GREEN_SPRITE = "resources/images/pickabels/crystal_green.png"
XP_GREEN_FRAME_SIZE = (11, 16)  # Each frame is 11x16 pixels
XP_GREEN_FRAME_COUNT = 6  # 6 frames in the animation
XP_GREEN_ANIMATION_FPS = 8  # Animation speed
XP_GREEN_XP_VALUE = 1  # Each green crystal gives 1 XP

# Yellow Crystal
XP_YELLOW_SPRITE = "resources/images/pickabels/crystal_yellow.png"
XP_YELLOW_FRAME_SIZE = (11, 16)
XP_YELLOW_FRAME_COUNT = 6
XP_YELLOW_ANIMATION_FPS = 8
XP_YELLOW_XP_VALUE = 2

# Light Blue Crystal
XP_LIGHT_BLUE_SPRITE = "resources/images/pickabels/crystal_lightblue.png"
XP_LIGHT_BLUE_FRAME_SIZE = (11, 16)
XP_LIGHT_BLUE_FRAME_COUNT = 6
XP_LIGHT_BLUE_ANIMATION_FPS = 8
XP_LIGHT_BLUE_XP_VALUE = 5

# Blue Crystal
XP_BLUE_SPRITE = "resources/images/pickabels/crystal_blue.png"
XP_BLUE_FRAME_SIZE = (11, 16)
XP_BLUE_FRAME_COUNT = 6
XP_BLUE_ANIMATION_FPS = 8
XP_BLUE_XP_VALUE = 10

# Red Crystal
XP_RED_SPRITE = "resources/images/pickabels/crystal_red.png"
XP_RED_FRAME_SIZE = (11, 16)
XP_RED_FRAME_COUNT = 6
XP_RED_ANIMATION_FPS = 8
XP_RED_XP_VALUE = 25

# Purple Crystal
XP_PURPLE_SPRITE = "resources/images/pickabels/crystal_purple.png"
XP_PURPLE_FRAME_SIZE = (11, 16)
XP_PURPLE_FRAME_COUNT = 6
XP_PURPLE_ANIMATION_FPS = 8
XP_PURPLE_XP_VALUE = 50

# XP Drop Chances for Plants
XP_PLANT_GREEN_CHANCE = 0.99  # 99% chance for green
XP_PLANT_YELLOW_CHANCE = 0.01  # 1% chance for yellow

# XP Drop Chances for Demons
XP_DEMON_GREEN_CHANCE = 0.0   # 0% chance for green
XP_DEMON_YELLOW_CHANCE = 0.9  # 90% chance for yellow
XP_DEMON_LIGHT_BLUE_CHANCE = 0.1  # 10% chance for light blue (higher value)

# General Pickable Configuration
PICKABLE_DESPAWN_TIME = 30.0  # Pickables despawn after 30 seconds
PICKABLE_COLLECTION_RANGE = 16  # DEPRECATED: Now uses player's pickup range instead
PICKABLE_FLOAT_HEIGHT = 8  # How high pickables float above ground
PICKABLE_FLOAT_SPEED = 2.0  # Speed of floating animation

# Enhancement System Configuration
ENHANCEMENT_BASE_REROLL_CHARGES = 0  # Player starts with 0 reroll charges (changed from 1)

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

# Pickable Sound Effects
PICKABLE_DROP_SOUND_PATH = "resources/sounds/pickable_dice_roll.mp3"
PICKABLE_COLLECT_SOUND_PATH = "resources/sounds/pickable.mp3"

# Player Sound Effects
PLAYER_LEVEL_UP_SOUND_PATH = "resources/sounds/player_level_up.mp3"

# Wave Sound Effects
NEW_WAVE_SOUND_PATH = "resources/sounds/new_wave.mp3"

# Enhancement UI Sound Effects  
ENHANCEMENT_SELECT_SOUND_PATH = "resources/sounds/pickable.mp3"
ENHANCEMENT_REROLL_SOUND_PATH = "resources/sounds/pickable_dice_roll.mp3"

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
