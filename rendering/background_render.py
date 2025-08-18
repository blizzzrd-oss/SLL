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

# Tile cache for performance - stores pre-calculated tile assignments
_tile_cache = {}
_cache_size_limit = 10000  # Limit cache size to prevent memory issues

def simple_noise(x, y, scale=0.1):
    """Simple noise function for natural tile clustering."""
    # Create pseudo-random but smooth noise using multiple octaves
    n1 = math.sin(x * scale) * math.cos(y * scale) 
    n2 = math.sin(x * scale * 2.1) * math.cos(y * scale * 1.7) * 0.5
    n3 = math.sin(x * scale * 4.3) * math.cos(y * scale * 3.9) * 0.25
    return n1 + n2 + n3

def get_cached_tile(tile_x, tile_y):
    """Get a cached tile or generate it if not cached."""
    global _tile_cache
    
    tile_key = (tile_x, tile_y)
    
    # Check if tile is already cached
    if tile_key in _tile_cache:
        return _tile_cache[tile_key]
    
    # Limit cache size to prevent memory issues
    if len(_tile_cache) >= _cache_size_limit:
        # Remove oldest entries (simple LRU approximation)
        keys_to_remove = list(_tile_cache.keys())[:_cache_size_limit // 4]
        for key in keys_to_remove:
            del _tile_cache[key]
    
    # Generate the tile
    biome_type = get_biome_type(tile_x, tile_y)
    
    # Add local variation within the biome, but no grassy tiles in stone areas
    local_hash = abs(hash((tile_x, tile_y))) % 100
    if local_hash < 15:  # 15% chance for variation
        if biome_type == 0:  # Grass areas can have some plant variations
            pattern_idx = 1 if local_hash < 8 else 0
        elif biome_type == 1:  # Yellow plant areas can have grass or red plants
            pattern_idx = 0 if local_hash < 5 else (2 if local_hash < 10 else 1)
        elif biome_type == 2:  # Red plant areas can have grass or yellow plants
            pattern_idx = 0 if local_hash < 5 else (1 if local_hash < 10 else 2)
        elif biome_type == 3:  # Grass-stone transition areas stay as grass-stone
            pattern_idx = 3  # No mixing for transition tiles
        else:  # Stone areas (biome_type == 4) stay pure stone
            pattern_idx = 4  # No grassy tiles in stone areas
    else:
        pattern_idx = biome_type
    
    # Select tile from biome with weighted probability
    biome_tiles = _background_patterns[pattern_idx]
    tile_surface = select_tile_from_biome(biome_tiles, tile_x, tile_y)
    
    # Cache the result
    _tile_cache[tile_key] = tile_surface
    
    return tile_surface

def clear_tile_cache():
    """Clear the tile cache to free memory or reset tiles."""
    global _tile_cache
    _tile_cache.clear()
    print(f"Tile cache cleared")

def get_cache_stats():
    """Get cache statistics for debugging."""
    return {
        'cache_size': len(_tile_cache),
        'cache_limit': _cache_size_limit,
        'memory_usage_tiles': len(_tile_cache)
    }

def get_raw_biome_type(x, y):
    """Get the base biome type without transition logic."""
    # Use noise to create natural biome boundaries
    noise_val = simple_noise(x, y, 0.02)  # Large scale for biomes
    detail_noise = simple_noise(x, y, 0.08) * 0.3  # Smaller scale for variation
    
    combined = noise_val + detail_noise
    
    # Define biome thresholds
    if combined < -0.6:
        return 0  # Grass areas
    elif combined < -0.1:
        return 1  # Grass with yellow plants
    elif combined < 0.4:
        return 2  # Grass with red plants  
    else:
        return 4  # Stone/rocky areas (index 4 now since grass_stone is index 3)

def is_adjacent_to_stone(x, y):
    """Check if a tile position is adjacent to stone biome."""
    # Check the 8 surrounding tiles
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Skip the center tile
            neighbor_biome = get_raw_biome_type(x + dx, y + dy)
            if neighbor_biome == 4:  # Stone biome
                return True
    return False

def get_biome_type(x, y):
    """Determine biome type based on position for natural clustering."""
    raw_biome = get_raw_biome_type(x, y)
    
    # If this tile is not stone but is adjacent to stone, use grass_stone transition
    if raw_biome != 4 and is_adjacent_to_stone(x, y):
        return 3  # grass_stone biome
    
    return raw_biome

def load_background_patterns():
    """Load biome tile patterns from image files specified in config with weighted selection."""
    global _background_patterns, _patterns_loaded
    if _patterns_loaded:
        return
    
    tile_size = TILE_SIZE
    biome_order = ['grass', 'grass_plant_yellow', 'grass_plant_red', 'grass_stone', 'stone']  # Order matches biome indices
    
    for biome_name in biome_order:
        biome_config = BIOME_TILES.get(biome_name)
        biome_tiles = []
        
        if isinstance(biome_config, list):
            # Multiple tiles with weights
            for tile_path, weight in biome_config:
                if os.path.exists(tile_path):
                    try:
                        tile_img = pygame.image.load(tile_path).convert()
                        # Scale to tile size if needed
                        if tile_img.get_size() != (tile_size, tile_size):
                            tile_img = pygame.transform.scale(tile_img, (tile_size, tile_size))
                        biome_tiles.append((tile_img, weight))
                        print(f"Loaded {biome_name} tile from {tile_path} (weight: {weight}%)")
                    except pygame.error as e:
                        print(f"Failed to load {biome_name} tile from {tile_path}: {e}")
                else:
                    print(f"Tile image not found: {tile_path}")
        elif isinstance(biome_config, str):
            # Single tile
            if os.path.exists(biome_config):
                try:
                    tile_img = pygame.image.load(biome_config).convert()
                    if tile_img.get_size() != (tile_size, tile_size):
                        tile_img = pygame.transform.scale(tile_img, (tile_size, tile_size))
                    biome_tiles.append((tile_img, 100))
                    print(f"Loaded {biome_name} tile from {biome_config}")
                except pygame.error as e:
                    print(f"Failed to load {biome_name} tile from {biome_config}: {e}")
            else:
                print(f"Tile image not found: {biome_config}")
        
        # If no tiles loaded successfully, create fallback
        if not biome_tiles:
            print(f"Using fallback tile for {biome_name}")
            fallback_tile = create_fallback_tile(biome_name, tile_size)
            biome_tiles.append((fallback_tile, 100))
        
        _background_patterns.append(biome_tiles)
    
    _patterns_loaded = True

def select_tile_from_biome(biome_tiles, tile_x, tile_y):
    """Select a tile from biome based on weights and position for consistency."""
    if len(biome_tiles) == 1:
        return biome_tiles[0][0]
    
    # Use hash of position to get consistent random value
    hash_val = abs(hash((tile_x, tile_y, 'tile_variant'))) % 100
    
    # Select tile based on cumulative weights
    cumulative = 0
    for tile_img, weight in biome_tiles:
        cumulative += weight
        if hash_val < cumulative:
            return tile_img
    
    # Fallback to first tile
    return biome_tiles[0][0]

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
    elif biome_name == 'grass_plant_yellow':
        # Yellow plant-like pattern
        tile = pygame.Surface((tile_size, tile_size))
        tile.fill(fallback_color)
        for i in range(12):
            x = (i * 11) % tile_size
            y = (i * 19) % tile_size
            darker_color = tuple(max(0, c - 16) for c in fallback_color)
            pygame.draw.circle(tile, darker_color, (x, y), 2)
    elif biome_name == 'grass_plant_red':
        # Red plant-like pattern
        tile = pygame.Surface((tile_size, tile_size))
        tile.fill(fallback_color)
        for i in range(10):
            x = (i * 13) % tile_size
            y = (i * 17) % tile_size
            darker_color = tuple(max(0, c - 20) for c in fallback_color)
            pygame.draw.circle(tile, darker_color, (x, y), 3)
    elif biome_name == 'grass_stone':
        # Grass-stone transition pattern
        tile = pygame.Surface((tile_size, tile_size))
        tile.fill(fallback_color)
        # Mix of grass dots and stone lines
        for i in range(6):
            x = (i * 13) % tile_size
            y = (i * 17) % tile_size
            darker_color = tuple(max(0, c - 15) for c in fallback_color)
            pygame.draw.circle(tile, darker_color, (x, y), 2)
        # Add some stone-like lines
        stone_color = tuple(max(0, c - 25) for c in fallback_color)
        for i in range(0, tile_size, 12):
            pygame.draw.line(tile, stone_color, (i, 0), (i, tile_size), 1)
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
            # Get cached tile (generates and caches if not already cached)
            tile_pattern = get_cached_tile(tile_x, tile_y)
            
            # Convert world position to screen position
            screen_x, screen_y = camera.world_to_screen(world_x, world_y)
            
            # Blit the tile pattern
            surface.blit(tile_pattern, (screen_x, screen_y))
