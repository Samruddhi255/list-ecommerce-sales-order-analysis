-- Example queries for the Olist consolidated dataset.
-- Table name used below: olist_combined_dataset
-- Adapt date functions and table-loading syntax to your SQL engine.

-- 1. Basic dataset size and unique order count
SELECT
    COUNT(*) AS joined_rows,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM olist_combined_dataset;

-- 2. Sum of item prices and freight (not automatically net revenue)
SELECT
    SUM(price) AS total_item_price,
    SUM(freight_value) AS total_freight_value
FROM olist_combined_dataset;

-- 3. Unique order count and sum of item prices by status
SELECT
    order_status,
    COUNT(DISTINCT order_id) AS unique_orders,
    SUM(price) AS sum_item_price
FROM olist_combined_dataset
GROUP BY order_status
ORDER BY sum_item_price DESC;

-- 4. Top product categories by summed item price
SELECT
    COALESCE(product_category_name, 'Unknown') AS product_category,
    SUM(price) AS sum_item_price,
    COUNT(DISTINCT order_id) AS unique_orders
FROM olist_combined_dataset
GROUP BY COALESCE(product_category_name, 'Unknown')
ORDER BY sum_item_price DESC
LIMIT 15;

-- 5. Monthly product-price trend (syntax shown for SQLite)
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS purchase_month,
    SUM(price) AS sum_item_price,
    COUNT(DISTINCT order_id) AS unique_orders
FROM olist_combined_dataset
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY strftime('%Y-%m', order_purchase_timestamp)
ORDER BY purchase_month;

-- Caution: avoid summing payment_value blindly. Joining payment-level values
-- to item-level rows can repeat payment values. Validate join grain first.
