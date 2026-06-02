"""Tests for console formatting helpers."""

import pandas as pd

from src.console import _strip_ansi, format_results_table


def test_format_results_table_contains_headers(sample_results_table):
    text = format_results_table(sample_results_table)
    assert "Faktor" in text
    assert "MAE" in text
    assert "najbolja MAE" in text


def test_format_results_table_marks_best_method(sample_results_table):
    text = format_results_table(sample_results_table)
    assert "Linear interpolation" in text or "linear" in text.lower()


def test_strip_ansi_removes_color_codes():
    colored = "\x1b[32mok\x1b[0m"
    assert _strip_ansi(colored) == "ok"


def test_format_results_table_empty():
    text = format_results_table(pd.DataFrame())
    assert "nema rezultata" in text
