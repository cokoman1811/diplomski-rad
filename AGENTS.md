# AGENTS.md

## Project overview

This is a master's thesis project about interpolation of time-series data using machine learning.

Thesis topic:
Interpolacija podataka pomoću strojnog učenja.

The goal is to compare classical interpolation methods and machine learning methods for reconstructing artificially removed values from high-resolution time-series data.

## Main experiment

1. Load high-resolution time-series data.
2. Artificially degrade the data by keeping only every nth value.
3. Treat removed values as missing.
4. Reconstruct missing values using interpolation and machine learning.
5. Compare methods using MAE, RMSE and R2.
6. Save result tables and figures.

## Dataset

Main dataset:
Jena Climate dataset.

Main target variable:
Temperature.

## Important docs

Before making changes, always read:

- docs/project.md
- docs/style.md
- docs/workflow.md
- docs/progress.md
- docs/decisions.md

## Coding rules

- Keep code simple and readable.
- Use pandas, numpy, scikit-learn, scipy and matplotlib.
- Do not add unnecessary frameworks.
- Do not use deep learning libraries unless explicitly requested.
- Do not create a GUI.
- Write short docstrings for functions.
- Save result tables in results/tables/.
- Save figures in results/figures/.
- Do not commit or push unless explicitly asked.

## Git rules

- Never add .venv/ to git.
- Never add data/raw/ to git.
- Never add data/processed/ to git.
- Never add cache files.
- Before suggesting a commit, check git status.
- Use small commits with clear messages.

## Documentation rule

After every important code change, update the relevant file in docs/.

Examples:
- If project goal changes, update docs/project.md.
- If code style changes, update docs/style.md.
- If workflow changes, update docs/workflow.md.
- If a task is completed, update docs/progress.md.
- If a technical decision is made, update docs/decisions.md.
