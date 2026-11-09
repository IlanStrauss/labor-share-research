# Labor's Share Before and After Tax

*Companion to the [main note](README.md), November 2026. Code: [`scripts/post_tax_labor_share.py`](scripts/post_tax_labor_share.py). Data: [`data/post_tax_labor_share.csv`](data/post_tax_labor_share.csv).*

After payroll and income taxes, labor's share of gross domestic income (GDI) fell from 47.6% in 1970 to 39.4% in 2024, a fall of 8.2 percentage points (pp), against 6.9 pp before tax. Taxes add 1.3 pp to the fall: payroll taxes rose from 4.0% to 5.7% of GDI, while income tax on wages fell slightly. Over the same years the profit share of GDI (profits after depreciation) rose 5.6 pp before tax and 5.5 pp after tax.

[![Labor and profit shares before and after tax](figures/labor_share_post_tax.png)](figures/labor_share_post_tax.png?raw=true)

*Click the figure to open it full size, or see the [PDF](figures/labor_share_post_tax.pdf).*

---

## Results, 1970 and 2024

| % of GDI | 1970 | 2024 | Change (pp) |
|---|---|---|---|
| Labor, pre-tax | 58.4 | 51.4 | −6.9 |
| Labor, post-tax (after payroll and income tax) | 47.6 | 39.4 | −8.2 |
| Profits after depreciation, pre-tax | 10.5 | 16.2 | +5.6 |
| Profits after depreciation, post-tax (after corporate and personal tax) | 7.0 | 12.5 | +5.5 |

Changes are computed from unrounded data. As a share of labor and profit income together, profits rose from 15.3% to 23.9% before tax and from 12.8% to 24.1% after tax. Post-tax profits rose slightly less than pre-tax profits because personal income tax on dividends rose by more than corporate income tax fell.

---

## Definitions

All measures divide by GDI, as in Figures 1 to 3 of the main note.

```
Pre-tax labor share  = Compensation / GDI
Post-tax labor share = (Compensation − Payroll taxes − Income tax on wages) / GDI
Income tax on wages  = τ × Wages and salaries
τ = Personal income taxes / (Wages + Proprietors' income + Rental income + Interest + Dividends)
```

- **Compensation**: compensation of employees, which includes wages, salaries, employer-paid benefits, and employer contributions for social insurance (BEA Table 1.10). This is the numerator of the main note's headline labor share.
- **Payroll taxes**: employer and employee contributions for government social insurance, mainly Social Security and Medicare, plus unemployment insurance and railroad retirement (BEA Table 3.6). Employer contributions also include small insurance-type items such as workers' compensation and pension-guaranty premiums, about 0.1% of GDI. We exclude contributions by the self-employed, whose income is not in compensation, and Medicare supplementary medical insurance premiums, which enrollees (mostly people aged 65 and over) pay.
- **τ**: the average income tax rate on household income, following [Mendoza, Razin and Tesar (1994)](https://doi.org/10.1016/0304-3932(94)90021-3), a widely used method for splitting personal income tax between labor and capital income in national accounts. Personal income taxes are federal plus state and local income taxes paid by persons (BEA Table 3.4); the denominator is household income from BEA Table 2.1. τ was 13.0% in 1970 and 14.9% in 2024.

For profits we use Figure 3's definition: corporate profits after depreciation (without IVA/CCAdj, BEA Table 1.12) plus one third of proprietors' income, over GDI. Post-tax profits subtract corporate income tax and τ times dividends received by persons and one third of proprietors' income, so profits carry the same average household income tax rate that wages carry. Figure 3 of the main note subtracts corporate income tax only.

---

## What This Does Not Count

Taxes pay for spending, and none of it is added back here. Payroll taxes fund Social Security and Medicare. Social Security benefits rise with a worker's own covered earnings, and Medicare eligibility depends on years of covered work, so workers get something back for these taxes. Payroll taxes that buy benefits workers value act less like a tax and more like part of pay (Summers 1989). Treating them that way, and subtracting only income tax on wages, labor's share fell 6.5 pp, slightly less than the 6.9 pp pre-tax decline. The steeper after-tax decline therefore rests on counting payroll taxes as a pure tax.

Other transfers and public services are not counted either. Allocating them requires distributional national accounts, which assign taxes and government spending to individuals rather than to labor and capital income ([Piketty, Saez and Zucman 2018](https://doi.org/10.1093/qje/qjx043)).

---

## Robustness and Data Notes

- **Capital gains tax.** τ spreads all personal income tax, including tax on realized capital gains, across wages and capital income, so some capital gains tax lands on wages. Removing the Treasury's figures for taxes on capital gains ([Office of Tax Analysis, 2016](https://home.treasury.gov/system/files/131/Taxes-Paid-on-Capital-Gains-for-Returns-with-Positive-Net-Capital-Gains-12202016.pdf), available for 1954–2014) raises the post-tax labor share by 0.2 pp in 1970 and by up to 0.8 pp in later years. The 1970–2024 after-tax decline would then be about 7.6 to 8.0 pp rather than 8.2 pp, still steeper than the pre-tax decline.
- **Data vintage.** All numbers come from BEA's NIPA bulk file dated 4 November 2026.

---

## Replication

```bash
python3 scripts/post_tax_labor_share.py
```

The script reads BEA's data from [`data/bea_nipa_extract.csv`](data/bea_nipa_extract.csv) (sources in [`data/README.md`](data/README.md)) and prints every number cited above. Requires matplotlib.

## References

- Gollin, D. (2002). Getting income shares right. *Journal of Political Economy*, 110(2), 458–474.
- Mendoza, E. G., Razin, A., and Tesar, L. L. (1994). Effective tax rates in macroeconomics: Cross-country estimates of tax rates on factor incomes and consumption. *Journal of Monetary Economics*, 34(3), 297–323.
- Piketty, T., Saez, E., and Zucman, G. (2018). Distributional national accounts: Methods and estimates for the United States. *Quarterly Journal of Economics*, 133(2), 553–609.
- Summers, L. H. (1989). Some simple economics of mandated benefits. *American Economic Review*, 79(2), 177–183.
- U.S. Department of the Treasury, Office of Tax Analysis (2016). Taxes paid on capital gains for returns with positive net capital gains, 1954–2014.
