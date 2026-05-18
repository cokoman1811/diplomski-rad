"""Optional helper: download hourly Split weather data from Open-Meteo."""

import json
from urllib.request import urlopen

import pandas as pd

from .paths import RAW_DIR, ensure_project_dirs


def download_real_weather_data() -> pd.DataFrame:
    """
    Download historical hourly temperature data for Split, Croatia.

    Saves raw CSV to data/raw/real_weather_split_2024.csv.
    """
    ensure_project_dirs()

    latitude = 43.5081
    longitude = 16.4402
    start_date = "2024-01-01"
    end_date = "2024-12-31"

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        "&hourly=temperature_2m"
        "&timezone=Europe%2FBerlin"
    )

    print("Downloading real weather data...")
    print(url)

    response = urlopen(url)
    data = json.loads(response.read())

    df = pd.DataFrame({
        "timestamp": pd.to_datetime(data["hourly"]["time"]),
        "temperature": data["hourly"]["temperature_2m"],
    })

    output_path = RAW_DIR / "real_weather_split_2024.csv"
    df.to_csv(output_path, index=False)

    print("Download finished.")
    print(f"Saved file: {output_path}")
    print()
    print(df.head())
    return df


if __name__ == "__main__":
    download_real_weather_data()
