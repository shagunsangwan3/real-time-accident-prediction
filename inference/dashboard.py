"""
dashboard.py — 3D World Map view for Real-Time Accident Risk Prediction
Run with:  streamlit run inference/dashboard.py
"""

import streamlit as st
import os

st.set_page_config(
    page_title="Accident Risk · Global Map",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject minimal CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
  header[data-testid="stHeader"]     { display:none; }
  .block-container                    { padding:0 !important; max-width:100%; }
  [data-testid="stAppViewContainer"]  { background:#000408; }
  iframe                              { border:none !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar controls ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Globe Controls")

    show_high   = st.toggle("🔴 Show High Risk",   value=True)
    show_medium = st.toggle("🟠 Show Medium Risk", value=True)
    show_low    = st.toggle("🟢 Show Low Risk",    value=True)

    st.divider()
    st.markdown("### 📡 Simulation")
    event_density = st.slider("Event Density", 20, 200, 80, 10)
    rotate_speed  = st.slider("Auto-Rotate Speed (×10⁻³)", 0, 10, 2)
    show_grid     = st.toggle("Grid Lines", value=True)
    show_stars    = st.toggle("Star Field", value=True)

    st.divider()
    st.markdown("""
**Controls:**  
🖱 **Drag** — rotate  
🖱 **Scroll** — zoom  
🖱 **Hover dot** — inspect
    """)

# ── Load and patch HTML ───────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

# Render as full-page iframe
st.components.v1.html(html_content, height=920, scrolling=False)
