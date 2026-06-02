"""Extended evaluation metrics and result summaries."""

import pandas as pd
from sklearn.metrics import explained_variance_score, max_error, median_absolute_error

from .evaluation import compute_metrics, compute_point_errors


def compute_extended_metrics(
    original: pd.Series,
    reconstructed: pd.Series,
    eval_mask: pd.Series,
) -> dict[str, float]:
    """Compute standard and extended regression metrics."""
    base = compute_metrics(original, reconstructed, eval_mask)
    y_true = original.loc[eval_mask]
    y_pred = reconstructed.loc[eval_mask]

    base["median_ae"] = float(median_absolute_error(y_true, y_pred))
    base["max_error"] = float(max_error(y_true, y_pred))
    base["explained_variance"] = float(explained_variance_score(y_true, y_pred))
    base["bias"] = float((y_pred - y_true).mean())
    return base


def compute_signed_errors(
    original: pd.Series,
    reconstructed: pd.Series,
    eval_mask: pd.Series,
) -> pd.Series:
    """Return signed prediction errors on the evaluation mask."""
    return (reconstructed - original).loc[eval_mask]


def compute_absolute_errors(
    original: pd.Series,
    reconstructed: pd.Series,
    eval_mask: pd.Series,
) -> pd.Series:
    """Return absolute errors on the evaluation mask."""
    return compute_point_errors(original, reconstructed, eval_mask)


def summarize_metrics_by_method(results: pd.DataFrame) -> pd.DataFrame:
    """Aggregate MAE, RMSE and R2 by method across factors."""
    return results.groupby("method")[["mae", "rmse", "r2"]].agg(["mean", "std", "min", "max"])


def summarize_metrics_by_factor(results: pd.DataFrame) -> pd.DataFrame:
    """Aggregate MAE, RMSE and R2 by factor across methods."""
    return results.groupby("factor")[["mae", "rmse", "r2"]].agg(["mean", "std", "min", "max"])


def worst_cases(
    original: pd.Series,
    reconstructed: pd.Series,
    eval_mask: pd.Series,
    n: int = 10,
) -> pd.DataFrame:
    """Return the largest absolute errors."""
    errors = compute_absolute_errors(original, reconstructed, eval_mask)
    worst = errors.sort_values(ascending=False).head(n)
    frame = pd.DataFrame({
        "timestamp": worst.index,
        "abs_error": worst.values,
        "actual": original.loc[worst.index].values,
        "predicted": reconstructed.loc[worst.index].values,
    })
    return frame


def metric_improvement_over_baseline(
    results: pd.DataFrame,
    baseline: str = "forward_fill",
    metric: str = "mae",
) -> pd.DataFrame:
    """Compute improvement relative to a baseline method."""
    rows = []
    for factor, group in results.groupby("factor"):
        baseline_value = group[group["method"] == baseline].iloc[0][metric]
        for _, row in group.iterrows():
            rows.append({
                "factor": factor,
                "method": row["method"],
                metric: row[metric],
                "baseline": baseline,
                f"baseline_{metric}": baseline_value,
                "improvement": baseline_value - row[metric],
                "relative_improvement_pct": (baseline_value - row[metric]) / baseline_value * 100,
            })
    return pd.DataFrame(rows)


def filter_results(
    results: pd.DataFrame,
    methods: list[str] | None = None,
    factors: list[int] | None = None,
) -> pd.DataFrame:
    """Filter a results table by methods and factors."""
    frame = results.copy()
    if methods is not None:
        frame = frame[frame["method"].isin(methods)]
    if factors is not None:
        frame = frame[frame["factor"].isin(factors)]
    return frame.reset_index(drop=True)


def top_n_methods(results: pd.DataFrame, metric: str = "mae", n: int = 3) -> pd.DataFrame:
    """Return top n methods per factor by a metric."""
    rows = []
    for factor, group in results.groupby("factor"):
        top = group.sort_values(metric).head(n)
        for rank, (_, row) in enumerate(top.iterrows(), start=1):
            rows.append({
                "factor": factor,
                "rank": rank,
                "method": row["method"],
                metric: row[metric],
            })
    return pd.DataFrame(rows)
