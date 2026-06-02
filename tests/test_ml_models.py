"""Tests for ML models."""

import pandas as pd

from src.feature_engineering import build_feature_matrix, get_prediction_rows, get_training_rows
from src.ml_models import reconstruct_with_ml
from src.preprocessing import degrade_series


def test_random_forest_reconstruction(synthetic_dataset):
    degraded = degrade_series(synthetic_dataset["temperature"], factor=2)
    features = build_feature_matrix(synthetic_dataset, degraded.degraded)
    train_mask = pd.Series(True, index=synthetic_dataset.index)
    train_rows = get_training_rows(degraded.degraded, train_mask)
    predict_rows = get_prediction_rows(degraded.degraded)

    reconstructed, params = reconstruct_with_ml(
        "random_forest",
        features,
        degraded.degraded,
        train_rows,
        predict_rows,
        tune=False,
    )
    assert reconstructed.isna().sum() == 0
    assert "n_estimators" in params or "max_depth" in params


def test_mlp_reconstruction(synthetic_dataset):
    degraded = degrade_series(synthetic_dataset["temperature"], factor=2)
    features = build_feature_matrix(synthetic_dataset, degraded.degraded)
    train_mask = pd.Series(True, index=synthetic_dataset.index)
    train_rows = get_training_rows(degraded.degraded, train_mask)
    predict_rows = get_prediction_rows(degraded.degraded)

    reconstructed, params = reconstruct_with_ml(
        "mlp",
        features,
        degraded.degraded,
        train_rows,
        predict_rows,
        tune=False,
    )
    assert reconstructed.isna().sum() == 0
    assert "hidden_layer_sizes" in params
