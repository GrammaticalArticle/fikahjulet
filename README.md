# Fikahjulet

**Fikahjulet** är ett hjul som jag har kodat i Python för att välja vem det är som ska bjuda på *fika* nästa gång.

---

## Vad behövs?

* **Python 3.6+**
* **colorama**
* **En dator med MacOS *(om du vill köra fönsterversionen)***

---

## Setup

1. **Klona repon:**
   ```bash
   git clone https://github.com/GrammaticalArticle/fikahjulet
   cd fikahjulet
   ```

2. **Ladda ner alla imports:**
   ```bash
   pip install colorama
   ```

3. **Lägg till namnen:**
   Öppna `data.json` och ändra placeholders till riktiga namn. Värden i `"taken"` (`false` eller `true`) ändras nu automatiskt:
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

Kör följande kommando:

```bash
python main.py
```

---
På MacOS finns även ett speciellt läge som använder fönster för att skapa hjulet. I så fall, kör följande kommando:

```bash
python macmain.py
```

---

## Struktur

```text
fikahjulet/
├── data.json
├── macmain.py
├── main.py
└── README.md
```
