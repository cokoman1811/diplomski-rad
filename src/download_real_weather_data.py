import json
import os
from urllib.request import urlopen

import pandas as pd


def download_real_weather_data():
    """
    Downloads real historical hourly temperature data for Split, Croatia
    from the Open-Meteo Historical Weather API.

    Output file:
    data/real_weather_split_2024.csv
    """

    os.makedirs("data", exist_ok=True)

    # Coordinates for Split, Croatia
    latitude = 43.5081
    longitude = 16.4402

    # One full year of data
    start_date = "2024-01-01"
    end_date = "2024-12-31"

    # Open-Meteo Historical Weather API URL
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

    timestamps = data["hourly"]["time"]
    temperatures = data["hourly"]["temperature_2m"]

    df = pd.DataFrame({
        "timestamp": pd.to_datetime(timestamps),
        "temperature": temperatures
    })

    output_path = "data/real_weather_split_2024.csv"
    df.to_csv(output_path, index=False)

    print("Download finished.")
    print(f"Saved file: {output_path}")
    print()
    print(df.head())


if __name__ == "__main__":
    download_real_weather_data()