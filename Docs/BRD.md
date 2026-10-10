# Business Requirements Document (BRD)
## Northpeak Retail Dashboard Analysis

**Version:** 1.0  
**Date:** October 2026  
**Project:** Northpeak Retail Analytics Platform  

---

## 1. Executive Summary

Northpeak is a Cameroonian retail company operating across all 10 regions of the country through both physical stores and online channels. The business has observed declining profit margins over the 2024–2026 period, particularly in the Furniture and Technology product categories. This project delivers an end-to-end analytics solution to diagnose the root causes, track KPIs over time, and support data-driven decision-making by leadership.

---

## 2. Business Problem

The business has identified the following challenges:

- **Profit margin erosion** across key product categories (Furniture, Technology) from 2024 to 2026
- **No centralized visibility** into sales performance across all 10 Cameroonian regions
- **Inability to compare** physical store vs. online channel performance effectively
- **Lack of customer segmentation insights** — no clear understanding of which customer segments (Consumer, Corporate, Home Office) are most profitable
- **Reactive decision-making** due to absence of real-time or near-real-time dashboards

---

## 3. Business Objectives

| # | Objective |
|---|-----------|
| 1 | Track total revenue, net profit, and margin % over time (2024–2026) |
| 2 | Identify which product categories and sub-categories are experiencing margin decline |
| 3 | Compare performance by region and sales channel (Physical Store vs. Online) |
| 4 | Analyze customer segment contribution to revenue and profitability |
| 5 | Provide an interactive dashboard for non-technical stakeholders |
| 6 | Establish a reusable, scalable data pipeline for future updates |

---

## 4. Scope

### In Scope
- Synthetic data generation simulating 70,000 sales transactions (Jan 2024 – Sep 2026)
- PostgreSQL star schema database design and implementation
- Python-based data generation and loading pipeline
- Exploratory data analysis and visualization in Jupyter Notebook
- Power BI interactive dashboard with filters, KPIs, and trend charts

### Out of Scope
- Real-time data ingestion from live POS or e-commerce systems
- Customer-level PII management or GDPR compliance workflows
- Forecasting or predictive machine learning models (future phase)
- Mobile application development

---

## 5. Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| CEO / Executive Leadership | Primary decision-maker | High-level KPIs, profitability trends |
| Sales Manager | Operational owner | Regional and channel performance |
| Finance Team | Budget and cost control | Margin analysis, discount impact |
| Marketing Team | Customer strategy | Segment insights, product performance |
| Data Analyst / Developer | Project builder | Technical implementation |

---

## 6. Functional Requirements

### 6.1 Data Generation
- Generate a minimum of 70,000 synthetic sales transactions
- Cover all 9 products across 3 categories (Furniture, Technology, Office Supplies)
- Cover all 10 regions of Cameroon with 14 geography entries (10 physical, 4 online)
- Generate 1,500 unique customers across 3 segments

### 6.2 Data Storage
- Store all data in a PostgreSQL relational database
- Implement a star schema with 1 fact table and 4 dimension tables
- Add performance indexes on all foreign key columns

### 6.3 Profit Erosion Simulation
- Simulate increasing discount rates over time (2024 → 2026)
- Apply higher erosion specifically to Furniture and Technology categories
- Cap maximum discount at 55%

### 6.4 Analytics & Visualization
- Produce Python visualizations (matplotlib/seaborn) showing key trends
- Build an interactive Power BI dashboard covering all business objectives

### 6.5 Dashboard Filters (Power BI)
- Filter by Year / Quarter / Month
- Filter by Product Category
- Filter by Region and Channel
- Filter by Customer Segment

---

## 7. Non-Functional Requirements

| Requirement | Detail |
|-------------|--------|
| Performance | Data script must complete full load in under 5 minutes |
| Scalability | Schema must support additional products, regions, or years without redesign |
| Security | All credentials stored in `.env` file, never committed to version control |
| Reproducibility | Seeded random generation (`np.random.seed(42)`) ensures consistent outputs |
| Portability | `requirements.txt` ensures environment can be reproduced on any machine |

---

## 8. Success Criteria

- All 70,000 rows successfully inserted into PostgreSQL without errors
- Dashboard renders all KPIs and visuals without performance issues
- Margin erosion trend is clearly visible in both the notebook and Power BI
- Regional and channel comparisons are accessible via dashboard filters
- Documentation is complete and project is reproducible by a new developer

---

## 9. Timeline

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Database schema design & data generation script | Complete |
| Phase 2 | Data loading into PostgreSQL | Complete |
| Phase 3 | Exploratory analysis & Python visualizations | Complete |
| Phase 4 | Power BI dashboard development | Complete |
| Phase 5 | Documentation & GitHub publication | In Progress |

---

## 10. Assumptions & Constraints

- Data is entirely synthetic and does not represent real Northpeak company operations
- Currency is in Central African CFA Franc (XAF)
- All prices and costs reflect approximate Cameroonian market values
- Analysis period is limited to January 2024 – September 2026
