"""Tests for data quality module."""

import pandas as pd
import pytest

from src.data_loader import load_jena_dataset
from src.data_quality import (
    assert_acceptable_quality,
    count_missing_by_column,
    covariate_range_report,
    detect_large_gaps,
    full_quality_report,
    hourly_coverage,
    missing_percentage_by_column,
    monthly_coverage,
    temperature_outlier_mask,
    temperature_range_report,
    validate_regular_sampling,
)
from src.preprocessing import slice_dataset_recent


def test_missing_counts_synthetic(synthetic_dataset):
    counts = count_missing_by_column(synthetic_dataset)
    assert counts["temperature"] == 0


def test_missing_percentage_synthetic(synthetic_dataset):
    pct = missing_percentage_by_column(synthetic_dataset)
    assert pct["temperature"] == 0.0


def test_detect_large_gaps_synthetic(synthetic_temperature):
    gaps = detect_large_gaps(synthetic_temperature.index, expected_minutes=10)
    assert len(gaps) == 0


def test_temperature_range_report(synthetic_dataset):
    report = temperature_range_report(synthetic_dataset)
    assert "min" in report
    assert report["max"] >= report["min"]


def test_covariate_range_report(synthetic_dataset):
    report = covariate_range_report(synthetic_dataset)
    assert len(report) == 4


def test_hourly_and_monthly_coverage(synthetic_dataset):
    assert len(hourly_coverage(synthetic_dataset)) >= 1
    assert len(monthly_coverage(synthetic_dataset)) >= 1


def test_validate_regular_sampling(synthetic_dataset):
    report = validate_regular_sampling(synthetic_dataset)
    assert report["duplicate_timestamps"] == 0


def test_temperature_outlier_mask(synthetic_dataset):
    mask = temperature_outlier_mask(synthetic_dataset)
    assert isinstance(mask, pd.Series)


def test_full_quality_report_jena_slice():
    dataset = slice_dataset_recent(load_jena_dataset(), 5000)
    report = full_quality_report(dataset)
    assert_acceptable_quality(report)
    assert "temperature" in report


def test_full_quality_report_synthetic(synthetic_dataset):
    report = full_quality_report(synthetic_dataset)
    assert_acceptable_quality(report)
