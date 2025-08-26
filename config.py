import pygame
import os

# Import configuration modules
from config_enemies import *
from config_waves import *
from config_sounds import *
from config_images import *

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

# =============================================================================
# SKILL CONFIGURATION
# =============================================================================
SKILL_COOLDOWN = 0.5  # Default cooldown for skills (seconds)

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
# PICKABLE SYSTEM CONFIGURATION
# =============================================================================
# Reroll Dice Pickable
REROLL_DICE_DROP_CHANCE = 0.008  # 0.8% chance to drop from plants
REROLL_DICE_REROLL_CHARGES = 1  # Grants 1 reroll charge

# XP Pickable Configuration
# Green Crystal (Base)
XP_GREEN_XP_VALUE = 1  # Each green crystal gives 1 XP

# Yellow Crystal
XP_YELLOW_XP_VALUE = 2

# Light Blue Crystal
XP_LIGHT_BLUE_XP_VALUE = 5

# Blue Crystal
XP_BLUE_XP_VALUE = 10

# Red Crystal
XP_RED_XP_VALUE = 25

# Purple Crystal
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
PICKABLE_FLOAT_HEIGHT = 8  # How high pickables float above ground
PICKABLE_FLOAT_SPEED = 2.0  # Speed of floating animation

# Screen Clearer Configuration
SCREEN_CLEARER_DROP_CHANCE = 0.003  # 0.3% chance to drop from demons (rarer than dice)

# XP Magnet Configuration
XP_MAGNET_DROP_CHANCE = 0.005  # 0.5% chance to drop from both plants and demons
XP_MAGNET_PULL_RADIUS = 500  # Radius in pixels to attract XP pickables from

# Enhancement System Configuration
ENHANCEMENT_BASE_REROLL_CHARGES = 1  # Player starts with 1 reroll charge

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
