"""Tests for validation module."""

from pathlib import Path

import pandas as pd
import pytest

from src.config import ALL_METHODS, CLASSICAL_METHODS
from src.validation import (
    ValidationError,
    assert_finite_metrics,
    assert_no_duplicate_index,
    default_factors,
    is_classical_method,
    is_ml_method,
    summarize_dataset_quality,
    validate_dataset_frame,
    validate_degradation_factor,
    validate_factor_list,
    validate_method_list,
    validate_method_name,
    validate_raw_csv_columns,
    validate_raw_file_exists,
    validate_temperature_series,
)


def test_validate_degradation_factor_ok():
    validate_degradation_factor(2)


def test_validate_degradation_factor_invalid():
    with pytest.raises(ValidationError):
        validate_degradation_factor(1)


def test_validate_method_name_ok():
    for method in ALL_METHODS:
        validate_method_name(method)


def test_validate_method_name_invalid():
    with pytest.raises(ValidationError):
        validate_method_name("lstm")


def test_validate_method_list_empty():
    with pytest.raises(ValidationError):
        validate_method_list([])


def test_validate_factor_list():
    validate_factor_list([2, 3, 6])


def test_validate_temperature_series(synthetic_temperature):
    validate_temperature_series(synthetic_temperature)


def test_validate_temperature_series_unsorted(synthetic_temperature):
    series = synthetic_temperature.iloc[::-1].copy()
    with pytest.raises(ValidationError):
        validate_temperature_series(series)


def test_validate_dataset_frame(synthetic_dataset):
    validate_dataset_frame(synthetic_dataset)


def test_validate_dataset_missing_temperature(synthetic_dataset):
    broken = synthetic_dataset.drop(columns=["temperature"])
    with pytest.raises(ValidationError):
        validate_dataset_frame(broken)


def test_validate_raw_file_exists():
    path = validate_raw_file_exists()
    assert path.name.endswith(".csv")


def test_validate_raw_csv_columns():
    checks = validate_raw_csv_columns()
    assert checks["datetime_column"] is True
    assert checks["temperature_column"] is True


def test_summarize_dataset_quality(synthetic_dataset):
    summary = summarize_dataset_quality(synthetic_dataset)
    assert summary["n_rows"] == len(synthetic_dataset)


def test_is_classical_and_ml():
    assert is_classical_method("linear")
    assert not is_ml_method("linear")
    assert is_ml_method("mlp")


def test_default_factors():
    assert 2 in default_factors(quick=True)
    assert 12 in default_factors(quick=False)


def test_assert_no_duplicate_index(synthetic_temperature):
    assert_no_duplicate_index(synthetic_temperature.index)


def test_assert_finite_metrics():
    assert_finite_metrics({"mae": 1.0, "rmse": 2.0, "r2": 0.9})


def test_assert_finite_metrics_invalid():
    with pytest.raises(ValidationError):
        assert_finite_metrics({"mae": -1.0, "rmse": 2.0, "r2": 0.9})
