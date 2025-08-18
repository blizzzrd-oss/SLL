"""
Background rendering for tiled world.
"""
import pygame
import math
from config import TILE_SIZE

# Simple visual background patterns
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
    """Create simple visual patterns for background tiles."""
    global _background_patterns, _patterns_loaded
    if _patterns_loaded:
        return
    
    # Create different tile patterns
    tile_size = TILE_SIZE
    
    # Pattern 1: Grass-like (light green with darker spots)
    grass_tile = pygame.Surface((tile_size, tile_size))
    grass_tile.fill((60, 140, 40))  # Base green
    for i in range(8):
        x = (i * 13) % tile_size
        y = (i * 17) % tile_size
        pygame.draw.circle(grass_tile, (45, 120, 30), (x, y), 3)
    _background_patterns.append(grass_tile)
    
    # Pattern 2: Dirt-like (brown with texture)
    dirt_tile = pygame.Surface((tile_size, tile_size))
    dirt_tile.fill((101, 67, 33))  # Base brown
    for i in range(12):
        x = (i * 11) % tile_size
        y = (i * 19) % tile_size
        pygame.draw.circle(dirt_tile, (85, 55, 25), (x, y), 2)
    _background_patterns.append(dirt_tile)
    
    # Pattern 3: Stone-like (gray with darker lines)
    stone_tile = pygame.Surface((tile_size, tile_size))
    stone_tile.fill((120, 120, 120))  # Base gray
    for i in range(0, tile_size, 8):
        pygame.draw.line(stone_tile, (100, 100, 100), (i, 0), (i, tile_size), 1)
        pygame.draw.line(stone_tile, (100, 100, 100), (0, i), (tile_size, i), 1)
    _background_patterns.append(stone_tile)
    
    _patterns_loaded = True

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
