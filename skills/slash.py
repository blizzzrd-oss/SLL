from config import PLAYER_SIZE
import pygame
import math
import os
from skills.base import Skill

SLASH_SHEET_PATH = os.path.join('resources', 'images', 'player_melee', 'slash', 'player_melee_slash.png')
SLASH_FRAME_COUNT = 5

class SlashSkill(Skill):
    # Class-level cache for frames
    _cached_frames = None

    def __init__(self, user, cooldown=0.5, damage=10, arc_deg=190, duration=0.25):
        super().__init__(user, cooldown)
        self.damage = damage
        self.arc_deg = arc_deg
        self.duration = duration
        # Use class-level cache for frames
        if SlashSkill._cached_frames is None:
            SlashSkill._cached_frames = self._load_frames()
        self.frames = SlashSkill._cached_frames
        self.total_frames = len(self.frames)
        self.frame_time = duration / max(1, self.total_frames)
        self.active = False
        self.animation_frame = 0
        self.hit_entities = set()
        self.start_angle = None
        self.end_angle = None
        self.center = None

    def _load_frames(self):
        frames = []
        if not os.path.exists(SLASH_SHEET_PATH):
            return frames
        sheet = pygame.image.load(SLASH_SHEET_PATH).convert_alpha()
        sheet_width, sheet_height = sheet.get_width(), sheet.get_height()
        frame_width = sheet_width // SLASH_FRAME_COUNT
        for i in range(SLASH_FRAME_COUNT):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))
            frames.append(frame)
        return frames

    def use(self, target_pos=None):
        now = pygame.time.get_ticks() / 1000
        if not self.can_use(now):
            return False
        self.last_used = now
        self.active = True
        self.animation_frame = 0
        self.hit_entities.clear()
        # Calculate arc center and angles
        self.center = self.user.rect.center
        self.target_pos = target_pos if target_pos else pygame.mouse.get_pos()
        dx, dy = self.target_pos[0] - self.center[0], self.target_pos[1] - self.center[1]
        angle = math.degrees(math.atan2(dy, dx)) % 360
        self.start_angle = (angle - self.arc_deg / 2) % 360
        self.end_angle = (angle + self.arc_deg / 2) % 360
        return True

    def update(self, dt, entities):
        if not self.active:
            return
        self.animation_frame += dt / self.frame_time
        if self.animation_frame >= self.total_frames:
            self.active = False
            return
        # Hit detection
        for entity in entities:
            if entity is self.user or entity in self.hit_entities:
                continue
            if self._in_slash_arc(entity):
                entity.take_damage(self.damage)
                self.hit_entities.add(entity)

    def draw(self, surface, last_move=(1,0)):
        if not self.active or not self.frames:
            return
        # Calculate current frame index
        frame_idx = min(int(self.animation_frame), self.total_frames - 1)
        frame = self.frames[frame_idx]
        # Always face the target_pos direction and rotate the sprite
        if not hasattr(self, 'target_pos') or self.target_pos is None:
            self.target_pos = pygame.mouse.get_pos()
        if hasattr(self.user, 'x') and hasattr(self.user, 'y'):
            px, py = int(self.user.x), int(self.user.y)
        else:
            px, py = self.user.rect.center
        dx, dy = self.target_pos[0] - px, self.target_pos[1] - py
        angle = math.degrees(math.atan2(dy, dx)) % 360
        # Sprite faces right (0°) by default, so rotate by -angle
        draw_frame = pygame.transform.rotate(frame, -angle)
        # Offset: place slash just next to player in target direction
        offset_dist = PLAYER_SIZE // 2 + 4
        norm = math.hypot(dx, dy)
        if norm == 0:
            norm = 1
        dir_x, dir_y = dx / norm, dy / norm
        offset_x = int(px + dir_x * offset_dist)
        offset_y = int(py + dir_y * offset_dist)
        rect = draw_frame.get_rect(center=(offset_x, offset_y))
        surface.blit(draw_frame, rect)
        # Removed yellow hitbox debug visualization

    def _in_slash_arc(self, entity):
        # Use the current slash sprite's rect as the hitbox, placed by target_pos
        frame_idx = min(int(self.animation_frame), self.total_frames - 1)
        frame = self.frames[frame_idx]
        if not hasattr(self, 'target_pos') or self.target_pos is None:
            self.target_pos = pygame.mouse.get_pos()
        if hasattr(self.user, 'x') and hasattr(self.user, 'y'):
            px, py = int(self.user.x), int(self.user.y)
        else:
            px, py = self.user.rect.center
        dx, dy = self.target_pos[0] - px, self.target_pos[1] - py
        offset_dist = PLAYER_SIZE // 2 + 4
        norm = math.hypot(dx, dy)
        if norm == 0:
            norm = 1
        dir_x, dir_y = dx / norm, dy / norm
        offset_x = int(px + dir_x * offset_dist)
        offset_y = int(py + dir_y * offset_dist)
        angle = math.degrees(math.atan2(dy, dx)) % 360
        draw_frame = pygame.transform.rotate(frame, -angle)
        rect = draw_frame.get_rect(center=(offset_x, offset_y))
        hit = rect.colliderect(entity.rect)
        return hit
