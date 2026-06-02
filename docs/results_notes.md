# Results notes

Notes for the thesis **Results** and **Discussion** chapters.
Generated after running `python main.py --run-all --no-tune`.

Evaluation period: removed values in the **2015–2016 test split** only.

---

## Experiment setup

- Dataset: Jena Climate (`jena_climate_2009_2016.csv`)
- Target: temperature (`T (degC)`)
- Degradation factors: 2, 3, 6, 12
- Classical methods: forward fill, linear, time, cubic, spline
- ML methods: Random Forest, MLP (default parameters in this run)
- Metrics: MAE, RMSE, R² on artificially removed values

Output files:

- `results/tables/experiment_results.csv`
- `results/tables/wilcoxon_vs_linear_factor_*.csv`
- `results/tables/friedman_factor_*.json`
- `results/figures/` (bar charts, heatmaps, boxplots, reconstruction plots)

---

## Main findings by degradation factor

### Factor 2 (simulated 20-minute resolution)

Best methods by MAE:

1. cubic (~0.074 °C)
2. time / linear (~0.076 °C)
3. forward fill (~0.165 °C)

Random Forest (~0.174 °C) is close to forward fill. Spline and MLP are worse in this run.

### Factor 3 (30-minute resolution)

Best methods:

1. linear / time / cubic (~0.103 °C)
2. forward fill / Random Forest (~0.23 °C)

### Factor 6 (60-minute resolution)

Best methods:

1. linear / time (~0.16 °C)
2. cubic (~0.163 °C)
3. forward fill (~0.40 °C)

Random Forest degrades strongly (~2.38 °C MAE) without tuning at this factor.

### Factor 12 (120-minute resolution)

Best methods:

1. linear / time (~0.25 °C)
2. cubic (~0.24 °C)
3. forward fill (~0.71 °C)

ML methods (RF, MLP) underperform classical methods at the highest degradation level in this run.

---

## General conclusions for the thesis

1. **Classical interpolation** (especially linear, time-based and cubic) is very strong when missing values follow a regular every-nth pattern.
2. **Error increases** with the degradation factor for all methods, as expected.
3. **Forward fill** is simple but clearly weaker when gaps become wider (factors 6 and 12).
4. **Spline** underperforms linear/cubic here — worth discussing overshooting or boundary effects.
5. **Machine learning** needs **hyperparameter tuning** (`python main.py --run-all` without `--no-tune`) before final thesis conclusions. Default MLP/RF settings are not competitive in this baseline run.
6. **Statistical tests** (Wilcoxon vs linear, Friedman across methods) are saved per factor in `results/tables/`.

---

## Suggested thesis phrases (Croatian)

- Rezultati pokazuju da klasične metode interpolacije postižu vrlo niske pogreške pri manjim faktorima degradacije.
- Usporedba pokazuje da se pogreška rekonstrukcije povećava s porastom faktora degradacije.
- Metoda linearna interpolacija i vremenska interpolacija ostvarile su najstabilnije rezultate u testnom razdoblju.
- Jedno od ograničenja rada je da ML modeli u ovom pokretanju nisu korišteni s GridSearch optimizacijom.

---

## Recommended next run for final thesis numbers

```powershell
python main.py --run-all
```

This enables ML hyperparameter tuning and saves `results/tables/best_params.json`.

Quick debug run:

```powershell
python main.py --quick
```

---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---

## Auto-generated summary

Updated: 2026-05-31 03:26:30

### Top methods overall

| method | average_rank |
| --- | --- |
| linear | 1.00 |

### Best method per factor

| factor | method | mae | rmse | r2 |
| --- | --- | --- | --- | --- |
| 2 | linear | 0.04679600000000002 | 0.07424446107286388 | 0.9995125205998068 |
