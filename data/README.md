# Data

Saved copies of every dataset the scripts use, so that the published numbers reproduce exactly. `python3 scripts/fetch_data.py` downloads them again; rerun the scripts afterwards and update the text.

| File | Source | Downloaded | Used by |
|---|---|---|---|
| `bea_nipa_extract.csv` | BEA NIPA annual bulk file, [NipaDataA.txt](https://apps.bea.gov/national/Release/TXT/NipaDataA.txt), dated 4 November 2026: every series the scripts read, in millions of current dollars, with BEA's series names | 9 Nov 2026 | all scripts |
| `pwt_labor_share.csv` | Penn World Table 11.0, `labsh` × 100, every country, from the publisher's archive ([DataverseNL, doi:10.34894/FABVLR](https://doi.org/10.34894/FABVLR)) | 9 Nov 2026 | Figure 1, Appendix B |
| `bls_nonfarm_labor_share.csv` | BLS labor share for all workers, nonfarm business sector, series PRS85006173, quarterly index (2017 = 100), from the [BLS public API](https://www.bls.gov/developers/) | 9 Nov 2026 | README sector scope, METHODOLOGY.md |
| `proprietors_income_split.csv` | Output of `scripts/proprietors_split.py`: labor's fraction of proprietors' income on Kravis's (1959) economy-wide basis, and the labor and capital parts of proprietors' income as % of GDI, 1929–2025 | | Figures 1 and 3, POST_TAX.md, AI_TRENDS.md, METHODOLOGY.md |
| `labor_share_measures.csv` | Output of `scripts/generate_chart.py`: the U.S. labor share measures and depreciation plotted in Figures 1 and 2, % of GDI (compensation also as % of net domestic income), 1970–2024 | | Figures 1 and 2 |
| `post_tax_labor_share.csv` | Output of `scripts/post_tax_labor_share.py` | | POST_TAX.md |
| `post_spending_shares.csv` | Output of `scripts/post_spending_shares.py`: labor and profit shares after taxes and government spending, with social benefits, public services, and grants, % of GDI, 1959–2025 | | POST_TAX.md |
| `ai_trend_projection.csv` | Output of `scripts/ai_trend_projection.py` | | AI_TRENDS.md |

`bea_raw/`, which git ignores, holds BEA's full bulk file after `fetch_data.py` downloads it.
