import math
import tkinter as tk
from PIL import Image, ImageTk
import json
import colorama
from pathlib import Path

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

def load_avatar(i, win_h):
    """Laddar avatar (avatar/avatar[1..10].png) om den finns, utan att sträcka ut den."""
    avatar_path = Path(__file__).parent / "avatar" / f"avatar{i + 1}.png"
    if avatar_path.exists():
        try:
            img = Image.open(avatar_path)
            # Anpassa höjden efter fönstret men behåll proportioner (ingen stretch)
            target_h = win_h - 12
            aspect_ratio = img.width / img.height
            target_w = max(1, int(target_h * aspect_ratio))
            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None
    return None

def finish_spin(people, cards, winnerindex, taken, data_path, data):
    winner_name = people[winnerindex]
    win, frame_w, name_lbl, sub_lbl = cards[winnerindex]

    win.title("! VINNARE !")
    frame_w.configure(bg="#15803d")
    name_lbl.configure(bg="#15803d", fg="#ffffff", text=f"★ {winner_name} ★")
    sub_lbl.configure(bg="#15803d", fg="#bbf7d0", text="BJUDER PÅ FIKA!")
    win.lift()

    print(f"\n{colorama.Fore.GREEN}Fikahjulet landade på {winner_name}!{colorama.Style.RESET_ALL}")
    taken[winnerindex] = True
    data_path.write_text(json.dumps(data, indent="\t", ensure_ascii=False), encoding="utf-8")

def close_button(arrow_frame, root):
    for widget in arrow_frame.winfo_children():
        widget.destroy()
    tk.Button(
        arrow_frame,
        text="Stäng hjul ✕",
        font=("Helvetica", 12, "bold"),
        command=root.destroy
    ).pack(expand=True, fill="both")