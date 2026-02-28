from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, sum, to_timestamp, date_trunc

def create_spark_session():
    spark = SparkSession.builder \
        .appName("Ecommerce ETL Pipeline") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def load_csv(spark, file_path: str) -> DataFrame:
    return spark.read.csv(
        file_path,
        header=True,
        inferSchema=True
    )
def clean_orders(df):
    df = df.dropna(subset=["order_id", "customer_id"])
    df = df.withColumn(
        "order_purchase_timestamp",
        to_timestamp(col("order_purchase_timestamp"))
    )
    return df.dropDuplicates(["order_id"])

def clean_payments(df):
    return df.dropna(subset=["order_id", "payment_value"])

def create_sales_df(orders, payments):
    return orders.join(payments, "order_id", "inner")

def monthly_revenue(df):
    return df.withColumn(
        "month",
        date_trunc("month", col("order_purchase_timestamp"))
    ).groupBy("month") \
     .agg(sum("payment_value").alias("revenue")) \
     .orderBy("month")


def write_parquet(df, path):
    df.write.mode("overwrite").csv(path)

def write_to_postgres(df, url, table, properties):
    df.write.jdbc(
        url=url,
        table=table,
        mode="overwrite",
        properties=properties
    )