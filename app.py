import streamlit as st
import time
import os
import sys
import numpy as np
from collections import deque
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# ---------- PATH SETUP ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# ---------- LOAD MODEL ----------
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "saved_model",
    "accident_lstm.h5"
)

model = load_model(MODEL_PATH, compile=False)

# ---------- IMPORT GPS STREAM ----------
from streaming.gps_simulator import gps_stream, df

# ---------- FEATURE FUNCTION ----------
def prepare_features(point):
    hour = point["time"].hour
    is_night = 1 if (hour >= 19 or hour <= 6) else 0
    is_weekend = 1 if point["time"].weekday() >= 5 else 0
    weather_condition_encoded = 0

    return [
        hour,
        is_night,
        is_weekend,
        round(point["lat"], 2),
        round(point["lng"], 2),
        weather_condition_encoded,
        point["visibility"],
        point["wind_speed"],
        point["temperature"],
        point["precipitation"],
        1
    ]

# ---------- UI ----------
st.set_page_config(page_title="Accident Risk Predictor", layout="centered")
st.title("🚦 Real-Time Accident Risk Prediction")

status = st.empty()
location = st.empty()
risk_box = st.empty()

SEQ_LEN = 10
buffer = deque(maxlen=SEQ_LEN)
scaler = MinMaxScaler()

stream = gps_stream(df, delay=1)

for point in stream:
    features = prepare_features(point)
    buffer.append(features)

    location.write(f"📍 Location: {point['lat']}, {point['lng']}")

    if len(buffer) == SEQ_LEN:
        X = np.array(buffer).reshape(1, SEQ_LEN, -1)
        X = scaler.fit_transform(
            X.reshape(-1, X.shape[-1])
        ).reshape(X.shape)

        pred = model.predict(X, verbose=0)[0][0]

        if pred < 1.8:
            risk = "🟢 LOW RISK"
        elif pred < 2.8:
            risk = "🟠 MEDIUM RISK"
        else:
            risk = "🔴 HIGH RISK"

        risk_box.subheader(risk)

    time.sleep(1)
