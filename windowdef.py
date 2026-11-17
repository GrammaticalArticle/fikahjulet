import math
import tkinter as tk
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

def get_question_mark_pos(i, win_w, win_h):
    custom_coords = {
        0: (610, 295, 180, 62),    # Fönster #1
        1: (790, 225, 180, 62),    # Fönster #2
        2: (970, 225, 180, 62),    # Fönster #3
        3: (1135, 295, 180, 62),   # Fönster #4
        4: (1135, 365, 180, 62),   # Fönster #5
        5: (1033, 435, 180, 62),   # Fönster #6
        6: (932, 505, 180, 62),    # Fönster #7
        7: (830, 575, 180, 62),    # Fönster #8
        8: (830, 645, 180, 104),   # Fönster #9
        9: (830, 830, 180, 62),    # Fönster #10
    }
    
    if i in custom_coords:
        x, y, w, h = custom_coords[i]
    else:
        x, y, w, h = (200 + (i * 50), 300, 180, 62)
        
    return int(x), int(y), int(w), int(h)

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