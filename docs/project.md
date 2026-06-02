# Project documentation

## Thesis title

**Interpolacija podataka pomoću strojnog učenja**

English title:

**Data interpolation using machine learning**

---

## Project overview

This project is a master's thesis project focused on interpolation of time-series data using machine learning.

The main goal is to compare classical interpolation methods with machine learning methods for reconstructing missing values in high-resolution time-series data.

The project uses an experimental approach where original data is artificially degraded by removing intermediate values. These removed values are then reconstructed using different methods, and the results are compared with the original known values.

---

## Main goal

The goal of this thesis is to investigate how well different methods can reconstruct missing values in time-series data.

The project compares:

- classical interpolation methods
- machine learning methods

The final goal is to determine which methods provide better reconstruction accuracy under different levels of temporal degradation.

---

## Research idea

The original dataset contains measurements recorded at a high temporal resolution.

To simulate lower temporal resolution, only every nth value is kept, while the values between them are removed and treated as missing.

After that, different interpolation and machine learning methods are used to reconstruct the missing values.

The reconstructed values are compared with the original values using evaluation metrics.

---

## Dataset

The main dataset used in this project is the **Jena Climate dataset**.

The Jena Climate dataset contains meteorological measurements recorded every 10 minutes.

It is suitable for this thesis because:

- it contains high-resolution time-series data
- it has regular time intervals
- it contains continuous numerical variables
- it is easy to use for interpolation experiments
- removed values can be compared with known original values

---

## Target variable

The main target variable is:

**Temperature**

Temperature is selected because it is:

- continuous
- intuitive
- easy to visualize
- suitable for interpolation
- useful for comparing reconstruction methods

---

## Main experiment

The experiment follows these steps:

1. Load the original high-resolution time-series dataset.
2. Select temperature as the target variable.
3. Artificially degrade the time series by keeping only every nth value.
4. Treat removed values as missing values.
5. Reconstruct missing values using classical interpolation methods.
6. Reconstruct missing values using machine learning methods.
7. Compare reconstructed values with the original values.
8. Evaluate results using MAE, RMSE and R2.
9. Save result tables and plots for the thesis.

---

## Degradation factors

The planned degradation factors are:

- 2
- 3
- 6
- 12

Example:

If the original data is recorded every 10 minutes, then factor 6 simulates data recorded every 60 minutes.

---

## Classical interpolation methods

The classical interpolation methods used in this project are:

- forward fill
- linear interpolation
- time interpolation
- cubic interpolation
- spline interpolation

These methods serve as baseline methods for comparison.

---

## Machine learning methods

The machine learning methods used in this project are:

- RandomForestRegressor
- MLPRegressor

These models are selected because they are available in scikit-learn, relatively simple to implement, and suitable for a one-month thesis timeline.

Deep learning models such as LSTM or Transformer models are not included in the first version of the project because they increase complexity and development risk.

---

## Evaluation metrics

The reconstruction quality is evaluated using:

- MAE
- RMSE
- R2 score

Evaluation is performed only on values that were artificially removed.

This is important because the original values are known, so the reconstruction error can be measured directly.

---

## Expected outputs

The project should produce:

- cleaned time-series data
- degraded time-series data
- reconstructed time-series data
- result tables in CSV format
- comparison plots
- evaluation metrics
- notes for thesis writing
- final discussion about method performance

---

## Expected result discussion

The final thesis should discuss:

- which method performs best
- how errors change when temporal resolution decreases
- when simple interpolation is sufficient
- when machine learning methods are useful
- limitations of the experiment
- possible improvements for future work

---

## Scope limitation

The first version of the project should stay simple and focused.

Do not add:

- multiple datasets
- GUI
- web application
- database
- Docker
- LSTM
- Transformer
- TensorFlow
- PyTorch

unless the baseline version is fully completed first.

The main priority is to finish a clean, understandable and defensible master's thesis project.