"""Tests for io_utils module."""

import json

import pandas as pd

from src.io_utils import load_json, save_json, save_results_table


def test_save_and_load_json(tmp_path, monkeypatch):
    monkeypatch.setattr("src.io_utils.TABLES_DIR", tmp_path)
    payload = {"metric": "mae", "value": 0.1}
    path = save_json(payload, "test.json")
    assert path.exists()
    loaded = load_json("test.json")
    assert loaded == payload


def test_save_results_table(tmp_path, monkeypatch):
    monkeypatch.setattr("src.io_utils.TABLES_DIR", tmp_path)
    frame = pd.DataFrame([{"method": "linear", "mae": 0.1}])
    path = save_results_table(frame, "table.csv")
    assert path.exists()
    loaded = pd.read_csv(path)
    assert loaded.iloc[0]["method"] == "linear"
