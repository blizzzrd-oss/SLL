"""
Enemy sprite preloading system.
Preloads all enemy sprites during the loading screen to avoid lag during gameplay.
"""

import pygame
import os
from entities.demon_logic import DemonEnemyLogic
from entities.plant_logic import PlantEnemyLogic
from config import ENEMY_TYPE_CONFIG


class EnemySpritePreloader:
    """Preloads all enemy sprites to avoid runtime loading delays."""
    
    @staticmethod
    def preload_all_enemy_sprites():
        """Preload sprites for all enemy types."""
        print("[SPRITES] Preloading enemy sprites...")
        success_count = 0
        total_enemies = 0
        
        # Get all enemy types from config
        for enemy_name, enemy_config in ENEMY_TYPE_CONFIG.items():
            total_enemies += 1
            try:
                success = EnemySpritePreloader.preload_enemy_sprites(enemy_name)
                if success:
                    success_count += 1
                    print(f"[SPRITES] ✅ Loaded {enemy_name} sprites")
                else:
                    print(f"[SPRITES] ❌ Failed to load {enemy_name} sprites")
            except Exception as e:
                print(f"[SPRITES] ❌ Error loading {enemy_name} sprites: {e}")
        
        print(f"[SPRITES] Enemy sprite preloading complete: {success_count}/{total_enemies} successful")
        return success_count == total_enemies
    
    @staticmethod
    def preload_enemy_sprites(enemy_name):
        """Preload sprites for a specific enemy type."""
        if enemy_name == 'Demon':
            return EnemySpritePreloader._preload_demon_sprites()
        elif enemy_name == 'Plant':
            return EnemySpritePreloader._preload_plant_sprites()
        else:
            print(f"[SPRITES] Unknown enemy type: {enemy_name}")
            return False
    
    @staticmethod
    def _preload_demon_sprites():
        """Preload demon sprites."""
        try:
            # Force load demon sprites by accessing the class cache
            if DemonEnemyLogic._sprite_cache is None:
                # Create a temporary instance to trigger sprite loading
                from entities.enemy import EnemyType, Enemy
                
                # Create a dummy demon type
                demon_config = ENEMY_TYPE_CONFIG['Demon']
                demon_type = EnemyType('Demon', **demon_config)
                
                # Create a dummy enemy to trigger sprite loading
                dummy_enemy = Enemy(demon_type, (0, 0))
                dummy_logic = DemonEnemyLogic(dummy_enemy)
                
                # Sprites should now be cached in the class
                if DemonEnemyLogic._sprite_cache and isinstance(DemonEnemyLogic._sprite_cache, dict):
                    sprite_states = list(DemonEnemyLogic._sprite_cache.keys())
                    print(f"[SPRITES] Demon sprites cached: {sprite_states}")
                    return True
                else:
                    print(f"[SPRITES] Demon sprite cache is empty or invalid")
                    return False
            else:
                print(f"[SPRITES] Demon sprites already cached")
                return True
                
        except Exception as e:
            print(f"[SPRITES] Failed to preload demon sprites: {e}")
            return False
    
    @staticmethod
    def _preload_plant_sprites():
        """Preload plant sprites."""
        try:
            # Force load plant sprites by accessing the class cache
            if PlantEnemyLogic._sprite_cache is None:
                # Create a temporary instance to trigger sprite loading
                from entities.enemy import EnemyType, Enemy
                
                # Create a dummy plant type
                plant_config = ENEMY_TYPE_CONFIG['Plant']
                plant_type = EnemyType('Plant', **plant_config)
                
                # Create a dummy enemy to trigger sprite loading
                dummy_enemy = Enemy(plant_type, (0, 0))
                dummy_logic = PlantEnemyLogic(dummy_enemy)
                
                # Sprites should now be cached in the class
                if PlantEnemyLogic._sprite_cache and isinstance(PlantEnemyLogic._sprite_cache, dict):
                    sprite_states = list(PlantEnemyLogic._sprite_cache.keys())
                    print(f"[SPRITES] Plant sprites cached: {sprite_states}")
                    return True
                else:
                    print(f"[SPRITES] Plant sprite cache is empty or invalid")
                    return False
            else:
                print(f"[SPRITES] Plant sprites already cached")
                return True
                
        except Exception as e:
            print(f"[SPRITES] Failed to preload plant sprites: {e}")
            return False
    
    @staticmethod
    def get_preload_status():
        """Get the current sprite preload status."""
        demon_loaded = DemonEnemyLogic._sprite_cache is not None
        plant_loaded = PlantEnemyLogic._sprite_cache is not None
        
        return {
            'demon_sprites_loaded': demon_loaded,
            'plant_sprites_loaded': plant_loaded,
            'all_loaded': demon_loaded and plant_loaded
        }
    
    @staticmethod
    def clear_sprite_caches():
        """Clear all sprite caches to free memory."""
        DemonEnemyLogic._sprite_cache = None
        PlantEnemyLogic._sprite_cache = None
        print("[SPRITES] All enemy sprite caches cleared")
