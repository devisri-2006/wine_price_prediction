import streamlit as st
import pandas as pd
import numpy as np
import pickle

# --- PAGE CONFIG ---
st.set_page_config(page_title="🍷 Wine Quality Classification", page_icon="🍷", layout="centered")

# --- GOLD + CENTER BURST ANIMATION CSS ---
def set_gold_classification_style():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), 
                    url("https://thumbs.dreamstime.com/b/winter-wine-bottle-nad-glass-wallpaper-background-picture-346941239.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }

    .stNumberInput label {
        color: white !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        text-shadow: 2px 2px 4px #000;
    }
    
    .success-label {
        font-size: 32px !important;
        color: #00FFCC !important;
        text-align: center;
        font-weight: bold;
        text-transform: uppercase;
        animation: bounce 1.2s infinite;
    }

    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-12px); }
        60% { transform: translateY(-6px); }
    }

    /* FALLING GOLD SPARKLES (15 particles) */
    .gold-sparkles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.6s ease-in-out;
    }

    .gold-particle {
        position: absolute;
        width: 12px;
        height: 12px;
        background: radial-gradient(circle, #FFD700 0%, #FFA500 50%, #FF8C00 100%);
        border-radius: 50%;
        animation: gold-fall 4s linear infinite;
        box-shadow: 0 0 25px #FFD700, 0 0 35px #FFA500;
    }

    .gold-particle:nth-child(1) { left: 8%; animation-delay: 0s; animation-duration: 3.8s; }
    .gold-particle:nth-child(2) { left: 18%; animation-delay: 0.2s; animation-duration: 4.2s; }
    .gold-particle:nth-child(3) { left: 28%; animation-delay: 0.4s; animation-duration: 3.9s; }
    .gold-particle:nth-child(4) { left: 38%; animation-delay: 0.6s; animation-duration: 4.1s; }
    .gold-particle:nth-child(5) { left: 48%; animation-delay: 0.8s; animation-duration: 3.7s; }
    .gold-particle:nth-child(6) { left: 58%; animation-delay: 1.0s; animation-duration: 4.3s; }
    .gold-particle:nth-child(7) { left: 68%; animation-delay: 1.2s; animation-duration: 3.6s; }
    .gold-particle:nth-child(8) { left: 78%; animation-delay: 1.4s; animation-duration: 4.0s; }
    .gold-particle:nth-child(9) { left: 88%; animation-delay: 1.6s; animation-duration: 3.5s; }
    .gold-particle:nth-child(10) { left: 12%; animation-delay: 1.8s; animation-duration: 4.4s; }
    .gold-particle:nth-child(11) { left: 32%; animation-delay: 2.0s; animation-duration: 3.9s; }
    .gold-particle:nth-child(12) { left: 52%; animation-delay: 2.2s; animation-duration: 4.1s; }
    .gold-particle:nth-child(13) { left: 72%; animation-delay: 2.4s; animation-duration: 3.8s; }
    .gold-particle:nth-child(14) { left: 22%; animation-delay: 2.6s; animation-duration: 4.2s; }
    .gold-particle:nth-child(15) { left: 62%; animation-delay: 2.8s; animation-duration: 3.7s; }

    @keyframes gold-fall {
        0% { transform: translateY(-150vh) rotate(0deg) scale(0); opacity: 0; }
        8% { opacity: 1; transform: scale(1.2); }
        25%, 75% { opacity: 1; }
        100% { transform: translateY(150vh) rotate(1080deg) scale(0); opacity: 0; }
    }

    /* CENTER BURST ANIMATION - PURPLE/PINK */
    .center-burst {
        position: fixed;
        top: 50%;
        left: 50%;
        width: 100px;
        height: 100px;
        margin-left: -50px;
        margin-top: -50px;
        pointer-events: none;
        z-index: 10000;
        opacity: 0;
        animation: centerExplode 2s ease-out forwards;
    }

    .center-star {
        position: absolute;
        width: 20px;
        height: 20px;
        background: radial-gradient(circle, #FF00FF 0%, #8A2BE2 70%, #4B0082 100%);
        border-radius: 50%;
        top: 50%;
        left: 50%;
        margin: -10px 0 0 -10px;
        animation: starBurst 2s ease-out forwards;
        box-shadow: 0 0 30px #FF00FF;
    }

    .center-star:nth-child(1) { transform: rotate(0deg) translateX(40px) rotate(0deg); animation-delay: 0.1s; }
    .center-star:nth-child(2) { transform: rotate(36deg) translateX(40px) rotate(-36deg); animation-delay: 0.15s; }
    .center-star:nth-child(3) { transform: rotate(72deg) translateX(40px) rotate(-72deg); animation-delay: 0.2s; }
    .center-star:nth-child(4) { transform: rotate(108deg) translateX(40px) rotate(-108deg); animation-delay: 0.25s; }
    .center-star:nth-child(5) { transform: rotate(144deg) translateX(40px) rotate(-144deg); animation-delay: 0.3s; }
    .center-star:nth-child(6) { transform: rotate(180deg) translateX(40px) rotate(-180deg); animation-delay: 0.35s; }
    .center-star:nth-child(7) { transform: rotate(216deg) translateX(40px) rotate(-216deg); animation-delay: 0.4s; }
    .center-star:nth-child(8) { transform: rotate(252deg) translateX(40px) rotate(-252deg); animation-delay: 0.45s; }

    @keyframes centerExplode {
        0% { opacity: 1; transform: scale(0); }
        50% { opacity: 1; transform: scale(1.5); }
        100% { opacity: 0; transform: scale(2); }
    }

    @keyframes starBurst {
        0% { opacity: 1; transform: scale(1); }
        100% { opacity: 0; transform: scale(0) translateX(100px); }
    }

    .gold-sparkles.active, .center-burst.active { opacity: 1 !important; }

    .stButton > button {
        background: linear-gradient(145deg, #722f37, #8B4513);
        color: white;
        border-radius: 15px;
        width: 100%;
        height: 3.8em;
        font-size: 22px;
        font-weight: bold;
        border: 3px solid #FFD700;
        transition: all 0.4s;
        box-shadow: 0 6px 20px rgba(255,215,0,0.4);
    }
    .stButton > button:hover {
        background: linear-gradient(145deg, #FFD700, #FFA500);
        color: #722f37;
        transform: scale(1.08);
        box-shadow: 0 10px 30px rgba(255,215,0,0.7), 0 0 30px #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

set_gold_classification_style()

# --- GOLD SPARKLES + CENTER BURST TRIGGER ---
def trigger_gold_center_burst():
    st.markdown("""
    <div class="gold-sparkles active">
        <div class="gold-particle"></div><div class="gold-particle"></div><div class="gold-particle"></div>
        <div class="gold-particle"></div><div class="gold-particle"></div><div class="gold-particle"></div>
        <div class="gold-particle"></div><div class="gold-particle"></div><div class="gold-particle"></div>
        <div class="gold-particle"></div><div class="gold-particle"></div><div class="gold-particle"></div>
        <div class="gold-particle"></div><div class="gold-particle"></div><div class="gold-particle"></div>
        <div class="gold-particle"></div><div class="gold-particle"></div>
    </div>
    <!-- CENTER PURPLE/PINK BURST -->
    <div class="center-burst active">
        <div class="center-star"></div><div class="center-star"></div><div class="center-star"></div>
        <div class="center-star"></div><div class="center-star"></div><div class="center-star"></div>
        <div class="center-star"></div><div class="center-star"></div>
    </div>
    """, unsafe_allow_html=True)

# --- LOAD MODELS ---
@st.cache_resource
def load_models():
    rf_model = pickle.load(open('finalized_RFmodel.sav', 'rb'))
    scaler = pickle.load(open('scaler_model.sav', 'rb'))
    return rf_model, scaler

try:
    rf_model, scaler = load_models()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# --- HEADER ---
st.title("🍷 Premium Wine Quality Predictor")
st.write("Enter the wine chemical properties below to get a quality rating.")

# --- INPUT FORM ---
col1, col2 = st.columns(2)

with col1:
    fixed_acidity = st.number_input("Fixed Acidity", value=8.3)
    volatile_acidity = st.number_input("Volatile Acidity", value=0.5)
    citric_acid = st.number_input("Citric Acid", value=0.3)
    residual_sugar = st.number_input("Residual Sugar", value=2.5)
    chlorides = st.number_input("Chlorides", value=0.08)
    free_sulfur_dioxide = st.number_input("Free Sulfur Dioxide", value=15.0)

with col2:
    total_sulfur_dioxide = st.number_input("Total Sulfur Dioxide", value=45.0)
    density = st.number_input("Density", value=0.99)
    pH_val = st.number_input("pH", value=3.3)
    sulphates = st.number_input("Sulphates", value=0.6)
    alcohol = st.number_input("Alcohol %", value=10.5)

# --- PREDICTION ---
if st.button("🚀 PREDICT QUALITY"):
    data = {
        'fixed acidity': fixed_acidity,
        'volatile acidity': volatile_acidity,
        'citric acid': citric_acid,
        'residual sugar': np.log(residual_sugar) if residual_sugar > 0 else 0,
        'chlorides': np.log(chlorides) if chlorides > 0 else 0,
        'free sulfur dioxide': np.log(free_sulfur_dioxide) if free_sulfur_dioxide > 0 else 0,
        'total sulfur dioxide': np.log(total_sulfur_dioxide) if total_sulfur_dioxide > 0 else 0,
        'density': density,
        'pH': pH_val,
        'sulphates': np.log(sulphates) if sulphates > 0 else 0,
        'alcohol': alcohol
    }
    
    input_df = pd.DataFrame([data])
    input_scaled = scaler.transform(input_df)
    prediction = rf_model.predict(input_scaled)[0]
    
    # 🎉 GOLD SPARKLES + CENTER BURST ANIMATION
    trigger_gold_center_burst()
    
    # SUCCESS MESSAGE
    st.markdown('<p class="success-label">✅ PREDICTION COMPLETE!</p>', unsafe_allow_html=True)
    
    # 3-TIER CLASSIFICATION
    if prediction >= 7:
        st.markdown("<h1 style='text-align: center; color: #FFD700; text-shadow: 0 0 25px #FFD700;'>🌟 EXCELLENT QUALITY 🍷</h1>", unsafe_allow_html=True)
    elif prediction >= 6:
        st.markdown("<h1 style='text-align: center; color: #FFFFFF; text-shadow: 0 0 15px #FFFFFF;'>👍 GOOD QUALITY 🍷</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #FFA500; text-shadow: 0 0 15px #FFA500;'>⚠️ POOR QUALITY 🍷</h1>", unsafe_allow_html=True)

st.markdown("---")