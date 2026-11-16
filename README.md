# Fikahjulet

**Fikahjulet** är ett hjul som jag har kodat i Python för att välja vem det är som ska bjuda på *fika* nästa gång.

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

2. **Ladda ner alla imports:**
   ```bash
   pip install colorama
   ```

3. **Lägg till namnen:**
   Öppna `data.json` och ändra placeholders till riktiga namn. Beroende på `"taken"`s längd ändras antalet värden (`false` eller `true`) så att det matchar antalet personer:
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

## Struktur

```text
fikahjulet/
├── main.py
├── data.json
└── README.md
```
