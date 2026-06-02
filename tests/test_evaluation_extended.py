"""Tests for extended evaluation metrics."""

import pandas as pd
import pytest

from src.evaluation_extended import (
    compute_absolute_errors,
    compute_extended_metrics,
    compute_signed_errors,
    filter_results,
    metric_improvement_over_baseline,
    summarize_metrics_by_factor,
    summarize_metrics_by_method,
    top_n_methods,
    worst_cases,
)
from src.preprocessing import degrade_series


def test_compute_extended_metrics(synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, 2)
    reconstructed = degraded.original.copy()
    mask = degraded.removed_mask
    metrics = compute_extended_metrics(degraded.original, reconstructed, mask)
    assert metrics["mae"] == 0.0
    assert "median_ae" in metrics
    assert "max_error" in metrics


def test_signed_and_absolute_errors(synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, 2)
    reconstructed = degraded.original.copy()
    removed_index = degraded.removed_mask[degraded.removed_mask].index[:5]
    reconstructed.loc[removed_index] = reconstructed.loc[removed_index] + 0.1
    mask = degraded.removed_mask
    signed = compute_signed_errors(degraded.original, reconstructed, mask)
    absolute = compute_absolute_errors(degraded.original, reconstructed, mask)
    assert signed.loc[removed_index[0]] == pytest.approx(0.1)
    assert absolute.loc[removed_index[0]] == pytest.approx(0.1)


def test_worst_cases(synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, 2)
    reconstructed = degraded.original.copy()
    reconstructed.iloc[0] += 5
    frame = worst_cases(degraded.original, reconstructed, degraded.removed_mask, n=5)
    assert len(frame) <= 5


def test_summaries(sample_results_table):
    by_method = summarize_metrics_by_method(sample_results_table)
    by_factor = summarize_metrics_by_factor(sample_results_table)
    assert "mae" in str(by_method.columns)
    assert "rmse" in str(by_factor.columns)


def test_metric_improvement(sample_results_table):
    frame = metric_improvement_over_baseline(sample_results_table, baseline="random_forest")
    assert "improvement" in frame.columns


def test_filter_and_top_n(sample_results_table):
    filtered = filter_results(sample_results_table, methods=["linear"], factors=[2])
    assert len(filtered) == 1
    top = top_n_methods(sample_results_table, n=1)
    assert len(top) == 2
