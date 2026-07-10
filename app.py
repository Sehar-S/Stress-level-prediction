import streamlit as st
import pandas as pd
import joblib

# Model aur columns load karo
model = joblib.load('stress_model.pkl')
model_columns = joblib.load('model_columns.pkl')

# Page config
st.set_page_config(page_title="Stress Level Predictor", page_icon="🧘", layout="centered")

st.title("🧘 Stress Level Predictor")
st.write("Apni lifestyle habits enter karo aur apna stress level check karo")

# Sidebar mein inputs lo
st.header("Apni Details Enter Karo")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 65, 30)
    sleep_duration = st.slider("Sleep Duration (hours)", 3.0, 10.0, 7.0, step=0.1)
    quality_of_sleep = st.slider("Quality of Sleep (1-10)", 1, 10, 6)
    physical_activity = st.slider("Physical Activity Level (min/day)", 0, 120, 45)

with col2:
    heart_rate = st.slider("Heart Rate (bpm)", 50, 120, 70)
    daily_steps = st.slider("Daily Steps", 1000, 15000, 6000)
    gender = st.selectbox("Gender", ["Male", "Female"])
    bmi_category = st.selectbox("BMI Category", ["Normal", "Overweight", "Obese"])

occupation = st.selectbox("Occupation", [
    "Software Engineer", "Doctor", "Sales Representative", "Teacher", "Nurse",
    "Engineer", "Accountant", "Scientist", "Lawyer", "Salesperson", "Manager"
])

# Predict button
if st.button("Predict Stress Level"):
    # Input ko dataframe mein convert karo
    input_dict = {
        'Age': age,
        'Sleep Duration': sleep_duration,
        'Quality of Sleep': quality_of_sleep,
        'Physical Activity Level': physical_activity,
        'Heart Rate': heart_rate,
        'Daily Steps': daily_steps,
        'Gender_Male': 1 if gender == 'Male' else 0,
    }

    # Occupation aur BMI ke liye one-hot columns manually set karo
    for col in model_columns:
        if col.startswith('Occupation_'):
            input_dict[col] = 1 if col == f'Occupation_{occupation}' else 0
        elif col.startswith('BMI Category_'):
            input_dict[col] = 1 if col == f'BMI Category_{bmi_category}' else 0

    # Missing columns ko 0 se fill karo
    input_df = pd.DataFrame([input_dict])
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Column order match karo model ke sath
    input_df = input_df[model_columns]

    # Prediction
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    # Result dikhao with color
    color_map = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
    st.subheader(f"{color_map[prediction]} Stress Level: {prediction}")

    # Confidence chart
    prob_df = pd.DataFrame({
        'Stress Level': model.classes_,
        'Probability': probabilities
    })
    st.bar_chart(prob_df.set_index('Stress Level'))

    # Tips based on result
    if prediction == "High":
        st.warning("💡 Tips: Neend barhao, exercise karo, aur breaks lo kaam ke doran.")
    elif prediction == "Medium":
        st.info("💡 Tips: Apni routine mein thora aur balance layo.")
    else:
        st.success("💡 Great! Apni current lifestyle maintain karo.")