"""
app.py — Main Streamlit entry point
Real-Time Accident Risk Prediction + 3D World Map

Pages:
  1. Home        — streamed per-point prediction (original)
  2. World Map   — 3D interactive globe with risk dots
"""

import streamlit as st
import os

st.set_page_config(
    page_title="Accident Risk Predictor",
    page_icon="🚦",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🚦 Accident Risk")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Live Predictor", "🌍 World Map (3D)"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Real-Time Accident Risk Prediction System")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: LIVE PREDICTOR
# ─────────────────────────────────────────────────────────────────────────────
if page == "🏠 Live Predictor":
    import time
    import sys
    import numpy as np
    from collections import deque

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(BASE_DIR)

    st.title("🚦 Real-Time Accident Risk Prediction")
    st.markdown("Streaming GPS sensor data through LSTM model to predict accident risk in real-time.")

    # Try to load model (graceful fallback if data/model missing)
    model = None
    try:
        from tensorflow.keras.models import load_model as tf_load
        MODEL_PATH = os.path.join(BASE_DIR, "models", "saved_model", "accident_lstm.h5")
        model = tf_load(MODEL_PATH, compile=False)
        st.success("✅ Model loaded")
    except Exception as e:
        st.warning(f"⚠️ Could not load model: {e}. Running in demo mode.")

    # Try to load real data stream
    gps_stream_fn = None
    df = None
    try:
        from streaming.gps_simulator import gps_stream, df as gps_df
        gps_stream_fn = gps_stream
        df = gps_df
        st.info(f"📡 Dataset loaded: {len(df)} rows")
    except Exception as e:
        st.warning(f"⚠️ GPS data not available: {e}. Using synthetic stream.")

    # ── Demo / synthetic fallback ──────────────────────────────────────────
    def synthetic_stream():
        import random, datetime
        while True:
            yield {
                "time": datetime.datetime.now(),
                "lat": random.uniform(25, 49),
                "lng": random.uniform(-125, -65),
                "visibility": random.uniform(1, 10),
                "wind_speed": random.uniform(0, 40),
                "temperature": random.uniform(20, 100),
                "precipitation": random.uniform(0, 1),
            }

    def prepare_features(point):
        hour = point["time"].hour
        is_night = 1 if (hour >= 19 or hour <= 6) else 0
        is_weekend = 1 if point["time"].weekday() >= 5 else 0
        return [
            hour, is_night, is_weekend,
            round(point["lat"], 2), round(point["lng"], 2),
            0,  # weather_condition_encoded
            point["visibility"], point["wind_speed"],
            point["temperature"], point["precipitation"],
            1,
        ]

    # ── UI ──────────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    location_box = col1.empty()
    risk_box     = col2.empty()
    progress     = st.empty()
    history_box  = st.empty()

    SEQ_LEN = 10
    buffer  = deque(maxlen=SEQ_LEN)
    history = []

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()

    stream = (gps_stream_fn(df, delay=1) if gps_stream_fn else synthetic_stream())
    max_steps = 30
    step = 0

    for point in stream:
        if step >= max_steps:
            st.success("✅ Stream demo complete. Refresh to restart.")
            break

        features = prepare_features(point)
        buffer.append(features)
        step += 1

        location_box.metric("📍 Location", f"{point['lat']:.2f}°, {point['lng']:.2f}°")
        progress.progress(step / max_steps, text=f"Processing point {step}/{max_steps}")

        if len(buffer) == SEQ_LEN:
            X = np.array(buffer).reshape(1, SEQ_LEN, -1)
            X = scaler.fit_transform(X.reshape(-1, X.shape[-1])).reshape(X.shape)

            if model:
                pred = model.predict(X, verbose=0)[0][0]
            else:
                # Synthetic prediction
                import random
                pred = random.uniform(0.5, 3.5)

            if pred < 1.8:
                risk, color, emoji = "LOW RISK",    "#22ff88", "🟢"
            elif pred < 2.8:
                risk, color, emoji = "MEDIUM RISK", "#ffaa00", "🟠"
            else:
                risk, color, emoji = "HIGH RISK",   "#ff3366", "🔴"

            risk_box.metric(f"{emoji} Risk Level", risk, f"score: {pred:.2f}")
            history.append({"lat": point["lat"], "lng": point["lng"], "risk": risk})

            if len(history) > 5:
                rows = "\n".join([
                    f"- {h['emoji'] if 'emoji' in h else h['risk']} @ {h['lat']:.2f}, {h['lng']:.2f}"
                    for h in history[-5:]
                ])
                history_box.markdown(f"**Recent predictions:**\n{rows}")

        time.sleep(1)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: WORLD MAP
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🌍 World Map (3D)":
    st.markdown("""
<style>
  header[data-testid="stHeader"]     { display:none; }
  .block-container                    { padding:0 !important; max-width:100%; }
  [data-testid="stAppViewContainer"]  { background:#000408; }
  iframe                              { border:none !important; }
  section[data-testid="stSidebar"]   { background:#00080f; }
</style>
""", unsafe_allow_html=True)

    # Sidebar controls for globe
    with st.sidebar:
        st.markdown("### 🌍 Globe Settings")
        show_high   = st.toggle("🔴 High Risk",   value=True)
        show_medium = st.toggle("🟠 Medium Risk", value=True)
        show_low    = st.toggle("🟢 Low Risk",    value=True)
        st.markdown("---")
        event_density = st.slider("Event Density", 20, 200, 80, 10)
        rotate_speed  = st.slider("Rotate Speed (×10⁻³)", 0, 10, 2)
        show_grid     = st.toggle("Grid Lines", value=True)
        show_stars    = st.toggle("Star Field", value=True)
        st.markdown("---")
        st.markdown("🖱 **Drag** — rotate  \n🖱 **Scroll** — zoom  \n🖱 **Hover** — inspect")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    HTML_PATH = os.path.join(BASE_DIR, "static", "world_map_3d.html")

    with open(HTML_PATH, "r") as f:
        html_content = f.read()

    config_script = f"""
<script>
window.GLOBE_CONFIG = {{
  showHigh:     {'true' if show_high   else 'false'},
  showMedium:   {'true' if show_medium else 'false'},
  showLow:      {'true' if show_low    else 'false'},
  eventDensity: {event_density},
  rotateSpeed:  {rotate_speed / 1000},
  showGrid:     {'true' if show_grid  else 'false'},
  showStars:    {'true' if show_stars else 'false'},
}};
</script>
"""
    html_content = html_content.replace("</head>", config_script + "\n</head>")
    st.components.v1.html(html_content, height=960, scrolling=False)
