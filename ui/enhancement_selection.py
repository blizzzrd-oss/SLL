"""
Enhancement Selection UI
Provides interface for selecting skill enhancements on level up.
"""

import pygame
from audio.sound_manager import SoundManager
from config_enhancements import ENHANCEMENT_UI
from config import (
    ENHANCEMENT_OVERLAY_COLOR, ENHANCEMENT_PANEL_COLOR, ENHANCEMENT_BORDER_COLOR,
    ENHANCEMENT_SKILL_SPECIFIC_BORDER_COLOR, ENHANCEMENT_TEXT_COLOR, 
    ENHANCEMENT_BUTTON_COLOR, ENHANCEMENT_BUTTON_HOVER_COLOR,
    ENHANCEMENT_BASE_REROLL_CHARGES
)


class EnhancementSelectionUI:
    """UI for selecting skill enhancements on level up."""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.choices = []
        self.selected_choice = None
        self.button_rects = []
        self.reroll_button_rect = None
        self.is_active = False
        self.reroll_charges = ENHANCEMENT_BASE_REROLL_CHARGES  # Start with base reroll charges from config
        self.on_reroll_callback = None  # Callback function for reroll
        
    def show_enhancement_selection(self, enhancement_choices, reroll_callback=None):
        """Show the enhancement selection screen."""
        self.choices = enhancement_choices
        self.selected_choice = None
        self.is_active = True
        self.on_reroll_callback = reroll_callback
        self._calculate_button_positions()
    
    def _calculate_button_positions(self):
        """Calculate button positions for enhancement choices."""
        self.button_rects = []
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Increase panel width
        panel_width = ENHANCEMENT_UI['panel_width'] + 200  # Increase width by 200px
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - ENHANCEMENT_UI['panel_height']) // 2
        
        # Calculate button layout
        button_count = len(self.choices)
        total_button_width = (button_count * ENHANCEMENT_UI['button_width'] + 
                             (button_count - 1) * ENHANCEMENT_UI['button_spacing'])
        
        start_x = panel_x + (panel_width - total_button_width) // 2
        button_y = panel_y + 120  # Position buttons below title (removed subtitle)
        
        for i in range(button_count):
            button_x = start_x + i * (ENHANCEMENT_UI['button_width'] + ENHANCEMENT_UI['button_spacing'])
            button_rect = pygame.Rect(
                button_x, button_y,
                ENHANCEMENT_UI['button_width'],
                ENHANCEMENT_UI['button_height']
            )
            self.button_rects.append(button_rect)
        
        # Calculate reroll button position (where instructions used to be)
        reroll_button_width = 200
        reroll_button_height = 40
        reroll_x = (screen_width - reroll_button_width) // 2
        reroll_y = panel_y + ENHANCEMENT_UI['panel_height'] - 60
        self.reroll_button_rect = pygame.Rect(reroll_x, reroll_y, reroll_button_width, reroll_button_height)
    
    def handle_event(self, event):
        """Handle input events for enhancement selection."""
        if not self.is_active:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Check enhancement buttons
                for i, button_rect in enumerate(self.button_rects):
                    if button_rect.collidepoint(mouse_pos):
                        enhancement_id = self.choices[i][0]
                        self.selected_choice = enhancement_id
                        
                        # Play enhancement selection sound
                        try:
                            SoundManager.play_enhancement_select_sound()
                        except Exception as e:
                            print(f"[WARNING] Failed to play enhancement select sound: {e}")
                        
                        self.is_active = False
                        return enhancement_id
                
                # Check reroll button
                if (self.reroll_button_rect and self.reroll_button_rect.collidepoint(mouse_pos) 
                    and self.reroll_charges > 0 and self.on_reroll_callback):
                    self.reroll_charges -= 1
                    
                    # Play reroll sound
                    try:
                        SoundManager.play_enhancement_reroll_sound()
                    except Exception as e:
                        print(f"[WARNING] Failed to play enhancement reroll sound: {e}")
                    
                    new_choices = self.on_reroll_callback()
                    if new_choices:
                        self.choices = new_choices
                        self._calculate_button_positions()
                    return "reroll"
        
        return None
    
    def render(self):
        """Render the enhancement selection UI."""
        if not self.is_active:
            return
            
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Draw semi-transparent overlay (same method as pause menu)
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill(ENHANCEMENT_OVERLAY_COLOR)
        self.screen.blit(overlay, (0, 0))
        
        # Draw main panel (semi-transparent)
        panel_width = ENHANCEMENT_UI['panel_width'] + 200  # Increased width
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - ENHANCEMENT_UI['panel_height']) // 2
        panel_rect = pygame.Rect(
            panel_x, panel_y,
            panel_width,
            ENHANCEMENT_UI['panel_height']
        )
        
        # Create semi-transparent panel surface
        panel_surface = pygame.Surface((panel_width, ENHANCEMENT_UI['panel_height']), pygame.SRCALPHA)
        panel_color_with_alpha = (*ENHANCEMENT_PANEL_COLOR, 200)  # Add alpha channel (200/255 = ~78% opacity)
        panel_surface.fill(panel_color_with_alpha)
        self.screen.blit(panel_surface, (panel_x, panel_y))
        
        pygame.draw.rect(self.screen, ENHANCEMENT_BORDER_COLOR, panel_rect, 3, border_radius=10)
        
        # Draw title
        title_text = self.font_large.render("Choose Enhancement", True, ENHANCEMENT_TEXT_COLOR)
        title_rect = title_text.get_rect(center=(screen_width // 2, panel_y + 40))
        self.screen.blit(title_text, title_rect)
        
        # Draw enhancement buttons
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (enhancement_id, enhancement) in enumerate(self.choices):
            button_rect = self.button_rects[i]
            
            # Check if mouse is hovering
            is_hovering = button_rect.collidepoint(mouse_pos)
            button_color = (ENHANCEMENT_BUTTON_HOVER_COLOR if is_hovering 
                          else ENHANCEMENT_BUTTON_COLOR)
            
            # Choose border color based on enhancement type
            is_skill_specific = enhancement.enhancement_type == 'specific'
            border_color = (ENHANCEMENT_SKILL_SPECIFIC_BORDER_COLOR if is_skill_specific 
                           else ENHANCEMENT_BORDER_COLOR)
            
            # Draw button
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=8)
            pygame.draw.rect(self.screen, border_color, button_rect, 2, border_radius=8)
            
            # Get enhancement display info
            display_info = enhancement.get_display_info()
            
            # Draw enhancement name
            name_text = self.font_medium.render(display_info['name'], True, ENHANCEMENT_TEXT_COLOR)
            name_rect = name_text.get_rect(center=(button_rect.centerx, button_rect.y + 20))
            self.screen.blit(name_text, name_rect)
            
            # Draw enhancement level
            level_text = self.font_small.render(display_info['level_text'], True, ENHANCEMENT_TEXT_COLOR)
            level_rect = level_text.get_rect(center=(button_rect.centerx, button_rect.y + 40))
            self.screen.blit(level_text, level_rect)
            
            # Draw description (wrapped)
            description_lines = self._wrap_text(display_info['description'], ENHANCEMENT_UI['button_width'] - 20)
            for j, line in enumerate(description_lines):
                line_text = self.font_small.render(line, True, ENHANCEMENT_TEXT_COLOR)
                line_rect = line_text.get_rect(center=(button_rect.centerx, button_rect.y + 60 + j * 16))
                self.screen.blit(line_text, line_rect)
        
        # Draw reroll button
        if self.reroll_button_rect:
            is_reroll_hovering = self.reroll_button_rect.collidepoint(mouse_pos)
            reroll_enabled = self.reroll_charges > 0
            
            if reroll_enabled:
                reroll_color = ENHANCEMENT_BUTTON_HOVER_COLOR if is_reroll_hovering else ENHANCEMENT_BUTTON_COLOR
            else:
                reroll_color = (100, 100, 100)  # Gray when disabled
            
            pygame.draw.rect(self.screen, reroll_color, self.reroll_button_rect, border_radius=8)
            pygame.draw.rect(self.screen, ENHANCEMENT_BORDER_COLOR, self.reroll_button_rect, 2, border_radius=8)
            
            reroll_text = f"Reroll ({self.reroll_charges} left)"
            text_color = ENHANCEMENT_TEXT_COLOR if reroll_enabled else (150, 150, 150)
            reroll_label = self.font_medium.render(reroll_text, True, text_color)
            reroll_label_rect = reroll_label.get_rect(center=self.reroll_button_rect.center)
            self.screen.blit(reroll_label, reroll_label_rect)
    
    def _wrap_text(self, text, max_width):
        """Wrap text to fit within max width."""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            text_surface = self.font_small.render(test_line, True, ENHANCEMENT_TEXT_COLOR)
            
            if text_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines[:3]  # Limit to 3 lines
    
    def close(self):
        """Close the enhancement selection UI."""
        self.is_active = False
        self.choices = []
        self.selected_choice = None
    
    def add_reroll_charges(self, amount):
        """Add reroll charges (for events, boss kills, etc.)."""
        self.reroll_charges += amount
        print(f"[ENHANCEMENT] Gained {amount} reroll charge(s). Total: {self.reroll_charges}")
    
    def get_reroll_charges(self):
        """Get current number of reroll charges."""
        return self.reroll_charges
    
    def reset_reroll_charges(self):
        """Reset reroll charges to base amount from config."""
        self.reroll_charges = ENHANCEMENT_BASE_REROLL_CHARGES
