from src.eda import run_eda
from src.feature import prepare_data
from src.train import run_training
from src.evaluate import run_evaluation
import time


def main():
    start = time.time()
    print("=" * 50)
    print("  Customer Churn Prediction Pipeline")
    print("=" * 50)

    print("\n[1/4] Running EDA...")
    run_eda()

    print("\n[2/4] Feature engineering...")
    prepare_data()

    print("\n[3/4] Training model...")
    model, X_test, y_test = run_training(tune=False)

    print("\n[4/4] Evaluating model...")
    run_evaluation()

    elapsed = round(time.time() - start, 1)
    print(f"\nPipeline complete in {elapsed}s")
    print("Run the app: streamlit run app.py")
    print("=" * 50)


if __name__ == "__main__":
    main()
