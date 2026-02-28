CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    month INT
);

CREATE TABLE fact_sales (
    sales_id SERIAL PRIMARY KEY,
    customer_key INT,
    date_key INT,
    payment_value NUMERIC
);