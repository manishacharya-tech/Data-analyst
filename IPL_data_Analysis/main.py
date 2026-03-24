import time
from pipeline.clean import clean_all
from pipeline.load import load_data
from pipeline.validate import validate

def run_pipeline():
    start = time.time()
    print("\n" + "=" * 55)
    print("  IPL Analytics Pipeline")
    print("  Run once — everything automated")
    print("=" * 55)
    print("\n[STEP 1/3] Cleaning and enriching data...")
    matches, deliveries = clean_all()

    print("\n[STEP 2/3] Loading to PostgreSQL...")
    load_data(matches, deliveries)

    print("\n[STEP 3/3] Running validation checks...")
    validate()

    elapsed = round(time.time() - start, 1)
    print(f"\n  Pipeline complete in {elapsed}s")
    print("  Open Power BI and connect to PostgreSQL ipl_db")
    print("=" * 55)


if __name__ == "__main__":
    run_pipeline()
