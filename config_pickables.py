"""
Pickable Items Configuration
All pickable-related settings including XP crystals, dice, and drop chances.
"""

# =============================================================================
# REROLL DICE PICKABLE CONFIGURATION
# =============================================================================
REROLL_DICE_FRAME_SIZE = 16  # 16x16 frames
REROLL_DICE_FRAME_COUNT = 6  # 6 different frames
REROLL_DICE_ANIMATION_FPS = 4  # Slow animation for visibility
REROLL_DICE_DROP_CHANCE = 0.008  # 0.8% chance to drop from plants
REROLL_DICE_REROLL_CHARGES = 1  # Grants 1 reroll charge

# =============================================================================
# XP CRYSTAL CONFIGURATION
# =============================================================================
# Green Crystal (Base)
XP_GREEN_FRAME_SIZE = (11, 16)  # Each frame is 11x16 pixels
XP_GREEN_FRAME_COUNT = 6  # 6 frames in the animation
XP_GREEN_ANIMATION_FPS = 8  # Animation speed
XP_GREEN_XP_VALUE = 1 # Each green crystal gives 1 XP

# Yellow Crystal
XP_YELLOW_FRAME_SIZE = (11, 16)
XP_YELLOW_FRAME_COUNT = 6
XP_YELLOW_ANIMATION_FPS = 8
XP_YELLOW_XP_VALUE = 2

# Light Blue Crystal
XP_LIGHT_BLUE_FRAME_SIZE = (11, 16)
XP_LIGHT_BLUE_FRAME_COUNT = 6
XP_LIGHT_BLUE_ANIMATION_FPS = 8
XP_LIGHT_BLUE_XP_VALUE = 5

# Blue Crystal
XP_BLUE_FRAME_SIZE = (11, 16)
XP_BLUE_FRAME_COUNT = 6
XP_BLUE_ANIMATION_FPS = 8
XP_BLUE_XP_VALUE = 10

# Red Crystal
XP_RED_FRAME_SIZE = (11, 16)
XP_RED_FRAME_COUNT = 6
XP_RED_ANIMATION_FPS = 8
XP_RED_XP_VALUE = 25

# Purple Crystal
XP_PURPLE_FRAME_SIZE = (11, 16)
XP_PURPLE_FRAME_COUNT = 6
XP_PURPLE_ANIMATION_FPS = 8
XP_PURPLE_XP_VALUE = 50

# =============================================================================
# XP DROP CHANCES BY ENEMY TYPE
# =============================================================================
XP_DROP_CONFIG = {
    'Plant': {
        'green': 0.98,   # 98% chance for green (low value)
        'yellow': 0.02,  # 2% chance for yellow
        'light_blue': 0.0,
        'blue': 0.0,
        'red': 0.0,
        'purple': 0.0
    },
    'Demon': {
        'green': 0.0,    # 0% chance for green
        'yellow': 0.9,   # 90% chance for yellow
        'light_blue': 0.1,  # 10% chance for light blue (higher value)
        'blue': 0.0,
        'red': 0.0,
        'purple': 0.0
    },
    'Hero': {
        'green': 0.25,   # 25% chance for green
        'yellow': 0.70,  # 70% chance for yellow
        'light_blue': 0.05,  # 5% chance for light blue
        'blue': 0.0,
        'red': 0.0,
        'purple': 0.0
    }
}

# =============================================================================
# GENERAL PICKABLE CONFIGURATION
# =============================================================================
PICKABLE_DESPAWN_TIME = 30.0  # Pickables despawn after 30 seconds
PICKABLE_FLOAT_HEIGHT = 8  # How high pickables float above ground
PICKABLE_FLOAT_SPEED = 2.0  # Speed of floating animation

# When XP pickables are spawned, try nearby offsets to avoid overlapping existing
# pickables. These control how many attempts to try and how far from the original
# drop point to search (in pixels).
PICKABLE_SPAWN_OFFSET_ATTEMPTS = 20  # How many random placement attempts to try
PICKABLE_SPAWN_OFFSET_MAX_RADIUS = 50  # Maximum radius (pixels) to search for free spot

# Enhancement System Configuration
ENHANCEMENT_BASE_REROLL_CHARGES = 1  # Player starts with 1 reroll charge

# =============================================================================
# SCREEN CLEARER PICKABLE CONFIGURATION (ENEMY KILLER)
# =============================================================================
# Animation/frame constants removed from here to avoid duplication with config_images.py
# (Keep drop chance here; visual/animation constants live in config_images.py)
SCREEN_CLEARER_DROP_CHANCE = 0.02  # 1% chance to drop from demons (rarer than dice)

# =============================================================================
# XP MAGNET PICKABLE CONFIGURATION
# =============================================================================
XP_MAGNET_FRAME_SIZE = 20  # 20x20 frames
XP_MAGNET_FRAME_COUNT = 6  # 6 different frames
XP_MAGNET_ANIMATION_FPS = 5  # Medium animation speed
XP_MAGNET_DROP_CHANCE = 0.01  # 1% chance to drop from both plants and demons
XP_MAGNET_PULL_RADIUS = 10000  # Radius in pixels to attract XP pickables from
