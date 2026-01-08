# FlexiMart Data Architecture Project

Student Name: Archana Sumeet Patil
Student ID:bitsom_ba_25071469
Email: archanaapaatil@gmail.com
Date:22/12/2025

Project Overview

This project is part of the Data for Artificial Intelligence course.  
It demonstrates the complete design and implementation of a data pipeline for FlexiMart, an e-commerce company.  
The pipeline covers ETL (Extract, Transform, Load), Relational Database Design,Business Queries,NoSQL Analysis with MongoDB,and a Data Warehouse with Star Schema.

## Repository Structure
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   └── data_quality_report.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   └── analytics_queries.sql
└── README.md



Technologies Used
Python (pandas, mysql-connector) → ETL pipeline
MySQL → Relational database
MongoDB → NoSQL product catalog
SQL (OLAP) → Data warehouse analytics
GitHub → Submission and version control

Setup Instructions

Database Setup

bash
Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql


MongoDB Setup
Import product catalog JSON
mongoimport --db fleximart --collection products --file part2-nosql/products_catalog.json --jsonArray

Run MongoDB operations
mongosh < part2-nosql/mongodb_operations.js


 Key Learnings
Through this project, I learned how to design and implement a complete data pipeline from raw files to analytics.
I understood the importance of data cleaning (handling duplicates, missing values, inconsistent formats).
I practiced SQL queries for business insights and explored NoSQL flexibility for product catalogs.
Finally, I gained experience in building a star schema for a data warehouse to support OLAP-style reporting.

Challenges Faced
Challenges Faced
Challenge: Handling inconsistent date and phone formats in raw CSV files.
Solution: Used Python’s pandas library to standardize formats and ensure consistency before loading into MySQL.

Challenge: Understanding the difference between relational and NoSQL databases.
Solution: Documented RDBMS limitations and MongoDB benefits, then implemented queries to demonstrate flexibility with embedded documents.







