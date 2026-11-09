"""
AI scenario: labor and profit shares in 2035 if AI doubles their trend since 2000.
See AI_TRENDS.md.

Run:  python3 scripts/ai_trend_projection.py
Writes data/ai_trend_projection.csv and figures/ai_trend_capital_share.{png,pdf}.

Method
- Shares, annual from 1970:
  - Labor's share of GDI before tax and after payroll and income tax, and the profit share of
    GDI (corporate profits after depreciation + 1/3 of proprietors' income) before tax and after
    corporate and personal tax, all as defined in post_tax_labor_share.py (BEA data).
  - The US non-housing business-sector profit share (ps_wide) from
    github.com/IlanStrauss/business-profit-share (data/business_profit_share_usa.csv, saved by fetch_data.py): 100 minus the labour share of business
    value added, with the self-employed paid what employees earn (Gutierrez and Piton 2020).
    It leaves out real estate, which holds owner-occupiers' imputed rents. Its profits are before depreciation.
- Smoother: LOESS (local linear regression, Cleveland 1979) with a 30% span, about 16 years.
  It sets the starting level in the last data year, free of that year's cyclical swing.
- Trend: OLS slope of the annual share on the year from 2000 to the last data year, with a
  90% interval from Newey-West standard errors (3 lags).
- Projection for year t after the last data year T:
      trend since 2000:  S_T + b (t - T)
      AI scenario:       S_T + 2b (t - T)
  where S_T is the smoothed share in year T and b the trend slope (percentage points a year).
"""

import csv
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import statsmodels.api as sm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from statsmodels.nonparametric.smoothers_lowess import lowess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import ROOT, load  # noqa: E402
from post_tax_labor_share import build  # noqa: E402

START = 1970
TREND_START = 2000
TARGET = 2035
SPAN = 0.3
AI_MULTIPLIER = 2
Z90 = 1.645
BUSINESS_CSV = os.path.join(ROOT, 'data', 'business_profit_share_usa.csv')

# Blue = pre-tax, orange = post-tax, as in the post-tax figure
BLUE, ORANGE, GRAY = '#2563eb', '#ea580c', '#4b5563'
# title, y-axis label, [(series key, label, color)]
PANELS = [
    ('Labor share of GDI', '% of gross domestic income',
     [('labor_pre_tax', 'Pre-tax', BLUE), ('labor_post_tax', 'Post-tax', ORANGE)]),
    ('Profit share of GDI (profits after depreciation)', '% of gross domestic income',
     [('profit_pre_tax', 'Pre-tax', BLUE), ('profit_after_all_taxes', 'Post-tax', ORANGE)]),
    ('Non-housing business-sector profit share (profits before depreciation)', '% of business value added',
     [('business', 'Pre-tax', BLUE)]),
]


def gdi_series(d):
    rows = [r for r in build(d) if r['year'] >= START]
    years = np.array([r['year'] for r in rows])
    keys = ['labor_pre_tax', 'labor_post_tax', 'profit_pre_tax', 'profit_after_all_taxes']
    return {k: (years, np.array([r[k] for r in rows])) for k in keys}


def business_share():
    with open(BUSINESS_CSV, newline='') as f:
        rows = [row for row in csv.DictReader(f)
                if row['iso3c'] == 'USA' and row['ps_wide'] and int(row['year']) >= START]
    rows.sort(key=lambda row: int(row['year']))
    years = np.array([int(row['year']) for row in rows])
    assert (np.diff(years) == 1).all(), 'business-sector series has gaps'
    return years, np.array([float(row['ps_wide']) for row in rows])


def trend(years, y, start=TREND_START):
    keep = years >= start
    X = sm.add_constant(years[keep].astype(float))
    fit = sm.OLS(y[keep], X).fit(cov_type='HAC', cov_kwds={'maxlags': 3})
    b, se = fit.params[1], fit.bse[1]
    return b, b - Z90 * se, b + Z90 * se


def project(years, y):
    smooth = lowess(y, years, frac=SPAN, it=0, return_sorted=False)
    b, lo, hi = trend(years, y)
    T, level = years[-1], smooth[-1]
    future = np.arange(T + 1, TARGET + 1)
    return {
        'smooth': smooth, 'b': b, 'b_lo': lo, 'b_hi': hi, 'level': level, 'T': T,
        'b_since_1970': trend(years, y, START)[0], 'future': future,
        'current': level + b * (future - T),
        'ai': level + AI_MULTIPLIER * b * (future - T),
        'ai_lo': level + AI_MULTIPLIER * lo * (future - T),
        'ai_hi': level + AI_MULTIPLIER * hi * (future - T),
    }


def main():
    series = gdi_series(load())
    series['business'] = business_share()
    res = {k: project(*v) for k, v in series.items()}

    with open(os.path.join(ROOT, 'data', 'ai_trend_projection.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['series', 'year', 'actual', 'loess', f'trend_since_{TREND_START}', 'ai_doubled_trend'])
        for k, (years, y) in series.items():
            r = res[k]
            for i, yr in enumerate(years):
                w.writerow([k, int(yr), round(y[i], 3), round(r['smooth'][i], 3), '', ''])
            for j, yr in enumerate(r['future']):
                w.writerow([k, int(yr), '', '', round(r['current'][j], 3), round(r['ai'][j], 3)])

    for k, (years, y) in series.items():
        r = res[k]
        T = r['T']
        print(f"\n{k}: actual {T} = {y[-1]:.2f}%, LOESS {T} = {r['level']:.2f}%")
        print(f"  trend {TREND_START}-{T}: {r['b']:+.3f} pp/yr (90% interval {r['b_lo']:+.3f} to {r['b_hi']:+.3f}); "
              f"{START}-{T}: {r['b_since_1970']:+.3f} pp/yr")
        print(f"  {TARGET}: trend since {TREND_START} {r['current'][-1]:.1f}%, AI (2x trend) {r['ai'][-1]:.1f}% "
              f"(90% interval {min(r['ai_lo'][-1], r['ai_hi'][-1]):.1f} to {max(r['ai_lo'][-1], r['ai_hi'][-1]):.1f})")

    plot(series, res)
    print('\nWrote data/ai_trend_projection.csv and figures/ai_trend_capital_share.{png,pdf}')


def y_limits(keys, series, res, step):
    vals = np.concatenate([np.concatenate([series[k][1], res[k]['smooth'], res[k]['ai']]) for k in keys])
    return step * np.floor(vals.min() / step), step * (np.ceil(vals.max() / step) + 1)


def plot(series, res):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(3, 1, figsize=(14, 22))
    for ax, (title, ylabel, members), step in zip(axes, PANELS, (4, 2, 4)):
        for k, label, color in members:
            years, y = series[k]
            r = res[k]
            T = r['T']
            ax.plot(years, y, '-', linewidth=2, color=color, alpha=0.35)
            ax.plot(years, r['smooth'], '-', linewidth=5, color=color, alpha=0.9, solid_capstyle='round')
            ax.plot(np.concatenate([[T], r['future']]), np.concatenate([[r['level']], r['ai']]), '--',
                    linewidth=4, color=color)
            ax.plot(TARGET, r['ai'][-1], 'o', markersize=10, color=color, markeredgecolor='white', markeredgewidth=2)
            ax.annotate(f"{label}: {r['ai'][-1]:.1f}%", xy=(TARGET, r['ai'][-1]), xytext=(12, 0),
                        textcoords='offset points', va='center', fontsize=17, color='#222')
        T = res[members[0][0]]['T']
        ax.axvline(T, color='#999', linewidth=1.5, alpha=0.6)
        ax.text(T + 0.5, 0.03, 'AI scenario', fontsize=14, color='#555', transform=ax.get_xaxis_transform())
        lo, hi = y_limits([k for k, _, _ in members], series, res, step)
        ax.set_ylim(lo, hi)
        ax.set_yticks(np.arange(lo, hi + step / 2, step))
        ax.set_xlim(START, TARGET + 9)
        ax.set_xticks(range(START, TARGET + 1, 5))
        ax.set_title(title, fontsize=22, fontweight='bold', loc='left')
        ax.set_ylabel(ylabel, fontsize=17)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        ax.tick_params(labelsize=16)
        ax.tick_params(axis='x', pad=10)
    key = [Patch(color=BLUE, label='Pre-tax'), Patch(color=ORANGE, label='Post-tax'),
           Line2D([0], [0], color=GRAY, linewidth=2, alpha=0.35, label='Annual data'),
           Line2D([0], [0], color=GRAY, linewidth=5, label='Smoothed (LOESS)'),
           Line2D([0], [0], color=GRAY, linewidth=4, linestyle='--', label=f'AI: trend since {TREND_START} doubled')]
    axes[0].legend(handles=key, loc='lower left', fontsize=15, framealpha=0.95)
    fig.text(0.5, 0.005,
             "Sources: BEA NIPA; non-housing business-sector share from github.com/IlanStrauss/business-profit-share "
             "(Gutiérrez–Piton method), which leaves out real estate."
             "\nPost-tax: labor after payroll and income tax; profits after corporate and "
             "personal tax. GDI profits are corporate profits after depreciation\nplus 1/3 of proprietors' income. "
             f"Trend = OLS slope of the annual share from {TREND_START} to the last data year; the scenario doubles it "
             "from the\nsmoothed last-year level (LOESS span 0.3). A mechanical scenario, not a forecast.",
             ha='center', fontsize=13, color='#555')
    plt.tight_layout(rect=(0, 0.045, 1, 1), h_pad=3)
    for ext in ('png', 'pdf'):
        kw = {'dpi': 150} if ext == 'png' else {}
        plt.savefig(os.path.join(ROOT, 'figures', f'ai_trend_capital_share.{ext}'), bbox_inches='tight',
                    facecolor='white', edgecolor='none', **kw)
    plt.close()


if __name__ == '__main__':
    main()
