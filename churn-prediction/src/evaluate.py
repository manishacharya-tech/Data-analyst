import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, roc_curve,
    precision_recall_curve, average_precision_score
)
import joblib
import os

os.makedirs("output/evaluation", exist_ok=True)


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_pred_prob = model.predict_proba(X_test)[:, 1]

    print("=" * 50)
    print("  MODEL EVALUATION REPORT")
    print("=" * 50)
    print(f"  Accuracy  : {(y_pred == y_test).mean():.4f}")
    print(f"  ROC-AUC   : {roc_auc_score(y_test, y_pred_prob):.4f}")
    print(f"  Avg Prec  : {average_precision_score(y_test, y_pred_prob):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred,
                                target_names=["No Churn", "Churned"]))
    return y_pred, y_pred_prob


def plot_confusion_matrix(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(7, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["No Churn", "Churned"],
                yticklabels=["No Churn", "Churned"])
    plt.title("Confusion Matrix", fontsize=14, fontweight="bold")
    plt.ylabel("Actual");
    plt.xlabel("Predicted")
    plt.tight_layout()
    plt.savefig("output/evaluation/confusion_matrix.png", dpi=150)
    plt.close()
    print("Saved: confusion_matrix.png")


def plot_roc_curve(y_test, y_pred_prob):
    fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
    auc = roc_auc_score(y_test, y_pred_prob)
    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, color="#2E74B5", lw=2,
             label=f"ROC Curve (AUC = {auc:.3f})")
    plt.plot([0, 1], [0, 1], "k--", lw=1, label="Random classifier")
    plt.fill_between(fpr, tpr, alpha=0.1, color="#2E74B5")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve", fontsize=14, fontweight="bold")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("output/evaluation/roc_curve.png", dpi=150)
    plt.close()
    print("Saved: roc_curve.png")


def plot_feature_importance(model, feature_names, top_n=15):
    importances = pd.Series(
        model.feature_importances_, index=feature_names
    ).sort_values(ascending=False).head(top_n)

    plt.figure(figsize=(10, 6))
    colors = ["#C0392B" if i < 3 else "#2E74B5"
              for i in range(len(importances))]
    plt.barh(importances.index[::-1],
             importances.values[::-1], color=colors[::-1])
    plt.title("Top 15 Feature Importances",
              fontsize=14, fontweight="bold")
    plt.xlabel("Importance Score")
    plt.tight_layout()
    plt.savefig("output/evaluation/feature_importance.png", dpi=150)
    plt.close()
    print("Saved: feature_importance.png")
    print("\nTop 5 Churn Drivers:")
    for name, score in importances.head(5).items():
        print(f"  {name}: {score:.4f}")


def run_evaluation():
    model = joblib.load("models/random_forest_model.pkl")
    features = joblib.load("models/feature_names.pkl")
    X_test = pd.read_csv("data/processed/X_test.csv")
    y_test = pd.read_csv("data/processed/y_test.csv").squeeze()

    y_pred, y_pred_prob = evaluate_model(model, X_test, y_test)
    plot_confusion_matrix(y_test, y_pred)
    plot_roc_curve(y_test, y_pred_prob)
    plot_feature_importance(model, features)
    print("\nEvaluation complete. 3 charts saved.")

if __name__ == "__main__":
    run_evaluation()
