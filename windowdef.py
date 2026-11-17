import math

def lerp(a, b, t): # Linear
    return a + (b - a) * t

def ease_out_cubic(t):
    return 1 - ((1 - t) ** 3)

def get_line_pos(i, screen_w, screen_h, n, win_h):
    lx = int(screen_w * 0.15)
    total_h = min(screen_h - 120, n * (win_h + 10))
    start_y = (screen_h - total_h) // 2
    step_y = total_h / max(1, n - 1) if n > 1 else 0
    ly = int(start_y + i * step_y - (win_h / 2))
    return lx, ly

def get_circle_pos(i, rot=0.0, step_angle=0.0, cx=0, cy=0, radius=0, win_w=0, win_h=0):
    angle = rot + (i * step_angle)
    x = int(cx + radius * math.cos(angle) - (win_w / 2))
    y = int(cy + radius * math.sin(angle) - (win_h / 2))
    return x, y