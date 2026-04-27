import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


def create_folders():
    os.makedirs("data", exist_ok=True)
    os.makedirs("figures", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("models", exist_ok=True)


def create_synthetic_temperature_data():
    """
    Creates artificial hourly temperature data.
    This is useful because we know the real values before removing some of them.
    """
    np.random.seed(42)

    timestamps = pd.date_range(start="2024-01-01", periods=1000, freq="h")

    time_index = np.arange(len(timestamps))

    trend = np.linspace(10, 20, len(timestamps))
    daily_pattern = 5 * np.sin(2 * np.pi * time_index / 24)
    weekly_pattern = 2 * np.sin(2 * np.pi * time_index / (24 * 7))
    noise = np.random.normal(0, 1.2, len(timestamps))

    temperature = trend + daily_pattern + weekly_pattern + noise

    df = pd.DataFrame({
        "timestamp": timestamps,
        "temperature": temperature
    })

    df.to_csv("data/original_temperature_data.csv", index=False)

    return df


def add_missing_values(df, missing_ratio):
    """
    Randomly removes a percentage of values from the temperature column.
    """
    df_missing = df.copy()

    np.random.seed(42)

    number_of_missing_values = int(len(df_missing) * missing_ratio)

    missing_indices = np.random.choice(
        df_missing.index,
        size=number_of_missing_values,
        replace=False
    )

    df_missing.loc[missing_indices, "temperature"] = np.nan

    return df_missing, missing_indices


def linear_interpolation(df_missing):
    df_filled = df_missing.copy()

    df_filled["temperature"] = df_filled["temperature"].interpolate(method="linear")
    df_filled["temperature"] = df_filled["temperature"].bfill().ffill()

    return df_filled


def spline_interpolation(df_missing):
    df_filled = df_missing.copy()

    df_filled["temperature"] = df_filled["temperature"].interpolate(
        method="spline",
        order=3
    )

    df_filled["temperature"] = df_filled["temperature"].bfill().ffill()

    return df_filled


def moving_average_interpolation(df_missing):
    df_filled = df_missing.copy()

    rolling_average = df_filled["temperature"].rolling(
        window=5,
        min_periods=1,
        center=True
    ).mean()

    df_filled["temperature"] = df_filled["temperature"].fillna(rolling_average)
    df_filled["temperature"] = df_filled["temperature"].interpolate(method="linear")
    df_filled["temperature"] = df_filled["temperature"].bfill().ffill()

    return df_filled


def knn_imputation(df_missing):
    df_temp = df_missing.copy()

    df_temp["hour"] = df_temp["timestamp"].dt.hour
    df_temp["dayofyear"] = df_temp["timestamp"].dt.dayofyear
    df_temp["time_index"] = np.arange(len(df_temp))

    imputer = KNNImputer(n_neighbors=5)

    imputed_values = imputer.fit_transform(
        df_temp[["temperature", "hour", "dayofyear", "time_index"]]
    )

    df_filled = df_missing.copy()
    df_filled["temperature"] = imputed_values[:, 0]

    return df_filled


def random_forest_imputation(df_missing):
    df_temp = df_missing.copy()

    df_temp["hour"] = df_temp["timestamp"].dt.hour
    df_temp["dayofyear"] = df_temp["timestamp"].dt.dayofyear
    df_temp["time_index"] = np.arange(len(df_temp))

    train_data = df_temp[df_temp["temperature"].notna()]
    missing_data = df_temp[df_temp["temperature"].isna()]

    features = ["hour", "dayofyear", "time_index"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(train_data[features], train_data["temperature"])

    predicted_values = model.predict(missing_data[features])

    df_filled = df_missing.copy()
    df_filled.loc[df_filled["temperature"].isna(), "temperature"] = predicted_values

    return df_filled


def evaluate_method(original_df, filled_df, missing_indices):
    real_values = original_df.loc[missing_indices, "temperature"]
    predicted_values = filled_df.loc[missing_indices, "temperature"]

    mae = mean_absolute_error(real_values, predicted_values)
    rmse = np.sqrt(mean_squared_error(real_values, predicted_values))

    return mae, rmse


def plot_original_data(original_df):
    plt.figure(figsize=(14, 6))
    plt.plot(original_df["timestamp"], original_df["temperature"])
    plt.title("Original synthetic temperature data")
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.tight_layout()
    plt.savefig("figures/original_temperature_data.png")
    plt.close()


def plot_method_result(original_df, missing_df, filled_df, method_name, missing_ratio):
    """
    Saves a graph that compares original data, missing data and reconstructed data.
    Only the first 200 points are shown to keep the graph readable.
    """
    original_short = original_df.iloc[:200]
    missing_short = missing_df.iloc[:200]
    filled_short = filled_df.iloc[:200]

    plt.figure(figsize=(14, 6))

    plt.plot(
        original_short["timestamp"],
        original_short["temperature"],
        label="Original data"
    )

    plt.scatter(
        missing_short["timestamp"],
        missing_short["temperature"],
        s=12,
        label="Data with missing values"
    )

    plt.plot(
        filled_short["timestamp"],
        filled_short["temperature"],
        label=f"{method_name} reconstruction"
    )

    plt.title(f"{method_name} - {int(missing_ratio * 100)}% missing values")
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.legend()
    plt.tight_layout()

    file_name = method_name.lower().replace(" ", "_")
    plt.savefig(f"figures/{file_name}_{int(missing_ratio * 100)}_percent.png")
    plt.close()


def main():
    create_folders()

    original_df = create_synthetic_temperature_data()
    plot_original_data(original_df)

    methods = {
        "Linear interpolation": linear_interpolation,
        "Spline interpolation": spline_interpolation,
        "Moving average": moving_average_interpolation,
        "KNN imputation": knn_imputation,
        "Random Forest": random_forest_imputation
    }

    missing_ratios = [0.10, 0.20, 0.30]

    results = []

    for missing_ratio in missing_ratios:
        missing_df, missing_indices = add_missing_values(original_df, missing_ratio)

        missing_df.to_csv(
            f"data/temperature_missing_{int(missing_ratio * 100)}_percent.csv",
            index=False
        )

        for method_name, method_function in methods.items():
            filled_df = method_function(missing_df)

            mae, rmse = evaluate_method(
                original_df,
                filled_df,
                missing_indices
            )

            results.append({
                "missing_percentage": int(missing_ratio * 100),
                "method": method_name,
                "MAE": round(mae, 4),
                "RMSE": round(rmse, 4)
            })

            plot_method_result(
                original_df,
                missing_df,
                filled_df,
                method_name,
                missing_ratio
            )

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(["missing_percentage", "RMSE"])

    results_df.to_csv("reports/results.csv", index=False)

    print("\nExperiment finished successfully.")
    print("\nResults:")
    print(results_df)


if __name__ == "__main__":
    main()