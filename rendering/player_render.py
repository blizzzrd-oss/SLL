"""
Player rendering
"""
import pygame
from config import (
    PLAYER_IDLE_SPRITE, PLAYER_WALK_SPRITE, PLAYER_RUN_SPRITE,
    PLAYER_HURT_HP_SPRITE, PLAYER_HURT_BARRIER_SPRITE,
    PLAYER_SPRITE_FRAME_WIDTH, PLAYER_SPRITE_FRAME_HEIGHT,
    PLAYER_IDLE_ANIMATION_FPS, PLAYER_WALK_ANIMATION_FPS, PLAYER_RUN_ANIMATION_FPS,
    PLAYER_HURT_ANIMATION_FPS
)
from utils.resource_path import resource_path

# Sprite sheet cache - now 2D arrays for directional sprites
_idle_sheet = None
_walk_sheet = None
_run_sheet = None
_hurt_hp_sheet = None
_hurt_barrier_sheet = None
_idle_frames = []  # Will be 2D: [direction][frame]
_walk_frames = []  # Will be 2D: [direction][frame]
_run_frames = []   # Will be 2D: [direction][frame]
_hurt_hp_frames = []   # Will be 2D: [direction][frame]
_hurt_barrier_frames = []  # Will be 2D: [direction][frame]
_idle_loaded = False
_walk_loaded = False
_run_loaded = False
_hurt_hp_loaded = False
_hurt_barrier_loaded = False

def _get_direction_from_last_move(last_move):
    """Convert last_move vector to direction index: 0=down, 1=up, 2=left, 3=right"""
    dx, dy = last_move
    if abs(dx) > abs(dy):
        if dx > 0:
            return 3  # right
        else:
            return 2  # left
    else:
        if dy > 0:
            return 0  # down
        else:
            return 1  # up


def _load_hurt_hp_frames():
    global _hurt_hp_sheet, _hurt_hp_frames, _hurt_hp_loaded
    if _hurt_hp_loaded:
        return
    _hurt_hp_sheet = pygame.image.load(resource_path(PLAYER_HURT_HP_SPRITE)).convert_alpha()
    sheet_width = _hurt_hp_sheet.get_width()
    sheet_height = _hurt_hp_sheet.get_height()
    
    # Calculate frames per row and number of rows (directions)
    num_frames = sheet_width // PLAYER_SPRITE_FRAME_WIDTH
    num_directions = sheet_height // PLAYER_SPRITE_FRAME_HEIGHT
    
    # Initialize 2D array: [direction][frame]
    _hurt_hp_frames = []
    for direction in range(num_directions):
        direction_frames = []
        for frame in range(num_frames):
            x = frame * PLAYER_SPRITE_FRAME_WIDTH
            y = direction * PLAYER_SPRITE_FRAME_HEIGHT
            sprite = _hurt_hp_sheet.subsurface((x, y, PLAYER_SPRITE_FRAME_WIDTH, PLAYER_SPRITE_FRAME_HEIGHT))
            direction_frames.append(sprite)
        _hurt_hp_frames.append(direction_frames)
    _hurt_hp_loaded = True

def _load_hurt_barrier_frames():
    global _hurt_barrier_sheet, _hurt_barrier_frames, _hurt_barrier_loaded
    if _hurt_barrier_loaded:
        return
    _hurt_barrier_sheet = pygame.image.load(resource_path(PLAYER_HURT_BARRIER_SPRITE)).convert_alpha()
    sheet_width = _hurt_barrier_sheet.get_width()
    sheet_height = _hurt_barrier_sheet.get_height()
    
    # Calculate frames per row and number of rows (directions)
    num_frames = sheet_width // PLAYER_SPRITE_FRAME_WIDTH
    num_directions = sheet_height // PLAYER_SPRITE_FRAME_HEIGHT
    
    # Initialize 2D array: [direction][frame]
    _hurt_barrier_frames = []
    for direction in range(num_directions):
        direction_frames = []
        for frame in range(num_frames):
            x = frame * PLAYER_SPRITE_FRAME_WIDTH
            y = direction * PLAYER_SPRITE_FRAME_HEIGHT
            sprite = _hurt_barrier_sheet.subsurface((x, y, PLAYER_SPRITE_FRAME_WIDTH, PLAYER_SPRITE_FRAME_HEIGHT))
            direction_frames.append(sprite)
        _hurt_barrier_frames.append(direction_frames)
    _hurt_barrier_loaded = True

def draw_player_hurt(surface, player, time, barrier_damage=False, camera=None):
    """Draw the player hurt animation at the player's position. If barrier_damage is True, use barrier hurt sprite."""
    if barrier_damage:
        _load_hurt_barrier_frames()
        frames = _hurt_barrier_frames
    else:
        _load_hurt_hp_frames()
        frames = _hurt_hp_frames
    
    # Get direction from player's last movement
    direction = _get_direction_from_last_move(getattr(player, 'last_move', (1, 0)))
    
    # Ensure we have frames for this direction
    if not frames or direction >= len(frames) or not frames[direction]:
        return
    
    direction_frames = frames[direction]
    num_frames = len(direction_frames)
    frame = int((time * PLAYER_HURT_ANIMATION_FPS))
    if frame >= num_frames:
        frame = num_frames - 1  # Clamp to last frame
    img = direction_frames[frame]
    
    # Apply camera transformation
    if camera:
        screen_x, screen_y = camera.world_to_screen(player.x, player.y)
    else:
        screen_x, screen_y = int(player.x), int(player.y)
    
    rect = img.get_rect(center=(screen_x, screen_y))
    surface.blit(img, rect)

def _load_idle_frames():
    global _idle_sheet, _idle_frames, _idle_loaded
    if _idle_loaded:
        return
    _idle_sheet = pygame.image.load(resource_path(PLAYER_IDLE_SPRITE)).convert_alpha()
    sheet_width = _idle_sheet.get_width()
    sheet_height = _idle_sheet.get_height()
    
    # Calculate frames per row and number of rows (directions)
    num_frames = sheet_width // PLAYER_SPRITE_FRAME_WIDTH
    num_directions = sheet_height // PLAYER_SPRITE_FRAME_HEIGHT
    
    # Initialize 2D array: [direction][frame]
    _idle_frames = []
    for direction in range(num_directions):
        direction_frames = []
        for frame in range(num_frames):
            x = frame * PLAYER_SPRITE_FRAME_WIDTH
            y = direction * PLAYER_SPRITE_FRAME_HEIGHT
            sprite = _idle_sheet.subsurface((x, y, PLAYER_SPRITE_FRAME_WIDTH, PLAYER_SPRITE_FRAME_HEIGHT))
            direction_frames.append(sprite)
        _idle_frames.append(direction_frames)
    _idle_loaded = True

def _load_walk_frames():
    global _walk_sheet, _walk_frames, _walk_loaded
    if _walk_loaded:
        return
    _walk_sheet = pygame.image.load(resource_path(PLAYER_WALK_SPRITE)).convert_alpha()
    sheet_width = _walk_sheet.get_width()
    sheet_height = _walk_sheet.get_height()
    
    # Calculate frames per row and number of rows (directions)
    num_frames = sheet_width // PLAYER_SPRITE_FRAME_WIDTH
    num_directions = sheet_height // PLAYER_SPRITE_FRAME_HEIGHT
    
    # Initialize 2D array: [direction][frame]
    _walk_frames = []
    for direction in range(num_directions):
        direction_frames = []
        for frame in range(num_frames):
            x = frame * PLAYER_SPRITE_FRAME_WIDTH
            y = direction * PLAYER_SPRITE_FRAME_HEIGHT
            sprite = _walk_sheet.subsurface((x, y, PLAYER_SPRITE_FRAME_WIDTH, PLAYER_SPRITE_FRAME_HEIGHT))
            direction_frames.append(sprite)
        _walk_frames.append(direction_frames)
    _walk_loaded = True

def _load_run_frames():
    global _run_sheet, _run_frames, _run_loaded
    if _run_loaded:
        return
    _run_sheet = pygame.image.load(resource_path(PLAYER_RUN_SPRITE)).convert_alpha()
    sheet_width = _run_sheet.get_width()
    sheet_height = _run_sheet.get_height()
    
    # Calculate frames per row and number of rows (directions)
    num_frames = sheet_width // PLAYER_SPRITE_FRAME_WIDTH
    num_directions = sheet_height // PLAYER_SPRITE_FRAME_HEIGHT
    
    # Initialize 2D array: [direction][frame]
    _run_frames = []
    for direction in range(num_directions):
        direction_frames = []
        for frame in range(num_frames):
            x = frame * PLAYER_SPRITE_FRAME_WIDTH
            y = direction * PLAYER_SPRITE_FRAME_HEIGHT
            sprite = _run_sheet.subsurface((x, y, PLAYER_SPRITE_FRAME_WIDTH, PLAYER_SPRITE_FRAME_HEIGHT))
            direction_frames.append(sprite)
        _run_frames.append(direction_frames)
    _run_loaded = True

def draw_player_run(surface, player, time, camera=None):
    """Draw the player run animation at the player's position."""
    _load_run_frames()
    
    # Get direction from player's last movement
    direction = _get_direction_from_last_move(getattr(player, 'last_move', (1, 0)))
    
    # Ensure we have frames for this direction
    if not _run_frames or direction >= len(_run_frames) or not _run_frames[direction]:
        return
    
    direction_frames = _run_frames[direction]
    num_frames = len(direction_frames)
    frame = int((time * PLAYER_RUN_ANIMATION_FPS) % num_frames)
    img = direction_frames[frame]
    
    # Apply camera transformation
    if camera:
        screen_x, screen_y = camera.world_to_screen(player.x, player.y)
    else:
        screen_x, screen_y = int(player.x), int(player.y)
    
    rect = img.get_rect(center=(screen_x, screen_y))
    surface.blit(img, rect)

def draw_player_idle(surface, player, time, camera=None):
    """Draw the player idle animation at the player's position."""
    _load_idle_frames()
    
    # Get direction from player's last movement
    direction = _get_direction_from_last_move(getattr(player, 'last_move', (1, 0)))
    
    # Ensure we have frames for this direction
    if not _idle_frames or direction >= len(_idle_frames) or not _idle_frames[direction]:
        return
    
    direction_frames = _idle_frames[direction]
    num_frames = len(direction_frames)
    frame = int((time * PLAYER_IDLE_ANIMATION_FPS) % num_frames)
    img = direction_frames[frame]
    
    # Apply camera transformation
    if camera:
        screen_x, screen_y = camera.world_to_screen(player.x, player.y)
    else:
        screen_x, screen_y = int(player.x), int(player.y)
    
    rect = img.get_rect(center=(screen_x, screen_y))
    surface.blit(img, rect)

def draw_player_walk(surface, player, time, camera=None):
    """Draw the player walk animation at the player's position."""
    _load_walk_frames()
    
    # Get direction from player's last movement
    direction = _get_direction_from_last_move(getattr(player, 'last_move', (1, 0)))
    
    # Ensure we have frames for this direction
    if not _walk_frames or direction >= len(_walk_frames) or not _walk_frames[direction]:
        return
    
    direction_frames = _walk_frames[direction]
    num_frames = len(direction_frames)
    frame = int((time * PLAYER_WALK_ANIMATION_FPS) % num_frames)
    img = direction_frames[frame]
    
    # Apply camera transformation
    if camera:
        screen_x, screen_y = camera.world_to_screen(player.x, player.y)
    else:
        screen_x, screen_y = int(player.x), int(player.y)
    
    rect = img.get_rect(center=(screen_x, screen_y))
    surface.blit(img, rect)
