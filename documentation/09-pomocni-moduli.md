# Pomoćni moduli

## `src/console.py`

Estetski ispis u terminalu:

- banner, sekcije, progress bar
- formatirana tablica rezultata
- leaderboard, putanje spremljenih datoteka
- boje preko `colorama`, Unicode fallback na ASCII
- automatski UTF-8 na stdout kad je moguće

## `src/benchmarks.py`

Mjeri wall-clock vrijeme po metodi:

- `benchmark_methods()` — klasične + ML (ML samo ako sample ≥ 4000)
- `format_benchmark_table()` — tekstualna tablica za terminal

## `src/experiment_runner.py`

**Srce projekta** — vidi [03-tok-eksperimenta.md](03-tok-eksperimenta.md).

- `ExperimentConfig`, `run_single_method()`, `run_experiments()`

## `src/__init__.py`

Označava `src` kao Python paket.

## `src/main.py` (unutar src/)

CLI entry point — vidi [04-ulazne-tocke.md](04-ulazne-tocke.md).

## Ovisnosti između modula (pojednostavljeno)

```
config, paths
    ↓
data_loader, download_data, validation, preprocessing
    ↓
interpolation_methods | feature_engineering → ml_models → hyperparameter_tuning
    ↓
evaluation → analysis, statistical_analysis
    ↓
plots, reporting, thesis_export, report_html
    ↓
experiment_runner → console
```

## Datoteke izvan `src/`

| Datoteka | Uloga |
|----------|-------|
| `requirements.txt` | Produkcijski paketi |
| `requirements-dev.txt` | pytest i dev alati |
| `AGENTS.md` | Pravila za AI agente |
| `pytest.ini` / `conftest.py` | Konfiguracija testova |
