import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    cross_val_score, GridSearchCV, StratifiedKFold
)
import joblib


def load_processed_data():
    X_train = pd.read_csv("data/processed/X_train.csv")
    X_test = pd.read_csv("data/processed/X_test.csv")
    y_train = pd.read_csv("data/processed/y_train.csv").squeeze()
    y_test = pd.read_csv("data/processed/y_test.csv").squeeze()
    return X_train, X_test, y_train, y_test


def train_baseline(X_train, y_train):
    print("[TRAIN] Training baseline Random Forest...")
    rf = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1  # use all CPU cores
    )
    # 5-fold cross-validation — more reliable than single split
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(
        rf, X_train, y_train,
        cv=cv, scoring="roc_auc"
    )
    print(f"  CV ROC-AUC: {cv_scores.mean():.4f} ")
    print(f"  Std Dev:    {cv_scores.std():.4f}")
    rf.fit(X_train, y_train)
    return rf


def tune_hyperparameters(X_train, y_train):
    print("[TRAIN] Tuning hyperparameters...")
    param_grid = {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5, 10],
        "max_features": ["sqrt", "log2"],
        "class_weight": [None, "balanced"]
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    grid_search = GridSearchCV(
        RandomForestClassifier(random_state=42, n_jobs=-1),
        param_grid,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1,
        verbose=1
    )
    grid_search.fit(X_train, y_train)
    print(f"  Best params:   {grid_search.best_params_}")
    print(f"  Best ROC-AUC:  {grid_search.best_score_:.4f}")
    return grid_search.best_estimator_


def save_model(model, path="models/random_forest_model.pkl"):
    joblib.dump(model, path)
    print(f"[TRAIN] Model saved to {path}")


def run_training(tune=False):
    X_train, X_test, y_train, y_test = load_processed_data()
    if tune:
        model = tune_hyperparameters(X_train, y_train)
    else:
        model = train_baseline(X_train, y_train)
    save_model(model)
    return model, X_test, y_test


if __name__ == "__main__":
    # Run baseline first, then tune if needed
    run_training(tune=False)

