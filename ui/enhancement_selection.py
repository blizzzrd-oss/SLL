"""
Enhancement Selection UI
Provides interface for selecting skill enhancements on level up.
"""

import pygame
from config_enhancements import ENHANCEMENT_UI
from config import (
    ENHANCEMENT_OVERLAY_COLOR, ENHANCEMENT_PANEL_COLOR, ENHANCEMENT_BORDER_COLOR,
    ENHANCEMENT_TEXT_COLOR, ENHANCEMENT_BUTTON_COLOR, ENHANCEMENT_BUTTON_HOVER_COLOR
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
        self.is_active = False
        
    def show_enhancement_selection(self, enhancement_choices):
        """Show the enhancement selection screen."""
        self.choices = enhancement_choices
        self.selected_choice = None
        self.is_active = True
        self._calculate_button_positions()
    
    def _calculate_button_positions(self):
        """Calculate button positions for enhancement choices."""
        self.button_rects = []
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        panel_x = (screen_width - ENHANCEMENT_UI['panel_width']) // 2
        panel_y = (screen_height - ENHANCEMENT_UI['panel_height']) // 2
        
        # Calculate button layout
        button_count = len(self.choices)
        total_button_width = (button_count * ENHANCEMENT_UI['button_width'] + 
                             (button_count - 1) * ENHANCEMENT_UI['button_spacing'])
        
        start_x = panel_x + (ENHANCEMENT_UI['panel_width'] - total_button_width) // 2
        button_y = panel_y + 150  # Position buttons below text
        
        for i in range(button_count):
            button_x = start_x + i * (ENHANCEMENT_UI['button_width'] + ENHANCEMENT_UI['button_spacing'])
            button_rect = pygame.Rect(
                button_x, button_y,
                ENHANCEMENT_UI['button_width'],
                ENHANCEMENT_UI['button_height']
            )
            self.button_rects.append(button_rect)
    
    def handle_event(self, event):
        """Handle input events for enhancement selection."""
        if not self.is_active:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                for i, button_rect in enumerate(self.button_rects):
                    if button_rect.collidepoint(mouse_pos):
                        enhancement_id = self.choices[i][0]
                        self.selected_choice = enhancement_id
                        self.is_active = False
                        return enhancement_id
        
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
        
        # Draw main panel
        panel_x = (screen_width - ENHANCEMENT_UI['panel_width']) // 2
        panel_y = (screen_height - ENHANCEMENT_UI['panel_height']) // 2
        panel_rect = pygame.Rect(
            panel_x, panel_y,
            ENHANCEMENT_UI['panel_width'],
            ENHANCEMENT_UI['panel_height']
        )
        
        pygame.draw.rect(self.screen, ENHANCEMENT_PANEL_COLOR, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, ENHANCEMENT_BORDER_COLOR, panel_rect, 3, border_radius=10)
        
        # Draw title
        title_text = self.font_large.render("Choose Enhancement", True, ENHANCEMENT_TEXT_COLOR)
        title_rect = title_text.get_rect(center=(screen_width // 2, panel_y + 40))
        self.screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.font_medium.render("Select a skill enhancement:", True, ENHANCEMENT_TEXT_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(screen_width // 2, panel_y + 70))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw enhancement buttons
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (enhancement_id, enhancement) in enumerate(self.choices):
            button_rect = self.button_rects[i]
            
            # Check if mouse is hovering
            is_hovering = button_rect.collidepoint(mouse_pos)
            button_color = (ENHANCEMENT_BUTTON_HOVER_COLOR if is_hovering 
                          else ENHANCEMENT_BUTTON_COLOR)
            
            # Draw button
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=8)
            pygame.draw.rect(self.screen, ENHANCEMENT_BORDER_COLOR, button_rect, 2, border_radius=8)
            
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
        
        # Draw instructions
        instruction_text = self.font_small.render("Click on an enhancement to select it", True, ENHANCEMENT_TEXT_COLOR)
        instruction_rect = instruction_text.get_rect(center=(screen_width // 2, panel_y + ENHANCEMENT_UI['panel_height'] - 30))
        self.screen.blit(instruction_text, instruction_rect)
    
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
