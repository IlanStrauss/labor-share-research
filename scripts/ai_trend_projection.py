"""
AI scenario: where profit shares end up in 2035 and 2050 if AI doubles their trend since 2000.
See AI_TRENDS.md.

Run:  python3 scripts/ai_trend_projection.py
Writes data/ai_trend_projection.csv and figures/ai_trend_capital_share.{png,pdf}.

Method
- Shares, annual from 1970:
  - Figure 3's profit share, (corporate profits without IVA/CCAdj + 1/3 of proprietors'
    income) / GDI, before tax [A053RC] and after corporate tax [A055RC], from BEA.
  - The US non-housing business-sector profit share (ps_wide) from
    github.com/IlanStrauss/business-profit-share: 100 minus the labour share of business
    value added, with the self-employed paid what employees earn (Gutierrez and Piton 2020).
- Smoother: LOESS (local linear regression, Cleveland 1979) with a 30% span, about 16 years.
  It sets the starting level in the last data year, free of that year's cyclical swing.
- Trend: OLS slope of the annual share on the year from 2000 to the last data year, with a
  90% interval from Newey-West standard errors (3 lags).
- Projection for year t after the last data year T:
      current trend:  S_T + b (t - T)
      AI scenario:    S_T + 2b (t - T)
  where S_T is the smoothed share in year T and b the trend slope (percentage points a year).
"""

import csv
import io
import os
import sys
import urllib.request

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import statsmodels.api as sm
from statsmodels.nonparametric.smoothers_lowess import lowess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import ROOT, load  # noqa: E402

START = 1970
TREND_START = 2000
END_PROJ = 2050
REPORT_YEARS = (2035, 2050)
SPAN = 0.3
AI_MULTIPLIER = 2
Z90 = 1.645
# Pinned to a commit, so these numbers do not move when that repository changes
BUSINESS_CSV = ('https://raw.githubusercontent.com/IlanStrauss/business-profit-share/'
                '6de05be00bf92d23817b87cacac49e8c779f32d3/data/processed/profit_share_extended.csv')

# key, panel title, y-axis label, color
PANELS = [
    ('pre_tax', 'Profit share of GDI, pre-tax', '% of gross domestic income', '#2563eb'),
    ('after_corporate_tax', 'Profit share of GDI, after corporate tax', '% of gross domestic income',
     '#0d9488'),
    ('business', 'Business-sector profit share (non-housing)', '% of business value added', '#c026d3'),
]


def bea_shares(d):
    last = max(d['A261RC'])
    years = np.arange(START, last + 1)
    gdi = np.array([d['A261RC'][y] for y in years])
    prop3 = np.array([d['A041RC'][y] for y in years]) / 3
    pre = 100 * (np.array([d['A053RC'][y] for y in years]) + prop3) / gdi
    post = 100 * (np.array([d['A055RC'][y] for y in years]) + prop3) / gdi
    return {'pre_tax': (years, pre), 'after_corporate_tax': (years, post)}


def business_share():
    with urllib.request.urlopen(BUSINESS_CSV) as r:
        rows = [row for row in csv.DictReader(io.TextIOWrapper(r, encoding='utf-8'))
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
    future = np.arange(T + 1, END_PROJ + 1)
    return {
        'smooth': smooth, 'b': b, 'b_lo': lo, 'b_hi': hi, 'level': level, 'T': T,
        'b_since_1970': trend(years, y, START)[0], 'future': future,
        'current': level + b * (future - T),
        'ai': level + AI_MULTIPLIER * b * (future - T),
        'ai_lo': level + AI_MULTIPLIER * lo * (future - T),
        'ai_hi': level + AI_MULTIPLIER * hi * (future - T),
    }


def main():
    series = bea_shares(load())
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
        print(f"  trend {TREND_START}-{T}: {r['b']:.3f} pp/yr (90% interval {r['b_lo']:.3f} to {r['b_hi']:.3f}); "
              f"{START}-{T}: {r['b_since_1970']:.3f} pp/yr")
        for yr in REPORT_YEARS:
            j = yr - T - 1
            print(f"  {yr}: trend since {TREND_START} {r['current'][j]:.1f}%, AI (2x trend) {r['ai'][j]:.1f}% "
                  f"(90% interval {r['ai_lo'][j]:.1f} to {r['ai_hi'][j]:.1f})")

    plot(series, res)
    print('\nWrote data/ai_trend_projection.csv and figures/ai_trend_capital_share.{png,pdf}')


def y_limits(keys, series, res, step):
    vals = np.concatenate([np.concatenate([series[k][1], res[k]['ai']]) for k in keys])
    return step * np.floor(vals.min() / step), step * (np.ceil(vals.max() / step) + 1)


def plot(series, res):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(1, 3, figsize=(28, 9.5))
    # The two GDI panels share one scale; the business-sector panel has its own
    gdi_keys = ['pre_tax', 'after_corporate_tax']
    limits = {k: (y_limits(gdi_keys, series, res, 2), 2) for k in gdi_keys}
    limits['business'] = (y_limits(['business'], series, res, 4), 4)
    for ax, (k, title, ylabel, color) in zip(axes, PANELS):
        years, y = series[k]
        r = res[k]
        T, future = r['T'], r['future']
        ax.plot(years, y, '-', linewidth=2, color=color, alpha=0.35, label='Actual')
        ax.plot(years, r['smooth'], '-', linewidth=5, color=color, alpha=0.9, label='LOESS trend',
                solid_capstyle='round')
        fx = np.concatenate([[T], future])
        ax.plot(fx, np.concatenate([[r['level']], r['current']]), ':', linewidth=4, color=color,
                label=f"Trend since {TREND_START} ({r['b']:+.2f} pp a year)")
        ax.plot(fx, np.concatenate([[r['level']], r['ai']]), '--', linewidth=4, color=color,
                label=f"AI: that trend doubled ({AI_MULTIPLIER * r['b']:+.2f} pp a year)")
        ax.axvline(T, color='#999', linewidth=1.5, linestyle='-', alpha=0.6)
        ax.text(T + 0.5, 0.02, 'projection', fontsize=13, color='#555', transform=ax.get_xaxis_transform())
        for yr in REPORT_YEARS:
            j = yr - T - 1
            # AI label above-left of its point, trend label below-right, clear of both lines
            for vals, offset, ha, va in [(r['ai'], (-8, 8), 'right', 'bottom'),
                                         (r['current'], (8, -8), 'left', 'top')]:
                ax.plot(yr, vals[j], 'o', markersize=9, color=color, markeredgecolor='white',
                        markeredgewidth=2)
                ax.annotate(f"{vals[j]:.1f}%", xy=(yr, vals[j]), xytext=offset,
                            textcoords='offset points', ha=ha, va=va, fontsize=14, color='#222')
        (lo, hi), step = limits[k]
        ax.set_title(title, fontsize=20, fontweight='bold', loc='left')
        ax.set_xlim(START, END_PROJ + 6)
        ax.set_xticks(range(START, END_PROJ + 1, 10))
        ax.set_ylim(lo, hi)
        ax.set_yticks(np.arange(lo, hi + step / 2, step))
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        ax.tick_params(labelsize=15)
        ax.set_ylabel(ylabel, fontsize=16)
        ax.legend(loc='upper left', fontsize=14, framealpha=0.95)
    fig.text(0.5, 0.01,
             "Sources: BEA NIPA bulk data; business-sector share from github.com/IlanStrauss/business-profit-share "
             "(Gutiérrez–Piton method; business value added excludes agriculture, real estate, public administration, education, "
             "and health, and depreciation counts as profit).\n"
             "GDI profit share uses Figure 3's definition: corporate profits without IVA/CCAdj plus 1/3 of proprietors' "
             f"income. Trend = OLS slope of the annual share from {TREND_START} to the last data year. Projections start "
             "from the smoothed last-year level (LOESS span 0.3). A mechanical scenario, not a forecast.",
             ha='center', fontsize=12, color='#555')
    plt.tight_layout(rect=(0, 0.06, 1, 1))
    for ext in ('png', 'pdf'):
        kw = {'dpi': 150} if ext == 'png' else {}
        plt.savefig(os.path.join(ROOT, 'figures', f'ai_trend_capital_share.{ext}'), bbox_inches='tight',
                    facecolor='white', edgecolor='none', **kw)
    plt.close()


if __name__ == '__main__':
    main()
