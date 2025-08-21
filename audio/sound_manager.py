"""
Sound manager for preloading and caching all game sounds.
"""
import pygame
import os
import random
from utils.resource_path import resource_path
from config import (
    SKILL_DASH_SOUND_PATH, SKILL_SLASH_SOUND_PATHS,
    ENEMY_PLANT_DEATH_SOUND_PATHS, SFX_VOLUME,
    HIT_ENEMY_SOUND_PATH, HIT_PLAYER_SOUND_PATH
)


class SoundManager:
    """Centralized sound management with preloading."""
    
    _instance = None
    _sounds_cache = {}
    _initialized = False
    _slash_sound_index = 0  # For rotating slash sounds
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
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
                    sound.set_volume(SFX_VOLUME)
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
                    sound.set_volume(SFX_VOLUME)
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
                    sound.set_volume(SFX_VOLUME)
                    plant_death_sounds.append(sound)
                    success_count += 1
                    print(f"[SOUND] Loaded plant death sound {i+1}")
                else:
                    print(f"[WARNING] Plant death sound file not found: {full_path}")
            except Exception as e:
                print(f"[WARNING] Failed to load plant death sound {i+1}: {e}")
        
        if plant_death_sounds:
            cls._sounds_cache['plant_death_sounds'] = plant_death_sounds
        
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
                    sound.set_volume(SFX_VOLUME)
                    cls._sounds_cache[f'hit_{hit_type}'] = sound
                    success_count += 1
                    print(f"[SOUND] Loaded hit sound: {hit_type}")
                else:
                    print(f"[WARNING] Hit sound file not found: {full_path}")
            except Exception as e:
                print(f"[WARNING] Failed to load hit sound {hit_type}: {e}")
        
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
            # Death sounds are important for player feedback, so force-play them
            cls.force_play_sound(sound, "plant death sound")
    
    @classmethod
    def play_hit_sound(cls, hit_type):
        """Play a hit sound (enemy or player)."""
        sound = cls._sounds_cache.get(f'hit_{hit_type}')
        if sound:
            try:
                # Hit sounds should play reliably for feedback
                channel = sound.play()
                if channel is None:
                    # Try to find a free channel
                    for i in range(pygame.mixer.get_num_channels()):
                        channel_obj = pygame.mixer.Channel(i)
                        if not channel_obj.get_busy():
                            channel = channel_obj.play(sound)
                            break
                    if channel is None:
                        print(f"[WARNING] Could not play hit sound {hit_type}: All channels busy")
            except Exception as e:
                print(f"[WARNING] Failed to play hit sound {hit_type}: {e}")
        else:
            print(f"[WARNING] Hit sound {hit_type} not found in cache")
    
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
                
            # If no channels available, stop the oldest non-priority sounds
            # We'll use a simple approach: stop channels that have been playing longest
            oldest_channel = None
            oldest_time = 0
            
            for i in range(pygame.mixer.get_num_channels()):
                channel_obj = pygame.mixer.Channel(i)
                if channel_obj.get_busy():
                    # For simplicity, we'll just stop the first busy channel we find
                    # In a more complex system, we'd track sound priorities and ages
                    channel_obj.stop()
                    channel = channel_obj.play(sound)
                    if channel is not None:
                        print(f"[SOUND] Force-played {sound_type} by stopping another sound")
                        return True
                    break
                    
            print(f"[WARNING] Could not force-play {sound_type}: Unable to free channels")
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
    def debug_sound_system(cls):
        """Print debug information about the sound system."""
        print(f"[SOUND DEBUG] {cls.get_channel_info()}")
        print(f"[SOUND DEBUG] Cached sounds: {list(cls._sounds_cache.keys())}")
        print(f"[SOUND DEBUG] Initialized: {cls._initialized}")
