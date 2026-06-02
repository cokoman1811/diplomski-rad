"""Tests for experiment runner."""

from src.config import CLASSICAL_METHODS
from src.experiment_runner import ExperimentConfig, run_experiments


def test_run_quick_experiment():
    config = ExperimentConfig(
        quick=True,
        factors=[2],
        methods=["linear", "forward_fill"],
        tune_ml=False,
        generate_plots=False,
    )
    output = run_experiments(config)
    assert len(output["results"]) == 2
    assert set(output["results"]["method"]) == {"linear", "forward_fill"}


def test_run_quick_with_ml():
    config = ExperimentConfig(
        quick=True,
        factors=[2],
        methods=["random_forest"],
        tune_ml=False,
        generate_plots=False,
    )
    output = run_experiments(config)
    assert len(output["results"]) == 1
    assert output["results"].iloc[0]["method"] == "random_forest"


def test_classical_methods_constant_exists():
    assert len(CLASSICAL_METHODS) == 5
