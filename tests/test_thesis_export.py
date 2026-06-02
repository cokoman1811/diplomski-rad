"""Tests for thesis export module."""

from src.experiment_runner import ExperimentConfig, run_experiments
from src.thesis_export import (
    build_croatian_summary_sentences,
    build_english_summary_sentences,
    export_all_thesis_tables,
    export_factor_definitions,
    export_method_catalog,
    export_method_metadata_table,
    export_metric_pivot_tables,
)


def test_export_metric_pivot_tables(tmp_path, sample_results_table, monkeypatch):
    monkeypatch.setattr("src.thesis_export.TABLES_DIR", tmp_path)
    paths = export_metric_pivot_tables(sample_results_table)
    assert set(paths.keys()) == {"mae", "rmse", "r2"}


def test_export_all_thesis_tables(tmp_path, sample_results_table, monkeypatch):
    monkeypatch.setattr("src.thesis_export.TABLES_DIR", tmp_path)
    paths = export_all_thesis_tables(sample_results_table)
    assert paths["leaderboard"].exists()
    assert paths["method_catalog"].exists()


def test_summary_sentences(sample_results_table):
    hr = build_croatian_summary_sentences(sample_results_table)
    en = build_english_summary_sentences(sample_results_table)
    assert any("Rezultati pokazuju" in sentence for sentence in hr)
    assert any("results show" in sentence.lower() for sentence in en)


def test_export_metadata_and_catalog(tmp_path, monkeypatch):
    monkeypatch.setattr("src.thesis_export.TABLES_DIR", tmp_path)
    assert export_method_metadata_table().exists()
    assert export_method_catalog().exists()
    assert export_factor_definitions().exists()


def test_thesis_export_after_quick_run(tmp_path, monkeypatch):
    monkeypatch.setattr("src.thesis_export.TABLES_DIR", tmp_path)
    monkeypatch.setattr("src.io_utils.TABLES_DIR", tmp_path)
    output = run_experiments(
        ExperimentConfig(quick=True, factors=[2], methods=["linear"], tune_ml=False, generate_plots=False)
    )
    paths = export_all_thesis_tables(output["results"])
    assert len(paths) >= 8
