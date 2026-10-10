# Process Maps
## Northpeak Retail Analytics — End-to-End Data Flow

**Version:** 1.0  
**Date:** October 2026

---

## 1. Overview

This document describes the complete data flow from raw generation through to the final Power BI dashboard. Each process is described with inputs, outputs, tools, and step-by-step logic.

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     NORTHPEAK DATA PIPELINE                      │
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │   Python     │    │  PostgreSQL  │    │    Power BI      │   │
│  │  Data Gen    │───►│  Star Schema │───►│   Dashboard      │   │
│  │  Script      │    │  northpeak_db│    │  (Visualization) │   │
│  └──────────────┘    └──────────────┘    └──────────────────┘   │
│         │                   │                      │             │
│    script_generate    northpeak_db          Northpeak retail     │
│    _data.py           (5 tables)            Dashboard            │
│                                             Analysis.pbix        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Process 1: Environment Setup

**Purpose:** Prepare the development environment before running the pipeline.

```
START
  │
  ├── 1. Clone repository from GitHub
  │
  ├── 2. Create virtual environment (optional but recommended)
  │         python -m venv venv
  │         venv\Scripts\activate  (Windows)
  │
  ├── 3. Install dependencies
  │         pip install -r requirements.txt
  │
  ├── 4. Copy .env.example to .env
  │         cp .env.example .env
  │
  ├── 5. Fill in database credentials in .env
  │         DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
  │
  ├── 6. Ensure PostgreSQL is running locally
  │         Default port: 5432
  │
  └── 7. Create target database in PostgreSQL
            CREATE DATABASE northpeak_db;

END
```

---

## 4. Process 2: Data Generation & Loading (`script_generate_data.py`)

**Purpose:** Generate synthetic retail data and load it into PostgreSQL.

```
START
  │
  ├── STEP 1: Load Environment Variables
  │         load_dotenv() reads credentials from .env
  │         Constructs SQLAlchemy connection engine
  │
  ├── STEP 2: Schema Creation (DDL)
  │         Drops existing tables (CASCADE) if they exist
  │         Creates dimension tables:
  │           ├── Dim_Date
  │           ├── Dim_Product
  │           ├── Dim_Customer
  │           └── Dim_Geography
  │         Creates fact table:
  │           └── Fact_Sales (with FK constraints)
  │         Creates performance indexes (9 total)
  │
  ├── STEP 3: Populate Dim_Date
  │         Generates date range: Jan 1, 2024 → Sep 30, 2026
  │         Computes: year, quarter, month, month_name,
  │                   week_of_year, day_of_week, is_weekend
  │         Loads ~1,004 rows via pandas .to_sql()
  │
  ├── STEP 4: Populate Dim_Product
  │         9 products across 3 categories defined inline
  │         Loads via pandas .to_sql()
  │
  ├── STEP 5: Populate Dim_Geography
  │         14 entries: 10 physical + 4 online
  │         All 10 Cameroon regions represented
  │         Loads via pandas .to_sql()
  │
  ├── STEP 6: Populate Dim_Customer
  │         np.random.seed(42) ensures reproducibility
  │         Generates 1,500 customers with:
  │           ├── Cameroonian first + last names
  │           ├── Segment (Consumer 55%, Corporate 30%, Home Office 15%)
  │           └── signup_date (random within Jan 2023 – Dec 2024)
  │         Loads via pandas .to_sql()
  │
  └── STEP 7: Generate & Load Fact_Sales (Batched)
            Total records: 70,000
            Batch size: 10,000 (7 batches)
            │
            For each batch:
              ├── Random sample: date_key, product_id, customer_id, geography_id
              ├── Random quantity: 1–11 units
              ├── Vectorized cost/price lookup from product arrays
              │
              ├── PROFIT EROSION LOGIC:
              │     years = date_key // 10000
              │     time_factor = (year - 2024) / 2.0     [0.0 → 1.0]
              │     base_discount = random(2%–12%)
              │     erosion_boost = time_factor × random(15%–35%)
              │     Final discount = base + erosion (only for PRD-101/102/201/202)
              │     Clipped at max 55%
              │
              ├── FINANCIAL CALCULATIONS:
              │     gross_revenue = qty × unit_price
              │     discount_amount = gross_revenue × discount_pct
              │     net_revenue = gross_revenue - discount_amount
              │     total_cost = qty × unit_cost
              │     net_profit = net_revenue - total_cost
              │     margin_pct = net_profit / net_revenue (0 if net_rev = 0)
              │
              └── Batch insert via .to_sql(method='multi', chunksize=2000)

END → 70,000 rows in Fact_Sales ✅
```

---

## 5. Process 3: Exploratory Analysis (Jupyter Notebook)

**Purpose:** Visualize and validate key business insights from the data.

```
START
  │
  ├── STEP 1: Connect to PostgreSQL
  │         load_dotenv() → build SQLAlchemy engine
  │
  ├── STEP 2: Query Data
  │         JOIN Fact_Sales with Dim_Date and Dim_Product
  │         Pull: discount_pct, quantity_sold, unit_cost, unit_price,
  │               net_revenue, net_profit, margin_pct, year, quarter, category
  │
  ├── STEP 3: Set Visualization Style
  │         sns.set_theme(style="whitegrid", palette="muted")
  │
  └── STEP 4: Generate Visualizations
            ├── Margin % over time by category (line chart)
            ├── Discount rate trend (bar or line chart)
            ├── Revenue and profit by category
            └── Additional exploratory charts

END → Charts saved / displayed in notebook
```

---

## 6. Process 4: Power BI Dashboard

**Purpose:** Deliver interactive business intelligence dashboard for stakeholders.

```
START
  │
  ├── STEP 1: Connect Power BI to PostgreSQL
  │         Get Data → PostgreSQL
  │         Server: localhost, Database: northpeak_db
  │
  ├── STEP 2: Import Tables
  │         Import: Fact_Sales, Dim_Date, Dim_Product,
  │                 Dim_Customer, Dim_Geography
  │
  ├── STEP 3: Define/Verify Relationships
  │         Fact_Sales[date_key] → Dim_Date[date_key]
  │         Fact_Sales[product_id] → Dim_Product[product_id]
  │         Fact_Sales[customer_id] → Dim_Customer[customer_id]
  │         Fact_Sales[geography_id] → Dim_Geography[geography_id]
  │
  ├── STEP 4: Build Measures (DAX)
  │         Total Net Revenue = SUM(Fact_Sales[net_revenue])
  │         Total Net Profit = SUM(Fact_Sales[net_profit])
  │         Avg Margin % = AVERAGE(Fact_Sales[margin_pct])
  │         Total Transactions = COUNTROWS(Fact_Sales)
  │
  ├── STEP 5: Build Report Pages
  │         ├── Page 1: Executive Summary (KPI cards + trend lines)
  │         ├── Page 2: Category & Product Analysis
  │         ├── Page 3: Regional & Channel Performance
  │         └── Page 4: Customer Segment Analysis
  │
  └── STEP 6: Add Slicers/Filters
            ├── Year / Quarter / Month
            ├── Product Category
            ├── Region & Channel
            └── Customer Segment

END → .pbix file saved in /powerbi/
```

---

## 7. Data Flow Summary

```
.env (credentials)
     │
     ▼
script_generate_data.py
     │
     ├── Creates schema in PostgreSQL
     ├── Inserts: Dim_Date (1,004 rows)
     ├── Inserts: Dim_Product (9 rows)
     ├── Inserts: Dim_Geography (14 rows)
     ├── Inserts: Dim_Customer (1,500 rows)
     └── Inserts: Fact_Sales (70,000 rows)
                    │
                    ▼
            northpeak_db (PostgreSQL)
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   Jupyter Notebook      Power BI Desktop
   (Python charts)       (Interactive dashboard)
          │                   │
          ▼                   ▼
   /notebooks/            /powerbi/
   visualization_         Northpeak retail
   retail_analysis        Dashboard Analysis.pbix
   .ipynb
```
