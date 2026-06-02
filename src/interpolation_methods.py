"""Classical interpolation methods for time series."""

import pandas as pd

METHOD_REGISTRY: dict[str, str] = {
    "forward_fill": "Forward fill",
    "linear": "Linear interpolation",
    "time": "Time interpolation",
    "cubic": "Cubic interpolation",
    "spline": "Spline interpolation",
}


def forward_fill(series: pd.Series) -> pd.Series:
    """Fill missing values with the previous observed value."""
    filled = series.ffill().bfill()
    filled.name = series.name
    return filled


def linear_interpolation(series: pd.Series) -> pd.Series:
    """Linear interpolation between observed values."""
    filled = series.interpolate(method="linear").bfill().ffill()
    filled.name = series.name
    return filled


def time_interpolation(series: pd.Series) -> pd.Series:
    """Time-aware interpolation using the datetime index."""
    filled = series.interpolate(method="time").bfill().ffill()
    filled.name = series.name
    return filled


def cubic_interpolation(series: pd.Series) -> pd.Series:
    """Cubic spline interpolation between observed values."""
    filled = series.interpolate(method="cubic").bfill().ffill()
    filled.name = series.name
    return filled


def spline_interpolation(series: pd.Series) -> pd.Series:
    """Spline interpolation of order 3."""
    filled = series.interpolate(method="spline", order=3).bfill().ffill()
    filled.name = series.name
    return filled


_METHOD_FUNCTIONS = {
    "forward_fill": forward_fill,
    "linear": linear_interpolation,
    "time": time_interpolation,
    "cubic": cubic_interpolation,
    "spline": spline_interpolation,
}


def interpolate(series: pd.Series, method: str) -> pd.Series:
    """Reconstruct missing values using a registered classical method."""
    if method not in _METHOD_FUNCTIONS:
        raise ValueError(f"Unknown method: {method}. Choose from {list(_METHOD_FUNCTIONS)}")

    return _METHOD_FUNCTIONS[method](series)


def list_classical_methods() -> list[str]:
    """Return available classical method keys."""
    return list(_METHOD_FUNCTIONS.keys())
