"""Hyperparameter tuning for ML models."""

import pandas as pd
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit

from .config import (
    GRID_SEARCH_CV_FOLDS,
    MLP_PARAM_GRID,
    RANDOM_STATE,
    RF_PARAM_GRID,
    TUNING_MAX_SAMPLES,
)


def _subsample_for_tuning(
    features: pd.DataFrame,
    target: pd.Series,
    max_samples: int,
) -> tuple[pd.DataFrame, pd.Series]:
    """Use the most recent rows for faster hyperparameter search."""
    if len(features) <= max_samples:
        return features, target
    return features.iloc[-max_samples:], target.iloc[-max_samples:]


def tune_random_forest(
    features: pd.DataFrame,
    target: pd.Series,
) -> dict:
    """Find best Random Forest parameters with time-series cross-validation."""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline

    x_tune, y_tune = _subsample_for_tuning(features, target, TUNING_MAX_SAMPLES)
    splitter = TimeSeriesSplit(n_splits=GRID_SEARCH_CV_FOLDS)

    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1)),
    ])

    param_grid = {
        "model__n_estimators": RF_PARAM_GRID["n_estimators"],
        "model__max_depth": RF_PARAM_GRID["max_depth"],
        "model__min_samples_leaf": RF_PARAM_GRID["min_samples_leaf"],
    }

    search = GridSearchCV(
        pipeline,
        param_grid,
        cv=splitter,
        scoring="neg_mean_absolute_error",
        n_jobs=-1,
    )
    search.fit(x_tune, y_tune)
    best = search.best_params_
    return {
        "n_estimators": best["model__n_estimators"],
        "max_depth": best["model__max_depth"],
        "min_samples_leaf": best["model__min_samples_leaf"],
    }


def tune_mlp(
    features: pd.DataFrame,
    target: pd.Series,
) -> dict:
    """Find best MLP parameters with time-series cross-validation."""
    from sklearn.impute import SimpleImputer
    from sklearn.neural_network import MLPRegressor
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    x_tune, y_tune = _subsample_for_tuning(features, target, TUNING_MAX_SAMPLES)
    splitter = TimeSeriesSplit(n_splits=GRID_SEARCH_CV_FOLDS)

    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("model", MLPRegressor(random_state=RANDOM_STATE, max_iter=500)),
    ])

    param_grid = {
        "model__hidden_layer_sizes": MLP_PARAM_GRID["hidden_layer_sizes"],
        "model__alpha": MLP_PARAM_GRID["alpha"],
        "model__learning_rate_init": MLP_PARAM_GRID["learning_rate_init"],
    }

    search = GridSearchCV(
        pipeline,
        param_grid,
        cv=splitter,
        scoring="neg_mean_absolute_error",
        n_jobs=-1,
    )
    search.fit(x_tune, y_tune)

    best = search.best_params_
    return {
        "hidden_layer_sizes": best["model__hidden_layer_sizes"],
        "alpha": best["model__alpha"],
        "learning_rate_init": best["model__learning_rate_init"],
    }
