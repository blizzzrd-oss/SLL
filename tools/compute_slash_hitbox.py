import os
import sys
import math

# Try using pygame first
try:
    import pygame
except Exception as e:
    print(f"[ERROR] pygame import failed: {e}")
    sys.exit(1)

# Config values copied from project config
SLASH_SHEET_PATH = os.path.join('resources', 'images', 'player_melee', 'slash', 'player_melee_slash.png')
SLASH_FRAME_COUNT = 5
BASE_SPRITE_SCALE = 1.2  # from slash.py
NARROW_RATIO = 0.7       # width reduction before rotation

# Helper to safely load image
def load_image(path):
    if not os.path.exists(path):
        print(f"[ERROR] File not found: {path}")
        return None
    img = pygame.image.load(path).convert_alpha()
    return img

def main():
    pygame.init()
    # Needed to allow convert_alpha() to work in headless/script mode
    pygame.display.init()
    pygame.display.set_mode((1,1))
    cwd = os.getcwd()
    sheet_path = os.path.join(cwd, SLASH_SHEET_PATH)
    img = load_image(sheet_path)
    if img is None:
        return

    sheet_w, sheet_h = img.get_width(), img.get_height()
    frame_w = sheet_w // SLASH_FRAME_COUNT
    frame_h = sheet_h

    print(f"Sheet size: {sheet_w}x{sheet_h} px")
    print(f"Frame size: {frame_w}x{frame_h} px (frame_w = sheet_w // {SLASH_FRAME_COUNT})")

    narrowed_w = int(frame_w * NARROW_RATIO)
    narrowed_h = frame_h
    print(f"Narrowed base (0° before rotation): {narrowed_w}x{narrowed_h} px (width * {NARROW_RATIO})")

    # Extract first frame as sample
    frame_surf = img.subsurface((0, 0, frame_w, frame_h)).copy()
    # Make the narrowed collision base
    from pygame import transform
    base_rect_frame = transform.smoothscale(frame_surf, (narrowed_w, narrowed_h))

    # Compute sizes for angles
    angles = [0, 45, 90]
    # Compute scales for default and triple strike
    scales = {
        'default (no AOE)': 1.0,
        'triple_strike': 3.0
    }

    for name, sm in scales.items():
        total_scale = BASE_SPRITE_SCALE * sm
        print(f"\nScale set: {name} -> size_multiplier={sm}, total_collision_scale={total_scale}")
        for angle in angles:
            # Rotate first, then scale as in the code
            rotated = transform.rotate(base_rect_frame, -angle)
            rot_w, rot_h = rotated.get_width(), rotated.get_height()
            final_w = int(rot_w * total_scale)
            final_h = int(rot_h * total_scale)
            print(f" angle {angle:>2}°: rotated bbox = {rot_w}x{rot_h} -> final collision = {final_w}x{final_h} px")

    pygame.quit()

if __name__ == '__main__':
    main()
