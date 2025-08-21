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
                sound.play()
            except Exception as e:
                print(f"[WARNING] Failed to play skill sound {skill_name}: {e}")
    
    @classmethod
    def play_random_plant_death_sound(cls):
        """Play a random plant death sound if available."""
        sound = cls.get_random_plant_death_sound()
        if sound:
            try:
                sound.play()
            except Exception as e:
                print(f"[WARNING] Failed to play plant death sound: {e}")
    
    @classmethod
    def play_hit_sound(cls, hit_type):
        """Play a hit sound (enemy or player)."""
        sound = cls._sounds_cache.get(f'hit_{hit_type}')
        if sound:
            try:
                sound.play()
            except Exception as e:
                print(f"[WARNING] Failed to play hit sound {hit_type}: {e}")
        else:
            print(f"[WARNING] Hit sound {hit_type} not found in cache")
