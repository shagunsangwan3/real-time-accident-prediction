# 🚦 Real-Time Accident Risk Prediction System

A deep learning–based real-time accident risk prediction system that analyzes
live GPS and weather sensor data streams to continuously predict accident risk
severity using LSTM models.

---

## 📌 Project Overview

Road accidents are influenced by time, location, and environmental conditions.
This project simulates a real-time data pipeline and applies deep learning to
predict accident risk dynamically instead of static batch predictions.

The system processes live GPS coordinates, weather parameters, and temporal
features to estimate accident severity in real time.

---

## 🧠 Key Features

- Real-time accident risk prediction using LSTM
- Live GPS and weather data simulation
- Time-series sequence modeling with rolling windows
- Automated risk classification (Low / Medium / High)
- End-to-end pipeline from raw data to real-time inference

---

## 🏗️ System Architecture

1. **Data Source**
   - Historical US accident data (GPS, time, weather conditions)

2. **Streaming Simulation**
   - GPS and sensor data streamed sequentially to mimic real-time flow

3. **Feature Engineering**
   - Time-based features (hour, night flag, weekend)
   - Location-based features (latitude, longitude bins)
   - Weather features (visibility, wind speed, temperature, precipitation)

4. **Deep Learning Model**
   - LSTM-based sequence model
   - Rolling window predictions on temporal data

5. **Inference Engine**
   - Continuous risk prediction
   - Risk level classification

---

## 🔧 Tech Stack

- **Programming Language:** Python  
- **Deep Learning:** TensorFlow, Keras  
- **Model:** LSTM (Time-Series Neural Network)  
- **Data Processing:** Pandas, NumPy  
- **Scaling & Preprocessing:** Scikit-learn  
- **Visualization / UI:** Streamlit (optional)  
- **Verreal-time-accident-prediction/
├── data/
│ └── raw/
├── notebooks/
│ ├── eda.ipynb
│ └── model_training.ipynb
├── streaming/
│ └── gps_simulator.py
├── inference/
│ └── realtime_predictor.py
├── models/
│ └── accident_lstm.h5
├── app.py
├── README.md
├── requirements.txt
└── .gitignore


---

## 📊 Model Details

- **Model Type:** LSTM (Long Short-Term Memory)
- **Input:** Sequential GPS + weather data
- **Output:** Accident severity risk score
- **Prediction Type:** Continuous + Risk Classification

---

## 🚨 Risk Classification Logic

| Prediction Score | Risk Level |
|------------------|-----------|
| < 1.8 | Low Risk |
| 1.8 – 2.8 | Medium Risk |
| > 2.8 | High Risk |

---

## ▶️ How to Run

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt

2️⃣ Run real-time prediction
python inference/realtime_predictor.py

3️⃣ (Optional) Run UI
streamlit run app.py

📂 Dataset Information

Due to large file size, datasets are not included in this repository.

You can download similar datasets from:

Kaggle – US Accidents Dataset

Place the dataset inside:

data/raw/

🎯 Use Cases

Smart traffic monitoring systems

Accident prevention analytics

Intelligent transportation systems

Real-time risk assessment dashboards

🚀 Future Improvements

Integration with real GPS APIs

Real-time weather API support

Advanced deep learning models (GRU / Transformers)

Cloud deployment

👤 Author

Shagun Sangwan
Aspiring Data Scientist | Machine Learning & Deep Learning Enthusiast

GitHub: https://github.com/shagunsangwan3

⭐ If you find this project useful, give it a star!

---

## ✅ Why this README is STRONG

✔ Explains **what + why + how**  
✔ Shows **real-time ML system thinking**  
✔ Avoids fake claims  
✔ Recruiter-friendly language  
✔ Perfect for **Data Scientist / ML Intern** roles  

---

## 🔜 Next Steps (Tell me what you want)
1️⃣ Push this project to GitHub (I’ll guide commands)  
2️⃣ Add **resume bullet points** for this project  
3️⃣ Optimize README for **ATS keywords**  
4️⃣ Review all 3 projects together (final polish)

Just tell me 👍
sion Control:** Git, GitHub  

---

## 📂 Project Structure

