# Tok eksperimenta

Glavna funkcija: `run_experiments()` u `src/experiment_runner.py`.

## Dijagram

```
load_jena_dataset()
        ↓
[quick?] slice zadnjih N uzoraka oko 2015.
        ↓
build_train_test_masks()
        ↓
for factor in [2,3,6,12]:
    degrade_series()          → svaki n-ti ostaje, ostalo NaN
    for method in methods:
        classical → interpolate()
        ml        → build features → train → predict
        compute_metrics()       → samo uklonjene točke u testu
        [plots]                 → PNG u results/figures/
    friedman + wilcoxon         → JSON/CSV po faktoru
        ↓
aggregate_results() → experiment_results.csv
save_all_reports()  → markdown + CSV
export_all_thesis_tables()
generate_html_report() → results/report.html
print_experiment_summary() → terminal (console.py)
```

## ExperimentConfig

Dataclass u `experiment_runner.py`:

| Polje | Značenje |
|-------|----------|
| `quick` | Manji uzorak, manje faktora |
| `factors` | Lista faktora degradacije |
| `methods` | Lista metoda |
| `tune_ml` | GridSearchCV za RF i MLP |
| `use_test_split` | Evaluacija samo 2015.–2016. |
| `generate_plots` | Generiraj PNG |

## Što se cacheira

`best_params` — hiperparametri ML modela nakon prvog tuninga po metodi (ne ponavlja se za svaki faktor).

## Trajanje

- `--quick --no-tune`: ~10 s
- `--run-all` s tuningom: nekoliko minuta (ovisno o CPU)

## Warnings tijekom runa

`Skipping features without any observed values: lag_*` — sklearn preskače prazne lag značajke kod ML modela. Nije greška; program nastavlja normalno.
