"""Tests for plotting module."""

import pandas as pd

from src.config import CLASSICAL_METHODS
from src.experiment_runner import ExperimentConfig, run_experiments
from src.plots import (
    plot_all_factor_rankings,
    plot_all_metric_lines,
    plot_error_boxplot,
    plot_error_by_hour,
    plot_error_by_month,
    plot_error_by_season,
    plot_error_by_weekday,
    plot_error_histogram,
    plot_metric_bars,
    plot_metric_heatmap,
    plot_metric_lines,
    plot_method_ranking,
    plot_reconstruction_window,
    plot_residual_scatter,
)
from src.preprocessing import degrade_series


def test_plot_reconstruction_window(tmp_path, synthetic_temperature, monkeypatch):
    monkeypatch.setattr("src.plots.FIGURES_DIR", tmp_path)
    degraded = degrade_series(synthetic_temperature, 2)
    reconstructed = synthetic_temperature.copy()
    path = plot_reconstruction_window(
        degraded.original,
        degraded.degraded,
        reconstructed,
        "linear",
        2,
        window_size=50,
    )
    assert path.exists()


def test_plot_metric_charts(sample_results_table, tmp_path, monkeypatch):
    monkeypatch.setattr("src.plots.FIGURES_DIR", tmp_path)
    assert plot_metric_bars(sample_results_table, "mae").exists()
    assert plot_metric_heatmap(sample_results_table, "mae").exists()
    assert plot_metric_lines(sample_results_table, "mae").exists()


def test_plot_error_charts(synthetic_temperature, tmp_path, monkeypatch):
    monkeypatch.setattr("src.plots.FIGURES_DIR", tmp_path)
    errors = (synthetic_temperature * 0.05).abs()
    assert plot_error_by_hour(errors, "linear", 2).exists()
    assert plot_error_by_month(errors, "linear", 2).exists()
    assert plot_error_by_weekday(errors, "linear", 2).exists()
    assert plot_error_by_season(errors, "linear", 2).exists()
    assert plot_error_histogram(errors, "linear", 2).exists()


def test_plot_ranking_and_boxplot(sample_results_table, tmp_path, monkeypatch):
    monkeypatch.setattr("src.plots.FIGURES_DIR", tmp_path)
    assert plot_method_ranking(sample_results_table, 2).exists()
    frame = pd.DataFrame({"linear": [1, 2, 3], "spline": [2, 3, 4]})
    assert plot_error_boxplot(frame, 2).exists()
    paths = plot_all_factor_rankings(sample_results_table)
    assert len(paths) == 2
    line_paths = plot_all_metric_lines(sample_results_table)
    assert len(line_paths) == 3


def test_plot_residual_scatter(synthetic_temperature, tmp_path, monkeypatch):
    monkeypatch.setattr("src.plots.FIGURES_DIR", tmp_path)
    mask = pd.Series(True, index=synthetic_temperature.index)
    path = plot_residual_scatter(
        synthetic_temperature,
        synthetic_temperature,
        mask,
        "linear",
        2,
    )
    assert path.exists()


def test_quick_run_generates_some_plots(tmp_path, monkeypatch):
    monkeypatch.setattr("src.plots.FIGURES_DIR", tmp_path)
    monkeypatch.setattr("src.io_utils.TABLES_DIR", tmp_path)
    config = ExperimentConfig(
        quick=True,
        factors=[2],
        methods=["linear"],
        tune_ml=False,
        generate_plots=True,
    )
    run_experiments(config)
    assert any(tmp_path.glob("*.png"))
