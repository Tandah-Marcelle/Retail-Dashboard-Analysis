# Data Dictionary
## Northpeak Retail Analytics — PostgreSQL Star Schema

**Database:** `northpeak_db`  
**Version:** 1.0  
**Last Updated:** October 2026

---

## Overview

The database follows a **star schema** design pattern with one central fact table (`Fact_Sales`) surrounded by four dimension tables (`Dim_Date`, `Dim_Product`, `Dim_Customer`, `Dim_Geography`).

---

## Table: Fact_Sales

The central transaction table. Each row represents one order line item.

| Column | Data Type | Nullable | Description |
|--------|-----------|----------|-------------|
| `order_line_id` | SERIAL (PK) | NO | Auto-incremented unique identifier for each order line |
| `order_id` | VARCHAR(30) | NO | Order identifier in format `ORD-0000001` |
| `date_key` | INT (FK) | NO | Foreign key to `Dim_Date.date_key` (format: YYYYMMDD) |
| `product_id` | VARCHAR(20) (FK) | NO | Foreign key to `Dim_Product.product_id` |
| `customer_id` | VARCHAR(20) (FK) | NO | Foreign key to `Dim_Customer.customer_id` |
| `geography_id` | INT (FK) | NO | Foreign key to `Dim_Geography.geography_id` |
| `quantity_sold` | INT | NO | Number of units sold in this transaction (range: 1–11) |
| `unit_price` | DECIMAL(10,2) | NO | Selling price per unit in XAF (from product standard price) |
| `unit_cost` | DECIMAL(10,2) | NO | Cost per unit in XAF (from product standard cost) |
| `discount_pct` | DECIMAL(5,4) | NO | Discount rate applied (0.0000 to 0.5500) |
| `gross_revenue` | DECIMAL(12,2) | NO | Revenue before discount: `quantity_sold × unit_price` |
| `discount_amount` | DECIMAL(12,2) | NO | Total discount value: `gross_revenue × discount_pct` |
| `net_revenue` | DECIMAL(12,2) | NO | Revenue after discount: `gross_revenue - discount_amount` |
| `total_cost` | DECIMAL(12,2) | NO | Total cost of goods sold: `quantity_sold × unit_cost` |
| `net_profit` | DECIMAL(12,2) | NO | Profit after costs: `net_revenue - total_cost` |
| `margin_pct` | DECIMAL(6,4) | NO | Profit margin ratio: `net_profit / net_revenue` |

**Indexes:**
- `idx_fact_date_key` on `date_key`
- `idx_fact_product_id` on `product_id`
- `idx_fact_customer_id` on `customer_id`
- `idx_fact_geography_id` on `geography_id`
- `idx_fact_order_id` on `order_id`

---

## Table: Dim_Product

Reference table for all products sold by Northpeak.

| Column | Data Type | Nullable | Description |
|--------|-----------|----------|-------------|
| `product_id` | VARCHAR(20) (PK) | NO | Unique product code (e.g., `PRD-101`) |
| `product_name` | VARCHAR(150) | NO | Full name of the product |
| `category` | VARCHAR(50) | NO | Top-level category: `Furniture`, `Technology`, `Office Supplies` |
| `sub_category` | VARCHAR(50) | NO | Sub-category within the category |
| `standard_unit_cost` | DECIMAL(10,2) | NO | Standard cost of one unit in XAF |
| `standard_unit_price` | DECIMAL(10,2) | NO | Standard selling price of one unit in XAF |

**Product Catalog:**

| product_id | product_name | category | sub_category | unit_cost (XAF) | unit_price (XAF) |
|------------|--------------|----------|--------------|-----------------|------------------|
| PRD-101 | Ergonomic Office Chair | Furniture | Chairs | 45,000 | 95,000 |
| PRD-102 | Executive Wooden Desk | Furniture | Tables | 85,000 | 180,000 |
| PRD-103 | Standing Desk Converter | Furniture | Furnishings | 30,000 | 65,000 |
| PRD-201 | Enterprise Laptop 15" | Technology | Computers | 250,000 | 480,000 |
| PRD-202 | 27-inch 4K Monitor | Technology | Monitors | 90,000 | 175,000 |
| PRD-203 | Wireless Noise-Canceling Headset | Technology | Accessories | 15,000 | 38,000 |
| PRD-301 | A4 Ream Paper Box | Office Supplies | Paper & Ink | 12,000 | 22,000 |
| PRD-302 | High-Capacity Toner Cartridge | Office Supplies | Paper & Ink | 20,000 | 45,000 |
| PRD-303 | Heavy Duty Stapler & Binder | Office Supplies | Binders | 5,000 | 12,000 |

**Index:** `idx_dim_prod_category` on `category`

---

## Table: Dim_Customer

Reference table for all customers.

| Column | Data Type | Nullable | Description |
|--------|-----------|----------|-------------|
| `customer_id` | VARCHAR(20) (PK) | NO | Unique customer ID in format `CUST-0001` |
| `customer_name` | VARCHAR(100) | NO | Full name (Cameroonian names, synthetic) |
| `segment` | VARCHAR(30) | NO | Customer segment: `Consumer`, `Corporate`, `Home Office` |
| `signup_date` | DATE | NO | Date customer registered (Jan 2023 – Dec 2024) |

**Segment Distribution:**
- Consumer: 55%
- Corporate: 30%
- Home Office: 15%

**Total Customers:** 1,500

**Index:** `idx_dim_cust_segment` on `segment`

---

## Table: Dim_Geography

Reference table for all store/channel locations.

| Column | Data Type | Nullable | Description |
|--------|-----------|----------|-------------|
| `geography_id` | INT (PK) | NO | Unique geography identifier |
| `region` | VARCHAR(30) | NO | One of Cameroon's 10 administrative regions |
| `channel` | VARCHAR(30) | NO | Sales channel: `Physical Store` or `Online` |
| `city` | VARCHAR(50) | NO | City name (or "City Direct" for online entries) |

**Geography Entries:**

| geography_id | region | channel | city |
|--------------|--------|---------|------|
| 1 | Littoral | Physical Store | Douala |
| 2 | Centre | Physical Store | Yaoundé |
| 3 | South-West | Physical Store | Buea |
| 4 | North-West | Physical Store | Bamenda |
| 5 | West | Physical Store | Bafoussam |
| 6 | North | Physical Store | Garoua |
| 7 | Far-North | Physical Store | Maroua |
| 8 | Adamawa | Physical Store | Ngaoundéré |
| 9 | East | Physical Store | Bertoua |
| 10 | South | Physical Store | Ebolowa |
| 11 | Littoral | Online | Douala Direct |
| 12 | Centre | Online | Yaoundé Direct |
| 13 | South-West | Online | Buea Direct |
| 14 | North-West | Online | Bamenda Direct |

**Index:** `idx_dim_geo_region` on `region`

---

## Table: Dim_Date

Date dimension for time-based analysis.

| Column | Data Type | Nullable | Description |
|--------|-----------|----------|-------------|
| `date_key` | INT (PK) | NO | Date in integer format YYYYMMDD (e.g., 20240115) |
| `full_date` | DATE | NO | Full date value |
| `year` | INT | NO | 4-digit year (2024, 2025, 2026) |
| `quarter` | INT | NO | Quarter number (1–4) |
| `month` | INT | NO | Month number (1–12) |
| `month_name` | VARCHAR(15) | NO | Month name (e.g., "January") |
| `week_of_year` | INT | NO | ISO week number (1–53) |
| `day_of_week` | VARCHAR(15) | NO | Day name (e.g., "Monday") |
| `is_weekend` | BOOLEAN | NO | `TRUE` if Saturday or Sunday |

**Date Range:** January 1, 2024 – September 30, 2026  
**Total Rows:** 1,004 calendar days

---

## Key Calculations Reference

| Metric | Formula |
|--------|---------|
| Gross Revenue | `quantity_sold × unit_price` |
| Discount Amount | `gross_revenue × discount_pct` |
| Net Revenue | `gross_revenue - discount_amount` |
| Total Cost | `quantity_sold × unit_cost` |
| Net Profit | `net_revenue - total_cost` |
| Margin % | `net_profit / net_revenue` |
| Standard Margin (no discount) | `(unit_price - unit_cost) / unit_price` |
