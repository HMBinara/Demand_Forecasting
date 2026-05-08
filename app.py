import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# Page Config
st.set_page_config(
    page_title="DemandForecaster AI",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border: none;
    }
    .prediction-card {
        padding: 25px;
        border-radius: 15px;
        background-color: #1e2130;
        border-left: 5px solid #00ffcc;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_artifacts():
    model_path = "Models/xgboost_demand_model.pkl"
    encoder_path = "Models/label_encoders.pkl"
    if os.path.exists(model_path) and os.path.exists(encoder_path):
        try:
            with open(model_path, "rb") as f:
                model = pickle.load(f)
            with open(encoder_path, "rb") as f:
                encoders = pickle.load(f)
            return model, encoders
        except Exception as e:
            st.error(f"Error loading files: {e}")
            return None, None
    return None, None

model, label_encoders = load_artifacts()

# Sidebar Info
with st.sidebar:
    st.title("🚀 Navigation")
    st.info("This AI system predicts product demand using market variables.")
    st.divider()
    st.write("**Developer:** HM Binara")
    st.write("**Method:** XGBoost Regression")

# Main Header
st.title("📊 Smart Demand Forecasting Dashboard")
st.markdown("Optimize your inventory and supply chain with high-accuracy ML predictions.")
st.divider()

if model is None:
    st.error("Model artifacts not found in 'models/' folder. Please check your file paths.")
    st.stop()

# Layout: 2 Columns for inputs
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📦 Product Context")
    category = st.selectbox("Product Category", label_encoders["Category"].classes_.tolist())
    
    # Inventory Level as a Number Input (User can type any value)
    inventory_level = st.number_input("Current Inventory Level", min_value=0, value=158, step=1)
    
    promotion = st.radio("Active Promotion?", [0, 1], 
                         format_func=lambda x: "Active" if x == 1 else "Inactive", 
                         horizontal=True)

with col2:
    st.subheader("💰 Pricing & Market")
    price = st.number_input("Our Unit Price ($)", min_value=0.0, value=1000.0)
    competitor_pricing = st.number_input("Competitor Price ($)", min_value=0.0, value=500.0)
    discount = st.slider("Discount Applied (%)", 0, 100, 5)

st.divider()

# Prediction Button
if st.button("Generate Forecast"):
    try:
        # Match the EXACT feature order of your model
        input_data = pd.DataFrame({
            "Price": [price],
            "Discount": [discount],
            "Inventory Level": [inventory_level],
            "Competitor Pricing": [competitor_pricing],
            "Promotion": [promotion],
            "Category": [category]
        })

        # Encoding
        for col, encoder in label_encoders.items():
            if col in input_data.columns:
                input_data[col] = encoder.transform(input_data[col])

        # Prediction
        prediction = model.predict(input_data)[0]
        result = int(max(0, prediction))

        # Modern Output Card
        st.markdown(f"""
            <div class="prediction-card">
                <h3 style='color: #00ffcc; margin-bottom: 5px;'>Forecast Result</h3>
                <h1 style='color: white; margin-top: 0px;'>{result} Units</h1>
                <p style='color: #808495;'>Based on current market pricing, promotions, and inventory levels.</p>
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Prediction Error: {e}")