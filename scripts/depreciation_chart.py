#!/usr/bin/env python3
"""
Generate Figure 4: depreciation (consumption of fixed capital) as % of GDI.

Top panel: depreciation by type of asset, stacked (BEA Table 5.2.5)
- Government fixed assets [A264RC]
- Housing: private residential [A754RC]
- Structures: private nonresidential [B188RC]
- Equipment: private [Y080RC]
- Intellectual property products: private software, R&D, and entertainment originals [Y083RC]
These sum to total depreciation [A262RC].

Bottom panel: depreciation of corporate capital (BEA Tables 1.12 and 1.14)
- Economic depreciation: BEA's consumption of fixed capital, corporate business [A438RC]
- As firms report it for tax: capital consumption allowances = A438RC + capital consumption
  adjustment [A059RC]. Corporate profits without CCAdj (Figure 3) are after this one.

Run: python3 scripts/depreciation_chart.py
Writes figures/depreciation.{png,pdf}.
"""

import os
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import ROOT, load  # noqa: E402

START, END = 1970, 2024

# Bottom to top of the stack. Categorical slots 5, 4, 3, 2, 1 of the dataviz palette
# (validated in this order: adjacent bands pass the color-vision checks; labels carry identity)
ASSETS = [
    ('A264RC', 'Government', '#e87ba4'),
    ('A754RC', 'Housing', '#eda100'),
    ('B188RC', 'Business structures', '#1baf7a'),
    ('Y080RC', 'Business equipment', '#eb6834'),
    ('Y083RC', 'Software, R&D, and other IP', '#2a78d6'),
]


def main():
    d = load()
    years = np.arange(START, END + 1)
    gdi = np.array([d['A261RC'][y] for y in years])
    share = {code: 100 * np.array([d[code][y] for y in years]) / gdi for code, _, _ in ASSETS}
    total = 100 * np.array([d['A262RC'][y] for y in years]) / gdi
    gap = np.abs(sum(share.values()) - total).max()
    assert gap < 0.05, f'asset types do not sum to total depreciation (gap {gap:.3f} pp)'
    corp_econ = 100 * np.array([d['A438RC'][y] for y in years]) / gdi
    corp_tax = 100 * np.array([d['A438RC'][y] + d['A059RC'][y] for y in years]) / gdi

    print(f"Depreciation, % of GDI: {total[0]:.1f} ({START}) -> {total[-1]:.1f} ({END}), {total[-1] - total[0]:+.1f} pp")
    for code, label, _ in ASSETS:
        s = share[code]
        print(f"  {label:30s} {s[0]:5.2f} -> {s[-1]:5.2f}  ({s[-1] - s[0]:+.2f} pp)")
    print(f"Corporate depreciation {END}: economic {corp_econ[-1]:.2f}, for tax {corp_tax[-1]:.2f} "
          f"({START}: {corp_econ[0]:.2f}, {corp_tax[0]:.2f})")

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(16, 19), gridspec_kw={'height_ratios': [1.25, 1]})

    # Top: stacked areas, 2px white gaps between bands, labels at the right edge
    ax = top
    base = np.zeros(len(years))
    for code, label, color in ASSETS:
        upper = base + share[code]
        ax.fill_between(years, base, upper, color=color, linewidth=2, edgecolor='white', label=label)
        ax.annotate(f"{label}: {share[code][-1]:.1f}%", xy=(END, (base[-1] + upper[-1]) / 2), xytext=(10, 0),
                    textcoords='offset points', va='center', fontsize=15, color='#222')
        base = upper
    ax.plot(years, total, color='#222', linewidth=2.5)
    ax.annotate(f"Total: {total[-1]:.1f}%", xy=(END, total[-1]), xytext=(10, 10), textcoords='offset points',
                va='bottom', fontsize=16, fontweight='bold', color='#222')
    ax.annotate(f"Total: {total[0]:.1f}%", xy=(START + 0.3, total[0]), xytext=(START + 1, 17.6),
                va='bottom', fontsize=16, fontweight='bold', color='#222',
                arrowprops=dict(arrowstyle='->', color='#222', lw=1.5))
    ax.set_title('Depreciation by type of asset', fontsize=22, fontweight='bold', loc='left')
    ax.set_ylim(0, 20)
    ax.set_yticks(range(0, 21, 2))

    # Bottom: the depreciation corporations deduct for tax against BEA's economic measure
    ax = bottom
    ax.plot(years, corp_econ, '-', linewidth=6, color='#374151', alpha=0.9,
            label="Economic depreciation (BEA's measure, in the depreciation total above)")
    ax.plot(years, corp_tax, '--', linewidth=5, color='#6250d6',
            label='Depreciation as firms report it for tax (Figure 3 profits are after this)')
    for series in (corp_econ, corp_tax):
        ax.annotate(f"{series[-1]:.1f}%", xy=(END, series[-1]), xytext=(10, 0), textcoords='offset points',
                    va='center', fontsize=16, color='#222')
    ax.set_title('Depreciation of corporate capital', fontsize=22, fontweight='bold', loc='left')
    ax.set_ylim(5, 11)
    ax.set_yticks(range(5, 12, 1))
    ax.legend(loc='upper left', fontsize=15, framealpha=0.95)

    for ax in (top, bottom):
        ax.set_xlim(START, END + 9)
        ax.set_xticks(range(START, END + 1, 5))
        ax.tick_params(labelsize=16)
        ax.tick_params(axis='x', pad=10)
        ax.set_ylabel('% of gross domestic income', fontsize=18)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    fig.text(0.5, 0.005,
             'Source: BEA NIPA bulk data (Tables 1.12, 1.14, and 5.2.5). Depreciation is consumption of fixed capital. '
             'Business assets are private nonresidential;\nIP is intellectual property products (software, research '
             'and development, and entertainment originals). Tax depreciation = capital consumption allowances.',
             ha='center', fontsize=13, color='#555')
    plt.tight_layout(rect=(0, 0.035, 1, 1), h_pad=3)
    for ext in ('png', 'pdf'):
        kw = {'dpi': 150} if ext == 'png' else {}
        plt.savefig(os.path.join(ROOT, 'figures', f'depreciation.{ext}'), bbox_inches='tight',
                    facecolor='white', edgecolor='none', **kw)
    plt.close()
    print('Wrote figures/depreciation.{png,pdf}')


if __name__ == '__main__':
    main()
