# Ulazne točke

## `main.py` (korijen repozitorija)

- Provjerava postoji li `.venv` i **ponovno pokreće** skriptu s venv Pythonom.
- Ako paketi nedostaju, ispisuje jasnu poruku.
- Poziva `src.main.main()`.

## `src/main.py`

- Parsira CLI argumente (`argparse`).
- Gradi `ExperimentConfig`.
- Poziva `run_experiments()`.
- S `--open-report` otvara HTML preko `open_html_report()`.

## `src/cli_helpers.py`

Prošireni CLI s podnaredbama (za ručno korištenje / testove):

| Naredba | Funkcija |
|---------|----------|
| `check-data` | Validacija i quality report Jena dataseta |
| `download-data` | Preuzmi CSV ako nedostaje |
| `method-catalog` | Ispiši opis metoda |
| `benchmark` | Mjeri vrijeme izvršavanja |
| `export-thesis` | Brzi run + thesis tablice |

## BAT skripte

| Datoteka | Naredba |
|----------|---------|
| `runfast.bat` | `.venv\python main.py --quick --open-report` |
| `run.bat` | `.venv\python main.py --run-all --open-report` |
| `open_report.bat` | `start results\report.html` |

## `shortcuts.ps1`

PowerShell aliasi `runfast` i `run` (zahtijeva `. .\shortcuts.ps1`).
