# Fikahjulet

**Fikahjulet** är ett hjul som jag har kodat i Python för att välja vem ska bjuda på *fika* nästa gång.

---

## Vad behövs?

* **Python 3.6+**
* **colorama**
* **pathlib**
* **random**
* **time**
* **os**

---

## Setup

1. **Klona repon:**
   ```bash
   git clone https://github.com/GrammaticalArticle/fikahjulet
   cd fikahjulet
   ```

2. **Ladda ner alla imports:**
   ```bash
   pip install colorama pathlib random time os
   ```

3. **Lägg till namnen:**
   Öppna `data.json` och ändra placeholders till riktiga namn. Se till att listan `"taken"` har exakt samma antal `false`-värden som det finns personer:
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

## Hur att starta Fikahjulet?

Kör följande kommando:

```bash
python main.py
```

---

## Struktur

```text
fikahjulet/
├── main.py
├── data.json
└── README.md
```
