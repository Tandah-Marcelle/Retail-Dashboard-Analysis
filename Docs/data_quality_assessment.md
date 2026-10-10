# Data Quality Assessment
## Northpeak Retail Analytics

**Version:** 1.0  
**Date:** October 2026  
**Assessment Type:** Synthetic Data Validation

---

## 1. Overview

This document assesses the quality, integrity, and reliability of the data used in the Northpeak Retail Analytics project. Since the dataset is synthetically generated, quality is evaluated against the generation logic, constraints, and business rules defined in the data pipeline.

---

## 2. Data Quality Dimensions

Quality is evaluated across six standard dimensions:

| Dimension | Definition |
|-----------|------------|
| **Completeness** | Are all required fields populated? No nulls in mandatory fields? |
| **Validity** | Do values conform to defined formats, ranges, and types? |
| **Consistency** | Are relationships between tables logically consistent? |
| **Accuracy** | Do computed fields reflect correct calculations? |
| **Uniqueness** | Are primary keys truly unique? |
| **Integrity** | Are all foreign key relationships satisfied? |

---

## 3. Completeness Assessment

### Fact_Sales
| Column | Null Policy | Status | Notes |
|--------|-------------|--------|-------|
| order_line_id | NOT NULL | ✅ PASS | Auto-generated SERIAL |
| order_id | NOT NULL | ✅ PASS | Generated as `ORD-XXXXXXX` |
| date_key | NOT NULL | ✅ PASS | Randomly sampled from valid date range |
| product_id | NOT NULL | ✅ PASS | Sampled from Dim_Product.product_id |
| customer_id | NOT NULL | ✅ PASS | Sampled from Dim_Customer.customer_id |
| geography_id | NOT NULL | ✅ PASS | Sampled from Dim_Geography.geography_id |
| All financial columns | NOT NULL | ✅ PASS | Computed from non-null inputs |

### Dimension Tables
| Table | Null Policy | Status |
|-------|-------------|--------|
| Dim_Date | All columns NOT NULL | ✅ PASS |
| Dim_Product | All columns NOT NULL | ✅ PASS |
| Dim_Customer | All columns NOT NULL | ✅ PASS |
| Dim_Geography | All columns NOT NULL | ✅ PASS |

---

## 4. Validity Assessment

### Value Range Checks

| Field | Expected Range | Validation Rule | Status |
|-------|----------------|-----------------|--------|
| `quantity_sold` | 1 – 11 | `np.random.randint(1, 12)` | ✅ PASS |
| `discount_pct` | 0.00 – 0.55 | `np.clip(discount, 0.0, 0.55)` | ✅ PASS |
| `margin_pct` | Can be negative (deep discount) | `net_profit / net_revenue` | ✅ PASS |
| `year` (Dim_Date) | 2024, 2025, 2026 | Date range constraint | ✅ PASS |
| `quarter` | 1 – 4 | Derived from date | ✅ PASS |
| `month` | 1 – 12 | Derived from date | ✅ PASS |

### Format Checks

| Field | Expected Format | Example | Status |
|-------|-----------------|---------|--------|
| `order_id` | `ORD-XXXXXXX` (7 digits) | `ORD-0000001` | ✅ PASS |
| `product_id` | `PRD-XXX` | `PRD-101` | ✅ PASS |
| `customer_id` | `CUST-XXXX` | `CUST-0001` | ✅ PASS |
| `date_key` | Integer YYYYMMDD | `20240115` | ✅ PASS |

---

## 5. Consistency Assessment

### Financial Calculation Consistency

| Check | Formula Verified | Status |
|-------|------------------|--------|
| Gross Revenue = qty × unit_price | `b_qty * b_unit_prices` | ✅ PASS |
| Discount Amount = gross × discount_pct | `gross_rev * discount_pct` | ✅ PASS |
| Net Revenue = gross - discount | `gross_rev - disc_amt` | ✅ PASS |
| Total Cost = qty × unit_cost | `b_qty * b_unit_costs` | ✅ PASS |
| Net Profit = net_revenue - total_cost | `net_rev - total_cost` | ✅ PASS |
| Margin % = net_profit / net_revenue | `net_profit / net_rev` (where net_rev > 0) | ✅ PASS |

### Edge Case: Zero Net Revenue
When `net_revenue = 0`, `margin_pct` is set to `0.0` (not divided by zero):
```python
margin_pct = np.where(net_rev > 0, (net_profit / net_rev), 0.0)
```
Status: ✅ Handled

---

## 6. Uniqueness Assessment

| Table | Primary Key | Uniqueness Check | Status |
|-------|-------------|------------------|--------|
| Fact_Sales | `order_line_id` (SERIAL) | Auto-increment guarantees uniqueness | ✅ PASS |
| Dim_Date | `date_key` | One row per calendar day | ✅ PASS |
| Dim_Product | `product_id` | 9 distinct products defined | ✅ PASS |
| Dim_Customer | `customer_id` | CUST-0001 to CUST-1500 (no duplicates) | ✅ PASS |
| Dim_Geography | `geography_id` | 14 entries, manually defined | ✅ PASS |

---

## 7. Referential Integrity Assessment

All foreign keys in `Fact_Sales` reference valid primary keys in their respective dimension tables.

| FK Column | References | Integrity Method | Status |
|-----------|------------|------------------|--------|
| `date_key` | `Dim_Date.date_key` | Sampled from `dim_date['date_key'].values` | ✅ PASS |
| `product_id` | `Dim_Product.product_id` | Sampled from `dim_product['product_id'].values` | ✅ PASS |
| `customer_id` | `Dim_Customer.customer_id` | Sampled from `dim_customer['customer_id'].values` | ✅ PASS |
| `geography_id` | `Dim_Geography.geography_id` | Sampled from `dim_geo['geography_id'].values` | ✅ PASS |

PostgreSQL `REFERENCES` constraints are also enforced at the database level.

---

## 8. Known Limitations

| Limitation | Description | Impact |
|------------|-------------|--------|
| Synthetic data | No real business transactions; data is generated | Low — purpose is analytics demonstration |
| Uniform randomness | Customer-product affinity not modeled | Segment behavior patterns may seem uniform |
| No returns/refunds | Dataset has no negative quantity records | Simplification for analytics clarity |
| No seasonal trends | Base randomness does not spike at holidays | Discount erosion is the primary trend signal |
| 4 online regions only | Online channel covers only Littoral, Centre, South-West, North-West | May underrepresent online potential in other regions |
| Fixed product catalog | Only 9 products across 3 categories | Real retailers have hundreds of SKUs |

---

## 9. Reproducibility

The data generation script uses a fixed random seed:
```python
np.random.seed(42)
```
This ensures that every execution of the script produces **identical data**, which is critical for:
- Reproducible analysis results
- Consistent dashboard outputs
- Version control of the dataset (schema + seed = deterministic output)

---

## 10. Recommended Validation Queries

Run these SQL queries after loading data to validate quality:

```sql
-- Check total row count
SELECT COUNT(*) FROM "Fact_Sales";  -- Expected: 70,000

-- Check for null financial values
SELECT COUNT(*) FROM "Fact_Sales"
WHERE net_revenue IS NULL OR net_profit IS NULL OR margin_pct IS NULL;  -- Expected: 0

-- Check discount range
SELECT MIN(discount_pct), MAX(discount_pct) FROM "Fact_Sales";
-- Expected: >= 0.0, <= 0.55

-- Check referential integrity
SELECT COUNT(*) FROM "Fact_Sales" f
LEFT JOIN "Dim_Date" d ON f.date_key = d.date_key
WHERE d.date_key IS NULL;  -- Expected: 0

-- Check margin erosion trend (key business insight)
SELECT d.year, p.category,
       ROUND(AVG(f.margin_pct) * 100, 2) AS avg_margin_pct
FROM "Fact_Sales" f
JOIN "Dim_Date" d ON f.date_key = d.date_key
JOIN "Dim_Product" p ON f.product_id = p.product_id
GROUP BY d.year, p.category
ORDER BY p.category, d.year;
```
