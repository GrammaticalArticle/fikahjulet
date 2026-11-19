# Fikahjulet

**Fikahjulet** är Python-program som slumpar fram vem som ska bjuda på fika nästa gång. Programmet ser till att ingen väljs två gånger förrän alla i listan har haft sin tur.

## Funktioner

* **Terminalläge (`main.py`):** Snurrar hjulet direkt i terminalen med färger och animationer.
* **Fönsterläge (`windowmain.py`):** Ett läge som använder `tkinter` så att fönster med deltagarnas namn bildar en cirkel, snurrar och avslutar med en race.
* **Konfiguration (`config.py`):** Används för att lägga till och ta bort deltagare.
* **Data:** Resultat sparas i `data.json` och återställs automatiskt när alla har bjudit.
