import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="Churn Predictor",
    page_icon="",
    layout="wide"
)


# ── Load model and assets ─────────────────────────────────
@st.cache_resource
def load_model():
    model = joblib.load("D:\churn-prediction/models/random_forest_model.pkl")
    scaler = joblib.load("D:\churn-prediction/models/scaler.pkl")
    features = joblib.load("D:\churn-prediction/models/feature_names.pkl")
    return model, scaler, features


model, scaler, feature_names = load_model()

# ── Header ────────────────────────────────────────────────
st.title("Customer Churn Predictor")
st.markdown(
    "Enter customer details below to predict churn probability."
    " Built with Random Forest — **ROC-AUC: 0.86**"
)
st.divider()

# ── Sidebar inputs ────────────────────────────────────────
st.sidebar.header("Customer Details")

tenure = st.sidebar.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.sidebar.slider("Monthly Charges ($)", 18.0, 120.0, 65.0)
total_charges = st.sidebar.slider("Total Charges ($)", 0.0, 8700.0,
                                  float(tenure * monthly_charges))
senior_citizen = st.sidebar.selectbox("Senior Citizen", [0, 1])
partner = st.sidebar.selectbox("Has Partner", ["Yes", "No"])
dependents = st.sidebar.selectbox("Has Dependents", ["Yes", "No"])
contract = st.sidebar.selectbox(
    "Contract Type",
    ["Month-to-month", "One year", "Two year"]
)
internet = st.sidebar.selectbox(
    "Internet Service",
    ["Fiber optic", "DSL", "No"]
)
payment = st.sidebar.selectbox(
    "Payment Method",
    ["Electronic check", "Mailed check",
     "Bank transfer (automatic)", "Credit card (automatic)"]
)
paperless = st.sidebar.selectbox("Paperless Billing", ["Yes", "No"])
num_services = st.sidebar.slider("Number of Services", 0, 9, 3)


# ── Build input DataFrame ─────────────────────────────────
def build_input():
    charges_per_tenure = total_charges / (tenure + 1)
    is_long_tenure = 1 if tenure >= 24 else 0

    # Build a dict matching training features
    row = {
        "SeniorCitizen": senior_citizen,
        "Partner": 1 if partner == "Yes" else 0,
        "Dependents": 1 if dependents == "Yes" else 0,
        "tenure": tenure,
        "PhoneService": 1,
        "PaperlessBilling": 1 if paperless == "Yes" else 0,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "charges_per_tenure": charges_per_tenure,
        "num_services": num_services,
        "is_long_tenure": is_long_tenure,
    }

    # One-hot encode contract type
    row["Contract_One year"] = 1 if contract == "One year" else 0
    row["Contract_Two year"] = 1 if contract == "Two year" else 0

    # One-hot encode internet service
    row["InternetService_Fiber optic"] = 1 if internet == "Fiber optic" else 0
    row["InternetService_No"] = 1 if internet == "No" else 0

    # One-hot encode payment method
    row["PaymentMethod_Credit card (automatic)"] = (
        1 if payment == "Credit card (automatic)" else 0
    )
    row["PaymentMethod_Electronic check"] = (
        1 if payment == "Electronic check" else 0
    )
    row["PaymentMethod_Mailed check"] = (
        1 if payment == "Mailed check" else 0
    )

    # Fill any missing features with 0
    df = pd.DataFrame([row])
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0
    df = df[feature_names]  # ensure correct column order

    # Scale numeric features
    numeric_cols = [
        "tenure", "MonthlyCharges", "TotalCharges",
        "charges_per_tenure", "num_services"
    ]
    df[numeric_cols] = scaler.transform(df[numeric_cols])
    return df


# ── Prediction ────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

input_df = build_input()
prob = model.predict_proba(input_df)[0][1]
pred = "Will Churn" if prob >= 0.5 else "Will Not Churn"
colour = "red" if prob >= 0.5 else "green"

with col1:
    st.metric("Churn Probability", f"{prob:.1%}")

with col2:
    st.metric("Prediction", pred)

with col3:
    risk = "HIGH" if prob >= 0.7 else "MEDIUM" if prob >= 0.4 else "LOW"
    st.metric("Risk Level", risk)

# ── Probability gauge ─────────────────────────────────────
st.divider()
st.subheader("Churn Probability")
st.progress(prob)
st.caption(
    f"This customer has a **{prob:.1%}** probability of churning. "
    f"Prediction: **{pred}**"
)

# ── Feature importance chart ──────────────────────────────
st.divider()
st.subheader("Top Churn Drivers (Model Insights)")
importances = pd.Series(
    model.feature_importances_, index=feature_names
).sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 4))
colors = ["#C0392B" if i < 3 else "#2E74B5" for i in range(10)]
ax.barh(importances.index[::-1],
        importances.values[::-1], color=colors[::-1])
ax.set_title("Feature Importance — What Drives Churn",
             fontweight="bold")
ax.set_xlabel("Importance Score")
plt.tight_layout()
st.pyplot(fig)

# ── Business recommendation ───────────────────────────────
st.divider()
st.subheader("Business Recommendation")
if prob >= 0.7:
    st.error(
        "HIGH RISK: Immediate retention action recommended. "
        "Offer contract upgrade discount or loyalty reward."
    )
elif prob >= 0.4:
    st.warning(
        "MEDIUM RISK: Monitor this customer. "
        "Consider a proactive check-in or service upgrade offer."
    )
else:
    st.success(
        "LOW RISK: Customer is likely to stay. "
        "No immediate intervention needed."
    )
