"""Feature engineering for machine learning models."""

import numpy as np
import pandas as pd

from .config import LAG_STEPS, ROLLING_WINDOWS, TEST_START, TRAIN_END


def _cyclic_features(index: pd.DatetimeIndex) -> pd.DataFrame:
    """Create cyclic time features from datetime index."""
    hour = index.hour + index.minute / 60.0
    day_of_year = index.dayofyear

    features = pd.DataFrame(index=index)
    features["hour_sin"] = np.sin(2 * np.pi * hour / 24.0)
    features["hour_cos"] = np.cos(2 * np.pi * hour / 24.0)
    features["doy_sin"] = np.sin(2 * np.pi * day_of_year / 365.25)
    features["doy_cos"] = np.cos(2 * np.pi * day_of_year / 365.25)
    features["hour"] = index.hour
    features["dayofyear"] = day_of_year
    features["month"] = index.month
    features["weekday"] = index.weekday
    return features


def _lag_features(series: pd.Series, lags: list[int]) -> pd.DataFrame:
    """Create lag features from the observed temperature series."""
    features = pd.DataFrame(index=series.index)
    for lag in lags:
        features[f"lag_{lag}"] = series.shift(lag)
    return features


def _rolling_features(series: pd.Series, windows: list[int]) -> pd.DataFrame:
    """Create rolling statistics using only past observed values."""
    features = pd.DataFrame(index=series.index)
    for window in windows:
        rolling = series.rolling(window=window, min_periods=1)
        features[f"roll_mean_{window}"] = rolling.mean()
        features[f"roll_std_{window}"] = rolling.std().fillna(0.0)
    return features


def build_feature_matrix(
    dataset: pd.DataFrame,
    degraded_temperature: pd.Series,
) -> pd.DataFrame:
    """
    Build ML features from time, lags, rolling stats and covariates.

    Covariates are always available. Lag and rolling features use the
    degraded temperature so missing target values are not leaked.
    """
    time_features = _cyclic_features(degraded_temperature.index)
    lag_features = _lag_features(degraded_temperature, LAG_STEPS)
    rolling_features = _rolling_features(degraded_temperature, ROLLING_WINDOWS)

    covariates = dataset.drop(columns=["temperature"], errors="ignore")
    features = pd.concat(
        [time_features, lag_features, rolling_features, covariates],
        axis=1,
    )
    return features


def build_train_test_masks(index: pd.DatetimeIndex) -> tuple[pd.Series, pd.Series]:
    """Return boolean masks for train and test periods."""
    train_end = pd.Timestamp(TRAIN_END)
    test_start = pd.Timestamp(TEST_START)

    train_mask = pd.Series(index <= train_end, index=index, name="train")
    test_mask = pd.Series(index >= test_start, index=index, name="test")
    return train_mask, test_mask


def get_training_rows(
    degraded: pd.Series,
    train_mask: pd.Series,
) -> pd.Series:
    """Observed target rows in the training period."""
    return degraded.notna() & train_mask


def get_prediction_rows(degraded: pd.Series) -> pd.Series:
    """Rows with missing target values."""
    return degraded.isna()
