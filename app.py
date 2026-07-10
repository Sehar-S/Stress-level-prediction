import streamlit as st
import pandas as pd
import joblib
import time

# Load model
model = joblib.load('stress_model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.set_page_config(page_title="Stress Level Predictor", page_icon="🧘", layout="centered")

# ---------- CUSTOM CSS (Modern + Animated) ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.title-container {
    text-align: center;
    padding: 20px 0 10px 0;
    animation: fadeInDown 1s ease-out;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    background: linear-gradient(90deg, #7ee8fa, #eec0c6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

.subtitle {
    color: #cfd8dc;
    font-size: 16px;
    margin-bottom: 25px;
}

.glass-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
    animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

div.stButton > button {
    background: linear-gradient(90deg, #7ee8fa, #a1c4fd);
    color: #0f2027;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    padding: 12px 30px;
    font-size: 16px;
    width: 100%;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 20px rgba(126, 232, 250, 0.6);
}

.result-box {
    text-align: center;
    padding: 25px;
    border-radius: 18px;
    animation: popIn 0.5s ease-out;
    margin-top: 15px;
}

@keyframes popIn {
    0% { opacity: 0; transform: scale(0.8); }
    100% { opacity: 1; transform: scale(1); }
}

.result-high { background: rgba(255, 82, 82, 0.15); border: 1px solid #ff5252; }
.result-medium { background: rgba(255, 193, 7, 0.15); border: 1px solid #ffc107; }
.result-low { background: rgba(76, 175, 80, 0.15); border: 1px solid #4caf50; }

.result-text {
    font-size: 30px;
    font-weight: 700;
    color: white;
}

label, .stSlider label, .stSelectbox label {
    color: #e0f7fa !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("""
<div class="title-container">
    <div class="main-title">🧘 Stress Level Predictor</div>
    <div class="subtitle">AI-powered stress assessment based on your lifestyle habits</div>
</div>
""", unsafe_allow_html=True)

# ---------- INPUT CARD ----------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    age = st.slider("Age", 18, 65, 30)
    sleep_duration = st.slider("Sleep Duration (hours)", 3.0, 10.0, 7.0, step=0.1)
    quality_of_sleep = st.slider("Quality of Sleep (1-10)", 1, 10, 6)
    physical_activity = st.slider("Physical Activity (min/day)", 0, 120, 45)
with col2:
    heart_rate = st.slider("Heart Rate (bpm)", 50, 120, 70)
    daily_steps = st.slider("Daily Steps", 1000, 15000, 6000)
    gender = st.selectbox("Gender", ["Male", "Female"])
    bmi_category = st.selectbox("BMI Category", ["Normal", "Overweight", "Obese"])

occupation = st.selectbox("Occupation", [
    "Software Engineer", "Doctor", "Sales Representative", "Teacher", "Nurse",
    "Engineer", "Accountant", "Scientist", "Lawyer", "Salesperson", "Manager"
])

predict_btn = st.button("✨ Predict My Stress Level")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- PREDICTION ----------
if predict_btn:
    with st.spinner("Analyzing your lifestyle..."):
        time.sleep(0.8)

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
        input_df = input_df[model_columns]

        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]

    # Result box styling
    style_map = {"High": "result-high", "Medium": "result-medium", "Low": "result-low"}
    emoji_map = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

    st.markdown(f"""
    <div class="result-box {style_map[prediction]}">
        <div class="result-text">{emoji_map[prediction]} Stress Level: {prediction}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Confidence chart
    prob_df = pd.DataFrame({'Stress Level': model.classes_, 'Probability': probabilities})
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("**Confidence Breakdown**")
    st.bar_chart(prob_df.set_index('Stress Level'))
    st.markdown('</div>', unsafe_allow_html=True)

    # Tips
    if prediction == "High":
        st.error("💡 **Tip:** Try to get 7-8 hours of sleep, exercise daily, and take regular breaks during work.")
    elif prediction == "Medium":
        st.warning("💡 **Tip:** Bring a bit more balance to your routine — improve both sleep and physical activity.")
    else:
        st.success("💡 **Great!** Keep maintaining your current lifestyle — it's healthy!")
