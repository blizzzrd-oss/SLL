"""
Game logic update system.
Handles all non-rendering game state updates.
"""

import pygame
import time
from entities.spawner import EnemySpawner
from entities.enemy import PlantType


class GameLogicManager:
    """Manages all game logic updates and state changes."""
    
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        
        # Initialize enemy management
        self.enemies = []
        self.game.enemies = self.enemies
        self.spawner = EnemySpawner(
            [PlantType], 
            get_game_time_fn=lambda: self.game_time,
            screen=screen,
            game=game
        )
        self.game_time = 0.0

    def update(self, dt, event_handler):
        """Update all game logic for this frame."""
        self.game_time += dt
        
        if self.game.game_over or event_handler.paused:
            return
            
        # Update core game systems
        self.game.update(dt)
        
        # Update enemy management
        self._update_enemies(dt)
        
        # Update player skills with auto-targeting
        self._update_player_skills(dt, event_handler)
        
        # Update player animation timers
        if self.game.player.anim_lock:
            self.game.player.anim_timer += dt

    def _update_enemies(self, dt):
        """Handle enemy spawning and updates."""
        # Spawn new enemies
        new_enemy = self.spawner.spawn_if_ready()
        if new_enemy:
            self.enemies.append(new_enemy)
            self.game.enemies = self.enemies
            
        # Update existing enemies
        for enemy in self.enemies[:]:
            enemy.update(dt, self.game.player)
            if hasattr(enemy, 'dead') and enemy.dead:
                self.enemies.remove(enemy)
                
        self.game.enemies = self.enemies

    def _update_player_skills(self, dt, event_handler):
        """Update player skills with auto-aim and auto-attack."""
        now = pygame.time.get_ticks() / 1000
        
        # Get player settings
        auto_attack, auto_aim = self._get_player_settings()
        
        # Handle pressed skills
        for skill_name in ['slash', 'dash']:
            if (event_handler.is_skill_pressed(skill_name) and 
                skill_name in self.game.player.skills):
                
                skill = self.game.player.skills[skill_name]
                if skill.can_use(now):
                    target = self._get_skill_target(skill, auto_aim)
                    if target is not None:
                        skill.use(target_pos=target)
        
        # Handle auto-attack
        if auto_attack:
            for name, skill in self.game.player.skills.items():
                if getattr(skill, 'is_movement_skill', False):
                    continue
                if skill.can_use(now):
                    target = self._get_skill_target(skill, auto_aim)
                    if target is not None:
                        skill.use(target_pos=target)
        
        # Update all skills
        for skill in self.game.player.skills.values():
            skill.update(dt, self.enemies)

    def _get_player_settings(self):
        """Extract auto-attack and auto-aim settings from player."""
        auto_attack = False
        auto_aim = False
        
        if hasattr(self.game.player, 'checkbox_options'):
            for opt in self.game.player.checkbox_options:
                if opt.get('label') == 'Auto Attack':
                    auto_attack = opt.get('checked', False)
                elif opt.get('label') == 'Auto Aim':
                    auto_aim = opt.get('checked', False)
                    
        return auto_attack, auto_aim

    def _get_skill_target(self, skill, auto_aim):
        """Determine the target for a skill based on settings."""
        # Movement skills always target mouse position
        if getattr(skill, 'is_movement_skill', False):
            return pygame.mouse.get_pos()
            
        # Auto-aim targets closest enemy
        if auto_aim:
            closest = self._get_closest_enemy()
            if closest:
                return closest.rect.center
            return None  # No target available
            
        # Default to mouse position
        return pygame.mouse.get_pos()

    def _get_closest_enemy(self):
        """Find the closest enemy to the player."""
        if not self.enemies:
            return None
            
        # Get player position
        if hasattr(self.game.player, 'x') and hasattr(self.game.player, 'y'):
            px, py = int(self.game.player.x), int(self.game.player.y)
        else:
            px, py = self.game.player.rect.center
            
        # Find closest enemy by distance
        closest = min(
            self.enemies, 
            key=lambda e: (e.rect.centerx - px) ** 2 + (e.rect.centery - py) ** 2
        )
        return closest
