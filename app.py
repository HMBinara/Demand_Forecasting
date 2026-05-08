import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# Set page configuration
st.set_page_config(page_title="Demand Forecasting", layout="centered")

@st.cache_resource
def load_artifacts():
    """
    Loads the trained model and label encoders from the 'models' folder.
    """
    model_path = "models/xgboost_demand_model.pkl"
    encoder_path = "models/label_encoders.pkl"

    if os.path.exists(model_path) and os.path.exists(encoder_path):
        try:
            with open(model_path, "rb") as f:
                model = pickle.load(f)
            with open(encoder_path, "rb") as f:
                encoders = pickle.load(f)
            return model, encoders
        except Exception as e:
            st.error(f"Error loading artifacts: {e}")
            return None, None
    else:
        return None, None

# Load model and encoders
model, label_encoders = load_artifacts()

# UI Header
st.title("📊 Demand Forecasting App")
st.markdown("Enter product details below to predict the expected demand.")
st.divider()

# Check if model exists before proceeding
if model is None or label_encoders is None:
    st.warning("⚠️ Model files not found in 'models/' folder!")
    st.stop() 

# Input Section
st.header("Input Features")

col1, col2 = st.columns(2)

with col1:
    price = st.number_input("Price", min_value=0.0, value=70.0)
    discount = st.number_input("Discount (%)", min_value=0, max_value=100, value=20)
    inventory_level = st.number_input("Inventory Level", min_value=0, value=80)

with col2:
    promotion = st.selectbox("Promotion", options=[0, 1], format_func=lambda x: "Active" if x == 1 else "Inactive")
    competitor_pricing = st.number_input("Competitor Price", min_value=0.0, value=60.0)
    category = st.selectbox(
        "Category",
        options=label_encoders["Category"].classes_.tolist()
    )

st.divider()

# Prediction Logic
if st.button("Predict Demand", use_container_width=True):
    try:
        # Create DataFrame in the exact order expected by the model
        input_data = pd.DataFrame({
            "Price": [price],
            "Discount": [discount],
            "Inventory Level": [inventory_level],
            "Competitor Pricing": [competitor_pricing],
            "Promotion": [promotion],
            "Category": [category]
        })

        # Categorical data encoding
        for col, encoder in label_encoders.items():
            if col in input_data.columns:
                input_data[col] = encoder.transform(input_data[col])

        # Make prediction
        prediction = model.predict(input_data)[0]
        
        # Display the result clearly
        result = int(max(0, prediction))
        st.success(f"### Predicted Demand: {result}")
        
    except Exception as e:
        st.error(f"Prediction Error: {e}")