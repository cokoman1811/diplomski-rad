"""Statistical analysis of method comparison."""

import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon


def summarize_errors(errors: pd.Series) -> dict[str, float]:
    """Compute additional error summary statistics."""
    return {
        "mean_abs_error": float(errors.mean()),
        "median_abs_error": float(errors.median()),
        "max_abs_error": float(errors.max()),
        "p90_abs_error": float(errors.quantile(0.90)),
        "p95_abs_error": float(errors.quantile(0.95)),
    }


def compare_two_methods(errors_a: pd.Series, errors_b: pd.Series) -> dict:
    """Paired Wilcoxon test between two methods on aligned errors."""
    aligned = pd.concat([errors_a, errors_b], axis=1, join="inner").dropna()
    if len(aligned) < 10:
        return {"statistic": None, "p_value": None, "n_pairs": len(aligned)}

    statistic, p_value = wilcoxon(aligned.iloc[:, 0], aligned.iloc[:, 1])
    return {
        "statistic": float(statistic),
        "p_value": float(p_value),
        "n_pairs": int(len(aligned)),
    }


def friedman_test(error_matrix: pd.DataFrame) -> dict:
    """Friedman test across multiple methods on aligned samples."""
    aligned = error_matrix.dropna()
    if aligned.shape[1] < 3 or len(aligned) < 10:
        return {"statistic": None, "p_value": None, "n_samples": len(aligned)}

    statistic, p_value = friedmanchisquare(*[aligned[col] for col in aligned.columns])
    return {
        "statistic": float(statistic),
        "p_value": float(p_value),
        "n_samples": int(len(aligned)),
    }


def build_error_matrix(
    error_dict: dict[str, pd.Series],
) -> pd.DataFrame:
    """Combine per-method error series into one DataFrame."""
    return pd.DataFrame(error_dict)


def compare_methods_for_factor(
    method_errors: dict[str, pd.Series],
    baseline_method: str = "linear",
) -> pd.DataFrame:
    """Compare each method against a baseline using Wilcoxon tests."""
    rows = []
    baseline = method_errors.get(baseline_method)
    if baseline is None:
        return pd.DataFrame()

    for method, errors in method_errors.items():
        if method == baseline_method:
            continue
        result = compare_two_methods(baseline, errors)
        rows.append({
            "method": method,
            "baseline": baseline_method,
            "statistic": result["statistic"],
            "p_value": result["p_value"],
            "n_pairs": result["n_pairs"],
        })

    return pd.DataFrame(rows)
