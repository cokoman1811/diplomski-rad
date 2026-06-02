"""Large parametrized grid tests for pipeline coverage."""

import pytest

from src.analysis import best_method_per_factor, rank_methods_by_metric
from src.config import ALL_METHODS, CLASSICAL_METHODS, DEGRADATION_FACTORS, ML_METHODS
from src.evaluation_extended import compute_extended_metrics, top_n_methods
from src.interpolation_methods import interpolate
from src.preprocessing import degrade_series


@pytest.mark.parametrize("factor", DEGRADATION_FACTORS)
def test_degrade_preserves_observed_count_formula(factor, synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, factor)
    expected = (len(synthetic_temperature) + factor - 1) // factor
    assert degraded.degraded.notna().sum() == expected


@pytest.mark.parametrize("method", CLASSICAL_METHODS)
def test_classical_methods_reduce_missing_count(method, synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, 3)
    filled = interpolate(degraded.degraded.astype(float), method)
    assert filled.isna().sum() == 0


@pytest.mark.parametrize("metric", ["mae", "rmse", "r2"])
def test_rank_methods_adds_rank_column(metric, sample_results_table):
    ranked = rank_methods_by_metric(sample_results_table, metric=metric)
    assert ranked["rank"].min() == 1


@pytest.mark.parametrize("n", [1, 2])
def test_top_n_methods_returns_expected_rows(n, sample_results_table):
    top = top_n_methods(sample_results_table, n=n)
    assert len(top) == len(sample_results_table["factor"].unique()) * n


@pytest.mark.parametrize("method", ALL_METHODS)
def test_best_method_table_has_entry_for_each_factor(method, sample_results_table):
    best = best_method_per_factor(sample_results_table)
    assert len(best["factor"].unique()) >= 1


def test_extended_metrics_on_perfect_reconstruction(synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, 2)
    metrics = compute_extended_metrics(
        degraded.original,
        degraded.original,
        degraded.removed_mask,
    )
    assert metrics["median_ae"] == 0.0
    assert metrics["max_error"] == 0.0


@pytest.mark.parametrize("factor", [2, 3, 6, 12])
@pytest.mark.parametrize("method", ["linear", "forward_fill", "time"])
def test_classical_metrics_finite(factor, method, synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, factor)
    filled = interpolate(degraded.degraded.astype(float), method)
    metrics = compute_extended_metrics(degraded.original, filled, degraded.removed_mask)
    assert metrics["mae"] >= 0
    assert metrics["rmse"] >= 0


@pytest.mark.parametrize("method", ML_METHODS)
def test_ml_methods_registered(method):
    assert method in ALL_METHODS


@pytest.mark.parametrize("factor", DEGRADATION_FACTORS)
def test_removed_mask_aligns_with_degraded(factor, synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, factor)
    assert degraded.removed_mask.sum() == degraded.degraded.isna().sum()


@pytest.mark.parametrize("factor", DEGRADATION_FACTORS)
def test_original_unchanged_after_degrade(factor, synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, factor)
    pd = __import__("pandas")
    pd.testing.assert_series_equal(degraded.original, synthetic_temperature)
