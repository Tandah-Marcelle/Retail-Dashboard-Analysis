# KPI Framework
## Northpeak Retail Analytics

**Version:** 1.0  
**Date:** October 2026

---

## 1. Overview

This document defines all Key Performance Indicators (KPIs) tracked in the Northpeak Retail Dashboard. Each KPI includes its business definition, formula, data source, and target/benchmark.

KPIs are organized across four perspectives:
- **Financial Performance**
- **Sales & Volume**
- **Customer**
- **Product & Category**

---

## 2. Financial Performance KPIs

### 2.1 Gross Revenue
| Field | Detail |
|-------|--------|
| Definition | Total revenue before any discounts are applied |
| Formula | `SUM(quantity_sold × unit_price)` |
| Source Table | `Fact_Sales.gross_revenue` |
| Unit | XAF (Central African CFA Franc) |
| Dimension Filters | Date, Product, Region, Channel, Segment |
| Business Use | Top-line revenue performance, growth tracking |

---

### 2.2 Net Revenue
| Field | Detail |
|-------|--------|
| Definition | Actual revenue collected after discounts |
| Formula | `SUM(gross_revenue - discount_amount)` |
| Source Table | `Fact_Sales.net_revenue` |
| Unit | XAF |
| Dimension Filters | Date, Product, Region, Channel, Segment |
| Business Use | True revenue performance indicator |

---

### 2.3 Total Cost of Goods Sold (COGS)
| Field | Detail |
|-------|--------|
| Definition | Total cost of all units sold |
| Formula | `SUM(quantity_sold × unit_cost)` |
| Source Table | `Fact_Sales.total_cost` |
| Unit | XAF |
| Dimension Filters | Date, Product, Region |
| Business Use | Procurement efficiency, cost control |

---

### 2.4 Net Profit
| Field | Detail |
|-------|--------|
| Definition | Profit remaining after deducting COGS from net revenue |
| Formula | `SUM(net_revenue - total_cost)` |
| Source Table | `Fact_Sales.net_profit` |
| Unit | XAF |
| Dimension Filters | Date, Product, Region, Channel, Segment |
| Business Use | Core profitability metric |

---

### 2.5 Profit Margin %
| Field | Detail |
|-------|--------|
| Definition | Percentage of net revenue that becomes profit |
| Formula | `AVG(net_profit / net_revenue) × 100` or `SUM(net_profit) / SUM(net_revenue) × 100` |
| Source Table | `Fact_Sales.margin_pct` |
| Unit | Percentage (%) |
| Benchmark | Healthy margin: > 40%; Warning zone: 20–40%; Critical: < 20% |
| Business Use | Primary indicator of business health and pricing effectiveness |

---

### 2.6 Total Discount Amount
| Field | Detail |
|-------|--------|
| Definition | Total monetary value lost to discounts |
| Formula | `SUM(discount_amount)` |
| Source Table | `Fact_Sales.discount_amount` |
| Unit | XAF |
| Business Use | Discount management and pricing policy review |

---

### 2.7 Average Discount Rate
| Field | Detail |
|-------|--------|
| Definition | Average percentage discount applied across transactions |
| Formula | `AVG(discount_pct) × 100` |
| Source Table | `Fact_Sales.discount_pct` |
| Unit | Percentage (%) |
| Benchmark | Acceptable: < 12%; Concern: 12–25%; Critical: > 25% |
| Business Use | Monitors discount creep over time |

---

## 3. Sales & Volume KPIs

### 3.1 Total Transactions
| Field | Detail |
|-------|--------|
| Definition | Total number of order line items |
| Formula | `COUNT(order_line_id)` |
| Source Table | `Fact_Sales` |
| Unit | Count |
| Business Use | Sales activity volume |

---

### 3.2 Total Units Sold
| Field | Detail |
|-------|--------|
| Definition | Total number of product units sold |
| Formula | `SUM(quantity_sold)` |
| Source Table | `Fact_Sales.quantity_sold` |
| Unit | Units |
| Business Use | Demand and inventory planning |

---

### 3.3 Average Order Value (AOV)
| Field | Detail |
|-------|--------|
| Definition | Average net revenue per order line |
| Formula | `SUM(net_revenue) / COUNT(order_line_id)` |
| Source Table | `Fact_Sales` |
| Unit | XAF |
| Business Use | Customer spending behavior |

---

### 3.4 Revenue by Channel
| Field | Detail |
|-------|--------|
| Definition | Net revenue split between Physical Store and Online |
| Formula | `SUM(net_revenue) GROUP BY channel` |
| Source Tables | `Fact_Sales` JOIN `Dim_Geography` |
| Unit | XAF, % share |
| Business Use | Channel strategy and investment decisions |

---

### 3.5 Revenue by Region
| Field | Detail |
|-------|--------|
| Definition | Net revenue by Cameroon administrative region |
| Formula | `SUM(net_revenue) GROUP BY region` |
| Source Tables | `Fact_Sales` JOIN `Dim_Geography` |
| Unit | XAF |
| Business Use | Geographic expansion and regional resource allocation |

---

## 4. Customer KPIs

### 4.1 Revenue by Segment
| Field | Detail |
|-------|--------|
| Definition | Net revenue contribution by customer segment |
| Formula | `SUM(net_revenue) GROUP BY segment` |
| Source Tables | `Fact_Sales` JOIN `Dim_Customer` |
| Unit | XAF, % share |
| Segments | Consumer (55%), Corporate (30%), Home Office (15%) |
| Business Use | Segment targeting and marketing spend allocation |

---

### 4.2 Profit by Segment
| Field | Detail |
|-------|--------|
| Definition | Net profit contribution per customer segment |
| Formula | `SUM(net_profit) GROUP BY segment` |
| Source Tables | `Fact_Sales` JOIN `Dim_Customer` |
| Unit | XAF |
| Business Use | Identifies most profitable customer segments |

---

### 4.3 Active Customers
| Field | Detail |
|-------|--------|
| Definition | Count of distinct customers who made a purchase |
| Formula | `COUNT(DISTINCT customer_id)` |
| Source Table | `Fact_Sales` |
| Unit | Count |
| Business Use | Customer base health |

---

## 5. Product & Category KPIs

### 5.1 Revenue by Category
| Field | Detail |
|-------|--------|
| Definition | Net revenue grouped by product category |
| Formula | `SUM(net_revenue) GROUP BY category` |
| Source Tables | `Fact_Sales` JOIN `Dim_Product` |
| Unit | XAF |
| Business Use | Category management and investment |

---

### 5.2 Margin % by Category
| Field | Detail |
|-------|--------|
| Definition | Profit margin percentage per product category |
| Formula | `SUM(net_profit) / SUM(net_revenue) × 100 GROUP BY category` |
| Source Tables | `Fact_Sales` JOIN `Dim_Product` |
| Unit | Percentage (%) |
| Business Use | Identifies which categories are eroding profitability |
| Key Insight | Technology and Furniture show declining margins 2024→2026 |

---

### 5.3 Margin Trend Over Time
| Field | Detail |
|-------|--------|
| Definition | Monthly or quarterly margin % tracked over time |
| Formula | `AVG(margin_pct) GROUP BY year, quarter/month` |
| Source Tables | `Fact_Sales` JOIN `Dim_Date` |
| Unit | Percentage (%) |
| Business Use | Detects margin erosion patterns and inflection points |

---

## 6. KPI Summary Dashboard Map

| KPI | Visualization Type | Primary Filter |
|-----|--------------------|----------------|
| Net Revenue | KPI Card + Line Chart | Date |
| Net Profit | KPI Card + Line Chart | Date |
| Margin % | KPI Card + Line Chart | Date, Category |
| Discount Rate | KPI Card + Bar Chart | Date, Category |
| Revenue by Region | Map + Bar Chart | Channel |
| Revenue by Category | Donut Chart | Date |
| Revenue by Segment | Donut Chart | Date |
| Margin by Category (trend) | Line Chart | Date |
| Total Transactions | KPI Card | Date, Region |
| Revenue by Channel | Bar/Stacked Chart | Date, Region |
