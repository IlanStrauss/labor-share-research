# Has the U.S. Labour Share Declined? A note (v.2)

## Executive Summary

**Has the U.S. labor share declined? Yes.** Across the standard BEA whole-economy measures in Table 1.11, the labor share is below its late-1960s/1970 peak. The decline is consistent across all measures examined here, though magnitude varies with methodological choices (sector scope, proprietors' income treatment, depreciation inclusion). Different measurement choices yield declines ranging from −4.8 pp to −8.9 pp — a substantial range, but all negative.

### Key Findings (1970-2024)

*All series are annual, BEA whole-economy shares from [Table 1.11 via FRED](https://fred.stlouisfed.org/release/tables?rid=53&eid=42211); latest year shown is 2024.*

| Measure | 1970 | 2024 | Change |
|---------|------|------|--------|
| **Gross Labor Share** (Compensation/GDI) | 58.4% | 51.9% | **−6.5 pp** |
| **Wages + Benefits** (excl. employer social insurance†) | 56.1% | 48.9% | **−7.2 pp** |
| **Wages Only** (excl. all supplements) | 51.6% | 42.7% | **−8.9 pp** |
| **Labor Share of Net Domestic Income** (Compensation/NDI) | 67.0% | 62.2% | **−4.8 pp** |
| Depreciation Share | 12.8% | 16.5% | +3.7 pp |
| Employer Social Insurance† Share | 2.3% | 3.0% | +0.7 pp |

*† Employer contributions for government social insurance ([BEA definition](https://www.bea.gov/help/glossary/contribution-government-social-insurance)). This is dominated by FICA (Social Security + Medicare, 7.65% of wages), but also includes smaller programs like unemployment insurance and workers' compensation.*

**Key takeaways:**
- The **standard gross measure** shows a −6.5 pp decline
- On a **net-income (NDI)** basis — where depreciation is treated as a capital cost subtracted before distribution — the decline is less: −4.8 pp
- Looking at **wages only** (excluding benefits and payroll taxes) shows the steepest decline: −8.9 pp

---

## Defining the Labor Share

The "labor share" is the fraction of national income that accrues to workers as compensation for their labor, as opposed to capital owners (profits, interest, rent). This section defines the key concepts.

### The Basic Definition

The **gross labor share** is defined as:

```
                    Compensation of Employees
Gross Labor Share = ─────────────────────────────
                    Gross Domestic Income (GDI)
```

This is the standard measure used in the literature ([Karabarbounis & Neiman 2014](https://www.nber.org/papers/w19136), [Autor et al. 2020](https://www.nber.org/papers/w23396), [Elsby et al. 2013](https://www.brookings.edu/articles/the-decline-of-the-u-s-labor-share/)).

### What Goes Into the Numerator?

**Compensation of Employees** (BEA series A4002E1A156NBEA) includes:

1. **Wages and Salaries**: Cash payments to workers before personal income taxes
2. **Supplements to Wages and Salaries**:
   - *Employer contributions for employee pension and insurance funds* (~6% of GDI): Health insurance, 401(k) contributions, life insurance
   - *Employer contributions for government social insurance* (~3% of GDI): Dominated by Social Security and Medicare payroll contributions (FICA, ~7.65% of wages), plus other government social insurance programs (unemployment insurance, workers' compensation, etc.)

This is a **pre-personal-income-tax** measure of total labor cost to employers. It does *not* include the employee's portion of FICA or personal income taxes — those are paid out of wages received.

### What Goes Into the Denominator?

**Gross Domestic Income (GDI)** is the sum of all incomes earned in production. At the **Table 1.11 level**, the identity is:

```
GDI = Compensation of Employees
    + Net Operating Surplus (NOS)
    + Taxes on Production and Imports less Subsidies
    + Consumption of Fixed Capital (Depreciation)
```

Where **Net Operating Surplus** is itself composed of:
- Corporate Profits (with IVA and CCAdj)
- Proprietors' Income
- Rental Income of Persons
- Net Interest and Miscellaneous Payments

This structure matters: the four NOS subcomponents are not independent. In particular, "Net Interest" is an offset item (see below), not a standalone income measure.

We use GDI rather than GDP because the labor share numerator (compensation) comes from the income side of the accounts. Using GDP would mix income-side numerators with expenditure-side denominators, introducing measurement noise from the statistical discrepancy.

### The Net Domestic Income (NDI) Measure

A key methodological choice is whether to measure factor shares over **gross** or **net** income. **Depreciation** (Consumption of Fixed Capital, CFC) represents resources that must be set aside to replace worn-out capital — it is not income available for distribution to workers or capital owners.

**The distributional logic (capital-first):**

Depreciation is a **capital maintenance cost**. Moving from **gross** to **net** income subtracts depreciation from the denominator (total domestic income) **before** dividing the income between labor and capital. This automatically raises the labor share (dividing labor income by a smaller number). Therefore:

1. Depreciation **reduces** capital's net income and in turn the net capital income share 
2. Labor's *higher* share of net income is then the residual consequence of the now smaller net-income pie

The accounting identities make this explicit:

```
Gross income identity (Table 1.11):
  GDI = Compensation + Net Operating Surplus + Taxes on Production + Depreciation

Net income identity (distribution-relevant):
  NDI = GDI − Depreciation = Compensation + Net Operating Surplus + Taxes on Production
```

On a net basis, depreciation has already been netted out of capital's claim; labor's higher share is the corollary of measuring the split over net income.

Following [Bridgman (2018)](https://bea.gov/papers/pdf/laborshare1410.pdf) and [Rognlie (2015)](https://www.brookings.edu/wp-content/uploads/2016/07/2015a_rognlie.pdf), we compute labor's share of **Net Domestic Income (NDI)**:

```
                                   Compensation of Employees
Labor Share of Net Income (NDI) = ────────────────────────────────────────
                                   GDI − Depreciation (= NDI)
```

**Terminology note:** In the labor share literature, "net" typically means *net of depreciation*, **not** net of taxes. All measures in this document are pre-income-tax.

Equivalently, if we measure labor's share over net income (NDI), the labor-share ratio rises mechanically because the denominator excludes depreciation. The NDI-basis measure shows a smaller decline than the gross measure because depreciation has risen substantially (from 12.8% to 16.5% of GDI). We are measuring labor's share of *sustainable, consumable income* rather than gross output.

### Alternative Numerator Definitions

We also examine alternative numerator definitions to isolate different components:

| Numerator | What It Measures | Interpretation |
|-----------|------------------|----------------|
| **Total Compensation** | Wages + all supplements | Total cost of employing labor |
| **Wages + Benefits (excl. employer social insurance)** | Wages + employer pension/insurance | Excludes employer payroll taxes |
| **Wages Only** | Cash wages before taxes | Excludes all non-cash compensation |

The choice of numerator matters: wages alone have fallen more steeply than total compensation because rising employer benefits and payroll taxes have partially offset wage stagnation.

---

## Figures

### Figure 1. Labor Share Declined Across All Measures Since 1970 Peak

![U.S. Gross Labor Share](labor_share_gross.png)

Figure 1 shows five different ways of measuring labor's share of national income, all using GDI as the denominator but varying the labor income numerator (the top of the equation). Each line represents a different definition of "labor income."

- **BEA Total Compensation**: Blue line. The standard gross labor share. The numerator is total compensation of employees (wages + supplements). This is the benchmark measure used in most academic literature.

- **Wages + Benefits (excl. employer social insurance)**: Pink line. The numerator excludes employer contributions for government social insurance (~3% of GDI, dominated by FICA) while keeping private benefits.

- **Penn World Table (1970–2019 only)**: Green lines. Uses a different methodology that imputes a labor share for self-employed workers, rather than treating proprietors' income as mixed. *Note: PWT data ends in 2019; the line does not extend to 2024.*

- **Adjusted: Includes ⅔ Proprietors' Income**: Purple line. Adds two-thirds of proprietors' income to the numerator, following [Gollin (2002)](https://web.williams.edu/Economics/wp/Gollin_Getting_Income_Shares_Right_working_paper_with_figures.pdf), to account for the labor component of self-employment income.

- **Wages Only**: Amber line. The numerator is just wages and salaries — no benefits, no employer payroll taxes. This shows the steepest decline.

**Interpretation:** All measures show a decline from 1970 to the latest available year (BEA series through 2024; Penn World Table through 2019). The magnitude varies: the decline is −6.5 pp for the standard measure, but −8.9 pp for wages only. This means that rising employer contributions to benefits and payroll taxes have partially masked wage stagnation. If you care about workers' cash wages, the decline is steeper than the headline labor share suggests.

Next, we move on to the importance of adjusting total income for depreciation. 

**Terminology note:** In the labor share literature, "net" means *net of depreciation* (using NDI as denominator), **not** net of taxes. All measures in this document are pre-income-tax.

### Figure 2. Labor Share of Net Income (NDI) Also Declined, But Less Steeply

![Gross vs Net Labor Share](labor_share_net_vs_gross.png)

Figure 2 shows the same total employee compensation (numerator) but divided by two different denominators: one is gross (GDI) the other is net (NDI), meaning depreciation of fixed capital has been deducted. 

Depreciation is a capital maintenance cost — it represents wear and tear on machinery, software, and buildings. Depreciation is not income available for consumption — it represents capital maintenance costs. If you want to know labor's share of *sustainable, distributable income*, the NDI measure is more appropriate. But the decline is real under both measures. The NDI-basis measure shows a smaller decline though (−4.8 pp vs −6.5 pp for gross). 

The standard measure of total income does not exclude depreciation (Blue line) - hence GDI. This contrasts with the red line (net domestic income), whereby depreciation is removed as income from the economy leading to the labour share of income increasing as it is divided by a smaller amount. It is a mechnical relationship. Labor's higher net-income share is the residual result. The gap between two lines has widened. In 1970, depreciation was 12.8% of GDI; by 2024, it had risen to 16.5%. As the depreciation share grew, the difference between GDI and NDI widened. This made labor's share of NDI rise *relative to* the gross labor share — even though both declined in absolute terms.


Next, Figure 3 shows the share of national income going to capital owners, computed as a residual after subtracting labor compensation, depreciation, and taxes on production from GDI. 

### Figure 3. Capital Share Rose as Labor Share Fell

![Capital Share](capital_share.png)

All three lines include exactly **⅓ of proprietors' income** (the capital portion per Gollin 2002), making them consistent with the Gollin-adjusted labor share in Figure 1.

**The equation:**
```
Capital Share = NOS − (⅔ × Proprietors' Income)
              = GDI − Compensation − Depreciation − Taxes on Production − (⅔ × Prop)
```


- ** Pre-Tax Total Capital Share Green**: Green line. Capital share before corporate income taxtes. This rose from 16.9% (1970) to 20.2% (2024), a +3.3 pp increase. This includes interest and rent income and is defined as net Operating Surplus minus ⅔ of proprietors' income, before corporate income taxes. 

- ** Post-Tax Total Capital Share**: Orange line. As above, but now subtracting taxes on corporate income. Still shows an increase, though smaller.

- ** Corporate Profits (less rent and interest) **: Dashed Indigo bottom line. My preferred measure. Properly excludes rent and interest income, which are expenses. Corporate profits (with IVA and CCAdj) minus ⅔ of proprietors' income. This rose from 9.8% (1970) to 13.8% (2024), a +4.0 pp increase. This likely reflects increased profit margins, market concentration, globalization and technological change, and the rise of high-margin technology firms.

**Key Point:** As labor's share of GDI fell by 6.5 percentage points, capital's share (Gollin-adjusted) rose by about 3.3 percentage points. The remainder was absorbed by rising depreciation (+3.7 pp) and a small decrease in taxes on production.


---

# Appendix

## Methodological Notes

### Why GDI, Not GDP? (Denominator Choice)

The labor share is a ratio. The **denominator** is the measure of total national income. We use **GDI** (Gross Domestic Income), not GDP, as the denominator. Here's why:

1. **The numerator comes from the income side.** Compensation of employees is a component of GDI (the income-side measure). Using GDI as the denominator means both numerator and denominator come from the same accounting framework.

2. **Using GDP as denominator introduces noise.** GDP (expenditure-side) and GDI (income-side) differ by a "statistical discrepancy" (typically ~1% of GDP). Dividing an income-side numerator by an expenditure-side denominator mixes measurement error into the ratio.

3. **The shares sum correctly with GDI.** When we use GDI as the denominator, the component shares (compensation, profits, depreciation, etc.) sum to exactly 100%. This would not hold if we used GDP.

### Tax Boundary Declaration

All factor shares in this note are measured **before income taxes**:

| Component | Tax Treatment | Reference |
|-----------|---------------|-----------|
| **Compensation** | Pre-personal income tax, pre-employee FICA; *includes* employer social insurance | Standard total labor cost |
| **Corporate Profits** (with IVA+CCAdj) | Pre-corporate income tax | [BEA definition](https://www.bea.gov/help/glossary/corporate-profits-iva-and-ccadj) |
| **Proprietors' Income** | Pre-personal income tax | Mixed labor/capital |
| **Taxes on Production** | Sales taxes, property taxes, excises | *Not* income taxes |

**What "pre-tax" and "post-tax" mean here:**
- **Pre-personal income tax**: Wages are measured before workers pay income taxes
- **Pre-corporate income tax**: Profits are measured before firms pay corporate taxes
- **Employer FICA**: Included in compensation (standard practice); can be separated out

**We do not construct an "after personal income taxes" labor share** in this note. Doing so requires tax-incidence assumptions (who bears the burden of each tax?) that are beyond the scope of this analysis.

### Assumption: Proprietors' Income

**Proprietors' income** (~7% of GDI) is "mixed income" — it contains both labor and capital returns for self-employed individuals (e.g., a sole-proprietor lawyer's earnings include both compensation for their work and returns on the firm's assets; a farmer's income reflects both their labor and the productivity of their land and equipment). This document follows **[Gollin (2002)](https://web.williams.edu/Economics/wp/Gollin_Getting_Income_Shares_Right_working_paper_with_figures.pdf)** in allocating **⅔ of proprietors' income to labor** and **⅓ to capital** when computing the "Adjusted" labor share measure (purple line in Figure 1).

**Sensitivity to this assumption** (using 2024 values, Prop ≈ 7%):
- Relative to the **Gollin-adjusted** series (Comp + ⅔·Prop ≈ 56.6%): allocating **0%** of proprietors' to labor gives ~4.7 pp lower; allocating **100%** gives ~2.3 pp higher.
- Relative to the **unadjusted** series (Comp/GDI = 51.9%): allocating **100%** of proprietors' to labor adds ~7 pp.

The **standard gross labor share** (blue line) does *not* include any proprietors' income in the numerator — it is simply Compensation of Employees / GDI. The Gollin adjustment only applies to the purple "Adjusted" line in Figure 1, which adds ⅔ of proprietors' income to compensation in the numerator to account for the labor component of self-employment earnings.

### What "Employee Compensation" Includes (Numerator Components)

The BEA "Compensation of Employees" series (A4002E1A156NBEA) includes:

| Component | 2024 Share | Description |
|-----------|------------|-------------|
| **Wages and Salaries** | 42.7% | Cash payments to workers (pre-income tax) |
| **Supplements** | 9.1% | Benefits + employer social insurance contributions |
| └ Employer pension/insurance | ~6.2% | Health insurance, 401(k) contributions |
| └ Employer social insurance (FICA) | ~3.0% | Employer portion of Social Security + Medicare |

**Tax treatment in labor share measures:**

| Tax Type | Treatment in Compensation | Notes |
|----------|---------------------------|-------|
| **Personal income tax** | Pre-tax | Workers pay this out of wages received |
| **Employee FICA** (~7.65%) | Pre-tax | Workers pay this out of wages received |
| **Employer FICA** (~7.65%) | Included in supplements | Standard practice (total labor cost) |

**Why include employer social insurance?** This is standard in the literature ([Karabarbounis & Neiman 2014](https://www.nber.org/papers/w19136), [Autor et al. 2020](https://www.nber.org/papers/w23396)) because:
1. It represents the **total cost of employing labor**
2. It funds benefits workers receive (Social Security, Medicare)
3. Excluding it would understate the true labor share

**Alternative measures for different questions:**

| If you want... | Use this measure | 1970→2024 |
|----------------|------------------|-----------|
| Total labor cost to firms | Total Compensation | −6.5 pp |
| Labor share ex-payroll taxes | Wages + Benefits (excl. employer social insurance) | −7.2 pp |
| Cash wages only | Wages Only | −8.9 pp |

The **"Wages + Benefits (excl. employer social insurance)"** line (teal in Figure 1) excludes employer payroll taxes while keeping private benefits. This shows that excluding payroll taxes, the labor share decline is *steeper* (−7.2 pp), not smaller — because employer social insurance rose from 2.3% to 3.0% of GDI.

### Gross vs Net Income (NDI) Labor Share

**Gross Labor Share** = Compensation / GDI

**Labor Share of Net Income (NDI)** = Compensation / NDI = Compensation / (GDI − Depreciation)

**Important:** "Net" here means *net of depreciation*, **not** net of taxes. This is standard terminology in the labor share literature but can confuse readers.

The NDI-basis measure matters because depreciation (Consumption of Fixed Capital) is **not income available for consumption** — it represents the resources needed to replace worn-out capital. Following [Bridgman (2018)](https://bea.gov/papers/pdf/laborshare1410.pdf) and [Rognlie (2015)](https://www.brookings.edu/wp-content/uploads/2016/07/2015a_rognlie.pdf), measuring labor's share of net income is more relevant for understanding the distribution of *sustainable* income.

**Why depreciation rose:**
- Shift from long-lived assets (buildings: 2-3%/year depreciation) to short-lived assets (software: 25-33%/year)
- Rise of intellectual property products (R&D, software, entertainment originals)
- More capital-intensive economy overall

### Capital Share Methodology: Interest, Rent, and the NIPA Identity

A concern raised: *How do we ensure interest income and rent aren't double-counted when calculating capital's share?*

#### The Key Principle: Profits Are "After Costs"

Corporate profits in the NIPAs (with IVA and CCAdj) are measured as receipts less expenses — including wages, interest paid, and rent paid. This is a *pre-corporate-income-tax* concept. ([BEA Glossary](https://www.bea.gov/help/glossary/corporate-profits-iva-and-ccadj))

#### The "Net Interest" Trap: It's NOT "Bank's Income"

**Caution:** The "Net Interest and Miscellaneous Payments" line in GDI is **not** a direct measure of financial sector income. It is an *offset item* that removes net interest receipts already embedded in corporate profits and proprietors' income. ([BEA NIPA Handbook](https://www.bea.gov/resources/methodologies/nipa-handbook))

Specifically:
- Corporate profits *include* net interest receipts (interest received minus interest paid) as part of business income
- The "Net Interest" GDI component then *offsets* these receipts — in the NIPA production account, interest flows are treated in a way that requires this offset item
- This ensures interest payments flow from borrowers to lenders without double-counting

**Do not interpret "Net Interest" as "the bank's income."** It reflects an accounting treatment of interest flows in the production-income identity, not a clean attribution of income to financial institutions. ([BEA NIPA Update](https://apps.bea.gov/scb/issues/2018/09-september/0918-nipa-update.htm))

#### How GDI Components Are Defined

| Component | What It Measures | Treatment of Interest/Rent |
|-----------|------------------|----------------------------|
| **Corporate Profits** (with IVA+CCAdj) | Profits from current production, *pre-corporate income tax* | Net of interest paid, rent paid, wages, depreciation |
| **Net Interest** | Offset for net interest receipts in profits/proprietors' income | **Not** = financial sector income |
| **Rental Income** | Income of persons from property ownership | Direct measure of landlord income |
| **Compensation** | Wages + supplements paid to employees | — |
| **Proprietors' Income** | Mixed labor/capital income of self-employed | — |
| **Depreciation (CFC)** | Consumption of fixed capital | Not "income" to anyone |
| **Taxes on Production** | Sales taxes, property taxes, excises, etc. | Distinct from income taxes |

#### Why Components Sum to 100%

At the Table 1.11 level, the four main aggregates sum to 100%:

**Compensation + Net Operating Surplus + Taxes on Production + Depreciation = GDI (100%)**

The NOS subcomponents (profits, proprietors', rental, net interest) sum to NOS, not directly to 100%. The BEA separates depreciation as its own GDI component rather than embedding it in profits.

#### Capital Share Calculation (If Needed)

For capital's share, the **residual method** is cleanest:

```
Capital Share = (GDI − Compensation − Taxes on Production − labor portion of Proprietors') / GDI
```

This avoids the "net interest" interpretation problem entirely.

For **depreciation-adjusted** capital share (using NDI):
```
Depreciation-Adjusted Capital Share = (NDI − Compensation − Taxes − labor portion of Proprietors') / NDI
```

**Recommendation:** If you're focused on "capital vs labor," use **Net Operating Surplus** as your capital aggregate (which BEA publishes), rather than manually summing profits + interest + rent. This sidesteps the net-interest accounting complexity.

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

### 2. Labor share of net income (NDI) declined less (~4.8 pp)

On an NDI basis — where depreciation is treated as a capital cost subtracted before distribution — the decline is attenuated. Labor's share of net income went from 67.0% (1970) to 62.2% (2024) — a decline of 4.8 pp compared to 6.5 pp for gross. The NDI-basis decline is ~26% smaller than the gross decline.

### 3. Decomposing the labor share decline

The three-way decomposition reveals where the "missing" labor share went:

| Measure (Numerator / GDI) | 1970 | 2024 | Change |
|---------------------------|------|------|--------|
| Total Compensation (wages + all supplements) | 58.4% | 51.9% | −6.5 pp |
| Wages + Benefits (excl. employer social insurance) | 56.1% | 48.9% | −7.2 pp |
| Wages Only (cash wages, no supplements) | 51.6% | 42.7% | −8.9 pp |

**Key insight:** The rise in supplements (+2.4 pp) consists of:
- **Private benefits** (pension, health insurance): ~+1.7 pp
- **Employer FICA** (Social Security, Medicare): ~+0.7 pp

If you view employer social insurance as a "tax on labor" rather than compensation *to* labor, the true labor share decline is steeper (−7.2 pp).

**Caveat:** Rising private benefits doesn't necessarily mean workers are better off — much of it reflects healthcare cost inflation, not improved coverage.

### 4. Historical context: 1929 was lower

The 1929 gross labor share was 49.5% — below the current 2024 level (51.9%). The 1970 peak was historically high, driven partly by:
- Strong unions
- Tight labor markets
- Less international competition
- Lower capital intensity

---

## Data Tables

### BEA GDI Component Shares (1970 vs 2024)

| Component | 1970 | 2024 | Δ |
|-----------|------|------|---|
| **Compensation of Employees** | **58.4%** | **51.9%** | **−6.5 pp** |
| └ Wages & Salaries | 51.6% | 42.7% | −8.9 pp |
| └ Wages + Benefits (excl. employer social insurance)† | 56.1% | 48.9% | −7.2 pp |
| └ Supplements (total) | 6.7% | 9.1% | +2.4 pp |
|   └ Employer pension/insurance | ~4.5% | ~6.2% | ~+1.7 pp |
|   └ Employer FICA (Social Security, Medicare) | ~2.3% | ~3.0% | ~+0.7 pp |
| Proprietors' Income | 7.3% | 7.0% | −0.3 pp |
| Corporate Profits (with IVA+CCAdj)‡ | 7.4% | 11.5% | +4.1 pp |
| Rental Income | ~2% | 3.7% | ~+2 pp |
| Net Interest | ~4% | 2.1% | ~−2 pp |
| **Depreciation (CFC)** | **12.8%** | **16.5%** | **+3.7 pp** |
| Taxes on Production§ | 7.0% | 6.7% | −0.3 pp |

*Sources: BEA NIPA Table 1.11 via FRED. Key series: [Compensation (A4002E1A156NBEA)](https://fred.stlouisfed.org/series/A4002E1A156NBEA), [Wages (W270RE1A156NBEA)](https://fred.stlouisfed.org/series/W270RE1A156NBEA), [Supplements (A038RE1A156NBEA)](https://fred.stlouisfed.org/series/A038RE1A156NBEA), [Depreciation (A262RE1A156NBEA)](https://fred.stlouisfed.org/series/A262RE1A156NBEA), [Corporate Profits (A445RE1A156NBEA)](https://fred.stlouisfed.org/series/A445RE1A156NBEA). 1970 subcomponent values are approximate. Note: Subcomponents may not sum exactly to totals due to rounding in published share series (e.g., 42.7% + 9.1% = 51.8% ≠ 51.9%).*

**Table notes:**
- † **Wages + Benefits (excl. employer social insurance)**: Compensation minus employer contributions for government social insurance (dominated by FICA). Shows a steeper decline (−7.2 pp) than total compensation (−6.5 pp).
- ‡ **Corporate Profits**: Reported *net of* interest paid, rent paid, and depreciation, but *before* corporate income taxes. Corporate income taxes are paid out of this figure. ([BEA definition](https://www.bea.gov/help/glossary/corporate-profits-iva-and-ccadj))
- § **Taxes on Production**: Includes sales taxes, property taxes, customs duties, etc. These are distinct from corporate income taxes (which come out of profits) and personal income taxes (which workers pay out of compensation).

**Optional extension (not shown):** For a *post-corporate-tax* profit measure, use "Corporate profits after tax with IVA and CCAdj" = profits before tax − taxes on corporate income. ([BEA NIPA Handbook](https://www.bea.gov/resources/methodologies/nipa-handbook))

### Historical Reference: 1929

| Measure | 1929 | 2024 | Note |
|---------|------|------|------|
| Gross Labor Share | 49.5% | 51.9% | 2024 is *higher* |
| Labor Share of NDI | 55.0% | 62.2% | 2024 is *much higher* |
| Depreciation | 10.0% | 16.5% | Rose substantially |
| Proprietors' Income | 13.5% | 7.0% | Collapsed (structural shift) |

*Caveat: Very long-run comparisons (1929 vs. 2024) can be sensitive to historical revisions and definitional changes in the national accounts. The 1929 figures provide context, not precision.*

---

## Which Measure Should You Use?

| Your Question | Recommended Measure | Why |
|---------------|---------------------|-----|
| **Are corporations squeezing workers?** | Gross (corporate sector) | Shows actual firm-level revenue split |
| **What income is sustainable?** | Labor share of NDI (Comp/NDI) | Depreciation isn't available for consumption |
| **How do wages compare to total labor costs?** | Wages vs Total Compensation | Reveals role of benefits/payroll taxes |
| **Labor share excl. govt social insurance?** | Wages + Benefits (excl. employer social insurance) | Excludes employer social insurance (dominated by FICA) from numerator |
| **International comparisons** | Penn World Table | Standardized methodology |
| **Short-run dynamics** | BLS Nonfarm Business | Quarterly frequency |

---

## Literature

### Key Papers

| Paper | Key Argument |
|-------|--------------|
| [**Bridgman (2018)**](https://bea.gov/papers/pdf/laborshare1410.pdf) | Net labor share is more relevant; shows less decline than gross |
| [**Rognlie (2015)**](https://www.brookings.edu/wp-content/uploads/2016/07/2015a_rognlie.pdf) | Most of capital share increase is housing; net capital share stable |
| [**Karabarbounis & Neiman (2014)**](https://www.nber.org/papers/w19136) | Global labor share declined; driven by falling investment prices |
| [**Autor et al. (2020)**](https://www.nber.org/papers/w23396) | "Superstar firms" with low labor shares capture market share |
| [**Koh et al. (2020)**](https://www.bse.eu/sites/default/files/working_paper_pdfs/927_1.pdf) | IPP capitalization explains entire decline |

---

## Data Sources

| Source | Series ID | Description |
|--------|-----------|-------------|
| BEA NIPA | [A4002E1A156NBEA](https://fred.stlouisfed.org/series/A4002E1A156NBEA) | Compensation share of GDI |
| BEA NIPA | [W270RE1A156NBEA](https://fred.stlouisfed.org/series/W270RE1A156NBEA) | Wages & salaries share of GDI |
| BEA NIPA | [A262RE1A156NBEA](https://fred.stlouisfed.org/series/A262RE1A156NBEA) | Depreciation share of GDI |
| BEA NIPA | [A041RE1A156NBEA](https://fred.stlouisfed.org/series/A041RE1A156NBEA) | Proprietors' income share of GDI |
| BEA NIPA | [A445RE1A156NBEA](https://fred.stlouisfed.org/series/A445RE1A156NBEA) | Corporate profits (pre-tax) share of GDI |
| BEA NIPA | [W273RE1A156NBEA](https://fred.stlouisfed.org/series/W273RE1A156NBEA) | Corporate profits (post-tax) share of GDI |
| Penn World Table | [LABSHPUSA156NRUG](https://fred.stlouisfed.org/series/LABSHPUSA156NRUG) | Labor share (different methodology) |
| BLS | [PRS85006173](https://fred.stlouisfed.org/series/PRS85006173) | Nonfarm business labor share index |

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

**Labor Share of Net Domestic Income (NDI):**

*Interpretation:* This is labor's share of **net income**, after depreciation has reduced the income available to capital. Depreciation lowers capital's net income first; labor's higher share of NDI is the consequence. The ratio form below is a convenient way to compute the same net-basis share.

```
NDI = GDI × (1 - Depreciation_Share)
Labor_Share_of_NDI = Compensation_Share / (1 - Depreciation_Share)

Example (2024):
NDI = 100% × (1 - 0.165) = 83.5%
Labor_Share_of_NDI = 51.9% / 83.5% = 62.2%
```

*For completeness, the net capital share counterpart:*
```
Net_Capital_Share (NDI basis) = NOS_Share / (1 - Depreciation_Share)

Example (2024):
Net_Capital_Share = 24.9% / 83.5% = 29.8%
```

Note: "Net" in labor share literature means net-of-depreciation, NOT net-of-taxes.

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

Research note compiled by Ilan Strauss using [Claude Code](https://claude.ai/code). Thank you to Rob Petersen for helpful feedback and clarifying discussions. All errors are my own.

January 2026

---

## Appendix: BLS Nonfarm Business Sector Corroboration

The main analysis uses **whole-economy BEA shares**, which include the government sector and owner-occupied housing. A natural concern: *Is the labor share decline driven by these scope choices rather than genuine trends in the private economy?*

### BLS Nonfarm Business Labor Share

The [BLS nonfarm business labor share index](https://fred.stlouisfed.org/series/PRS85006173) provides an independent check. This series:

- Covers the **nonfarm business sector only** (excludes government, nonprofits, owner-occupied housing)
- Uses **quarterly frequency** (more timely than annual BEA shares)
- Is an **index** (2017=100), not a percentage share — but changes are directly comparable

### Key Finding: Decline Is Confirmed

| Period | BLS Index Value | Change |
|--------|-----------------|--------|
| 1970 Q1 | ~115 | — |
| 2024 Q4 | 96.9 | **−16%** from 1970 peak |

The BLS nonfarm business labor share shows a **~16% decline** from its early-1970s high — *larger* than the whole-economy BEA decline. This confirms:

1. **The decline is real**, not an artifact of government/housing inclusion
2. **If anything, the whole-economy measure understates the private-sector decline** (because government has high labor share and no operating surplus)

### Why Nonfarm Business Shows a Steeper Decline

- **Government sector**: ~15% of GDP, but has near-100% labor share (no profits). Including government *raises* measured whole-economy labor share.
- **Owner-occupied housing**: Adds imputed rental income to GDI with zero compensation. Including it *lowers* measured labor share.
- These effects partially offset, but the net result is that whole-economy measures are *less sensitive* to private-sector profit dynamics than nonfarm business measures.

### Data Source

| Source | Series ID | Description |
|--------|-----------|-------------|
| BLS | [PRS85006173](https://fred.stlouisfed.org/series/PRS85006173) | Nonfarm business labor share index (2017=100) |

*Note: The BLS index is not directly comparable to BEA percentage shares. To convert approximate levels: if 2017 labor share ≈ 58%, then index value 96.9 implies ~56% labor share in 2024 Q4.*

---

## Changelog

### v.2.1 (January 2026)
- **Terminology:** Renamed "Depreciation-Adjusted Labor Share" → "Labor Share of Net Domestic Income (NDI)" throughout to avoid implying depreciation "adjusts" labor
- **Exposition:** Rewrote depreciation sections to present the **capital share effect as logically prior** — depreciation reduces capital's net income first; labor's higher NDI share is the consequence
- **Accounting identities:** Added explicit GDI and NDI identities to make the distributional logic unambiguous
- **Links:** Fixed 5 broken academic links (Gollin, Bridgman, Koh et al., BEA handbook/update) with working alternatives


















