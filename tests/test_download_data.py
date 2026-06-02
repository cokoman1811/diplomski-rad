"""Tests for download_data module."""

from pathlib import Path

from src.download_data import ensure_jena_data
from src.validation import validate_raw_file_exists


def test_ensure_jena_data():
    path = ensure_jena_data()
    assert path.exists()
    assert path.name.endswith(".csv")


def test_raw_file_validation():
    path = validate_raw_file_exists()
    assert isinstance(path, Path)
