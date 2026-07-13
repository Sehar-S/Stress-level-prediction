# 🧘 Stress Level Predictor

An AI-powered web application that predicts a person's stress level (Low, Medium, or High) based on their daily lifestyle habits. Built as the first project in a machine learning series exploring different algorithms across healthcare use cases.

🔗 **Live App:**  https://stress-level-prediction-ltbzozctatdbbxdah3f8fj.streamlit.app/

---

##  What This Project Does

Stress is closely linked to everyday habits like sleep, physical activity, and overall health. This app takes a person's lifestyle details as input and predicts their likely stress level, along with a confidence breakdown and personalized tips.

**Note:** This is an educational project intended to demonstrate machine learning concepts, not a clinical or diagnostic tool.

---

## 🧬 Input Features Explained

| Feature | What It Means |
|---|---|
| **Age** | Age of the person |
| **Gender** | Male / Female |
| **Occupation** | Person's profession (e.g. Doctor, Teacher, Engineer) |
| **Sleep Duration** | Average number of hours slept per night |
| **Quality of Sleep** | Self-rated sleep quality on a scale of 1–10 |
| **Physical Activity Level** | Minutes of physical activity per day |
| **BMI Category** | Body Mass Index category (Normal, Overweight, Obese) |
| **Heart Rate** | Resting heart rate in beats per minute |
| **Daily Steps** | Average number of steps taken per day |

In simple terms: poor sleep, low physical activity, and higher resting heart rate are generally associated with higher stress levels. The model learns these relationships from real lifestyle data to make its prediction.

---

##  Model Details

- **Algorithm:** Random Forest Classifier
- **Problem Type:** Multi-class classification (Low / Medium / High stress)
- **Preprocessing:** One-hot encoding for categorical features (Gender, Occupation, BMI Category)
- **Dataset:** Sleep Health and Lifestyle Dataset (374 records)
- **Output:** Predicted stress category with confidence scores for each class

### Performance
- Achieved ~98.6% accuracy on the test set
- Evaluated using accuracy, precision, recall, F1-score, and confusion matrix

---

##  Tech Stack

- **Python**   data processing and model training
- **Scikit-learn**   Random Forest model, preprocessing, evaluation
- **Pandas**   data handling
- **Streamlit**   interactive web app interface
- **Joblib**   model serialization

---

##  Running Locally

```bash
pip install streamlit pandas scikit-learn joblib
streamlit run app.py
```

Make sure `stress_model.pkl` and `model_columns.pkl` are in the same folder as `app.py`.

---

## ⚠️ Disclaimer

This tool is built for educational purposes as part of a machine learning learning project. It is not a substitute for professional mental health advice. Please consult a qualified professional for any concerns about stress or wellbeing.
