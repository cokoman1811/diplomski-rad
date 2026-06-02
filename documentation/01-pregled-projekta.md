# Pregled projekta

## Cilj

Usporediti **klasične metode interpolacije** i **metode strojnog učenja** pri rekonstrukciji temperature iz Jena Climate dataseta nakon umjetne degradacije podataka (zadržavanje svakog n-tog uzorka).

## Glavni eksperiment

1. Učitaj visokorezolucijski vremenski niz temperature (+ covariates).
2. Podijeli podatke: treniranje do 2014., test 2015.–2016.
3. Degradiraj seriju faktorima 2, 3, 6, 12.
4. Rekonstruiraj uklonjene vrijednosti svakom metodom.
5. Evaluiraj MAE, RMSE i R² samo na uklonjenim točkama u testnom razdoblju.
6. Spremi tablice, grafove i HTML izvještaj.

## Struktura repozitorija

| Mapa / datoteka | Namjena |
|-----------------|---------|
| `src/` | Sav Python kod pipelinea |
| `tests/` | Pytest testovi |
| `data/raw/` | Jena CSV (nije u gitu) |
| `results/tables/` | CSV i JSON rezultati |
| `results/figures/` | PNG grafovi |
| `results/report.html` | HTML viewer |
| `documentation/` | Ova tehnička dokumentacija |
| `docs/` | Projektne bilješke, odluke, workflow |
| `legacy/` | Stari sintetički prototip |
| `main.py` | Ulazna točka (automatski koristi `.venv`) |
| `runfast.bat` / `run.bat` | Brzi / puni run + browser |
| `open_report.bat` | Samo otvori postojeći HTML |

## Metode u eksperimentu

**Klasične:** forward_fill, linear, time, cubic, spline  

**ML:** random_forest, mlp  

## Izlazi nakon runa

- `experiment_results.csv` — glavna tablica
- deseci pomoćnih CSV-ova (rang, pivot, thesis export)
- ~50–65 PNG grafova
- `report.html` — preglednik u browseru
