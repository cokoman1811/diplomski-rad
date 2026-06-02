"""Tests for evaluation metrics."""

import pandas as pd

from src.evaluation import aggregate_results, compute_metrics, compute_point_errors
from src.preprocessing import degrade_series


def test_compute_metrics_perfect_reconstruction(synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, factor=2)
    metrics = compute_metrics(
        degraded.original,
        degraded.original,
        degraded.removed_mask,
    )
    assert metrics["mae"] == 0.0
    assert metrics["rmse"] == 0.0
    assert metrics["r2"] == 1.0


def test_compute_point_errors(synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, factor=2)
    reconstructed = degraded.original.copy()
    errors = compute_point_errors(
        degraded.original,
        reconstructed,
        degraded.removed_mask,
    )
    assert (errors == 0).all()


def test_aggregate_results_sorting():
    results = [
        {"factor": 6, "method": "linear", "mae": 1.0},
        {"factor": 2, "method": "spline", "mae": 0.5},
    ]
    frame = aggregate_results(results)
    assert frame.iloc[0]["factor"] == 2
