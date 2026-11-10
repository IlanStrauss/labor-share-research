# AI Scenario: Labor and Profit Shares in 2035

*Companion to the [main note](README.md), November 2026. Code: [`scripts/ai_trend_projection.py`](scripts/ai_trend_projection.py). Data: [`data/ai_trend_projection.csv`](data/ai_trend_projection.csv).*

If AI doubles the trend each share has followed since 2000, then by 2035 labor's share of GDI falls about 3 percentage points (pp) from 2025, and the profit share of GDI (profits after depreciation) rises about 4 to 4.5 pp, both before and after tax. These are mechanical extrapolations of a past trend, not forecasts.

| % of GDI | 2025 | 2035, AI scenario (90% interval) |
|---|---|---|
| Labor, pre-tax | 50.9 | 48.1 (47.2 to 49.1) |
| Labor, post-tax | 38.6 | 35.8 (35.1 to 36.5) |
| Profits after depreciation, pre-tax | 15.3 | 19.8 (17.8 to 21.8) |
| Profits after depreciation, post-tax | 11.8 | 15.7 (14.0 to 17.4) |

Post-tax means after payroll and income tax for labor, and after corporate and personal tax for profits, as in [POST_TAX.md](POST_TAX.md).

[![AI scenario: labor and profit shares to 2035](figures/ai_trend_capital_share.png)](figures/ai_trend_capital_share.png?raw=true)

*Click the figure to open it full size, or see the [PDF](figures/ai_trend_capital_share.pdf).*

---

## Method

Four shares, annual from 1970:

- **Labor share of GDI**: compensation over GDI, before tax and after payroll and income tax.
- **Profit share of GDI**: Figure 3's definition, corporate profits after depreciation (without IVA/CCAdj) plus the capital part of proprietors' income (proprietors' income is split each year in the same ratio as the rest of the economy's income, the "economy-wide basis" of Kravis 1959), over GDI, before tax and after corporate and personal tax.

The shares come from BEA's NIPA bulk file (4 November 2026), through 2025. Each share is projected separately:

```
S(t) = S(T) + m × b × (t − T)
```

- **S(t)**: projected share in year t, in %.
- **T**: the last data year, 2025.
- **S(T)**: the starting level, the smoothed share in year T. The smoother is LOESS, a moving local regression ([Cleveland 1979](https://doi.org/10.1080/01621459.1979.10481038)), with a window of 30% of the sample, about 16 years, so the start is free of the last year's cyclical swing.
- **b**: the trend, the OLS slope of the annual share on the year from 2000 to T, in pp a year. Its 90% interval uses Newey-West standard errors with 3 lags, which allow for persistence in the share from year to year.
- **m**: 2 in the AI scenario. With m = 1 the trend since 2000 simply continues; those values are in the CSV.

| Share | S(T), % | b, pp a year (90% interval) |
|---|---|---|
| Labor, pre-tax | 51.5 | −0.168 (−0.216 to −0.120) |
| Labor, post-tax | 39.0 | −0.159 (−0.193 to −0.124) |
| Profits after depreciation, pre-tax | 15.7 | 0.206 (0.105 to 0.307) |
| Profits after depreciation, post-tax | 12.0 | 0.183 (0.097 to 0.269) |

---

## Reading the Numbers

- The trend since 2000 is 1.4 to 2.0 times the trend since 1970 for every share, so the AI scenario moves each share 2.7 to 4.0 times as fast as its long-run pace.
- The 90% intervals cover uncertainty in the trend only, not year-to-year swings around it, so the range of plausible outcomes is wider.
- Labor and profit shares are projected separately, so their changes need not offset. The rest of GDI (depreciation, production taxes, rent, interest, and the labor part of proprietors' income) is not projected.
- The post-tax trends carry past tax changes forward, such as the 2017 cut in the corporate tax rate. Future tax changes would move the post-tax lines regardless of AI.

---

## Replication

```bash
python3 scripts/ai_trend_projection.py
```

Reads the data saved in [`data/`](data/) (sources in [`data/README.md`](data/README.md)) and prints every number cited above. Requires matplotlib, numpy, and statsmodels.

## References

- Cleveland, W. S. (1979). Robust locally weighted regression and smoothing scatterplots. *Journal of the American Statistical Association*, 74(368), 829–836.
- Kravis, I. B. (1959). Relative income shares in fact and theory. *American Economic Review*, 49(5), 917–949.
- Newey, W. K., and West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.
