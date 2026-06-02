"""Tests for thesis chapter text generators."""

import pandas as pd
import pytest

from src.config import CLASSICAL_METHODS, DEGRADATION_FACTORS, ML_METHODS
from src.thesis_chapters import (
    CHAPTER_TITLES_HR,
    EXPERIMENT_STEPS_HR,
    METHODOLOGY_SECTIONS_HR,
    build_full_thesis_skeleton,
    generate_chapter_outline,
    generate_conclusion_paragraphs,
    generate_dataset_description,
    generate_degradation_description,
    generate_evaluation_description,
    generate_introduction_paragraphs,
    generate_literature_outline,
    generate_methodology_chapter,
    generate_results_discussion,
    list_experiment_steps,
    list_methodology_sections,
)


def test_chapter_outline_contains_all_chapters():
    text = generate_chapter_outline()
    for title in CHAPTER_TITLES_HR.values():
        assert title in text


def test_methodology_sections_list_matches_constant():
    assert list_methodology_sections() == METHODOLOGY_SECTIONS_HR


def test_experiment_steps_list_matches_constant():
    assert list_experiment_steps() == EXPERIMENT_STEPS_HR


def test_dataset_description_mentions_target():
    text = generate_dataset_description()
    assert "temperatura" in text.lower()
    assert "Jena" in text


def test_degradation_description_lists_factors():
    text = generate_degradation_description()
    for factor in DEGRADATION_FACTORS:
        assert str(factor) in text


def test_evaluation_description_mentions_metrics():
    text = generate_evaluation_description()
    assert "MAE" in text
    assert "RMSE" in text
    assert "R²" in text


def test_methodology_chapter_lists_all_methods():
    text = generate_methodology_chapter()
    for method in CLASSICAL_METHODS + ML_METHODS:
        assert method in text


def test_introduction_has_multiple_paragraphs():
    paragraphs = generate_introduction_paragraphs()
    assert len(paragraphs) >= 3


def test_literature_outline_has_bullets():
    text = generate_literature_outline()
    assert text.count("- ") >= 5


def test_results_discussion_empty_table():
    text = generate_results_discussion(pd.DataFrame())
    assert "nisu dostupni" in text


def test_results_discussion_with_sample_table(sample_results_table):
    text = generate_results_discussion(sample_results_table)
    assert "linear" in text
    assert "Faktor" in text


def test_conclusion_without_results():
    paragraphs = generate_conclusion_paragraphs(None)
    assert len(paragraphs) >= 2


def test_conclusion_with_results(sample_results_table):
    paragraphs = generate_conclusion_paragraphs(sample_results_table)
    assert any("linear" in paragraph for paragraph in paragraphs)


def test_full_skeleton_without_results():
    text = build_full_thesis_skeleton()
    assert "Metodologija" in text
    assert "Zaključak" in text
    assert "Bilingual method appendix" in text


def test_full_skeleton_with_results(sample_results_table):
    text = build_full_thesis_skeleton(sample_results_table)
    assert "Rezultati i analiza" in text


@pytest.mark.parametrize("section", METHODOLOGY_SECTIONS_HR)
def test_methodology_outline_lists_each_section(section):
    text = generate_chapter_outline()
    assert section in text


@pytest.mark.parametrize("step_index", range(len(EXPERIMENT_STEPS_HR)))
def test_methodology_chapter_numbered_steps(step_index):
    text = generate_methodology_chapter()
    assert f"{step_index + 1}." in text
