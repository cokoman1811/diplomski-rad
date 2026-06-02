# AGENTS.md

## Project role

You are an AI coding assistant helping with a master's thesis project.

The project topic is:

**Interpolacija podataka pomoću strojnog učenja**

English title:

**Data interpolation using machine learning**

Your job is to help with:
- Python code
- project structure
- documentation
- experiment design
- debugging
- result analysis
- thesis writing notes

Do not make large changes without explaining the plan first.

---

## Project overview

This project compares classical interpolation methods and machine learning methods for reconstructing missing values in time-series data.

The main idea is:

1. Load high-resolution time-series data.
2. Artificially reduce temporal resolution by keeping only every nth value.
3. Treat removed values as missing.
4. Reconstruct missing values using interpolation and machine learning.
5. Compare methods using evaluation metrics.
6. Save result tables and plots for the thesis.

---

## Dataset

Main dataset:

**Jena Climate dataset**

Reason for using it:

- It contains high-resolution meteorological time-series data.
- Measurements are recorded every 10 minutes.
- It is suitable for simulating lower temporal resolution.
- Temperature is continuous and easy to visualize.

Main target variable:

**Temperature**

---

## Methods

Classical interpolation methods:

- forward fill
- linear interpolation
- time interpolation
- cubic interpolation
- spline interpolation

Machine learning methods:

- RandomForestRegressor
- MLPRegressor

Do not add LSTM, Transformer, TensorFlow or PyTorch unless explicitly requested.

---

## Evaluation metrics

Use:

- MAE
- RMSE
- R2 score

Important rule:

Evaluation must be performed only on values that were artificially removed.

Do not evaluate on the full series unless explicitly requested.

---

## Important project documentation

Before making any changes, always read these files:

- `docs/project.md`
- `docs/style.md`
- `docs/workflow.md`
- `docs/progress.md`
- `docs/decisions.md`

If these files do not exist, suggest creating them.

---

## Coding rules

Follow these rules when writing code:

- Use Python.
- Use pandas, numpy, scikit-learn, scipy and matplotlib.
- Keep code simple and readable.
- Use English for code, variable names, function names and comments.
- Use short docstrings for all important functions.
- Prefer simple functions over complex abstractions.
- Do not create a GUI.
- Do not add unnecessary frameworks.
- Do not over-engineer the project.
- Do not rewrite the whole project unless explicitly asked.
- Work on one file or one small task at a time.

---

## Folder rules

Expected project structure:

```text
diplomski rad/
├── AGENTS.md
├── docs/
│   ├── project.md
│   ├── style.md
│   ├── workflow.md
│   ├── progress.md
│   └── decisions.md
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