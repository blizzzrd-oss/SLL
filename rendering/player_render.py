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
from rendering.menu import resource_path

# Sprite sheet cache
_idle_sheet = None
_walk_sheet = None
_run_sheet = None
_hurt_hp_sheet = None
_hurt_barrier_sheet = None
_idle_frames = []
_walk_frames = []
_run_frames = []
_hurt_hp_frames = []
_hurt_barrier_frames = []
_idle_loaded = False
_walk_loaded = False
_run_loaded = False
_hurt_hp_loaded = False
_hurt_barrier_loaded = False


def _load_hurt_hp_frames():
    global _hurt_hp_sheet, _hurt_hp_frames, _hurt_hp_loaded
    if _hurt_hp_loaded:
        return
    _hurt_hp_sheet = pygame.image.load(resource_path(PLAYER_HURT_HP_SPRITE)).convert_alpha()
    sheet_width = _hurt_hp_sheet.get_width()
    num_frames = sheet_width // PLAYER_SPRITE_FRAME_WIDTH
    _hurt_hp_frames = [
        _hurt_hp_sheet.subsurface((i * PLAYER_SPRITE_FRAME_WIDTH, 0, PLAYER_SPRITE_FRAME_WIDTH, PLAYER_SPRITE_FRAME_HEIGHT))
        for i in range(num_frames)
    ]
    _hurt_hp_loaded = True

def _load_hurt_barrier_frames():
    global _hurt_barrier_sheet, _hurt_barrier_frames, _hurt_barrier_loaded
    if _hurt_barrier_loaded:
        return
    _hurt_barrier_sheet = pygame.image.load(resource_path(PLAYER_HURT_BARRIER_SPRITE)).convert_alpha()
    sheet_width = _hurt_barrier_sheet.get_width()
    num_frames = sheet_width // PLAYER_SPRITE_FRAME_WIDTH
    _hurt_barrier_frames = [
        _hurt_barrier_sheet.subsurface((i * PLAYER_SPRITE_FRAME_WIDTH, 0, PLAYER_SPRITE_FRAME_WIDTH, PLAYER_SPRITE_FRAME_HEIGHT))
        for i in range(num_frames)
    ]
    _hurt_barrier_loaded = True

def draw_player_hurt(surface, player, time, barrier_damage=False):
    """Draw the player hurt animation at the player's position. If barrier_damage is True, use barrier hurt sprite."""
    if barrier_damage:
        _load_hurt_barrier_frames()
        frames = _hurt_barrier_frames
    else:
        _load_hurt_hp_frames()
        frames = _hurt_hp_frames
    num_frames = len(frames)
    frame = int((time * PLAYER_HURT_ANIMATION_FPS))
    if frame >= num_frames:
        frame = num_frames - 1  # Clamp to last frame
    img = frames[frame]
    rect = img.get_rect(center=(int(player.x), int(player.y)))
    surface.blit(img, rect)

def _load_idle_frames():
    global _idle_sheet, _idle_frames, _idle_loaded
    if _idle_loaded:
        return
    _idle_sheet = pygame.image.load(resource_path(PLAYER_IDLE_SPRITE)).convert_alpha()
    sheet_width = _idle_sheet.get_width()
    num_frames = sheet_width // PLAYER_SPRITE_FRAME_WIDTH
    _idle_frames = [
        _idle_sheet.subsurface((i * PLAYER_SPRITE_FRAME_WIDTH, 0, PLAYER_SPRITE_FRAME_WIDTH, PLAYER_SPRITE_FRAME_HEIGHT))
        for i in range(num_frames)
    ]
    _idle_loaded = True

def _load_walk_frames():
    global _walk_sheet, _walk_frames, _walk_loaded
    if _walk_loaded:
        return
    _walk_sheet = pygame.image.load(resource_path(PLAYER_WALK_SPRITE)).convert_alpha()
    sheet_width = _walk_sheet.get_width()
    num_frames = sheet_width // PLAYER_SPRITE_FRAME_WIDTH
    _walk_frames = [
        _walk_sheet.subsurface((i * PLAYER_SPRITE_FRAME_WIDTH, 0, PLAYER_SPRITE_FRAME_WIDTH, PLAYER_SPRITE_FRAME_HEIGHT))
        for i in range(num_frames)
    ]
    _walk_loaded = True

def _load_run_frames():
    global _run_sheet, _run_frames, _run_loaded
    if _run_loaded:
        return
    _run_sheet = pygame.image.load(resource_path(PLAYER_RUN_SPRITE)).convert_alpha()
    sheet_width = _run_sheet.get_width()
    num_frames = sheet_width // PLAYER_SPRITE_FRAME_WIDTH
    _run_frames = [
        _run_sheet.subsurface((i * PLAYER_SPRITE_FRAME_WIDTH, 0, PLAYER_SPRITE_FRAME_WIDTH, PLAYER_SPRITE_FRAME_HEIGHT))
        for i in range(num_frames)
    ]
    _run_loaded = True

def draw_player_run(surface, player, time):
    """Draw the player run animation at the player's position."""
    _load_run_frames()
    num_frames = len(_run_frames)
    frame = int((time * PLAYER_RUN_ANIMATION_FPS) % num_frames)
    img = _run_frames[frame]
    rect = img.get_rect(center=(int(player.x), int(player.y)))
    surface.blit(img, rect)

def draw_player_idle(surface, player, time):
    """Draw the player idle animation at the player's position."""
    _load_idle_frames()
    num_frames = len(_idle_frames)
    frame = int((time * PLAYER_IDLE_ANIMATION_FPS) % num_frames)
    img = _idle_frames[frame]
    rect = img.get_rect(center=(int(player.x), int(player.y)))
    surface.blit(img, rect)

def draw_player_walk(surface, player, time):
    """Draw the player walk animation at the player's position."""
    _load_walk_frames()
    num_frames = len(_walk_frames)
    frame = int((time * PLAYER_WALK_ANIMATION_FPS) % num_frames)
    img = _walk_frames[frame]
    rect = img.get_rect(center=(int(player.x), int(player.y)))
    surface.blit(img, rect)
