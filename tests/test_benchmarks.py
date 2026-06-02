"""Tests for benchmarks module."""

from src.benchmarks import (
    benchmark_classical_only,
    benchmark_methods,
    benchmark_single_method,
    format_benchmark_table,
)
from src.config import CLASSICAL_METHODS
from src.data_loader import load_jena_dataset
from src.experiment_runner import ExperimentConfig
from src.preprocessing import slice_dataset_recent


def test_benchmark_single_method():
    dataset = slice_dataset_recent(load_jena_dataset(), 1000)
    result = benchmark_single_method(dataset, "linear", 2)
    assert result.method == "linear"
    assert result.seconds > 0
    assert result.n_samples > 0


def test_benchmark_methods_subset():
    frame = benchmark_methods(
        methods=["linear", "forward_fill"],
        factors=[2],
        sample_size=1000,
    )
    assert len(frame) == 2
    assert "seconds_per_1000_samples" in frame.columns


def test_benchmark_classical_only():
    frame = benchmark_classical_only(sample_size=1000)
    assert len(frame) == len(CLASSICAL_METHODS) * 2


def test_format_benchmark_table():
    import pandas as pd

    frame = pd.DataFrame([
        {"method": "linear", "factor": 2, "seconds": 0.12, "n_samples": 100, "seconds_per_1000_samples": 1.2}
    ])
    text = format_benchmark_table(frame)
    assert "linear" in text
