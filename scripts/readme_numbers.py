"""
Print every number the README cites, from the data saved in data/.

Run:  python3 scripts/readme_numbers.py

POST_TAX.md and AI_TRENDS.md numbers are printed by post_tax_labor_share.py and
ai_trend_projection.py. All shares are % of gross domestic income (GDI) unless stated.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import ROOT, load  # noqa: E402

A, B = 1970, 2024
d = load()


def gdi(code, y):
    return 100 * d[code][y] / d['A261RC'][y]


def ndi(y):
    return d['A261RC'][y] - d['A262RC'][y]


MEASURES = {
    'Labor share (compensation / GDI)': lambda y: gdi('A4002C', y),
    'Profit share, pre-tax (after depreciation)': lambda y: gdi('A053RC', y) + gdi('A041RC', y) / 3,
    'Profit share, post-tax (after depreciation)': lambda y: gdi('A055RC', y) + gdi('A041RC', y) / 3,
    'Depreciation': lambda y: gdi('A262RC', y),
    'Net operating surplus': lambda y: gdi('W271RC', y),
    'Taxes on production and imports less subsidies': lambda y: gdi('W056RC', y) - gdi('A107RC', y),
    'Labor share of NDI (compensation / NDI)': lambda y: 100 * d['A4002C'][y] / ndi(y),
    'Wages only (wages and salaries / GDI)': lambda y: gdi('W270RC', y),
    'Profits / NDI, pre-tax': lambda y: 100 * (d['A053RC'][y] + d['A041RC'][y] / 3) / ndi(y),
    'Profits / NDI, post-tax': lambda y: 100 * (d['A055RC'][y] + d['A041RC'][y] / 3) / ndi(y),
}


def section(title):
    print(f"\n{title}")


def main():
    section(f"Key Findings table, figures, and text ({A} and {B}; change computed from unrounded data)")
    print(f"  {'':48s}{A:>8d}{B:>8d}{'pp':>8s}{'%':>7s}")
    v = {}
    for name, f in MEASURES.items():
        a, b = f(A), f(B)
        v[name] = (a, b)
        print(f"  {name:48s}{a:8.1f}{b:8.1f}{b - a:+8.1f}{100 * (b / a - 1):+6.0f}%")

    dl = v['Labor share (compensation / GDI)'][1] - v['Labor share (compensation / GDI)'][0]
    dcfc = v['Depreciation'][1] - v['Depreciation'][0]
    dnos = v['Net operating surplus'][1] - v['Net operating surplus'][0]
    dtax = (v['Taxes on production and imports less subsidies'][1]
            - v['Taxes on production and imports less subsidies'][0])
    section("Key takeaway: GDI split of labor's fall (the three changes sum to minus labor's change)")
    print(f"  labor {dl:+.2f} | depreciation {dcfc:+.2f}, net operating surplus {dnos:+.2f}, "
          f"production taxes less subsidies {dtax:+.2f} (sum {dcfc + dnos + dtax:+.2f})")
    print(f"  depreciation's rise = {100 * dcfc / -dl:.0f}% of labor's fall")
    post = v['Profits / NDI, post-tax']
    print(f"  post-tax profits / NDI rose {post[1] - post[0]:+.1f} pp")

    section(f"Definitions and compensation, {B}")
    print(f"  rental income of persons {gdi('A048RC', B):.1f}%; net interest and miscellaneous payments "
          f"(national) {gdi('W255RC', B):.1f}%")
    print(f"  employer contributions: pension and insurance funds {gdi('B040RC', B):.1f}%, "
          f"government social insurance {gdi('B039RC', B):.1f}%")

    section("Figure 4: depreciation")
    ipp = gdi('Y083RC', B) - gdi('Y083RC', A)
    print(f"  software, R&D, and other IP: {gdi('Y083RC', A):.1f} -> {gdi('Y083RC', B):.1f} ({ipp:+.1f} pp of {dcfc:+.1f})")
    for y in (A, B):
        econ = gdi('A438RC', y)
        tax = econ + gdi('A059RC', y)
        print(f"  {y}: corporate depreciation for tax {tax:.1f}%, economic {econ:.1f}% "
              f"(capital consumption adjustment {gdi('A059RC', y):+.1f})")
    print(f"  on BEA's economic depreciation, the rise in corporate profits since {A} would be "
          f"{gdi('A059RC', A) - gdi('A059RC', B):.1f} pp smaller")

    with open(os.path.join(ROOT, 'data', 'pwt_labor_share.csv'), newline='') as f:
        pwt = {(r['iso3c'], int(r['year'])): (r['country'], float(r['labor_share_pct'])) for r in csv.DictReader(f)}
    last = max(y for c, y in pwt if c == 'USA')
    section(f"Figure 1 and Appendix B: Penn World Table 11.0 labor share, {last}")
    g7 = ['CAN', 'DEU', 'FRA', 'GBR', 'ITA', 'JPN', 'USA', 'KOR']
    for c in sorted(g7, key=lambda c: -pwt[(c, last)][1]):
        print(f"  {pwt[(c, last)][0]:16s}{pwt[(c, last)][1]:6.1f}%")
    lower = sorted((v_, n) for (c, y), (n, v_) in pwt.items() if y == last and v_ < pwt[('USA', last)][1])
    print(f"  {len(lower)} of {sum(1 for c, y in pwt if y == last)} countries are below the US in {last}")

    with open(os.path.join(ROOT, 'data', 'bls_nonfarm_labor_share.csv'), newline='') as f:
        q = [(int(r['year']), r['period'], float(r['index_2017_100'])) for r in csv.DictReader(f)]
    annual = {}
    for y, _, x in q:
        annual.setdefault(y, []).append(x)
    annual = {y: sum(x) / len(x) for y, x in annual.items() if len(x) == 4}
    peak = max((y for y in annual if 1970 <= y <= 1975), key=annual.get)
    section("Sector scope: BLS nonfarm business labor share (index, 2017 = 100, annual averages)")
    print(f"  early-1970s peak {peak}: {annual[peak]:.1f}; {B}: {annual[B]:.1f}; change {100 * (annual[B] / annual[peak] - 1):.1f}%")


if __name__ == '__main__':
    main()
