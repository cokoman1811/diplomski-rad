# Dokumentacija projekta

Diplomski rad: **Interpolacija podataka pomoću strojnog učenja**.

Ovaj folder sadrži tehničku dokumentaciju cijelog repozitorija — što radi svaka datoteka, kako moduli surađuju i kako pokrenuti program.

## Sadržaj

| Datoteka | Opis |
|----------|------|
| **[STO-SE-DOGADA.md](STO-SE-DOGADA.md)** | **Počni ovdje** — uvod i objašnjenje cijelog projekta jednostavnim jezikom |
| [01-pregled-projekta.md](01-pregled-projekta.md) | Cilj rada, struktura mapa, glavni tok |
| [02-pokretanje.md](02-pokretanje.md) | Kako pokrenuti eksperiment, HTML viewer, skripte |
| [03-tok-eksperimenta.md](03-tok-eksperimenta.md) | Korak-po-korak što se događa u `run_experiments` |
| [04-ulazne-tocke.md](04-ulazne-tocke.md) | `main.py`, BAT datoteke, CLI |
| [05-podaci.md](05-podaci.md) | Učitavanje, validacija, kvaliteta, degradacija |
| [06-metode.md](06-metode.md) | Klasična interpolacija, ML, značajke, tuning |
| [07-evaluacija-i-analiza.md](07-evaluacija-i-analiza.md) | Metrike, statistika, analiza rezultata |
| [08-izlaz-i-vizualizacija.md](08-izlaz-i-vizualizacija.md) | Grafovi, tablice, HTML report, thesis export |
| [09-pomocni-moduli.md](09-pomocni-moduli.md) | Config, paths, console, method_info, benchmarks |
| [10-testovi-i-legacy.md](10-testovi-i-legacy.md) | Test suite i stari prototip |

## Brza mapa modula (`src/`)

```
main.py / experiment_runner.py     → pokretanje eksperimenta
config.py / paths.py               → postavke i putanje
data_loader.py / download_data.py  → Jena dataset
preprocessing.py                   → degradacija (svaki n-ti uzorak)
interpolation_methods.py           → klasične metode
feature_engineering.py / ml_models.py → ML pipeline
evaluation.py / analysis.py        → MAE, RMSE, R², rangiranje
plots.py / report_html.py          → PNG grafovi + HTML viewer
console.py                         → lijepi ispis u terminalu
```

## Povezana dokumentacija

Projektna pravila i odluke ostaju u mapi `docs/`:

- `docs/project.md` — opis rada
- `docs/workflow.md` — dnevni radni tok
- `docs/decisions.md` — tehničke odluke
- `docs/progress.md` — status zadataka
