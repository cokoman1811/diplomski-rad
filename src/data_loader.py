"""Load the Jena Climate dataset."""

from pathlib import Path

import pandas as pd

from .config import (
    COVARIATE_COLUMNS,
    DATETIME_COLUMN,
    JENA_RAW_FILENAME,
    TEMPERATURE_COLUMN,
)
from .paths import RAW_DIR


def load_jena_raw(raw_dir: Path | None = None) -> pd.DataFrame:
    """Load the full Jena CSV with datetime index."""
    raw_dir = raw_dir or RAW_DIR
    csv_path = raw_dir / JENA_RAW_FILENAME

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Jena Climate file not found: {csv_path}. "
            f"Place {JENA_RAW_FILENAME} in data/raw/."
        )

    df = pd.read_csv(csv_path)
    df.index = pd.to_datetime(df[DATETIME_COLUMN], dayfirst=True)
    df = df.drop(columns=[DATETIME_COLUMN])
    df = df.sort_index()
    return df


def load_jena_temperature(raw_dir: Path | None = None) -> pd.Series:
    """
    Load temperature from the Jena Climate CSV in data/raw/.

    Returns a Series indexed by datetime, sorted from oldest to newest.
    """
    df = load_jena_raw(raw_dir)
    temperature = pd.to_numeric(df[TEMPERATURE_COLUMN], errors="coerce")
    temperature.name = "temperature"
    return temperature.sort_index()


def load_jena_covariates(raw_dir: Path | None = None) -> pd.DataFrame:
    """Load selected covariate columns with datetime index."""
    df = load_jena_raw(raw_dir)
    covariates = df[COVARIATE_COLUMNS].apply(pd.to_numeric, errors="coerce")
    return covariates.sort_index()


def load_jena_dataset(raw_dir: Path | None = None) -> pd.DataFrame:
    """Load temperature and covariates in one DataFrame."""
    temperature = load_jena_temperature(raw_dir)
    covariates = load_jena_covariates(raw_dir)
    dataset = covariates.copy()
    dataset["temperature"] = temperature
    return dataset.sort_index()


if __name__ == "__main__":
    series = load_jena_temperature()
    print(series.head())
    print()
    print(f"Length: {len(series)}")
    print(f"From {series.index.min()} to {series.index.max()}")
