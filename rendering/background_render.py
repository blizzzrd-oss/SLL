"""
Background rendering for tiled world.
"""
import pygame
import math
import os
from config import TILE_SIZE, BIOME_TILES, BIOME_FALLBACK_COLORS

# Background tile patterns
_background_patterns = []
_patterns_loaded = False

def simple_noise(x, y, scale=0.1):
    """Simple noise function for natural tile clustering."""
    # Create pseudo-random but smooth noise using multiple octaves
    n1 = math.sin(x * scale) * math.cos(y * scale) 
    n2 = math.sin(x * scale * 2.1) * math.cos(y * scale * 1.7) * 0.5
    n3 = math.sin(x * scale * 4.3) * math.cos(y * scale * 3.9) * 0.25
    return n1 + n2 + n3

def get_biome_type(x, y):
    """Determine biome type based on position for natural clustering."""
    # Use noise to create natural biome boundaries
    noise_val = simple_noise(x, y, 0.02)  # Large scale for biomes
    detail_noise = simple_noise(x, y, 0.08) * 0.3  # Smaller scale for variation
    
    combined = noise_val + detail_noise
    
    # Define biome thresholds
    if combined < -0.5:
        return 0  # Grass areas
    elif combined < 0.3:
        return 1  # Dirt/transition areas  
    else:
        return 2  # Stone/rocky areas

def load_background_patterns():
    """Load biome tile patterns from image files specified in config."""
    global _background_patterns, _patterns_loaded
    if _patterns_loaded:
        return
    
    tile_size = TILE_SIZE
    biome_order = ['grass', 'dirt', 'stone']  # Order matches biome indices
    
    for biome_name in biome_order:
        tile_path = BIOME_TILES.get(biome_name)
        
        if tile_path and os.path.exists(tile_path):
            # Load image tile
            try:
                tile_img = pygame.image.load(tile_path).convert()
                # Scale to tile size if needed
                if tile_img.get_size() != (tile_size, tile_size):
                    tile_img = pygame.transform.scale(tile_img, (tile_size, tile_size))
                _background_patterns.append(tile_img)
                print(f"Loaded {biome_name} tile from {tile_path}")
            except pygame.error as e:
                print(f"Failed to load {biome_name} tile from {tile_path}: {e}")
                # Create fallback tile
                fallback_tile = create_fallback_tile(biome_name, tile_size)
                _background_patterns.append(fallback_tile)
        else:
            print(f"Tile image not found for {biome_name}, using fallback")
            # Create fallback tile
            fallback_tile = create_fallback_tile(biome_name, tile_size)
            _background_patterns.append(fallback_tile)
    
    _patterns_loaded = True

def create_fallback_tile(biome_name, tile_size):
    """Create a procedural fallback tile if image is not available."""
    fallback_color = BIOME_FALLBACK_COLORS.get(biome_name, (128, 128, 128))
    
    if biome_name == 'grass':
        # Grass-like pattern
        tile = pygame.Surface((tile_size, tile_size))
        tile.fill(fallback_color)
        for i in range(8):
            x = (i * 13) % tile_size
            y = (i * 17) % tile_size
            darker_color = tuple(max(0, c - 20) for c in fallback_color)
            pygame.draw.circle(tile, darker_color, (x, y), 3)
    elif biome_name == 'dirt':
        # Dirt-like pattern
        tile = pygame.Surface((tile_size, tile_size))
        tile.fill(fallback_color)
        for i in range(12):
            x = (i * 11) % tile_size
            y = (i * 19) % tile_size
            darker_color = tuple(max(0, c - 16) for c in fallback_color)
            pygame.draw.circle(tile, darker_color, (x, y), 2)
    else:  # stone
        # Stone-like pattern
        tile = pygame.Surface((tile_size, tile_size))
        tile.fill(fallback_color)
        darker_color = tuple(max(0, c - 20) for c in fallback_color)
        for i in range(0, tile_size, 8):
            pygame.draw.line(tile, darker_color, (i, 0), (i, tile_size), 1)
            pygame.draw.line(tile, darker_color, (0, i), (tile_size, i), 1)
    
    return tile

def draw_tiled_background(surface, camera, tile_size=None, buffer_tiles=None):
    """Draw a simple visual background that clearly shows world movement."""
    load_background_patterns()
    
    if not _background_patterns:
        return
    
    if tile_size is None:
        tile_size = TILE_SIZE
    
    screen_width = surface.get_width()
    screen_height = surface.get_height()
    
    # Calculate which tiles are visible (with buffer for smooth scrolling)
    buffer = 2
    tiles_x = math.ceil(screen_width / tile_size) + buffer * 2
    tiles_y = math.ceil(screen_height / tile_size) + buffer * 2
    
    # Calculate starting tile indices based on camera position
    start_tile_x = int(camera.x // tile_size) - buffer
    start_tile_y = int(camera.y // tile_size) - buffer
    
    # Draw tiles
    for row in range(tiles_y):
        for col in range(tiles_x):
            # Calculate world tile coordinates
            tile_x = start_tile_x + col
            tile_y = start_tile_y + row
            
            # Calculate world position of this tile
            world_x = tile_x * tile_size
            world_y = tile_y * tile_size
            
            # Use biome-based clustering for more natural tile distribution
            biome_type = get_biome_type(tile_x, tile_y)
            
            # Add some local variation within the biome
            local_hash = abs(hash((tile_x, tile_y))) % 100
            if local_hash < 15:  # 15% chance for variation
                # Occasionally use a different tile type for natural mixing
                if biome_type == 0:  # Grass areas can have some dirt
                    pattern_idx = 1 if local_hash < 8 else 0
                elif biome_type == 1:  # Dirt areas can have grass or stone
                    pattern_idx = 0 if local_hash < 5 else (2 if local_hash < 10 else 1)
                else:  # Stone areas can have some dirt
                    pattern_idx = 1 if local_hash < 8 else 2
            else:
                pattern_idx = biome_type
            
            tile_pattern = _background_patterns[pattern_idx]
            
            # Convert world position to screen position
            screen_x, screen_y = camera.world_to_screen(world_x, world_y)
            
            # Blit the tile pattern
            surface.blit(tile_pattern, (screen_x, screen_y))
