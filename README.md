# Fikahjulet

**Fikahjulet** är ett hjul som jag har kodat i Python för att välja vem det är som ska bjuda på *fika* nästa gång.

**Fikahjulet** använder `colorama` i den klassiska versionen (`main.py`) som körs i konsollen, och `tkinter` samt `Pillow` för att skapa fönstren i fönster-läge (`windowmain.py`).

## Vad behövs?

* **Python 3.6+**
* **colorama**
* **Pillow** (för att läsa in och skala avatarytor i fönsterläget)

## Setup

1. **Klona repon:**
   ```bash
   git clone https://github.com/GrammaticalArticle/fikahjulet
   cd fikahjulet
   ```

2. **Ladda ner beroenden:**
   ```bash
   pip install colorama Pillow
   ```

3. **Lägg till namnen och avatars:**
   * Öppna `data.json` och ändra placeholders till riktiga namn. Värden i `"taken"` (`false` eller `true`) ändras automatiskt.
   * För att lägga till valfria avatarer för person 1 till 10, skapa en mapp som heter `avatar/` och lägg till bilderna som `avatar1.png`, `avatar2.png`, etc. Bilderna skalas automatiskt till fönstrets höjd utan att sträckas ut.

## Hur startar man Fikahjulet?

Om du vill köra den klassiska versionen i terminalen, kör följande kommando:

```bash
python main.py
```

Det finns även ett annat läge som använder fönster för att skapa hjulet, en snygg inledande animation och ett spännande race där vinnaren från hjulet får en något större bubbla och text för att visa att de är vinnare. För att köra detta läge, använd följande kommando:

```bash
python windowmain.py
```

## Struktur

```text
fikahjulet/
├── data.json
├── .gitignore
├── README.md
├── windowmain.py
├── main.py
├── common.py
├── windowdef.py
└── avatar/
    ├── avatar1.png
    ├── avatar2.png
    └── ...
```