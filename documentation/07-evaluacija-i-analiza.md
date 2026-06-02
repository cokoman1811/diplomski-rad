# Evaluacija i statistička analiza

## `src/evaluation.py`

Osnovne metrike na evaluacijskoj maski:

- **MAE** — srednja apsolutna pogreška
- **RMSE** — korijen srednje kvadratne pogreške
- **R²** — koeficijent determinacije

Funkcije:

- `compute_metrics(original, reconstructed, eval_mask)`
- `compute_point_errors()` — apsolutne pogreške po točkama
- `aggregate_results()` — spaja listu dictova u DataFrame

## `src/evaluation_extended.py`

Proširene metrike: median_ae, max_error, explained_variance, bias.

- `summarize_metrics_by_method()` / `by_factor()`
- `top_n_methods()` — top N metoda po faktoru

## `src/analysis.py`

Analiza performansi za izvještaje:

- `rank_methods_by_metric()` — rang unutar faktora
- `best_method_per_factor()`
- `compare_classical_vs_ml()`
- `build_method_leaderboard()` — prosječni rang po metodi
- `method_stability_score()`, `classical_ml_gap()`
- analiza grešaka po danu, sezoni, satu

## `src/statistical_analysis.py`

- `friedman_test()` — usporedba više metoda
- `compare_methods_for_factor()` — Wilcoxon vs linear baseline
- `build_error_matrix()` — matrica grešaka po metodama
- `summarize_errors()`

## `src/statistical_analysis_extended.py`

Dodatni testovi (Kruskal-Wallis, bootstrap, paired t-test) za dublju analizu u testovima i proširene izvještaje.

## Interpretacija

Evaluacija je **samo na uklonjenim točkama u testnom razdoblju** — model ne “varajući” gleda poznate vrijednosti iz train dijela.

Negativan R² (npr. loš MLP) znači da model predviđa gorе od prosjeka.
