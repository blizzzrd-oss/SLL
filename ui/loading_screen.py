"""
Loading screen for map preloading.
"""
import pygame
import time
from rendering.background_render import preload_map_area, preload_map_tiles
from config import WORLD_SIZE, TILE_SIZE
from audio.sound_manager import SoundManager

class LoadingScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.progress = 0
        self.status_text = "Initializing..."
        
    def update_progress(self, progress_percent, tiles_done, total_tiles):
        """Callback function for preload progress updates."""
        self.progress = progress_percent
        self.status_text = f"Loading tiles... {tiles_done:,} / {total_tiles:,}"
    
    def draw(self):
        """Draw the loading screen."""
        # Clear screen with dark background
        self.screen.fill((20, 20, 30))
        
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Title
        title_text = self.font_large.render("Loading World", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Progress bar
        bar_width = 400
        bar_height = 20
        bar_x = (screen_width - bar_width) // 2
        bar_y = screen_height // 2 - 20
        
        # Progress bar background
        pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        
        # Progress bar fill
        fill_width = int((self.progress / 100) * bar_width)
        if fill_width > 0:
            pygame.draw.rect(self.screen, (50, 200, 50), (bar_x, bar_y, fill_width, bar_height))
        
        # Progress bar border
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Progress percentage
        progress_text = self.font_small.render(f"{self.progress:.1f}%", True, (255, 255, 255))
        progress_rect = progress_text.get_rect(center=(screen_width // 2, bar_y + bar_height + 30))
        self.screen.blit(progress_text, progress_rect)
        
        # Status text
        status_surface = self.font_small.render(self.status_text, True, (200, 200, 200))
        status_rect = status_surface.get_rect(center=(screen_width // 2, progress_rect.bottom + 40))
        self.screen.blit(status_surface, status_rect)
        
        pygame.display.flip()
    
    def preload_world_map(self):
        """Preload the entire world map."""
        print("Starting full world preload...")
        success = preload_map_tiles(WORLD_SIZE, TILE_SIZE, self.update_progress)
        
        if success:
            self.progress = 100
            self.status_text = "Loading complete!"
            self.draw()
            time.sleep(0.5)  # Show completion briefly
        
        return success
    
    def preload_area_around_spawn(self, spawn_x=0, spawn_y=0, radius_tiles=200):
        """Preload a large area around spawn point."""
        print(f"Starting area preload around ({spawn_x}, {spawn_y}) with radius {radius_tiles}")
        
        # Convert world coordinates to tile coordinates
        spawn_tile_x = spawn_x // TILE_SIZE
        spawn_tile_y = spawn_y // TILE_SIZE
        
        success = preload_map_area(spawn_tile_x, spawn_tile_y, radius_tiles, self.update_progress)
        
        if success:
            self.progress = 100
            self.status_text = "Loading complete!"
            self.draw()
            time.sleep(0.5)  # Show completion briefly
        
        return success
    
    def run_loading_sequence(self, preload_type="area", **kwargs):
        """Run the loading sequence with visual feedback."""
        clock = pygame.time.Clock()
        
        # Initial draw
        self.draw()
        
        # Start preloading in background (we'll simulate async behavior)
        start_time = time.time()
        
        # First, preload sounds
        self.status_text = "Loading sounds..."
        self.draw()
        sound_success = SoundManager.preload_all_sounds()
        if not sound_success:
            print("[WARNING] Some sounds failed to load")
        
        # Then preload map tiles
        if preload_type == "full":
            success = self.preload_world_map()
        elif preload_type == "area":
            success = self.preload_area_around_spawn(**kwargs)
        else:
            print(f"Unknown preload type: {preload_type}")
            return False
        
        end_time = time.time()
        loading_time = end_time - start_time
        
        print(f"Loading completed in {loading_time:.2f} seconds")
        return success

def show_loading_screen(screen, preload_type="area", **kwargs):
    """Convenience function to show loading screen and preload map."""
    loading_screen = LoadingScreen(screen)
    return loading_screen.run_loading_sequence(preload_type, **kwargs)
