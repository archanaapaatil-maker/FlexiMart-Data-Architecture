import os
import re
import pandas as pd
import mysql.connector
from datetime import datetime

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "2244@NKB"  
DB_NAME = "fleximart"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CUSTOMERS_CSV = os.path.join(BASE_DIR, "customers_raw.csv")
PRODUCTS_CSV = os.path.join(BASE_DIR, "products_raw.csv")
SALES_CSV = os.path.join(BASE_DIR, "sales_raw.csv")
REPORT_PATH = os.path.join(BASE_DIR, "data_quality_report.txt")

# ========= HELPERS =========
def standardize_email(email):
    if pd.isna(email) or str(email).strip() == "":
        return None
    return str(email).strip().lower().replace(" ", "")

def standardize_phone(phone):
    if pd.isna(phone) or str(phone).strip() == "":
        return None
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) >= 12 and digits.startswith("91"):
        digits = digits[-10:]
    if len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"+91-{digits}"
    return None

def parse_date(date_str):
    if pd.isna(date_str) or str(date_str).strip() == "":
        return None
    try:
        return pd.to_datetime(date_str, dayfirst=True).strftime("%Y-%m-%d")
    except:
        return None

def normalize_category(cat):
    if pd.isna(cat) or str(cat).strip() == "":
        return None
    c = str(cat).strip().lower()
    if "electronic" in c: return "Electronics"
    if "fashion" in c: return "Fashion"
    if "grocery" in c: return "Groceries"
    return c.title()

# ========= CONNECT =========
def get_connection():
    return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)

def ensure_schema(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS fleximart;")
    cursor.execute("USE fleximart;")
    cursor.execute("DROP TABLE IF EXISTS order_items;")
    cursor.execute("DROP TABLE IF EXISTS orders;")
    cursor.execute("DROP TABLE IF EXISTS products;")
    cursor.execute("DROP TABLE IF EXISTS customers;")

    cursor.execute("""
    CREATE TABLE customers (
        customer_id INT PRIMARY KEY AUTO_INCREMENT,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20),
        city VARCHAR(50),
        registration_date DATE
    );
    """)
    cursor.execute("""
    CREATE TABLE products (
        product_id INT PRIMARY KEY AUTO_INCREMENT,
        product_name VARCHAR(100),
        category VARCHAR(50),
        price DECIMAL(10,2),
        stock_quantity INT DEFAULT 0
    );
    """)
    cursor.execute("""
    CREATE TABLE orders (
        order_id INT PRIMARY KEY AUTO_INCREMENT,
        customer_id INT,
        order_date DATE,
        total_amount DECIMAL(10,2),
        status VARCHAR(20),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    """)
    cursor.execute("""
    CREATE TABLE order_items (
        order_item_id INT PRIMARY KEY AUTO_INCREMENT,
        order_id INT,
        product_id INT,
        quantity INT,
        unit_price DECIMAL(10,2),
        subtotal DECIMAL(10,2),
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """)

# ========= TRANSFORM =========
def transform_customers(df):
    original_count = len(df)

    df["email"] = df["email"].apply(standardize_email)
    df["phone"] = df["phone"].apply(standardize_phone)
    df["city"] = df["city"].apply(lambda x: str(x).title() if pd.notna(x) else None)
    df["registration_date"] = df["registration_date"].apply(parse_date)

    # Remove duplicates by customer_id first
    df = df.drop_duplicates(subset=["customer_id"], keep="first")

    # Remove duplicates by email
    df = df.drop_duplicates(subset=["email"], keep="first")

    # Drop rows with missing email
    missing_emails = df["email"].isna().sum()
    df = df.dropna(subset=["email"])

    transformed_count = len(df)
    return df, {
        "processed": original_count,
        "duplicates_removed": original_count - len(df),
        "missing_emails_dropped": missing_emails,
        "loaded": transformed_count
    }

def transform_products(df):
    original_count = len(df)

    df["product_name"] = df["product_name"].str.strip()
    df["category"] = df["category"].apply(normalize_category)
    df["stock_quantity"] = df["stock_quantity"].fillna(0).astype(int)
    missing_prices = df["price"].isna().sum()
    df = df.dropna(subset=["price"])
    df = df.drop_duplicates(subset=["product_id"], keep="first")

    transformed_count = len(df)
    return df, {
        "processed": original_count,
        "duplicates_removed": original_count - len(df),
        "missing_prices_dropped": missing_prices,
        "loaded": transformed_count
    }

def transform_sales(df):
    original_count = len(df)

    for col in ["transaction_id", "customer_id", "product_id", "status"]:
        df[col] = df[col].apply(lambda s: str(s).strip() if pd.notna(s) else s)

    df["transaction_date"] = df["transaction_date"].apply(parse_date)

    # Remove duplicate transactions
    df = df.drop_duplicates(subset=["transaction_id"], keep="first")

    # Drop rows with missing customer_id or product_id
    missing_customer_ids = df["customer_id"].isna().sum() + (df["customer_id"] == "").sum()
    missing_product_ids = df["product_id"].isna().sum() + (df["product_id"] == "").sum()
    df = df[df["customer_id"].notna() & (df["customer_id"].str.strip() != "")]
    df = df[df["product_id"].notna() & (df["product_id"].str.strip() != "")]

    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)
    df["subtotal"] = df["quantity"] * df["unit_price"]

    transformed_count = len(df)
    return df, {
        "processed": original_count,
        "duplicates_removed": original_count - len(df),
        "missing_customer_ids_dropped": missing_customer_ids,
        "missing_product_ids_dropped": missing_product_ids,
        "loaded": transformed_count
    }

# ========= LOAD =========
def load_to_mysql(customers_df, products_df, sales_df):
    cnx = get_connection()
    cursor = cnx.cursor()
    ensure_schema(cursor)

    cursor.execute("USE fleximart;")

    cust_map = {}
    for _, row in customers_df.iterrows():
        cursor.execute("INSERT INTO customers (first_name,last_name,email,phone,city,registration_date) VALUES (%s,%s,%s,%s,%s,%s)",
                       (row["first_name"], row["last_name"], row["email"], row["phone"], row["city"], row["registration_date"]))
        cust_map[row["customer_id"]] = cursor.lastrowid

    prod_map = {}
    for _, row in products_df.iterrows():
        cursor.execute("INSERT INTO products (product_name,category,price,stock_quantity) VALUES (%s,%s,%s,%s)",
                       (row["product_name"], row["category"], row["price"], row["stock_quantity"]))
        prod_map[row["product_id"]] = cursor.lastrowid

    for tx_id, group in sales_df.groupby("transaction_id"):
        cid = group.iloc[0]["customer_id"]
        if cid not in cust_map: continue
        order_date = group.iloc[0]["transaction_date"]
        status = group.iloc[0]["status"]
        total_amount = group["subtotal"].sum()
        cursor.execute("INSERT INTO orders (customer_id,order_date,total_amount,status) VALUES (%s,%s,%s,%s)",
                       (cust_map[cid], order_date, total_amount, status))
        order_id = cursor.lastrowid
        for _, row in group.iterrows():
            pid = row["product_id"]
            if pid not in prod_map: continue
            cursor.execute("INSERT INTO order_items (order_id,product_id,quantity,unit_price,subtotal) VALUES (%s,%s,%s,%s,%s)",
                           (order_id, prod_map[pid], row["quantity"], row["unit_price"], row["subtotal"]))

    cnx.commit()

# ========= PIPELINE =========
def main():
    customers_raw = pd.read_csv(CUSTOMERS_CSV)
    products_raw = pd