# Technical decisions

## Dataset

Decision:
Use the Jena Climate dataset as the main dataset.

Reason:
It contains high-resolution time-series data recorded every 10 minutes, which is suitable for simulating lower temporal resolution.

## Target variable

Decision:
Use temperature as the main target variable.

Reason:
Temperature is intuitive, continuous and easy to visualize.

## Evaluation

Decision:
Evaluate only on artificially removed values.

Reason:
The original values are known, so the reconstruction error can be measured directly.

## Models

Decision:
Use RandomForestRegressor and MLPRegressor as the first machine learning models.

Reason:
They are available in scikit-learn, simple to implement and suitable for a one-month thesis timeline.

## Deep learning

Decision:
Do not use LSTM or Transformer models in the first version.

Reason:
They increase complexity and risk. They can be added later only if the baseline project is finished.
