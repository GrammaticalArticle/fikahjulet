# This file is only for Mac users
import sys
import json
import math
import tkinter as tk
from pathlib import Path
from random import choice, uniform
import colorama

colorama.init()

if sys.platform != "darwin":
    print("Denna program fungerar bara på macOS. Starta main.py istället.")
    print("Jag kommer inte ens försöka porta detta till Windows eller Linux.")
    sys.exit()

# Läsa json, skapa variabler
data_path = Path(__file__).with_name("data.json")
data = json.loads(data_path.read_text(encoding="utf-8"))

people = [p.strip() for p in data["people"]]
taken = data["taken"]

if not people:
    print("Inga personer hittades i data.json!")
    sys.exit()

if len(taken) < len(people):
    taken.extend([False] * (len(people) - len(taken)))
    data["taken"] = taken
elif len(taken) > len(people):
    taken = taken[:len(people)]
    data["taken"] = taken

if taken == [True for _ in people]:
    taken = [False for _ in people]
    data["taken"] = taken

print(f"{colorama.Fore.GREEN}-- Fikahjulet --{colorama.Style.RESET_ALL}")
input("Tryck på Enter för att starta hjulet...")

root = tk.Tk()
root.withdraw()

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

win_w, win_h = 180, 62
arrow_w, arrow_h = 175, 62

radius = min(screen_w, screen_h) // 3 - 25
cx = (screen_w // 2) - 85
cy = screen_h // 2

n = len(people)
available = [i for i, status in enumerate(taken) if not status]
winnerindex = choice(available)

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
tk.Label(
    arrow_frame,
    text="<= VINNARE",
    font=("Helvetica", 15, "bold"),
    bg="#14532d",
    fg="#4ade80"
).pack(expand=True)

arrow_x = int(cx + radius + (win_w / 2) + 30)
arrow_y = int(cy - (arrow_h / 2))
arrow_win.geometry(f"{arrow_w}x{arrow_h}+{arrow_x}+{arrow_y}")

full_spins = 9
step_angle = (2 * math.pi) / n
target_offset = 0.0 - (winnerindex * step_angle)
total_rotation = (full_spins * 2 * math.pi) + (target_offset % (2 * math.pi))

# Tidsramar i frames (ca 60 FPS)
line_frames = 50        # 1. Mitten till linjen
snake_frames = 120      # 2. Bildar cirkeln
spin_frames = 660       # 3. Hjulsnurret (11 sek)

frame = 0

def lerp(a, b, t): # Linear
    return a + (b - a) * t

def ease_out_cubic(t):
    return 1 - ((1 - t) ** 3)

def get_line_pos(i):
    lx = int(screen_w * 0.15)
    total_h = min(screen_h - 120, n * (win_h + 10))
    start_y = (screen_h - total_h) // 2
    step_y = total_h / max(1, n - 1) if n > 1 else 0
    ly = int(start_y + i * step_y - (win_h / 2))
    return lx, ly

def get_circle_pos(i, rot=0.0):
    angle = rot + (i * step_angle)
    x = int(cx + radius * math.cos(angle) - (win_w / 2))
    y = int(cy + radius * math.sin(angle) - (win_h / 2))
    return x, y

def animate():
    global frame
    center_x = int(cx - (win_w / 2))
    center_y = int(cy - (win_h / 2))

    # 1. Från mitten till linjen
    if frame <= line_frames:
        t = ease_out_cubic(frame / line_frames)
        for i, (win, _, _, _) in enumerate(cards):
            lx, ly = get_line_pos(i)
            x = int(lerp(center_x, lx, t))
            y = int(lerp(center_y, ly, t))
            win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # 2. Bilda cirkeln
    elif frame <= line_frames + snake_frames:
        local_f = frame - line_frames
        
        if local_f == 1:
            arrow_win.deiconify()

        # Vi hittar vart varje fönster ska vara
        for i, (win, _, _, _) in enumerate(cards):
            lx, ly = get_line_pos(i)
            final_tx, final_ty = get_circle_pos(i, 0.0)
            
            # delay
            delay = i * (snake_frames / (n * 1.5))
            duration = snake_frames * 0.6
            
            card_t = (local_f - delay) / duration
            card_t = max(0.0, min(1.0, card_t))
            t = ease_out_cubic(card_t)

            x = int(lerp(lx, final_tx, t))
            y = int(lerp(ly, final_ty, t))
            win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # 3. Snurra hjulet
    else:
        local_f = frame - (line_frames + snake_frames)
        t = local_f / spin_frames
        ease = 1 - ((1 - t) ** 4)
        current_rot = ease * total_rotation

        for i, (win, _, _, _) in enumerate(cards):
            x, y = get_circle_pos(i, current_rot)
            win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    total_all = line_frames + snake_frames + spin_frames
    if frame < total_all:
        frame += 1
        root.after(16, animate)
    else:
        finish_spin()

def finish_spin():
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

    for widget in arrow_frame.winfo_children():
        widget.destroy()
    tk.Button(
        arrow_frame,
        text="Stäng hjul ✕",
        font=("Helvetica", 12, "bold"),
        command=root.destroy
    ).pack(expand=True, fill="both")

animate()
root.mainloop()