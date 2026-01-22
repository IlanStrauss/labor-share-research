#!/usr/bin/env python3
"""
Generate labor share comparison chart showing different measurement approaches.
Data sources: BEA NIPA, Penn World Table via FRED
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# === DATA ===
# All data verified against FRED (January 2026)

# BEA Compensation of Employees as % of GDI (A4002E1A156NBEA)
bea_years = [1929, 1935, 1940, 1945, 1950, 1955, 1960, 1965, 1970, 1975,
             1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]
bea_comp = [49.5, 50.6, 51.8, 56.4, 53.0, 54.5, 55.4, 54.7, 58.4, 56.7,
            57.7, 55.7, 57.0, 55.7, 56.6, 54.0, 53.0, 52.8, 54.6, 51.9]

# BEA Depreciation as % of GDI (A262RE1A156NBEA)
bea_dep = [10.0, 11.4, 10.4, 10.3, 11.2, 11.5, 12.5, 11.9, 12.8, 14.3,
           15.2, 14.9, 15.1, 14.9, 14.6, 15.1, 16.0, 15.9, 17.0, 16.5]

# BEA Proprietors' Income as % of GDI (A041RE1A156NBEA)
bea_prop = [13.5, 13.3, 12.1, 12.3, 12.6, 11.5, 9.8, 9.6, 7.8, 6.9,
            6.2, 6.6, 7.0, 7.4, 7.6, 8.4, 7.6, 7.4, 7.5, 7.0]

# Penn World Table Labor Share (LABSHPUSA156NRUG) - only 1950-2019
pwt_years = [1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995,
             2000, 2005, 2010, 2015, 2019]
pwt_labsh = [62.8, 62.7, 63.7, 61.9, 64.9, 62.6, 62.4, 60.2, 61.5, 60.7,
             63.7, 60.6, 58.8, 59.6, 59.7]

# === CALCULATE DERIVED MEASURES ===

# Net Labor Share = Compensation / (100 - Depreciation)
net_labor_share = [comp / (100 - dep) * 100 for comp, dep in zip(bea_comp, bea_dep)]

# Adjusted Labor Share (with 2/3 of proprietors' income)
alpha = 0.67
adj_labor_share = [comp + (alpha * prop) for comp, prop in zip(bea_comp, bea_prop)]

# === CREATE FIGURE ===
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(14, 8))

# Plot lines
ax.plot(bea_years, bea_comp, 'o-', linewidth=2.5, markersize=6,
        color='#2563eb', label='BEA: Employee Compensation / GDI (Gross)')

ax.plot(pwt_years, pwt_labsh, 's-', linewidth=2.5, markersize=6,
        color='#16a34a', label='Penn World Table: Labor Share')

ax.plot(bea_years, net_labor_share, '^-', linewidth=2.5, markersize=6,
        color='#dc2626', label='Net Labor Share (adjusted for depreciation)')

ax.plot(bea_years, adj_labor_share, 'd-', linewidth=2.5, markersize=6,
        color='#9333ea', label='Adjusted: + 2/3 of Proprietors\' Income')

# Add reference lines
ax.axhline(y=50, color='gray', linestyle=':', alpha=0.5, linewidth=1)
ax.axhline(y=60, color='gray', linestyle=':', alpha=0.5, linewidth=1)

# Annotations for key events
ax.annotate('1970 Peak', xy=(1970, 58.4), xytext=(1972, 54),
            fontsize=9, color='#2563eb',
            arrowprops=dict(arrowstyle='->', color='#2563eb', lw=1.5))

ax.annotate('Post-2008\nDecline', xy=(2010, 53), xytext=(2015, 48),
            fontsize=9, color='#2563eb',
            arrowprops=dict(arrowstyle='->', color='#2563eb', lw=1.5))

# Formatting
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Labor Share (%)', fontsize=12, fontweight='bold')
ax.set_title('U.S. Labor Share of GDI (Whole Economy): Multiple Measurement Approaches (1929-2024)',
             fontsize=14, fontweight='bold', pad=20)

ax.set_xlim(1925, 2028)
ax.set_ylim(45, 75)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

# Legend
ax.legend(loc='upper left', fontsize=10, framealpha=0.95)

# Add source note
fig.text(0.5, 0.01,
         'Sources: BEA NIPA Table 1.11 (FRED: A4002E1A156NBEA, A262RE1A156NBEA, A041RE1A156NBEA); '
         'Penn World Table 10.01 (FRED: LABSHPUSA156NRUG)',
         ha='center', fontsize=9, color='#444')

# Add methodology note - positioned below chart in source area
note_text = "Key: Gross = Compensation/GDI  |  Net = Compensation/(GDI−Depreciation)  |  Adjusted = Comp. + ⅔×Proprietors' Income"
fig.text(0.5, 0.05, note_text, ha='center', fontsize=8, color='#555',
         style='italic')

plt.tight_layout()
plt.subplots_adjust(bottom=0.12)

# Save
plt.savefig('labor_share_comparison.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('labor_share_comparison.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')

print("Charts saved: labor_share_comparison.png and labor_share_comparison.pdf")
