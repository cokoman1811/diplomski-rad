"""Save and load experiment outputs."""

import json
from pathlib import Path

import pandas as pd

from .paths import TABLES_DIR, ensure_project_dirs


def save_results_table(df: pd.DataFrame, filename: str) -> Path:
    """Save a results DataFrame to results/tables/."""
    ensure_project_dirs()
    path = TABLES_DIR / filename
    df.to_csv(path, index=False)
    return path


def save_json(data: dict, filename: str) -> Path:
    """Save a dictionary as JSON to results/tables/."""
    ensure_project_dirs()
    path = TABLES_DIR / filename
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    return path


def load_json(filename: str) -> dict:
    """Load JSON from results/tables/."""
    path = TABLES_DIR / filename
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
