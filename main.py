# Fikahjulet

# Imports
import json
from pathlib import Path
from random import choice
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
data_path = Path(__file__).with_name("data.json")
data = json.loads(data_path.read_text(encoding="utf-8"))

people = data["people"]
taken = data["taken"]

if taken == [1 for _ in people]:
    taken = [0 for _ in people]
    data["taken"] = taken

clear()
print("-- Fikahjulet --")
sleep(1)
input("Tryck på enter för att snurra hjulet")
clear()

arrowindex = 0
available = [i for i, status in enumerate(taken) if status == 0]
winnerindex = choice(available)
winner = (7 * len(people)) + winnerindex

for step in range(winner + 1):
    print("\033[H", end="") # Tillbaka till första raden
    print("-- Fikahjulet --\n")
    
    arrowpoint = arrowindex % len(people)
    
    for i, person in enumerate(people):
        arrow = " <--" if i == arrowpoint else "    "
        style = (colorama.Fore.RED + colorama.Style.BRIGHT) if taken[i] == 1 else (colorama.Fore.WHITE + colorama.Style.NORMAL)
        print(f"{style}{person:<12}{colorama.Style.RESET_ALL}{arrow}", flush=True)
        
    progress = step / winner
    
    sleep(0.04 + (progress ** 5) * .7)
    
    arrowindex += 1

print(f"\nFikahjulet landade på {people[winnerindex]}")

taken[winnerindex] = 1

# Spara på slutet
data_path.write_text(json.dumps(data, indent="\t", ensure_ascii=False), encoding="utf-8")