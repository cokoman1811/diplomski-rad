"""Extended statistical analysis utilities."""

import numpy as np
import pandas as pd
from scipy.stats import kruskal, mannwhitneyu, ttest_rel, wilcoxon

from .statistical_analysis import build_error_matrix, compare_two_methods, summarize_errors


def paired_t_test(errors_a: pd.Series, errors_b: pd.Series) -> dict:
    """Paired t-test between two aligned error series."""
    aligned = pd.concat([errors_a, errors_b], axis=1, join="inner").dropna()
    if len(aligned) < 10:
        return {"statistic": None, "p_value": None, "n_pairs": len(aligned)}
    statistic, p_value = ttest_rel(aligned.iloc[:, 0], aligned.iloc[:, 1])
    return {
        "statistic": float(statistic),
        "p_value": float(p_value),
        "n_pairs": int(len(aligned)),
    }


def mann_whitney_test(errors_a: pd.Series, errors_b: pd.Series) -> dict:
    """Mann-Whitney U test for unpaired samples."""
    sample_a = errors_a.dropna()
    sample_b = errors_b.dropna()
    if len(sample_a) < 10 or len(sample_b) < 10:
        return {"statistic": None, "p_value": None}
    statistic, p_value = mannwhitneyu(sample_a, sample_b, alternative="two-sided")
    return {"statistic": float(statistic), "p_value": float(p_value)}


def kruskal_wallis_test(error_matrix: pd.DataFrame) -> dict:
    """Kruskal-Wallis test across multiple methods."""
    aligned = error_matrix.dropna()
    if aligned.shape[1] < 3 or len(aligned) < 10:
        return {"statistic": None, "p_value": None, "n_samples": len(aligned)}
    statistic, p_value = kruskal(*[aligned[col] for col in aligned.columns])
    return {
        "statistic": float(statistic),
        "p_value": float(p_value),
        "n_samples": int(len(aligned)),
    }


def compare_all_pairs(error_dict: dict[str, pd.Series]) -> pd.DataFrame:
    """Run Wilcoxon tests for all method pairs."""
    methods = list(error_dict.keys())
    rows = []
    for i, method_a in enumerate(methods):
        for method_b in methods[i + 1:]:
            result = compare_two_methods(error_dict[method_a], error_dict[method_b])
            rows.append({
                "method_a": method_a,
                "method_b": method_b,
                "statistic": result["statistic"],
                "p_value": result["p_value"],
                "n_pairs": result["n_pairs"],
            })
    return pd.DataFrame(rows)


def significant_pairs(comparison_frame: pd.DataFrame, alpha: float = 0.05) -> pd.DataFrame:
    """Filter comparisons with p-value below alpha."""
    if comparison_frame.empty:
        return comparison_frame
    return comparison_frame[comparison_frame["p_value"] < alpha].sort_values("p_value")


def effect_size_mean_difference(errors_a: pd.Series, errors_b: pd.Series) -> float:
    """Mean absolute difference between two error series."""
    aligned = pd.concat([errors_a, errors_b], axis=1, join="inner").dropna()
    if aligned.empty:
        return float("nan")
    return float((aligned.iloc[:, 0] - aligned.iloc[:, 1]).mean())


def bootstrap_mean_ci(
    errors: pd.Series,
    n_bootstrap: int = 500,
    alpha: float = 0.05,
    random_state: int = 42,
) -> dict[str, float]:
    """Bootstrap confidence interval for mean absolute error."""
    values = errors.dropna().values
    if len(values) == 0:
        return {"lower": float("nan"), "upper": float("nan"), "mean": float("nan")}
    rng = np.random.default_rng(random_state)
    means = []
    for _ in range(n_bootstrap):
        sample = rng.choice(values, size=len(values), replace=True)
        means.append(sample.mean())
    lower = float(np.quantile(means, alpha / 2))
    upper = float(np.quantile(means, 1 - alpha / 2))
    return {"lower": lower, "upper": upper, "mean": float(values.mean())}


def method_significance_report(error_dict: dict[str, pd.Series]) -> pd.DataFrame:
    """Build a full pairwise significance report."""
    pairs = compare_all_pairs(error_dict)
    pairs["significant_0_05"] = pairs["p_value"] < 0.05
    pairs["mean_difference"] = [
        effect_size_mean_difference(error_dict[row.method_a], error_dict[row.method_b])
        for row in pairs.itertuples()
    ]
    return pairs


def aggregate_significance_by_factor(
    error_by_factor: dict[int, dict[str, pd.Series]],
) -> pd.DataFrame:
    """Combine pairwise significance reports for all factors."""
    frames = []
    for factor, error_dict in error_by_factor.items():
        report = method_significance_report(error_dict)
        report["factor"] = factor
        frames.append(report)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def summarize_statistical_battery(error_dict: dict[str, pd.Series]) -> dict:
    """Return a compact dict of statistical test outputs."""
    matrix = build_error_matrix(error_dict)
    return {
        "kruskal": kruskal_wallis_test(matrix),
        "pairwise": compare_all_pairs(error_dict).to_dict(orient="records"),
    }
