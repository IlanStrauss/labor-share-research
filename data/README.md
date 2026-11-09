# Data

Saved copies of every dataset the scripts use, so that the published numbers reproduce exactly. `python3 scripts/fetch_data.py` downloads them again; rerun the scripts afterwards and update the text.

| File | Source | Downloaded | Used by |
|---|---|---|---|
| `bea_nipa_extract.csv` | BEA NIPA annual bulk file, [NipaDataA.txt](https://apps.bea.gov/national/Release/TXT/NipaDataA.txt), dated 4 November 2026: every series the scripts read, in millions of current dollars, with BEA's series names | 9 Nov 2026 | all scripts |
| `pwt_labor_share.csv` | Penn World Table 11.0, `labsh` × 100, every country, from the publisher's archive ([DataverseNL, doi:10.34894/FABVLR](https://doi.org/10.34894/FABVLR)) | 9 Nov 2026 | Figure 1, Appendix B |
| `bls_nonfarm_labor_share.csv` | BLS labor share for all workers, nonfarm business sector, series PRS85006173, quarterly index (2017 = 100), from the [BLS public API](https://www.bls.gov/developers/) | 9 Nov 2026 | README sector scope |
| `business_profit_share_usa.csv` | US rows of `data/processed/profit_share_extended.csv` in [business-profit-share](https://github.com/IlanStrauss/business-profit-share), commit `6de05be` | 9 Nov 2026 | AI scenario |
| `post_tax_labor_share.csv` | Output of `scripts/post_tax_labor_share.py` | | POST_TAX.md |
| `ai_trend_projection.csv` | Output of `scripts/ai_trend_projection.py` | | AI_TRENDS.md |

`bea_raw/`, which git ignores, holds BEA's full bulk file after `fetch_data.py` downloads it.
