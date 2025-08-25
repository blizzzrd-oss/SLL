"""
Game logic update system.
Handles all non-rendering game state updates.
"""

import pygame
import time
import random
from entities.spawner import EnemySpawner
from entities.enemy import PlantType, DemonType
from core.wave_system import WaveManager
from config import REROLL_DICE_DROP_CHANCE


class GameLogicManager:
    """Manages all game logic updates and state changes."""
    
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        
        # Initialize wave system
        self.wave_manager = WaveManager(game.mode)
        
        # Initialize enemy management
        self.enemies = []
        self.game.enemies = self.enemies
        self.spawner = EnemySpawner(
            [PlantType, DemonType], 
            get_game_time_fn=lambda: self.game_time,
            screen=screen,
            game=game,
            wave_manager=self.wave_manager  # Pass wave manager to spawner
        )
        self.game_time = 0.0

    def update(self, dt, event_handler):
        """Update all game logic for this frame."""
        # Only update game time if the game is not over and not paused
        if not self.game.game_over and not event_handler.paused:
            self.game_time += dt
        
        if self.game.game_over or event_handler.paused:
            return
        
        # Update wave system
        wave_changed = self.wave_manager.update(dt)
        if wave_changed:
            print(f"[GAME] Wave {self.wave_manager.current_wave} started!")
            # Handle wave events
            self._process_wave_events()
            
        # Update core game systems
        self.game.update(dt)
        
        # Update enemy management
        self._update_enemies(dt)
        
        # Update projectile system
        self.game.projectile_manager.update(dt, self.game.player)
        
        # Update pickable system
        self.game.pickable_manager.update(dt, self.game.player)
        
        # Update player skills with auto-targeting
        self._update_player_skills(dt, event_handler)
        
        # Update player animation timers
        if self.game.player.anim_lock:
            self.game.player.anim_timer += dt
    
    def _process_wave_events(self):
        """Process events triggered by wave progression."""
        pending_events = self.wave_manager.get_pending_events()
        
        for event_data in pending_events:
            # Trigger the event in the game's event system
            if hasattr(self.game, 'event_manager'):
                self.game.event_manager.force_event(event_data['type'])
                print(f"[WAVE] Triggered event: {event_data['type']}")

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
            
            # Check for early XP drop using timer-based approach (0.3 seconds after health reaches 0)
            if (hasattr(enemy, 'logic') and hasattr(enemy.logic, 'state') and 
                enemy.logic.state == 'death' and not enemy.logic.xp_dropped):
                
                # Check if 0.3 seconds have passed since death started
                if enemy.logic.death_timer >= 0.3:
                    # Drop XP pickable early
                    crystal_type = self._determine_xp_crystal_type(enemy)
                    
                    import random
                    offset_x = random.uniform(-10, 10)
                    offset_y = random.uniform(-10, 10)
                    self.game.pickable_manager.create_xp_pickable(
                        enemy.x + offset_x, 
                        enemy.y + offset_y,
                        crystal_type
                    )
                    
                    print(f"[XP] Dropped {crystal_type} XP crystal from {enemy.type.name} (early drop)")
                    
                    # Check for other pickable drops (reroll dice, etc.)
                    if hasattr(enemy.type, 'name') and enemy.type.name in ['Plant', 'Demon']:
                        self._check_pickable_drops(enemy)
                    
                    # Mark as dropped to avoid dropping again
                    enemy.logic.xp_dropped = True
            
            # Handle final enemy removal when death animation completes
            if hasattr(enemy, 'dead') and enemy.dead:
                self.enemies.remove(enemy)
                # Notify wave manager of enemy death
                self.wave_manager.on_enemy_killed()
                self.wave_manager.on_enemy_killed()
                
        self.game.enemies = self.enemies

    def _update_player_skills(self, dt, event_handler):
        """Update player skills with auto-aim and auto-attack."""
        now = pygame.time.get_ticks() / 1000
        
        # Get player settings
        auto_attack, auto_aim = self._get_player_settings()
        
        # Handle pressed skills (for continuous activation like holding space for dash)
        for skill_name in ['slash', 'dash']:
            if (event_handler.is_skill_pressed(skill_name) and 
                skill_name in self.game.player.skills and
                event_handler.can_continuous_activate(skill_name)):
                
                skill = self.game.player.skills[skill_name]
                if skill.can_use(now):
                    target = self._get_skill_target(skill, auto_aim)
                    if target is not None:
                        skill.use(target_pos=target)
                        event_handler.mark_skill_activated(skill_name)
        
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
    
    def get_wave_info(self):
        """Get current wave information for UI display."""
        return self.wave_manager.get_wave_info()
    
    def get_current_wave(self):
        """Get current wave number."""
        return self.wave_manager.current_wave
    
    def force_next_wave(self):
        """Force advance to next wave (for testing/debugging)."""
        self.wave_manager.force_next_wave()
        
    def _check_pickable_drops(self, enemy):
        """Check if enemy should drop pickables."""
        # Check for reroll dice drop
        if random.random() < REROLL_DICE_DROP_CHANCE:
            # Drop at enemy position
            drop_x = enemy.position[0]
            drop_y = enemy.position[1]
            self.game.pickable_manager.create_reroll_dice(drop_x, drop_y)
            print(f"[PICKABLES] Reroll dice dropped at ({drop_x}, {drop_y})")

    def _determine_xp_crystal_type(self, enemy):
        """Determine which type of XP crystal to drop based on enemy type."""
        import random
        from config import (XP_PLANT_GREEN_CHANCE, XP_PLANT_YELLOW_CHANCE,
                           XP_DEMON_GREEN_CHANCE, XP_DEMON_YELLOW_CHANCE, XP_DEMON_LIGHT_BLUE_CHANCE)
        
        # For plants: Use config values
        if hasattr(enemy.type, 'name') and enemy.type.name == 'Plant':
            rand = random.random()
            if rand < XP_PLANT_GREEN_CHANCE:
                return 'green'
            else:
                return 'yellow'
        # For demons: Use config values with 3 crystal types
        elif hasattr(enemy.type, 'name') and enemy.type.name == 'Demon':
            rand = random.random()
            if rand < XP_DEMON_GREEN_CHANCE:
                return 'green'
            elif rand < XP_DEMON_GREEN_CHANCE + XP_DEMON_YELLOW_CHANCE:
                return 'yellow'
            else:
                return 'light_blue'
        
        # For other enemy types (future expansion)
        # For now, default to green
        return 'green'

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
        # Movement skills always target mouse position (converted to world coordinates)
        if getattr(skill, 'is_movement_skill', False):
            mouse_screen = pygame.mouse.get_pos()
            return self.game.camera.screen_to_world(mouse_screen[0], mouse_screen[1])
            
        # Auto-aim targets closest enemy
        if auto_aim:
            closest = self._get_closest_enemy()
            if closest:
                return closest.rect.center
            return None  # No target available
            
        # Default to mouse position (converted to world coordinates)
        mouse_screen = pygame.mouse.get_pos()
        return self.game.camera.screen_to_world(mouse_screen[0], mouse_screen[1])

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
