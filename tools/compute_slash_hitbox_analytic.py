import math

# Matches values used in skills/slash.py
FRAME_W = 32
FRAME_H = 32
NARROW_RATIO = 0.7
BASE_SPRITE_SCALE = 1.2

def analytic_size(narrow_w, h0, angle_deg, total_scale):
    theta = math.radians(-angle_deg)
    c = math.cos(theta)
    s = math.sin(theta)
    hw = narrow_w / 2.0
    hh = h0 / 2.0
    corners = [( hw,  hh), (-hw,  hh), (-hw, -hh), ( hw, -hh)]
    rx = [c * x - s * y for (x, y) in corners]
    ry = [s * x + c * y for (x, y) in corners]
    rot_w = max(rx) - min(rx)
    rot_h = max(ry) - min(ry)
    final_w = int(rot_w * total_scale)
    final_h = int(rot_h * total_scale)
    return rot_w, rot_h, final_w, final_h


def main():
    frame_w = FRAME_W
    frame_h = FRAME_H
    narrow_w = int(frame_w * NARROW_RATIO)
    h0 = frame_h
    angles = [0, 45, 90]
    scales = {
        'default (size_multiplier=1.0)': 1.0,
        'triple_strike (size_multiplier=3.0)': 3.0
    }
    print(f"Frame: {frame_w}x{frame_h}, narrowed base: {narrow_w}x{h0}\n")
    for name, sm in scales.items():
        total_scale = BASE_SPRITE_SCALE * sm
        print(f"Scale: {name} -> total_collision_scale={total_scale}")
        for angle in angles:
            rot_w, rot_h, final_w, final_h = analytic_size(narrow_w, h0, angle, total_scale)
            print(f" angle {angle:>2}°: rot_w={rot_w:.3f}, rot_h={rot_h:.3f} -> final={final_w}x{final_h} px")
        print()

if __name__ == '__main__':
    main()
