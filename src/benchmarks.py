"""Benchmark execution time for reconstruction methods."""

import time
from dataclasses import dataclass

import pandas as pd

from .config import ALL_METHODS, CLASSICAL_METHODS
from .data_loader import load_jena_dataset
from .experiment_runner import ExperimentConfig, run_single_method
from .feature_engineering import build_train_test_masks
from .preprocessing import degrade_series, slice_dataset_recent
from .validation import validate_method_name


@dataclass
class BenchmarkResult:
    """Timing result for one method run."""

    method: str
    factor: int
    seconds: float
    n_samples: int


def _time_call(callable_obj, *args, **kwargs) -> tuple[float, object]:
    """Measure wall-clock time of a callable."""
    start = time.perf_counter()
    result = callable_obj(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return elapsed, result


def benchmark_single_method(
    dataset: pd.DataFrame,
    method: str,
    factor: int,
    config: ExperimentConfig | None = None,
) -> BenchmarkResult:
    """Benchmark one method on a degraded series."""
    validate_method_name(method)
    config = config or ExperimentConfig(tune_ml=False, generate_plots=False)
    temperature = dataset["temperature"]
    train_mask, test_mask = build_train_test_masks(temperature.index)
    degraded = degrade_series(temperature, factor)
    cached_params = {}

    seconds, output = _time_call(
        run_single_method,
        dataset,
        degraded,
        method,
        train_mask,
        test_mask,
        config,
        cached_params,
    )
    _, metrics, _ = output
    return BenchmarkResult(
        method=method,
        factor=factor,
        seconds=seconds,
        n_samples=metrics["n_samples"],
    )


def benchmark_methods(
    methods: list[str] | None = None,
    factors: list[int] | None = None,
    sample_size: int = 5000,
) -> pd.DataFrame:
    """Benchmark selected methods on a recent data slice."""
    methods = methods or list(ALL_METHODS)
    factors = factors or [2, 6]
    dataset = slice_dataset_recent(load_jena_dataset(), sample_size)
    config = ExperimentConfig(tune_ml=False, generate_plots=False, use_test_split=True)

    # ML models need enough training rows after lag features and seasonal split.
    if sample_size < 4000:
        methods = [method for method in methods if method in CLASSICAL_METHODS]

    rows = []
    for factor in factors:
        for method in methods:
            result = benchmark_single_method(dataset, method, factor, config)
            rows.append({
                "method": result.method,
                "factor": result.factor,
                "seconds": result.seconds,
                "n_samples": result.n_samples,
                "seconds_per_1000_samples": result.seconds / result.n_samples * 1000,
            })
    return pd.DataFrame(rows)


def benchmark_classical_only(sample_size: int = 5000) -> pd.DataFrame:
    """Benchmark only classical methods."""
    return benchmark_methods(methods=list(CLASSICAL_METHODS), sample_size=sample_size)


def format_benchmark_table(frame: pd.DataFrame) -> str:
    """Return a readable string table of benchmark results."""
    display = frame.copy()
    display["seconds"] = display["seconds"].map(lambda x: f"{x:.3f}")
    display["seconds_per_1000_samples"] = display["seconds_per_1000_samples"].map(
        lambda x: f"{x:.3f}"
    )
    return display.to_string(index=False)
