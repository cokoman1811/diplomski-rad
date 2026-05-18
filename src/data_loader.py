"""Load time-series temperature data for the thesis experiments."""

import zipfile
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

from .paths import PROCESSED_DIR, RAW_DIR, ensure_project_dirs

JENA_DATA_URL = (
    "https://storage.googleapis.com/tensorflow/tf-keras-datasets/"
    "jena_climate_2009_2016.csv.zip"
)
JENA_ZIP_FILENAME = "jena_climate_2009_2016.csv.zip"
JENA_RAW_FILENAME = "jena_climate_2009_2016.csv"
JENA_PROCESSED_FILENAME = "jena_temperature.csv"

TIMESTAMP_COLUMNS = ("Date Time", "timestamp", "time", "datetime")
TEMPERATURE_COLUMNS = ("T (degC)", "temperature", "T", "temp")


def download_jena_climate(raw_dir: Path | None = None) -> Path:
    """Download the Jena Climate CSV into data/raw/ if it is not already present."""
    ensure_project_dirs()
    raw_dir = raw_dir or RAW_DIR
    raw_dir.mkdir(parents=True, exist_ok=True)

    csv_path = raw_dir / JENA_RAW_FILENAME
    if csv_path.exists():
        return csv_path

    zip_path = raw_dir / JENA_ZIP_FILENAME
    print(f"Downloading Jena Climate dataset to {zip_path}...")
    urlretrieve(JENA_DATA_URL, zip_path)

    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(raw_dir)

    if not csv_path.exists():
        raise FileNotFoundError(f"Expected CSV not found after extract: {csv_path}")

    print(f"Download finished: {csv_path}")
    return csv_path


def _pick_column(columns: pd.Index, candidates: tuple[str, ...]) -> str:
    """Return the first matching column name from a list of candidates."""
    for name in candidates:
        if name in columns:
            return name
    raise ValueError(f"None of {candidates} found in columns: {list(columns)}")


def _normalize_temperature_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only timestamp and temperature with consistent column names."""
    timestamp_col = _pick_column(df.columns, TIMESTAMP_COLUMNS)
    temperature_col = _pick_column(df.columns, TEMPERATURE_COLUMNS)

    normalized = df[[timestamp_col, temperature_col]].copy()
    normalized.columns = ["timestamp", "temperature"]
    normalized["timestamp"] = pd.to_datetime(normalized["timestamp"], dayfirst=True)
    normalized["temperature"] = pd.to_numeric(normalized["temperature"], errors="coerce")
    normalized = normalized.dropna(subset=["timestamp", "temperature"])
    normalized = normalized.sort_values("timestamp").reset_index(drop=True)
    return normalized


def load_jena_temperature(
    raw_dir: Path | None = None,
    processed_dir: Path | None = None,
    save_processed: bool = True,
) -> pd.DataFrame:
    """
    Load the Jena Climate dataset (10-minute resolution) and return temperature.

    Returns a DataFrame with columns: timestamp, temperature.
    """
    csv_path = download_jena_climate(raw_dir)
    raw_df = pd.read_csv(csv_path)
    df = _normalize_temperature_frame(raw_df)

    if save_processed:
        processed_dir = processed_dir or PROCESSED_DIR
        processed_dir.mkdir(parents=True, exist_ok=True)
        output_path = processed_dir / JENA_PROCESSED_FILENAME
        df.to_csv(output_path, index=False)
        print(f"Processed data saved to {output_path}")

    return df


def load_temperature_csv(path: Path | str) -> pd.DataFrame:
    """Load a CSV file that contains timestamp and temperature columns."""
    df = pd.read_csv(path)
    return _normalize_temperature_frame(df)


if __name__ == "__main__":
    data = load_jena_temperature()
    print(data.head())
    print()
    print(f"Rows: {len(data)}")
    print(f"From {data['timestamp'].min()} to {data['timestamp'].max()}")
