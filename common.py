import os

loadinganimation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
waveanimation = ["⠁⠀⠀⠀", "⠋⠀⠀⠀", "⠞⠁⠀⠀", "⡴⠋⠀⠀", "⣠⠞⠁⠀", "⢀⡴⠋⠀", "⠀⣠⠞⠁", "⠀⢀⡴⠋", "⠀⠀⣠⠞", "⠀⠀⢀⡴", "⠀⠀⠀⣠", "⠀⠀⠀⢀", "⠀⠀⠀⠀"]

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def format_json(taken, people, data):
    if not people:
        print("Inga personer hittades. Genererar...")
        people = [f"Person {i + 1}" for i in range(10)]
    if len(taken) < len(people):
        print("För få värden hittades. Genererar...")
        taken.extend([False] * (len(people) - len(taken)))
        data["taken"] = taken
    elif len(taken) > len(people):
        print("För många värden hittades. Klipper...")
        taken = taken[:len(people)]
        data["taken"] = taken
    if taken == [True for _ in people]:
        taken = [False for _ in people]
        data["taken"] = taken

    return taken, people, data