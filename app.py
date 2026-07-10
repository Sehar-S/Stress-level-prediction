
import streamlit as st
import pandas as pd
import joblib
import time

# Load model
model = joblib.load('stress_model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.set_page_config(page_title="Stress Level Predictor", page_icon="", layout="centered")

# ---------- CUSTOM CSS (Dark Navy Theme) ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #05070f, #0a0e1a, #0d1b2a, #10233a);
    background-size: 400% 400%;
    animation: gradientShift 18s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.title-container {
    text-align: center;
    padding: 25px 0 15px 0;
    animation: fadeInDown 1s ease-out;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}

.main-title {
    font-size: 40px;
    font-weight: 700;
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}

.subtitle {
    color: #8ba3c7;
    font-size: 15px;
    margin-bottom: 10px;
}

.glass-card {
    background: rgba(20, 35, 60, 0.45);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 26px;
    border: 1px solid rgba(79, 172, 254, 0.15);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
    margin-bottom: 20px;
    animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.section-label {
    color: #4facfe;
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

div.stButton > button {
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    color: #05070f;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    padding: 13px 30px;
    font-size: 16px;
    width: 100%;
    transition: all 0.3s ease;
    letter-spacing: 0.3px;
}

div.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px rgba(79, 172, 254, 0.5);
}

.result-box {
    text-align: center;
    padding: 28px;
    border-radius: 18px;
    animation: popIn 0.5s ease-out;
    margin-top: 15px;
}

@keyframes popIn {
    0% { opacity: 0; transform: scale(0.85); }
    100% { opacity: 1; transform: scale(1); }
}

.result-high { background: rgba(255, 82, 82, 0.12); border: 1px solid rgba(255, 82, 82, 0.4); }
.result-medium { background: rgba(255, 193, 7, 0.12); border: 1px solid rgba(255, 193, 7, 0.4); }
.result-low { background: rgba(56, 239, 125, 0.12); border: 1px solid rgba(56, 239, 125, 0.4); }

.result-text {
    font-size: 28px;
    font-weight: 700;
    color: #f0f4fa;
}

.result-sub {
    color: #8ba3c7;
    font-size: 14px;
    margin-top: 6px;
}

label, .stSlider label, .stSelectbox label {
    color: #c3d4ec !important;
    font-weight: 500 !important;
    font-size: 14px !important;
}

hr {
    border-color: rgba(79, 172, 254, 0.15);
}

/* Slider color */
.stSlider [data-baseweb="slider"] > div > div {
    background: linear-gradient(90deg, #4facfe, #00f2fe) !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("""
<div class="title-container">
    <div class="main-title"> Stress Level Predictor</div>
    <div class="subtitle">AI-powered stress assessment based on your lifestyle habits</div>
</div>
""", unsafe_allow_html=True)

# ---------- INPUT CARD ----------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">👤 Personal Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    age = st.slider("Age", 18, 65, 30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    bmi_category = st.selectbox("BMI Category", ["Normal", "Overweight", "Obese"])
with col2:
    occupation = st.selectbox("Occupation", [
        "Software Engineer", "Doctor", "Sales Representative", "Teacher", "Nurse",
        "Engineer", "Accountant", "Scientist", "Lawyer", "Salesperson", "Manager"
    ])

st.markdown('<div class="section-label" style="margin-top:20px;">😴 Sleep & Activity</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    sleep_duration = st.slider("Sleep Duration (hours)", 3.0, 10.0, 7.0, step=0.1)
    quality_of_sleep = st.slider("Quality of Sleep (1-10)", 1, 10, 6)
with col4:
    physical_activity = st.slider("Physical Activity (min/day)", 0, 120, 45)
    daily_steps = st.slider("Daily Steps", 1000, 15000, 6000)

st.markdown('<div class="section-label" style="margin-top:20px;">❤️ Vitals</div>', unsafe_allow_html=True)
heart_rate = st.slider("Heart Rate (bpm)", 50, 120, 70)

st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("✨ Predict My Stress Level")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- PREDICTION ----------
if predict_btn:
    with st.spinner("Analyzing your lifestyle..."):
        time.sleep(0.1)

        input_dict = {
            'Age': age, 'Sleep Duration': sleep_duration, 'Quality of Sleep': quality_of_sleep,
            'Physical Activity Level': physical_activity, 'Heart Rate': heart_rate,
            'Daily Steps': daily_steps, 'Gender_Male': 1 if gender == 'Male' else 0,
        }
        for col in model_columns:
            if col.startswith('Occupation_'):
                input_dict[col] = 1 if col == f'Occupation_{occupation}' else 0
            elif col.startswith('BMI Category_'):
                input_dict[col] = 1 if col == f'BMI Category_{bmi_category}' else 0

        input_df = pd.DataFrame([input_dict])
        for col in model_columns:
            if col not in input_df.columns:
                input_df[col] = 0

if predict_btn:
    st.write("Debug: Button clicked, starting prediction...")  
    with st.spinner("Analyzing your lifestyle..."):
