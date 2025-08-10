"""
Game Events System
Handles special events that can occur during gameplay based on game mode.
"""

import pygame
import random
from core.game_modes import GAME_EVENTS, get_game_mode_config

class GameEvent:
    def __init__(self, event_type, config):
        self.type = event_type
        self.name = config['name']
        self.description = config['description']
        self.duration = config['duration']
        self.effect_type = config['effect_type']
        self.effect_value = config['effect_value']
        
        self.time_remaining = self.duration
        self.active = True
        
    def update(self, dt):
        """Update the event timer"""
        if self.active:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.active = False
        return self.active
    
    def get_display_text(self):
        """Get text to display for this event"""
        minutes = int(self.time_remaining // 60)
        seconds = int(self.time_remaining % 60)
        return f"{self.name} - {minutes:02d}:{seconds:02d}"

class GameEventManager:
    def __init__(self, game_mode):
        self.game_mode = game_mode
        self.mode_config = get_game_mode_config(game_mode)
        self.active_events = []
        self.event_check_timer = 0.0
        self.event_check_interval = 60.0  # Check for new events every minute
        
        # Event notification system
        self.recent_notifications = []
        self.notification_duration = 5.0  # Show notifications for 5 seconds
        
    def update(self, dt):
        """Update all active events and check for new ones"""
        # Update existing events
        self.active_events = [event for event in self.active_events if event.update(dt)]
        
        # Update notifications
        self.recent_notifications = [
            (text, time_left - dt) for text, time_left in self.recent_notifications 
            if time_left - dt > 0
        ]
        
        # Check for new events
        self.event_check_timer += dt
        if self.event_check_timer >= self.event_check_interval:
            self.event_check_timer = 0.0
            self._check_for_new_events()
    
    def _check_for_new_events(self):
        """Check if any new events should start"""
        for event_type in ['healing_shrine', 'bonus_loot_event', 'enemy_weakness_event']:
            chance_key = f"{event_type}_chance"
            if chance_key in self.mode_config:
                chance = self.mode_config[chance_key]
                if random.random() < chance:
                    self._start_event(event_type)
        
        # Hard mode specific events
        if self.game_mode == 'Hard':
            if 'boss_swarm_event_chance' in self.mode_config:
                chance = self.mode_config['boss_swarm_event_chance']
                if random.random() < chance:
                    self._start_event('boss_swarm_event')
    
    def _start_event(self, event_type):
        """Start a new event"""
        # Don't start the same event type if one is already active
        if any(event.type == event_type for event in self.active_events):
            return
            
        if event_type in GAME_EVENTS:
            config = GAME_EVENTS[event_type]
            new_event = GameEvent(event_type, config)
            self.active_events.append(new_event)
            
            # Add notification
            notification_text = f"Event Started: {new_event.name}"
            self.recent_notifications.append((notification_text, self.notification_duration))
            print(f"[GAME EVENT] {notification_text} - {new_event.description}")
    
    def get_active_multipliers(self):
        """Get all active multipliers from events"""
        multipliers = {
            'damage_to_enemies': 1.0,
            'loot_drop_rate': 1.0,
            'elite_spawn_rate': 1.0,
        }
        
        for event in self.active_events:
            if event.effect_type == 'damage_multiplier':
                multipliers['damage_to_enemies'] *= event.effect_value
            elif event.effect_type == 'loot_multiplier':
                multipliers['loot_drop_rate'] *= event.effect_value
            elif event.effect_type == 'elite_spawn_rate':
                multipliers['elite_spawn_rate'] *= event.effect_value
        
        return multipliers
    
    def is_healing_shrine_active(self):
        """Check if healing shrine event is active"""
        for event in self.active_events:
            if event.type == 'healing_shrine' and event.active:
                return True, event.effect_value
        return False, 0
    
    def get_active_events_display(self):
        """Get list of active events for UI display"""
        return [{
            'type': event.type,
            'name': event.name,
            'duration': event.duration,
            'elapsed': event.duration - event.time_remaining,
            'remaining': event.time_remaining
        } for event in self.active_events if event.active]
    
    def get_recent_notifications(self):
        """Get recent event notifications for UI display"""
        return [text for text, _ in self.recent_notifications]
    
    def force_event(self, event_type):
        """Force start an event (for testing/debugging)"""
        self._start_event(event_type)
