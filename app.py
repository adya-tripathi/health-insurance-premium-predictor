import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global : ye pure mein hi apply hoga kyunki html aur body par lgaya hai */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background */
    .stApp {
        background-color: #0E1117;
    }

    /* Main card with the main heading*/
    .main-card {
        background: #1A1F2C;
        border-radius: 16px;
        padding: 2rem 2.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
    }

    /* main card's heading*/
    .header-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00F0FF
        margin-bottom: 0.2rem;
    }
    /*main card's sub heading*/
    .header-sub {
        font-size: 0.95rem;
        color: #94A3B8
        margin-bottom: 0rem;
    }

    /* Section label */
    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #bfdbfe;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.8rem;
        margin-top: 1.4rem;
    }

    /* Result box */
    .result-box {
        background: linear-gradient(135deg, #1a56db 0%, #1e40af 100%);
        border-radius: 14px;
        padding: 1.8rem 2rem;
        text-align: center;
        margin-top: 1rem;
    }
    .result-label {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .result-amount {
        color: white;
        font-size: 2.6rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .result-note {
        color: #bfdbfe;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }

    /* Warning box */
    .warning-box {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        font-size: 0.85rem;
        color: #92400e;
        margin-top: 1rem;
    }

    /* Divider */
    .divider {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 1.2rem 0;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("model/model1.pkl", "rb") as f:
        return pickle.load(f)

try:
    model = load_model()
    model_loaded = True
except FileNotFoundError:
    model_loaded = False


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-card">
    <div class="header-title">🏥 Insurance Premium Predictor</div>
    <div class="header-sub">Enter the required fields below to estimate your annual health insurance cost.</div>
    <hr class="divider">
""", unsafe_allow_html=True)

if not model_loaded:
    st.error("⚠️ Model file not found. Make sure `model/model.pkl` exists.")
    st.stop()


# ── Input form ────────────────────────────────────────────────────────────────

st.markdown('<div class="section-label">Personal Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age (years)",
        min_value=18, max_value=100, value=30, step=1,
        help="Your current age"
    )

with col2:
    sex = st.selectbox(
        "Sex",
        options=["Male", "Female"]
    )

st.markdown('<div class="section-label">Health Information</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    bmi = st.number_input(
        "BMI (Body Mass Index)",
        min_value=10.0, max_value=60.0, value=25.0, step=0.1,
        help="BMI = weight(kg) / height(m)²"
    )

with col4:
    smoker = st.selectbox(
        "Do you smoke?",
        options=["No", "Yes"]
    )

st.markdown('<div class="section-label">Family & Location</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    children = st.number_input(
        "Number of Children",
        min_value=0, max_value=10, value=0, step=1,
        help="Children or dependents covered under the plan"
    )

with col6:
    region = st.selectbox(
        "Region",
        options=["Northeast", "Northwest", "Southeast", "Southwest"]
    )


# ── Predict button ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("Calculate My Premium", use_container_width=True, type="primary")

st.markdown("</div>", unsafe_allow_html=True)  # close main-card


# ── Prediction logic ──────────────────────────────────────────────────────────
if predict_btn:

    sex_encoded    = 1 if sex == "Female" else 0
    smoker_encoded = 1 if smoker == "Yes" else 0

    region_nw = 1 if region == "Northwest"  else 0
    region_se = 1 if region == "Southeast"  else 0
    region_sw = 1 if region == "Southwest"  else 0

    bmi_smoker_interaction = bmi * smoker_encoded   
    age_squared = age ** 2               
    
    input_data = np.array([[
        age,
        sex_encoded,
        bmi,
        children,
        smoker_encoded,
        region_nw,
        region_se,
        region_sw,
        bmi_smoker_interaction,
        age_squared
    ]])

    prediction = model.predict(input_data)[0]
    #to avoid negative predictions
    prediction = max(0, prediction) 

    # ── Result display ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Estimated Annual Premium</div>
        <div class="result-amount">${prediction:,.0f}</div>
        <div class="result-note">This is a model estimate — actual premiums vary by provider.</div>
    </div>
    """, unsafe_allow_html=True)

    # Smoker warning
    if smoker == "Yes":
        st.markdown("""
        <div class="warning-box">
            🚬 <strong>Smoking significantly increases your premium.</strong>
            Quitting could reduce your annual cost by up to 3×.
        </div>
        """, unsafe_allow_html=True)

    # BMI note
    if bmi >= 30:
        st.markdown("""
        <div class="warning-box">
            ⚖️ <strong>Your BMI is above 30 (obese range).</strong>
            This is factored into a higher premium estimate.
        </div>
        """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<br>
<div style="text-align:center; color:#a0aec0; font-size:0.78rem;">
    Built with Streamlit &nbsp;|&nbsp; Dataset Source: Kaggle(Medical Cost Dataset)
</div>
""", unsafe_allow_html=True)
