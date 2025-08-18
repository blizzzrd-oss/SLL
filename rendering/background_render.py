"""
Background rendering for tiled world.
"""
import pygame
import math
import os
import random
import time
from config import TILE_SIZE, BIOME_TILES, BIOME_FALLBACK_COLORS

# Background tile patterns
_background_patterns = []
_patterns_loaded = False

# Tile cache for performance - stores pre-calculated tile assignments
_tile_cache = {}
_cache_size_limit = 50000  # Increased limit for pre-loading
_preload_complete = False

# Debug counters
_cache_hits = 0
_cache_misses = 0

# World generation seed - changes each game start
_world_seed = None

# Pre-computed lookup tables for faster noise
_sin_table = [math.sin(i * 0.01) for i in range(628)]  # 0 to 2π
_cos_table = [math.cos(i * 0.01) for i in range(628)]

def fast_sin(x):
    """Fast sine using lookup table."""
    return _sin_table[int(abs(x * 100)) % 628]

def fast_cos(x):
    """Fast cosine using lookup table."""
    return _cos_table[int(abs(x * 100)) % 628]

def generate_world_seed():
    """Generate a new random seed for world generation."""
    global _world_seed
    _world_seed = int(time.time() * 1000) % 1000000  # Use current time as seed
    print(f"Generated world seed: {_world_seed}")
    return _world_seed

def set_world_seed(seed):
    """Set a specific seed for world generation."""
    global _world_seed
    _world_seed = seed
    print(f"Set world seed: {_world_seed}")

def get_world_seed():
    """Get the current world seed."""
    return _world_seed

def seeded_hash(x, y, salt=""):
    """Generate a seeded hash based on world seed and coordinates."""
    if _world_seed is None:
        generate_world_seed()
    
    # Combine world seed with coordinates and salt for deterministic randomness
    combined = hash((x, y, salt, _world_seed))
    return abs(combined) % 1000000

def simple_noise(x, y, scale=0.1):
    """Optimized noise function for natural tile clustering with world seed."""
    if _world_seed is None:
        generate_world_seed()
    
    # Add world seed offset to make different worlds
    seed_offset_x = (_world_seed % 1000) * 0.1
    seed_offset_y = ((_world_seed // 1000) % 1000) * 0.1
    
    # Use lookup tables instead of math.sin/cos for speed
    scaled_x = (x + seed_offset_x) * scale
    scaled_y = (y + seed_offset_y) * scale
    n1 = fast_sin(scaled_x) * fast_cos(scaled_y)
    n2 = fast_sin(scaled_x * 2.1) * fast_cos(scaled_y * 1.7) * 0.5
    n3 = fast_sin(scaled_x * 4.3) * fast_cos(scaled_y * 3.9) * 0.25
    return n1 + n2 + n3

def get_cached_tile(tile_x, tile_y):
    """Get a cached tile or generate it if not cached."""
    global _tile_cache, _cache_hits, _cache_misses
    
    tile_key = (tile_x, tile_y)
    
    # Check if tile is already cached
    if tile_key in _tile_cache:
        _cache_hits += 1
        return _tile_cache[tile_key]
    
    _cache_misses += 1
    
    # Only limit cache size if we're not in preload mode and cache is getting large
    if not _preload_complete and len(_tile_cache) >= _cache_size_limit:
        # Remove oldest entries (simple cleanup)
        keys_to_remove = list(_tile_cache.keys())[:2000]  # Remove 2000 at a time
        for key in keys_to_remove:
            del _tile_cache[key]
    
    # Generate the tile with simple biome mixing
    biome_type = get_biome_type(tile_x, tile_y)
    
    # Simple mixing for natural variation
    local_hash = seeded_hash(tile_x, tile_y, "biome_mix") % 100
    pattern_idx = biome_type  # Default to the biome type
    
    if local_hash < 15:  # 15% chance for natural mixing between grass types
        if biome_type == 0:  # Grass areas can have some plant variations
            pattern_idx = 1 if local_hash < 8 else 0
        elif biome_type == 1:  # Yellow plant areas can have grass or red plants
            pattern_idx = 0 if local_hash < 5 else (2 if local_hash < 10 else 1)
        elif biome_type == 2:  # Red plant areas can have grass or yellow plants
            pattern_idx = 0 if local_hash < 5 else (1 if local_hash < 10 else 2)
    
    # Select tile from biome with weighted probability
    biome_tiles = _background_patterns[pattern_idx]
    tile_surface = select_tile_from_biome(biome_tiles, tile_x, tile_y)
    
    # Cache the result
    _tile_cache[tile_key] = tile_surface
    
    return tile_surface

def preload_map_tiles(world_size, tile_size, progress_callback=None):
    """Preload all tiles for a given world size into cache."""
    global _preload_complete
    
    # Ensure patterns are loaded first
    load_background_patterns()
    
    if not _background_patterns:
        print("Failed to load background patterns for preloading")
        return False
    
    # Calculate how many tiles we need for the world
    tiles_per_side = world_size // tile_size
    total_tiles = tiles_per_side * tiles_per_side
    
    print(f"Preloading {total_tiles:,} tiles for {world_size}x{world_size} world...")
    
    tiles_processed = 0
    
    # Generate tiles in chunks to avoid blocking
    chunk_size = 1000  # Process 1000 tiles at a time
    
    for start_y in range(0, tiles_per_side, int(chunk_size**0.5)):
        for start_x in range(0, tiles_per_side, int(chunk_size**0.5)):
            # Process a chunk
            end_x = min(start_x + int(chunk_size**0.5), tiles_per_side)
            end_y = min(start_y + int(chunk_size**0.5), tiles_per_side)
            
            for tile_y in range(start_y, end_y):
                for tile_x in range(start_x, end_x):
                    # Convert to world coordinates (centered around 0,0)
                    world_tile_x = tile_x - tiles_per_side // 2
                    world_tile_y = tile_y - tiles_per_side // 2
                    
                    # Generate and cache the tile
                    get_cached_tile(world_tile_x, world_tile_y)
                    tiles_processed += 1
                    
                    # Call progress callback if provided
                    if progress_callback and tiles_processed % 100 == 0:
                        progress = (tiles_processed / total_tiles) * 100
                        progress_callback(progress, tiles_processed, total_tiles)
    
    _preload_complete = True
    print(f"Preloading complete! Cached {len(_tile_cache):,} tiles")
    return True

def preload_map_area(center_x, center_y, radius_tiles, progress_callback=None):
    """Preload tiles in a circular area around a center point."""
    global _preload_complete
    
    # Ensure patterns are loaded first
    load_background_patterns()
    
    if not _background_patterns:
        print("Failed to load background patterns for preloading")
        return False
    
    # Calculate tiles in circular area
    tiles_to_load = []
    for dy in range(-radius_tiles, radius_tiles + 1):
        for dx in range(-radius_tiles, radius_tiles + 1):
            # Check if tile is within circular radius
            distance = (dx * dx + dy * dy) ** 0.5
            if distance <= radius_tiles:
                tile_x = center_x + dx
                tile_y = center_y + dy
                tiles_to_load.append((tile_x, tile_y))
    
    total_tiles = len(tiles_to_load)
    print(f"Preloading {total_tiles:,} tiles in {radius_tiles} tile radius...")
    
    for i, (tile_x, tile_y) in enumerate(tiles_to_load):
        # Generate and cache the tile
        get_cached_tile(tile_x, tile_y)
        
        # Call progress callback if provided
        if progress_callback and i % 50 == 0:
            progress = (i / total_tiles) * 100
            progress_callback(progress, i, total_tiles)
    
    print(f"Area preloading complete! Cached {total_tiles:,} tiles")
    return True

def get_preload_status():
    """Get the current preload status."""
    return {
        'preload_complete': _preload_complete,
        'tiles_cached': len(_tile_cache),
        'cache_limit': _cache_size_limit
    }

def clear_tile_cache():
    """Clear the tile cache to free memory or reset tiles."""
    global _tile_cache, _preload_complete
    _tile_cache.clear()
    _preload_complete = False
    print(f"Tile cache cleared")

def generate_new_world():
    """Generate a completely new world with new seed."""
    global _tile_cache, _preload_complete
    generate_world_seed()  # Generate new seed
    _tile_cache.clear()  # Clear all cached tiles
    _preload_complete = False
    print(f"New world generated with seed: {_world_seed}")

def get_cache_stats():
    """Get cache statistics for debugging."""
    global _cache_hits, _cache_misses
    total_requests = _cache_hits + _cache_misses
    hit_ratio = (_cache_hits / total_requests * 100) if total_requests > 0 else 0
    
    return {
        'tile_cache_size': len(_tile_cache),
        'tile_cache_limit': _cache_size_limit,
        'preload_complete': _preload_complete,
        'cache_hits': _cache_hits,
        'cache_misses': _cache_misses,
        'cache_hit_ratio': f"{hit_ratio:.1f}%"
    }

def print_cache_stats():
    """Print current cache statistics."""
    stats = get_cache_stats()
    print(f"Cache Stats: {stats['tile_cache_size']:,} tiles cached, "
          f"Hit ratio: {stats['cache_hit_ratio']}, "
          f"Preload: {'✓' if stats['preload_complete'] else '✗'}")

def is_tile_cached(tile_x, tile_y):
    """Check if a specific tile is already cached."""
    tile_key = (tile_x, tile_y)
    return tile_key in _tile_cache

def get_biome_type(x, y):
    """Determine biome type based on position for natural clustering."""
    # Use noise to create natural biome boundaries
    noise_val = simple_noise(x, y, 0.02)  # Large scale for biomes
    detail_noise = simple_noise(x, y, 0.08) * 0.3  # Smaller scale for variation
    
    combined = noise_val + detail_noise
    
    # Define biome thresholds for 3 biomes
    if combined < -0.3:
        return 0  # Grass areas
    elif combined < 0.3:
        return 1  # Grass with yellow plants
    else:
        return 2  # Grass with red plants

def load_background_patterns():
    """Load biome tile patterns from image files specified in config with weighted selection."""
    global _background_patterns, _patterns_loaded
    if _patterns_loaded:
        return
    
    tile_size = TILE_SIZE
    biome_order = ['grass', 'grass_plant_yellow', 'grass_plant_red']  # Only 3 biomes now
    
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
    
    # Use seeded hash for consistent but varied results
    hash_val = seeded_hash(tile_x, tile_y, 'tile_variant') % 100
    
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
    else:
        # Default pattern
        tile = pygame.Surface((tile_size, tile_size))
        tile.fill(fallback_color)
    
    return tile

def draw_tiled_background(surface, camera, tile_size=None, buffer_tiles=None):
    """Draw optimized background using cached tiles."""
    load_background_patterns()
    
    if not _background_patterns:
        return
    
    if tile_size is None:
        tile_size = TILE_SIZE
    
    screen_width = surface.get_width()
    screen_height = surface.get_height()
    
    # Calculate which tiles are visible (with buffer for smooth scrolling)
    buffer = 1  # Reduced buffer
    tiles_x = math.ceil(screen_width / tile_size) + buffer * 2
    tiles_y = math.ceil(screen_height / tile_size) + buffer * 2
    
    # Calculate starting tile indices based on camera position
    start_tile_x = int(camera.x // tile_size) - buffer
    start_tile_y = int(camera.y // tile_size) - buffer
    
    # Pre-calculate camera offset for faster rendering
    camera_offset_x = camera.x % tile_size
    camera_offset_y = camera.y % tile_size
    
    # Optimized rendering loop
    for row in range(tiles_y):
        screen_y = row * tile_size - camera_offset_y
        tile_y = start_tile_y + row
        
        for col in range(tiles_x):
            screen_x = col * tile_size - camera_offset_x
            tile_x = start_tile_x + col
            
            # Get cached tile (should be instant if preloaded)
            tile_pattern = get_cached_tile(tile_x, tile_y)
            
            # Direct blit without coordinate transformation
            surface.blit(tile_pattern, (screen_x, screen_y))
