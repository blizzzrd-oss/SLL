"""
Menu UI logic for main menu, savegame selection, and settings.
"""
import pygame
import os
import sys
import json
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
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Menu:
    """
    Handles the main menu, savegame, and settings UI and logic.
    """
    def __init__(self, screen, start_game_callback=None):
        self.screen = screen
        self.state = 'main'  # 'main', 'savegame', 'settings'
        self.selected = 0
        self.font = pygame.font.SysFont(None, FONT_SIZE_LARGE)
        self.small_font = pygame.font.SysFont(None, FONT_SIZE_SMALL)
        self.main_menu_buttons = [
            Button((100, 100, 400, 60), 'New Game / Continue', self.font, COLOR_TEXT, COLOR_HIGHLIGHT),
            Button((100, 180, 400, 60), 'Settings', self.font, COLOR_TEXT, COLOR_HIGHLIGHT),
            Button((100, 260, 400, 60), 'Quit', self.font, COLOR_TEXT, COLOR_HIGHLIGHT),
        ]
        self.savegame_back_button = Button((100, 330, 200, 40), 'Back', self.small_font, COLOR_BACK, COLOR_HIGHLIGHT)
        # Save slots: list of 3 slots, None or string for each slot
        self.save_slots = [None, None, None]
        # Gamemode menu
        self.gamemode_buttons = [
            Button((100, 100, 400, 60), 'Easy', self.font, COLOR_TEXT, COLOR_HIGHLIGHT),
            Button((100, 180, 400, 60), 'Normal', self.font, COLOR_TEXT, COLOR_HIGHLIGHT),
            Button((100, 260, 400, 60), 'Hard', self.font, COLOR_TEXT, COLOR_HIGHLIGHT),
        ]
        self.gamemode_back_button = Button((100, 340, 200, 40), 'Back', self.small_font, COLOR_BACK, COLOR_HIGHLIGHT)
        self.selected_slot = None  # Track which slot was selected
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
        self.checkbox_x = self.slider_x
        self.checkbox_y_start = self.sfx_label_y + 50
        self.checkbox_spacing = 40
        self.checkbox_size = 28
        from config import GAME_FPS_OPTIONS, GAME_DEFAULT_FPS
        self._settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'settings.json')
        self.fps_options = GAME_FPS_OPTIONS
        self.fps = GAME_DEFAULT_FPS
        self.load_settings()
        self.start_game_callback = start_game_callback
        # Ensure music volume matches loaded setting
        try:
            pygame.mixer.music.set_volume(self.music_volume / 100)
        except Exception:
            pass

    def load_settings(self):
        try:
            with open(self._settings_path, 'r') as f:
                data = json.load(f)
            # Always treat as percent int (0-100), round to nearest 5
            mv = data.get('music_volume', MUSIC_VOLUME * 100)
            sv = data.get('sfx_volume', SFX_VOLUME * 100)
            self.music_volume = int(round(float(mv)))
            self.music_volume = min(100, max(0, (self.music_volume // 5) * 5))
            self.sfx_volume = int(round(float(sv)))
            self.sfx_volume = min(100, max(0, (self.sfx_volume // 5) * 5))
            self.fps = int(data.get('fps', self.fps_options[0]))
            self.checkbox_options = [
                {"label": "Auto Aim", "checked": bool(data.get('auto_aim', True))},
                {"label": "Auto Attack", "checked": bool(data.get('auto_attack', True))},
                {"label": "Auto Skills", "checked": bool(data.get('auto_skills', True))},
            ]
        except Exception:
            self.music_volume = int(MUSIC_VOLUME * 100)
            self.sfx_volume = int(SFX_VOLUME * 100)
            self.fps = self.fps_options[0]
            self.checkbox_options = [
                {"label": "Auto Aim", "checked": True},
                {"label": "Auto Attack", "checked": True},
                {"label": "Auto Skills", "checked": True},
            ]

    def save_settings(self):
        data = {
            'music_volume': int(self.music_volume),
            'sfx_volume': int(self.sfx_volume),
            'fps': int(self.fps),
            'auto_aim': self.checkbox_options[0]["checked"],
            'auto_attack': self.checkbox_options[1]["checked"],
            'auto_skills': self.checkbox_options[2]["checked"]
        }
        try:
            with open(self._settings_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            pass

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
        elif self.state == 'gamemode':
            self.draw_gamemode_menu()
        pygame.display.flip()

    def draw_gamemode_menu(self):
        title = self.font.render('Select Game Mode', True, COLOR_TEXT)
        self.screen.blit(title, (100, 40))
        mouse_pos = pygame.mouse.get_pos()
        for button in self.gamemode_buttons:
            button.check_hover(mouse_pos)
            button.draw(self.screen)
        self.gamemode_back_button.check_hover(mouse_pos)
        self.gamemode_back_button.draw(self.screen)

    def draw_main_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(self.main_menu_buttons):
            button.check_hover(mouse_pos)
            button.draw(self.screen)

    def draw_savegame_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        self.slot_rects = []
        for i in range(3):
            slot = self.save_slots[i] or 'Empty Slot'
            y = 100 + i * 70
            rect = pygame.Rect(100, y, 400, 60)
            self.slot_rects.append(rect)
            is_hovered = rect.collidepoint(mouse_pos)
            # Button style: fill, border, highlight on hover/selection
            fill_color = COLOR_HIGHLIGHT if is_hovered or i == self.selected else COLOR_BACK
            border_color = COLOR_TEXT if not is_hovered else COLOR_HIGHLIGHT
            pygame.draw.rect(self.screen, fill_color, rect, border_radius=8)
            pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=8)
            # Draw label centered
            label_color = COLOR_BLACK if is_hovered or i == self.selected else COLOR_TEXT
            label = self.font.render(f'Slot {i+1}: {slot}', True, label_color)
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)
        # Always place back button well below the last slot
        self.savegame_back_button.rect.y = 100 + 3 * 70 + 40
        self.savegame_back_button.check_hover(mouse_pos)
        self.savegame_back_button.draw(self.screen)

    def draw_settings_menu(self):
        # Layout constants
        top_y = 60
        spacing_y = 60
        slider_offset = 40
        # FPS label and buttons
        fps_label = self.small_font.render(f'FPS:', True, COLOR_TEXT)
        fps_label_x = self.slider_label_x
        fps_label_y = top_y
        self.screen.blit(fps_label, (fps_label_x, fps_label_y))
        # Draw FPS options as buttons right next to label
        fps_btn_x = fps_label_x + 60
        fps_btn_y = fps_label_y - 6
        btn_w, btn_h = 70, 36
        self.fps_rects = []
        for i, fps in enumerate(self.fps_options):
            rect = pygame.Rect(fps_btn_x + i*(btn_w+10), fps_btn_y, btn_w, btn_h)
            color = COLOR_HIGHLIGHT if self.fps == fps else COLOR_GRAY
            pygame.draw.rect(self.screen, color, rect, border_radius=6)
            label = self.small_font.render(str(fps), True, COLOR_BLACK if self.fps == fps else COLOR_TEXT)
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)
            self.fps_rects.append(rect)
        # Music/SFX sliders and labels (move down)
        music_label_y = top_y + spacing_y
        sfx_label_y = music_label_y + spacing_y
        music_label = self.small_font.render(f'Music Volume: {int(self.music_volume)}%', True, COLOR_TEXT)
        sfx_label = self.small_font.render(f'SFX Volume: {int(self.sfx_volume)}%', True, COLOR_TEXT)
        self.screen.blit(music_label, (self.slider_label_x, music_label_y))
        self.screen.blit(sfx_label, (self.slider_label_x, sfx_label_y))
        # Draw sliders (simple rectangles, no color)
        pygame.draw.rect(self.screen, COLOR_TEXT, (self.slider_x, music_label_y, int((self.music_volume/100)*self.slider_width), self.slider_height))
        pygame.draw.rect(self.screen, COLOR_TEXT, (self.slider_x, sfx_label_y, int((self.sfx_volume/100)*self.slider_width), self.slider_height))
        # Draw slider backgrounds for clarity
        pygame.draw.rect(self.screen, COLOR_GRAY, (self.slider_x, music_label_y, self.slider_width, self.slider_height), 2)
        pygame.draw.rect(self.screen, COLOR_GRAY, (self.slider_x, sfx_label_y, self.slider_width, self.slider_height), 2)
        # Draw checkboxes (move down)
        checkbox_y_start = sfx_label_y + slider_offset
        for i, opt in enumerate(self.checkbox_options):
            box_y = checkbox_y_start + i * self.checkbox_spacing
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
        """Returns True if the settings menu should exit (e.g. back button or ESC), else False."""
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
                    slot_val = self.save_slots[self.selected]
                    if slot_val is None:
                        self.selected_slot = self.selected
                        self.state = 'gamemode'
                    else:
                        # TODO: Load game logic here
                        pass
                elif event.key == pygame.K_ESCAPE:
                    self.state = 'main'
                    self.selected = 0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Check slot clicks
                for i, rect in enumerate(getattr(self, 'slot_rects', [])):
                    if rect.collidepoint(mouse_pos):
                        slot_val = self.save_slots[i]
                        if slot_val is None:
                            self.selected_slot = i
                            self.state = 'gamemode'
                        else:
                            # TODO: Load game logic here
                            pass
                        return
                if self.savegame_back_button.is_clicked(mouse_pos):
                    self.state = 'main'
                    self.selected = 0
        elif self.state == 'gamemode':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for idx, button in enumerate(self.gamemode_buttons):
                    if button.is_clicked(mouse_pos):
                        # Start new game with selected mode
                        if self.start_game_callback:
                            self.start_game_callback(self.selected_slot, button.text)
                        self.state = 'main'  # Optionally reset menu state
                        return
                if self.gamemode_back_button.is_clicked(mouse_pos):
                    self.state = 'savegame'
                    self.selected = self.selected_slot if self.selected_slot is not None else 0
        elif self.state == 'settings':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % 2
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % 2
                if event.key == pygame.K_LEFT:
                    if self.selected == 0:
                        self.music_volume = max(0, self.music_volume - 5)
                        pygame.mixer.music.set_volume(self.music_volume / 100)
                        self.save_settings()
                    elif self.selected == 1:
                        self.sfx_volume = max(0, self.sfx_volume - 5)
                        self.save_settings()
                elif event.key == pygame.K_RIGHT:
                    if self.selected == 0:
                        self.music_volume = min(100, self.music_volume + 5)
                        pygame.mixer.music.set_volume(self.music_volume / 100)
                        self.save_settings()
                    elif self.selected == 1:
                        self.sfx_volume = min(100, self.sfx_volume + 5)
                        self.save_settings()
                elif event.key == pygame.K_ESCAPE:
                    self.state = 'main'
                    self.selected = 0
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Check if user clicked on the music volume slider
                if self.slider_x <= mouse_pos[0] <= self.slider_x + self.slider_width and self.music_label_y <= mouse_pos[1] <= self.music_label_y + self.slider_height:
                    rel_x = mouse_pos[0] - self.slider_x
                    percent = int(round((rel_x / self.slider_width) * 100 / 5) * 5)
                    self.music_volume = min(100, max(0, percent))
                    self.dragging_music = True
                    pygame.mixer.music.set_volume(self.music_volume / 100)
                    self.save_settings()
                # Check if user clicked on the sfx volume slider
                elif self.slider_x <= mouse_pos[0] <= self.slider_x + self.slider_width and self.sfx_label_y <= mouse_pos[1] <= self.sfx_label_y + self.slider_height:
                    rel_x = mouse_pos[0] - self.slider_x
                    percent = int(round((rel_x / self.slider_width) * 100 / 5) * 5)
                    self.sfx_volume = min(100, max(0, percent))
                    self.dragging_sfx = True
                    self.save_settings()
                # FPS buttons
                elif hasattr(self, 'fps_rects') and any(r.collidepoint(mouse_pos) for r in self.fps_rects):
                    for i, rect in enumerate(self.fps_rects):
                        if rect.collidepoint(mouse_pos):
                            self.fps = self.fps_options[i]
                            self.save_settings()
                            break
                # Checkboxes
                else:
                    for i, opt in enumerate(self.checkbox_options):
                        box_y = self.checkbox_y_start + i * self.checkbox_spacing
                        if (self.checkbox_x <= mouse_pos[0] <= self.checkbox_x + self.checkbox_size and
                            box_y <= mouse_pos[1] <= box_y + self.checkbox_size):
                            opt["checked"] = not opt["checked"]
                            self.save_settings()
                            break
                if self.settings_back_button.is_clicked(mouse_pos):
                    self.state = 'main'
                    self.selected = 0
                    return True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging_music = False
                self.dragging_sfx = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                if self.dragging_music:
                    if self.slider_x <= mouse_pos[0] <= self.slider_x + self.slider_width:
                        rel_x = mouse_pos[0] - self.slider_x
                        percent = int(round((rel_x / self.slider_width) * 100 / 5) * 5)
                        self.music_volume = min(100, max(0, percent))
                        pygame.mixer.music.set_volume(self.music_volume / 100)
                        self.save_settings()
                if self.dragging_sfx:
                    if self.slider_x <= mouse_pos[0] <= self.slider_x + self.slider_width:
                        rel_x = mouse_pos[0] - self.slider_x
                        percent = int(round((rel_x / self.slider_width) * 100 / 5) * 5)
                        self.sfx_volume = min(100, max(0, percent))
                        self.save_settings()
            return False

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
