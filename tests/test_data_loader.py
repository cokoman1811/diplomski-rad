"""Tests for data loading."""

from pathlib import Path

import pandas as pd
import pytest

from src.config import JENA_RAW_FILENAME, TEMPERATURE_COLUMN
from src.data_loader import load_jena_covariates, load_jena_dataset, load_jena_temperature


def test_load_jena_temperature():
    series = load_jena_temperature()
    assert isinstance(series, pd.Series)
    assert series.name == "temperature"
    assert series.index.is_monotonic_increasing
    assert len(series) > 100_000


def test_load_jena_dataset_columns():
    dataset = load_jena_dataset()
    assert "temperature" in dataset.columns
    assert "p (mbar)" in dataset.columns


def test_load_jena_covariates():
    covariates = load_jena_covariates()
    assert len(covariates.columns) == 4


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_jena_temperature(raw_dir=tmp_path)


def test_jena_raw_file_exists():
    path = Path("data/raw") / JENA_RAW_FILENAME
    assert path.exists()
    assert TEMPERATURE_COLUMN in pd.read_csv(path, nrows=1).columns
