"""
Event handling system for the game.
Separates input handling from the main game loop.
"""

import pygame
from config import HUD_TOGGLE_KEY


class GameEventHandler:
    """Handles all game input events and user interactions."""
    
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.skill_pressed = {'slash': False, 'dash': False}
        
        # State flags
        self.running = True
        self.should_exit = False
        self.paused = False
        self.pause_menu_selected = 0
        self.in_settings_menu = False
        self.settings_menu = None
        self.hud_visible = True
        
        # Pause menu configuration
        self.pause_menu_options = ["Resume", "Settings", "Surrender", "Quit"]
        self.pause_menu_rects = []

    def handle_all_events(self):
        """Process all pygame events for this frame."""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.should_exit = True
                
            elif self.game.game_over:
                self._handle_game_over_events(event)
                
            elif event.type == pygame.KEYDOWN and event.key == HUD_TOGGLE_KEY:
                self.hud_visible = not self.hud_visible
                
            elif not self.in_settings_menu and not self.game.game_over:
                self._handle_gameplay_events(event, mouse_pos)
                
            elif self.in_settings_menu:
                self._handle_settings_menu_events(event)

    def _handle_game_over_events(self, event):
        """Handle events when game is over."""
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
            self.should_exit = True

    def _handle_gameplay_events(self, event, mouse_pos):
        """Handle events during normal gameplay."""
        # Track skill button states
        self._update_skill_button_states(event)
        
        # Manual skill activation for instant response
        self._handle_manual_skill_activation(event, mouse_pos)
        
        # Pause menu events
        self._handle_pause_menu_events(event, mouse_pos)

    def _update_skill_button_states(self, event):
        """Track which skill buttons are currently pressed."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.skill_pressed['slash'] = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.skill_pressed['slash'] = False
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.skill_pressed['dash'] = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.skill_pressed['dash'] = False

    def _handle_manual_skill_activation(self, event, mouse_pos):
        """Handle immediate skill activation on button press."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if 'slash' in self.game.player.skills:
                self.game.player.skills['slash'].use(target_pos=mouse_pos)
                
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if 'dash' in self.game.player.skills:
                self.game.player.skills['dash'].use(target_pos=mouse_pos)

    def _handle_pause_menu_events(self, event, mouse_pos):
        """Handle pause menu navigation and selection."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused = not self.paused
            
        if not self.paused:
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.pause_menu_selected = (self.pause_menu_selected - 1) % len(self.pause_menu_options)
            elif event.key == pygame.K_DOWN:
                self.pause_menu_selected = (self.pause_menu_selected + 1) % len(self.pause_menu_options)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._process_pause_menu_option(self.pause_menu_options[self.pause_menu_selected])
                
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.pause_menu_rects):
                if rect.collidepoint(mouse_pos):
                    self.pause_menu_selected = i
                    
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.pause_menu_rects):
                if rect.collidepoint(mouse_pos):
                    self._process_pause_menu_option(self.pause_menu_options[i])

    def _process_pause_menu_option(self, option):
        """Execute the selected pause menu option."""
        from rendering.menu import Menu
        
        if option == "Resume":
            self.paused = False
        elif option == "Surrender":
            self.running = False
        elif option == "Settings":
            self.in_settings_menu = True
            if self.settings_menu is None:
                self.settings_menu = Menu(self.screen)
                self.settings_menu.state = 'settings'
        elif option == "Quit":
            pygame.quit()
            exit()

    def _handle_settings_menu_events(self, event):
        """Handle events in the settings menu."""
        from rendering.menu import Menu
        
        if self.settings_menu is None:
            self.settings_menu = Menu(self.screen)
            self.settings_menu.state = 'settings'
            
        if self.settings_menu.handle_event(event):
            self.in_settings_menu = False
            self.settings_menu = None

    def show_settings_menu_if_active(self):
        """Draw settings menu if currently active."""
        if not self.in_settings_menu:
            return False
            
        from rendering.menu import Menu
        
        if self.settings_menu is None:
            self.settings_menu = Menu(self.screen)
            self.settings_menu.state = 'settings'
            
        self.settings_menu.draw()
        pygame.display.flip()
        return True

    def is_skill_pressed(self, skill_name):
        """Check if a skill button is currently pressed."""
        return self.skill_pressed.get(skill_name, False)
