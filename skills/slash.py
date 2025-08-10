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
        if target_pos:
            dx, dy = target_pos[0] - self.center[0], target_pos[1] - self.center[1]
            angle = math.degrees(math.atan2(dy, dx)) % 360
        else:
            angle = self.user.facing_angle if hasattr(self.user, 'facing_angle') else 0
        self.start_angle = (angle - self.arc_deg / 2) % 360
        self.end_angle = (angle + self.arc_deg / 2) % 360
        print(f"[SLASH DEBUG] Player pos={self.center} facing_angle={angle:.2f} arc=({self.start_angle:.2f} to {self.end_angle:.2f}) arc_deg={self.arc_deg} max_dist=100")
        return True

    def update(self, dt, entities):
        if not self.active:
            return
        self.animation_frame += dt / self.frame_time
        if self.animation_frame >= self.total_frames:
            self.active = False
            return
        # Hit detection
        print('--- ENEMY DEBUG (slash skill) ---')
        for entity in entities:
            print(f"Slash check id={id(entity)} pos={getattr(entity, 'position', None)} rect={getattr(entity, 'rect', None)} health={getattr(entity, 'health', None)}")
            if entity is self.user or entity in self.hit_entities:
                continue
            if self._in_slash_arc(entity):
                print(f"[DEBUG] Slash HIT entity id={id(entity)}")
                entity.take_damage(self.damage)
                self.hit_entities.add(entity)

    def draw(self, surface, last_move=(1,0)):
        if not self.active or not self.frames:
            return
        # Calculate current frame index
        frame_idx = min(int(self.animation_frame), self.total_frames - 1)
        frame = self.frames[frame_idx]
        # Determine direction from last_move
        move_x, move_y = last_move if last_move != (0,0) else (1,0)
        mirror = move_x < 0
        draw_frame = pygame.transform.flip(frame, True, False) if mirror else frame
        # Offset: place slash just next to player in movement direction
        offset_dist = PLAYER_SIZE // 2 + 4
        if hasattr(self.user, 'x') and hasattr(self.user, 'y'):
            px, py = int(self.user.x), int(self.user.y)
        else:
            px, py = self.user.rect.center
        offset_x = px + (offset_dist if move_x >= 0 else -offset_dist)
        offset_y = py
        rect = draw_frame.get_rect(center=(offset_x, offset_y))
        surface.blit(draw_frame, rect)

    def _in_slash_arc(self, entity):
        # Use the current slash sprite's rect as the hitbox
        frame_idx = min(int(self.animation_frame), self.total_frames - 1)
        frame = self.frames[frame_idx]
        move_x, move_y = (1, 0)
        if hasattr(self.user, 'last_move'):
            move_x, move_y = self.user.last_move
        elif hasattr(self.user, 'facing_angle'):
            # Approximate direction from facing_angle
            angle_rad = math.radians(self.user.facing_angle)
            move_x, move_y = math.cos(angle_rad), math.sin(angle_rad)
        offset_dist = PLAYER_SIZE // 2 + 4
        if hasattr(self.user, 'x') and hasattr(self.user, 'y'):
            px, py = int(self.user.x), int(self.user.y)
        else:
            px, py = self.user.rect.center
        offset_x = px + (offset_dist if move_x >= 0 else -offset_dist)
        offset_y = py
        rect = frame.get_rect(center=(offset_x, offset_y))
        hit = rect.colliderect(entity.rect)
        print(f"[SLASH DEBUG] Enemy id={id(entity)} enemy_rect={entity.rect} slash_rect={rect} hit={hit}")
        return hit
