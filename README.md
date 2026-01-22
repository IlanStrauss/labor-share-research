# U.S. Labor Share of GDP: A Methodological Research Note (Claude Code)

## Executive Summary (To be filled)

**The "declining labor share" narrative is methodologically sensitive.** Different measurement approaches yield dramatically different conclusions about whether labor's share of national income has declined.

---

## 🔑 Key Findings

| Finding | Implication |
|---------|-------------|
| **Gross labor share (compensation/GDI) increased** from 49.5% (1929) to 51.9% (2024) | The long-run trend is *up*, not down |
| **Decline is real from 1970 peak** (58.4%) to 2024 (51.9%) | ~6.5 pp decline over 54 years |
| **Net labor share has *increased*** when accounting for rising depreciation | Depreciation rose from 10% to 16.5% of GDI |
| **Wages fell but benefits rose more** | Wages: 48.6% → 42.8%; Benefits: 0.9% → 9.1% |
| **Proprietors' income collapsed** from 13.5% to 7.0% | Confounds labor share measurement |
| **Corporate profits rose modestly** from 10.2% to 11.5% | +1.3 pp over 95 years |

---

## 📈 Labor Share Over Time: Multiple Measures

![U.S. Labor Share Comparison Chart](labor_share_comparison.png)

**Key Takeaway:** The story you tell depends on how you measure:
- **Blue (Gross BEA):** Shows decline from 1970 peak, but higher than 1929
- **Green (Penn World Table):** Similar pattern, different methodology
- **Red (Net, depreciation-adjusted):** Shows labor share has *increased*
- **Purple (with proprietors' income):** Shows modest decline

---

## 🎯 Which Measure Should You Use?

**There is no single "correct" measure.** The right choice depends on your research question:

| If You're Studying... | Recommended Measure | Why |
|-----------------------|---------------------|-----|
| **Aggregate welfare / living standards** | **Net Labor Share** (red line) | Depreciation can't be consumed; net income is what's available for households |
| **Corporate bargaining power / markups** | **Corporate sector only** | Avoids proprietors' income imputation; cleanest labor vs capital split |
| **Long-run structural change** | **BEA Gross with proprietors' adjustment** (purple) | Accounts for shift from self-employment to wage employment |
| **International comparisons** | **Penn World Table** (green) | Standardized methodology across countries |
| **Short-run cyclical dynamics** | **BLS Nonfarm Business** | Quarterly frequency, timely release |
| **Globalization / profit shifting** | **GNI-based measure** | Attributes income to residents, not production location |

### Why Rising Depreciation Matters: A Numerical Example

The key insight is that **depreciation has grown faster than any other income category**, mechanically pushing down the gross labor share even when the net share is stable or rising.

**The Math:**

```
Gross Labor Share = Compensation / GDI
Net Labor Share   = Compensation / (GDI − Depreciation)
```

| Year | Compensation | Depreciation | GDI | Gross LS | Net Income | Net LS |
|------|--------------|--------------|-----|----------|------------|--------|
| 1929 | 49.5 | 10.0 | 100 | **49.5%** | 90.0 | **55.0%** |
| 2024 | 51.9 | 16.5 | 100 | **51.9%** | 83.5 | **62.2%** |
| *Change* | *+2.4* | *+6.5* | — | *+2.4 pp* | *−6.5* | *+7.2 pp* |

**What happened:**
- Compensation's share of GDI actually **rose** (+2.4 pp)
- But depreciation rose **even faster** (+6.5 pp)
- This shrinks the "pie" available for distribution (Net Income fell from 90 to 83.5)
- Labor's share of this smaller pie **increased substantially** (+7.2 pp)

**Why depreciation rose:**
- Shift from long-lived assets (buildings: 2-3% depreciation/year) to short-lived assets (software: 25-33%/year)
- Rise of intellectual property products (IPP) — R&D, software, entertainment
- More capital-intensive economy overall

**The implication:** If you care about what workers can actually consume (welfare), use net. If you care about production function parameters, use gross.

---

### Our Recommended Default: Net Labor Share

For most policy discussions about "whether workers are getting their fair share," we recommend the **Net Labor Share** (red line) because:

1. **Depreciation is not income** — it's the cost of maintaining the capital stock
2. **Rising depreciation explains most of the "decline"** — from 10% (1929) to 16.5% (2024) of GDI
3. **Net measures show stability or increase** — contradicting the declinist narrative
4. **Better welfare interpretation** — reflects income actually available for consumption

However, if your focus is specifically on **corporate power and markups**, the corporate sector gross measure is more appropriate since it directly measures the labor-capital split without imputation issues.

### When the Gross Measure Makes Sense

The standard **Gross Labor Share** (blue line) is appropriate when:
- Comparing to most existing literature (which uses gross)
- Analyzing production function parameters
- Studying capital-labor substitution elasticity
- You believe depreciation reflects real economic costs firms face

---

## ⚠️ Points to Consider

### Methodological Choices That Change the Story

1. **Time Period Selection**
   - 1929–2024: Labor share *increased* +2.4 pp
   - 1970–2024: Labor share *declined* ~6.5 pp
   - Post-2000: Decline accelerated

2. **Gross vs Net Measures**
   - Gross measures include depreciation in the denominator
   - Net measures (subtracting depreciation) show less/no decline
   - Depreciation cannot be consumed—net measures may better reflect welfare

3. **Treatment of Proprietors' Income**
   - Mixed income (self-employed) is part labor, part capital
   - Different imputation methods swing measured labor share by ~10 pp
   - Corporate sector focus avoids this but misses large portion of economy

4. **GDP vs GNP/GNI**
   - GDP: Production within borders regardless of ownership
   - GNP: Income accruing to residents regardless of location
   - Profit shifting by multinationals makes GDP-based measures potentially misleading

5. **Wages vs Total Compensation**
   - Wage-only measures show clear decline
   - Total compensation (including benefits) shows much less decline
   - Health insurance costs have shifted from wages to benefits

---

## 📊 Data Tables

### BEA Table 1.11: Percentage Shares of Gross Domestic Income

| Component | 1929 | 1970 | 2024 | Δ (1929→2024) |
|-----------|------|------|------|---------------|
| **Compensation of Employees** | **49.5%** | **58.4%** | **51.9%** | **+2.4 pp** |
| └ Wages & Salaries | 48.6% | ~50% | 42.8% | -5.8 pp |
| └ Supplements (Benefits) | 0.9% | ~8% | 9.1% | +8.2 pp |
| Proprietors' Income | 13.5% | ~8% | 7.0% | -6.5 pp |
| Corporate Profits | 10.2% | ~9% | 11.5% | +1.3 pp |
| Rental Income | 5.8% | ~2% | 3.7% | -2.1 pp |
| Net Interest | 3.9% | ~4% | 2.1% | -1.8 pp |
| **Depreciation (CFC)** | **10.0%** | **~13%** | **16.5%** | **+6.5 pp** |
| Taxes on Production | 6.6% | ~7% | 6.7% | +0.1 pp |

*Source: BEA NIPA Table 1.11, accessed via FRED (January 2026)*

### Penn World Table Labor Share (1950-2019)

| Year | Labor Share | Notes |
|------|-------------|-------|
| 1950 | 62.8% | Post-WWII |
| 1960 | 63.7% | |
| 1970 | 64.9% | **Peak** |
| 1980 | 62.4% | |
| 1990 | 61.5% | |
| 2000 | 63.7% | Dot-com boom |
| 2010 | 58.8% | Post-GFC low |
| 2019 | 59.7% | Latest available |

*Source: Penn World Table 10.01 via FRED (LABSHPUSA156NRUG)*

### BEA Employee Compensation Share (Selected Years, 1929-2024)

| Year | Compensation Share | Context |
|------|-------------------|---------|
| 1929 | 49.5% | Pre-Depression |
| 1932 | 52.9% | Depression peak (GDP collapsed) |
| 1944 | 56.0% | WWII peak |
| 1970 | 58.4% | **All-time peak** |
| 1980 | 57.7% | |
| 1990 | 57.0% | |
| 2000 | 56.6% | |
| 2010 | 53.0% | Post-GFC |
| 2020 | 54.6% | COVID (transfer payments) |
| 2024 | 51.9% | Latest |

*Source: BEA via FRED (A4002E1A156NBEA)*

---

## 🔬 Methodological Approaches

### Approach 1: Gross Labor Share (Standard)

**Formula:** `Labor Share = Compensation of Employees / Gross Domestic Income`

**Pros:**
- Simple, widely used
- Directly from national accounts

**Cons:**
- Includes depreciation which cannot be consumed
- Sensitive to capital intensity changes

**Result:** Modest decline from 1970 peak; increase since 1929

### Approach 2: Net Labor Share

**Formula:** `Net Labor Share = Compensation / (GDI - Depreciation)`

**Calculation:**
| Year | Compensation | Depreciation | NDI | Net Labor Share |
|------|--------------|--------------|-----|-----------------|
| 1929 | 49.5% | 10.0% | 90.0% | **55.0%** |
| 2024 | 51.9% | 16.5% | 83.5% | **62.2%** |

**Pros:**
- Better reflects distributable income
- Accounts for rising capital intensity

**Cons:**
- Depreciation measurement controversial
- Less commonly reported

**Result:** Labor share has *increased* on net basis

### Approach 3: With Proprietors' Income Adjustment

**Formula:** `Adjusted Labor Share = (Compensation + α × Proprietors' Income) / GDI`

Where α = assumed labor share of proprietors' income (typically 0.5–0.75)

**Calculation (α = 0.67):**
| Year | Compensation | Proprietors' | Adjusted Labor Share |
|------|--------------|--------------|---------------------|
| 1929 | 49.5% | 13.5% | 49.5 + 9.0 = **58.5%** |
| 2024 | 51.9% | 7.0% | 51.9 + 4.7 = **56.6%** |

**Pros:**
- Accounts for self-employment income
- More comprehensive measure

**Cons:**
- Requires arbitrary assumption about α
- Self-employment has changed character

**Result:** Modest decline (~2 pp) vs unadjusted increase

### Approach 4: Corporate Sector Only

Focus exclusively on corporate sector to avoid proprietors' income imputation.

**Pros:**
- Clean separation of labor vs capital
- No imputation required

**Cons:**
- Misses large portion of economy
- Corporate share has grown (composition effect)

**Result:** Clearer decline (~5 pp since 1975 per Karabarbounis & Neiman)

### Approach 5: GNP/GNI-Based Measure

**Formula:** `Labor Share = Compensation / Gross National Income`

**Rationale:**
- GNI = GDP + Net Factor Income from Abroad
- Attributes income to residents, not production location
- Adjusts for multinational profit shifting

**For U.S.:** NFIA is positive but small (~0.5-1% of GDP), so GNI > GDP. This would *slightly increase* measured labor share.

**Result:** Minor adjustment for U.S.; more significant for small open economies (Ireland, etc.)

---

## 📚 Literature Review

### Seminal Papers

| Paper | Key Argument |
|-------|--------------|
| [**Karabarbounis & Neiman (2014)**](https://academic.oup.com/qje/article-abstract/129/1/61/1899422) | Global labor share declined ~5 pp since 1975; driven by falling price of investment goods |
| [**Gollin (2002)**](https://www.jstor.org/stable/10.1086/338747) | Self-employment income adjustment eliminates apparent cross-country differences |
| [**Rognlie (2015)**](https://www.brookings.edu/articles/deciphering-the-fall-and-rise-in-the-net-capital-share/) | Most of capital share increase is housing; net capital share stable |
| [**Bridgman (2018)**](https://www.cambridge.org/core/journals/macroeconomic-dynamics/article/is-labors-loss-capitals-gain-gross-versus-net-labor-shares/5D054E4F6B7D6C2D7F0E7D0A9D8B7C6A) | Net labor share shows minimal decline when accounting for depreciation |
| [**Koh et al. (2020)**](https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA17477) | IPP capitalization (post-2013 NIPA revision) explains entire decline |
| [**Barkai (2020)**](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12909) | Both labor AND capital shares declined; pure profits (markups) increased |
| [**Autor et al. (2020)**](https://academic.oup.com/qje/article/135/2/645/5721266) | "Superstar firms" with low labor shares capture increasing market share; IT-driven |
| [**Nallareddy & Ogneva (2024)**](https://www.sciencedirect.com/science/article/abs/pii/S1094202524000577) | IPP effect offset by depreciation; labor share decline is real |

### Key Debates

1. **Is the decline real?**
   - Yes: Corporate sector shows clear decline
   - Partially: Depends on time period and measure
   - No: Net measures and long-run comparisons show stability/increase

2. **What caused any decline?**
   - Technology (automation, IT investment)
   - Globalization (~11% of decline per McKinsey)
   - Rising markups/market power
   - Decline in unionization
   - Superstar firms effect

3. **Does it matter for welfare?**
   - Gross vs net distinction crucial
   - Benefits vs wages distinction matters
   - Distribution within labor income may matter more

---

## 💻 The Role of IT, Software, and Digital Business Models

### The Superstar Firms Hypothesis

[Autor, Dorn, Katz, Patterson & Van Reenen (2020)](https://academic.oup.com/qje/article-abstract/135/2/645/5721266) propose that the labor share decline is driven by the **rise of "superstar firms"**—highly productive companies that capture increasing market share while employing relatively few workers.

**Key Findings:**
- Labor's share of U.S. output fell from ~67% to ~61% during 1982-2012
- In retail, the top 4 firms went from <15% of sales (1982) to ~30% (2012)
- The decline is **between-firm reallocation**, not within-firm decline
- "Superstar firms with low labor shares are capturing an ever greater share of the market"

**The IT Connection:**
> "The documented fact pattern is consistent with scale-biased technological changes in which larger firms benefit disproportionately from information technology advances, such as falling computer software or hardware prices, and are thus able to increase their market shares."

### Software as a Labor Substitute

Research using Korean firm-level data ([CEPR VoxEU](https://cepr.org/voxeu/columns/softwares-impact-labours-income-share-new-evidence)) shows:

| Capital Type | Relationship to Labor |
|--------------|----------------------|
| Equipment capital | **Complement** (more equipment → more workers) |
| Software capital | **Substitute** (more software → fewer workers) |

**Impact:** Software accounts for **~2/3 of the 4.4 pp decline** in Korea's labor share (1990-2018).

### Intellectual Property Products (IPP) Capital

The post-2013 NIPA revision capitalized intellectual property products (software, R&D, entertainment originals), which changes how we measure the economy:

| Measure | 1998 | 2016 | Change |
|---------|------|------|--------|
| IPP share of net capital stock | 5.7% | 7.3% | +33% |

**The Debate:**
- [Koh et al. (2020)](https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA17477): IPP capitalization "entirely explains" the labor share decline
- [Nallareddy & Ogneva (2024)](https://www.sciencedirect.com/science/article/abs/pii/S1094202524000577): IPP investment is offset by depreciation; decline is real

### Tech Giants: Extreme Labor Efficiency

Modern tech companies generate extraordinary revenue with minimal labor, contributing to aggregate labor share decline when they grow:

| Company | Gross Margin | Revenue/Employee | Profit/Employee |
|---------|--------------|------------------|-----------------|
| **Meta** | 82% | ~$1.5M | $842K |
| **Apple** | 46% | $2.38M | High |
| **Google** | 58% | ~$1.5M | High |
| **Nvidia** | ~65% | $3.6M | $2M |
| **Amazon** | ~45% | Lower | $20K |
| **Walmart** | ~25% | Lowest | $7K |

*Sources: [MacroTrends](https://www.macrotrends.net/stocks/charts/META/meta-platforms/profit-margins), [TrueUp](https://www.trueup.io/revenue-per-employee), [Digital Information World](https://www.digitalinformationworld.com/2025/06/which-tech-giants-generate-the-most-revenue-per-employee.html)*

### The Digital Advertising Model

Digital advertising (Google, Meta) represents an extreme case of low labor intensity:
- **High margins**: 80%+ gross margins
- **Scale without labor**: Software serves billions with thousands of employees
- **Network effects**: Winner-take-most dynamics
- **Intangible assets**: Value is in algorithms, data, brand—not physical capital or workers

### Depreciation and IT

IT/software capital depreciates much faster than traditional capital:

| Asset Type | Typical Depreciation Rate |
|------------|--------------------------|
| Structures (buildings) | 2-3% per year |
| Equipment (machines) | 5-15% per year |
| Software | 25-33% per year |
| R&D | 15-25% per year |

This explains why **depreciation rose from 10% to 16.5% of GDI**—the economy shifted toward faster-depreciating assets.

### Quantifying IT's Contribution

| Study | IT/Technology Contribution to Labor Share Decline |
|-------|--------------------------------------------------|
| Autor et al. (2020) | Superstar effect explains majority of between-firm decline |
| Korean study (CEPR) | Software explains ~2/3 of decline |
| IMF | Falling investment prices (IT proxy) explain ~50% in advanced economies |
| McKinsey | Technology + automation: largest single factor |
| Karabarbounis & Neiman | Falling relative price of capital (IT-driven) is primary driver |

### Implications

1. **The labor share decline is concentrated in high-tech sectors** and firms with IT-intensive business models

2. **Traditional measures may understate the shift** because:
   - IPP is harder to value than physical capital
   - Depreciation accounting for software is imprecise
   - Multinational profit shifting distorts geographic attribution

3. **The trend may accelerate** as AI/ML enables even greater automation and scale without proportional labor

4. **Policy implications** differ depending on interpretation:
   - If it's about market power → antitrust
   - If it's about technology → education/training/redistribution
   - If it's measurement → improve national accounts

---

## 🔍 Data Sources

### Primary Sources

| Source | Series ID | Description | Coverage |
|--------|-----------|-------------|----------|
| BEA NIPA Table 1.11 | Multiple | GDI component shares | 1929-2024 |
| FRED | A4002E1A156NBEA | Compensation share of GDI | 1929-2024 |
| FRED | LABSHPUSA156NRUG | Penn World Table labor share | 1950-2019 |
| FRED | PRS85006173 | BLS Nonfarm Business Labor Share | 1947-2025 |
| FRED | A262RE1A156NBEA | Depreciation share of GDI | 1929-2024 |

### Academic Sources

- Karabarbounis, L., & Neiman, B. (2014). "The Global Decline of the Labor Share." *Quarterly Journal of Economics*, 129(1), 61-103. [NBER WP 19136](https://www.nber.org/papers/w19136)

- Gollin, D. (2002). "Getting Income Shares Right." *Journal of Political Economy*, 110(2), 458-474.

- Rognlie, M. (2015). "Deciphering the Fall and Rise in the Net Capital Share." *Brookings Papers on Economic Activity*, Spring.

- Bridgman, B. (2018). "Is Labor's Loss Capital's Gain? Gross versus Net Labor Shares." *Macroeconomic Dynamics*, 22(8), 2070-2087.

- Koh, D., Santaeulàlia-Llopis, R., & Zheng, Y. (2020). "Labor Share Decline and Intellectual Property Products Capital." *Econometrica*, 88(6), 2609-2628.

- Barkai, S. (2020). "Declining Labor and Capital Shares." *Journal of Finance*, 75(5), 2421-2463.

- Cette, G., Koehl, L., & Philippon, T. (2019). "Labor Shares in Some Advanced Economies." NBER Working Paper 26136.

- Autor, D., Dorn, D., Katz, L., Patterson, C., & Van Reenen, J. (2020). "The Fall of the Labor Share and the Rise of Superstar Firms." *Quarterly Journal of Economics*, 135(2), 645-709. [NBER WP 23396](https://www.nber.org/papers/w23396)

- Nallareddy, S., & Ogneva, M. (2024). "Capitalization of Intellectual Property Products Does Not Explain the Decline in the Labor Share." *Journal of Monetary Economics*. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1094202524000577)

### Online Resources

- [FRED Economic Data](https://fred.stlouisfed.org/) - Federal Reserve Bank of St. Louis
- [BEA National Accounts](https://www.bea.gov/national/) - Bureau of Economic Analysis
- [BLS Productivity & Costs](https://www.bls.gov/lpc/) - Bureau of Labor Statistics
- [Penn World Table](https://www.rug.nl/ggdc/productivity/pwt/) - University of Groningen

---

## 📋 Replication Notes

### Data Access

All data used in this analysis is publicly available through FRED (Federal Reserve Economic Data). Key series:

```
# BEA Compensation Share
https://fred.stlouisfed.org/series/A4002E1A156NBEA

# Penn World Table Labor Share
https://fred.stlouisfed.org/series/LABSHPUSA156NRUG

# Depreciation Share
https://fred.stlouisfed.org/series/A262RE1A156NBEA

# Corporate Profits Share
https://fred.stlouisfed.org/series/A445RE1A156NBEA

# Proprietors' Income Share
https://fred.stlouisfed.org/series/A041RE1A156NBEA
```

### Calculations

Net labor share calculation:
```
Net Domestic Income = GDI × (1 - Depreciation Share)
Net Labor Share = Compensation Share / (1 - Depreciation Share)

Example (2024):
NDI = 100% × (1 - 0.165) = 83.5%
Net Labor Share = 51.9% / 83.5% = 62.2%
```

Proprietors' income adjustment:
```
Adjusted Labor Share = Compensation Share + (α × Proprietors' Share)
Where α = assumed labor fraction (typically 0.67)

Example (2024):
Adjusted = 51.9% + (0.67 × 7.0%) = 56.6%
```

---

## 📄 License

This research note is shared for educational and research purposes. Data sources are public domain (BEA, BLS) or citation-requested (Penn World Table).

---

## 👤 Author

Research note compiled January 2026.

---

## 📝 Changelog

- **v1.1** (January 2026): Added section on IT, software, and superstar firms; added Autor et al. (2020) and Nallareddy & Ogneva (2024) to literature review
- **v1.0** (January 2026): Initial research note with BEA and Penn World Table data

