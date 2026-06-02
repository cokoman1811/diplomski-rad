"""Tests for CLI helpers."""

from src.cli_helpers import (
    build_extended_parser,
    dispatch_cli,
    run_benchmark,
    run_check_data,
    run_export_thesis,
    run_method_catalog,
)


def test_build_extended_parser():
    parser = build_extended_parser()
    args = parser.parse_args(["check-data"])
    assert args.command == "check-data"


def test_run_check_data():
    report = run_check_data()
    assert "temperature" in report


def test_run_method_catalog():
    text = run_method_catalog()
    assert "Method catalog" in text


def test_run_benchmark():
    text = run_benchmark(sample_size=1000)
    assert "linear" in text


def test_dispatch_check_data():
    parser = build_extended_parser()
    args = parser.parse_args(["check-data"])
    report = dispatch_cli(args)
    assert "sampling" in report


def test_run_export_thesis_quick(tmp_path, monkeypatch):
    monkeypatch.setattr("src.thesis_export.TABLES_DIR", tmp_path)
    monkeypatch.setattr("src.io_utils.TABLES_DIR", tmp_path)
    monkeypatch.setattr("src.reporting.TABLES_DIR", tmp_path)
    output = run_export_thesis(quick=True)
    assert "results" in output
    assert output["paths"]["leaderboard"].exists()
