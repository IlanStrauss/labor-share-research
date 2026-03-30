#!/usr/bin/env python3
"""
Generate Figure 3: Corporate Profit Share chart.
Shows pre-tax and post-tax corporate profit share (excluding rent and interest),
plus 1/3 of proprietors' income per Gollin (2002).

Data sources: BEA NIPA Table 1.11 via FRED
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# === DATA ===
# Years for the time series
years = [1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]

# Corporate Profits Before Tax (without IVA/CCAdj) as % of GDI
# Calculated from: A053RC1A027NBEA / GDIA * 100
# Source: FRED, verified January 2026
corp_profits_pretax = [8.1, 7.5, 7.2, 7.4, 6.8, 8.5, 8.3, 10.5, 10.8, 11.5, 11.0, 14.4]

# Corporate Profits After Tax (without IVA/CCAdj) as % of GDI
# Calculated from: A055RC1A027NBEA / GDIA * 100
# Source: FRED, verified January 2026
corp_profits_posttax = [5.2, 4.5, 4.5, 4.8, 4.5, 6.2, 5.8, 8.2, 8.6, 9.5, 9.0, 12.1]

# Proprietors' Income as % of GDI (A041RE1A156NBEA)
# Source: BEA NIPA Table 1.11 via FRED
prop_income = [7.8, 6.9, 6.2, 6.6, 7.0, 7.4, 7.6, 8.4, 7.6, 7.4, 7.5, 7.0]

# === CALCULATE GOLLIN-ADJUSTED CORPORATE PROFIT SHARE ===
# Add 1/3 of proprietors' income (the capital portion per Gollin 2002)
alpha = 1/3

pretax_adjusted = [cp + (alpha * pi) for cp, pi in zip(corp_profits_pretax, prop_income)]
posttax_adjusted = [cp + (alpha * pi) for cp, pi in zip(corp_profits_posttax, prop_income)]

# === CREATE FIGURE ===
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 7))

# Plot lines
ax.plot(years, pretax_adjusted, 'o-', linewidth=2.5, markersize=7,
        color='#16a34a', label='Pre-Tax Corporate Profit Share')

ax.plot(years, posttax_adjusted, 's-', linewidth=2.5, markersize=7,
        color='#f97316', label='Post-Tax Corporate Profit Share')

# Add reference line at 10%
ax.axhline(y=10, color='gray', linestyle=':', alpha=0.5, linewidth=1)
ax.axhline(y=15, color='gray', linestyle=':', alpha=0.5, linewidth=1)

# Annotations
ax.annotate(f'2024: {pretax_adjusted[-1]:.1f}%',
            xy=(2024, pretax_adjusted[-1]), xytext=(2018, pretax_adjusted[-1] + 1.5),
            fontsize=9, color='#16a34a',
            arrowprops=dict(arrowstyle='->', color='#16a34a', lw=1.2))

ax.annotate(f'2024: {posttax_adjusted[-1]:.1f}%',
            xy=(2024, posttax_adjusted[-1]), xytext=(2018, posttax_adjusted[-1] - 1.5),
            fontsize=9, color='#f97316',
            arrowprops=dict(arrowstyle='->', color='#f97316', lw=1.2))

ax.annotate(f'1970: {pretax_adjusted[0]:.1f}%',
            xy=(1970, pretax_adjusted[0]), xytext=(1974, pretax_adjusted[0] + 1.5),
            fontsize=9, color='#16a34a',
            arrowprops=dict(arrowstyle='->', color='#16a34a', lw=1.2))

# Formatting
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Corporate Profit Share of GDI (%)', fontsize=12, fontweight='bold')
ax.set_title('Figure 3. Corporate Profit Share Rose as Labor Share Fell (1970-2024)',
             fontsize=14, fontweight='bold', pad=20)

ax.set_xlim(1968, 2028)
ax.set_ylim(5, 20)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

# Legend
ax.legend(loc='upper left', fontsize=10, framealpha=0.95)

# Add source note
fig.text(0.5, 0.02,
         'Source: BEA NIPA Table 1.11 via FRED. Corporate profits (without IVA/CCAdj) + ⅓ × Proprietors\' Income.\n'
         'Excludes rental income and net interest, which go to property owners and lenders respectively.',
         ha='center', fontsize=9, color='#444')

# Add key finding box
textstr = f'Change 1970→2024:\nPre-tax: +{pretax_adjusted[-1] - pretax_adjusted[0]:.1f} pp\nPost-tax: +{posttax_adjusted[-1] - posttax_adjusted[0]:.1f} pp'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.97, 0.05, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)

# Save to figures directory
plt.savefig('figures/capital_share.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('figures/capital_share.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')

print("Figure 3 saved: figures/capital_share.png and figures/capital_share.pdf")

# Print summary statistics
print(f"\nSummary:")
print(f"Pre-tax corporate profit share: {pretax_adjusted[0]:.1f}% (1970) → {pretax_adjusted[-1]:.1f}% (2024), +{pretax_adjusted[-1] - pretax_adjusted[0]:.1f} pp")
print(f"Post-tax corporate profit share: {posttax_adjusted[0]:.1f}% (1970) → {posttax_adjusted[-1]:.1f}% (2024), +{posttax_adjusted[-1] - posttax_adjusted[0]:.1f} pp")
