"""Shared pytest fixtures."""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def synthetic_temperature():
    """Create a small hourly temperature series."""
    index = pd.date_range("2024-01-01", periods=240, freq="10min")
    values = 10 + 5 * np.sin(np.arange(len(index)) * 2 * np.pi / 144)
    return pd.Series(values, index=index, name="temperature")


@pytest.fixture
def synthetic_dataset(synthetic_temperature):
    """Create a small dataset with covariates."""
    frame = pd.DataFrame(index=synthetic_temperature.index)
    frame["p (mbar)"] = 1000 + np.random.default_rng(42).normal(0, 2, len(frame))
    frame["rh (%)"] = 60 + np.random.default_rng(43).normal(0, 5, len(frame))
    frame["wv (m/s)"] = np.abs(np.random.default_rng(44).normal(2, 0.5, len(frame)))
    frame["max. wv (m/s)"] = frame["wv (m/s)"] + 1
    frame["temperature"] = synthetic_temperature
    return frame


@pytest.fixture
def sample_results_table():
    """Small experiment results table for reporting/analysis tests."""
    return pd.DataFrame([
        {"factor": 2, "method": "linear", "mae": 0.1, "rmse": 0.2, "r2": 0.99, "n_samples": 100},
        {"factor": 2, "method": "random_forest", "mae": 0.2, "rmse": 0.3, "r2": 0.95, "n_samples": 100},
        {"factor": 6, "method": "linear", "mae": 0.3, "rmse": 0.4, "r2": 0.95, "n_samples": 200},
        {"factor": 6, "method": "random_forest", "mae": 0.4, "rmse": 0.5, "r2": 0.90, "n_samples": 200},
    ])
