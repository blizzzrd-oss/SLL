"""
Image and Visual Asset Configuration
All image paths, sprite configurations, and visual asset definitions.
"""

import os

# =============================================================================
# BACKGROUND AND BIOME TILES
# =============================================================================
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

# Grass tile directory
GRASS_TILES_PATH = "resources/images/Tiles/grass"

# =============================================================================
# PLAYER SPRITES AND ANIMATIONS
# =============================================================================
# Player Sprite Configuration
PLAYER_IDLE_SPRITE = 'resources/images/player/Idle/Slime1_Idle_full.png'
PLAYER_WALK_SPRITE = 'resources/images/player/Walk/Slime1_Walk_full.png'
PLAYER_RUN_SPRITE = 'resources/images/player/Run/Slime1_Run_full.png'
PLAYER_HURT_HP_SPRITE = 'resources/images/player/Hurt/Slime1_Hurt_full_hp.png'
PLAYER_HURT_BARRIER_SPRITE = 'resources/images/player/Hurt/Slime1_Hurt_full_barrier.png'

# Player Animation Configuration
PLAYER_SPRITE_FRAME_WIDTH = 64
PLAYER_SPRITE_FRAME_HEIGHT = 64

# =============================================================================
# SKILL SPRITES AND EFFECTS
# =============================================================================
# Slash Skill Configuration
SLASH_SHEET_PATH = 'resources/images/player_melee/slash/player_melee_slash.png'
SLASH_SHEET_PATH_ALT = os.path.join('resources', 'images', 'player_melee', 'slash', 'player_melee_slash.png')

# =============================================================================
# PICKABLE SPRITES
# =============================================================================
# Reroll Dice Pickable
REROLL_DICE_SPRITE = "resources/images/pickabels/reroll_dice.png"

# XP Crystal Sprites
XP_GREEN_SPRITE = "resources/images/pickabels/crystal_green.png"
XP_YELLOW_SPRITE = "resources/images/pickabels/crystal_yellow.png"
XP_LIGHT_BLUE_SPRITE = "resources/images/pickabels/crystal_lightblue.png"
XP_BLUE_SPRITE = "resources/images/pickabels/crystal_blue.png"
XP_RED_SPRITE = "resources/images/pickabels/crystal_red.png"
XP_PURPLE_SPRITE = "resources/images/pickabels/crystal_purple.png"

# Other Pickable Sprites
SCREEN_CLEARER_SPRITE = "resources/images/pickabels/screen_clearer.png"
XP_MAGNET_SPRITE = "resources/images/pickabels/xp_magnet.png"

# =============================================================================
# ENEMY SPRITES
# =============================================================================
# Demon Enemy Sprites
DEMON_SPRITE_FILES = {
    'idle': 'Demon_Idle_full.png',
    'flying': 'Demon_Flying_full.png', 
    'attack': 'Demon_Attack_full.png',
    'hurt': 'Demon_Hurt_full.png',
    'death': 'Demon_Death_full.png',
}

# Demon sprite base path
DEMON_SPRITES_BASE_PATH = "resources/images/enemies/Deamon/"

# Plant Enemy Sprites
PLANT_SPRITE_FILES = {
    'idle': 'Plant_Idle_full.png',
    'walk': 'Plant_Walk_full.png',
    'run': 'Plant_Run_full.png',
    'death': 'Plant_Death_full.png',
    'attack': 'Plant_Attack_full.png',
}

# Plant sprite base path
PLANT_SPRITES_BASE_PATH = "resources/images/enemies/Plant"

# =============================================================================
# UI AND MENU IMAGES
# =============================================================================
# Menu button images
MENU_BUTTON_IMAGE_PATH = r'C:\Repos\SLL\resources\images\UI\menu\buttons\slime_button_292x145.png'
MENU_BUTTON_WIDTH = 292
MENU_BUTTON_HEIGHT = 145

# Game mode selection image
GAMEMODE_SELECT_IMAGE_PATH = r'C:\Repos\SLL\resources\images\UI\menu\buttons\slect_game_mode.png'
