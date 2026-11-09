# AI Scenario: Labor and Profit Shares in 2035

*Companion to the [main note](README.md), November 2026. Code: [`scripts/ai_trend_projection.py`](scripts/ai_trend_projection.py). Data: [`data/ai_trend_projection.csv`](data/ai_trend_projection.csv).*

If AI doubles the trend each share has followed since 2000, then by 2035 labor's share of GDI falls about 3 percentage points (pp) from 2025, and the profit share of GDI (profits after depreciation) rises about 4 pp, both before and after tax. These are mechanical extrapolations of a past trend, not forecasts.

| % of GDI | 2025 | 2035, AI scenario (90% interval) |
|---|---|---|
| Labor, pre-tax | 50.9 | 48.1 (47.2 to 49.1) |
| Labor, post-tax | 38.6 | 35.8 (35.1 to 36.5) |
| Profits after depreciation, pre-tax | 15.7 | 19.9 (17.9 to 21.8) |
| Profits after depreciation, post-tax | 12.1 | 15.7 (14.0 to 17.4) |

Post-tax means after payroll and income tax for labor, and after corporate and personal tax for profits, as in [POST_TAX.md](POST_TAX.md). The US non-housing business-sector profit share from [business-profit-share](https://github.com/IlanStrauss/business-profit-share) reaches 46.6% of business value added in 2035 on the doubled trend (like our GDI profit shares, it leaves out owner-occupiers' imputed rents; it sits far above them mainly because it counts depreciation as profit, while they deduct it).

[![AI scenario: labor and profit shares to 2035](figures/ai_trend_capital_share.png)](figures/ai_trend_capital_share.png?raw=true)

*Click the figure to open it full size, or see the [PDF](figures/ai_trend_capital_share.pdf).*

---

## Method

Five shares, annual from 1970:

- **Labor share of GDI**: compensation over GDI, before tax and after payroll and income tax.
- **Profit share of GDI**: Figure 3's definition, corporate profits after depreciation (without IVA/CCAdj) plus one third of proprietors' income, over GDI, before tax and after corporate and personal tax.
- **Non-housing business-sector profit share**: 100 minus the labor share of US business value added, with the self-employed paid what employees earn, following [Gutiérrez and Piton (2020)](https://doi.org/10.1257/aeri.20190285). Business value added excludes real estate, which holds owner-occupied housing and its imputed rents, as well as agriculture, public administration, education, and health. Depreciation counts as profit here. The series is `ps_wide` from business-profit-share (commit `6de05be`), through 2023, saved in [`data/business_profit_share_usa.csv`](data/business_profit_share_usa.csv).

The GDI shares come from BEA's NIPA bulk file (4 November 2026), through 2025. Each share is projected separately:

```
S(t) = S(T) + m × b × (t − T)
```

- **S(t)**: projected share in year t, in %.
- **T**: the last data year, 2025 (2023 for the business sector).
- **S(T)**: the starting level, the smoothed share in year T. The smoother is LOESS, a moving local regression ([Cleveland 1979](https://doi.org/10.1080/01621459.1979.10481038)), with a window of 30% of the sample, about 16 years, so the start is free of the last year's cyclical swing.
- **b**: the trend, the OLS slope of the annual share on the year from 2000 to T, in pp a year. Its 90% interval uses Newey-West standard errors with 3 lags, which allow for persistence in the share from year to year.
- **m**: 2 in the AI scenario. With m = 1 the trend since 2000 simply continues; those values are in the CSV.

| Share | S(T), % | b, pp a year (90% interval) |
|---|---|---|
| Labor, pre-tax | 51.5 | −0.168 (−0.216 to −0.120) |
| Labor, post-tax | 39.0 | −0.159 (−0.193 to −0.124) |
| Profits after depreciation, pre-tax | 16.1 | 0.188 (0.090 to 0.285) |
| Profits after depreciation, post-tax | 12.4 | 0.167 (0.083 to 0.252) |
| Non-housing business sector, profits before depreciation | 39.4 | 0.300 (0.197 to 0.404) |

---

## Reading the Numbers

- The trend since 2000 is 1.4 to 1.9 times the trend since 1970 for every share, so the AI scenario moves each share three to four times as fast as its long-run pace.
- The 90% intervals cover uncertainty in the trend only, not year-to-year swings around it, so the range of plausible outcomes is wider.
- Labor and profit shares are projected separately, so their changes need not offset. The rest of GDI (depreciation, production taxes, rent, interest, and two thirds of proprietors' income) is not projected.
- The post-tax trends carry past tax changes forward, such as the 2017 cut in the corporate tax rate. Future tax changes would move the post-tax lines regardless of AI.
- The non-housing business-sector share sits far above the GDI shares mainly because it counts all business income other than labor compensation as profit, including depreciation and net interest, and because its denominator leaves out government, education, and health, where labor takes most of value added. Since depreciation counts as profit, rising depreciation lifts this share, while the GDI profit shares are after depreciation. Leaving out housing works the other way: real estate's value added is almost all capital income, so including it would raise the share.

---

## Replication

```bash
python3 scripts/ai_trend_projection.py
```

Reads the data saved in [`data/`](data/) (sources in [`data/README.md`](data/README.md)) and prints every number cited above. Requires matplotlib, numpy, and statsmodels.

## References

- Cleveland, W. S. (1979). Robust locally weighted regression and smoothing scatterplots. *Journal of the American Statistical Association*, 74(368), 829–836.
- Gollin, D. (2002). Getting income shares right. *Journal of Political Economy*, 110(2), 458–474.
- Gutiérrez, G., and Piton, S. (2020). Revisiting the global decline of the (non-housing) labor share. *American Economic Review: Insights*, 2(3), 321–338.
- Newey, W. K., and West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.
- Strauss, I. (2026). Business-sector profit shares, 45 countries, 1970–2025. https://github.com/IlanStrauss/business-profit-share
