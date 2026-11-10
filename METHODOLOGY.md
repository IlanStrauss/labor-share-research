# Methodological Notes

This document contains detailed methodological notes, data tables, and technical appendices for the labor share analysis. For the main analysis, see [README.md](README.md).

---

## Why GDI, Not GDP? (Denominator Choice)

The labor share is a ratio. The **denominator** is the measure of total national income. We use **GDI** (Gross Domestic Income), not GDP, as the denominator. Here's why:

1. **The numerator comes from the income side.** Compensation of employees is a component of GDI (the income-side measure). Using GDI as the denominator means both numerator and denominator come from the same accounting framework.

2. **Using GDP as denominator introduces noise.** GDP (expenditure-side) and GDI (income-side) differ by a "statistical discrepancy" (typically ~1% of GDP). Dividing an income-side numerator by an expenditure-side denominator mixes measurement error into the ratio.

3. **The shares sum correctly with GDI.** When we use GDI as the denominator, the component shares (compensation, profits, depreciation, etc.) sum to exactly 100%. This would not hold if we used GDP.

---

## Tax Boundary Declaration

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

The main note's shares are before income taxes. [POST_TAX.md](POST_TAX.md) builds after-tax labor and profit shares, assuming each tax is borne by the income it is levied on.

---

## Assumption: Proprietors' Income

**Proprietors' income** (6.5% of GDI in 2024) we view as "mixed income" — it contains both labor and capital returns for self-employed individuals (e.g., a sole-proprietor lawyer's earnings include both compensation for their work and returns on the firm's assets; a farmer's income reflects both their labor and the productivity of their land and equipment). This document splits proprietors' income between labor and capital **in the same ratio as the rest of the economy's income**, year by year, for the "Adjusted" labor share measure (purple line in Figure 1) and the profit share (Figure 3). Labor's fraction is compensation divided by compensation plus net operating surplus other than proprietors' income: 81.3% in 1970 and 72.8% in 2024 ([`data/proprietors_income_split.csv`](data/proprietors_income_split.csv)). This is the "economy-wide basis" of Kravis (1959). [Elsby, Hobijn and Şahin (2013)](https://www.brookings.edu/articles/the-decline-of-the-u-s-labor-share/) show that the main alternative, the BLS method of paying the self-employed what employees earn, implied a negative capital share among the self-employed in the 1980s. Earlier versions of this note gave a fixed two-thirds to labor, a common convention since Johnson (1954) ([Krueger 1999](https://doi.org/10.1257/aer.89.2.45)). 

**Sensitivity to this assumption** (2024 values, proprietors' income = 6.5% of GDI):
- Relative to the **adjusted** series (Comp + labor part = 56.2%): allocating **0%** of proprietors' income to labor gives 51.4%, 4.8 pp lower; allocating **100%** gives 58.0%, 1.8 pp higher.
- The earlier two-thirds rule gave 55.8% in 2024 and a 1970–2024 fall of 7.4 pp, against 8.1 pp now, because labor's fraction fell from 81% to 73%.
- Relative to the **unadjusted** series (Comp/GDI = 51.4%): allocating **100%** of proprietors' income to labor adds 6.5 pp.

The **standard gross labor share** (blue line) does *not* include any proprietors' income in the numerator — it is simply Compensation of Employees / GDI. The adjustment only applies to the purple "Adjusted" line in Figure 1, which adds the labor part of proprietors' income to compensation in the numerator to account for the labor component of self-employment earnings.

---

## What "Employee Compensation" Includes (Numerator Components)

BEA's compensation of employees (series A4002C) includes:

| Component | 2024 Share | Description |
|-----------|------------|-------------|
| **Wages and Salaries** | 42.3% | Cash payments to workers (pre-income tax) |
| **Supplements** | 9.1% | Benefits + employer social insurance contributions |
| └ Employer pension/insurance | 6.1% | Health insurance, 401(k) contributions |
| └ Employer social insurance (FICA) | 2.9% | Employer portion of Social Security + Medicare |

*The two employer contributions come from BEA's national income table (Table 1.12), so they sum to 0.1 pp less than supplements paid by domestic employers.*

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
| Total labor cost to firms | Total Compensation | −6.9 pp |
| Labor share ex-payroll taxes | Wages + Benefits (excl. employer social insurance) | −7.6 pp |
| Cash wages only | Wages Only | −9.3 pp |

The **"Wages + Benefits (excl. employer social insurance)"** line (pink in Figure 1) excludes employer payroll taxes while keeping private benefits. This shows that excluding payroll taxes, the labor share decline is *steeper* (−7.6 pp), not smaller, because employer social insurance rose from 2.2% to 2.9% of GDI.

---

## Gross vs Net Income (NDI) Labor Share

**Gross Labor Share** = Compensation / GDI

**Labor Share of Net Income (NDI)** = Compensation / NDI = Compensation / (GDI − Depreciation)

**Important:** "Net" here means *net of depreciation*, **not** net of taxes. This is standard terminology in the labor share literature but can confuse readers.

The NDI-basis measure matters because depreciation (Consumption of Fixed Capital) is **not income available for consumption** — it represents the resources needed to replace worn-out capital. Following [Bridgman (2018)](https://doi.org/10.1017/S1365100516001000) and [Rognlie (2015)](https://www.brookings.edu/wp-content/uploads/2016/07/2015a_rognlie.pdf), measuring labor's share of net income is more relevant for understanding the distribution of *sustainable* income.

**Why depreciation rose:** almost all of the rise is intellectual property products (software, R&D, and entertainment originals). Their depreciation rose from 1.4% to 4.5% of GDI between 1970 and 2024, 3.1 pp of depreciation's 3.6 pp rise (Figure 4 of the main note). These assets wear out fast: [BEA depreciates](https://apps.bea.gov/national/pdf/BEA_depreciation_rates.pdf) software at 33–55% a year, against 2–3% for office and commercial buildings.

---

## Capital Share Methodology: Interest, Rent, and the NIPA Identity

A concern raised: *How do we ensure interest income and rent aren't double-counted when calculating capital's share?*

### The Key Principle: Profits Are "After Costs"

Corporate profits in the NIPAs (with IVA and CCAdj) are measured as receipts less expenses — including wages, interest paid, and rent paid. This is a *pre-corporate-income-tax* concept. ([BEA Glossary](https://www.bea.gov/help/glossary/corporate-profits-iva-and-ccadj))

### Net Interest Is Not "Bank's Income"

The "Net Interest and Miscellaneous Payments" line in GDI is the interest that businesses pay less the interest they receive ([BEA NIPA Handbook](https://www.bea.gov/resources/methodologies/nipa-handbook)). Corporate profits and proprietors' income are measured after both, so net interest and profits do not overlap. Interest that one business pays another cancels out, so the line measures what businesses as a whole pay, net, to lenders outside the business sector, such as households, government, and foreign lenders.

**Do not interpret "Net Interest" as "the bank's income."** A bank's interest margin is part of its own profits; the net interest line is not a measure of financial-sector income.

### How GDI Components Are Defined

| Component | What It Measures | Treatment of Interest/Rent |
|-----------|------------------|----------------------------|
| **Corporate Profits** (with IVA+CCAdj) | Profits from current production, *pre-corporate income tax* | Net of interest paid, rent paid, wages, depreciation |
| **Net Interest** | Interest paid by businesses less interest they receive | **Not** = financial sector income |
| **Rental Income** | Income of persons from property ownership | Direct measure of landlord income |
| **Compensation** | Wages + supplements paid to employees | — |
| **Proprietors' Income** | Mixed labor/capital income of self-employed | — |
| **Depreciation (CFC)** | Consumption of fixed capital | Not "income" to anyone |
| **Taxes on Production** | Sales taxes, property taxes, excises, etc. | Distinct from income taxes |

### Why Components Sum to 100%

At the Table 1.11 level, the four main aggregates sum to 100%:

**Compensation + Net Operating Surplus + Taxes on Production + Depreciation = GDI (100%)**

The NOS subcomponents (corporate profits, proprietors' income, rental income, net interest, business transfer payments, and the current surplus of government enterprises) sum to NOS, not directly to 100%. The BEA separates depreciation as its own GDI component rather than embedding it in profits.

### Capital Share Calculation (If Needed)

For capital's share, the **residual method** is cleanest:

```
Capital Share = (GDI − Compensation − Taxes on Production − labor part of Proprietors' income) / GDI
```

This avoids the "net interest" interpretation problem entirely.

For **depreciation-adjusted** capital share (using NDI):
```
Depreciation-Adjusted Capital Share = (NDI − Compensation − Taxes − labor part of Proprietors' income) / NDI
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

The **nonfarm business sector** shows a steeper decline. The [BLS nonfarm business labor share index](https://data.bls.gov/timeseries/PRS85006173) fell about 15% from 1970 to 2024 (annual averages of 114.0 and 96.5), against 12% for compensation over GDI. See the BLS section below for why the two differ.

---

## Key Findings Explained

### 1. Gross labor share declined 6.9 pp from its 1970 peak

Labor share peaked at 58.4% in 1970, its highest since BEA's data begin in 1929, and fell to 51.4% by 2024. This timing coincides with declining unionization, globalization, and automation — though causal attribution requires careful analysis.

### 2. Labor share of net income (NDI) declined less (5.4 pp)

On an NDI basis, where depreciation is treated as a capital cost subtracted before distribution, the decline is attenuated. Labor's share of net income went from 66.9% (1970) to 61.5% (2024), a decline of 5.4 pp compared to 6.9 pp for gross. The NDI-basis decline is 22% smaller than the gross decline.

### 3. Decomposing the labor share decline

The three-way decomposition reveals where the "missing" labor share went:

| Measure (Numerator / GDI) | 1970 | 2024 | Change |
|---------------------------|------|------|--------|
| Total Compensation (wages + all supplements) | 58.4% | 51.4% | −6.9 pp |
| Wages + Benefits (excl. employer social insurance) | 56.1% | 48.5% | −7.6 pp |
| Wages Only (cash wages, no supplements) | 51.6% | 42.3% | −9.3 pp |

**Key insight:** The rise in supplements (+2.3 pp) consists of:
- **Private benefits** (pension, health insurance): +1.6 pp
- **Employer FICA** (Social Security, Medicare): +0.7 pp

If you view employer social insurance as a "tax on labor" rather than compensation *to* labor, the labor share decline is steeper (−7.6 pp).

**Caveat:** Rising private benefits doesn't necessarily mean workers are better off — much of it reflects healthcare cost inflation, not improved coverage.

---

## Data Tables

### BEA GDI Component Shares (1970 vs 2024)

| Component | 1970 | 2024 | Δ |
|-----------|------|------|---|
| **Compensation of Employees** | **58.4%** | **51.4%** | **−6.9 pp** |
| └ Wages & Salaries | 51.6% | 42.3% | −9.3 pp |
| └ Wages + Benefits (excl. employer social insurance)† | 56.1% | 48.5% | −7.6 pp |
| └ Supplements (total) | 6.7% | 9.1% | +2.3 pp |
|   └ Employer pension/insurance | 4.5% | 6.1% | +1.6 pp |
|   └ Employer FICA (Social Security, Medicare) | 2.2% | 2.9% | +0.7 pp |
| Proprietors' Income | 7.3% | 6.5% | −0.7 pp |
| Corporate Profits (with IVA+CCAdj), domestic industries‡ | 7.4% | 11.3% | +3.9 pp |
| Rental Income | 1.9% | 3.6% | +1.7 pp |
| Net Interest, domestic industries | 3.8% | 3.5% | −0.3 pp |
| Other Net Operating Surplus¶ | 0.3% | 0.8% | +0.5 pp |
| **Depreciation (CFC)** | **12.8%** | **16.4%** | **+3.6 pp** |
| Taxes on Production and Imports less Subsidies§ | 8.1% | 6.4% | −1.7 pp |

*Source: BEA NIPA Tables 1.10 and 1.12, from BEA's bulk data file of 4 November 2026, saved in [`data/`](data/); `python3 scripts/readme_numbers.py` prints this table. Compensation and the rows below it from Proprietors' Income down sum to 100% of GDI. Changes are computed from unrounded data. The two employer contributions come from Table 1.12, so they sum to 0.1 pp less than supplements in 2024.*

**Table notes:**
- † **Wages + Benefits (excl. employer social insurance)**: Compensation minus employer contributions for government social insurance (dominated by FICA). Shows a steeper decline (−7.6 pp) than total compensation (−6.9 pp).
- ‡ **Corporate Profits**: Reported *net of* interest paid, rent paid, and depreciation, but *before* corporate income taxes. Corporate income taxes are paid out of this figure. ([BEA definition](https://www.bea.gov/help/glossary/corporate-profits-iva-and-ccadj)) This row uses BEA's economic depreciation (with IVA and CCAdj); Figure 3 of the main note uses depreciation as firms report it for tax (without IVA and CCAdj), and Figure 4 compares the two.
- ¶ **Other Net Operating Surplus**: business current transfer payments (net) and the current surplus of government enterprises.
- § **Taxes on Production and Imports less Subsidies**: Includes sales taxes, property taxes, customs duties, etc. These are distinct from corporate income taxes (which come out of profits) and personal income taxes (which workers pay out of compensation).

**After-tax measures:** [POST_TAX.md](POST_TAX.md) builds labor and profit shares after payroll, income, and corporate taxes.

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
| [**Bridgman (2018)**](https://doi.org/10.1017/S1365100516001000) | Net labor share is more relevant; shows less decline than gross |
| [**Rognlie (2015)**](https://www.brookings.edu/wp-content/uploads/2016/07/2015a_rognlie.pdf) | The long-run rise in the net capital share comes from housing |
| [**Karabarbounis & Neiman (2014)**](https://www.nber.org/papers/w19136) | Global labor share declined; driven by falling investment prices |
| [**Autor et al. (2020)**](https://www.nber.org/papers/w23396) | "Superstar firms" with low labor shares capture market share |
| [**Koh et al. (2020)**](https://doi.org/10.3982/ECTA17477) | IPP capitalization explains entire decline |
| [**Barkai, Nallareddy and Ogneva (2025)**](https://doi.org/10.1016/j.red.2024.101268) | The decline does not depend on IPP capitalization |

---

## Data Sources

| Source | Series ID | Description |
|--------|-----------|-------------|
| BEA NIPA | A261RC | Gross domestic income |
| BEA NIPA | A4002C | Compensation of employees, paid |
| BEA NIPA | W270RC | Wages and salaries |
| BEA NIPA | A262RC | Consumption of fixed capital (depreciation) |
| BEA NIPA | A041RC | Proprietors' income with IVA and CCAdj |
| BEA NIPA | A445RC | Corporate profits with IVA and CCAdj, domestic industries |
| BEA NIPA | A053RC, A055RC | Corporate profits before and after tax, without IVA and CCAdj (Figure 3) |
| Penn World Table 11.0 | labsh | Labor share (different methodology) |
| BLS | [PRS85006173](https://data.bls.gov/timeseries/PRS85006173) | Nonfarm business labor share index |

All data are saved in [`data/`](data/). [`data/README.md`](data/README.md) gives each dataset's source and download date, and [`scripts/fetch_data.py`](scripts/fetch_data.py) lists every BEA series the scripts use.

---

## Replication

### Running the Code

```bash
python3 scripts/readme_numbers.py   # prints every number in README.md and this document
python3 scripts/generate_chart.py
```

`generate_chart.py` produces:
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
NDI = 100% × (1 - 0.1640) = 83.60%
Labor_Share_of_NDI = 51.42% / 83.60% = 61.51%
```

*For completeness, the net capital share counterpart:*
```
Net_Capital_Share (NDI basis) = NOS_Share / (1 - Depreciation_Share)

Example (2024):
Net_Capital_Share = 25.77% / 83.60% = 30.83%
```

Note: "Net" in labor share literature means net-of-depreciation, NOT net-of-taxes.

**Adjusted Labor Share (with proprietors' income):**
```
Adjusted = Compensation_Share + (α × Proprietors_Share)
where α = Compensation / (Compensation + Net_Operating_Surplus − Proprietors_Income), recomputed each year

Example (2024):
α = 51.42% / (51.42% + 25.77% − 6.54%) = 0.728
Adjusted = 51.42% + (0.728 × 6.54%) = 56.18%
```

---

## BLS Nonfarm Business Sector Corroboration

The main analysis uses **whole-economy BEA shares**, which include the government sector and owner-occupied housing. A natural concern: *Is the labor share decline driven by these scope choices rather than genuine trends in the private economy?*

### BLS Nonfarm Business Labor Share

The [BLS nonfarm business labor share index](https://data.bls.gov/timeseries/PRS85006173) provides an independent check. This series:

- Covers the **nonfarm business sector only** (excludes government, nonprofits, owner-occupied housing)
- Credits the self-employed with the average hourly pay of employees
- Uses **quarterly frequency** (more timely than annual BEA shares)
- Is an **index** (2017=100), not a percentage share — but changes are directly comparable

### Key Finding: Decline Is Confirmed

| Period | BLS Index Value | Change |
|--------|-----------------|--------|
| 1970 (annual average) | 114.0 | — |
| 2024 (annual average) | 96.5 | **−15%** from 1970 |

The BLS nonfarm business labor share shows a **15% decline** from 1970, its early-1970s peak, to 2024, *larger* than the 12% decline in compensation over GDI. The decline is therefore not an artifact of including government and housing.

### Why the Two Measures Differ

- **Government** has no operating surplus: its value added is employee compensation (77% in 2024) plus depreciation of its capital (23%). Including it *raises* the level of the whole-economy labor share.
- **Owner-occupied housing** adds imputed rental income to GDI with no compensation. Including it *lowers* the level.
- **Over time, both pull the whole-economy share down.** General government's value added fell from 15.2% of GDP in 1970 to 10.5% in 2024, and housing's rose from 7.3% to 9.4%. Leaving out general government and housing value added, compensation's share of the rest of GDI fell from about 60% to about 54%, a 10% decline, smaller than the 12% whole-economy decline.
- **Scope therefore does not explain why the BLS index falls more.** The BLS measure also differs in method: it credits the self-employed with employees' average hourly pay. [Elsby, Hobijn and Şahin (2013)](https://www.brookings.edu/articles/the-decline-of-the-u-s-labor-share/) find that this imputation accounts for about a third of the decline in the BLS headline measure.

### Data Source

| Source | Series ID | Description |
|--------|-----------|-------------|
| BLS | [PRS85006173](https://data.bls.gov/timeseries/PRS85006173) | Nonfarm business labor share index (2017=100) |

*Note: The BLS series is an index (2017 = 100), so only its percentage changes can be compared with BEA's shares.*


---

## Literature Review

### What Studies Find Quantitatively

Reported magnitudes of the labor share decline vary across studies, sectors, and periods. [Karabarbounis and Neiman (2014)](https://www.nber.org/papers/w19136) document a decline of about 5 pp in the global corporate labor share, from roughly 64 percent in 1975 to about 59 percent in 2012. [Elsby, Hobijn and Şahin (2013)](https://www.brookings.edu/articles/the-decline-of-the-u-s-labor-share/) find that the BLS headline labor share for U.S. nonfarm business averaged 64.6 percent over 1948 to 1987 and 58.3 percent over 2010 to 2012, a fall of 6.4 pp, while the payroll share (employee compensation alone) fell 3.9 pp. [Autor et al. (2020)](https://www.nber.org/papers/w23396) show that the U.S. decline is driven mainly by a reallocation of sales toward firms with low labor shares rather than by falling labor shares within most firms.

Alternative measures yield different pictures. [Bridgman (2018)](https://doi.org/10.1017/S1365100516001000) finds that the net labor share, after depreciation and production taxes, is within its historical range, while the gross share is at its lowest level. [Rognlie (2015)](https://www.brookings.edu/wp-content/uploads/2016/07/2015a_rognlie.pdf) shows that the long-run rise in the net capital share comes from housing; elsewhere the net capital share has only recovered from a fall that lasted from 1948 through the 1970s. Barkai (2020, *Journal of Finance*) finds that in the U.S. nonfinancial corporate sector from 1984 to 2014 both the labor share and the capital share fell, offset by a large rise in the share of pure profits. [Koh, Santaeulàlia-Llopis and Zheng (2020)](https://doi.org/10.3982/ECTA17477) argue that the capitalization of intellectual-property products (IPP) in the national accounts fully accounts for the decline over the past 90 years.

Our estimates for the whole economy from the 1970 peak are 6.9 pp for compensation over GDI, 5.4 pp over NDI, and 9.3 pp for wages only, so the measured decline varies by about 70 percent across these choices alone. The studies above cover different sectors and years, so their magnitudes are not directly comparable with ours.

### Causal Mechanisms

The literature proposes four broad, non-mutually-exclusive mechanisms.

**Falling capital-goods prices** ([Karabarbounis and Neiman 2014](https://www.nber.org/papers/w19136)). If capital and labor are gross substitutes, a fall in the relative price of investment goods raises the capital-labor ratio and lowers labor's share. They estimate that the lower price of investment goods explains roughly half of the global decline.

**Market power and superstar firms** ([Autor et al. 2020](https://www.nber.org/papers/w23396); De Loecker, Eeckhout, and Unger 2020, *QJE*; Barkai 2020, *Journal of Finance*). Rising product-market concentration reallocates output toward low-labor-share firms, and rising markups redistribute income from both labor and capital toward pure profits. De Loecker et al. estimate that aggregate U.S. markups rose from 21 percent above marginal cost in 1980 to 61 percent in 2016.

**Automation and task displacement** ([Acemoglu and Restrepo 2019](https://www.aeaweb.org/articles?id=10.1257/jep.33.2.3), *JEP*). Automation shifts tasks from labor to capital, which lowers labor's share of value added, while new tasks for labor raise it. They find that over the last three decades displacement has been stronger, and the creation of new tasks weaker, than in earlier decades. See also Acemoglu and Restrepo (2020, *JPE*) on robots and local labor markets, and (2022, *Econometrica*) on automation and wage inequality.

**Intangible-capital measurement** ([Koh et al. 2020](https://doi.org/10.3982/ECTA17477)). The decline is a consequence of the BEA's capitalization of IPP: software in 1999, and R&D and entertainment, literary, and artistic originals in 2013. [Barkai, Nallareddy and Ogneva (2025, *Review of Economic Dynamics*)](https://doi.org/10.1016/j.red.2024.101268) rebut this. With the same U.S. aggregates, they find that the labor share has clearly declined in recent decades whether or not IPP is capitalized: Koh et al.'s straight-line trend over 1929 to 2018 mistakes slow long-run growth in IPP for a recent drop, and on net value added, faster IPP investment is almost entirely offset by its depreciation.

### Data and Measurement Issues

Several methodological choices materially affect the reported decline, and studies handle them differently.

*Sector scope.* Whole-economy measures include government and owner-occupied housing. Government has no operating surplus (its value added is compensation plus depreciation), which raises the level of the whole-economy share; housing adds imputed rental income with no compensation, which lowers it. The BLS nonfarm business index, which leaves out both and also imputes pay to the self-employed, fell about 15 percent from 1970 to 2024, against about 12 percent for compensation over GDI (see the BLS section above).

*Gross versus net income.* Depreciation rose from 12.8 percent of GDI in 1970 to 16.4 percent in 2024, almost all of it from intellectual property products, which wear out fast: BEA depreciates software at 33 to 55 percent a year, against 2 to 3 percent for office and commercial buildings. The gap between gross and net labor-share measures has therefore widened. Bridgman and Rognlie prefer net; Karabarbounis-Neiman and Autor et al. use gross.

*Proprietors' income.* Proprietors' income, 6.5 percent of GDI in 2024, mixes the self-employed's pay for their work with returns on their business assets. A common convention since Johnson (1954) gives two-thirds of it to labor ([Krueger 1999](https://doi.org/10.1257/aer.89.2.45)); the BLS instead credits the self-employed with employees' average hourly pay. Elsby, Hobijn and Şahin (2013) find that the BLS imputation implied a negative capital share among the self-employed in the 1980s and accounts for about a third of the decline in the BLS headline measure; two alternatives from Kravis (1959), which split self-employment income in the same proportion as the rest of the economy or give the self-employed's capital the same return as other capital, show smaller declines. This note uses the first of these, the economy-wide basis. [Gollin (2002)](https://web.williams.edu/Economics/wp/Gollin_Getting_Income_Shares_Right_working_paper_with_figures.pdf) shows that the treatment of self-employment income matters greatly for comparing labor shares across countries. Here, giving none or all of it to labor moves the 2024 share by up to 6.5 pp.

*IPP capitalization.* The BEA's 1999 and 2013 comprehensive revisions reclassified software, then R&D and entertainment, literary, and artistic originals, as investment rather than expense. Koh et al. (2020) argue that this accounting change alone drives the observed decline; Barkai, Nallareddy and Ogneva (2025) find that the decline does not depend on it.

*Housing.* Owner-occupied housing contributes imputed rental income to GDI with no offsetting labor compensation. [Rognlie (2015)](https://www.brookings.edu/wp-content/uploads/2016/07/2015a_rognlie.pdf) shows that housing accounts for the long-run rise in the net capital share, so part of the "capital versus labor" story is a story about housing.

*Wages versus total compensation.* Rising employer benefits (health insurance, pensions) and payroll taxes have partly offset falling cash wages. Wages-only measures show a decline about a third larger than total compensation (9.3 pp versus 6.9 pp). Whether employer contributions count as compensation to labor or as a tax on labor is a definitional choice with material consequences for the reported magnitude.

This note maps these measurement choices to the research questions they best answer, rather than defending a single specification.
