import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# 1. DATABASE CONNECTION
# =========================================================
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "northpeak_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
print("Connecting to PostgreSQL...")

# =========================================================
# 2. DDL SCRIPT WITH INDEXES FOR PERFORMANCE
# =========================================================
ddl_script = """
DROP TABLE IF EXISTS "Fact_Sales" CASCADE;
DROP TABLE IF EXISTS "Dim_Product" CASCADE;
DROP TABLE IF EXISTS "Dim_Customer" CASCADE;
DROP TABLE IF EXISTS "Dim_Geography" CASCADE;
DROP TABLE IF EXISTS "Dim_Date" CASCADE;

-- DIMENSION TABLES
CREATE TABLE "Dim_Product" (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    standard_unit_cost DECIMAL(10, 2) NOT NULL,
    standard_unit_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE "Dim_Customer" (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(30) NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE "Dim_Geography" (
    geography_id INT PRIMARY KEY,
    region VARCHAR(30) NOT NULL,
    channel VARCHAR(30) NOT NULL,
    city VARCHAR(50) NOT NULL
);

CREATE TABLE "Dim_Date" (
    date_key INT PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(15) NOT NULL,
    week_of_year INT NOT NULL,
    day_of_week VARCHAR(15) NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

-- FACT TABLE
CREATE TABLE "Fact_Sales" (
    order_line_id SERIAL PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    date_key INT NOT NULL REFERENCES "Dim_Date"(date_key),
    product_id VARCHAR(20) NOT NULL REFERENCES "Dim_Product"(product_id),
    customer_id VARCHAR(20) NOT NULL REFERENCES "Dim_Customer"(customer_id),
    geography_id INT NOT NULL REFERENCES "Dim_Geography"(geography_id),
    quantity_sold INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    discount_pct DECIMAL(5, 4) NOT NULL,
    gross_revenue DECIMAL(12, 2) NOT NULL,
    discount_amount DECIMAL(12, 2) NOT NULL,
    net_revenue DECIMAL(12, 2) NOT NULL,
    total_cost DECIMAL(12, 2) NOT NULL,
    net_profit DECIMAL(12, 2) NOT NULL,
    margin_pct DECIMAL(6, 4) NOT NULL
);

-- =========================================================
-- INDEX CREATION FOR HIGH-PERFORMANCE SEARCHES & JOINS
-- =========================================================
CREATE INDEX idx_fact_date_key ON "Fact_Sales"(date_key);
CREATE INDEX idx_fact_product_id ON "Fact_Sales"(product_id);
CREATE INDEX idx_fact_customer_id ON "Fact_Sales"(customer_id);
CREATE INDEX idx_fact_geography_id ON "Fact_Sales"(geography_id);
CREATE INDEX idx_fact_order_id ON "Fact_Sales"(order_id);

CREATE INDEX idx_dim_geo_region ON "Dim_Geography"(region);
CREATE INDEX idx_dim_prod_category ON "Dim_Product"(category);
CREATE INDEX idx_dim_cust_segment ON "Dim_Customer"(segment);
"""

with engine.begin() as conn:
    conn.execute(text(ddl_script))
print("Schema and indexes created successfully.")

# =========================================================
# 3. POPULATE CAMEROONIAN DIMENSION DATA
# =========================================================

# A. Dim_Date (3 Years: Jan 2024 - Sep 2026)
date_range = pd.date_range(start="2024-01-01", end="2026-09-30", freq="D")
dim_date = pd.DataFrame({
    'date_key': date_range.strftime('%Y%m%d').astype(int),
    'full_date': date_range.date,
    'year': date_range.year,
    'quarter': date_range.quarter,
    'month': date_range.month,
    'month_name': date_range.strftime('%B'),
    'week_of_year': date_range.isocalendar().week,
    'day_of_week': date_range.strftime('%A'),
    'is_weekend': date_range.dayofweek >= 5
})
dim_date.to_sql('Dim_Date', engine, if_exists='append', index=False)

# B. Dim_Product
products_data = [
    ("PRD-101", "Ergonomic Office Chair", "Furniture", "Chairs", 45000.00, 95000.00),
    ("PRD-102", "Executive Wooden Desk", "Furniture", "Tables", 85000.00, 180000.00),
    ("PRD-103", "Standing Desk Converter", "Furniture", "Furnishings", 30000.00, 65000.00),
    ("PRD-201", "Enterprise Laptop 15\"", "Technology", "Computers", 250000.00, 480000.00),
    ("PRD-202", "27-inch 4K Monitor", "Technology", "Monitors", 90000.00, 175000.00),
    ("PRD-203", "Wireless Noise-Canceling Headset", "Technology", "Accessories", 15000.00, 38000.00),
    ("PRD-301", "A4 Ream Paper Box", "Office Supplies", "Paper & Ink", 12000.00, 22000.00),
    ("PRD-302", "High-Capacity Toner Cartridge", "Office Supplies", "Paper & Ink", 20000.00, 45000.00),
    ("PRD-303", "Heavy Duty Stapler & Binder", "Office Supplies", "Binders", 5000.00, 12000.00)
]
dim_product = pd.DataFrame(products_data, columns=[
    'product_id', 'product_name', 'category', 'sub_category', 'standard_unit_cost', 'standard_unit_price'
])
dim_product.to_sql('Dim_Product', engine, if_exists='append', index=False)

# C. Dim_Geography (All 10 Regions of Cameroon)
cameroon_geo = [
    (1, "Littoral", "Physical Store", "Douala"),
    (2, "Centre", "Physical Store", "Yaoundé"),
    (3, "South-West", "Physical Store", "Buea"),
    (4, "North-West", "Physical Store", "Bamenda"),
    (5, "West", "Physical Store", "Bafoussam"),
    (6, "North", "Physical Store", "Garoua"),
    (7, "Far-North", "Physical Store", "Maroua"),
    (8, "Adamawa", "Physical Store", "Ngaoundéré"),
    (9, "East", "Physical Store", "Bertoua"),
    (10, "South", "Physical Store", "Ebolowa"),
    (11, "Littoral", "Online", "Douala Direct"),
    (12, "Centre", "Online", "Yaoundé Direct"),
    (13, "South-West", "Online", "Buea Direct"),
    (14, "North-West", "Online", "Bamenda Direct")
]
dim_geo = pd.DataFrame(cameroon_geo, columns=['geography_id', 'region', 'channel', 'city'])
dim_geo.to_sql('Dim_Geography', engine, if_exists='append', index=False)

# D. Dim_Customer (Cameroonian Names)
np.random.seed(42)
first_names = ["Emmanuel", "Samuel", "Darryl", "Brenda", "Paul", "Nga", "Fongoh", "Abakar", "Tchinda", "Ateba", "Eboa", "Nfor"]
last_names = ["Eto'o", "Biya", "Mbeki", "Atangana", "Njoya", "Tanyi", "Fouda", "Kamga", "Aboubakar", "Ndongmo", "Bello"]
segments = ['Consumer', 'Corporate', 'Home Office']

num_customers = 1500
customers = []
for i in range(1, num_customers + 1):
    c_name = f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
    customers.append((
        f"CUST-{i:04d}",
        c_name,
        np.random.choice(segments, p=[0.55, 0.30, 0.15]),
        datetime(2023, 1, 1).date() + timedelta(days=int(np.random.randint(0, 700)))
    ))
dim_customer = pd.DataFrame(customers, columns=['customer_id', 'customer_name', 'segment', 'signup_date'])
dim_customer.to_sql('Dim_Customer', engine, if_exists='append', index=False)

print("Dimensions populated.")

# =========================================================
# 4. HIGH-PERFORMANCE BATCH FACT DATA GENERATION (~70,000 ROWS)
# =========================================================
print("Generating ~70,000 sales transaction records in batches...")

TOTAL_RECORDS = 70000
BATCH_SIZE = 10000

date_keys = dim_date['date_key'].values
dates_dt = pd.to_datetime(dim_date['date_key'].astype(str), format='%Y%m%d')
prod_ids = dim_product['product_id'].values
prod_costs = dict(zip(dim_product['product_id'], dim_product['standard_unit_cost']))
prod_prices = dict(zip(dim_product['product_id'], dim_product['standard_unit_price']))
cust_ids = dim_customer['customer_id'].values
geo_ids = dim_geo['geography_id'].values

total_inserted = 0

for batch_start in range(0, TOTAL_RECORDS, BATCH_SIZE):
    current_batch_size = min(BATCH_SIZE, TOTAL_RECORDS - batch_start)
    
    # 1. Random Selections
    b_date_keys = np.random.choice(date_keys, size=current_batch_size)
    b_prod_ids = np.random.choice(prod_ids, size=current_batch_size)
    b_cust_ids = np.random.choice(cust_ids, size=current_batch_size)
    b_geo_ids = np.random.choice(geo_ids, size=current_batch_size)
    b_qty = np.random.randint(1, 12, size=current_batch_size)
    
    # Vectorized Price/Cost Lookup
    b_unit_costs = np.array([prod_costs[p] for p in b_prod_ids])
    b_unit_prices = np.array([prod_prices[p] for p in b_prod_ids])
    
    # 2. Embedded Profit Erosion Logic over time
    # Years: 2024 (Early) -> ~5-10% discount, 2026 (Late) -> ~25-45% discount on Technology/Furniture
    years = b_date_keys // 10000
    time_factor = (years - 2024) / 2.0  # Scales linearly 0.0 -> 1.0
    
    base_discounts = np.random.uniform(0.02, 0.12, size=current_batch_size)
    erosion_boost = time_factor * np.random.uniform(0.15, 0.35, size=current_batch_size)
    
    # Apply extra discounts on specific product lines to simulate targeted margin erosion
    tech_furniture_mask = np.isin(b_prod_ids, ['PRD-101', 'PRD-102', 'PRD-201', 'PRD-202'])
    discount_pct = np.where(tech_furniture_mask, base_discounts + erosion_boost, base_discounts)
    discount_pct = np.clip(discount_pct, 0.0, 0.55).round(4) # Cap max discount at 55%
    
    # 3. Financial Computations
    gross_rev = (b_qty * b_unit_prices).round(2)
    disc_amt = (gross_rev * discount_pct).round(2)
    net_rev = (gross_rev - disc_amt).round(2)
    total_cost = (b_qty * b_unit_costs).round(2)
    net_profit = (net_rev - total_cost).round(2)
    margin_pct = np.where(net_rev > 0, (net_profit / net_rev), 0.0).round(4)
    
    # Order IDs
    order_ids = [f"ORD-{idx:07d}" for idx in range(batch_start + 1, batch_start + current_batch_size + 1)]
    
    # Build Batch DataFrame
    fact_batch = pd.DataFrame({
        'order_id': order_ids,
        'date_key': b_date_keys,
        'product_id': b_prod_ids,
        'customer_id': b_cust_ids,
        'geography_id': b_geo_ids,
        'quantity_sold': b_qty,
        'unit_price': b_unit_prices,
        'unit_cost': b_unit_costs,
        'discount_pct': discount_pct,
        'gross_revenue': gross_rev,
        'discount_amount': disc_amt,
        'net_revenue': net_rev,
        'total_cost': total_cost,
        'net_profit': net_profit,
        'margin_pct': margin_pct
    })
    
    # Fast Batch Insert into PostgreSQL
    fact_batch.to_sql('Fact_Sales', engine, if_exists='append', index=False, method='multi', chunksize=2000)
    
    total_inserted += current_batch_size
    print(f"Batch inserted: {total_inserted}/{TOTAL_RECORDS} rows...")

print("\nSuccess! 70,000 transaction rows inserted successfully into PostgreSQL.")