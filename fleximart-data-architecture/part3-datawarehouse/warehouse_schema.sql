-- FlexiMart Data Warehouse Schema
-- Star Schema Design

-- Create database for warehouse
CREATE DATABASE fleximart_dw;
USE fleximart_dw;

-- Dimension: Customer
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    registration_date DATE
);

-- Dimension: Product
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INT
);

-- Dimension: Date
CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    day INT,
    month VARCHAR(15),
    quarter VARCHAR(5),
    year INT
);

-- Dimension: Order
CREATE TABLE dim_order (
    order_id INT PRIMARY KEY,
    status VARCHAR(20),
    order_date DATE
);

-- Fact Table: Sales
CREATE TABLE fact_sales (
    sales_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    customer_id INT,
    product_id INT,
    date_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    subtotal DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (order_id) REFERENCES dim_order(order_id)
);
 
