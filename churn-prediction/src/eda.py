import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
cwd = os.getcwd()


os.makedirs("output/eda", exist_ok=True)


def load_and_inspect(path="../data/raw/Telco-Customer-Churn.csv"):
    df = pd.read_csv(path)
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nNull values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    print(f"\nTarget distribution:")
    print(df["Churn"].value_counts())
    print(f"\nChurn rate: {df["Churn"].value_counts(normalize=True)["Yes"]:.1%}")
    return df

def plot_churn_distribution(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    # Churn count
    churn_counts = df["Churn"].value_counts()
    axes[0].bar(churn_counts.index, churn_counts.values,
                color=["#2E74B5", "#C0392B"])
    axes[0].set_title("Churn Distribution", fontweight="bold")
    axes[0].set_ylabel("Count")
    for i, v in enumerate(churn_counts.values):
        axes[0].text(i, v + 20, str(v), ha="center", fontweight="bold")
    # Churn by contract type
    contract_churn = df.groupby("Contract")["Churn"].apply(
        lambda x: (x == "Yes").mean() * 100
    ).sort_values(ascending=False)
    axes[1].bar(contract_churn.index, contract_churn.values,
                color=["#C0392B", "#E67E22", "#2E74B5"])
    axes[1].set_title("Churn Rate by Contract Type", fontweight="bold")
    axes[1].set_ylabel("Churn Rate (%)")
    for i, v in enumerate(contract_churn.values):
        axes[1].text(i, v + 0.5, f"{v:.1f}%", ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig("output/eda/churn_distribution.png", dpi=150)
    plt.close()
    print("Saved: churn_distribution.png")


def plot_numeric_features(df):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]

    for ax, col in zip(axes, numeric_cols):
        churned = df[df["Churn"] == "Yes"][col].dropna()
        not_churned = df[df["Churn"] == "No"][col].dropna()
        ax.hist(not_churned, bins=30, alpha=0.6,
                color="#2E74B5", label="No Churn")
        ax.hist(churned, bins=30, alpha=0.6,
                color="#C0392B", label="Churned")
        ax.set_title(f"{col} by Churn", fontweight="bold")
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig("output/eda/numeric_distributions.png", dpi=150)
    plt.close()
    print("Saved: numeric_distributions.png")


def plot_categorical_churn(df):
    cat_cols = ["InternetService", "PaymentMethod",
                "PaperlessBilling", "SeniorCitizen"]
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    axes = axes.flatten()

    for ax, col in zip(axes, cat_cols):
        churn_rate = df.groupby(col)["Churn"].apply(
            lambda x: (x == "Yes").mean() * 100
        ).sort_values(ascending=False)
        bars = ax.bar(range(len(churn_rate)),
                      churn_rate.values, color="#2E74B5")
        ax.set_xticks(range(len(churn_rate)))
        ax.set_xticklabels(churn_rate.index,
                           rotation=20, ha="right", fontsize=8)
        ax.set_title(f"Churn Rate by {col}", fontweight="bold")
        ax.set_ylabel("Churn Rate (%)")
        for bar, val in zip(bars, churn_rate.values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    val + 0.3, f"{val:.1f}%",
                    ha="center", fontsize=8, fontweight="bold")

    plt.tight_layout()
    plt.savefig("output/eda/categorical_churn.png", dpi=150)
    plt.close()
    print("Saved: categorical_churn.png")


def run_eda():
    df = load_and_inspect()
    plot_churn_distribution(df)
    plot_numeric_features(df)
    plot_categorical_churn(df)
    print("\nEDA complete. 3 charts saved to output/eda/")
    return df


if __name__ == "__main__":
    run_eda()



