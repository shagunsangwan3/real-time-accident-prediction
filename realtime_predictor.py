# ===============================
# REAL-TIME ACCIDENT RISK PREDICTOR
# ===============================

import os
import sys
import numpy as np
from collections import deque
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# -------------------------------
# 1. PATH SETUP (MUST BE FIRST)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# -------------------------------
# 2. IMPORT GPS STREAM (AFTER PATH FIX)
# -------------------------------
from streaming.gps_simulator import gps_stream, df

# -------------------------------
# 3. LOAD TRAINED MODEL
# -------------------------------
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "saved_model",
    "accident_lstm.h5"
)

model = load_model(MODEL_PATH, compile=False)
print("✅ Model loaded successfully")

# -------------------------------
# 4. FEATURE PREPARATION FUNCTION
# -------------------------------
def prepare_features(point):
    hour = point["time"].hour
    is_night = 1 if (hour >= 19 or hour <= 6) else 0
    is_weekend = 1 if point["time"].weekday() >= 5 else 0

    # 🔹 placeholder to match training feature count
    weather_condition_encoded = 0

    features = [
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
        1  # accident_count placeholder
    ]

    return features

# -------------------------------
# 5. ROLLING BUFFER FOR LSTM
# -------------------------------
SEQ_LEN = 10
buffer = deque(maxlen=SEQ_LEN)
scaler = MinMaxScaler()

# -------------------------------
# 6. RISK CLASSIFICATION
# -------------------------------
def classify_risk(pred):
    if pred < 1.8:
        return "LOW RISK"
    elif pred < 2.8:
        return "MEDIUM RISK"
    else:
        return "HIGH RISK"

# -----------------------------------------
# 7. AUTO-STOP CONFIG (VERY IMPORTANT)
# -----------------------------------------
MAX_PREDICTIONS = 20   # ⬅️ change this number anytime
prediction_count = 0

# -----------------------------------------
# 8. REAL-TIME PREDICTION LOOP
# -----------------------------------------
if __name__ == "__main__":
    print("🚦 Starting real-time prediction...\n")

    stream = gps_stream(df, delay=1)

    for point in stream:

        # 🔴 AUTO STOP
        if prediction_count >= MAX_PREDICTIONS:
            print("\n✅ Prediction finished. Stream stopped safely.")
            break

        features = prepare_features(point)
        buffer.append(features)

        if len(buffer) == SEQ_LEN:
            X = np.array(buffer).reshape(1, SEQ_LEN, -1)

            X = scaler.fit_transform(
                X.reshape(-1, X.shape[-1])
            ).reshape(X.shape)

            prediction = model.predict(X, verbose=0)[0][0]
            risk = classify_risk(prediction)

            print(
                "LAT:", point["lat"],
                "LNG:", point["lng"],
                "RISK:", risk
            )

            prediction_count += 1

        time.sleep(1)

