"""
AI scenario: where the profit (capital) share ends up in 2035 and 2050 if AI doubles its trend.
See AI_TRENDS.md.

Run:  python3 scripts/ai_trend_projection.py
Writes data/ai_trend_projection.csv and figures/ai_trend_capital_share.{png,pdf}.

Method
- Share: Figure 3's profit share, (corporate profits without IVA/CCAdj + 1/3 of proprietors'
  income) / GDI, before tax [A053RC] and after corporate tax [A055RC], annual, from BEA.
- Smoother: LOESS (local linear regression, Cleveland 1979) with a 30% span, about 17 years.
  It sets the starting level in the last data year, free of that year's cyclical swing.
- Trend: OLS slope of the annual share on the year over 1970 to the last data year, with a
  90% interval from Newey-West standard errors (3 lags).
- Projection for year t after the last data year T:
      current trend:  S_T + b (t - T)
      AI scenario:    S_T + 2b (t - T)
  where S_T is the smoothed share in year T and b the trend slope (percentage points a year).
"""

import csv
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import statsmodels.api as sm
from statsmodels.nonparametric.smoothers_lowess import lowess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import ROOT, load  # noqa: E402

START = 1970
END_PROJ = 2050
REPORT_YEARS = (2035, 2050)
SPAN = 0.3
AI_MULTIPLIER = 2
Z90 = 1.645


def shares(d):
    last = max(d['A261RC'])
    years = np.arange(START, last + 1)
    gdi = np.array([d['A261RC'][y] for y in years])
    prop3 = np.array([d['A041RC'][y] for y in years]) / 3
    pre = 100 * (np.array([d['A053RC'][y] for y in years]) + prop3) / gdi
    post = 100 * (np.array([d['A055RC'][y] for y in years]) + prop3) / gdi
    return years, {'pre_tax': pre, 'after_corporate_tax': post}


def trend(years, y, start=START):
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
    out = {
        'smooth': smooth, 'b': b, 'b_lo': lo, 'b_hi': hi, 'level': level, 'T': T,
        'b_since_2000': trend(years, y, 2000)[0], 'future': future,
        'current': level + b * (future - T),
        'ai': level + AI_MULTIPLIER * b * (future - T),
        'ai_lo': level + AI_MULTIPLIER * lo * (future - T),
        'ai_hi': level + AI_MULTIPLIER * hi * (future - T),
    }
    return out


def main():
    years, series = shares(load())
    res = {k: project(years, v) for k, v in series.items()}

    rows = []
    for i, yr in enumerate(years):
        r = {'year': int(yr)}
        for k in series:
            r[f'{k}_actual'] = series[k][i]
            r[f'{k}_loess'] = res[k]['smooth'][i]
        rows.append(r)
    for j, yr in enumerate(res['pre_tax']['future']):
        r = {'year': int(yr)}
        for k in series:
            r[f'{k}_current_trend'] = res[k]['current'][j]
            r[f'{k}_ai_doubled_trend'] = res[k]['ai'][j]
        rows.append(r)
    cols = list(dict.fromkeys(c for r in rows for c in r))
    with open(os.path.join(ROOT, 'data', 'ai_trend_projection.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: round(v, 3) if isinstance(v, float) else v for c, v in r.items()})

    for k, r in res.items():
        T = r['T']
        print(f"\n{k}: actual {T} = {series[k][-1]:.2f}%, LOESS {T} = {r['level']:.2f}%")
        print(f"  trend {START}-{T}: {r['b']:.3f} pp/yr (90% interval {r['b_lo']:.3f} to {r['b_hi']:.3f}); "
              f"since 2000: {r['b_since_2000']:.3f} pp/yr")
        for yr in REPORT_YEARS:
            j = yr - T - 1
            print(f"  {yr}: current trend {r['current'][j]:.1f}%, AI (2x trend) {r['ai'][j]:.1f}% "
                  f"(90% interval {r['ai_lo'][j]:.1f} to {r['ai_hi'][j]:.1f})")

    plot(years, series, res)
    print('\nWrote data/ai_trend_projection.csv and figures/ai_trend_capital_share.{png,pdf}')


def plot(years, series, res):
    plt.style.use('seaborn-v0_8-whitegrid')
    panels = [('pre_tax', 'Profit share of GDI, pre-tax', '#2563eb'),
              ('after_corporate_tax', 'Profit share of GDI, after corporate tax', '#0d9488')]
    fig, axes = plt.subplots(1, 2, figsize=(20, 9.5), sharey=True)
    for ax, (k, title, color) in zip(axes, panels):
        r = res[k]
        T, future = r['T'], r['future']
        ax.plot(years, series[k], '-', linewidth=2, color=color, alpha=0.35, label='Actual')
        ax.plot(years, r['smooth'], '-', linewidth=5, color=color, alpha=0.9, label='LOESS trend',
                solid_capstyle='round')
        fx = np.concatenate([[T], future])
        ax.plot(fx, np.concatenate([[r['level']], r['current']]), ':', linewidth=4, color=color,
                label=f"Current trend ({r['b']:+.2f} pp a year)")
        ax.plot(fx, np.concatenate([[r['level']], r['ai']]), '--', linewidth=4, color=color,
                label=f"AI: trend doubled ({AI_MULTIPLIER * r['b']:+.2f} pp a year)")
        ax.axvline(T, color='#999', linewidth=1.5, linestyle='-', alpha=0.6)
        ax.text(T + 0.5, 4.6, 'projection', fontsize=13, color='#555')
        for yr in REPORT_YEARS:
            j = yr - T - 1
            # AI label above-left of its point, current-trend label below-right, clear of both lines
            for vals, offset, ha, va in [(r['ai'], (-8, 8), 'right', 'bottom'),
                                         (r['current'], (8, -8), 'left', 'top')]:
                ax.plot(yr, vals[j], 'o', markersize=9, color=color, markeredgecolor='white',
                        markeredgewidth=2)
                ax.annotate(f"{vals[j]:.1f}%", xy=(yr, vals[j]), xytext=offset,
                            textcoords='offset points', ha=ha, va=va, fontsize=14, color='#222')
        ax.set_title(title, fontsize=20, fontweight='bold', loc='left')
        ax.set_xlim(START, END_PROJ + 6)
        ax.set_xticks(range(START, END_PROJ + 1, 10))
        ax.set_ylim(4, 24)
        ax.set_yticks(range(4, 25, 2))
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        ax.tick_params(labelsize=15)
        ax.legend(loc='upper left', fontsize=14, framealpha=0.95)
    axes[0].set_ylabel('% of gross domestic income', fontsize=16)
    fig.text(0.5, 0.01,
             "Source: BEA NIPA bulk data. Profit share as in Figure 3: corporate profits without IVA/CCAdj plus "
             "1/3 of proprietors' income, over GDI. LOESS span 0.3 (about 17 years).\n"
             f"Trend = OLS slope of the annual share, {START} to {years[-1]}. Projections start from the "
             f"smoothed {years[-1]} level. A mechanical scenario, not a forecast.",
             ha='center', fontsize=12, color='#555')
    plt.tight_layout(rect=(0, 0.06, 1, 1))
    for ext in ('png', 'pdf'):
        kw = {'dpi': 150} if ext == 'png' else {}
        plt.savefig(os.path.join(ROOT, 'figures', f'ai_trend_capital_share.{ext}'), bbox_inches='tight',
                    facecolor='white', edgecolor='none', **kw)
    plt.close()


if __name__ == '__main__':
    main()
