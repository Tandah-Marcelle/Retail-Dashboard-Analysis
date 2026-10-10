# Data Model
## Northpeak Retail Analytics — Star Schema Design

**Version:** 1.0  
**Database:** PostgreSQL (`northpeak_db`)  
**Pattern:** Star Schema (Kimball methodology)

---

## 1. Schema Overview

The data model follows a classic **star schema** — one central fact table connected to four dimension tables. This pattern is optimized for analytical queries and BI tool compatibility.

```
                    ┌──────────────┐
                    │  Dim_Date    │
                    │──────────────│
                    │ date_key(PK) │
                    │ full_date    │
                    │ year         │
                    │ quarter      │
                    │ month        │
                    │ month_name   │
                    │ week_of_year │
                    │ day_of_week  │
                    │ is_weekend   │
                    └──────┬───────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
┌────────┴──────┐  ┌───────▼────────┐  ┌────┴────────────┐
│  Dim_Product  │  │   Fact_Sales   │  │  Dim_Customer   │
│───────────────│  │────────────────│  │─────────────────│
│ product_id(PK)│◄─┤ product_id(FK) │  │ customer_id(PK) │
│ product_name  │  │ date_key(FK)   ├─►│ customer_name   │
│ category      │  │ customer_id(FK)│  │ segment         │
│ sub_category  │  │ geography_id(FK│  │ signup_date     │
│ unit_cost     │  │ order_line_id  │  └─────────────────┘
│ unit_price    │  │ order_id       │
└───────────────┘  │ quantity_sold  │  ┌─────────────────┐
                   │ unit_price     │  │  Dim_Geography  │
                   │ unit_cost      │  │─────────────────│
                   │ discount_pct   │◄─┤ geography_id(PK)│
                   │ gross_revenue  │  │ region          │
                   │ discount_amount│  │ channel         │
                   │ net_revenue    │  │ city            │
                   │ total_cost     │  └─────────────────┘
                   │ net_profit     │
                   │ margin_pct     │
                   └────────────────┘
```

---

## 2. Relationships

| From Table | Foreign Key | To Table | Primary Key | Cardinality |
|------------|-------------|----------|-------------|-------------|
| Fact_Sales | `date_key` | Dim_Date | `date_key` | Many-to-One |
| Fact_Sales | `product_id` | Dim_Product | `product_id` | Many-to-One |
| Fact_Sales | `customer_id` | Dim_Customer | `customer_id` | Many-to-One |
| Fact_Sales | `geography_id` | Dim_Geography | `geography_id` | Many-to-One |

---

## 3. Design Decisions

### Why Star Schema?
- Simplest model for BI tools like Power BI to auto-detect relationships
- Optimized for aggregation queries (SUM, AVG, COUNT GROUP BY)
- Denormalized dimensions reduce join complexity
- Industry-standard pattern for retail analytics data warehouses

### Pre-computed Metrics in Fact Table
Financial metrics (`gross_revenue`, `net_revenue`, `net_profit`, `margin_pct`) are computed at load time rather than at query time. This decision:
- Dramatically reduces query execution time in Power BI
- Ensures consistent calculation logic across all reports
- Avoids rounding inconsistencies from repeated runtime calculation

### Integer Date Key
The `date_key` uses format `YYYYMMDD` as an integer (e.g., `20240115`). Benefits:
- Faster joins than VARCHAR or DATE comparisons
- Human-readable without conversion
- Sortable natively

### Surrogate Keys
- `order_line_id` uses `SERIAL` (auto-increment) as surrogate PK
- `geography_id` uses integer surrogate (not region name) to support multiple channels per region

---

## 4. Indexing Strategy

Indexes are created on all foreign key columns in `Fact_Sales` and high-cardinality filter columns in dimensions:

```sql
-- Fact table indexes (join & filter performance)
CREATE INDEX idx_fact_date_key       ON "Fact_Sales"(date_key);
CREATE INDEX idx_fact_product_id     ON "Fact_Sales"(product_id);
CREATE INDEX idx_fact_customer_id    ON "Fact_Sales"(customer_id);
CREATE INDEX idx_fact_geography_id   ON "Fact_Sales"(geography_id);
CREATE INDEX idx_fact_order_id       ON "Fact_Sales"(order_id);

-- Dimension indexes (filter & group-by performance)
CREATE INDEX idx_dim_geo_region      ON "Dim_Geography"(region);
CREATE INDEX idx_dim_prod_category   ON "Dim_Product"(category);
CREATE INDEX idx_dim_cust_segment    ON "Dim_Customer"(segment);
```

---

## 5. Data Volume

| Table | Rows | Notes |
|-------|------|-------|
| Fact_Sales | 70,000 | Core transaction data |
| Dim_Date | 1,004 | Jan 2024 – Sep 2026 |
| Dim_Product | 9 | 3 categories, 6 sub-categories |
| Dim_Customer | 1,500 | Synthetic Cameroonian names |
| Dim_Geography | 14 | 10 physical stores + 4 online |

---

## 6. Profit Erosion Logic (Embedded Business Scenario)

A key design feature is the **intentional margin erosion** embedded in the data generation:

```
discount_pct = base_discount + (time_factor × erosion_boost)

Where:
  base_discount  = random(2% – 12%)            ← applies to all products
  time_factor    = (year - 2024) / 2.0          ← 0.0 in 2024, 1.0 in 2026
  erosion_boost  = time_factor × random(15%–35%) ← only for Furniture & Technology

Max discount cap: 55%
Affected products: PRD-101, PRD-102, PRD-201, PRD-202
```

This creates a realistic, analyzable business problem visible in dashboard trends.

---

## 7. Power BI Connection

To connect Power BI to this schema:

1. Open Power BI Desktop
2. Get Data → PostgreSQL Database
3. Server: `localhost`, Database: `northpeak_db`
4. Import tables: `Fact_Sales`, `Dim_Date`, `Dim_Product`, `Dim_Customer`, `Dim_Geography`
5. Verify relationships auto-detected (or define manually using foreign keys above)
6. Set `date_key` as integer, `full_date` as Date type
