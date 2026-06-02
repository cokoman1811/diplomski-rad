"""Tests for method_info module."""

import pytest

from src.config import ALL_METHODS, CLASSICAL_METHODS, ML_METHODS
from src.method_info import (
    classical_method_docs,
    full_method_catalog_markdown,
    get_method_description,
    list_methods_with_descriptions,
    ml_method_docs,
)


def test_get_method_description_all_methods():
    for method in ALL_METHODS:
        info = get_method_description(method)
        assert "name" in info
        assert "description" in info


def test_get_method_description_invalid():
    with pytest.raises(KeyError):
        get_method_description("unknown")


def test_list_methods_with_descriptions():
    methods = list_methods_with_descriptions()
    assert len(methods) == len(ALL_METHODS)


def test_classical_method_docs_content():
    text = classical_method_docs()
    assert "Linear interpolation" in text
    for method in CLASSICAL_METHODS:
        assert method in text


def test_ml_method_docs_content():
    text = ml_method_docs()
    for method in ML_METHODS:
        assert method in text


def test_full_method_catalog_markdown():
    text = full_method_catalog_markdown()
    assert "# Method catalog" in text
    assert "Machine learning methods" in text
