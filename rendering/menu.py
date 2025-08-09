"""
Menu UI logic for main menu, savegame selection, and settings.
"""
import pygame
import os
import sys
from config import (
    MUSIC_VOLUME, SFX_VOLUME, BG_MUSIC_PATH,
    COLOR_BG, COLOR_TEXT, COLOR_HIGHLIGHT, COLOR_SLIDER_MUSIC, COLOR_SLIDER_SFX, COLOR_BACK,
    COLOR_BLACK, COLOR_GRAY,
    FONT_SIZE_LARGE, FONT_SIZE_SMALL, WINDOW_WIDTH, WINDOW_HEIGHT
)

# Helper for resource paths

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Menu:
    """
    Handles the main menu, savegame, and settings UI and logic.
    """
    def __init__(self, screen):
        self.screen = screen
        self.state = 'main'  # 'main', 'savegame', 'settings'
        self.selected = 0
        self.save_slots = [None, None, None]  # Placeholder for savegame slots
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME
        self.font = pygame.font.SysFont(None, FONT_SIZE_LARGE)
        self.small_font = pygame.font.SysFont(None, FONT_SIZE_SMALL)
        self.main_menu_buttons = [
            Button((100, 100, 400, 60), 'New Game / Continue', self.font, COLOR_TEXT, COLOR_HIGHLIGHT),
            Button((100, 180, 400, 60), 'Settings', self.font, COLOR_TEXT, COLOR_HIGHLIGHT),
            Button((100, 260, 400, 60), 'Quit', self.font, COLOR_TEXT, COLOR_HIGHLIGHT),
        ]
        self.savegame_back_button = Button((100, 300, 200, 40), 'Back', self.small_font, COLOR_BACK, COLOR_HIGHLIGHT)
        self.settings_back_button = Button((100, 240, 200, 40), 'Back', self.small_font, COLOR_BACK, COLOR_HIGHLIGHT)
        self.dragging_music = False
        self.dragging_sfx = False
        # Slider positions and sizes
        self.slider_label_x = 100
        self.music_label_y = 110
        self.sfx_label_y = 170
        self.slider_x = 380
        self.slider_width = 200
        self.slider_height = 20
        # Checkbox options
        self.checkbox_options = [
            {"label": "Auto Aim", "checked": True},
            {"label": "Auto Attack", "checked": True},
            {"label": "Auto Skills", "checked": True},
        ]
        self.checkbox_x = self.slider_x
        self.checkbox_y_start = self.sfx_label_y + 50
        self.checkbox_spacing = 40
        self.checkbox_size = 28

    def run(self):
        """Main menu loop. Handles events and drawing until quit."""
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)
            self.draw()
            clock.tick(60)
        pygame.quit()

    def draw(self):
        """Draws the current menu state to the screen."""
        self.screen.fill(COLOR_BG)
        if self.state == 'main':
            self.draw_main_menu()
        elif self.state == 'savegame':
            self.draw_savegame_menu()
        elif self.state == 'settings':
            self.draw_settings_menu()
        pygame.display.flip()

    def draw_main_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(self.main_menu_buttons):
            button.check_hover(mouse_pos)
            button.draw(self.screen)

    def draw_savegame_menu(self):
        for i in range(3):
            slot = self.save_slots[i] or 'Empty Slot'
            color = COLOR_HIGHLIGHT if i == self.selected else COLOR_TEXT
            label = self.font.render(f'Slot {i+1}: {slot}', True, color)
            self.screen.blit(label, (100, 100 + i * 60))
        mouse_pos = pygame.mouse.get_pos()
        self.savegame_back_button.check_hover(mouse_pos)
        self.savegame_back_button.draw(self.screen)

    def draw_settings_menu(self):
        # Render labels with %
        music_label = self.small_font.render(f'Music Volume: {int(self.music_volume*100)}%', True, COLOR_TEXT)
        sfx_label = self.small_font.render(f'SFX Volume: {int(self.sfx_volume*100)}%', True, COLOR_TEXT)
        self.screen.blit(music_label, (self.slider_label_x, self.music_label_y))
        self.screen.blit(sfx_label, (self.slider_label_x, self.sfx_label_y))
        # Draw sliders (simple rectangles, no color)
        pygame.draw.rect(self.screen, COLOR_TEXT, (self.slider_x, self.music_label_y, int(self.music_volume*self.slider_width), self.slider_height))
        pygame.draw.rect(self.screen, COLOR_TEXT, (self.slider_x, self.sfx_label_y, int(self.sfx_volume*self.slider_width), self.slider_height))
        # Draw slider backgrounds for clarity
        pygame.draw.rect(self.screen, COLOR_GRAY, (self.slider_x, self.music_label_y, self.slider_width, self.slider_height), 2)
        pygame.draw.rect(self.screen, COLOR_GRAY, (self.slider_x, self.sfx_label_y, self.slider_width, self.slider_height), 2)
        # Draw checkboxes
        for i, opt in enumerate(self.checkbox_options):
            box_y = self.checkbox_y_start + i * self.checkbox_spacing
            # Draw box
            pygame.draw.rect(self.screen, COLOR_GRAY, (self.checkbox_x, box_y, self.checkbox_size, self.checkbox_size), 2)
            # Fill if checked
            if opt["checked"]:
                pygame.draw.rect(self.screen, COLOR_TEXT, (self.checkbox_x+4, box_y+4, self.checkbox_size-8, self.checkbox_size-8))
            # Draw label
            label = self.small_font.render(opt["label"], True, COLOR_TEXT)
            self.screen.blit(label, (self.checkbox_x + self.checkbox_size + 10, box_y + 2))
        mouse_pos = pygame.mouse.get_pos()
        self.settings_back_button.check_hover(mouse_pos)
        self.settings_back_button.draw(self.screen)

    def handle_event(self, event):
        """Handles user input events for the menu."""
        if self.state == 'main':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if self.main_menu_buttons[0].is_clicked(mouse_pos):
                    self.state = 'savegame'
                    self.selected = 0
                elif self.main_menu_buttons[1].is_clicked(mouse_pos):
                    self.state = 'settings'
                    self.selected = 0
                elif self.main_menu_buttons[2].is_clicked(mouse_pos):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % 3
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % 3
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:
                        self.state = 'savegame'
                        self.selected = 0
                    elif self.selected == 1:
                        self.state = 'settings'
                        self.selected = 0
                    elif self.selected == 2:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif self.state == 'savegame':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % 3
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % 3
                elif event.key == pygame.K_RETURN:
                    # Select save slot (start game or load)
                    pass
                elif event.key == pygame.K_ESCAPE:
                    self.state = 'main'
                    self.selected = 0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if self.savegame_back_button.is_clicked(mouse_pos):
                    self.state = 'main'
                    self.selected = 0
        elif self.state == 'settings':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % 2
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % 2
                elif event.key == pygame.K_LEFT:
                    if self.selected == 0:
                        self.music_volume = max(0, self.music_volume - 0.05)
                        pygame.mixer.music.set_volume(self.music_volume)
                    elif self.selected == 1:
                        self.sfx_volume = max(0, self.sfx_volume - 0.05)
                elif event.key == pygame.K_RIGHT:
                    if self.selected == 0:
                        self.music_volume = min(1, self.music_volume + 0.05)
                        pygame.mixer.music.set_volume(self.music_volume)
                    elif self.selected == 1:
                        self.sfx_volume = min(1, self.sfx_volume + 0.05)
                elif event.key == pygame.K_ESCAPE:
                    self.state = 'main'
                    self.selected = 0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Check if user clicked on the music volume slider
                if self.slider_x <= mouse_pos[0] <= self.slider_x + self.slider_width and self.music_label_y <= mouse_pos[1] <= self.music_label_y + self.slider_height:
                    rel_x = mouse_pos[0] - self.slider_x
                    self.music_volume = min(1, max(0, rel_x / self.slider_width))
                    self.dragging_music = True
                    pygame.mixer.music.set_volume(self.music_volume)
                # Check if user clicked on the sfx volume slider
                elif self.slider_x <= mouse_pos[0] <= self.slider_x + self.slider_width and self.sfx_label_y <= mouse_pos[1] <= self.sfx_label_y + self.slider_height:
                    rel_x = mouse_pos[0] - self.slider_x
                    self.sfx_volume = min(1, max(0, rel_x / self.slider_width))
                    self.dragging_sfx = True
                # Checkboxes
                else:
                    for i, opt in enumerate(self.checkbox_options):
                        box_y = self.checkbox_y_start + i * self.checkbox_spacing
                        if (self.checkbox_x <= mouse_pos[0] <= self.checkbox_x + self.checkbox_size and
                            box_y <= mouse_pos[1] <= box_y + self.checkbox_size):
                            opt["checked"] = not opt["checked"]
                            break
                if self.settings_back_button.is_clicked(mouse_pos):
                    self.state = 'main'
                    self.selected = 0
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging_music = False
                self.dragging_sfx = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                if self.dragging_music:
                    if self.slider_x <= mouse_pos[0] <= self.slider_x + self.slider_width:
                        rel_x = mouse_pos[0] - self.slider_x
                        self.music_volume = min(1, max(0, rel_x / self.slider_width))
                        pygame.mixer.music.set_volume(self.music_volume)
                if self.dragging_sfx:
                    if self.slider_x <= mouse_pos[0] <= self.slider_x + self.slider_width:
                        rel_x = mouse_pos[0] - self.slider_x
                        self.sfx_volume = min(1, max(0, rel_x / self.slider_width))

class Button:
    def __init__(self, rect, text, font, color, highlight_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.highlight_color = highlight_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.highlight_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        label = self.font.render(self.text, True, COLOR_BLACK)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
