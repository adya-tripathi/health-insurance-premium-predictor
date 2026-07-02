# 🏥 Health Insurance Premium Predictor 

A Machine Learning web application that predicts medical insurance premiums based on individual health markers and demographic data. This project contains my exploration and understanding of the data then fitting various models to it and then choosing the one with best r2_score an optimized Random Forest Regressor to handle complex non-linear health interactions and is deployed via an interactive Streamlit dashboard.

## 📊 Project Overview
Predicting medical insurance costs accurately is critical for both providers and consumers. Standard linear models often fail to capture the exponential compounding risk of combined habits (like high BMI,age factor,combined with smoking habits and other health risks). 

This project transitions from a baseline **Linear Regression model (~80% R²) withot any feature engineering to a (~88.5% R²) with some engineered features** to an optimized **Random Forest Regressor**, achieving significantly higher accuracy by engineering custom interaction features.

## 🚀 Live Demo
[text](https://health-insurance-premium-predictor-bqububebayhhgmg4rfcfxv.streamlit.app/)


### Key Features
* **Feature Engineering:** Added custom interactions (`bmi_smoker_interaction`) and non-linear terms (`age_squared`) to capture high-risk outlier trends.
* **Smart UI:** A clean, interactive Streamlit interface allowing users to input data via sliders and dropdowns to get instant premium estimates.
* **Robust Serialization:** Model packaged and optimized using `pickle` for rapid inference.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Machine Learning:** Scikit-Learn, NumPy, Pandas
* **Model Tracking/Evaluation:** R² Score, Mean Absolute Error (MAE)
* **Deployment/UI:** Streamlit
* **Model Storage:** Pickle

---

## 📂 Repository Structure
insurance-premium-predictor/
├── data/
│   └── insurance.csv        ← dataset
├── notebooks/
│   └── analysis.ipynb       ← EDA + model work
├── app.py                   ← streamlit app
├── model/
│   └── model.pkl            ← trained model
├── requirements.txt
└── README.md

⚙️ Installation & Local Setup

Follow these steps to run the Streamlit app locally on your machine:

Clone the repository
Create a virtual environment
Install dependencies:
Make sure your requirements.txt includes: streamlit, scikit-learn, pandas, numpy, and pickle.
Launch the Streamlit App
