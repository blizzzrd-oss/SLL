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
    def preload_all_sounds(cls):
        """Preload all game sounds during loading screen."""
        if cls._initialized:
            return True
            
        print("[SOUND] Preloading game sounds...")
        success_count = 0
        total_sounds = 0
        
        # Single skill sounds
        single_skill_sounds = {
            'dash': SKILL_DASH_SOUND_PATH
        }
        
        for skill_name, sound_path in single_skill_sounds.items():
            total_sounds += 1
            try:
                full_path = resource_path(sound_path)
                if os.path.exists(full_path):
                    sound = pygame.mixer.Sound(full_path)
                    # Volume will be set dynamically when played
                    cls._sounds_cache[f'skill_{skill_name}'] = sound
                    success_count += 1
                    print(f"[SOUND] Loaded skill sound: {skill_name}")
                else:
                    print(f"[WARNING] Skill sound file not found: {full_path}")
            except Exception as e:
                print(f"[WARNING] Failed to load skill sound {skill_name}: {e}")
        
        # Multiple slash sounds
        slash_sounds = []
        for i, sound_path in enumerate(SKILL_SLASH_SOUND_PATHS):
            total_sounds += 1
            try:
                full_path = resource_path(sound_path)
                if os.path.exists(full_path):
                    sound = pygame.mixer.Sound(full_path)
                    # Volume will be set dynamically when played
                    slash_sounds.append(sound)
                    success_count += 1
                    print(f"[SOUND] Loaded slash sound {i+1}")
                else:
                    print(f"[WARNING] Slash sound file not found: {full_path}")
            except Exception as e:
                print(f"[WARNING] Failed to load slash sound {i+1}: {e}")
        
        if slash_sounds:
            cls._sounds_cache['slash_sounds'] = slash_sounds
        
        # Enemy death sounds
        plant_death_sounds = []
        for i, sound_path in enumerate(ENEMY_PLANT_DEATH_SOUND_PATHS):
            total_sounds += 1
            try:
                full_path = resource_path(sound_path)
                if os.path.exists(full_path):
                    sound = pygame.mixer.Sound(full_path)
                    # Volume will be set dynamically when played
                    plant_death_sounds.append(sound)
                    success_count += 1
                    print(f"[SOUND] Loaded plant death sound {i+1}")
                else:
                    print(f"[WARNING] Plant death sound file not found: {full_path}")
            except Exception as e:
                print(f"[WARNING] Failed to load plant death sound {i+1}: {e}")
        
        if plant_death_sounds:
            cls._sounds_cache['plant_death_sounds'] = plant_death_sounds
        
        # Pickable sounds
        pickable_sounds = {
            'drop': PICKABLE_DROP_SOUND_PATH,
            'dice_drop': PICKABLE_DICE_DROP_SOUND_PATH,
            'collect': PICKABLE_COLLECT_SOUND_PATH
        }
        
        for sound_type, sound_path in pickable_sounds.items():
            total_sounds += 1
            try:
                full_path = resource_path(sound_path)
                if os.path.exists(full_path):
                    sound = pygame.mixer.Sound(full_path)
                    # Volume will be set dynamically when played (pickable category)
                    cls._sounds_cache[f'pickable_{sound_type}'] = sound
                    success_count += 1
                    print(f"[SOUND] Loaded pickable sound: {sound_type}")
                else:
                    print(f"[WARNING] Pickable sound file not found: {full_path}")
            except Exception as e:
                print(f"[WARNING] Failed to load pickable sound {sound_type}: {e}")
        
        # Player sounds
        player_sounds = {
            'level_up': PLAYER_LEVEL_UP_SOUND_PATH,
            'new_wave': NEW_WAVE_SOUND_PATH,
            'enhancement_select': ENHANCEMENT_SELECT_SOUND_PATH,
            'enhancement_reroll': ENHANCEMENT_REROLL_SOUND_PATH
        }
        
        for sound_type, sound_path in player_sounds.items():
            total_sounds += 1
            try:
                full_path = resource_path(sound_path)
                if os.path.exists(full_path):
                    sound = pygame.mixer.Sound(full_path)
                    # Volume will be set dynamically when played (SFX category)
                    cls._sounds_cache[f'player_{sound_type}'] = sound
                    success_count += 1
                    print(f"[SOUND] Loaded player sound: {sound_type}")
                else:
                    print(f"[WARNING] Player sound file not found: {full_path}")
            except Exception as e:
                print(f"[WARNING] Failed to load player sound {sound_type}: {e}")
        
        # Hit sounds
        hit_sounds = {
            'enemy': HIT_ENEMY_SOUND_PATH,
            'player': HIT_PLAYER_SOUND_PATH
        }
        
        for hit_type, sound_path in hit_sounds.items():
            total_sounds += 1
            try:
                full_path = resource_path(sound_path)
                if os.path.exists(full_path):
                    sound = pygame.mixer.Sound(full_path)
                    # Volume will be set dynamically when played (SFX category)
                    cls._sounds_cache[f'hit_{hit_type}'] = sound
                    success_count += 1
                    print(f"[SOUND] Loaded hit sound: {hit_type}")
                else:
                    print(f"[WARNING] Hit sound file not found: {full_path}")
            except Exception as e:
                print(f"[WARNING] Failed to load hit sound {hit_type}: {e}")
        
        # UI sounds (wave, enhancement selection, etc.)
        ui_sounds = {
            'wave': NEW_WAVE_SOUND_PATH,
            'enhancement_select': ENHANCEMENT_SELECT_SOUND_PATH,
            'enhancement_reroll': ENHANCEMENT_REROLL_SOUND_PATH
        }
        
        for sound_type, sound_path in ui_sounds.items():
            total_sounds += 1
            try:
                full_path = resource_path(sound_path)
                if os.path.exists(full_path):
                    sound = pygame.mixer.Sound(full_path)
                    # Volume will be set dynamically when played (UI category)
                    cls._sounds_cache[f'ui_{sound_type}'] = sound
                    success_count += 1
                    print(f"[SOUND] Loaded UI sound: {sound_type}")
                else:
                    print(f"[WARNING] UI sound file not found: {full_path}")
            except Exception as e:
                print(f"[WARNING] Failed to load UI sound {sound_type}: {e}")
        
        cls._initialized = True
        print(f"[SOUND] Preloading complete: {success_count}/{total_sounds} sounds loaded")
        return success_count > 0
    
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
            # Special handling for slash sounds (rotating)
            sound = cls.get_next_slash_sound()
        else:
            # Normal skill sounds
            sound = cls.get_skill_sound(skill_name)
        
        if sound:
            try:
                # Set volume for SFX category
                sound.set_volume(cls._sfx_volume)
                
                # Try to play the sound, and if no channels are available, find a free one
                channel = sound.play()
                if channel is None:
                    # No free channels, try to stop the oldest channel and play again
                    pygame.mixer.stop()  # Stop all sounds briefly to free channels
                    channel = sound.play()
                    if channel is None:
                        print(f"[WARNING] Could not play skill sound {skill_name}: No available channels")
            except Exception as e:
                print(f"[WARNING] Failed to play skill sound {skill_name}: {e}")
    
    @classmethod
    def play_random_plant_death_sound(cls):
        """Play a random plant death sound if available."""
        sound = cls.get_random_plant_death_sound()
        if sound:
            # Set volume for SFX category
            sound.set_volume(cls._sfx_volume)
            # Death sounds are important for player feedback, so force-play them
            cls.force_play_sound(sound, "plant death sound")
    
    @classmethod
    def play_hit_sound(cls, hit_type):
        """Play a hit sound (enemy or player)."""
        sound = cls._sounds_cache.get(f'hit_{hit_type}')
        if sound:
            try:
                # Set volume for SFX category
                sound.set_volume(cls._sfx_volume)
                
                # Hit sounds should play reliably for feedback
                channel = sound.play()
                if channel is None:
                    # Hit sounds are important for feedback, force play them
                    cls.force_play_sound(sound, f"hit sound {hit_type}")
            except Exception as e:
                print(f"[WARNING] Failed to play hit sound {hit_type}: {e}")
        else:
            print(f"[WARNING] Hit sound {hit_type} not found in cache")
    
    @classmethod
    def play_pickable_drop_sound(cls):
        """Play the pickable drop sound."""
        sound = cls._sounds_cache.get('pickable_drop')
        if sound:
            try:
                # Set volume for Pickable category
                sound.set_volume(cls._pickable_volume)
                
                channel = sound.play()
                if channel is None:
                    # Force play pickable sounds as they provide important feedback
                    cls.force_play_sound(sound, "pickable drop sound")
            except Exception as e:
                print(f"[WARNING] Failed to play pickable drop sound: {e}")
    
    @classmethod
    def play_pickable_dice_drop_sound(cls):
        """Play the pickable dice drop sound."""
        sound = cls._sounds_cache.get('pickable_dice_drop')
        if sound:
            try:
                # Set volume for Pickable category
                sound.set_volume(cls._pickable_volume)
                
                channel = sound.play()
                if channel is None:
                    # Force play pickable sounds as they provide important feedback
                    cls.force_play_sound(sound, "pickable dice drop sound")
            except Exception as e:
                print(f"[WARNING] Failed to play pickable dice drop sound: {e}")
    
    @classmethod
    def play_pickable_collect_sound(cls):
        """Play the pickable collect sound."""
        sound = cls._sounds_cache.get('pickable_collect')
        if sound:
            try:
                # Set volume for Pickable category
                sound.set_volume(cls._pickable_volume)
                
                channel = sound.play()
                if channel is None:
                    # Force play pickable sounds as they provide important feedback
                    cls.force_play_sound(sound, "pickable collect sound")
            except Exception as e:
                print(f"[WARNING] Failed to play pickable collect sound: {e}")
    
    @classmethod
    def play_player_level_up_sound(cls):
        """Play the player level up sound."""
        sound = cls._sounds_cache.get('player_level_up')
        if sound:
            try:
                # Set volume for SFX category
                sound.set_volume(cls._sfx_volume)
                
                channel = sound.play()
                if channel is None:
                    # Force play level up sound as it's important player feedback
                    cls.force_play_sound(sound, "player level up sound")
            except Exception as e:
                print(f"[WARNING] Failed to play player level up sound: {e}")
    
    @classmethod
    def play_new_wave_sound(cls):
        """Play the new wave sound."""
        sound = cls._sounds_cache.get('player_new_wave')
        if sound:
            try:
                channel = sound.play()
                if channel is None:
                    # Force play new wave sound as it's important game feedback
                    cls.force_play_sound(sound, "new wave sound")
            except Exception as e:
                print(f"[WARNING] Failed to play new wave sound: {e}")
    
    @classmethod
    def play_enhancement_select_sound(cls):
        """Play the enhancement selection sound."""
        sound = cls._sounds_cache.get('player_enhancement_select')
        if sound:
            try:
                channel = sound.play()
                if channel is None:
                    # Force play enhancement sound as it's important UI feedback
                    cls.force_play_sound(sound, "enhancement select sound")
            except Exception as e:
                print(f"[WARNING] Failed to play enhancement select sound: {e}")
    
    @classmethod
    def play_enhancement_reroll_sound(cls):
        """Play the enhancement reroll sound."""
        sound = cls._sounds_cache.get('player_enhancement_reroll')
        if sound:
            try:
                channel = sound.play()
                if channel is None:
                    # Force play reroll sound as it's important UI feedback
                    cls.force_play_sound(sound, "enhancement reroll sound")
            except Exception as e:
                print(f"[WARNING] Failed to play enhancement reroll sound: {e}")
    
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
    def play_wave_sound(cls):
        """Play the new wave sound."""
        sound = cls._sounds_cache.get('ui_wave')
        if sound:
            try:
                # Set volume for UI category
                sound.set_volume(cls._ui_volume)
                
                channel = sound.play()
                if channel is None:
                    # Force play wave sound as it's important UI feedback
                    cls.force_play_sound(sound, "wave sound")
            except Exception as e:
                print(f"[WARNING] Failed to play wave sound: {e}")
    
    @classmethod
    def play_enhancement_select_sound(cls):
        """Play the enhancement selection sound."""
        sound = cls._sounds_cache.get('ui_enhancement_select')
        if sound:
            try:
                # Set volume for UI category
                sound.set_volume(cls._ui_volume)
                
                channel = sound.play()
                if channel is None:
                    # Force play enhancement sound as it's important UI feedback
                    cls.force_play_sound(sound, "enhancement select sound")
            except Exception as e:
                print(f"[WARNING] Failed to play enhancement select sound: {e}")
    
    @classmethod
    def play_enhancement_reroll_sound(cls):
        """Play the enhancement reroll sound."""
        sound = cls._sounds_cache.get('ui_enhancement_reroll')
        if sound:
            try:
                # Set volume for UI category
                sound.set_volume(cls._ui_volume)
                
                channel = sound.play()
                if channel is None:
                    # Force play enhancement reroll sound as it's important UI feedback
                    cls.force_play_sound(sound, "enhancement reroll sound")
            except Exception as e:
                print(f"[WARNING] Failed to play enhancement reroll sound: {e}")
    
    @classmethod
    def debug_sound_system(cls):
        """Print debug information about the sound system."""
        print(f"[SOUND DEBUG] {cls.get_channel_info()}")
        print(f"[SOUND DEBUG] Cached sounds: {list(cls._sounds_cache.keys())}")
        print(f"[SOUND DEBUG] Initialized: {cls._initialized}")
        print(f"[SOUND DEBUG] SFX Volume: {cls._sfx_volume}")
        print(f"[SOUND DEBUG] Pickable Volume: {cls._pickable_volume}")
        print(f"[SOUND DEBUG] UI Volume: {cls._ui_volume}")
