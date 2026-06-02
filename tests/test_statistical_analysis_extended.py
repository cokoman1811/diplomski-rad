"""Tests for extended statistical analysis."""

import pandas as pd

from src.statistical_analysis_extended import (
    aggregate_significance_by_factor,
    bootstrap_mean_ci,
    compare_all_pairs,
    effect_size_mean_difference,
    kruskal_wallis_test,
    mann_whitney_test,
    method_significance_report,
    paired_t_test,
    significant_pairs,
    summarize_statistical_battery,
)


def _sample_errors():
    return {
        "linear": pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
        "spline": pd.Series([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]),
        "random_forest": pd.Series([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5]),
    }


def test_compare_all_pairs():
    pairs = compare_all_pairs(_sample_errors())
    assert len(pairs) == 3


def test_significant_pairs():
    pairs = compare_all_pairs(_sample_errors())
    significant = significant_pairs(pairs, alpha=0.05)
    assert isinstance(significant, pd.DataFrame)


def test_paired_t_test():
    errors = _sample_errors()
    result = paired_t_test(errors["linear"], errors["spline"])
    assert result["p_value"] is not None


def test_mann_whitney_test():
    errors = _sample_errors()
    result = mann_whitney_test(errors["linear"], errors["spline"])
    assert result["p_value"] is not None


def test_kruskal_wallis_test():
    import pandas as pd

    matrix = pd.DataFrame(_sample_errors())
    result = kruskal_wallis_test(matrix)
    assert result["n_samples"] == 12


def test_effect_size_mean_difference():
    errors = _sample_errors()
    diff = effect_size_mean_difference(errors["linear"], errors["spline"])
    assert diff == -1.0


def test_bootstrap_mean_ci():
    errors = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    ci = bootstrap_mean_ci(errors, n_bootstrap=200)
    assert ci["lower"] <= ci["mean"] <= ci["upper"]


def test_method_significance_report():
    report = method_significance_report(_sample_errors())
    assert "mean_difference" in report.columns


def test_aggregate_significance_by_factor():
    report = aggregate_significance_by_factor({2: _sample_errors(), 6: _sample_errors()})
    assert set(report["factor"]) == {2, 6}


def test_summarize_statistical_battery():
    summary = summarize_statistical_battery(_sample_errors())
    assert "kruskal" in summary
    assert "pairwise" in summary
