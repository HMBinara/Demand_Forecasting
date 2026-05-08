Markdown
# 📊 Smart Demand Forecasting System (XGBoost)

A professional AI-driven dashboard designed to forecast product demand based on pricing, promotions, and market trends. This tool helps businesses optimize inventory levels and supply chain management using Machine Learning.

## 🚀 Live Demo
You can access the live application here: 
👉 [Demand Forecasting App](https://demandforecasting-wvqqt9wwuta2b8btrzbbwq.streamlit.app/)

## 🛠️ Tech Stack
- **Language:** Python 3.12
- **Framework:** Streamlit (Custom CSS for professional UI)
- **ML Library:** XGBoost Regression, Scikit-Learn
- **Data Handling:** Pandas, NumPy
- **Deployment:** Streamlit Cloud

## 📁 Project Structure
```text
Demand_Forecasting/
├── models/                  # Trained models & encoders (All Small Letters)
│   ├── xgboost_demand_model.pkl
│   └── label_encoders.pkl
├── notebooks/               # Training scripts & Data analysis
│   └── Demand_Forecasting.ipynb
├── app.py                   # Main Streamlit Application
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
└── .gitignore               # Ignored files (venv, pycache)
⚙️ Installation & Setup
To run this project locally, follow these steps:

Clone the repository:

Bash
git clone [https://github.com/HMBinara/Demand_Forecasting.git](https://github.com/HMBinara/Demand_Forecasting.git)
cd Demand_Forecasting
Create a Virtual Environment:

Bash
python -m venv venv
# Activate on Windows:
.\venv\Scripts\activate
Install Dependencies:

Bash
pip install -r requirements.txt
Run the Application:

Bash
streamlit run app.py
💡 Key Features
Accurate Predictions: Uses the XGBoost algorithm for high-performance regression.

Dynamic Inputs: Users can manually type inventory levels and product prices.

Competitor Analysis: Real-time comparison with competitor pricing to adjust demand.

Categorical Support: Integrated Label Encoders for various product categories like Electronics, Clothing, and Groceries.

Developer: HM Binara
