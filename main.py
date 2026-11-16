# Fikahjulet

# Imports
import json
from pathlib import Path
from random import choice, randint
from time import sleep
import os
import colorama

colorama.init()

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Läsa json, skapa variabler
loadinganimation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
waveanimation = ["⠁⠀⠀⠀", "⠋⠀⠀⠀", "⠞⠁⠀⠀", "⡴⠋⠀⠀", "⣠⠞⠁⠀", "⢀⡴⠋⠀", "⠀⣠⠞⠁", "⠀⢀⡴⠋", "⠀⠀⣠⠞", "⠀⠀⢀⡴", "⠀⠀⠀⣠", "⠀⠀⠀⢀", "⠀⠀⠀⠀"]

data_path = Path(__file__).with_name("data.json")
data = json.loads(data_path.read_text(encoding="utf-8"))

people = data["people"]
taken = data["taken"]

if not people:
    print("Inga personer hittades i data.json!")
    exit()

if len(taken) < len(people):
    taken.extend([False] * (len(people) - len(taken)))
    data["taken"] = taken
elif len(taken) > len(people):
    taken = taken[:len(people)]
    data["taken"] = taken

if taken == [True for _ in people]:
    taken = [False for _ in people]
    data["taken"] = taken

clear()
print(f"{colorama.Fore.GREEN}-- Fikahjulet --{colorama.Style.RESET_ALL}")
sleep(1)
input("Tryck på enter för att snurra hjulet")
clear()

for i in range(randint(12, 30)):
    print(f"Startar hjulet {loadinganimation[i % len(loadinganimation)]}", end="\r", flush=True)
    sleep(0.1)

arrowindex = 0
available = [i for i, status in enumerate(taken) if not status]
winnerindex = choice(available)
winner = (7 * len(people)) + winnerindex

for step in range(winner + 1):
    print("\033[H", end="") # Tillbaka till första raden
    print(f"{colorama.Fore.GREEN}-- Fikahjulet --{colorama.Style.RESET_ALL}\n")
    print(f"{colorama.Fore.LIGHTGREEN_EX}{colorama.Style.BRIGHT}{waveanimation[step % len(waveanimation)]} {colorama.Fore.BLUE}Snurrar hjulet... {colorama.Fore.LIGHTGREEN_EX}{colorama.Style.BRIGHT}{waveanimation[step % len(waveanimation)]}{colorama.Style.RESET_ALL}\n")

    arrowpoint = arrowindex % len(people)
    
    for i, person in enumerate(people):
        arrow = " <--" if i == arrowpoint else "    "
        style = (colorama.Fore.RED + colorama.Style.BRIGHT) if taken[i] else (colorama.Fore.WHITE + colorama.Style.NORMAL)
        print(f"{style}{person:<12}{colorama.Style.RESET_ALL}{arrow}", flush=True)
        
    progress = step / winner
    
    sleep(0.04 + (progress ** 5) * .7)
    
    arrowindex += 1

print(f"\nFikahjulet landade på {people[winnerindex]}")

taken[winnerindex] = True

# Spara på slutet
data_path.write_text(json.dumps(data, indent="\t", ensure_ascii=False), encoding="utf-8")