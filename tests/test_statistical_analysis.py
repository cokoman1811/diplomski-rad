"""Tests for statistical analysis."""

import pandas as pd

from src.statistical_analysis import (
    build_error_matrix,
    compare_methods_for_factor,
    compare_two_methods,
    friedman_test,
    summarize_errors,
)


def test_summarize_errors():
    errors = pd.Series([1.0, 2.0, 3.0, 4.0])
    summary = summarize_errors(errors)
    assert summary["mean_abs_error"] == 2.5
    assert summary["max_abs_error"] == 4.0


def test_compare_two_methods():
    errors_a = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0])
    errors_b = pd.Series([2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0])
    result = compare_two_methods(errors_a, errors_b)
    assert result["p_value"] is not None


def test_friedman_and_wilcoxon_tables():
    errors = {
        "linear": pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]),
        "spline": pd.Series([1.5, 2.5, 3.5, 4.5, 5.5, 6.5]),
        "random_forest": pd.Series([0.8, 1.8, 2.8, 3.8, 4.8, 5.8]),
    }
    matrix = build_error_matrix(errors)
    friedman = friedman_test(matrix)
    assert friedman["n_samples"] == 6
    comparison = compare_methods_for_factor(errors, baseline_method="linear")
    assert len(comparison) == 2
