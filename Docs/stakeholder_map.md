# Stakeholder Map
## Northpeak Retail Analytics

**Version:** 1.0  
**Date:** October 2026

---

## 1. Overview

This document maps all stakeholders involved in or affected by the Northpeak Retail Analytics project. It defines each stakeholder's role, level of influence, interest in the project, and how they interact with the deliverables.

---

## 2. Stakeholder Matrix

The matrix plots stakeholders by **Influence** (ability to affect the project) and **Interest** (how much they care about outcomes).

```
HIGH INFLUENCE
      │
      │   ┌─────────────────┐        ┌─────────────────┐
      │   │  Finance Team   │        │  CEO/Executive  │
      │   │  (Manage)       │        │  Leadership     │
      │   │                 │        │  (Collaborate)  │
      │   └─────────────────┘        └─────────────────┘
      │
      │   ┌─────────────────┐        ┌─────────────────┐
      │   │  IT / DBA       │        │  Sales Manager  │
      │   │  (Monitor)      │        │  (Collaborate)  │
      │   │                 │        │                 │
      │   └─────────────────┘        └─────────────────┘
LOW   │
INFLUENCE  ──────────────────────────────────────────────────
           LOW INTEREST                            HIGH INTEREST
                                   ┌─────────────────┐
                                   │  Marketing Team │
                                   │  (Inform)       │
                                   └─────────────────┘
                              ┌─────────────────┐
                              │  Data Analyst/  │
                              │  Developer      │
                              │  (Lead)         │
                              └─────────────────┘
```

---

## 3. Stakeholder Profiles

### 3.1 CEO / Executive Leadership

| Field | Detail |
|-------|--------|
| Role | Primary decision-maker and project sponsor |
| Interest Level | High |
| Influence Level | High |
| Engagement Strategy | Collaborate — keep informed on outcomes and insights |
| Primary Deliverable | Executive Summary page on Power BI dashboard |
| Key Questions | Is the business profitable? Are margins improving or declining? |
| Preferred Format | High-level KPI cards, trend lines, minimal detail |
| Communication | Monthly dashboard review, high-level summary report |

---

### 3.2 Sales Manager

| Field | Detail |
|-------|--------|
| Role | Operational owner of sales performance |
| Interest Level | High |
| Influence Level | High |
| Engagement Strategy | Collaborate — direct input on KPI definitions and regional breakdowns |
| Primary Deliverable | Regional & Channel Performance dashboard page |
| Key Questions | Which regions are performing best? Is online growing vs physical? |
| Preferred Format | Maps, bar charts, regional comparisons |
| Communication | Weekly dashboard access, monthly review meeting |

---

### 3.3 Finance Team

| Field | Detail |
|-------|--------|
| Role | Budget ownership, cost control, margin analysis |
| Interest Level | High |
| Influence Level | High |
| Engagement Strategy | Manage — critical stakeholder for financial accuracy sign-off |
| Primary Deliverable | Margin analysis, discount impact reports |
| Key Questions | What is the true margin per category? How much revenue is lost to discounts? |
| Preferred Format | Detailed tables, trend charts, variance analysis |
| Communication | Monthly financial review, direct dashboard access |

---

### 3.4 Marketing Team

| Field | Detail |
|-------|--------|
| Role | Customer strategy, campaign planning |
| Interest Level | Medium-High |
| Influence Level | Medium |
| Engagement Strategy | Inform — provide segment insights without requiring their input |
| Primary Deliverable | Customer Segment Analysis dashboard page |
| Key Questions | Which customer segment is most valuable? What products do Corporate customers buy? |
| Preferred Format | Donut charts, segment breakdowns, product-customer cross tabs |
| Communication | Quarterly segment report |

---

### 3.5 Data Analyst / Developer

| Field | Detail |
|-------|--------|
| Role | Project builder and technical owner |
| Interest Level | High |
| Influence Level | Medium |
| Engagement Strategy | Lead — responsible for all technical deliverables |
| Primary Deliverables | All: data pipeline, notebook, Power BI dashboard, documentation |
| Key Questions | Is the data pipeline reliable? Are KPIs calculated correctly? |
| Preferred Format | Technical documentation, SQL, Python code |
| Communication | Continuous — self-directed development |

---

### 3.6 IT / Database Administrator (DBA)

| Field | Detail |
|-------|--------|
| Role | Manages PostgreSQL infrastructure and access |
| Interest Level | Low-Medium |
| Influence Level | High |
| Engagement Strategy | Monitor — keep informed of database requirements and access needs |
| Primary Deliverable | Database schema documentation, credentials setup |
| Key Questions | Does the schema follow naming conventions? Are indexes appropriate? |
| Preferred Format | ERD, DDL scripts, index documentation |
| Communication | As needed — during setup and for access provisioning |

---

## 4. RACI Matrix

RACI: **R**esponsible, **A**ccountable, **C**onsulted, **I**nformed

| Deliverable | CEO | Sales Mgr | Finance | Marketing | Data Analyst | IT/DBA |
|-------------|-----|-----------|---------|-----------|--------------|--------|
| Database schema design | I | C | C | - | R/A | C |
| Data generation script | I | - | - | - | R/A | I |
| Data loading to PostgreSQL | I | - | - | - | R/A | C |
| KPI definition & framework | A | C | C | C | R | - |
| Jupyter Notebook analysis | I | I | I | - | R/A | - |
| Power BI dashboard | A | C | C | C | R | - |
| Documentation | I | - | - | - | R/A | I |
| Project sign-off | A | C | C | - | R | - |

---

## 5. Communication Plan

| Stakeholder | Channel | Frequency | Content |
|-------------|---------|-----------|---------|
| CEO / Executive | Power BI dashboard + summary | Monthly | KPIs, profit trends |
| Sales Manager | Power BI dashboard | Weekly | Regional, channel performance |
| Finance Team | Power BI dashboard + export | Monthly | Margin, discount analysis |
| Marketing Team | Dashboard share + report | Quarterly | Segment insights |
| IT / DBA | Documentation + direct meeting | As needed | Schema, access |
| Data Analyst | GitHub + self-managed | Continuous | All deliverables |

---

## 6. Stakeholder Concerns & Mitigations

| Stakeholder | Concern | Mitigation |
|-------------|---------|------------|
| Finance Team | Calculation accuracy | All formulas documented in data dictionary; SQL validation queries provided |
| CEO | Dashboard too technical | Executive Summary page uses only KPI cards and simple trend lines |
| IT/DBA | Security of credentials | Credentials stored in `.env`, excluded from version control via `.gitignore` |
| Sales Manager | Missing regional data | All 10 Cameroon regions included in Dim_Geography |
| Marketing | Segment data is synthetic | Clearly stated in BRD — for analytical demonstration purposes |
