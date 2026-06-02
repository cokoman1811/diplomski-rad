"""Tests for hyperparameter tuning."""

import pandas as pd

from src.feature_engineering import build_feature_matrix
from src.hyperparameter_tuning import tune_mlp, tune_random_forest
from src.preprocessing import degrade_series


def test_tune_random_forest(synthetic_dataset):
    degraded = degrade_series(synthetic_dataset["temperature"], 2)
    features = build_feature_matrix(synthetic_dataset, degraded.degraded)
    train_mask = pd.Series(True, index=synthetic_dataset.index)
    train_rows = degraded.degraded.notna() & train_mask
    params = tune_random_forest(features.loc[train_rows], degraded.degraded.loc[train_rows])
    assert "n_estimators" in params
    assert "max_depth" in params


def test_tune_mlp(synthetic_dataset):
    degraded = degrade_series(synthetic_dataset["temperature"], 2)
    features = build_feature_matrix(synthetic_dataset, degraded.degraded)
    train_mask = pd.Series(True, index=synthetic_dataset.index)
    train_rows = degraded.degraded.notna() & train_mask
    params = tune_mlp(features.loc[train_rows], degraded.degraded.loc[train_rows])
    assert "hidden_layer_sizes" in params
    assert "alpha" in params
