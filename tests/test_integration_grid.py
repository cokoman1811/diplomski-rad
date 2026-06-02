"""Integration tests across methods and degradation factors."""

import pytest

from src.config import ALL_METHODS, CLASSICAL_METHODS, DEGRADATION_FACTORS, ML_METHODS, QUICK_DEGRADATION_FACTORS
from src.experiment_runner import ExperimentConfig, run_experiments, run_single_method
from src.feature_engineering import build_train_test_masks
from src.interpolation_methods import interpolate, list_classical_methods
from src.preprocessing import degrade_series, slice_dataset_recent
from src.data_loader import load_jena_dataset
from src.thesis_export import export_all_thesis_tables


@pytest.mark.parametrize("method", CLASSICAL_METHODS)
def test_each_classical_method_on_synthetic(method, synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, 2)
    filled = interpolate(degraded.degraded.astype(float), method)
    assert filled.isna().sum() == 0


@pytest.mark.parametrize("factor", [2, 3, 6, 12])
def test_degradation_factors_on_synthetic(factor, synthetic_temperature):
    degraded = degrade_series(synthetic_temperature, factor)
    observed = degraded.degraded.notna().sum()
    assert observed > 0
    assert degraded.removed_mask.sum() > 0


@pytest.mark.parametrize("method", ["linear", "forward_fill"])
@pytest.mark.parametrize("factor", [2, 6])
def test_run_single_method_jena_slice(method, factor):
    dataset = slice_dataset_recent(load_jena_dataset(), 2000)
    temperature = dataset["temperature"]
    train_mask, test_mask = build_train_test_masks(temperature.index)
    degraded = degrade_series(temperature, factor)
    config = ExperimentConfig(tune_ml=False, generate_plots=False)
    reconstructed, metrics, errors = run_single_method(
        dataset,
        degraded,
        method,
        train_mask,
        test_mask,
        config,
        {},
    )
    assert metrics["mae"] >= 0
    assert metrics["n_samples"] > 0
    assert len(errors) == metrics["n_samples"]


def test_quick_experiment_all_methods():
    config = ExperimentConfig(
        quick=True,
        methods=list(ALL_METHODS),
        tune_ml=False,
        generate_plots=False,
    )
    output = run_experiments(config)
    assert len(output["results"]) == len(ALL_METHODS) * len(QUICK_DEGRADATION_FACTORS)


def test_quick_experiment_exports_thesis_tables(tmp_path, monkeypatch):
    monkeypatch.setattr("src.thesis_export.TABLES_DIR", tmp_path)
    config = ExperimentConfig(
        quick=True,
        factors=[2],
        methods=["linear", "random_forest"],
        tune_ml=False,
        generate_plots=False,
    )
    output = run_experiments(config)
    paths = export_all_thesis_tables(output["results"])
    assert paths["ranked"].exists()
    assert paths["summary_sentences"].exists()


@pytest.mark.parametrize("method", list_classical_methods())
def test_classical_methods_registry(method):
    assert method in CLASSICAL_METHODS


@pytest.mark.parametrize("method", ML_METHODS)
def test_ml_methods_in_all_methods(method):
    assert method in ALL_METHODS


def test_all_degradation_factors_in_config():
    assert DEGRADATION_FACTORS == [2, 3, 6, 12]
