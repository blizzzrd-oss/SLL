"""
Sound and Audio Configuration
All sound-related settings including volumes, file paths, and audio system configuration.
"""

# =============================================================================
# AUDIO VOLUME CONFIGURATION
# =============================================================================
MUSIC_VOLUME = 0.0    # 10% default
SFX_VOLUME = 0.05      # 5% default - Skills, Attacks, Hurt, Death, Walk, Idle, level up
PICKABLE_VOLUME = 0.05 # 5% default - All pickable-related sounds
UI_VOLUME = 0.05       # 5% default - Wave, enhancement selection, UI sounds

# =============================================================================
# BACKGROUND MUSIC CONFIGURATION
# =============================================================================
BG_MUSIC_PATH = "resources/sounds/bg_music01.mp3"

# =============================================================================
# AUDIO PERFORMANCE SETTINGS
# =============================================================================
AUDIO_CHANNELS = 64  # Number of audio channels (increased for better performance)
AUDIO_FORCE_PLAY_MAX_CHANNELS_TO_STOP = 3  # Max channels to stop when force-playing important sounds

# =============================================================================
# SKILL SOUND EFFECTS
# =============================================================================
SKILL_DASH_SOUND_PATH = "resources/sounds/skill_dash.mp3"
SKILL_SLASH_SOUND_PATHS = [
    "resources/sounds/skill_slash01.wav",
    "resources/sounds/skill_slash02.wav",
    "resources/sounds/skill_slash03.mp3"
]

# =============================================================================
# HIT SOUND EFFECTS
# =============================================================================
HIT_ENEMY_SOUND_PATH = "resources/sounds/hit_enemy.mp3"
HIT_PLAYER_SOUND_PATH = "resources/sounds/hit_player.wav"

# =============================================================================
# ENEMY SOUND EFFECTS
# =============================================================================
ENEMY_PLANT_DEATH_SOUND_PATHS = [
    "resources/sounds/death_enemy_plant01.wav",
    "resources/sounds/death_enemy_plant02.wav", 
    "resources/sounds/death_enemy_plant03.wav"
]

# =============================================================================
# PICKABLE SOUND EFFECTS
# =============================================================================
PICKABLE_DROP_SOUND_PATH = "resources/sounds/pickable_drop.mp3"  # General pickable drop sound (placeholder)
PICKABLE_DICE_DROP_SOUND_PATH = "resources/sounds/pickable_dice_roll.mp3"  # Specific to dice drops
PICKABLE_COLLECT_SOUND_PATH = "resources/sounds/pickable.mp3"

# =============================================================================
# PLAYER SOUND EFFECTS
# =============================================================================
PLAYER_LEVEL_UP_SOUND_PATH = "resources/sounds/player_level_up.mp3"

# =============================================================================
# WAVE SOUND EFFECTS
# =============================================================================
NEW_WAVE_SOUND_PATH = "resources/sounds/new_wave.mp3"

# =============================================================================
# ENHANCEMENT UI SOUND EFFECTS
# =============================================================================
ENHANCEMENT_SELECT_SOUND_PATH = "resources/sounds/pickable.mp3"
ENHANCEMENT_REROLL_SOUND_PATH = "resources/sounds/pickable_dice_roll.mp3"
