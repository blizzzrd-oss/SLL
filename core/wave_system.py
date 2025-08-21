"""
Wave-based progression system for enemy spawning and events.
Replaces time-based progression with wave-based progression.
"""

import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from config import (
    WAVE_DURATION, WAVE_SYSTEM_CONFIGURATION, WAVE_EVENT_CHANCES,
    BOSS_WAVE_INTERVAL, ELITE_WAVE_INTERVAL, BOSS_WAVE_HEALTH_BONUS, 
    BOSS_WAVE_DAMAGE_BONUS, ELITE_WAVE_HEALTH_BONUS, ELITE_WAVE_SPEED_BONUS
)


@dataclass
class WaveConfig:
    """Configuration for a single wave."""
    wave_number: int
    duration: float = 30.0  # Default wave duration in seconds
    spawn_rate_multiplier: float = 1.0
    enemy_health_multiplier: float = 1.0
    enemy_damage_multiplier: float = 1.0
    enemy_speed_multiplier: float = 1.0
    
    # Events that can trigger during this wave
    events: List[str] = None
    event_chances: Dict[str, float] = None  # Event name -> chance per wave
    
    # Special wave properties
    is_boss_wave: bool = False
    special_enemies: List[str] = None
    description: str = ""
    
    def __post_init__(self):
        if self.events is None:
            self.events = []
        if self.event_chances is None:
            self.event_chances = {}
        if self.special_enemies is None:
            self.special_enemies = []


class WaveManager:
    """Manages wave progression and wave-based events."""
    
    def __init__(self, game_mode: str):
        self.game_mode = game_mode
        self.current_wave = 1
        self.wave_start_time = 0.0  # Use game time instead of real time
        self.total_game_time = 0.0
        
        # Wave configuration - use centralized config
        self.default_wave_interval = WAVE_DURATION  # Use centralized wave duration
        self.wave_config = WAVE_SYSTEM_CONFIGURATION  # Use comprehensive config
        self.current_wave_config = self._generate_wave_config(1)
        
        # Event tracking
        self.wave_events_triggered = []
        self.pending_events = []
        
        # Statistics
        self.total_waves_completed = 0
        self.enemies_killed_this_wave = 0
        
    def _generate_wave_config(self, wave_number: int) -> WaveConfig:
        """Generate configuration for a specific wave number."""
        # Get multipliers from centralized config
        spawn_scaling = self.wave_config['WAVE_SPAWN_RATE_SCALING']
        enemy_multipliers = self.wave_config['WAVE_ENEMY_MULTIPLIERS']
        
        # Use the highest defined wave as fallback for waves beyond configuration
        max_defined_wave = max(spawn_scaling.keys())
        effective_wave = min(wave_number, max_defined_wave)
        
        # Mode-specific adjustments
        mode_multipliers = self._get_mode_multipliers()
        
        config = WaveConfig(
            wave_number=wave_number,
            duration=self.default_wave_interval,
            spawn_rate_multiplier=spawn_scaling[effective_wave] * mode_multipliers.get('spawn_rate', 1.0),
            enemy_health_multiplier=enemy_multipliers['health'][effective_wave] * mode_multipliers.get('enemy_health', 1.0),
            enemy_damage_multiplier=enemy_multipliers['damage'][effective_wave],
            enemy_speed_multiplier=enemy_multipliers['speed'][effective_wave],
        )
        
        # Add wave-specific events
        self._configure_wave_events(config)
        
        # Special wave types - use config values
        if wave_number % BOSS_WAVE_INTERVAL == 0:  # Boss waves
            config.is_boss_wave = True
            config.description = f"Boss Wave {wave_number}"
            config.spawn_rate_multiplier *= 1.5
            config.enemy_health_multiplier *= BOSS_WAVE_HEALTH_BONUS
            config.enemy_damage_multiplier *= BOSS_WAVE_DAMAGE_BONUS
        elif wave_number % ELITE_WAVE_INTERVAL == 0:  # Elite waves
            config.description = f"Elite Wave {wave_number}"
            config.enemy_health_multiplier *= ELITE_WAVE_HEALTH_BONUS
            config.enemy_speed_multiplier *= ELITE_WAVE_SPEED_BONUS
        else:
            config.description = f"Wave {wave_number}"
            
        return config
    
    def _get_mode_multipliers(self) -> Dict[str, float]:
        """Get mode-specific multipliers."""
        mode_configs = {
            'Easy': {
                'spawn_rate': 0.8,
                'enemy_health': 0.8,
            },
            'Normal': {
                'spawn_rate': 1.0,
                'enemy_health': 1.0,
            },
            'Hard': {
                'spawn_rate': 1.3,
                'enemy_health': 1.2,
            }
        }
        return mode_configs.get(self.game_mode, mode_configs['Normal'])
    
    def _configure_wave_events(self, config: WaveConfig):
        """Configure events that can happen during this wave."""
        # Use centralized wave event configuration
        for event_name, event_config in WAVE_EVENT_CHANCES.items():
            unlock_wave = event_config['unlock_wave']
            base_chance = event_config['base_chance']
            mode_multipliers = event_config['mode_multipliers']
            
            # Check if this event is unlocked for the current wave
            if config.wave_number >= unlock_wave:
                config.events.append(event_name)
                
                # Apply mode-specific multiplier
                mode_multiplier = mode_multipliers.get(self.game_mode, 1.0)
                final_chance = base_chance * mode_multiplier
                config.event_chances[event_name] = final_chance
    
    def update(self, dt: float) -> bool:
        """
        Update wave progression using game time.
        Returns True if a new wave started.
        """
        self.total_game_time += dt
        wave_elapsed = self.total_game_time - self.wave_start_time
        
        # Check if current wave duration has elapsed
        if wave_elapsed >= self.current_wave_config.duration:
            return self._advance_to_next_wave()
        
        return False
    
    def _advance_to_next_wave(self) -> bool:
        """Advance to the next wave."""
        self.total_waves_completed += 1
        self.current_wave += 1
        self.wave_start_time = self.total_game_time  # Use game time
        self.enemies_killed_this_wave = 0
        self.wave_events_triggered = []
        
        # Generate new wave configuration
        self.current_wave_config = self._generate_wave_config(self.current_wave)
        
        # Trigger wave events based on chances
        self._trigger_wave_events()
        
        print(f"[WAVE] {self.current_wave_config.description} started!")
        return True
    
    def _trigger_wave_events(self):
        """Trigger events for the current wave based on chances."""
        import random
        
        for event_name, chance in self.current_wave_config.event_chances.items():
            if random.random() < chance:
                self.pending_events.append({
                    'type': event_name,
                    'wave': self.current_wave,
                    'triggered_at': self.total_game_time  # Use game time
                })
                self.wave_events_triggered.append(event_name)
                print(f"[WAVE] Event '{event_name}' triggered for wave {self.current_wave}")
    
    def get_current_spawn_multiplier(self) -> float:
        """Get the current spawn rate multiplier for this wave."""
        return self.current_wave_config.spawn_rate_multiplier
    
    def get_current_enemy_multipliers(self) -> Dict[str, float]:
        """Get current enemy stat multipliers for this wave."""
        return {
            'health': self.current_wave_config.enemy_health_multiplier,
            'damage': self.current_wave_config.enemy_damage_multiplier,
            'speed': self.current_wave_config.enemy_speed_multiplier,
        }
    
    def get_current_player_multipliers(self) -> Dict[str, float]:
        """Get current player progression multipliers for this wave."""
        player_multipliers = self.wave_config['WAVE_PLAYER_MULTIPLIERS']
        
        # Use the highest defined wave as fallback for waves beyond configuration
        max_defined_wave = max(player_multipliers['cooldown_reduction'].keys())
        effective_wave = min(self.current_wave, max_defined_wave)
        
        return {
            'cooldown_reduction': player_multipliers['cooldown_reduction'][effective_wave],
            'magic_find': player_multipliers['magic_find'][effective_wave],
        }
    
    def get_current_xp_multiplier(self) -> float:
        """Get current XP gain multiplier for this wave."""
        xp_scaling = self.wave_config['WAVE_XP_GAIN_SCALING']
        
        # Use the highest defined wave as fallback for waves beyond configuration
        max_defined_wave = max(xp_scaling.keys())
        effective_wave = min(self.current_wave, max_defined_wave)
        
        return xp_scaling[effective_wave]
    
    def get_wave_progress(self) -> float:
        """Get current wave progress as a percentage (0.0 to 1.0)."""
        wave_elapsed = self.total_game_time - self.wave_start_time
        return min(wave_elapsed / self.current_wave_config.duration, 1.0)
    
    def get_wave_time_remaining(self) -> float:
        """Get time remaining in current wave."""
        wave_elapsed = self.total_game_time - self.wave_start_time
        return max(self.current_wave_config.duration - wave_elapsed, 0.0)
    
    def get_pending_events(self) -> List[Dict[str, Any]]:
        """Get and clear pending events for the event manager."""
        events = self.pending_events.copy()
        self.pending_events.clear()
        return events
    
    def on_enemy_killed(self):
        """Called when an enemy is killed during this wave."""
        self.enemies_killed_this_wave += 1
    
    def get_wave_info(self) -> Dict[str, Any]:
        """Get information about the current wave for UI display."""
        return {
            'number': self.current_wave,
            'description': self.current_wave_config.description,
            'progress': self.get_wave_progress(),
            'time_remaining': self.get_wave_time_remaining(),
            'is_boss_wave': self.current_wave_config.is_boss_wave,
            'enemies_killed': self.enemies_killed_this_wave,
            'active_events': self.wave_events_triggered,
        }
    
    def force_next_wave(self):
        """Force advancement to next wave (for testing/debugging)."""
        self._advance_to_next_wave()
    
    def set_wave_interval(self, interval: float):
        """Set the default wave interval."""
        self.default_wave_interval = interval
        # Update current wave config if needed
        if hasattr(self.current_wave_config, 'duration'):
            self.current_wave_config.duration = interval
