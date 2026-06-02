"""Tests for feature engineering."""

import pandas as pd

from src.feature_engineering import (
    build_feature_matrix,
    build_train_test_masks,
    get_prediction_rows,
    get_training_rows,
)
from src.preprocessing import degrade_series


def test_build_feature_matrix_shape(synthetic_dataset):
    degraded = degrade_series(synthetic_dataset["temperature"], factor=2)
    features = build_feature_matrix(synthetic_dataset, degraded.degraded)
    assert len(features) == len(synthetic_dataset)
    assert "hour_sin" in features.columns
    assert "lag_1" in features.columns


def test_train_and_prediction_rows(synthetic_dataset):
    degraded = degrade_series(synthetic_dataset["temperature"], factor=2)
    train_mask = pd.Series(True, index=synthetic_dataset.index)
    train_rows = get_training_rows(degraded.degraded, train_mask)
    predict_rows = get_prediction_rows(degraded.degraded)
    assert train_rows.sum() > 0
    assert predict_rows.sum() > 0
