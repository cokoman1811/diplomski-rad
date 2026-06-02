"""Tests for classical interpolation methods."""

import pandas as pd

from src.interpolation_methods import interpolate, list_classical_methods


def test_list_classical_methods():
    methods = list_classical_methods()
    assert "linear" in methods
    assert len(methods) == 5


def test_interpolate_linear_fills_missing(synthetic_temperature):
    degraded = synthetic_temperature.copy()
    degraded.iloc[1:10] = pd.NA
    filled = interpolate(degraded.astype(float), "linear")
    assert filled.isna().sum() == 0


def test_all_classical_methods_run(synthetic_temperature):
    degraded = synthetic_temperature.copy()
    degraded.iloc[3:15] = pd.NA
    degraded = degraded.astype(float)
    for method in list_classical_methods():
        filled = interpolate(degraded, method)
        assert filled.isna().sum() == 0
