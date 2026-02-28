CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_purchase_timestamp TIMESTAMP
);

CREATE TABLE order_payments (
    order_id VARCHAR(50),
    payment_value NUMERIC
);