"""Tests for HTML report generation."""

from pathlib import Path

import pytest

from src.report_html import (
    FigureEntry,
    _group_entries_by_method,
    collect_figure_entries,
    generate_html_report,
    _parse_figure_metadata,
)


def test_parse_reconstruction_metadata():
    category, factor, method = _parse_figure_metadata("reconstruction_factor_6_linear.png")
    assert category == "Rekonstrukcija"
    assert factor == "6"
    assert method == "linear"


def test_generate_html_report(tmp_path, sample_results_table):
    figures_dir = tmp_path / "figures"
    figures_dir.mkdir()
    (figures_dir / "reconstruction_factor_2_linear.png").write_bytes(b"fake")
    (figures_dir / "hist_factor_2_random_forest.png").write_bytes(b"fake")

    output = tmp_path / "report.html"
    path = generate_html_report(
        sample_results_table,
        output_path=output,
        figures_dir=figures_dir,
    )

    text = path.read_text(encoding="utf-8")
    assert path.exists()
    assert "Galerija grafikona po metodama" in text
    assert "method-section" in text
    assert "Linear interpolation" in text
    assert "figures/reconstruction_factor_2_linear.png" in text
    assert "filter-category" in text


def test_group_entries_by_method():
    entries = [
        FigureEntry(
            filename="a.png",
            title="t1",
            category="Rekonstrukcija",
            factor="2",
            method="linear",
            rel_path="figures/a.png",
        ),
        FigureEntry(
            filename="b.png",
            title="t2",
            category="Heatmap",
            factor="",
            method="MAE",
            rel_path="figures/b.png",
        ),
    ]
    sections = _group_entries_by_method(entries)
    assert sections[0][0] == "linear"
    assert sections[-1][0] == "__global__"


def test_collect_figure_entries_empty(tmp_path):
    figures_dir = tmp_path / "figures"
    figures_dir.mkdir()
    assert collect_figure_entries(figures_dir) == []
