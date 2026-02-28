SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS month,
    SUM(payment_value) AS revenue
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY month
ORDER BY month;

SELECT
    month,
    SUM(revenue) OVER (
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS rolling_3_month
FROM (
    SELECT
        DATE_TRUNC('month', order_purchase_timestamp) AS month,
        SUM(payment_value) AS revenue
    FROM orders o
    JOIN order_payments p ON o.order_id = p.order_id
    GROUP BY month
) t;