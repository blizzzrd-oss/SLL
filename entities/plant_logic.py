import pygame
import os


class PlantEnemyLogic:
    """
    Handles movement, animation, and attack logic for Plant enemies.
    """
    SPRITE_PATH = os.path.join('resources', 'images', 'enemies', 'Plant')
    ANIMATIONS = {
        'idle': 'Plant_Idle_full.png',
        'walk': 'Plant_Walk_full.png',
        'run': 'Plant_Run_full.png',
        'hurt': 'Plant_Hurt_full.png',
        'death': 'Plant_Death_full.png',
        'attack': 'Plant_Attack_full.png',
    }
    FRAME_COUNTS = {
        'idle': 6,
        'walk': 8,
        'run': 8,
        'hurt': 4,
        'death': 8,
        'attack': 6,
    }
    # Class-level sprite cache
    _sprite_cache = None

    def __init__(self, enemy):
        self.enemy = enemy
        self.state = 'idle'
        self.anim_frame = 0
        self.anim_timer = 0.0
        if PlantEnemyLogic._sprite_cache is None:
            PlantEnemyLogic._sprite_cache = self._load_sprites()
        self.sprites = PlantEnemyLogic._sprite_cache
        self.attack_cooldown = 1.0
        self.last_attack = -float('inf')

    def _load_sprites(self):
        sprites = {}
        directions = 4  # Down, Up, Left, Right (top to bottom in image)
        for state, fname in self.ANIMATIONS.items():
            path = os.path.join(self.SPRITE_PATH, fname)
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                frame_count = self.FRAME_COUNTS[state]
                w = img.get_width() // frame_count
                h = img.get_height() // directions
                # 2D list: sprites[state][direction][frame]
                sprites[state] = [
                    [img.subsurface((i*w, d*h, w, h)) for i in range(frame_count)]
                    for d in range(directions)
                ]
            else:
                sprites[state] = [[] for _ in range(directions)]
        return sprites

    def update(self, dt, player):
        # Movement towards player
        dx = player.position[0] - self.enemy.position[0]
        dy = player.position[1] - self.enemy.position[1]
        dist = (dx**2 + dy**2) ** 0.5
        speed = self.enemy.type.speed
        # Map movement to sprite row: 0=down, 1=up, 2=left, 3=right
        if abs(dx) > abs(dy):
            if dx > 0:
                direction = 3  # right
            else:
                direction = 2  # left
        else:
            if dy > 0:
                direction = 0  # down
            else:
                direction = 1  # up
        self.direction = direction
        if dist > 1:
            move_x = dx / dist
            move_y = dy / dist
            self.enemy.position = (
                self.enemy.position[0] + move_x * speed * dt,
                self.enemy.position[1] + move_y * speed * dt
            )
            self.enemy.rect.center = (int(self.enemy.position[0]), int(self.enemy.position[1]))
            self.state = 'run' if speed > 4 else 'walk'
        else:
            self.state = 'idle'
        # Attack if close
        if dist < 48:
            now = pygame.time.get_ticks() / 1000
            if now - self.last_attack > self.attack_cooldown:
                self.state = 'attack'
                player.take_damage(5, source=self.enemy)
                self.last_attack = now
        # Animation update
        self.anim_timer += dt
        frames = self.FRAME_COUNTS[self.state]
        if self.anim_timer > 0.1:
            self.anim_frame = (self.anim_frame + 1) % frames
            self.anim_timer = 0.0
        # Death
        if self.enemy.health <= 0:
            self.state = 'death'

    def draw(self, surface):
        # Use direction-aware sprites
        state_sprites = self.sprites.get(self.state, [[] for _ in range(4)])
        direction = getattr(self, 'direction', 0)
        frame_list = state_sprites[direction] if direction < len(state_sprites) else []
        if frame_list:
            frame = frame_list[self.anim_frame % len(frame_list)]
            rect = frame.get_rect(center=self.enemy.rect.center)
            surface.blit(frame, rect)
