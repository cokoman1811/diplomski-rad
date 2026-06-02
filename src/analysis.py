"""Extended error and performance analysis for thesis results."""

import pandas as pd

from .config import CLASSICAL_METHODS, ML_METHODS


def rank_methods_by_metric(results: pd.DataFrame, metric: str = "mae") -> pd.DataFrame:
    """Rank methods within each degradation factor by a metric."""
    ranked = results.copy()
    ranked["rank"] = ranked.groupby("factor")[metric].rank(method="min")
    return ranked.sort_values(["factor", "rank", "method"]).reset_index(drop=True)


def best_method_per_factor(results: pd.DataFrame, metric: str = "mae") -> pd.DataFrame:
    """Return the best method for each factor."""
    rows = []
    for factor, group in results.groupby("factor"):
        best = group.sort_values(metric).iloc[0]
        rows.append({
            "factor": factor,
            "method": best["method"],
            metric: best[metric],
            "rmse": best["rmse"],
            "r2": best["r2"],
        })
    return pd.DataFrame(rows)


def compare_classical_vs_ml(results: pd.DataFrame, metric: str = "mae") -> pd.DataFrame:
    """Compare average metric between classical and ML method groups."""
    frame = results.copy()
    frame["group"] = frame["method"].apply(
        lambda name: "classical" if name in CLASSICAL_METHODS else "ml"
    )
    summary = frame.groupby(["factor", "group"])[metric].agg(["mean", "min", "max"]).reset_index()
    return summary


def error_by_weekday(errors: pd.Series) -> pd.Series:
    """Mean absolute error grouped by weekday."""
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    grouped = errors.groupby(errors.index.weekday).mean()
    grouped.index = [names[i] for i in grouped.index]
    return grouped


def error_by_season(errors: pd.Series) -> pd.Series:
    """Mean absolute error grouped by meteorological season."""
    month = errors.index.month

    def season(m: int) -> str:
        if m in (12, 1, 2):
            return "winter"
        if m in (3, 4, 5):
            return "spring"
        if m in (6, 7, 8):
            return "summer"
        return "autumn"

    seasons = pd.Series([season(m) for m in month], index=errors.index)
    return errors.groupby(seasons).mean()


def error_by_year(errors: pd.Series) -> pd.Series:
    """Mean absolute error grouped by calendar year."""
    return errors.groupby(errors.index.year).mean()


def compute_bias(original: pd.Series, reconstructed: pd.Series, mask: pd.Series) -> float:
    """Mean signed error (reconstructed minus original)."""
    diff = reconstructed.loc[mask] - original.loc[mask]
    return float(diff.mean())


def compute_mape(original: pd.Series, reconstructed: pd.Series, mask: pd.Series) -> float:
    """Mean absolute percentage error on masked values."""
    y_true = original.loc[mask]
    y_pred = reconstructed.loc[mask]
    denom = y_true.abs().replace(0, pd.NA)
    return float((y_true - y_pred).abs().div(denom).dropna().mean() * 100)


def degradation_impact_table(results: pd.DataFrame, method: str) -> pd.DataFrame:
    """Show how one method degrades as factor increases."""
    subset = results[results["method"] == method].sort_values("factor")
    if subset.empty:
        return pd.DataFrame()
    base = subset.iloc[0]["mae"]
    table = subset.copy()
    table["mae_increase_vs_factor_2"] = table["mae"] - base
    table["mae_ratio_vs_factor_2"] = table["mae"] / base if base else table["mae"]
    return table


def method_stability_score(results: pd.DataFrame, metric: str = "mae") -> pd.DataFrame:
    """
    Lower score means more stable performance across factors.

    Uses standard deviation of the metric across factors.
    """
    stats = results.groupby("method")[metric].agg(["mean", "std", "min", "max"])
    stats = stats.sort_values("std")
    stats["stability_rank"] = range(1, len(stats) + 1)
    return stats.reset_index()


def build_method_leaderboard(results: pd.DataFrame) -> pd.DataFrame:
    """Overall leaderboard using average rank across factors."""
    ranked = rank_methods_by_metric(results, "mae")
    leaderboard = ranked.groupby("method")["rank"].mean().sort_values()
    leaderboard = leaderboard.reset_index()
    leaderboard.columns = ["method", "average_rank"]
    return leaderboard


def split_errors_train_test(
    errors: pd.Series,
    train_mask: pd.Series,
    test_mask: pd.Series,
) -> dict[str, pd.Series]:
    """Split error series into train and test periods."""
    return {
        "train": errors.loc[errors.index.isin(errors.index[train_mask.reindex(errors.index, fill_value=False)])],
        "test": errors.loc[errors.index.isin(errors.index[test_mask.reindex(errors.index, fill_value=False)])],
    }


def summarize_errors_by_period(
    errors: pd.Series,
    train_mask: pd.Series,
    test_mask: pd.Series,
) -> pd.DataFrame:
    """Summarize error statistics for train and test periods."""
    aligned_train = train_mask.reindex(errors.index, fill_value=False)
    aligned_test = test_mask.reindex(errors.index, fill_value=False)
    rows = []
    for label, mask in [("train", aligned_train), ("test", aligned_test)]:
        subset = errors.loc[mask]
        if subset.empty:
            continue
        rows.append({
            "period": label,
            "mean": float(subset.mean()),
            "median": float(subset.median()),
            "max": float(subset.max()),
            "count": int(len(subset)),
        })
    return pd.DataFrame(rows)


def pivot_results(results: pd.DataFrame, metric: str = "mae") -> pd.DataFrame:
    """Pivot results to method x factor table."""
    return results.pivot(index="method", columns="factor", values=metric)


def find_methods_beating_baseline(
    results: pd.DataFrame,
    baseline: str = "linear",
    metric: str = "mae",
) -> pd.DataFrame:
    """List methods that beat a baseline on each factor."""
    rows = []
    for factor, group in results.groupby("factor"):
        baseline_row = group[group["method"] == baseline]
        if baseline_row.empty:
            continue
        baseline_value = baseline_row.iloc[0][metric]
        winners = group[group[metric] < baseline_value]
        for _, row in winners.iterrows():
            rows.append({
                "factor": factor,
                "method": row["method"],
                metric: row[metric],
                f"{baseline}_{metric}": baseline_value,
                "improvement": baseline_value - row[metric],
            })
    return pd.DataFrame(rows)


def compute_error_quantiles(errors: pd.Series) -> dict[str, float]:
    """Compute common quantiles of absolute errors."""
    return {
        "q50": float(errors.quantile(0.50)),
        "q75": float(errors.quantile(0.75)),
        "q90": float(errors.quantile(0.90)),
        "q95": float(errors.quantile(0.95)),
        "q99": float(errors.quantile(0.99)),
    }


def aggregate_error_profiles(error_by_factor: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """Aggregate mean error profile across methods for each factor."""
    rows = []
    for factor, frame in error_by_factor.items():
        for method in frame.columns:
            rows.append({
                "factor": factor,
                "method": method,
                "mean_abs_error": float(frame[method].mean()),
            })
    return pd.DataFrame(rows)


def classical_ml_gap(results: pd.DataFrame, metric: str = "mae") -> pd.DataFrame:
    """Compute gap between best classical and best ML method per factor."""
    rows = []
    for factor, group in results.groupby("factor"):
        classical = group[group["method"].isin(CLASSICAL_METHODS)]
        ml = group[group["method"].isin(ML_METHODS)]
        if classical.empty or ml.empty:
            continue
        best_classical = classical.loc[classical[metric].idxmin()]
        best_ml = ml.loc[ml[metric].idxmin()]
        rows.append({
            "factor": factor,
            "best_classical": best_classical["method"],
            "best_classical_mae": best_classical[metric],
            "best_ml": best_ml["method"],
            "best_ml_mae": best_ml[metric],
            "gap_ml_minus_classical": best_ml[metric] - best_classical[metric],
        })
    return pd.DataFrame(rows)
