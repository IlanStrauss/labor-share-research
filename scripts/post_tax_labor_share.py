"""
Labor's share of GDI before and after tax, with the profit share for comparison.
See POST_TAX.md.

Run:  python3 scripts/post_tax_labor_share.py
Writes data/post_tax_labor_share.csv and figures/labor_share_post_tax.{png,pdf}.

All shares are % of gross domestic income (GDI). BEA series codes in brackets.

Labor
- Pre-tax labor share = compensation of employees [A4002C] / GDI [A261RC]
- Payroll taxes = employer contributions for government social insurance [B039RC]
  + employee contributions: Social Security and Medicare [A1587C], state unemployment
  insurance [CON544], railroad retirement [CON550], state and local funds [B738RC].
  Excludes self-employed contributions [CON520] and Medicare Part B premiums [CON530].
- Income tax on wages = tau_h x wages [A034RC], where tau_h is the average income tax
  rate on household income (Mendoza, Razin and Tesar 1994):
      tau_h = (federal [B231RC] + state and local [B245RC] personal income taxes)
              / (wages + proprietors' income [A041RC] + rental income [A048RC]
                 + personal interest [A064RC] + personal dividends [B703RC])
- After-income-tax labor share = (compensation - income tax on wages) / GDI
- Post-tax labor share = (compensation - payroll taxes - income tax on wages) / GDI

Profits (Figure 3's concept: corporate profits without IVA/CCAdj + 1/3 of proprietors' income)
- Pre-tax = (profits before tax [A053RC] + prop/3) / GDI
- After corporate tax = (profits after tax [A055RC] + prop/3) / GDI
- After all taxes = after corporate tax - tau_h x (personal dividends + prop/3) / GDI

Robustness (1954-2014): tau_h recomputed without Treasury's taxes on capital gains
(Office of Tax Analysis, December 2016 table), so no capital gains tax falls on wages.
"""

import csv
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import ROOT, load  # noqa: E402

# Treasury OTA, "Taxes Paid on Capital Gains for Returns with Positive Net Capital Gains,
# 1954-2014" ($ millions), selected years used in the robustness check
OTA_CAPITAL_GAINS_TAX = {1970: 3161, 1980: 12459, 1990: 27829, 2000: 127297, 2007: 137141, 2014: 139127}

FIRST_YEAR = 1948
PLOT_START = 1970


def build(d):
    last = max(d['A261RC'])
    rows = []
    for y in range(FIRST_YEAR, last + 1):
        gdi = d['A261RC'][y]
        comp = d['A4002C'][y]
        wages = d['A034RC'][y]
        prop = d['A041RC'][y]
        divs = d['B703RC'][y]
        payroll = (d['B039RC'][y] + d['A1587C'][y] + d['CON544'].get(y, 0)
                   + d['CON550'].get(y, 0) + d['B738RC'].get(y, 0))
        income_tax = d['B231RC'][y] + d['B245RC'][y]
        hh_income = wages + prop + d['A048RC'][y] + d['A064RC'][y] + divs
        tau_h = income_tax / hh_income
        tax_wages = tau_h * wages
        tax_capital = tau_h * (divs + prop / 3)
        r = {
            'year': y,
            'labor_pre_tax': 100 * comp / gdi,
            'labor_after_income_tax': 100 * (comp - tax_wages) / gdi,
            'labor_post_tax': 100 * (comp - payroll - tax_wages) / gdi,
            'payroll_taxes': 100 * payroll / gdi,
            'income_tax_on_wages': 100 * tax_wages / gdi,
            'avg_household_income_tax_rate': 100 * tau_h,
            'profit_pre_tax': 100 * (d['A053RC'][y] + prop / 3) / gdi,
            'profit_after_corporate_tax': 100 * (d['A055RC'][y] + prop / 3) / gdi,
            'profit_after_all_taxes': 100 * (d['A055RC'][y] + prop / 3 - tax_capital) / gdi,
            'corporate_income_tax': 100 * d['A054RC'][y] / gdi,
            'personal_tax_on_profits': 100 * tax_capital / gdi,
        }
        if y in OTA_CAPITAL_GAINS_TAX:
            tau_ex_cg = (income_tax - OTA_CAPITAL_GAINS_TAX[y]) / hh_income
            r['labor_post_tax_ex_capital_gains_tax'] = 100 * (comp - payroll - tau_ex_cg * wages) / gdi
        rows.append(r)
    return rows


def write_csv(rows, path):
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: round(v, 3) if isinstance(v, float) else v for k, v in r.items()})


def summarize(rows):
    R = {r['year']: r for r in rows}
    last = rows[-1]['year']
    show = ['labor_pre_tax', 'labor_after_income_tax', 'labor_post_tax', 'payroll_taxes',
            'income_tax_on_wages', 'avg_household_income_tax_rate', 'profit_pre_tax',
            'profit_after_corporate_tax', 'profit_after_all_taxes', 'corporate_income_tax',
            'personal_tax_on_profits']
    years = [1970, 1980, 1990, 2000, 2007, 2019, 2024, last]
    print(f"{'% of GDI':32s}" + ''.join(f"{y:>8d}" for y in years) + '  70-24  90-24')
    for k in show:
        print(f"{k:32s}" + ''.join(f"{R[y][k]:8.2f}" for y in years)
              + f"{R[2024][k] - R[1970][k]:7.2f}{R[2024][k] - R[1990][k]:7.2f}")
    print('\nProfits as % of labor + profits (the profit/wage split):')
    for lab, prof in [('labor_pre_tax', 'profit_pre_tax'),
                      ('labor_post_tax', 'profit_after_all_taxes'),
                      ('labor_after_income_tax', 'profit_after_all_taxes')]:
        s = {y: 100 * R[y][prof] / (R[y][lab] + R[y][prof]) for y in (1970, 2024)}
        print(f"  {prof} / ({lab} + {prof}): {s[1970]:.1f}% (1970) -> {s[2024]:.1f}% (2024), {s[2024] - s[1970]:+.1f} pp")
    print('\nCombined swing 1970-2024 (labor fall + profit rise, pp of GDI):')
    for lab, prof in [('labor_pre_tax', 'profit_pre_tax'),
                      ('labor_post_tax', 'profit_after_all_taxes'),
                      ('labor_post_tax', 'profit_after_corporate_tax'),
                      ('labor_after_income_tax', 'profit_after_all_taxes')]:
        dl = R[2024][lab] - R[1970][lab]
        dp = R[2024][prof] - R[1970][prof]
        print(f"  {lab} {dl:+.2f}, {prof} {dp:+.2f}: swing {dp - dl:.2f}")
    print('\nRobustness, capital gains tax removed from the income tax pool:')
    for y in sorted(OTA_CAPITAL_GAINS_TAX):
        print(f"  {y}: post-tax labor share {R[y]['labor_post_tax']:.2f} -> "
              f"{R[y]['labor_post_tax_ex_capital_gains_tax']:.2f}")


def plot(rows, png, pdf):
    plt.style.use('seaborn-v0_8-whitegrid')
    rows = [r for r in rows if r['year'] >= PLOT_START]
    years = [r['year'] for r in rows]
    last = years[-1]
    # Color = tax treatment, the same in both panels: before tax, one tax layer, all taxes
    # (palette checked for color-vision deficiency with the dataviz validator)
    BLUE, TEAL, MAGENTA = '#2563eb', '#0d9488', '#c026d3'
    panels = [
        ('Labor share of GDI', [
            ('labor_pre_tax', 'Pre-tax (compensation)', BLUE),
            ('labor_after_income_tax', 'After income tax on wages', TEAL),
            ('labor_post_tax', 'After payroll and income tax', MAGENTA)], (34, 62)),
        ('Profit share of GDI', [
            ('profit_pre_tax', 'Pre-tax (as in Figure 3)', BLUE),
            ('profit_after_corporate_tax', 'After corporate tax (as in Figure 3)', TEAL),
            ('profit_after_all_taxes', 'After corporate and personal tax', MAGENTA)], (4, 18)),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(20, 9.5))
    for ax, (title, series, ylim), legend_loc in zip(axes, panels, ['lower left', 'upper left']):
        for key, label, color in series:
            vals = [r[key] for r in rows]
            ax.plot(years, vals, '-', linewidth=5, color=color, alpha=0.85, label=label,
                    solid_capstyle='round')
            ax.annotate(f"{vals[-1]:.1f}%", xy=(last, vals[-1]), xytext=(8, 0),
                        textcoords='offset points', va='center', fontsize=15, color='#222')
        ax.set_title(title, fontsize=20, fontweight='bold', loc='left')
        ax.set_xlim(PLOT_START, last + 4)
        ax.set_xticks(range(1970, last + 1, 10))
        ax.set_ylim(*ylim)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        ax.tick_params(labelsize=15)
        ax.set_ylabel('% of gross domestic income', fontsize=16)
        ax.legend(loc=legend_loc, fontsize=14, framealpha=0.95)
    fig.text(0.5, 0.01,
             "Source: BEA NIPA bulk data (Tables 1.10, 2.1, 3.4, 3.6). Income tax on wages and on dividends and "
             "proprietors' income uses the average household income tax rate (Mendoza, Razin and Tesar 1994).\n"
             "Payroll taxes are employer and employee social insurance contributions. Profits are corporate "
             "profits without IVA/CCAdj plus 1/3 of proprietors' income (Gollin 2002).",
             ha='center', fontsize=12, color='#555')
    plt.tight_layout(rect=(0, 0.06, 1, 1))
    plt.savefig(png, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(pdf, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()


if __name__ == '__main__':
    rows = build(load())
    os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
    write_csv(rows, os.path.join(ROOT, 'data', 'post_tax_labor_share.csv'))
    summarize(rows)
    plot(rows, os.path.join(ROOT, 'figures', 'labor_share_post_tax.png'),
         os.path.join(ROOT, 'figures', 'labor_share_post_tax.pdf'))
    print('\nWrote data/post_tax_labor_share.csv and figures/labor_share_post_tax.{png,pdf}')
