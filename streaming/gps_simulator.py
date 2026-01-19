import pandas as pd
import time
import os

# ---------- PATH SETUP ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "US_Accidents_March23.csv")

# ---------- LOAD DATA ----------
cols = [
    "Start_Time",
    "Start_Lat",
    "Start_Lng",
    "Visibility(mi)",
    "Wind_Speed(mph)",
    "Temperature(F)",
    "Precipitation(in)"
]

df = pd.read_csv(DATA_PATH, usecols=cols)
df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors="coerce")
df = df.dropna().reset_index(drop=True)

# ---------- GPS STREAM ----------
def gps_stream(df, delay=1):
    """
    Simulates real-time GPS + Sensor data
    """
    for _, row in df.iterrows():
        data_point = {
            "time": row["Start_Time"],
            "lat": row["Start_Lat"],
            "lng": row["Start_Lng"],
            "visibility": row["Visibility(mi)"],
            "wind_speed": row["Wind_Speed(mph)"],
            "temperature": row["Temperature(F)"],
            "precipitation": row["Precipitation(in)"]
        }

        yield data_point
        time.sleep(delay)

# ---------- TEST ----------
if __name__ == "__main__":
    stream = gps_stream(df, delay=1)

    for i, point in enumerate(stream):
        print(point)
        if i == 5:
            break
