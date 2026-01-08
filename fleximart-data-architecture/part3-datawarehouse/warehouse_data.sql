 -- FlexiMart Data Warehouse Data Loading
USE fleximart_dw;

-- Load Dimension: Customer
INSERT INTO dim_customer (customer_id, first_name, last_name, email, city, registration_date)
SELECT customer_id, first_name, last_name, email, city, registration_date
FROM fleximart.customers;

-- Load Dimension: Product
INSERT INTO dim_product (product_id, product_name, category, price, stock_quantity)
SELECT product_id, product_name, category, price, stock_quantity
FROM fleximart.products;

-- Load Dimension: Date
-- Generate surrogate date_id as YYYYMMDD
INSERT INTO dim_date (date_id, full_date, day, month, quarter, year)
SELECT 
    DATE_FORMAT(order_date, '%Y%m%d') AS date_id,
    order_date AS full_date,
    DAY(order_date) AS day,
    MONTHNAME(order_date) AS month,
    CONCAT('Q', QUARTER(order_date)) AS quarter,
    YEAR(order_date) AS year
FROM fleximart.orders
GROUP BY order_date;

-- Load Dimension: Order
INSERT INTO dim_order (order_id, status, order_date)
SELECT order_id, status, order_date
FROM fleximart.orders;

-- Load Fact Table: Sales
INSERT INTO fact_sales (order_id, customer_id, product_id, date_id, quantity, unit_price, subtotal, total_amount)
SELECT 
    oi.order_id,
    o.customer_id,
    oi.product_id,
    DATE_FORMAT(o.order_date, '%Y%m%d') AS date_id,
    oi.quantity,
    oi.unit_price,
    oi.subtotal,
    o.total_amount
FROM fleximart.order_items oi
JOIN fleximart.orders o ON oi.order_id = o.order_id;

