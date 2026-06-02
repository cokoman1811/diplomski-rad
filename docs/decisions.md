# Technical decisions

## Purpose

This file contains the main technical decisions made during the project.

The goal is to keep track of why certain datasets, methods, tools and limitations were chosen.

---

## Decision 1 — Dataset

### Decision

Use the **Jena Climate dataset** as the main dataset.

### Reason

The Jena Climate dataset contains high-resolution meteorological time-series data recorded every 10 minutes.

It is suitable for this thesis because:

- it contains regular time-series measurements
- it has continuous numerical variables
- it is easy to use for interpolation experiments
- it allows simulation of lower temporal resolution
- original values are known, so reconstruction error can be measured directly

### Status

Accepted.

---

## Decision 2 — Target variable

### Decision

Use **temperature** as the main target variable.

### Reason

Temperature is selected because it is:

- continuous
- intuitive
- easy to visualize
- suitable for interpolation
- understandable in the thesis discussion

Using one main variable keeps the project simple and focused.

### Status

Accepted.

---

## Decision 3 — Main experiment design

### Decision

The main experiment will artificially remove values from the original high-resolution time series.

Only every nth value will be kept, while the values between them will be treated as missing.

### Reason

This approach allows direct evaluation because the removed values are still known from the original dataset.

The reconstructed values can be compared with the original values using error metrics.

### Status

Accepted.

---

## Decision 4 — Degradation factors

### Decision

Use the following degradation factors:

- 2
- 3
- 6
- 12

### Reason

These factors simulate different levels of temporal resolution reduction.

For example, if the original data is recorded every 10 minutes:

- factor 2 simulates 20-minute resolution
- factor 3 simulates 30-minute resolution
- factor 6 simulates 60-minute resolution
- factor 12 simulates 120-minute resolution

This allows comparison of method performance under different missing-value conditions.

### Status

Accepted.

---

## Decision 5 — Evaluation strategy

### Decision

Evaluate reconstruction quality only on artificially removed values.

### Reason

The goal is to measure how accurately each method reconstructs missing values.

Evaluating only on removed values gives a fair comparison because those are the values that each method had to reconstruct.

### Status

Accepted.

---

## Decision 6 — Evaluation metrics

### Decision

Use these metrics:

- MAE
- RMSE
- R2 score

### Reason

These metrics provide different views of reconstruction quality.

MAE measures average absolute error.

RMSE gives more weight to larger errors.

R2 shows how well reconstructed values explain the variation in the original values.

### Status

Accepted.

---

## Decision 7 — Classical interpolation methods

### Decision

Use these classical interpolation methods:

- forward fill
- linear interpolation
- time interpolation
- cubic interpolation
- spline interpolation

### Reason

These methods are standard baseline approaches for missing-value reconstruction in time-series data.

They are simple, fast and easy to explain in a master's thesis.

They also provide a useful comparison point for machine learning methods.

### Status

Accepted.

---

## Decision 8 — Machine learning methods

### Decision

Use these machine learning models:

- RandomForestRegressor
- MLPRegressor

### Reason

Both models are available in scikit-learn and are suitable for a focused one-month thesis implementation.

Random Forest is stable, robust and usually performs well with limited tuning.

MLPRegressor provides a simple neural-network-based method without requiring TensorFlow or PyTorch.

### Status

Accepted.

---

## Decision 9 — No deep learning in the first version

### Decision

Do not use LSTM, Transformer, TensorFlow or PyTorch in the first version of the project.

### Reason

Deep learning models increase complexity and development risk.

The main priority is to complete a clean, working and defensible baseline version of the thesis.

Deep learning models can be added later only if the baseline version is finished.

### Status

Accepted.

---

## Decision 10 — Python libraries

### Decision

Use the following main Python libraries:

- pandas
- numpy
- scikit-learn
- scipy
- matplotlib
- jupyter

### Reason

These libraries are sufficient for:

- loading and processing time-series data
- implementing interpolation methods
- training simple machine learning models
- calculating metrics
- creating plots

They are also common and easy to explain in the thesis.

### Status

Accepted.

---

## Decision 11 — Project structure

### Decision

Use the following project structure:

```text
diplomski rad/
├── AGENTS.md
├── docs/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── results/
│   ├── figures/
│   └── tables/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

---

## Decision 12 — Covariates for machine learning

### Decision

Use Jena covariates `p (mbar)`, `rh (%)`, `wv (m/s)` and `max. wv (m/s)` as additional ML features.

### Reason

These variables are measured at the same timestamps as temperature and may improve ML reconstruction without changing the classical baseline setup.

### Status

Accepted.

---

## Decision 13 — Temporal train/test split

### Decision

Train ML models on observed values from 2009–2014 and evaluate reconstruction on removed values from 2015–2016.

### Reason

This tests whether models generalize to a later period instead of only memorizing the training years.

### Status

Accepted.

---

## Decision 14 — Hyperparameter tuning

### Decision

Use `GridSearchCV` with `TimeSeriesSplit` for Random Forest and MLP hyperparameter selection.

### Reason

This avoids arbitrary default parameters and makes the ML comparison more defensible in the thesis.

### Status

Accepted.

---

## Decision 15 — Statistical comparison

### Decision

Compare methods using Wilcoxon signed-rank tests against a linear baseline and Friedman tests across methods.

### Reason

Metric tables alone do not show whether differences are statistically meaningful.

### Status

Accepted.

---

## Decision 16 — HTML report viewer

### Decision

After each experiment run, generate a static HTML report at `results/report.html` with result tables, a figure gallery and CSV links. Optionally open it in the browser with `--open-report`.

### Reason

This provides a simple way to explore reconstruction results and figures without building a desktop GUI or web application backend.

### Status

Accepted.