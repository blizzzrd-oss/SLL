"""
Pickable Items Configuration
All pickable-related settings including XP crystals, dice, and drop chances.
"""

# =============================================================================
# REROLL DICE PICKABLE CONFIGURATION
# =============================================================================
REROLL_DICE_SPRITE = "resources/images/pickabels/reroll_dice.png"
REROLL_DICE_FRAME_SIZE = 16  # 16x16 frames
REROLL_DICE_FRAME_COUNT = 6  # 6 different frames
REROLL_DICE_ANIMATION_FPS = 4  # Slow animation for visibility
REROLL_DICE_DROP_CHANCE = 0.008  # 0.8% chance to drop from plants
REROLL_DICE_REROLL_CHARGES = 1  # Grants 1 reroll charge

# =============================================================================
# XP CRYSTAL CONFIGURATION
# =============================================================================
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

# =============================================================================
# XP DROP CHANCES BY ENEMY TYPE
# =============================================================================
# XP Drop Chances for Plants
XP_PLANT_GREEN_CHANCE = 0.98  # 98% chance for green
XP_PLANT_YELLOW_CHANCE = 0.02  # 2% chance for yellow

# XP Drop Chances for Demons
XP_DEMON_GREEN_CHANCE = 0.0   # 0% chance for green
XP_DEMON_YELLOW_CHANCE = 0.9  # 90% chance for yellow
XP_DEMON_LIGHT_BLUE_CHANCE = 0.1  # 10% chance for light blue (higher value)

# =============================================================================
# GENERAL PICKABLE CONFIGURATION
# =============================================================================
PICKABLE_DESPAWN_TIME = 30.0  # Pickables despawn after 30 seconds
PICKABLE_FLOAT_HEIGHT = 8  # How high pickables float above ground
PICKABLE_FLOAT_SPEED = 2.0  # Speed of floating animation

# =============================================================================
# PICKABLE SOUND EFFECTS
# =============================================================================
PICKABLE_DROP_SOUND_PATH = "resources/sounds/pickable_dice_roll.mp3"
PICKABLE_COLLECT_SOUND_PATH = "resources/sounds/pickable.mp3"

# =============================================================================
# SCREEN CLEARER PICKABLE CONFIGURATION (ENEMY KILLER)
# =============================================================================
SCREEN_CLEARER_SPRITE = "resources/images/pickabels/screen_clearer.png"
SCREEN_CLEARER_FRAME_SIZE = 24  # 24x24 frames (larger than dice)
SCREEN_CLEARER_FRAME_COUNT = 8  # More frames for dramatic effect
SCREEN_CLEARER_ANIMATION_FPS = 6  # Slightly faster animation
SCREEN_CLEARER_DROP_CHANCE = 0.903  # 0.3% chance to drop from demons (rarer than dice)

# =============================================================================
# XP MAGNET PICKABLE CONFIGURATION
# =============================================================================
XP_MAGNET_SPRITE = "resources/images/pickabels/xp_magnet.png"
XP_MAGNET_FRAME_SIZE = 20  # 20x20 frames
XP_MAGNET_FRAME_COUNT = 6  # 6 different frames
XP_MAGNET_ANIMATION_FPS = 5  # Medium animation speed
XP_MAGNET_DROP_CHANCE = 0.105  # 0.5% chance to drop from both plants and demons
XP_MAGNET_PULL_RADIUS = 500  # Radius in pixels to attract XP pickables from
