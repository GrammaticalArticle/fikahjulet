import json
import tkinter as tk
from pathlib import Path
from common import clear
from time import sleep
import colorama
from common import format_json

# Läs in data.json
data_path = Path(__file__).with_name("data.json")
data = json.loads(data_path.read_text(encoding="utf-8"))

taken, people, data = format_json(data["taken"], data["people"], data)

data_path.write_text(json.dumps(data, indent="\t", ensure_ascii=False), encoding="utf-8")

data_path = Path(__file__).with_name("data.json")
data = json.loads(data_path.read_text(encoding="utf-8"))

root = tk.Tk()
root.title("Fikahjulet Configuration")
root.geometry("300x400")

listbox = tk.Listbox(root, font=("Helvetica", 11))
listbox.pack(padx=10, pady=10, fill="both", expand=True)

for person in data["people"]:
    listbox.insert(tk.END, person)

entry = tk.Entry(root, font=("Helvetica", 11))
entry.pack(padx=10, pady=5, fill="x")

def add():
    name = entry.get().strip()
    if name:
        if not name in data["people"]:
            data["people"].append(name)
            data["taken"].append(False)
            listbox.insert(tk.END, name)
            entry.delete(0, tk.END)
        else:
            clear()
            print("(det här är fake)")
            print("Deleting System32")
            for i in range(15):
                print(f"\r{colorama.Fore.RED}{colorama.Style.BRIGHT}Deleting System32 [" + "#"*i + " "*(14-i) + f"]{colorama.Style.RESET_ALL}", end="")
                sleep(0.12)
            print()
            entry.delete(0, tk.END)
            root.destroy()

def remove():
    try:
        selected_index = listbox.curselection()[0]
        
        data["people"].pop(selected_index)
        data["taken"].pop(selected_index)
        
        listbox.delete(selected_index)
    except IndexError:
        pass

def save():
    data_path.write_text(json.dumps(data, indent="\t", ensure_ascii=False), encoding="utf-8")
    print("Ändringarna har sparats till data.json!")
    sleep(0.2)

# Koppla knapparna till funktionerna
btn_add = tk.Button(root, text="Lägg till", command=add)
btn_add.pack(padx=10, pady=2, fill="x")

btn_remove = tk.Button(root, text="Ta bort markerad", command=remove)
btn_remove.pack(padx=10, pady=2, fill="x")

btn_save = tk.Button(root, text="Spara",command=save)
btn_save.pack(padx=10, pady=10, fill="x")

root.mainloop()