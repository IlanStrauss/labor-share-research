"""
Print every number README.md and METHODOLOGY.md cite, from the data saved in data/.

Run:  python3 scripts/readme_numbers.py

POST_TAX.md and AI_TRENDS.md numbers are printed by post_tax_labor_share.py and
ai_trend_projection.py. All shares are % of gross domestic income (GDI) unless stated.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import ROOT, load  # noqa: E402
from proprietors_split import capital_part, labor_fraction, labor_part  # noqa: E402

A, B = 1970, 2024
d = load()


def gdi(code, y):
    return 100 * d[code][y] / d['A261RC'][y]


def ndi(y):
    return d['A261RC'][y] - d['A262RC'][y]


def kp(y):
    # Capital part of proprietors' income, economy-wide split (proprietors_split.py)
    return capital_part(d, y)


MEASURES = {
    'Labor share (compensation / GDI)': lambda y: gdi('A4002C', y),
    'Profit share, pre-tax (after depreciation)': lambda y: 100 * (d['A053RC'][y] + kp(y)) / d['A261RC'][y],
    'Profit share, post-tax (after depreciation)': lambda y: 100 * (d['A055RC'][y] + kp(y)) / d['A261RC'][y],
    'Depreciation': lambda y: gdi('A262RC', y),
    'Net operating surplus': lambda y: gdi('W271RC', y),
    'Taxes on production and imports less subsidies': lambda y: gdi('W056RC', y) - gdi('A107RC', y),
    'Labor share of NDI (compensation / NDI)': lambda y: 100 * d['A4002C'][y] / ndi(y),
    'Wages only (wages and salaries / GDI)': lambda y: gdi('A4102C', y),
    'Adjusted (compensation + labor part of proprietors)': lambda y: gdi('A4002C', y) + 100 * labor_part(d, y) / d['A261RC'][y],
    'Profits / NDI, pre-tax': lambda y: 100 * (d['A053RC'][y] + kp(y)) / ndi(y),
    'Profits / NDI, post-tax': lambda y: 100 * (d['A055RC'][y] + kp(y)) / ndi(y),
}


def section(title):
    print(f"\n{title}")


def main():
    section(f"Key Findings table, figures, and text ({A} and {B}; change computed from unrounded data)")
    print(f"  {'':52s}{A:>8d}{B:>8d}{'pp':>8s}{'%':>7s}")
    v = {}
    for name, f in MEASURES.items():
        a, b = f(A), f(B)
        v[name] = (a, b)
        print(f"  {name:52s}{a:8.1f}{b:8.1f}{b - a:+8.1f}{100 * (b / a - 1):+6.0f}%")

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

    section("Proprietors' income split: economy-wide basis, against the earlier two-thirds rule")
    print(f"  labor fraction of proprietors' income: {100 * labor_fraction(d, A):.1f}% ({A}), "
          f"{100 * labor_fraction(d, B):.1f}% ({B})")
    old = {
        'Adjusted (compensation + labor part of proprietors)': lambda y: gdi('A4002C', y) + 2 * gdi('A041RC', y) / 3,
        'Profit share, pre-tax (after depreciation)': lambda y: gdi('A053RC', y) + gdi('A041RC', y) / 3,
        'Profit share, post-tax (after depreciation)': lambda y: gdi('A055RC', y) + gdi('A041RC', y) / 3,
    }
    for name, f in old.items():
        print(f"  {name}: two-thirds rule {f(A):.1f} -> {f(B):.1f} ({f(B) - f(A):+.1f} pp); "
              f"economy-wide {v[name][0]:.1f} -> {v[name][1]:.1f} ({v[name][1] - v[name][0]:+.1f} pp)")

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
    qv = {(y, p): x for y, p, x in q}
    print(f"  quarterly: {A}Q1 {qv[(A, 'Q01')]:.1f}, {B}Q4 {qv[(B, 'Q04')]:.1f}, latest {q[-1][0]}{q[-1][1]} {q[-1][2]:.1f}")
    lab = v['Labor share (compensation / GDI)']
    print(f"  whole economy, compensation / GDI: {100 * (lab[1] / lab[0] - 1):.1f}%")

    comp, prop, th = gdi('A4002C', B), gdi('A041RC', B), labor_fraction(d, B)
    section(f"METHODOLOGY.md: proprietors' income, {B}")
    print(f"  proprietors' income {prop:.1f}%; labor fraction {100 * th:.1f}%; labor part {th * prop:.1f}%; "
          f"compensation {comp:.1f}%; adjusted (compensation + labor part) {comp + th * prop:.1f}%")
    print(f"  against the adjusted share: none to labor {-th * prop:+.1f} pp, all to labor {(1 - th) * prop:+.1f} pp; "
          f"against compensation alone: all to labor {prop:+.1f} pp")

    section(f"METHODOLOGY.md: GDI by component ({A} and {B})")
    nos_parts = ('A041RC', 'A445RC', 'A048RC', 'W272RC')
    rows = [
        ('Compensation of employees', lambda y: gdi('A4002C', y)),
        ('  Wages and salaries', lambda y: gdi('A4102C', y)),
        ('  Wages and benefits (less employer social insurance)', lambda y: gdi('A4002C', y) - gdi('B039RC', y)),
        ('  Supplements', lambda y: gdi('A4002C', y) - gdi('A4102C', y)),
        ('    Employer contributions, pension and insurance funds', lambda y: gdi('B040RC', y)),
        ('    Employer contributions, government social insurance', lambda y: gdi('B039RC', y)),
        ("Proprietors' income", lambda y: gdi('A041RC', y)),
        ('Corporate profits with IVA and CCAdj, domestic', lambda y: gdi('A445RC', y)),
        ('Rental income of persons', lambda y: gdi('A048RC', y)),
        ('Net interest, domestic industries', lambda y: gdi('W272RC', y)),
        ('Rest of net operating surplus', lambda y: gdi('W271RC', y) - sum(gdi(c, y) for c in nos_parts)),
        ('Depreciation', lambda y: gdi('A262RC', y)),
        ('Taxes on production and imports less subsidies', lambda y: gdi('W056RC', y) - gdi('A107RC', y)),
    ]
    for name, f in rows:
        print(f"  {name:56s}{f(A):8.1f}{f(B):8.1f}{f(B) - f(A):+8.1f}")
    top = [0, 6, 7, 8, 9, 10, 11, 12]
    for y in (A, B):
        print(f"  {y}: top-level rows sum to {sum(rows[i][1](y) for i in top):.2f}; supplements less the two "
              f"employer contributions {round(rows[3][1](y) - rows[4][1](y) - rows[5][1](y), 2) + 0.0:+.2f}")

    section(f"METHODOLOGY.md: net domestic income (NDI), {B} worked example")
    net = 100 - gdi('A262RC', B)
    print(f"  NDI {net:.1f}% of GDI; compensation / NDI {100 * comp / net:.1f}%; net operating surplus "
          f"{gdi('W271RC', B):.1f}% of GDI = {100 * gdi('W271RC', B) / net:.1f}% of NDI")
    nd, gd = v['Labor share of NDI (compensation / NDI)'], v['Labor share (compensation / GDI)']
    print(f"  {A}-{B}: NDI labor share {nd[1] - nd[0]:+.1f} pp, GDI labor share {gd[1] - gd[0]:+.1f} pp "
          f"(the NDI fall is {100 * (1 - (nd[1] - nd[0]) / (gd[1] - gd[0])):.0f}% smaller)")
    wages = v['Wages only (wages and salaries / GDI)']
    print(f"  wages-only fall is {100 * ((wages[1] - wages[0]) / (gd[1] - gd[0]) - 1):.0f}% larger than compensation's")
    share = lambda y: d['A4002C'][y] / d['A261RC'][y]
    print(f"  highest compensation / GDI since {min(d['A4002C'])}: {max(d['A4002C'], key=share)}")

    section("METHODOLOGY.md: general government")
    for y in (A, B):
        print(f"  {y}: value added {100 * d['A765RC'][y] / d['A191RC'][y]:.1f}% of GDP; compensation "
              f"{100 * d['A194RC'][y] / d['A765RC'][y]:.1f}% and depreciation {100 * d['A265RC'][y] / d['A765RC'][y]:.1f}% "
              f"of its value added; housing value added {100 * d['A2009C'][y] / d['A191RC'][y]:.1f}% of GDP")
        rest = 100 * (d['A4002C'][y] - d['A194RC'][y]) / (d['A261RC'][y] - d['A765RC'][y] - d['A2009C'][y])
        print(f"        compensation outside general government / GDI less government and housing value added: {rest:.1f}%")


if __name__ == '__main__':
    main()
