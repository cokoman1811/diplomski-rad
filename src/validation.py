"""Validate datasets and experiment inputs."""

from pathlib import Path

import numpy as np
import pandas as pd

from .config import (
    ALL_METHODS,
    CLASSICAL_METHODS,
    COVARIATE_COLUMNS,
    DEGRADATION_FACTORS,
    JENA_RAW_FILENAME,
    ML_METHODS,
    TEMPERATURE_COLUMN,
)
from .paths import RAW_DIR


class ValidationError(ValueError):
    """Raised when dataset or configuration validation fails."""


def validate_degradation_factor(factor: int) -> None:
    """Check that a degradation factor is valid."""
    if not isinstance(factor, int):
        raise ValidationError(f"Factor must be an integer, got {type(factor)}")
    if factor < 2:
        raise ValidationError(f"Factor must be at least 2, got {factor}")
    if factor > 100:
        raise ValidationError(f"Factor seems unreasonably large: {factor}")


def validate_method_name(method: str) -> None:
    """Check that a method name is registered."""
    if method not in ALL_METHODS:
        raise ValidationError(
            f"Unknown method '{method}'. Valid methods: {', '.join(ALL_METHODS)}"
        )


def validate_method_list(methods: list[str]) -> None:
    """Validate a list of method names."""
    if not methods:
        raise ValidationError("Method list cannot be empty.")
    for method in methods:
        validate_method_name(method)


def validate_factor_list(factors: list[int]) -> None:
    """Validate a list of degradation factors."""
    if not factors:
        raise ValidationError("Factor list cannot be empty.")
    for factor in factors:
        validate_degradation_factor(factor)


def validate_temperature_series(series: pd.Series) -> None:
    """Validate a temperature time series."""
    if not isinstance(series, pd.Series):
        raise ValidationError("Expected a pandas Series.")
    if series.empty:
        raise ValidationError("Temperature series is empty.")
    if not isinstance(series.index, pd.DatetimeIndex):
        raise ValidationError("Temperature series must have a DatetimeIndex.")
    if not series.index.is_monotonic_increasing:
        raise ValidationError("Temperature series index must be sorted ascending.")
    if series.isna().all():
        raise ValidationError("Temperature series contains only missing values.")
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.isna().all():
        raise ValidationError("Temperature values are not numeric.")


def validate_dataset_frame(dataset: pd.DataFrame) -> None:
    """Validate the combined Jena dataset frame."""
    if dataset.empty:
        raise ValidationError("Dataset is empty.")
    if "temperature" not in dataset.columns:
        raise ValidationError("Dataset must contain a 'temperature' column.")
    validate_temperature_series(dataset["temperature"])
    missing_covariates = [col for col in COVARIATE_COLUMNS if col not in dataset.columns]
    if missing_covariates:
        raise ValidationError(f"Missing covariate columns: {missing_covariates}")


def validate_raw_file_exists(raw_dir: Path | None = None) -> Path:
    """Ensure the Jena raw CSV exists and return its path."""
    raw_dir = raw_dir or RAW_DIR
    csv_path = raw_dir / JENA_RAW_FILENAME
    if not csv_path.exists():
        raise ValidationError(
            f"Raw dataset not found at {csv_path}. Run download_jena_climate() first."
        )
    return csv_path


def validate_raw_csv_columns(raw_dir: Path | None = None) -> dict[str, bool]:
    """Check required columns in the raw CSV header."""
    csv_path = validate_raw_file_exists(raw_dir)
    header = pd.read_csv(csv_path, nrows=0).columns.tolist()
    checks = {
        "datetime_column": "Date Time" in header,
        "temperature_column": TEMPERATURE_COLUMN in header,
    }
    for column in COVARIATE_COLUMNS:
        checks[f"covariate_{column}"] = column in header
    return checks


def summarize_dataset_quality(dataset: pd.DataFrame) -> dict:
    """Return basic quality indicators for a dataset."""
    temperature = dataset["temperature"]
    return {
        "n_rows": int(len(dataset)),
        "start": str(dataset.index.min()),
        "end": str(dataset.index.max()),
        "temperature_missing_pct": float(temperature.isna().mean() * 100),
        "temperature_min": float(temperature.min()),
        "temperature_max": float(temperature.max()),
        "temperature_mean": float(temperature.mean()),
        "duplicate_timestamps": int(dataset.index.duplicated().sum()),
    }


def is_classical_method(method: str) -> bool:
    """Return True if the method is classical."""
    return method in CLASSICAL_METHODS


def is_ml_method(method: str) -> bool:
    """Return True if the method uses machine learning."""
    return method in ML_METHODS


def default_factors(quick: bool = False) -> list[int]:
    """Return default degradation factors."""
    from .config import QUICK_DEGRADATION_FACTORS

    return list(QUICK_DEGRADATION_FACTORS if quick else DEGRADATION_FACTORS)


def assert_no_duplicate_index(index: pd.DatetimeIndex) -> None:
    """Raise if datetime index contains duplicates."""
    if index.duplicated().any():
        raise ValidationError("Datetime index contains duplicate timestamps.")


def assert_finite_metrics(metrics: dict) -> None:
    """Raise if computed metrics contain non-finite values unexpectedly."""
    for key in ("mae", "rmse", "r2"):
        value = metrics.get(key)
        if value is None:
            raise ValidationError(f"Missing metric: {key}")
        if key in ("mae", "rmse") and value < 0:
            raise ValidationError(f"{key} cannot be negative.")
        if not np.isfinite(value) and key != "r2":
            raise ValidationError(f"Non-finite metric value for {key}: {value}")
