"""Tests for config constants."""

from src import config


def test_degradation_factors():
    assert 2 in config.DEGRADATION_FACTORS
    assert 12 in config.DEGRADATION_FACTORS


def test_method_lists():
    assert len(config.CLASSICAL_METHODS) == 5
    assert len(config.ML_METHODS) == 2
    assert set(config.ALL_METHODS) == set(config.CLASSICAL_METHODS + config.ML_METHODS)


def test_param_grids_not_empty():
    assert config.RF_PARAM_GRID["n_estimators"]
    assert config.MLP_PARAM_GRID["alpha"]


def test_train_test_dates():
    assert config.TRAIN_END < config.TEST_START


def test_quick_settings():
    assert config.QUICK_SAMPLE_SIZE > 1000
    assert set(config.QUICK_DEGRADATION_FACTORS).issubset(set(config.DEGRADATION_FACTORS))
