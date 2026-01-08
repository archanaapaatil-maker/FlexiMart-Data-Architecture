   FlexiMart Data Warehouse: Star Schema Design

     Overview
The FlexiMart data warehouse is designed to support analytical reporting and business intelligence.  
We use a     Star Schema     model, which consists of a central     Fact Table     surrounded by multiple     Dimension Tables    .  
This design simplifies queries, improves performance, and aligns with OLAP (Online Analytical Processing) requirements.

  

     Fact Table: fact_sales
    Purpose:     Stores transactional sales data for analysis.  
    Attributes:    
- `sales_id` (Primary Key, surrogate key)
- `order_id` (Reference to source system)
- `customer_id` (FK → dim_customer)
- `product_id` (FK → dim_product)
- `date_id` (FK → dim_date)
- `quantity`
- `unit_price`
- `subtotal`
- `total_amount`

  

     Dimension Tables

       dim_customer
- `customer_id` (Primary Key)
- `first_name`
- `last_name`
- `email`
- `city`
- `registration_date`

       dim_product
- `product_id` (Primary Key)
- `product_name`
- `category`
- `price`
- `stock_quantity`

       dim_date
- `date_id` (Primary Key, surrogate key)
- `full_date`
- `day`
- `month`
- `quarter`
- `year`

       dim_order
- `order_id` (Primary Key)
- `status`
- `order_date`

  

     Relationships
-     fact_sales → dim_customer    : Many sales records can belong to one customer.  
-     fact_sales → dim_product    : Many sales records can reference one product.  
-     fact_sales → dim_date    : Each sale is associated with one date.  
-     fact_sales → dim_order    : Each sale belongs to one order.

  

     Why Star Schema?
-     Simplicity:     Easy to understand and query for business analysts.  
-     Performance:     Optimized for aggregation queries (SUM, COUNT, AVG).  
-     Flexibility:     Supports slicing and dicing across multiple dimensions (customer, product, time).  
-     Scalability:     Can handle large volumes of sales data efficiently.

  

     Sample Representation

       fact_sales
| sales_id | order_id | customer_id | product_id | date_id | quantity | unit_price | subtotal | total_amount |
|      -|      -|        -|        |      |      -|        |      -|        --|
| 1        | 101      | 1           | 1          | 20240115| 1        | 45999.00   | 45999.00 | 45999.00     |
| 2        | 102      | 2           | 2          | 20240116| 2        | 2999.00    | 5998.00  | 5998.00      |

       dim_customer
| customer_id | first_name | last_name | city      |
|        -|        |      --|      --|
| 1           | Rahul      | Sharma    | Bangalore |
| 2           | Priya      | Patel     | Mumbai    |

       dim_product
| product_id | product_name       | category    | price   |
|        |            --|        -|      |
| 1          | Samsung Galaxy S21 | Electronics | 45999.00|
| 2          | Nike Running Shoes | Fashion     | 3499.00 |

       dim_date
| date_id  | full_date  | day | month | quarter | year |
|      -|        |  --|    -|      |    |
| 20240115 | 2024-01-15 | 15  | Jan   | Q1      | 2024 |
| 20240116 | 2024-01-16 | 16  | Jan   | Q1      | 2024 |
