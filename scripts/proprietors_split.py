"""
Split of proprietors' income between labor and capital, on Kravis's (1959) economy-wide basis:
each year, proprietors' income is divided in the same ratio as the rest of the economy's net
income, that is, compensation of employees against net operating surplus other than
proprietors' income (corporate profits, rental income, net interest, business transfer
payments, and the current surplus of government enterprises). BEA series codes in brackets.

    labor fraction = compensation [A4002C]
                     / (compensation + net operating surplus - proprietors' income [A041RC])

Net operating surplus is GDI [A261RC] less compensation, taxes on production and imports
[W056RC] less subsidies [A107RC], and depreciation [A262RC]. BEA's own series [W271RC] starts
in 1959 and matches this to within $4 million in every year.

The labor part of proprietors' income [A041RC] is the labor fraction times proprietors' income,
and the capital part is the rest. Elsby, Hobijn and Sahin (2013) compare this measure with the
BLS method, which pays the self-employed what employees earn.

Run:  python3 scripts/proprietors_split.py
Writes data/proprietors_income_split.csv.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import ROOT, load  # noqa: E402


def net_operating_surplus(d, y):
    return d['A261RC'][y] - d['A4002C'][y] - d['W056RC'][y] + d['A107RC'][y] - d['A262RC'][y]


def labor_fraction(d, y):
    comp, prop = d['A4002C'][y], d['A041RC'][y]
    return comp / (comp + net_operating_surplus(d, y) - prop)


def labor_part(d, y):
    return labor_fraction(d, y) * d['A041RC'][y]


def capital_part(d, y):
    return (1 - labor_fraction(d, y)) * d['A041RC'][y]


def main():
    d = load()
    years = sorted(set.intersection(*(set(d[c]) for c in ('A261RC', 'A4002C', 'A041RC', 'W056RC', 'A107RC', 'A262RC'))))
    assert max(abs(net_operating_surplus(d, y) - d['W271RC'][y]) for y in d['W271RC']) <= 5
    with open(os.path.join(ROOT, 'data', 'proprietors_income_split.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['year', 'labor_fraction_pct', 'proprietors_income_pct_gdi',
                    'labor_part_pct_gdi', 'capital_part_pct_gdi'])
        for y in years:
            gdi = d['A261RC'][y]
            w.writerow([y, round(100 * labor_fraction(d, y), 3), round(100 * d['A041RC'][y] / gdi, 3),
                        round(100 * labor_part(d, y) / gdi, 3), round(100 * capital_part(d, y) / gdi, 3)])
    share = {y: 100 * labor_fraction(d, y) for y in years}
    print(f"Labor fraction of proprietors' income: {share[1970]:.1f}% (1970), {share[2024]:.1f}% (2024); "
          f"range {min(share.values()):.1f}% ({min(share, key=share.get)}) to "
          f"{max(share.values()):.1f}% ({max(share, key=share.get)})")
    print(f"Wrote data/proprietors_income_split.csv ({years[0]}-{years[-1]})")


if __name__ == '__main__':
    main()
