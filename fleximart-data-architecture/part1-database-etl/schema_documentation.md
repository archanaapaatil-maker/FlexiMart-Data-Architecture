FlexiMart Database Schema Documentation
Entity    Relationship Description

The FlexiMart relational database is designed to store customer, product, and sales transaction data in a normalized relational structure. The schema consists of four core entities: customers, products, orders, and order_items.

Each customer can place multiple orders (one    to    many relationship).
Each order can contain multiple order items (one    to    many relationship).
Each order item is associated with exactly one product (many    to    one relationship).

This structure minimizes redundancy, enforces data integrity, and supports efficient analytical queries.


 
Entity: customers
Purpose: Stores customer information.  
Attributes:
     `customer_id`: Unique identifier (Primary Key, Auto Increment)
     `first_name`: Customer’s first name
     `last_name`: Customer’s last name
     `email`: Customer’s email (unique, required)
     `phone`: Standardized phone number
     `city`: Customer’s city of residence
     `registration_date`: Date of registration (YYYY    MM    DD)

Relationships:  
     One customer can place many orders (1:M with orders table).

  
Entity: products
      Purpose:       Stores product catalog information.  
      Attributes:      
     `product_id`: Unique identifier (Primary Key, Auto Increment)
     `product_name`: Name of the product
     `category`: Standardized product category (Electronics, Fashion, Groceries, etc.)
     `price`: Product price (decimal)
     `stock_quantity`: Available stock (integer)

      Relationships:        
     One product can appear in many order_items (1:M with order_items table).

  
     Entity: orders
      Purpose:       Stores customer orders.  
      Attributes:      
     `order_id`: Unique identifier (Primary Key, Auto Increment)
     `customer_id`: Foreign Key referencing customers
     `order_date`: Date of the order
     `total_amount`: Total order value
     `status`: Order status (Completed, Pending, Cancelled)

      Relationships:        
     One order belongs to one customer (M:1 with customers).  
     One order can contain many order_items (1:M with order_items).

  
     Entity: order_items
      Purpose:       Stores details of products within each order.  
      Attributes:      
     `order_item_id`: Unique identifier (Primary Key, Auto Increment)
     `order_id`: Foreign Key referencing orders
     `product_id`: Foreign Key referencing products
     `quantity`: Number of units purchased
     `unit_price`: Price per unit
     `subtotal`: Calculated as quantity × unit_price

      Relationships:        
     Each order_item belongs to one order (M:1 with orders).  
     Each order_item belongs to one product (M:1 with products).

  
Normalization Explanation (3NF Justification)

The FlexiMart schema is designed in Third Normal Form (3NF)       to eliminate redundancy and anomalies:

           Functional Dependencies:        
       Customer attributes depend only on `customer_id`.  
       Product attributes depend only on `product_id`.  
       Order attributes depend only on `order_id`.  
       Order_item attributes depend only on `order_item_id`.  

     Avoiding Anomalies:  
             Update anomaly:       Customer details are stored once in the customers table, so updating an email does not require changes in multiple places.  
             Insert anomaly:       New products can be added without requiring an order record.  
             Delete anomaly:       Deleting an order does not remove product or customer information, since they are stored separately.  

This design ensures data integrity, supports scalability, and avoids duplication.

  
Sample Data Representation

      customers
| customer_id | first_name | last_name | email                  | phone         | city      | registration_date |
|                                                    |                                                |                                            |                                                                                                |                                                            |                                            |                                                                            |
| 1           | Rahul      | Sharma    | rahul.sharma@gmail.com | +91    9876543210| Bangalore | 2023    01    15        |
| 2           | Priya      | Patel     | priya.patel@yahoo.com  | +91    9988776655| Mumbai    | 2023    02    20        |

       products
| product_id | product_name        | category    | price   | stock_quantity |
|                                                |                                                                                    |                                                    |                                    |                                                                |
| 1          | Samsung Galaxy S21  | Electronics | 45999.00| 150            |
| 2          | Nike Running Shoes  | Fashion     | 3499.00 | 80             |

       orders
| order_id | customer_id | order_date | total_amount | status    |
|                                        |                                                    |                                                |                                                        |                                            |
| 1        | 1           | 2024    01    15 | 45999.00     | Completed |
| 2        | 2           | 2024    01    16 | 5998.00      | Completed |

       order_items
| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|                                                            |                                                                                                   |                                        |
| 1             | 1        | 1          | 1        | 45999.00   | 45999.00 |
| 2             | 2        | 2          | 2        | 2999.00    | 5998.00  |
