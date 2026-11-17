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

# Skapa pil på höger sida (gömd) - Ursprunglig position vid start
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

# Fas 4 (hoppar direkt till linje på 2 sek = 120 frames)
phase4_frames = 120

phase5_frames = 120        # 5. Gör en linje (race)     2 sek
phase6_frames = 360        # 6. Skapa röda linjer       2 sek
phase7_frames = 360        # 7. Nedräkning 3, 2, 1, 0   6 sek (60 frames per sekund)
phase8_frames = 900        # 8. Race                   15 sek

frame = 0

red_line_win = None
end_line_win = None
traffic_lights = []

race_profiles = []
for i in range(n):
    if i == winnerindex:
        finish_ratio = 1.0
        wobble1 = uniform(0.02, 0.05)
        wobble2 = uniform(-0.04, -0.01)
    else:
        finish_ratio = uniform(0.85, 0.97)
        wobble1 = uniform(0.06, 0.14)
        wobble2 = uniform(-0.07, 0.05)
    race_profiles.append((finish_ratio, wobble1, wobble2))

def animate():
    global frame, red_line_win, end_line_win, traffic_lights
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

    # 4. Direkt till linje utan frågetecken (2 sekunder)
    elif frame <= phase1_frames + phase2_frames + phase3_frames + phase4_frames:
        local_f = frame - (phase1_frames + phase2_frames + phase3_frames)

        if local_f == 1:
            finish_spin(people, cards, winnerindex, taken, data_path, data)
            arrow_win.title("Fikahjulet")
            arrow_name_lbl.configure(text="GÖR ER REDO!")
            arrow_sub_lbl.configure(text="Ställ upp vid startlinjen!")
            arrow_win.lift()

        t = ease_out_cubic(local_f / phase4_frames)
        final_rot = total_rotation

        for i, (win, _, _, _) in enumerate(cards):
            start_x, start_y = get_circle_pos(i, final_rot, step_angle, cx, cy, radius, win_w, win_h)
            lx, ly = get_line_pos(i, screen_w, screen_h, n, win_h)

            x = int(lerp(start_x, lx, t))
            y = int(lerp(start_y, ly, t))
            
            win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # 5. Skapa röda linjer (Startlinje och Mållinje)
    elif frame <= phase1_frames + phase2_frames + phase3_frames + phase4_frames + phase5_frames:
        local_f = frame - (phase1_frames + phase2_frames + phase3_frames + phase4_frames)

        if local_f == 1:
            red_line_win = tk.Toplevel(root)
            red_line_win.overrideredirect(True)
            red_line_win.attributes("-topmost", True)
            tk.Frame(red_line_win, bg="#dc2626").pack(fill="both", expand=True)
            red_line_win.geometry("10x20+540+60")
            red_line_win.update_idletasks()
            red_line_win.lift()

            end_line_win = tk.Toplevel(root)
            end_line_win.overrideredirect(True)
            end_line_win.attributes("-topmost", True)
            tk.Frame(end_line_win, bg="#dc2626").pack(fill="both", expand=True)
            finish_line_x = screen_w - 550
            end_line_win.geometry(f"10x20+{finish_line_x}+60")
            end_line_win.update_idletasks()
            end_line_win.lift()

        if red_line_win is not None and end_line_win is not None:
            t = ease_out_cubic(local_f / phase5_frames)
            current_h = int(lerp(20, screen_h - 120, t))
            red_line_win.geometry(f"10x{current_h}+540+60")
            end_line_win.geometry(f"10x{current_h}+{screen_w - 550}+60")

    # 6. Nedräkning 3, 2, 1, 0 (360 frames = 6 sekunder @ 60 FPS)
    elif frame <= phase1_frames + phase2_frames + phase3_frames + phase4_frames + phase5_frames + phase6_frames:
        local_f = frame - (phase1_frames + phase2_frames + phase3_frames + phase4_frames + phase5_frames)

        light_w, light_h = 90, 90
        spacing = 20
        total_lights_w = (3 * light_w) + (2 * spacing)
        base_x = (screen_w - total_lights_w) // 2
        start_y = 40
        target_y = 110

        # Sekund 1 (frames 1 - 60): Skapa trafikljus och visa "3" (alla röda eller mörka början)
        if local_f == 1:
            traffic_lights.clear()
            for idx in range(3):
                l_win = tk.Toplevel(root)
                l_win.overrideredirect(True)
                l_win.attributes("-topmost", True)
                l_frame = tk.Frame(l_win, bg="#334155")
                l_frame.pack(fill="both", expand=True)
                lx = base_x + idx * (light_w + spacing)
                l_win.geometry(f"{light_w}x1+{lx}+{start_y}")
                l_win.update_idletasks()
                l_win.lift()
                traffic_lights.append((l_win, l_frame))
            
            arrow_name_lbl.configure(text="3")
            arrow_sub_lbl.configure(text="")

        if local_f <= 60:
            t = ease_out_cubic(local_f / 60)
            cur_y = int(lerp(start_y, target_y, t))
            cur_h = max(1, int(lerp(1, light_h, t)))
            for idx, (l_win, _) in enumerate(traffic_lights):
                lx = base_x + idx * (light_w + spacing)
                l_win.geometry(f"{light_w}x{cur_h}+{lx}+{cur_y}")

            # Mjuk förflyttning av pilen till 125 px från toppen
            current_arrow_x, current_arrow_y = arrow_win.winfo_x(), arrow_win.winfo_y()
            target_arrow_x = int((screen_w - arrow_w) // 2)
            target_arrow_y = 125
            
            ax = int(lerp(current_arrow_x, target_arrow_x, t))
            ay = int(lerp(current_arrow_y, target_arrow_y, t))
            arrow_win.geometry(f"{arrow_w}x{arrow_h}+{ax}+{ay}")
            arrow_win.lift()

        # Sekund 2 (frames 61 - 120): Siffra 2, första ljuset blir RÖTT
        elif local_f == 61:
            arrow_name_lbl.configure(text="2")
            traffic_lights[0][0].configure(bg="#ef4444")
            traffic_lights[0][1].configure(bg="#ef4444")

        # Sekund 3 (frames 121 - 180): Siffra 1, andra ljuset blir GULT
        elif local_f == 121:
            arrow_name_lbl.configure(text="1")
            traffic_lights[1][0].configure(bg="#eab308")
            traffic_lights[1][1].configure(bg="#eab308")

        # Sekund 4 (frames 181 - 240): Siffra 0, tredje ljuset blir GRÖNT
        elif local_f == 181:
            arrow_name_lbl.configure(text="0")
            traffic_lights[2][0].configure(bg="#22c55e")
            traffic_lights[2][1].configure(bg="#22c55e")

        # Sekund 5-6 (frames 241 - 360): "KÖR!!" (eller liknande text) innan racet startar
        elif local_f == 241:
            arrow_name_lbl.configure(text="KÖR!!")

    # 7. Racet (900 frames = 15 sek) + startljusen glider ut samtidigt
    elif frame <= phase1_frames + phase2_frames + phase3_frames + phase4_frames + phase5_frames + phase6_frames + phase7_frames:
        local_f = frame - (phase1_frames + phase2_frames + phase3_frames + phase4_frames + phase5_frames + phase6_frames)
        t = local_f / phase7_frames

        # Glid ut startljusen uppåt under första sekunden av racet
        if local_f <= 60 and traffic_lights:
            light_w, light_h = 90, 90
            spacing = 20
            base_x = (screen_w - ((3 * light_w) + (2 * spacing))) // 2
            slide_t = ease_out_cubic(local_f / 60)
            cur_y = int(lerp(110, 40, slide_t))
            cur_h = max(1, int(lerp(light_h, 1, slide_t)))
            for idx, (l_win, _) in enumerate(traffic_lights):
                lx = base_x + idx * (light_w + spacing)
                l_win.geometry(f"{light_w}x{cur_h}+{lx}+{cur_y}")
        elif local_f == 61 and traffic_lights:
            for l_win, _ in traffic_lights:
                l_win.destroy()
            traffic_lights.clear()

        finish_line_x = screen_w - 450
        for i, (win, _, _, _) in enumerate(cards):
            start_x, ly = get_line_pos(i, screen_w, screen_h, n, win_h)
            finish_ratio, wobble1, wobble2 = race_profiles[i]

            base_progress = t * finish_ratio
            surge = math.sin(t * math.pi) * wobble1 + math.sin(t * 3 * math.pi) * wobble2
            progress = max(0.0, base_progress + surge * (1 - abs(2 * t - 1)))

            x = int(lerp(start_x, finish_line_x, progress))
            win.geometry(f"{win_w}x{win_h}+{x}+{ly}")

        if local_f == phase7_frames:
            win, frame_w, name_lbl, sub_lbl = cards[winnerindex]
            frame_w.configure(bg="#ca8a04")
            name_lbl.configure(bg="#ca8a04", text=f"👑 {winner_name} 👑")
            sub_lbl.configure(bg="#ca8a04", fg="#fef08a", text="DUBBELVINNARE!")
            win.lift()

    total_all = (
        phase1_frames + phase2_frames + phase3_frames + phase4_frames +
        phase5_frames + phase6_frames + phase7_frames
    )
    if frame < total_all:
        frame += 1
        root.after(16, animate)
    else:
        close_button(arrow_frame, root)

animate()
root.mainloop()