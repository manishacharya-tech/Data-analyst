import logging
from config.config import DATA_PATH, OUTPUT_PATH, DB_URL, DB_PROPERTIES
from src.ETL import create_spark_session,load_csv,clean_orders,clean_payments,create_sales_df,monthly_revenue,write_parquet,write_to_postgres
logging.basicConfig(level=logging.INFO)
def main():
    spark = create_spark_session()

    try:
        logging.info("Loading data...")

        orders = load_csv(spark, DATA_PATH + "olist_orders_dataset.csv")
        payments = load_csv(spark, DATA_PATH + "olist_order_payments_dataset.csv")

        logging.info("Cleaning data...")

        orders_clean = clean_orders(orders)
        payments_clean = clean_payments(payments)

        sales_df = create_sales_df(orders_clean, payments_clean)

        logging.info("Calculating KPIs...")

        monthly_df = monthly_revenue(sales_df)

        logging.info("Writing to Parquet...")

        write_parquet(monthly_df, OUTPUT_PATH + "monthly_revenue")

        logging.info("Writing to PostgreSQL...")

        write_to_postgres(
            monthly_df,
            DB_URL,
            "monthly_revenue_summary",
            DB_PROPERTIES
        )

        logging.info("Pipeline Completed Successfully")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")

    spark.stop()

if __name__ == "__main__":
    main()