"""Documentation and thesis note tests."""

import pytest

from src.config import ALL_METHODS, CLASSICAL_METHODS, ML_METHODS
from src.method_info import (
    CROATIAN_THESIS_NOTES,
    ENGLISH_THESIS_NOTES,
    METHOD_DESCRIPTIONS,
    build_bilingual_method_appendix,
    classical_method_docs,
    full_method_catalog_markdown,
    get_croatian_thesis_note,
    get_english_thesis_note,
    get_method_description,
    list_methods_with_descriptions,
    ml_method_docs,
)


@pytest.mark.parametrize("method", ALL_METHODS)
def test_method_description_exists(method):
    info = get_method_description(method)
    assert info["name"]
    assert info["description"]


@pytest.mark.parametrize("method", ALL_METHODS)
def test_croatian_thesis_note_exists(method):
    note = get_croatian_thesis_note(method)
    assert len(note) > 20


@pytest.mark.parametrize("method", ALL_METHODS)
def test_english_thesis_note_exists(method):
    note = get_english_thesis_note(method)
    assert len(note) > 10


def test_all_methods_have_bilingual_notes():
    assert set(CROATIAN_THESIS_NOTES) == set(ALL_METHODS)
    assert set(ENGLISH_THESIS_NOTES) == set(ALL_METHODS)


def test_list_methods_with_descriptions_count():
    methods = list_methods_with_descriptions()
    assert len(methods) == len(ALL_METHODS)


def test_classical_docs_cover_all_classical_methods():
    text = classical_method_docs()
    for method in CLASSICAL_METHODS:
        assert method in text


def test_ml_docs_cover_all_ml_methods():
    text = ml_method_docs()
    for method in ML_METHODS:
        assert method in text


def test_full_method_catalog_contains_sections():
    text = full_method_catalog_markdown()
    assert "Classical methods" in text
    assert "Machine learning methods" in text


def test_bilingual_appendix_contains_all_methods():
    text = build_bilingual_method_appendix()
    for method in ALL_METHODS:
        assert method in text
        assert "Hrvatski" in text
        assert "English" in text


@pytest.mark.parametrize("method", CLASSICAL_METHODS)
def test_classical_methods_do_not_use_covariates(method):
    assert METHOD_DESCRIPTIONS[method]["uses_covariates"] is False


@pytest.mark.parametrize("method", ML_METHODS)
def test_ml_methods_use_covariates(method):
    assert METHOD_DESCRIPTIONS[method]["uses_covariates"] is True


@pytest.mark.parametrize("method", ML_METHODS)
def test_ml_methods_need_training(method):
    assert METHOD_DESCRIPTIONS[method]["needs_training"] is True
