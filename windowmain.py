# spoiler: jag har kollat upp en massa kod för att jag
#          inte har en aning hur fönster i tkinter funkar
import sys
import json
import math
import tkinter as tk
from pathlib import Path
from random import choice, uniform
import colorama
from common import clear, format_json
from windowdef import *

colorama.init()

# Läsa json, skapa variabler
data_path = Path(__file__).with_name("data.json")
data = json.loads(data_path.read_text(encoding="utf-8"))

people = [p.strip() for p in data["people"]]
taken = data["taken"]

if not people:
    print("Inga personer hittades i data.json!")
    sys.exit()

available = [i for i, status in enumerate(taken) if not status]
if not available:
    print("Alla personer är redan tagna!")
    sys.exit()

format_json(taken, people, data)

print(f"{colorama.Fore.GREEN}-- Fikahjulet --{colorama.Style.RESET_ALL}")
input("Tryck på Enter för att starta hjulet...")

root = tk.Tk()
root.withdraw()

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

win_w, win_h = 180, 62
arrow_w, arrow_h = 220, 70

radius = min(screen_w, screen_h) // 3 - 25
cx = (screen_w // 2) - 85
cy = screen_h // 2

n = len(people)
winnerindex = choice(available)
winner_name = people[winnerindex]

# Skapa ett fönster per person
cards = []
for i, person in enumerate(people):
    win = tk.Toplevel(root)
    win.title(f"#{i + 1}")
    win.resizable(False, False)
    win.attributes("-topmost", True)

    bg_color = "#7f1d1d" if taken[i] else "#0f172a"
    fg_color = "#fca5a5" if taken[i] else "#38bdf8"
    status_txt = "REDAN TAGEN" if taken[i] else f"{100/len(available):.1f}% CHANS"

    frame = tk.Frame(win, bg=bg_color)
    frame.pack(fill="both", expand=True)

    name_lbl = tk.Label(frame, text=person, font=("Helvetica", 14, "bold"), bg=bg_color, fg="#ffffff")
    name_lbl.pack(pady=(6, 0))

    sub_lbl = tk.Label(frame, text=status_txt, font=("Helvetica", 10, "bold"), bg=bg_color, fg=fg_color)
    sub_lbl.pack()

    # Placera alla på samma punkt i mitten från början
    start_x = int(cx - (win_w / 2))
    start_y = int(cy - (win_h / 2))
    win.geometry(f"{win_w}x{win_h}+{start_x}+{start_y}")

    cards.append((win, frame, name_lbl, sub_lbl))

# Skapa pil på höger sida (gömd)
arrow_win = tk.Toplevel(root)
arrow_win.title("Pil")
arrow_win.resizable(False, False)
arrow_win.attributes("-topmost", True)
arrow_win.withdraw()

arrow_frame = tk.Frame(arrow_win, bg="#14532d")
arrow_frame.pack(fill="both", expand=True)

arrow_name_lbl = tk.Label(
    arrow_frame,
    text="<= VINNARE",
    font=("Helvetica", 14, "bold"),
    bg="#14532d",
    fg="#4ade80"
)
arrow_name_lbl.pack(pady=(8, 0))

arrow_sub_lbl = tk.Label(
    arrow_frame,
    text="",
    font=("Helvetica", 10, "bold"),
    bg="#14532d",
    fg="#bbf7d0"
)
arrow_sub_lbl.pack()

arrow_x = int(cx + radius + (win_w / 2) + 30)
arrow_y = int(cy - (arrow_h / 2))
arrow_win.geometry(f"{arrow_w}x{arrow_h}+{arrow_x}+{arrow_y}")

full_spins = 9
step_angle = (2 * math.pi) / n
target_offset = 0.0 - (winnerindex * step_angle)
total_rotation = (full_spins * 2 * math.pi) + (target_offset % (2 * math.pi))

# Tid i frames (@ 60 FPS)
phase1_frames = 120        # 1. Mitten till linjen       2 sek
phase2_frames = 180        # 2. Bildar cirkeln           3 sek
phase3_frames = 900        # 3. Hjulsnurret             15 sek

# Fas 4 uppdelad i exakta steg (300 + 180 + 300 = 780 frames)
p4_wait1 = 300             # Vänta 5 sek efter snurr
p4_morph = 180             # Forma frågetecken (3 sek)
p4_wait2 = 300             # Vänta 5 sek efter textbyte
phase4_frames = p4_wait1 + p4_morph + p4_wait2

phase5_frames = 180        # 5. Gör en linje (race)     3 sek
phase6_frames = 120        # 6. Skapa rött streck       2 sek

frame = 0

def animate():
    global frame
    center_x = int(cx - (win_w / 2))
    center_y = int(cy - (win_h / 2))

    # 1. Från mitten till linjen
    if frame <= phase1_frames:
        t = ease_out_cubic(frame / phase1_frames)
        for i, (win, _, _, _) in enumerate(cards):
            lx, ly = get_line_pos(i, screen_w, screen_h, n, win_h)
            x = int(lerp(center_x, lx, t))
            y = int(lerp(center_y, ly, t))
            win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # 2. Bilda cirkeln
    elif frame <= phase1_frames + phase2_frames:
        local_f = frame - phase1_frames

        if local_f == 1:
            arrow_win.deiconify()

        for i, (win, _, _, _) in enumerate(cards):
            lx, ly = get_line_pos(i, screen_w, screen_h, n, win_h)
            final_tx, final_ty = get_circle_pos(i, 0.0, step_angle, cx, cy, radius, win_w, win_h)
            
            delay = i * (phase2_frames / (n * 1.5))
            duration = phase2_frames * 0.6
            
            card_t = (local_f - delay) / duration
            card_t = max(0.0, min(1.0, card_t))
            t = ease_out_cubic(card_t)

            x = int(lerp(lx, final_tx, t))
            y = int(lerp(ly, final_ty, t))
            win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # 3. Snurra hjulet
    elif frame <= phase1_frames + phase2_frames + phase3_frames:
        local_f = frame - (phase1_frames + phase2_frames)
        t = local_f / phase3_frames
        ease = 1 - ((1 - t) ** 4)
        current_rot = ease * total_rotation

        for i, (win, _, _, _) in enumerate(cards):
            x, y = get_circle_pos(i, current_rot, step_angle, cx, cy, radius, win_w, win_h)
            win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # 4. Frågetecken och textsekvens
    elif frame <= phase1_frames + phase2_frames + phase3_frames + phase4_frames:
        local_f = frame - (phase1_frames + phase2_frames + phase3_frames)

        if local_f == 1:
            finish_spin(people, cards, winnerindex, taken, data_path, data)
            arrow_win.title("Fikahjulet")
            arrow_name_lbl.configure(text="Ge inte upp än.")
            arrow_sub_lbl.configure(text="Spelet är inte slut.")
            arrow_win.lift()

        elif p4_wait1 < local_f <= p4_wait1 + p4_morph:
            morph_f = local_f - p4_wait1
            t = morph_f / p4_morph
            ease = ease_out_cubic(t)
            final_rot = total_rotation

            for i, (win, _, name_lbl, sub_lbl) in enumerate(cards):
                start_x, start_y = get_circle_pos(i, final_rot, step_angle, cx, cy, radius, win_w, win_h)
                final_x, final_y, target_w, target_h = get_question_mark_pos(i, win_w, win_h)

                x = int(lerp(start_x, final_x, ease))
                y = int(lerp(start_y, final_y, ease))
                w = int(lerp(win_w, target_w, ease))
                h = int(lerp(win_h, target_h, ease))
                
                win.geometry(f"{w}x{h}+{x}+{y}")

        elif local_f == p4_wait1 + p4_morph + 1:
            arrow_name_lbl.configure(text="Det finns fortfarande en chans")
            arrow_sub_lbl.configure(text="för någon annan att vinna!")
            arrow_win.lift()

    elif frame <= phase1_frames + phase2_frames + phase3_frames + phase4_frames + phase5_frames:
        local_f = frame - (phase1_frames + phase2_frames + phase3_frames + phase4_frames)
        t = ease_out_cubic(frame / phase5_frames)
        for i, (win, _, _, _) in enumerate(cards):
            lx, ly = get_line_pos(i, screen_w, screen_h, n, win_h)
            x = int(lerp(center_x, lx, t))
            y = int(lerp(center_y, ly, t))
            win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    elif frame <= phase1_frames + phase2_frames + phase3_frames + phase4_frames + phase5_frames + phase6_frames:
            local_f = frame - (phase1_frames + phase2_frames + phase3_frames + phase4_frames + phase5_frames)
    

    total_all = phase1_frames + phase2_frames + phase3_frames + phase4_frames + phase5_frames + phase6_frames
    if frame < total_all:
        frame += 1
        root.after(16, animate)
    else:
        close_button(arrow_frame, root)

animate()
root.mainloop()
