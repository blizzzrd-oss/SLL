"""
Background rendering for tiled world.
"""
import pygame
import os
import random

# Cache for loaded tiles
_grass_tiles = []
_tiles_loaded = False

def load_grass_tiles():
    """Load grass tiles from resources/images/Tiles/grass/"""
    global _grass_tiles, _tiles_loaded
    if _tiles_loaded:
        return
    
    grass_dir = "resources/images/Tiles/grass"
    if os.path.exists(grass_dir):
        for filename in os.listdir(grass_dir):
            if filename.endswith('.png'):
                tile_path = os.path.join(grass_dir, filename)
                tile = pygame.image.load(tile_path).convert_alpha()
                _grass_tiles.append(tile)
    
    if not _grass_tiles:
        # Fallback: create a simple green tile
        fallback_tile = pygame.Surface((64, 64))
        fallback_tile.fill((50, 150, 50))  # Green
        _grass_tiles.append(fallback_tile)
    
    _tiles_loaded = True

def draw_tiled_background(surface, camera_x, camera_y, tile_size=64):
    """Draw a tiled grass background based on camera position."""
    load_grass_tiles()
    
    if not _grass_tiles:
        return
    
    screen_width = surface.get_width()
    screen_height = surface.get_height()
    
    # Calculate which tiles are visible (with extra buffer to ensure full coverage)
    start_tile_x = int(camera_x // tile_size) - 2
    start_tile_y = int(camera_y // tile_size) - 2
    end_tile_x = start_tile_x + (screen_width // tile_size) + 5
    end_tile_y = start_tile_y + (screen_height // tile_size) + 5
    
    # Draw tiles
    for tile_y in range(start_tile_y, end_tile_y):
        for tile_x in range(start_tile_x, end_tile_x):
            # Use tile coordinates to pick a consistent tile
            tile_index = abs(tile_x + tile_y * 1000) % len(_grass_tiles)
            tile = _grass_tiles[tile_index]
            
            # Calculate screen position
            screen_x = tile_x * tile_size - camera_x + screen_width // 2
            screen_y = tile_y * tile_size - camera_y + screen_height // 2
            
            surface.blit(tile, (screen_x, screen_y))
