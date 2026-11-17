# Fikahjulet

**Fikahjulet** är ett hjul som jag har kodat i Python för att välja vem det är som ska bjuda på *fika* nästa gång.

**Fikahjulet** använder `colorama` i den klassiska versionen (`main.py`) som kört i konsollen, och `tkinter` för att skapa fönstren i fönster-läge (`windowmain.py`)

---

## Vad behövs?

* **Python 3.6+**
* **colorama**

---

## Setup

1. **Klona repon:**
   ```bash
   git clone https://github.com/GrammaticalArticle/fikahjulet
   cd fikahjulet
   ```

2. **Ladda ner colorama:**
   ```bash
   pip install colorama
   ```

3. **Lägg till namnen:**
   Öppna `data.json` och ändra placeholders till riktiga namn. Värden i `"taken"` (`false` eller `true`) ändras  automatiskt:
   ```json
   {
     "people": [
       "Anna",
       "Bertil",
       "Charlie",
       "Dennis",
       "Emil",
       "Felicia",
       "Gustav",
       "Hugo"
     ],
     "taken": [
       false,
       false,
       false,
       false,
       false,
       false,
       false,
       false
     ]
   }
   ```

---

## Hur startar man Fikahjulet?

Om du vill köra den klassiska versionen i terminalen, kör följande kommando:

```bash
python main.py
```

---
Det finns även ett annat läge som använder fönster för att skapa hjulet och en liten animation på början. I så fall, kör följande kommando:

```bash
python windowmain.py
```

---

## Struktur

```text
fikahjulet/
├── data.json
├── .gitignore
├── README.md
├── windowmain.py
├── main.py
├── common.py
└── windowdef.py
```
