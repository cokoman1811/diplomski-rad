"""Plotting utilities for thesis results."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .paths import FIGURES_DIR, ensure_project_dirs

STANDARD_FIGSIZE = (12, 6)


def _save_figure(path: Path) -> Path:
    """Save and close the current matplotlib figure."""
    ensure_project_dirs()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def plot_reconstruction_window(
    original: pd.Series,
    degraded: pd.Series,
    reconstructed: pd.Series,
    method: str,
    factor: int,
    window_size: int = 500,
) -> Path:
    """Plot original, degraded and reconstructed values for a short window."""
    window = original.iloc[:window_size]
    degraded_window = degraded.iloc[:window_size]
    reconstructed_window = reconstructed.iloc[:window_size]

    plt.figure(figsize=STANDARD_FIGSIZE)
    plt.plot(window.index, window.values, label="Original", linewidth=1.5)
    plt.plot(
        degraded_window.index,
        degraded_window.values,
        "o",
        markersize=3,
        label="Observed after degradation",
    )
    plt.plot(
        reconstructed_window.index,
        reconstructed_window.values,
        label=f"{method} reconstruction",
        linewidth=1.2,
    )
    plt.title(f"Reconstruction comparison (factor={factor}, method={method})")
    plt.xlabel("Time")
    plt.ylabel("Temperature (degC)")
    plt.legend()
    plt.xticks(rotation=30)

    filename = f"reconstruction_factor_{factor}_{method}.png"
    return _save_figure(FIGURES_DIR / filename)


def plot_metric_bars(results: pd.DataFrame, metric: str) -> Path:
    """Bar chart of a metric by method for each degradation factor."""
    methods = results["method"].unique()
    factors = sorted(results["factor"].unique())
    x = np.arange(len(methods))
    width = 0.8 / max(len(factors), 1)

    plt.figure(figsize=STANDARD_FIGSIZE)
    for index, factor in enumerate(factors):
        subset = results[results["factor"] == factor].set_index("method")
        values = [subset.loc[method, metric] if method in subset.index else 0 for method in methods]
        plt.bar(x + index * width, values, width=width, label=f"factor={factor}")

    plt.title(f"{metric.upper()} by method and degradation factor")
    plt.xlabel("Method")
    plt.ylabel(metric.upper())
    plt.xticks(x + width * (len(factors) - 1) / 2, methods, rotation=45, ha="right")
    plt.legend()
    return _save_figure(FIGURES_DIR / f"bar_{metric}.png")


def plot_metric_heatmap(results: pd.DataFrame, metric: str) -> Path:
    """Heatmap of method versus degradation factor."""
    pivot = results.pivot(index="method", columns="factor", values=metric)
    plt.figure(figsize=STANDARD_FIGSIZE)
    plt.imshow(pivot.values, aspect="auto", cmap="YlOrRd")
    plt.colorbar(label=metric.upper())
    plt.xticks(range(len(pivot.columns)), pivot.columns)
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.title(f"{metric.upper()} heatmap")
    plt.xlabel("Degradation factor")
    plt.ylabel("Method")

    for row in range(pivot.shape[0]):
        for col in range(pivot.shape[1]):
            plt.text(col, row, f"{pivot.values[row, col]:.3f}", ha="center", va="center")

    return _save_figure(FIGURES_DIR / f"heatmap_{metric}.png")


def plot_error_boxplot(error_frame: pd.DataFrame, factor: int) -> Path:
    """Boxplot of absolute errors across methods."""
    plt.figure(figsize=STANDARD_FIGSIZE)
    plt.boxplot(
        [error_frame[col].dropna().values for col in error_frame.columns],
        labels=error_frame.columns,
    )
    plt.title(f"Absolute error distribution (factor={factor})")
    plt.xlabel("Method")
    plt.ylabel("Absolute error")
    plt.xticks(rotation=45, ha="right")
    return _save_figure(FIGURES_DIR / f"boxplot_factor_{factor}.png")


def plot_error_by_hour(errors: pd.Series, method: str, factor: int) -> Path:
    """Average absolute error grouped by hour of day."""
    hourly = errors.groupby(errors.index.hour).mean()
    plt.figure(figsize=STANDARD_FIGSIZE)
    plt.plot(hourly.index, hourly.values, marker="o")
    plt.title(f"Mean absolute error by hour (factor={factor}, method={method})")
    plt.xlabel("Hour of day")
    plt.ylabel("Mean absolute error")
    return _save_figure(FIGURES_DIR / f"error_by_hour_factor_{factor}_{method}.png")


def plot_error_by_month(errors: pd.Series, method: str, factor: int) -> Path:
    """Average absolute error grouped by month."""
    monthly = errors.groupby(errors.index.month).mean()
    plt.figure(figsize=STANDARD_FIGSIZE)
    plt.plot(monthly.index, monthly.values, marker="o")
    plt.title(f"Mean absolute error by month (factor={factor}, method={method})")
    plt.xlabel("Month")
    plt.ylabel("Mean absolute error")
    return _save_figure(FIGURES_DIR / f"error_by_month_factor_{factor}_{method}.png")


def plot_residual_scatter(
    original: pd.Series,
    reconstructed: pd.Series,
    mask: pd.Series,
    method: str,
    factor: int,
) -> Path:
    """Scatter plot of predicted versus actual values."""
    y_true = original.loc[mask]
    y_pred = reconstructed.loc[mask]
    plt.figure(figsize=STANDARD_FIGSIZE)
    plt.scatter(y_true, y_pred, alpha=0.3, s=8)
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], "r--", label="Ideal")
    plt.title(f"Actual vs reconstructed (factor={factor}, method={method})")
    plt.xlabel("Actual temperature")
    plt.ylabel("Reconstructed temperature")
    plt.legend()
    return _save_figure(FIGURES_DIR / f"scatter_factor_{factor}_{method}.png")


def plot_error_histogram(errors: pd.Series, method: str, factor: int) -> Path:
    """Histogram of absolute errors."""
    plt.figure(figsize=STANDARD_FIGSIZE)
    plt.hist(errors.dropna(), bins=40, edgecolor="black")
    plt.title(f"Error histogram (factor={factor}, method={method})")
    plt.xlabel("Absolute error")
    plt.ylabel("Frequency")
    return _save_figure(FIGURES_DIR / f"hist_factor_{factor}_{method}.png")


def plot_method_ranking(results: pd.DataFrame, factor: int) -> Path:
    """Horizontal bar chart ranking methods by MAE for one factor."""
    subset = results[results["factor"] == factor].sort_values("mae")
    plt.figure(figsize=STANDARD_FIGSIZE)
    plt.barh(subset["method"], subset["mae"])
    plt.title(f"Method ranking by MAE (factor={factor})")
    plt.xlabel("MAE")
    plt.ylabel("Method")
    return _save_figure(FIGURES_DIR / f"ranking_factor_{factor}.png")


def plot_metric_lines(results: pd.DataFrame, metric: str) -> Path:
    """Line plot showing metric change across factors for each method."""
    plt.figure(figsize=STANDARD_FIGSIZE)
    for method, group in results.groupby("method"):
        ordered = group.sort_values("factor")
        plt.plot(ordered["factor"], ordered[metric], marker="o", label=method)
    plt.title(f"{metric.upper()} vs degradation factor")
    plt.xlabel("Degradation factor")
    plt.ylabel(metric.upper())
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    return _save_figure(FIGURES_DIR / f"lines_{metric}.png")


def plot_error_by_weekday(errors: pd.Series, method: str, factor: int) -> Path:
    """Mean absolute error by weekday."""
    from .analysis import error_by_weekday

    grouped = error_by_weekday(errors)
    plt.figure(figsize=STANDARD_FIGSIZE)
    plt.bar(grouped.index, grouped.values)
    plt.title(f"Mean absolute error by weekday (factor={factor}, method={method})")
    plt.xlabel("Weekday")
    plt.ylabel("Mean absolute error")
    return _save_figure(FIGURES_DIR / f"error_by_weekday_factor_{factor}_{method}.png")


def plot_error_by_season(errors: pd.Series, method: str, factor: int) -> Path:
    """Mean absolute error by season."""
    from .analysis import error_by_season

    grouped = error_by_season(errors)
    plt.figure(figsize=STANDARD_FIGSIZE)
    plt.bar(grouped.index, grouped.values)
    plt.title(f"Mean absolute error by season (factor={factor}, method={method})")
    plt.xlabel("Season")
    plt.ylabel("Mean absolute error")
    return _save_figure(FIGURES_DIR / f"error_by_season_factor_{factor}_{method}.png")


def plot_all_factor_rankings(results: pd.DataFrame) -> list[Path]:
    """Create ranking plots for every factor in the results table."""
    paths = []
    for factor in sorted(results["factor"].unique()):
        paths.append(plot_method_ranking(results, factor))
    return paths


def plot_all_metric_lines(results: pd.DataFrame) -> list[Path]:
    """Create line plots for MAE, RMSE and R2."""
    return [plot_metric_lines(results, metric) for metric in ("mae", "rmse", "r2")]
