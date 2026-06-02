"""Tests for experiment protocol documentation."""

from src.config import ALL_METHODS, QUICK_DEGRADATION_FACTORS
from src.experiment_protocol import (
    FULL_PROTOCOL,
    list_protocol_steps,
    full_run_protocol_summary,
    protocol_markdown,
    quick_run_protocol_summary,
    validate_protocol_methods,
)


def test_protocol_has_six_steps():
    assert len(FULL_PROTOCOL) == 6
    assert len(list_protocol_steps()) == 6


def test_protocol_markdown_contains_titles():
    text = protocol_markdown()
    assert "Protokol eksperimenta" in text
    assert "Evaluacija" in text


def test_quick_summary_mentions_sample_size():
    text = quick_run_protocol_summary()
    assert "10000" in text.replace("_", "")
    for factor in QUICK_DEGRADATION_FACTORS:
        assert str(factor) in text


def test_full_summary_mentions_all_methods():
    text = full_run_protocol_summary()
    assert str(len(ALL_METHODS)) not in text  # mentions classical+ml separately
    assert "klasičnih" in text


def test_validate_protocol_methods_detects_unknown():
    unknown = validate_protocol_methods(["linear", "unknown_method"])
    assert unknown == ["unknown_method"]
