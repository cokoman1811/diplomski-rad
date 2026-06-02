"""Data quality checks for Jena Climate dataset."""

import pandas as pd

from .config import COVARIATE_COLUMNS, TEMPERATURE_COLUMN
from .validation import ValidationError, validate_dataset_frame


def _temperature_column(dataset: pd.DataFrame) -> str:
    """Return the name of the temperature column."""
    if "temperature" in dataset.columns:
        return "temperature"
    if TEMPERATURE_COLUMN in dataset.columns:
        return TEMPERATURE_COLUMN
    raise ValidationError("Dataset has no temperature column.")


def count_missing_by_column(dataset: pd.DataFrame) -> pd.Series:
    """Count missing values per column."""
    return dataset.isna().sum()


def missing_percentage_by_column(dataset: pd.DataFrame) -> pd.Series:
    """Missing value percentage per column."""
    return dataset.isna().mean() * 100


def detect_large_gaps(index: pd.DatetimeIndex, expected_minutes: int = 10) -> pd.Series:
    """Return time gaps larger than expected sampling interval."""
    deltas = index.to_series().diff().dt.total_seconds().div(60)
    return deltas[deltas > expected_minutes * 1.5]


def detect_duplicate_timestamps(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """Return duplicate timestamps if any exist."""
    duplicated = index[index.duplicated()]
    return duplicated


def temperature_outlier_mask(
    dataset: pd.DataFrame,
    z_threshold: float = 4.0,
) -> pd.Series:
    """Flag temperature outliers using z-score."""
    values = dataset[_temperature_column(dataset)]
    z_scores = (values - values.mean()) / values.std()
    return z_scores.abs() > z_threshold


def covariate_range_report(dataset: pd.DataFrame) -> pd.DataFrame:
    """Min, max and mean for each covariate."""
    rows = []
    for column in COVARIATE_COLUMNS:
        if column not in dataset.columns:
            continue
        series = pd.to_numeric(dataset[column], errors="coerce")
        rows.append({
            "column": column,
            "min": float(series.min()),
            "max": float(series.max()),
            "mean": float(series.mean()),
            "missing_pct": float(series.isna().mean() * 100),
        })
    return pd.DataFrame(rows)


def temperature_range_report(dataset: pd.DataFrame) -> dict:
    """Summary statistics for temperature."""
    series = pd.to_numeric(dataset[_temperature_column(dataset)], errors="coerce")
    return {
        "min": float(series.min()),
        "max": float(series.max()),
        "mean": float(series.mean()),
        "std": float(series.std()),
        "missing_pct": float(series.isna().mean() * 100),
    }


def hourly_coverage(dataset: pd.DataFrame) -> pd.Series:
    """Number of samples per hour of day."""
    return dataset.groupby(dataset.index.hour).size()


def monthly_coverage(dataset: pd.DataFrame) -> pd.Series:
    """Number of samples per month."""
    return dataset.groupby(dataset.index.month).size()


def validate_regular_sampling(dataset: pd.DataFrame, expected_minutes: int = 10) -> dict:
    """Check whether sampling is mostly regular."""
    gaps = detect_large_gaps(dataset.index, expected_minutes)
    return {
        "n_rows": len(dataset),
        "large_gaps": int(len(gaps)),
        "duplicate_timestamps": int(dataset.index.duplicated().sum()),
    }


def full_quality_report(dataset: pd.DataFrame) -> dict:
    """Build a complete data quality report."""
    validate_dataset_frame(dataset)
    return {
        "missing_by_column": count_missing_by_column(dataset).to_dict(),
        "missing_pct_by_column": missing_percentage_by_column(dataset).to_dict(),
        "temperature": temperature_range_report(dataset),
        "covariates": covariate_range_report(dataset).to_dict(orient="records"),
        "sampling": validate_regular_sampling(dataset),
        "hourly_coverage_min": int(hourly_coverage(dataset).min()),
        "hourly_coverage_max": int(hourly_coverage(dataset).max()),
        "monthly_coverage_min": int(monthly_coverage(dataset).min()),
        "monthly_coverage_max": int(monthly_coverage(dataset).max()),
    }


def assert_acceptable_quality(report: dict, max_missing_pct: float = 5.0) -> None:
    """Raise if data quality is below acceptable thresholds."""
    temp_missing = report["temperature"]["missing_pct"]
    if temp_missing > max_missing_pct:
        raise ValidationError(f"Temperature missing pct too high: {temp_missing:.2f}%")
    if report["sampling"]["duplicate_timestamps"] > 0:
        raise ValidationError("Duplicate timestamps detected in dataset.")
