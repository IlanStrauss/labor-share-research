"""
Labor's and profits' shares of GDI after taxes and government spending. See POST_TAX.md.

Run:  python3 scripts/post_spending_shares.py
Writes data/post_spending_shares.csv and figures/shares_post_spending.{png,pdf}.

Starts from the post-tax shares in post_tax_labor_share.py and adds what each side receives
from government, following the "net social wage" of Shaikh and Tonak (1987) as extended to
2012 by Moos (2019). All shares are % of GDI [A261RC]. BEA series codes in brackets.

Labor
- Social benefits = government social benefits to persons [A063RC] (Social Security [W823RC],
  Medicare [W824RC], Medicaid [W729RC], unemployment insurance, veterans' benefits, SNAP,
  refundable tax credits, and others; Table 3.12), less the Medicare supplementary medical
  insurance premiums enrollees pay [CON530]. All of it counts as labor's, as in Shaikh and
  Tonak: retirees' benefits as deferred pay, the rest as support for workers and their families.
- Public services = government consumption expenditures on health (public hospitals and
  clinics) [G17007], recreation and culture [G17008], education [G17009], and income security
  [G17010] (Table 3.17), the services households use directly. Labor's part is wages' share of
  household income, the ratio that splits income tax between wages and capital income in
  post_tax_labor_share.py (Shaikh and Tonak split these services by a labor share in the same way).
- After taxes and spending = post-tax labor share + social benefits + labor's part of public services

Profits
- Government grants = federal capital transfers to business (Table 5.11): financial
  stabilization payments [W950RC, 2008-2012] and other capital transfers [W951RC], counted in
  the year paid.
- After taxes and grants = profits after corporate and personal tax + government grants

Collective spending (defense, police and courts, roads, general administration, and interest)
is left out of both. Subsidies and tax breaks are already in profits.
"""

import math
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import ROOT, load  # noqa: E402
from post_tax_labor_share import build as build_post_tax, household_income, write_csv  # noqa: E402

# Government consumption expenditures on health, recreation and culture, education, and
# income security (Table 3.17), the services households use directly
SERVICES = ['G17007', 'G17008', 'G17009', 'G17010']

FIRST_YEAR = 1959  # Table 3.17 starts in 1959
PLOT_START = 1970


def build(d):
    post_tax = {r['year']: r for r in build_post_tax(d)}
    rows = []
    for y in range(FIRST_YEAR, max(d['A261RC']) + 1):
        gdi = d['A261RC'][y]
        p = post_tax[y]
        premiums = d['CON530'].get(y, 0)
        medicare = d['W824RC'].get(y, 0)
        medicaid = d['W729RC'].get(y, 0)
        benefits = d['A063RC'][y] - premiums
        services = sum(d[c][y] for c in SERVICES)
        wage_share = d['A034RC'][y] / household_income(d, y)
        grants = d['W950RC'].get(y, 0) + d['W951RC'].get(y, 0)
        rows.append({
            'year': y,
            'labor_pre_tax': p['labor_pre_tax'],
            'labor_post_tax': p['labor_post_tax'],
            'social_benefits': 100 * benefits / gdi,
            'social_security': 100 * d['W823RC'][y] / gdi,
            'medicare_less_premiums': 100 * (medicare - premiums) / gdi,
            'medicaid': 100 * medicaid / gdi,
            'other_social_benefits': 100 * (d['A063RC'][y] - d['W823RC'][y] - medicare - medicaid) / gdi,
            'public_services': 100 * services / gdi,
            'wage_share_of_household_income': 100 * wage_share,
            'public_services_to_labor': 100 * wage_share * services / gdi,
            'labor_after_spending': p['labor_post_tax'] + 100 * (benefits + wage_share * services) / gdi,
            'profit_pre_tax': p['profit_pre_tax'],
            'profit_after_all_taxes': p['profit_after_all_taxes'],
            'government_grants_to_business': 100 * grants / gdi,
            'financial_stabilization_payments': 100 * d['W950RC'].get(y, 0) / gdi,
            'profit_after_grants': p['profit_after_all_taxes'] + 100 * grants / gdi,
        })
    return rows


def summarize(rows):
    R = {r['year']: r for r in rows}
    last = rows[-1]['year']
    show = ['labor_pre_tax', 'labor_post_tax', 'social_benefits', 'social_security',
            'medicare_less_premiums', 'medicaid', 'other_social_benefits', 'public_services',
            'wage_share_of_household_income', 'public_services_to_labor', 'labor_after_spending',
            'profit_pre_tax', 'profit_after_all_taxes', 'government_grants_to_business',
            'profit_after_grants']
    years = [1970, 1980, 1990, 2000, 2007, 2019, 2024, last]
    print(f"{'% of GDI':32s}" + ''.join(f"{y:>8d}" for y in years) + '  70-24  90-24')
    for k in show:
        print(f"{k:32s}" + ''.join(f"{R[y][k]:8.2f}" for y in years)
              + f"{R[2024][k] - R[1970][k]:7.2f}{R[2024][k] - R[1990][k]:7.2f}")
    print('\nLabor after taxes and spending, other ways to split public services:')
    for label, f in [('all to labor', lambda r: r['labor_post_tax'] + r['social_benefits'] + r['public_services']),
                     ('none to labor', lambda r: r['labor_post_tax'] + r['social_benefits'])]:
        print(f"  {label}: {f(R[1970]):.2f} (1970) -> {f(R[2024]):.2f} (2024), {f(R[2024]) - f(R[1970]):+.2f} pp")
    print('\nProfits as % of labor + profits after taxes and spending:')
    s = {y: 100 * R[y]['profit_after_grants'] / (R[y]['labor_after_spending'] + R[y]['profit_after_grants'])
         for y in (1970, 2024)}
    print(f"  {s[1970]:.1f}% (1970) -> {s[2024]:.1f}% (2024), {s[2024] - s[1970]:+.1f} pp")
    peak = max((r for r in rows if r['year'] >= PLOT_START), key=lambda r: r['labor_after_spending'])
    grants = max(rows, key=lambda r: r['government_grants_to_business'])
    print(f"\nPeak labor share after spending: {peak['labor_after_spending']:.2f} in {peak['year']}")
    print(f"Largest grants: {grants['government_grants_to_business']:.2f} in {grants['year']}")


def spread(values, gap):
    # Nudge end-of-line labels apart so that no two are closer than gap
    order = sorted(range(len(values)), key=values.__getitem__)
    out = list(values)
    for a, b in zip(order, order[1:]):
        out[b] = max(out[b], out[a] + gap)
    return out


def plot(rows, png, pdf):
    plt.style.use('seaborn-v0_8-whitegrid')
    rows = [r for r in rows if r['year'] >= PLOT_START]
    years = [r['year'] for r in rows]
    last = years[-1]
    # Color = treatment, the same in both panels and as in the post-tax figure: blue before tax,
    # orange after taxes, teal after taxes and spending (checked with the dataviz validator).
    # Teal is dashed so that the post-tax profit line shows through where grants are near zero.
    BLUE, ORANGE, TEAL = '#2563eb', '#ea580c', '#0d9488'
    panels = [
        ('Labor share of GDI', [
            ('labor_pre_tax', 'Pre-tax (compensation)', BLUE),
            ('labor_post_tax', 'Post-tax (after payroll and income tax)', ORANGE),
            ('labor_after_spending', 'Post-tax plus social benefits and public services', TEAL)]),
        ('Profit share of GDI (profits after depreciation)', [
            ('profit_pre_tax', 'Pre-tax (Figure 3 definition)', BLUE),
            ('profit_after_all_taxes', 'Post-tax (after corporate and personal tax)', ORANGE),
            ('profit_after_grants', 'Post-tax plus government grants to business', TEAL)]),
    ]
    fig, axes = plt.subplots(2, 1, figsize=(14, 16))
    for ax, (title, series), legend_loc in zip(axes, panels, ['lower left', 'upper left']):
        vals_all = [r[k] for k, _, _ in series for r in rows]
        lo, hi = 2 * math.floor(min(vals_all) / 2 - 1), 2 * math.ceil(max(vals_all) / 2 + 1)
        ends = spread([rows[-1][k] for k, _, _ in series], gap=0.035 * (hi - lo))
        for (key, label, color), end in zip(series, ends):
            vals = [r[key] for r in rows]
            style = dict(linestyle=(0, (1.6, 1.0)), dash_capstyle='butt') if color == TEAL else dict(solid_capstyle='round')
            ax.plot(years, vals, linewidth=5, color=color, alpha=0.9, label=label, **style)
            ax.annotate(f"{vals[-1]:.1f}%", xy=(last, vals[-1]), xytext=(last + 0.6, end),
                        textcoords='data', va='center', fontsize=15, color='#222')
        ax.set_title(title, fontsize=22, fontweight='bold', loc='left')
        ax.set_xlim(PLOT_START, last + 4)
        ax.set_xticks(range(1970, last + 1, 10))
        ax.set_ylim(lo, hi)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        ax.tick_params(labelsize=15)
        ax.tick_params(axis='x', pad=10)
        ax.set_ylabel('% of gross domestic income', fontsize=16)
        ax.legend(loc=legend_loc, fontsize=14, framealpha=0.95)
    fig.text(0.5, 0.01,
             "Source: BEA NIPA bulk data (Tables 1.10, 1.12, 2.1, 3.4, 3.6, 3.12, 3.17, 5.11). Social benefits are government social "
             "benefits to persons, less Medicare\npremiums paid by enrollees. Public services are government spending on health, "
             "education, recreation and culture, and income security services; labor's part\nis wages' share of household income. "
             "Government grants are federal capital transfers to business, including the 2008-12 financial stabilization payments.\n"
             "Collective spending such as defense, police, and roads is left out. Net social wage method of Shaikh and Tonak (1987) "
             "and Moos (2019).",
             ha='center', fontsize=12, color='#555')
    plt.tight_layout(rect=(0, 0.08, 1, 1), h_pad=3)
    plt.savefig(png, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(pdf, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()


if __name__ == '__main__':
    rows = build(load())
    write_csv(rows, os.path.join(ROOT, 'data', 'post_spending_shares.csv'))
    summarize(rows)
    plot(rows, os.path.join(ROOT, 'figures', 'shares_post_spending.png'),
         os.path.join(ROOT, 'figures', 'shares_post_spending.pdf'))
    print('\nWrote data/post_spending_shares.csv and figures/shares_post_spending.{png,pdf}')
