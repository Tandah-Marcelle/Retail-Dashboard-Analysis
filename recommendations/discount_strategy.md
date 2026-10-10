# Discount Strategy Recommendations
## NorthPeak Retail — Pricing Discipline & Promotional Policy Reform

**Prepared by:** TANDAH DJIMELI MARCELLE  
**Date:** October 2026  
**Priority:** CRITICAL — Immediate Action Required

---

## 1. The Discount Problem — Quantified

Before recommending what to change, it is important to be precise about what the data actually reveals.

### The Discount Rate Distribution

```
Discount Band     | % of Orders | Avg Margin | Profit Contribution
< 10%             |    ~62%     |    ~48%    |     Healthy ✅
10% – 15%         |    ~19%     |    ~38%    |     Acceptable ⚠️
15% – 20%         |    ~10%     |    ~24%    |     Danger Zone 🟡
> 20%             |    ~9%      |    ~12%    |     Destructive 🔴
> 30%             |    subset   |    ~5%     |     Near breakeven 🔴
```

**13,377 orders (19.11%)** were placed above 20% discount. These orders:
- Generated volume but not proportional profit
- Compressed company-wide margins by an estimated 2–3 percentage points
- Were applied uniformly across order sizes — not correlated with bulk buying (r = 0.00)

### What the Correlation Tells Us

The single most impactful finding in the entire dataset:

> **discount_pct ↔ margin_pct: r = -0.87**

This is not a weak signal. A correlation of -0.87 means discount rate alone explains approximately **76% of the variance in profit margin**. There is no ambiguity here. Discounting is the root cause of NorthPeak's margin decline.

---

## 2. Recommended Discount Policy Framework

### 2.1 Implement a Hard Discount Ceiling by Category

| Category | Current Avg Discount | Recommended Max | Rationale |
|----------|---------------------|-----------------|-----------|
| Technology | ~14% | **15%** | High unit price absorbs small discounts; anything above destroys margin |
| Furniture | ~13% | **15%** | Tables and Chairs have high COGS — margin window is thin |
| Office Supplies | ~8% | **12%** | Already lean; discounts rarely justified given stable demand |

**Implementation:** Enforce ceiling at the point-of-sale or order management system. Any request above the ceiling requires Finance sign-off within 24 hours.

---

### 2.2 Introduce a Three-Tier Discount Authorization Model

Currently, no tiered authorization appears to exist — deep discounts were applied across all order sizes and all channels. Replace this with:

```
TIER 1 — Standard Discount (0% – 10%)
  Authorized by: Sales Representative
  Applies to: All products, all channels
  No approval needed

TIER 2 — Promotional Discount (10.01% – 15%)
  Authorized by: Regional Sales Manager
  Applies to: Seasonal promotions, loyalty customers
  Requires: Customer segment justification logged in system

TIER 3 — Exception Discount (15.01% – 20%)
  Authorized by: Finance Officer + Sales Director (joint)
  Applies to: Clearance, bulk corporate contracts only
  Requires: Written business case, expected volume guarantee

TIER 4 — BLOCKED (>20%)
  No authorization pathway
  Exception only for inventory liquidation with CFO approval
```

---

### 2.3 Decouple Discounts from Order Quantity

The data shows **zero correlation (r = 0.00)** between quantity sold and discount applied. This means discounts are not functioning as volume incentives — they are being applied randomly or as sales shortcuts.

**Recommendation:** Introduce a formal **volume discount ladder** that replaces ad-hoc discounting:

| Units per Order | Max Discount | Rationale |
|----------------|-------------|-----------|
| 1 – 3 | 5% | Standard pricing |
| 4 – 6 | 8% | Small volume reward |
| 7 – 9 | 10% | Medium volume reward |
| 10 – 11 | 12% | Max volume reward |

This creates a rational link between discounts and buying behavior — which currently does not exist.

---

### 2.4 Classify and Manage "Deep Promo" Events Separately

The KDE margin distribution revealed two distinct populations in the data:
- **Standard Sale (≤15%):** Margin peaks around 50–57% — healthy and predictable
- **Deep Promo (>15%):** Margin peaks around 32–33% — significantly compressed

These are two different business modes. They should be tracked, reported, and governed separately.

**Recommendation:**
- Tag every transaction above 15% as a "Promotional Event" in the system
- Track Deep Promo as a separate KPI on the dashboard
- Set a quarterly limit: Deep Promo orders should not exceed **8% of total orders** (down from 19.11%)

---

## 3. The 15% Threshold — Why It Matters

The data shows a specific inflection point at 15% discount:

```
At 10% discount:  Avg margin ≈ 48%   → Profitable
At 15% discount:  Avg margin ≈ 35%   → Acceptable
At 20% discount:  Avg margin ≈ 22%   → Marginal
At 30% discount:  Avg margin ≈ 12%   → Near-breakeven
At 40%+ discount: Avg margin ≈  5%   → Destroying value
```

The 15% line is where returns stop justifying the pricing concession. This is NorthPeak's **discount breakeven boundary** and should be treated as a policy line, not a guideline.

---

## 4. Expected Impact of Implementing This Policy

If discount authorization tiers are implemented and the 15% cap is enforced on 80% of transactions:

| Metric | Current | Projected (12 months) |
|--------|---------|----------------------|
| Avg Discount Rate | 12.04% | ~8–9% |
| Orders above 20% discount | 19.11% | < 5% |
| Avg Profit Margin % | 40.62% | ~44–46% |
| Annual net profit recovery | — | +1.5 to +2.5 billion FCFA |

---

## 5. Implementation Timeline

| Action | Owner | Timeline | Priority |
|--------|-------|----------|----------|
| Define discount ceiling policy document | Sales Director + Finance | Week 1–2 | Critical |
| Configure POS/order system discount limits | IT / Operations | Week 2–4 | Critical |
| Train all sales reps on new tiers | Sales Manager | Week 3–5 | High |
| Launch volume discount ladder | Marketing + Sales | Week 4–6 | High |
| Begin monthly discount audit reporting | Data Analyst | Week 6+ | High |
| Review and adjust ceilings at 6-month mark | Finance | Month 6 | Medium |

---

## 6. What Not to Do

❌ **Don't eliminate discounts entirely.** Discounts under 10% are healthy and contribute to customer retention without meaningfully compressing margin.

❌ **Don't apply the same cap to all categories.** Office Supplies can tolerate slightly less discounting than Technology without losing sales — a blanket policy would be too blunt.

❌ **Don't wait for annual review.** The margin decline accelerated sharply in Q1 2026. Every quarter of inaction deepens the erosion. This is a Q4 2026 action item.
