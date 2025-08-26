"""
Sound manager for preloading and caching all game sounds.
"""
import pygame
import os
import random
from utils.resource_path import resource_path
from config_sounds import (
    SKILL_DASH_SOUND_PATH, SKILL_SLASH_SOUND_PATHS,
    ENEMY_PLANT_DEATH_SOUND_PATHS, SFX_VOLUME, PICKABLE_VOLUME, UI_VOLUME,
    HIT_ENEMY_SOUND_PATH, HIT_PLAYER_SOUND_PATH,
    PICKABLE_DROP_SOUND_PATH, PICKABLE_DICE_DROP_SOUND_PATH, PICKABLE_COLLECT_SOUND_PATH,
    PLAYER_LEVEL_UP_SOUND_PATH, NEW_WAVE_SOUND_PATH,
    ENHANCEMENT_SELECT_SOUND_PATH, ENHANCEMENT_REROLL_SOUND_PATH,
    AUDIO_FORCE_PLAY_MAX_CHANNELS_TO_STOP
)


class SoundManager:
    """Centralized sound management with preloading."""
    
    _instance = None
    _sounds_cache = {}
    _initialized = False
    _slash_sound_index = 0  # For rotating slash sounds
    
    # Volume levels (0.0 to 1.0)
    _sfx_volume = SFX_VOLUME
    _pickable_volume = PICKABLE_VOLUME 
    _ui_volume = UI_VOLUME
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def set_sfx_volume(cls, volume):
        """Set SFX volume (0-100)."""
        cls._sfx_volume = volume / 100.0
    
    @classmethod 
    def set_pickable_volume(cls, volume):
        """Set Pickable volume (0-100)."""
        cls._pickable_volume = volume / 100.0
        
    @classmethod
    def set_ui_volume(cls, volume):
        """Set UI volume (0-100)."""
        cls._ui_volume = volume / 100.0
    
    @classmethod
    def get_sfx_volume(cls):
        """Get current SFX volume (0.0-1.0)."""
        return cls._sfx_volume
        
    @classmethod
    def get_pickable_volume(cls):
        """Get current Pickable volume (0.0-1.0)."""
        return cls._pickable_volume
        
    @classmethod
    def get_ui_volume(cls):
        """Get current UI volume (0.0-1.0)."""
        return cls._ui_volume

    @classmethod
    def _load_single_sound(cls, path, name):
        """Helper method to load a single sound file."""
        try:
            full_path = resource_path(path)
            if os.path.exists(full_path):
                sound = pygame.mixer.Sound(full_path)
                print(f"[SOUND] Loaded {name}")
                return sound
            else:
                print(f"[WARNING] Sound file not found: {full_path}")
                return None
        except Exception as e:
            print(f"[WARNING] Failed to load {name}: {e}")
            return None

    @classmethod
    def _load_sound_list(cls, paths, name_prefix):
        """Helper method to load a list of sound files."""
        sounds = []
        for i, path in enumerate(paths):
            sound = cls._load_single_sound(path, f"{name_prefix} {i+1}")
            if sound:
                sounds.append(sound)
        return sounds

    @classmethod
    def _load_sound_dict(cls, sound_dict, cache_prefix=""):
        """Helper method to load sounds from a dictionary."""
        loaded_count = 0
        for sound_type, sound_path in sound_dict.items():
            sound = cls._load_single_sound(sound_path, f"{cache_prefix}{sound_type}")
            if sound:
                cache_key = f"{cache_prefix}{sound_type}" if cache_prefix else sound_type
                cls._sounds_cache[cache_key] = sound
                loaded_count += 1
        return loaded_count
    
    @classmethod
    def preload_all_sounds(cls):
        """Preload all game sounds during loading screen."""
        if cls._initialized:
            return True
            
        print("[SOUND] Preloading game sounds...")
        success_count = 0
        
        # Single skill sounds
        skill_sounds = {'dash': SKILL_DASH_SOUND_PATH}
        success_count += cls._load_sound_dict(skill_sounds, "skill_")
        
        # Multiple slash sounds (special handling)
        slash_sounds = cls._load_sound_list(SKILL_SLASH_SOUND_PATHS, "slash sound")
        if slash_sounds:
            cls._sounds_cache['slash_sounds'] = slash_sounds
            success_count += len(slash_sounds)
        
        # Enemy death sounds (special handling) 
        plant_death_sounds = cls._load_sound_list(ENEMY_PLANT_DEATH_SOUND_PATHS, "plant death sound")
        if plant_death_sounds:
            cls._sounds_cache['plant_death_sounds'] = plant_death_sounds
            success_count += len(plant_death_sounds)
        # Per-enemy death sounds mapping (optional)
        try:
            from config_sounds import ENEMY_DEATH_SOUND_PATHS
            for etype, paths in ENEMY_DEATH_SOUND_PATHS.items():
                sounds = cls._load_sound_list(paths, f"{etype} death sound")
                if sounds:
                    cls._sounds_cache[f'death_{etype}'] = sounds
                    success_count += len(sounds)
        except Exception:
            pass
        
        # Pickable sounds
        pickable_sounds = {
            'drop': PICKABLE_DROP_SOUND_PATH,
            'dice_drop': PICKABLE_DICE_DROP_SOUND_PATH,
            'collect': PICKABLE_COLLECT_SOUND_PATH
        }
        success_count += cls._load_sound_dict(pickable_sounds, "pickable_")
        
        # Hit sounds (global) and per-enemy-type hit sounds
        hit_sounds = {
            'enemy': HIT_ENEMY_SOUND_PATH,
            'player': HIT_PLAYER_SOUND_PATH
        }
        success_count += cls._load_sound_dict(hit_sounds, "hit_")

        # Per-enemy hit sounds (optional)
        try:
            from config_sounds import ENEMY_HIT_SOUND_PATHS
            # Load each list into cache with key 'hit_<EnemyName>_<i>' and a list entry
            for etype, paths in ENEMY_HIT_SOUND_PATHS.items():
                sounds = cls._load_sound_list(paths, f"{etype} hit sound")
                if sounds:
                    cls._sounds_cache[f'hit_{etype}'] = sounds
                    success_count += len(sounds)
        except Exception:
            # ENEMY_HIT_SOUND_PATHS optional
            pass
        
        # Player/SFX sounds
        sfx_sounds = {
            'level_up': PLAYER_LEVEL_UP_SOUND_PATH
        }
        success_count += cls._load_sound_dict(sfx_sounds, "sfx_")
        
        # UI sounds
        ui_sounds = {
            'wave': NEW_WAVE_SOUND_PATH,
            'enhancement_select': ENHANCEMENT_SELECT_SOUND_PATH,
            'enhancement_reroll': ENHANCEMENT_REROLL_SOUND_PATH
        }
        success_count += cls._load_sound_dict(ui_sounds, "ui_")
        
        cls._initialized = True
        print(f"[SOUND] Preloading complete: {success_count} sounds loaded")
        return success_count > 0
    
    @classmethod
    def _play_sound_with_volume(cls, sound, volume, sound_name, force_play=False):
        """Helper method to play a sound with specific volume."""
        if not sound:
            print(f"[WARNING] {sound_name} not found in cache")
            return False
            
        try:
            sound.set_volume(volume)
            channel = sound.play()
            
            if channel is None and force_play:
                cls.force_play_sound(sound, sound_name)
            elif channel is None:
                print(f"[WARNING] Could not play {sound_name}: No available channels")
                return False
            return True
        except Exception as e:
            print(f"[WARNING] Failed to play {sound_name}: {e}")
            return False

    @classmethod
    def get_skill_sound(cls, skill_name):
        """Get a preloaded skill sound."""
        return cls._sounds_cache.get(f'skill_{skill_name}')
    
    @classmethod
    def get_random_plant_death_sound(cls):
        """Get a random plant death sound."""
        sounds = cls._sounds_cache.get('plant_death_sounds')
        if sounds and len(sounds) > 0:
            return random.choice(sounds)
        return None

    @classmethod
    def get_random_death_sound_for_type(cls, enemy_type_name: str):
        sounds = cls._sounds_cache.get(f'death_{enemy_type_name}')
        if sounds and len(sounds) > 0:
            return random.choice(sounds)
        # Fallback to plant death
        return cls.get_random_plant_death_sound()

    @classmethod
    def get_random_enemy_hit_sound_for_type(cls, enemy_type_name: str):
        """Get a random hit sound for a specific enemy type, falling back to global enemy hit."""
        import random
        sounds = cls._sounds_cache.get(f'hit_{enemy_type_name}')
        if sounds and len(sounds) > 0:
            return random.choice(sounds)
        # Fallback to global enemy hit
        return cls._sounds_cache.get('hit_enemy')
    
    @classmethod
    def get_next_slash_sound(cls):
        """Get the next slash sound in rotation."""
        sounds = cls._sounds_cache.get('slash_sounds')
        if sounds and len(sounds) > 0:
            sound = sounds[cls._slash_sound_index]
            cls._slash_sound_index = (cls._slash_sound_index + 1) % len(sounds)
            return sound
        return None
    
    @classmethod
    def play_skill_sound(cls, skill_name):
        """Play a skill sound if available."""
        if skill_name == 'slash':
            sound = cls.get_next_slash_sound()
        else:
            sound = cls.get_skill_sound(skill_name)
        
        cls._play_sound_with_volume(sound, cls._sfx_volume, f"skill {skill_name}")
    
    @classmethod
    def play_random_plant_death_sound(cls):
        """Play a random plant death sound if available."""
        sound = cls.get_random_plant_death_sound()
        cls._play_sound_with_volume(sound, cls._sfx_volume, "plant death sound", force_play=True)
    
    @classmethod
    def play_hit_sound(cls, hit_type):
        """Play a hit sound (enemy or player)."""
        sound = cls._sounds_cache.get(f'hit_{hit_type}')
        cls._play_sound_with_volume(sound, cls._sfx_volume, f"hit sound {hit_type}", force_play=True)
    
    # Pickable sounds
    @classmethod
    def play_pickable_drop_sound(cls):
        """Play the pickable drop sound."""
        sound = cls._sounds_cache.get('pickable_drop')
        cls._play_sound_with_volume(sound, cls._pickable_volume, "pickable drop sound", force_play=True)
    
    @classmethod
    def play_pickable_dice_drop_sound(cls):
        """Play the pickable dice drop sound."""
        sound = cls._sounds_cache.get('pickable_dice_drop')
        cls._play_sound_with_volume(sound, cls._pickable_volume, "pickable dice drop sound", force_play=True)
    
    @classmethod
    def play_pickable_collect_sound(cls):
        """Play the pickable collect sound."""
        sound = cls._sounds_cache.get('pickable_collect')
        cls._play_sound_with_volume(sound, cls._pickable_volume, "pickable collect sound", force_play=True)
    
    # SFX sounds
    @classmethod
    def play_player_level_up_sound(cls):
        """Play the player level up sound."""
        sound = cls._sounds_cache.get('sfx_level_up')
        cls._play_sound_with_volume(sound, cls._sfx_volume, "player level up sound", force_play=True)
    
    # UI sounds
    @classmethod
    def play_wave_sound(cls):
        """Play the new wave sound."""
        sound = cls._sounds_cache.get('ui_wave')
        cls._play_sound_with_volume(sound, cls._ui_volume, "wave sound", force_play=True)
    
    @classmethod
    def play_enhancement_select_sound(cls):
        """Play the enhancement selection sound."""
        sound = cls._sounds_cache.get('ui_enhancement_select')
        cls._play_sound_with_volume(sound, cls._ui_volume, "enhancement select sound", force_play=True)
    
    @classmethod
    def play_enhancement_reroll_sound(cls):
        """Play the enhancement reroll sound."""
        sound = cls._sounds_cache.get('ui_enhancement_reroll')
        cls._play_sound_with_volume(sound, cls._ui_volume, "enhancement reroll sound", force_play=True)
    
    @classmethod
    def force_play_sound(cls, sound, sound_type="unknown"):
        """Force play a sound with higher priority, stopping other sounds if needed."""
        if not sound:
            return False
            
        try:
            # First try normal play
            channel = sound.play()
            if channel is not None:
                return True
                
            # If no channels available, aggressively free up channels
            # Stop multiple channels to ensure we can play the sound
            channels_stopped = 0
            total_channels = pygame.mixer.get_num_channels()
            
            for i in range(total_channels):
                channel_obj = pygame.mixer.Channel(i)
                if channel_obj.get_busy():
                    channel_obj.stop()
                    channels_stopped += 1
                    
                    # Try to play after stopping each channel
                    channel = sound.play()
                    if channel is not None:
                        if channels_stopped > 1:
                            print(f"[SOUND] Force-played {sound_type} by stopping {channels_stopped} channels")
                        else:
                            print(f"[SOUND] Force-played {sound_type} by stopping 1 channel")
                        return True
                    
                    # If stopping one channel wasn't enough, try stopping a few more
                    if channels_stopped >= AUDIO_FORCE_PLAY_MAX_CHANNELS_TO_STOP:  # Use config limit
                        break
                        
            print(f"[WARNING] Could not force-play {sound_type}: Unable to free channels after stopping {channels_stopped}")
            return False
            
        except Exception as e:
            print(f"[WARNING] Failed to force-play {sound_type}: {e}")
            return False
    
    @classmethod
    def get_channel_info(cls):
        """Get information about current channel usage for debugging."""
        total_channels = pygame.mixer.get_num_channels()
        busy_channels = sum(1 for i in range(total_channels) if pygame.mixer.Channel(i).get_busy())
        return f"Channels: {busy_channels}/{total_channels} busy"
    
    @classmethod
    def cleanup_finished_channels(cls):
        """Clean up any channels that should be finished playing."""
        cleaned = 0
        total_channels = pygame.mixer.get_num_channels()
        
        for i in range(total_channels):
            channel_obj = pygame.mixer.Channel(i)
            if channel_obj.get_busy():
                # Check if the channel is playing an extremely short sound that might be stuck
                # This is a safety mechanism to prevent channel leaks
                try:
                    # For now, we'll just count busy channels
                    # In a more sophisticated system, we'd track sound start times
                    pass
                except:
                    # If there's any issue with the channel, stop it
                    channel_obj.stop()
                    cleaned += 1
        
        if cleaned > 0:
            print(f"[SOUND] Cleaned up {cleaned} potentially stuck channels")
    
    @classmethod
    def debug_sound_system(cls):
        """Print debug information about the sound system."""
        print(f"[SOUND DEBUG] {cls.get_channel_info()}")
        print(f"[SOUND DEBUG] Cached sounds: {list(cls._sounds_cache.keys())}")
        print(f"[SOUND DEBUG] Initialized: {cls._initialized}")
        print(f"[SOUND DEBUG] SFX Volume: {cls._sfx_volume}")
        print(f"[SOUND DEBUG] Pickable Volume: {cls._pickable_volume}")
        print(f"[SOUND DEBUG] UI Volume: {cls._ui_volume}")
