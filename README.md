# Fikahjulet

**Fikahjulet** är ett hjul som jag har kodat i Python för att välja vem det är som ska bjuda på *fika* nästa gång.

**Fikahjulet** använder `colorama` i den klassiska versionen (`main.py`) som körs i konsollen, och `tkinter` samt `Pillow` för att skapa fönstren i fönster-läge (`windowmain.py`).

## Vad behövs?

* **Python 3.6+**
* **colorama**
* **Pillow**

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
      * Alternativt kan man starta `config.py` med `python config.py`.
   * För att lägga till valfria avatarer för person 1 till 10, skapa en mapp som heter `avatar/` och lägg till bilderna som `avatar1.png`, `avatar2.png`, osv.
      * Funktionen för att lägga till, ändra, och ta bort bilder i konfigurationsfilen `config.py` är inte än tillgängligt.

## Hur startar man Fikahjulet?

Om du vill köra den klassiska versionen i terminalen, kör följande kommando:

```bash
python main.py
```

Det finns även ett annat läge som använder fönster för att skapa hjulet. För att köra detta läge, använd följande kommando:

```bash
python windowmain.py
```

Från start är datan fylld med placeholders. De kan bytas genom att manuellt ändra data.json, eller genom ett konfiguationsscript. För att köra konfigurationsscriptet, starta följande kommando:

```bash
python config.py
```

## Struktur

```text
fikahjulet/
├── data.json
├── .gitignore
├── README.md
├── common.py
├── config.py
├── main.py
├── windowdef.py
├── windowmain.py
├── avatar/
│   ├── avatar1.png
│   ├── avatar2.png
│   └── ...
└── tests/
    ├── conftest.py
    ├── test_common.py
    ├── test_windowdef.py
    ├── test_windowmain.py
    ├── test_config.py
    └── test_main.py
```