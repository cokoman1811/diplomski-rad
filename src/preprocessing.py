"""Temporal degradation and data preparation."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .config import DEGRADATION_FACTORS, TEST_START, TRAIN_END
from .paths import PROCESSED_DIR, ensure_project_dirs


@dataclass
class DegradedSeries:
    """Original, degraded series and mask of removed positions."""

    original: pd.Series
    degraded: pd.Series
    removed_mask: pd.Series
    factor: int


def degrade_series(series: pd.Series, factor: int) -> DegradedSeries:
    """
    Keep every nth value and mark intermediate values as missing.

    Positions 0, factor, 2*factor, ... remain observed.
    """
    if factor < 2:
        raise ValueError("Degradation factor must be at least 2.")

    original = series.sort_index().copy()
    positions = np.arange(len(original))
    removed = positions % factor != 0

    degraded = original.copy()
    degraded.iloc[removed] = np.nan

    removed_mask = pd.Series(removed, index=original.index, name="removed")
    return DegradedSeries(
        original=original,
        degraded=degraded,
        removed_mask=removed_mask,
        factor=factor,
    )


def build_train_test_masks(index: pd.DatetimeIndex) -> tuple[pd.Series, pd.Series]:
    """Return boolean masks for train and test periods."""
    train_end = pd.Timestamp(TRAIN_END)
    test_start = pd.Timestamp(TEST_START)

    train_mask = pd.Series(index <= train_end, index=index, name="train")
    test_mask = pd.Series(index >= test_start, index=index, name="test")
    return train_mask, test_mask


def evaluation_mask(
    removed_mask: pd.Series,
    test_mask: pd.Series | None = None,
) -> pd.Series:
    """Mask of points used for metric calculation."""
    if test_mask is None:
        return removed_mask
    return removed_mask & test_mask


def save_degraded_series(degraded: DegradedSeries, output_dir=None) -> Path:
    """Save degraded series and mask to data/processed/."""
    ensure_project_dirs()
    output_dir = output_dir or PROCESSED_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    factor = degraded.factor
    base = output_dir / f"jena_temperature_factor_{factor}"

    degraded.degraded.to_csv(base.with_name(f"{base.name}_degraded.csv"))
    degraded.removed_mask.to_csv(base.with_name(f"{base.name}_mask.csv"))
    return base


def slice_recent(series: pd.Series, n_rows: int) -> pd.Series:
    """Return the most recent n_rows for quick experiments."""
    return series.iloc[-n_rows:].copy()


def slice_dataset_recent(dataset: pd.DataFrame, n_rows: int) -> pd.DataFrame:
    """Return the most recent n_rows from a dataset."""
    return dataset.iloc[-n_rows:].copy()
