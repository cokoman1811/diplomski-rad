"""Tests for reporting module."""

import pandas as pd

from src.reporting import (
    _dataframe_to_markdown,
    generate_results_markdown,
    save_all_reports,
    save_best_methods_table,
    save_classical_ml_comparison,
    save_leaderboard,
    save_ranked_results,
    save_results_report,
    update_results_notes_template,
)


def test_dataframe_to_markdown():
    frame = pd.DataFrame({"a": [1], "b": [2]})
    text = _dataframe_to_markdown(frame)
    assert "| a | b |" in text
    assert "| 1 | 2 |" in text


def test_generate_results_markdown(sample_results_table):
    text = generate_results_markdown(sample_results_table)
    assert "# Experiment report" in text
    assert "linear" in text


def test_save_results_report(tmp_path, sample_results_table, monkeypatch):
    monkeypatch.setattr("src.reporting.TABLES_DIR", tmp_path)
    path = save_results_report(sample_results_table, filename="report.md")
    assert path.exists()
    assert path.read_text(encoding="utf-8").startswith("# Experiment report")


def test_save_all_reports(tmp_path, sample_results_table, monkeypatch):
    monkeypatch.setattr("src.reporting.TABLES_DIR", tmp_path)
    paths = save_all_reports(sample_results_table)
    assert paths["markdown"].exists()
    assert paths["ranked"].exists()
    assert paths["leaderboard"].exists()


def test_save_individual_tables(tmp_path, sample_results_table, monkeypatch):
    monkeypatch.setattr("src.reporting.TABLES_DIR", tmp_path)
    assert save_ranked_results(sample_results_table).exists()
    assert save_best_methods_table(sample_results_table).exists()
    assert save_leaderboard(sample_results_table).exists()
    assert save_classical_ml_comparison(sample_results_table).exists()


def test_update_results_notes_template(tmp_path, sample_results_table):
    notes = tmp_path / "results_notes.md"
    notes.write_text("# Notes\n", encoding="utf-8")
    update_results_notes_template(sample_results_table, notes)
    content = notes.read_text(encoding="utf-8")
    assert "Auto-generated summary" in content
