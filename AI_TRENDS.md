# AI Scenario: Profit Shares in 2035 and 2050

*Companion to the [main note](README.md), November 2026. Code: [`scripts/ai_trend_projection.py`](scripts/ai_trend_projection.py). Data: [`data/ai_trend_projection.csv`](data/ai_trend_projection.csv).*

If AI doubles the trend since 2000, the pre-tax profit share of GDI reaches 19.9% by 2035 and 25.5% by 2050, against 18.0% and 20.8% if the trend since 2000 simply continues. After corporate tax, the doubled trend gives 17.9% by 2035 and 23.7% by 2050, against 15.9% and 18.8%. The US business-sector profit share from [business-profit-share](https://github.com/IlanStrauss/business-profit-share) reaches 46.6% by 2035 and 55.6% by 2050 on the doubled trend, against 43.0% and 47.5% (it sits far above the GDI shares mainly because it counts depreciation as profit, while they deduct it). These are mechanical extrapolations of a past trend, not forecasts.

![AI scenario for profit shares](figures/ai_trend_capital_share.png)

---

## Method

Three shares, annual from 1970:

- **Profit share of GDI**, Figure 3's definition: corporate profits (without IVA/CCAdj) plus one third of proprietors' income, divided by GDI, before tax and after corporate tax. From BEA's NIPA bulk file (dated 4 November 2026), through 2025.
- **Business-sector profit share**: 100 minus the labor share of US business value added, with the self-employed paid what employees earn, following [Gutiérrez and Piton (2020)](https://doi.org/10.1257/aeri.20190285). Business value added excludes agriculture, real estate (which holds owner-occupied housing), public administration, education, and health. It is a gross measure: depreciation counts as profit. The series is `ps_wide` from [business-profit-share](https://github.com/IlanStrauss/business-profit-share) (commit `6de05be`), through 2023.

```
S(t) = S(T) + m × b × (t − T)
```

- **S(t)**: projected share in year t, in %.
- **T**: the last data year, 2025 for the GDI shares and 2023 for the business-sector share.
- **S(T)**: the smoothed share in year T, which is the starting level: 16.1% pre-tax, 14.0% after corporate tax, and 39.4% for the business sector. The actual values are 15.7%, 13.6%, and 41.1%.
- **b**: the trend, measured as the OLS slope of the annual share on the year from 2000 to T, in percentage points (pp) a year. It is 0.188 pre-tax (90% interval 0.090 to 0.285), 0.195 after corporate tax (0.114 to 0.276), and 0.300 for the business sector (0.197 to 0.404). The intervals use Newey-West standard errors with 3 lags, which allow for some persistence in the share from year to year.
- **m**: 1 for the trend since 2000, 2 for the AI scenario.

The smoother is LOESS, a moving local regression ([Cleveland 1979](https://doi.org/10.1080/01621459.1979.10481038)), with a window of 30% of the sample, about 16 years. It sets the starting level without the last year's cyclical swing. The trend b comes from the raw annual data.

---

## Reading the Numbers

- The trend since 2000 is about twice the 1970–2025 trend: 0.19 against 0.10 pp a year pre-tax, 0.20 against 0.12 after corporate tax, and 0.30 against 0.17 for the business sector (1970–2023). The AI scenario therefore runs at about four times the long-run pace.
- The 90% intervals for 2050 under the AI scenario run from 20.6% to 30.4% pre-tax, 19.7% to 27.8% after corporate tax, and 50.0% to 61.2% for the business sector. They cover uncertainty in the trend only, not year-to-year shocks around it, so the range of plausible outcomes is wider.
- The business-sector share sits far above the GDI shares mainly because it counts all business income other than labor compensation as profit, including depreciation and net interest, and because its denominator leaves out government, education, and health, where labor takes most of value added. Since depreciation counts as profit, rising depreciation lifts this share, while the GDI shares measure profits after depreciation.
- The after-tax trend includes the past fall in corporate tax as a share of GDI. Future tax changes would move the after-tax line regardless of AI.
- Labor's share is not projected.

---

## Replication

```bash
python3 scripts/ai_trend_projection.py
```

Uses the same BEA bulk file as [`POST_TAX.md`](POST_TAX.md), downloads the business-sector series from business-profit-share at a fixed commit, and prints every number cited above. Requires matplotlib, numpy, and statsmodels.

## References

- Cleveland, W. S. (1979). Robust locally weighted regression and smoothing scatterplots. *Journal of the American Statistical Association*, 74(368), 829–836.
- Gollin, D. (2002). Getting income shares right. *Journal of Political Economy*, 110(2), 458–474.
- Gutiérrez, G., and Piton, S. (2020). Revisiting the global decline of the (non-housing) labor share. *American Economic Review: Insights*, 2(3), 321–338.
- Newey, W. K., and West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.
- Strauss, I. (2026). Business-sector profit shares, 45 countries, 1970–2025. https://github.com/IlanStrauss/business-profit-share
