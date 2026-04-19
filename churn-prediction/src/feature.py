import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os
path = "data/raw/Telco-Customer-Churn.csv"
os.makedirs("data/processed", exist_ok=True)
os.makedirs("models", exist_ok=True)

def clean_data(df):
    # Drop customerID — not predictive
    df = df.drop(columns=["customerID"])

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"], errors="coerce"
    )
    # Fill nulls in TotalCharges with MonthlyCharges
    # (new customers have 0 tenure so TotalCharges is empty)
    df["TotalCharges"] = df["TotalCharges"].fillna(
        df["MonthlyCharges"]
    )

    # Encode target variable
    df["Churn"] = (df["Churn"] == "Yes").astype(int)

    return df


def engineer_features(df):
    # New feature 1: charges per month of tenure
    # Captures value-for-money perception
    df["charges_per_tenure"] = (
            df["TotalCharges"] / (df["tenure"] + 1)
    )

    # New feature 2: number of services subscribed
    services = [
        "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies"
    ]
    df["num_services"] = df[services].apply(
        lambda row: sum(1 for v in row if v not in
                        ["No", "No internet service", "No phone service"]),
        axis=1
    )

    # New feature 3: is long-term customer?
    df["is_long_tenure"] = (df["tenure"] >= 24).astype(int)

    return df

def encode_features(df):
    # Binary yes/no columns
    binary_cols = [
        "gender", "Partner", "Dependents", "PhoneService",
        "PaperlessBilling"
    ]
    for col in binary_cols:
        df[col] = (df[col] == "Yes").astype(int)

    # Multi-category columns — one-hot encode
    multi_cols = [
        "MultipleLines", "InternetService", "OnlineSecurity",
        "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies", "Contract", "PaymentMethod"
    ]
    df = pd.get_dummies(df, columns=multi_cols, drop_first=True)

    return df


def prepare_data(path, test_size=0.2):
    df = pd.read_csv(path)
    df = clean_data(df)
    df = engineer_features(df)
    df = encode_features(df)

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size,
        random_state=42, stratify=y
    )

    # Scale numeric features
    numeric_cols = [
        "tenure", "MonthlyCharges", "TotalCharges",
        "charges_per_tenure", "num_services"
    ]
    scaler = StandardScaler()
    X_train[numeric_cols] = scaler.fit_transform(
        X_train[numeric_cols]
    )
    X_test[numeric_cols] = scaler.transform(
        X_test[numeric_cols]
    )

    # Save processed data and scaler
    X_train.to_csv("data/processed/X_train.csv", index=False)
    X_test.to_csv("data/processed/X_test.csv", index=False)
    y_train.to_csv("data/processed/y_train.csv", index=False)
    y_test.to_csv("data/processed/y_test.csv", index=False)
    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(list(X_train.columns), "models/feature_names.pkl")

    print(f"Train size: {len(X_train):,} rows")
    print(f"Test size:  {len(X_test):,} rows")
    print(f"Features:   {X_train.shape[1]}")
    print(f"Churn rate in train: {y_train.mean():.1%}")

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    prepare_data()
