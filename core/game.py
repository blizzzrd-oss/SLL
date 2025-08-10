"""
Game logic for the roguelike hack and slash.
Handles player, monsters, loot, skills, and inventory.
"""

import pygame
from entities.player import Player
from rendering.player_render import draw_player_idle, draw_player_walk
from core.player_movement import handle_player_movement
from core.game_modes import get_game_mode_config
from core.game_events import GameEventManager

class Game:
    def __init__(self, screen, slot, mode):
        self.screen = screen
        self.slot = slot  # Save slot index
        self.mode = mode  # 'Easy', 'Normal', 'Hard'
        
        # Load game mode configuration
        self.mode_config = get_game_mode_config(mode)
        print(f"[GAME MODE] Starting {self.mode_config['display_name']}")
        print(f"[GAME MODE] {self.mode_config['description']}")
        
        # Initialize game event manager
        self.event_manager = GameEventManager(mode)
        
        # Initialize player with mode-specific stats
        self.player = Player()
        self._apply_mode_modifiers()
        
        self.game_over = False
        # TODO: Initialize monsters, loot, map, etc.

    def _apply_mode_modifiers(self):
        """Apply game mode modifiers to player stats"""
        # Modify player stats based on game mode
        original_health = self.player.max_health
        original_damage = getattr(self.player, 'base_damage', 10)  # Default if not set
        
        # Apply multipliers
        self.player.max_health = int(original_health * self.mode_config['player_health_multiplier'])
        self.player.health = self.player.max_health  # Set current health to new max
        
        # Store base damage if not already stored
        if not hasattr(self.player, 'base_damage'):
            self.player.base_damage = original_damage
        
        # Store mode multipliers for use during gameplay
        self.player.mode_damage_multiplier = self.mode_config['player_damage_multiplier']
        self.player.mode_speed_multiplier = self.mode_config['player_speed_multiplier']
        
        print(f"[GAME MODE] Player health: {original_health} -> {self.player.max_health}")
        print(f"[GAME MODE] Player damage multiplier: {self.player.mode_damage_multiplier}")

    def reset(self):
        """Reset the game state except for settings."""
        self.player = Player()
        self._apply_mode_modifiers()
        self.event_manager = GameEventManager(self.mode)
        self.game_over = False
        # TODO: Reset monsters, loot, map, etc.

    def update(self, dt):
        if not self.game_over:
            # Update event manager
            self.event_manager.update(dt)
            
            # Apply healing shrine effect if active
            is_healing, heal_rate = self.event_manager.is_healing_shrine_active()
            if is_healing and self.player.health < self.player.max_health:
                heal_amount = heal_rate * dt
                self.player.health = min(self.player.max_health, self.player.health + heal_amount)
            
            self.player.update(dt)
            
            # Check for player death
            if self.player.health <= 0:
                self.game_over = True
        # TODO: Update monsters, loot, etc.
    
    def get_effective_damage(self, base_damage):
        """Calculate effective damage with mode and event multipliers"""
        multipliers = self.event_manager.get_active_multipliers()
        mode_multiplier = self.mode_config['player_damage_multiplier']
        event_multiplier = multipliers.get('damage_to_enemies', 1.0)
        
        return base_damage * mode_multiplier * event_multiplier
    
    def get_enemy_spawn_rate_multiplier(self):
        """Get the current enemy spawn rate multiplier"""
        base_multiplier = self.mode_config['enemy_spawn_rate_multiplier']
        multipliers = self.event_manager.get_active_multipliers()
        elite_multiplier = multipliers.get('elite_spawn_rate', 1.0)
        
        return base_multiplier, elite_multiplier
    
    def get_loot_drop_multiplier(self):
        """Get the current loot drop rate multiplier"""
        base_multiplier = self.mode_config['loot_drop_rate_multiplier']
        multipliers = self.event_manager.get_active_multipliers()
        event_multiplier = multipliers.get('loot_drop_rate', 1.0)
        
        return base_multiplier * event_multiplier
    
    def get_mode_theme_color(self):
        """Get the theme color for the current game mode"""
        return self.mode_config.get('theme_color', (255, 255, 255))
    
    def get_active_events_for_display(self):
        """Get active events for UI display"""
        return self.event_manager.get_active_events_display()
    
    def get_event_notifications(self):
        """Get recent event notifications for UI display"""
        return self.event_manager.get_recent_notifications()
