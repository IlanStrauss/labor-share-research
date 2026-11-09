#!/usr/bin/env python3
"""
Generate Figure 3: Corporate Profit Share chart.
Shows pre-tax and post-tax corporate profit share (profits after depreciation,
excluding rent and interest), plus 1/3 of proprietors' income (a common split since Johnson 1954).

Data: BEA NIPA bulk file, annual, read by bea_nipa.py (BEA series codes in brackets)
- Pre-tax  = (corporate profits before tax without IVA/CCAdj [A053RC] + 1/3 x proprietors' income [A041RC]) / GDI [A261RC]
- Post-tax = (corporate profits after tax without IVA/CCAdj [A055RC] + 1/3 x proprietors' income) / GDI
Corporate profits are measured after depreciation as firms report it for tax.

Run: python3 scripts/generate_capital_share_chart.py
"""

import os
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import ROOT, load  # noqa: E402

# === DATA ===
START, END = 1970, 2024
years = list(range(START, END + 1))
d = load()

# Capital's share of proprietors' income (a common split since Johnson 1954)
alpha = 1/3

pretax_adjusted = [100 * (d['A053RC'][y] + alpha * d['A041RC'][y]) / d['A261RC'][y] for y in years]
posttax_adjusted = [100 * (d['A055RC'][y] + alpha * d['A041RC'][y]) / d['A261RC'][y] for y in years]

# === CREATE FIGURE (same sizes as Figures 1 and 2) ===
# Blue = pre-tax, orange = post-tax, as in the post-tax figure
# (pair checked for color-vision deficiency with the dataviz validator)
COLORS = {'pretax': '#2563eb', 'posttax': '#ea580c'}
LINE_WIDTH = 7.0
LINE_ALPHA = 0.75
MARKER_SIZE = 10
AXIS_LABEL_SIZE = 18
TICK_SIZE = 16
LEGEND_SIZE = 16
ANNOTATION_SIZE = 16
SOURCE_SIZE = 12

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(16, 10))

ax.plot(years, pretax_adjusted, '-', linewidth=LINE_WIDTH, color=COLORS['pretax'], alpha=LINE_ALPHA,
        marker='o', markersize=MARKER_SIZE, markevery=5, label='Pre-tax')
ax.plot(years, posttax_adjusted, '-', linewidth=LINE_WIDTH, color=COLORS['posttax'], alpha=LINE_ALPHA,
        marker='s', markersize=MARKER_SIZE, markevery=5, label='Post-tax (after corporate income tax)')

# Values at the start and end of each line
for series in (pretax_adjusted, posttax_adjusted):
    ax.annotate(f'{series[0]:.1f}%', xy=(START, series[0]), xytext=(10, 0), textcoords='offset points',
                va='center', fontsize=ANNOTATION_SIZE, color='#222')
    ax.annotate(f'{series[-1]:.1f}%', xy=(END, series[-1]), xytext=(12, 0), textcoords='offset points',
                va='center', fontsize=ANNOTATION_SIZE, color='#222')

# Formatting (no title: the heading is in the README above the figure)
ax.set_xlabel('Year', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
ax.set_ylabel('Corporate profits after depreciation (% of GDI)', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
ax.set_xlim(START, END + 3)
ax.set_xticks(range(START, END + 1, 5))
ax.tick_params(axis='both', labelsize=TICK_SIZE)
ax.tick_params(axis='x', pad=10)
ax.set_ylim(4, 20)
ax.set_yticks(range(4, 21, 2))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.legend(loc='upper left', fontsize=LEGEND_SIZE, framealpha=0.95)

fig.text(0.5, 0.01,
         'Source: BEA NIPA bulk data (Tables 1.10 and 1.12). Corporate profits without IVA/CCAdj, which are after depreciation '
         'as firms report it for tax,\nplus ⅓ of proprietors\' income (Johnson 1954). Excludes rental income and net interest, '
         'which go to property owners and lenders.',
         ha='center', fontsize=SOURCE_SIZE, color='#555')

plt.tight_layout()
plt.subplots_adjust(bottom=0.12)

for ext in ('png', 'pdf'):
    kw = {'dpi': 150} if ext == 'png' else {}
    plt.savefig(os.path.join(ROOT, 'figures', f'capital_share.{ext}'), bbox_inches='tight',
                facecolor='white', edgecolor='none', **kw)
plt.close()

print("Figure 3 saved: figures/capital_share.png and figures/capital_share.pdf")
print(f"\nSummary:")
print(f"Pre-tax corporate profit share: {pretax_adjusted[0]:.1f}% ({START}) → {pretax_adjusted[-1]:.1f}% ({END}), "
      f"{pretax_adjusted[-1] - pretax_adjusted[0]:+.1f} pp")
print(f"Post-tax corporate profit share: {posttax_adjusted[0]:.1f}% ({START}) → {posttax_adjusted[-1]:.1f}% ({END}), "
      f"{posttax_adjusted[-1] - posttax_adjusted[0]:+.1f} pp")
