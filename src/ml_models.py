"""Machine learning models for temperature reconstruction."""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .config import RANDOM_STATE
from .hyperparameter_tuning import tune_mlp, tune_random_forest


def predict_random_forest(
    features: pd.DataFrame,
    target: pd.Series,
    train_rows: pd.Series,
    predict_rows: pd.Series,
    params: dict | None = None,
    tune: bool = True,
) -> tuple[pd.Series, dict]:
    """Train Random Forest on observed rows and predict missing values."""
    if params is None and tune:
        params = tune_random_forest(features.loc[train_rows], target.loc[train_rows])
    params = params or {"n_estimators": 100, "max_depth": 20, "min_samples_leaf": 1}

    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1, **params)),
    ])
    model.fit(features.loc[train_rows], target.loc[train_rows])

    reconstructed = target.copy()
    reconstructed.loc[predict_rows] = model.predict(features.loc[predict_rows])
    reconstructed.name = target.name
    return reconstructed, params


def predict_mlp(
    features: pd.DataFrame,
    target: pd.Series,
    train_rows: pd.Series,
    predict_rows: pd.Series,
    params: dict | None = None,
    tune: bool = True,
) -> tuple[pd.Series, dict]:
    """Train MLP on observed rows and predict missing values."""
    if params is None and tune:
        params = tune_mlp(features.loc[train_rows], target.loc[train_rows])
    params = params or {
        "hidden_layer_sizes": (128, 64),
        "alpha": 0.001,
        "learning_rate_init": 0.001,
    }

    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        (
            "model",
            MLPRegressor(
                hidden_layer_sizes=params["hidden_layer_sizes"],
                alpha=params["alpha"],
                learning_rate_init=params["learning_rate_init"],
                random_state=RANDOM_STATE,
                max_iter=500,
            ),
        ),
    ])

    pipeline.fit(features.loc[train_rows], target.loc[train_rows])

    reconstructed = target.copy()
    reconstructed.loc[predict_rows] = pipeline.predict(features.loc[predict_rows])
    reconstructed.name = target.name
    return reconstructed, params


def reconstruct_with_ml(
    method: str,
    features: pd.DataFrame,
    degraded: pd.Series,
    train_rows: pd.Series,
    predict_rows: pd.Series | None = None,
    params: dict | None = None,
    tune: bool = True,
) -> tuple[pd.Series, dict]:
    """Reconstruct missing temperature values with an ML model."""
    if predict_rows is None:
        predict_rows = degraded.isna()

    if method == "random_forest":
        return predict_random_forest(
            features, degraded, train_rows, predict_rows, params=params, tune=tune
        )
    if method == "mlp":
        return predict_mlp(
            features, degraded, train_rows, predict_rows, params=params, tune=tune
        )

    raise ValueError(f"Unknown ML method: {method}")
