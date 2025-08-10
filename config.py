# HUD toggle key
import pygame
HUD_TOGGLE_KEY = pygame.K_TAB
# HUD section config
HUD_TOP_HEIGHT = 80
HUD_BOTTOM_HEIGHT = 100
HUD_LEFT_WIDTH = 300
HUD_RIGHT_WIDTH = 300
HUD_ALPHA = 120
HUD_COLOR = (40, 40, 40, HUD_ALPHA)
HUD_LABEL_COLOR = (200, 200, 200)
HUD_LABEL_FONT_SIZE = 32
# Game loop UI and menu config
GAME_BG_COLOR = (20, 20, 20)
GAME_OVERLAY_COLOR = (0, 0, 0, 180) # Semi-transparent black
PAUSE_OVERLAY_COLOR = (0, 0, 0, 140) # Semi-transparent black
GAME_OVER_FONT_SIZE = 120
PAUSE_FONT_SIZE = 80
MENU_FONT_SIZE = 48
PAUSE_MENU_HIGHLIGHT_COLOR = (255, 255, 0)
PAUSE_MENU_TEXT_COLOR = (255, 255, 255)
PAUSE_MENU_OPTIONS = ["Resume", "Surrender", "Settings", "Quit"]
# Player hurt animation config
PLAYER_HURT_HP_SPRITE = 'resources/images/player/Hurt/Slime1_Hurt_full_hp.png'
PLAYER_HURT_BARRIER_SPRITE = 'resources/images/player/Hurt/Slime1_Hurt_full_barrier.png'
PLAYER_HURT_ANIMATION_FPS = 12  # Frames per second for hurt
# FPS options
GAME_FPS_OPTIONS = [60, 120, 240]
GAME_DEFAULT_FPS = 60
# Player sprite/animation config
PLAYER_IDLE_SPRITE = 'resources/images/player/Idle/Slime1_Idle_full.png'
PLAYER_WALK_SPRITE = 'resources/images/player/Walk/Slime1_Walk_full.png'
PLAYER_RUN_SPRITE = 'resources/images/player/Run/Slime1_Run_full.png'
PLAYER_RUN_ANIMATION_FPS = 14  # Frames per second for run
PLAYER_SPRITE_FRAME_WIDTH = 64  # Adjust to your sprite frame width
PLAYER_SPRITE_FRAME_HEIGHT = 64 # Adjust to your sprite frame height
PLAYER_IDLE_ANIMATION_FPS = 6   # Frames per second for idle
PLAYER_WALK_ANIMATION_FPS = 10  # Frames per second for walk
# General Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_GRAY = (128, 128, 128)
# UI Colors
COLOR_BG = (30, 30, 30)
COLOR_TEXT = (200, 200, 200)
COLOR_HIGHLIGHT = (200, 200, 50)
COLOR_SLIDER_MUSIC = (100, 100, 255)
COLOR_SLIDER_SFX = (100, 255, 100)
COLOR_BACK = (180, 180, 180)

# UI Font Sizes
FONT_SIZE_LARGE = 48
FONT_SIZE_SMALL = 32

# Window size
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
"""
Game configuration constants and settings.
"""

# Player attribute defaults
PLAYER_START_HEALTH = 100
PLAYER_START_BARRIER = 50
PLAYER_BARRIER_DECAY_PERCENT_PER_SEC = 10  # percent per second
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
PLAYER_PASSIVE_SKILLS = {
	'toughness': 0,
	'regeneration': 0,
	'barrier_boost': 0,
	# Add more passives as needed
}
PLAYER_ACTIVE_SKILLS = {
	'slash': 0,
	'dash': 0,
	'barrier_burst': 0,
	# Add more actives as needed
}
SAVEGAME_PATH = "savegame.sav"

# Audio settings
MUSIC_VOLUME = 0.1  # 10%
SFX_VOLUME = 0.1    # 10%
BG_MUSIC_PATH = "resources/sounds/bg_music01.mp3"
