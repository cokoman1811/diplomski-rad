"""Tests for analysis module."""

import pandas as pd
import pytest

from src.analysis import (
    aggregate_error_profiles,
    best_method_per_factor,
    build_method_leaderboard,
    classical_ml_gap,
    compare_classical_vs_ml,
    compute_bias,
    compute_error_quantiles,
    compute_mape,
    degradation_impact_table,
    error_by_season,
    error_by_weekday,
    error_by_year,
    find_methods_beating_baseline,
    method_stability_score,
    pivot_results,
    rank_methods_by_metric,
)
from src.config import CLASSICAL_METHODS


@pytest.fixture
def sample_results():
    """Small results table for analysis tests."""
    return pd.DataFrame([
        {"factor": 2, "method": "linear", "mae": 0.1, "rmse": 0.2, "r2": 0.99, "n_samples": 100},
        {"factor": 2, "method": "spline", "mae": 0.5, "rmse": 0.6, "r2": 0.90, "n_samples": 100},
        {"factor": 2, "method": "random_forest", "mae": 0.2, "rmse": 0.3, "r2": 0.95, "n_samples": 100},
        {"factor": 6, "method": "linear", "mae": 0.3, "rmse": 0.4, "r2": 0.95, "n_samples": 200},
        {"factor": 6, "method": "spline", "mae": 0.8, "rmse": 0.9, "r2": 0.80, "n_samples": 200},
        {"factor": 6, "method": "random_forest", "mae": 0.4, "rmse": 0.5, "r2": 0.90, "n_samples": 200},
    ])


def test_rank_methods_by_metric(sample_results):
    ranked = rank_methods_by_metric(sample_results)
    assert "rank" in ranked.columns
    assert ranked.loc[ranked["method"] == "linear", "rank"].min() == 1


def test_best_method_per_factor(sample_results):
    best = best_method_per_factor(sample_results)
    assert len(best) == 2
    assert all(best["method"] == "linear")


def test_compare_classical_vs_ml(sample_results):
    summary = compare_classical_vs_ml(sample_results)
    assert set(summary["group"]) <= {"classical", "ml"}


def test_build_method_leaderboard(sample_results):
    board = build_method_leaderboard(sample_results)
    assert board.iloc[0]["method"] == "linear"


def test_method_stability_score(sample_results):
    stability = method_stability_score(sample_results)
    assert "std" in stability.columns


def test_pivot_results(sample_results):
    pivot = pivot_results(sample_results)
    assert pivot.loc["linear", 2] == pytest.approx(0.1)


def test_find_methods_beating_baseline(sample_results):
    winners = find_methods_beating_baseline(sample_results, baseline="spline")
    assert not winners.empty


def test_degradation_impact_table(sample_results):
    table = degradation_impact_table(sample_results, "linear")
    assert "mae_ratio_vs_factor_2" in table.columns


def test_classical_ml_gap(sample_results):
    gap = classical_ml_gap(sample_results)
    assert not gap.empty


def test_error_by_weekday(synthetic_temperature):
    errors = (synthetic_temperature * 0.01).abs()
    grouped = error_by_weekday(errors)
    assert len(grouped) <= 7


def test_error_by_season(synthetic_temperature):
    errors = (synthetic_temperature * 0.01).abs()
    grouped = error_by_season(errors)
    assert len(grouped) >= 1


def test_error_by_year(synthetic_temperature):
    errors = (synthetic_temperature * 0.01).abs()
    grouped = error_by_year(errors)
    assert len(grouped) >= 1


def test_compute_bias_and_mape(synthetic_temperature):
    mask = pd.Series(True, index=synthetic_temperature.index)
    bias = compute_bias(synthetic_temperature, synthetic_temperature + 0.1, mask)
    mape = compute_mape(synthetic_temperature, synthetic_temperature, mask)
    assert bias == pytest.approx(0.1)
    assert mape == pytest.approx(0.0)


def test_compute_error_quantiles():
    errors = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    quantiles = compute_error_quantiles(errors)
    assert quantiles["q50"] == 5.5


def test_aggregate_error_profiles():
    frame = pd.DataFrame({"linear": [1.0, 2.0], "spline": [2.0, 3.0]})
    profile = aggregate_error_profiles({2: frame})
    assert len(profile) == 2
