-- FlexiMart Data Warehouse Analytics Queries

-- Query 1: Top Customers by Spending
-- Show top 5 customers with highest total spending in 2024
SELECT 
    CONCAT(dc.first_name, ' ', dc.last_name) AS customer_name,
    SUM(fs.total_amount) AS total_spent
FROM fact_sales fs
JOIN dim_customer dc ON fs.customer_id = dc.customer_id
JOIN dim_date dd ON fs.date_id = dd.date_id
WHERE dd.year = 2024
GROUP BY dc.customer_id, dc.first_name, dc.last_name
ORDER BY total_spent DESC
LIMIT 5;


-- Query 2: Category Revenue Analysis
-- Show revenue by product category for 2024
SELECT 
    dp.category,
    SUM(fs.quantity) AS total_quantity,
    SUM(fs.subtotal) AS total_revenue
FROM fact_sales fs
JOIN dim_product dp ON fs.product_id = dp.product_id
JOIN dim_date dd ON fs.date_id = dd.date_id
WHERE dd.year = 2024
GROUP BY dp.category
ORDER BY total_revenue DESC;


-- Query 3: Monthly Sales Trend
-- Show monthly revenue and cumulative revenue for 2024
SELECT 
    dd.month AS month_name,
    SUM(fs.total_amount) AS monthly_revenue,
    SUM(SUM(fs.total_amount)) OVER (ORDER BY dd.month) AS cumulative_revenue
FROM fact_sales fs
JOIN dim_date dd ON fs.date_id = dd.date_id
WHERE dd.year = 2024
GROUP BY dd.month
ORDER BY MIN(dd.full_date);


-- Query 4: Product Performance
-- Show top 5 products by total quantity sold in 2024
SELECT 
    dp.product_name,
    SUM(fs.quantity) AS total_quantity_sold
FROM fact_sales fs
JOIN dim_product dp ON fs.product_id = dp.product_id
JOIN dim_date dd ON fs.date_id = dd.date_id
WHERE dd.year = 2024
GROUP BY dp.product_id, dp.product_name
ORDER BY total_quantity_sold DESC
LIMIT 5;
 
