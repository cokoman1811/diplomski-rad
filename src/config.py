"""Experiment configuration constants."""

JENA_RAW_FILENAME = "jena_climate_2009_2016.csv"
DATETIME_COLUMN = "Date Time"
TEMPERATURE_COLUMN = "T (degC)"

COVARIATE_COLUMNS = [
    "p (mbar)",
    "rh (%)",
    "wv (m/s)",
    "max. wv (m/s)",
]

DEGRADATION_FACTORS = [2, 3, 6, 12]
QUICK_DEGRADATION_FACTORS = [2, 6]

CLASSICAL_METHODS = [
    "forward_fill",
    "linear",
    "time",
    "cubic",
    "spline",
]

ML_METHODS = [
    "random_forest",
    "mlp",
]

ALL_METHODS = CLASSICAL_METHODS + ML_METHODS

TRAIN_END = "2014-12-31 23:50:00"
TEST_START = "2015-01-01 00:00:00"

RANDOM_STATE = 42
QUICK_SAMPLE_SIZE = 10_000
LAG_STEPS = [1, 2, 3, 6]
ROLLING_WINDOWS = [3, 6, 12]

RF_PARAM_GRID = {
    "n_estimators": [50, 100],
    "max_depth": [10, 20, None],
    "min_samples_leaf": [1, 2],
}

MLP_PARAM_GRID = {
    "hidden_layer_sizes": [(64,), (128, 64)],
    "alpha": [0.0001, 0.001],
    "learning_rate_init": [0.001, 0.01],
}

GRID_SEARCH_CV_FOLDS = 3
TUNING_MAX_SAMPLES = 20_000
