"""Evaluation metrics for reconstructed time series."""

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute_metrics(
    original: pd.Series,
    reconstructed: pd.Series,
    eval_mask: pd.Series,
) -> dict[str, float]:
    """Compute MAE, RMSE and R2 on the evaluation mask."""
    y_true = original.loc[eval_mask]
    y_pred = reconstructed.loc[eval_mask]

    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred) ** 0.5
    r2 = r2_score(y_true, y_pred)

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "n_samples": int(eval_mask.sum()),
    }


def compute_point_errors(
    original: pd.Series,
    reconstructed: pd.Series,
    eval_mask: pd.Series,
) -> pd.Series:
    """Return absolute errors for each evaluated point."""
    errors = (original - reconstructed).abs()
    return errors.loc[eval_mask]


def aggregate_results(results: list[dict]) -> pd.DataFrame:
    """Convert a list of result dicts to a sorted DataFrame."""
    frame = pd.DataFrame(results)
    if frame.empty:
        return frame
    return frame.sort_values(["factor", "method"]).reset_index(drop=True)
