# U.S. Labor Share of GDI: A Methodological Note

## Executive Summary

**The "declining labor share" narrative is highly measurement-sensitive.** Different measurement approaches yield dramatically different conclusions about whether labor's share of national income has declined since the 1970 peak.

### Key Findings (1970-2024)

| Measure | 1970 | 2024 | Change |
|---------|------|------|--------|
| **Gross Labor Share** (Compensation/GDI) | 58.4% | 51.9% | **−6.5 pp** |
| **Wages + Benefits** (excl. employer FICA) | 56.1% | 48.9% | **−7.2 pp** |
| **Wages Only** (excl. all supplements) | 51.6% | 42.7% | **−8.9 pp** |
| **Net Labor Share** (Compensation/NDI) | 67.0% | 62.2% | **−4.8 pp** |
| Depreciation Share | 12.8% | 16.5% | +3.7 pp |
| Employer FICA Share | 2.3% | 3.0% | +0.7 pp |

**Historical context:** In 1929, the gross labor share was 49.5% — *below* the current 2024 level. The 1970 peak (58.4%) was historically high, not the "normal" level.

---

## Charts

### Chart 1: Gross Labor Share (1970-2024)

![U.S. Gross Labor Share](labor_share_gross.png)

This chart shows multiple measurement approaches for the period since the 1970 peak:
- **Blue**: BEA Total Compensation / GDI (standard gross measure)
- **Teal**: Wages + Benefits only (excluding employer FICA—"pre-payroll-tax")
- **Green**: Penn World Table labor share (different methodology for self-employment)
- **Purple**: Adjusted measure including ⅔ of proprietors' income
- **Amber**: Wages only (excluding all supplements)

### Chart 2: Gross vs Net Labor Share (Depreciation Effect)

![Gross vs Net Labor Share](labor_share_net_vs_gross.png)

This chart isolates the effect of rising depreciation:
- **Blue**: Gross labor share (Compensation / GDI)
- **Red**: Net labor share (Compensation / NDI, where NDI = GDI − Depreciation)
- **Gray shaded area**: Depreciation's share of GDI (secondary axis)

**Key insight:** The net measure shows a smaller decline (−4.8 pp) than the gross measure (−6.5 pp). This difference (~26% smaller decline) reflects how rising depreciation affects the choice of denominator: as depreciation rose from 12.8% to 16.5% of GDI, the net denominator (NDI) shrank, mechanically pushing up the net labor share relative to gross.

---

## Methodological Notes

### Why GDI, Not GDP?

When measuring labor's share of national income, we use **GDI** (Gross Domestic Income), not GDP. Here's why:

1. **Labor share data comes from the income side.** The BEA series we use — compensation, profits, depreciation — are all components of GDI.

2. **Using GDP introduces noise.** GDP and GDI differ by a "statistical discrepancy" (typically ~1% of GDP). Dividing income-side numerators by GDP mixes measurement error into the ratio.

3. **GDI is internally consistent.** Both numerator (compensation) and denominator (GDI) come from the same accounting framework.

### What "Compensation" Includes (Pre-Tax Considerations)

The BEA "Compensation of Employees" series (A4002E1A156NBEA) includes:

| Component | 2024 Share | Description |
|-----------|------------|-------------|
| **Wages and Salaries** | 42.7% | Cash payments to workers (pre-income tax) |
| **Supplements** | 9.2% | Benefits + employer social insurance contributions |
| └ Employer pension/insurance | ~6.2% | Health insurance, 401(k) contributions |
| └ Employer social insurance (FICA) | ~3.0% | Employer portion of Social Security + Medicare |

**Tax treatment in labor share measures:**

| Tax Type | Treatment in Compensation | Notes |
|----------|---------------------------|-------|
| **Personal income tax** | Pre-tax | Workers pay this out of wages received |
| **Employee FICA** (~7.65%) | Pre-tax | Workers pay this out of wages received |
| **Employer FICA** (~7.65%) | Included in supplements | Standard practice (total labor cost) |

**Why include employer FICA?** This is standard in the literature ([Karabarbounis & Neiman 2014](https://www.nber.org/papers/w19136), [Autor et al. 2020](https://www.nber.org/papers/w23396)) because:
1. It represents the **total cost of employing labor**
2. It funds benefits workers receive (Social Security, Medicare)
3. Excluding it would understate the true labor share

**Alternative measures for different questions:**

| If you want... | Use this measure | 1970→2024 |
|----------------|------------------|-----------|
| Total labor cost to firms | Total Compensation | −6.5 pp |
| Labor share ex-payroll taxes | Wages + Benefits (excl. FICA) | −7.2 pp |
| Cash wages only | Wages Only | −8.9 pp |

The **"Wages + Benefits (excl. FICA)"** line (teal in Chart 1) excludes employer payroll taxes while keeping private benefits. This shows that excluding payroll taxes, the labor share decline is *steeper* (−7.2 pp), not smaller—because employer FICA rose from 2.3% to 3.0% of GDI.

### Gross vs Net Labor Share: The Depreciation Question

**Gross Labor Share** = Compensation / GDI

**Net Labor Share** = Compensation / (GDI − Depreciation)

The net measure matters because depreciation (Consumption of Fixed Capital) is **not income available for consumption** — it represents the resources needed to replace worn-out capital. Following [Bridgman (2018)](https://www.researchgate.net/publication/318349851_IS_LABOR'S_LOSS_CAPITAL'S_GAIN_GROSS_VERSUS_NET_LABOR_SHARES) and [Rognlie (2015)](https://www.brookings.edu/wp-content/uploads/2016/07/2015a_rognlie.pdf), net labor share is more relevant for understanding the distribution of *sustainable* income.

**Why depreciation rose:**
- Shift from long-lived assets (buildings: 2-3%/year depreciation) to short-lived assets (software: 25-33%/year)
- Rise of intellectual property products (R&D, software, entertainment originals)
- More capital-intensive economy overall

### Capital Share Methodology: Avoiding Double-Counting

A concern raised: *How do we ensure interest income and rent aren't double-counted when calculating capital's share?*

**The BEA national accounts handle this correctly.** Here's how:

#### How GDI Components Are Defined

| Component | What It Measures | Interest/Rent Treatment |
|-----------|------------------|-------------------------|
| **Corporate Profits** | Net earnings *after* deducting interest paid, rent paid, wages, depreciation | Interest & rent already subtracted |
| **Net Interest** | Interest received minus interest paid (economy-wide) | Captures financial sector's net income |
| **Rental Income** | Income from property ownership | Captures landlords' income |
| **Compensation** | Wages + supplements paid to employees | — |
| **Proprietors' Income** | Mixed labor/capital income of self-employed | — |
| **Depreciation (CFC)** | Accounting allowance for capital wearing out | Not "income" to anyone |

#### Why There's No Double-Counting

Consider a manufacturing firm that:
- Earns $100M revenue
- Pays $50M in wages
- Pays $5M in interest to banks
- Pays $3M in rent to landlords
- Has $10M in depreciation
- Has $32M in profits

In the national accounts:
- **Compensation**: +$50M (goes to labor share)
- **Corporate Profits**: +$32M (interest and rent already deducted)
- **Net Interest**: +$5M (this is the bank's income, correctly attributed to financial sector)
- **Rental Income**: +$3M (this is the landlord's income)
- **Depreciation**: +$10M

Total = $100M = GDI ✓

**The key insight:** Corporate profits are reported *net of* interest and rent expenses. So when we add Net Interest and Rental Income as separate capital income components, we're correctly attributing income to the entities that receive it (banks, landlords), not double-counting.

**Why GDI components sum to 100%:** The BEA separates depreciation as its own GDI component rather than embedding it in profits or other categories. This is why: Compensation + Profits + Proprietors' Income + Rental Income + Net Interest + Depreciation + Taxes on Production = GDI (100%). Each component is mutually exclusive.

#### Capital Share Calculation

If you want to calculate capital's share:

```
Capital Share = (Corporate Profits + Net Interest + Rental Income + some portion of Proprietors' Income) / GDI
```

Or equivalently:
```
Capital Share = (GDI - Compensation - Depreciation - Taxes on Production - labor portion of Proprietors') / GDI
```

For **net** capital share (excluding depreciation from both sides):
```
Net Capital Share = (NDI - Compensation - Taxes - labor portion of Proprietors') / NDI
```

---

## Sector Scope: Whole Economy vs Business Sector

This analysis uses **whole-economy GDI shares**, which include:
- Government sector (employees paid by government)
- Housing sector (imputed rent from owner-occupied housing)
- All industries and legal forms

**Why this matters:**
- **Government tends to raise measured labor share** — government has little measured operating surplus
- **Owner-occupied housing can lower labor share** — adds imputed rental income with no compensation

The **nonfarm business sector** shows a clearer decline. The [BLS nonfarm business labor share index](https://fred.stlouisfed.org/series/PRS85006173) is down ~16% from its early-1970s high (index: ~115 in 1970 vs 96.9 in 2024Q4).

---

## Key Findings Explained

### 1. Gross labor share declined ~6.5 pp from 1970 peak

Labor share peaked at 58.4% in 1970 and fell to 51.9% by 2024. This timing coincides with declining unionization, globalization, and automation — though causal attribution requires careful analysis.

### 2. Net labor share declined less (~4.8 pp)

When adjusting for rising depreciation, the decline is attenuated. Net labor share went from 67.0% (1970) to 62.2% (2024) — a decline of 4.8 pp compared to 6.5 pp for gross. The net decline is ~26% smaller than the gross decline.

### 3. Decomposing the labor share decline

The three-way decomposition reveals where the "missing" labor share went:

| Measure | 1970 | 2024 | Change |
|---------|------|------|--------|
| Total Compensation | 58.4% | 51.9% | −6.5 pp |
| Wages + Benefits (ex-FICA) | 56.1% | 48.9% | −7.2 pp |
| Wages Only | 51.6% | 42.7% | −8.9 pp |

**Key insight:** The rise in supplements (+2.4 pp) consists of:
- **Private benefits** (pension, health insurance): ~+1.7 pp
- **Employer FICA** (Social Security, Medicare): ~+0.7 pp

If you view employer FICA as a "tax on labor" rather than compensation *to* labor, the true labor share decline is steeper (−7.2 pp).

**Caveat:** Rising private benefits doesn't necessarily mean workers are better off — much of it reflects healthcare cost inflation, not improved coverage.

### 4. Historical context: 1929 was lower

The 1929 gross labor share was 49.5% — below the current 2024 level (51.9%). The 1970 peak was historically high, driven partly by:
- Strong unions
- Tight labor markets
- Less international competition
- Lower capital intensity

Starting from 1970 (the peak) rather than 1929 (pre-modern economy) changes the narrative entirely.

---

## Data Tables

### BEA GDI Component Shares (1970 vs 2024)

| Component | 1970 | 2024 | Δ |
|-----------|------|------|---|
| **Compensation of Employees** | **58.4%** | **51.9%** | **−6.5 pp** |
| └ Wages & Salaries | 51.6% | 42.7% | −8.9 pp |
| └ Wages + Benefits (excl. employer FICA)† | 56.1% | 48.9% | −7.2 pp |
| └ Supplements (total) | 6.8% | 9.2% | +2.4 pp |
|   └ Employer pension/insurance | ~4.5% | ~6.2% | ~+1.7 pp |
|   └ Employer FICA (Social Security, Medicare) | ~2.3% | ~3.0% | ~+0.7 pp |
| Proprietors' Income | 7.3% | 7.0% | −0.3 pp |
| Corporate Profits (with IVA+CCAdj)‡ | 7.4% | 11.5% | +4.1 pp |
| Rental Income | ~2% | 3.7% | ~+2 pp |
| Net Interest | ~4% | 2.1% | ~−2 pp |
| **Depreciation (CFC)** | **12.8%** | **16.5%** | **+3.7 pp** |
| Taxes on Production§ | ~7% | 6.7% | ~0 pp |

*Source: BEA NIPA Table 1.11 via FRED. 1970 subcomponent values are approximate.*

**Table notes:**
- † **Wages + Benefits (excl. employer FICA)**: Compensation minus employer FICA. This "pre-payroll-tax" measure shows a steeper decline (−7.2 pp) than total compensation (−6.5 pp).
- ‡ **Corporate Profits**: Reported *net of* interest paid, rent paid, and depreciation, but *before* corporate income taxes. Corporate income taxes are paid out of this figure.
- § **Taxes on Production**: Includes sales taxes, property taxes, customs duties, etc. These are distinct from corporate income taxes (which come out of profits) and personal income taxes (which workers pay out of compensation).

### Historical Reference: 1929

| Measure | 1929 | 2024 | Note |
|---------|------|------|------|
| Gross Labor Share | 49.5% | 51.9% | 2024 is *higher* |
| Net Labor Share | 55.0% | 62.2% | 2024 is *much higher* |
| Depreciation | 10.0% | 16.5% | Rose substantially |
| Proprietors' Income | 13.5% | 7.0% | Collapsed (structural shift) |

---

## Which Measure Should You Use?

| Your Question | Recommended Measure | Why |
|---------------|---------------------|-----|
| **Are corporations squeezing workers?** | Gross (corporate sector) | Shows actual firm-level revenue split |
| **What income is sustainable?** | Net (depreciation-adjusted) | Depreciation isn't available for consumption |
| **How do wages compare to total labor costs?** | Wages vs Total Compensation | Reveals role of benefits/payroll taxes |
| **International comparisons** | Penn World Table | Standardized methodology |
| **Short-run dynamics** | BLS Nonfarm Business | Quarterly frequency |

---

## Literature

### Key Papers

| Paper | Key Argument |
|-------|--------------|
| [**Bridgman (2018)**](https://www.researchgate.net/publication/318349851_IS_LABOR'S_LOSS_CAPITAL'S_GAIN_GROSS_VERSUS_NET_LABOR_SHARES) | Net labor share is more relevant; shows less decline than gross |
| [**Rognlie (2015)**](https://www.brookings.edu/wp-content/uploads/2016/07/2015a_rognlie.pdf) | Most of capital share increase is housing; net capital share stable |
| [**Karabarbounis & Neiman (2014)**](https://www.nber.org/papers/w19136) | Global labor share declined; driven by falling investment prices |
| [**Autor et al. (2020)**](https://www.nber.org/papers/w23396) | "Superstar firms" with low labor shares capture market share |
| [**Koh et al. (2020)**](https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA17477) | IPP capitalization explains entire decline |

---

## Data Sources

| Source | Series ID | Description |
|--------|-----------|-------------|
| BEA NIPA | A4002E1A156NBEA | Compensation share of GDI |
| BEA NIPA | W270RE1A156NBEA | Wages & salaries share of GDI |
| BEA NIPA | A262RE1A156NBEA | Depreciation share of GDI |
| BEA NIPA | A041RE1A156NBEA | Proprietors' income share of GDI |
| Penn World Table | LABSHPUSA156NRUG | Labor share (different methodology) |
| BLS | PRS85006173 | Nonfarm business labor share index |

All data accessed via [FRED](https://fred.stlouisfed.org/) (Federal Reserve Economic Data).

---

## Replication

### Running the Code

```bash
python3 generate_chart.py
```

This produces:
- `labor_share_gross.png/pdf` — Main chart with multiple measures
- `labor_share_net_vs_gross.png/pdf` — Depreciation effect chart
- `labor_share_comparison.png/pdf` — Combined overview

### Calculations

**Net Labor Share:**
```
NDI = GDI × (1 - Depreciation_Share)
Net_Labor_Share = Compensation_Share / (1 - Depreciation_Share)

Example (2024):
NDI = 100% × (1 - 0.165) = 83.5%
Net_Labor_Share = 51.9% / 83.5% = 62.2%
```

**Adjusted Labor Share (with proprietors' income):**
```
Adjusted = Compensation_Share + (α × Proprietors_Share)
where α = 0.67 (following Gollin 2002)

Example (2024):
Adjusted = 51.9% + (0.67 × 7.0%) = 56.6%
```

---

## License

This research note is shared for educational and research purposes. Data sources are public domain (BEA, BLS) or citation-requested (Penn World Table).

---

## Author

Research note compiled by [Claude Code](https://claude.ai/code) under the direction of **Ilan Strauss**.

January 2026

---

## Changelog

- **v2.1** (January 2026): Added "Wages + Benefits (excl. FICA)" measure; clarified tax treatment (corporate profits are pre-corporate income tax); added explicit note that GDI components sum to 100%; expanded supplements decomposition in data tables
- **v2.0** (January 2026): Refocused on 1970-2024 period; added separate gross/net charts; improved axis readability (5-year intervals); added wages-only measure; expanded methodology notes on pre-tax treatment and capital share calculation
- **v1.1** (January 2026): Added section on IT, software, and superstar firms
- **v1.0** (January 2026): Initial research note
