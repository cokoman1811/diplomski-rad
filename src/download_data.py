"""Download and prepare raw Jena Climate data."""

import zipfile
from pathlib import Path
from urllib.request import urlretrieve

from .config import JENA_RAW_FILENAME
from .paths import RAW_DIR, ensure_project_dirs
from .validation import ValidationError, validate_raw_csv_columns, validate_raw_file_exists
from .console import print_data_ready, print_download_complete, print_download_start

JENA_DATA_URL = (
    "https://storage.googleapis.com/tensorflow/tf-keras-datasets/"
    "jena_climate_2009_2016.csv.zip"
)
JENA_ZIP_FILENAME = "jena_climate_2009_2016.csv.zip"


def download_jena_climate(raw_dir: Path | None = None, force: bool = False) -> Path:
    """
    Download and extract the Jena Climate CSV into data/raw/.

    Returns the path to the extracted CSV file.
    """
    ensure_project_dirs()
    raw_dir = raw_dir or RAW_DIR
    raw_dir.mkdir(parents=True, exist_ok=True)
    csv_path = raw_dir / JENA_RAW_FILENAME

    if csv_path.exists() and not force:
        return csv_path

    zip_path = raw_dir / JENA_ZIP_FILENAME
    print_download_start(JENA_DATA_URL)
    urlretrieve(JENA_DATA_URL, zip_path)

    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(raw_dir)

    if not csv_path.exists():
        raise FileNotFoundError(f"Expected CSV not found after extract: {csv_path}")

    print_download_complete(csv_path)
    return csv_path


def ensure_jena_data(raw_dir: Path | None = None) -> Path:
    """Download Jena data if missing and validate columns."""
    raw_dir = raw_dir or RAW_DIR
    try:
        csv_path = validate_raw_file_exists(raw_dir)
    except ValidationError:
        csv_path = download_jena_climate(raw_dir)

    checks = validate_raw_csv_columns(raw_dir)
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise ValidationError(f"Raw CSV column validation failed: {failed}")
    return csv_path


if __name__ == "__main__":
    data_path = ensure_jena_data()
    print_data_ready(data_path)
