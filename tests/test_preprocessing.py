"""Tests for preprocessing."""

import pandas as pd

from src.preprocessing import (
    build_train_test_masks,
    degrade_series,
    evaluation_mask,
    slice_recent,
)


def test_degrade_series_factor_2(synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, factor=2)
    assert degraded.degraded.notna().sum() == len(synthetic_temperature) // 2 + (
        1 if len(synthetic_temperature) % 2 else 0
    )
    assert degraded.removed_mask.sum() == degraded.degraded.isna().sum()


def test_degrade_series_invalid_factor(synthetic_temperature):
    try:
        degrade_series(synthetic_temperature, factor=1)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_evaluation_mask_with_test_split(synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, factor=3)
    train_mask, test_mask = build_train_test_masks(synthetic_temperature.index)
    mask = evaluation_mask(degraded.removed_mask, test_mask)
    assert mask.dtype == bool
    assert mask.sum() <= degraded.removed_mask.sum()


def test_slice_recent(synthetic_temperature):
    sliced = slice_recent(synthetic_temperature, 50)
    assert len(sliced) == 50
