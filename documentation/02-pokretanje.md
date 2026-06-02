# Pokretanje programa

## Preporučeni način (Windows)

```bat
runfast.bat
```

Brzi eksperiment (manji uzorak, faktori 2 i 6) + generiranje `report.html` + otvaranje u browseru.

Puni eksperiment:

```bat
run.bat
```

Samo otvori postojeći HTML (bez novog runa):

```bat
open_report.bat
```

## PowerShell / terminal

```powershell
cd "C:\Users\...\diplomski rad"
python main.py --quick --open-report
python main.py --run-all --open-report
python main.py --run-all --no-tune
```

`main.py` automatski prebacuje na `.venv\Scripts\python.exe` ako postoji.

## Važne CLI opcije

| Opcija | Značenje |
|--------|----------|
| `--quick` | Manji dataset, faktori 2 i 6 |
| `--run-all` | Cijeli dataset, faktori 2, 3, 6, 12 |
| `--no-tune` | Bez GridSearch za ML |
| `--no-plots` | Bez PNG grafova |
| `--open-report` | Otvori `results/report.html` nakon runa |
| `--factor N` | Samo odabrani faktor (ponovljivo) |
| `--method NAME` | Samo odabrana metoda |

## HTML viewer

Datoteka: `results/report.html`

- tablice rezultata i leaderboard
- galerija grafova s filterima (kategorija, faktor, metoda)
- linkovi na CSV tablice

Header se **skrola s ostatkom stranice** (nije fiksiran na vrhu).

Ručno otvaranje:

```powershell
start results\report.html
```

## Okruženje

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

Ako vidiš `No module named 'pandas'`, koristi `.venv` Python, ne Windows Store `python`.
