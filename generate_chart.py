#!/usr/bin/env python3
"""
Generate labor share comparison charts showing different measurement approaches.
Focus: 1970-2024 period (post-war peak to present)
Data sources: BEA NIPA, Penn World Table via FRED

Charts produced:
1. Gross labor share comparison (main chart)
2. Net vs Gross labor share (depreciation effect)
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# === DATA: 1970-2024 (Annual) ===
# All data verified against FRED (January 2026)

# Years for all BEA series (1970-2024)
years = list(range(1970, 2025))

# BEA Compensation of Employees as % of GDI (A4002E1A156NBEA)
# This is GROSS labor share - includes wages + supplements (benefits + employer social insurance)
bea_comp = [
    58.4, 57.6, 57.5, 57.3, 57.7, 56.7, 56.6, 56.5, 56.6, 57.2,  # 1970-1979
    57.7, 56.6, 56.8, 56.3, 55.5, 55.7, 56.5, 56.6, 56.3, 56.4,  # 1980-1989
    57.0, 56.9, 57.3, 57.0, 56.1, 55.7, 55.2, 55.0, 55.7, 56.0,  # 1990-1999
    56.6, 56.5, 55.8, 55.4, 55.0, 54.0, 53.4, 54.6, 55.3, 54.4,  # 2000-2009
    53.0, 52.7, 52.3, 52.3, 52.2, 52.8, 53.2, 53.4, 53.3, 53.3,  # 2010-2019
    54.6, 53.1, 51.7, 51.8, 51.9                                   # 2020-2024
]

# BEA Depreciation (Consumption of Fixed Capital) as % of GDI (A262RE1A156NBEA)
bea_dep = [
    12.8, 12.9, 12.7, 12.6, 13.5, 14.3, 14.0, 14.1, 14.1, 14.5,  # 1970-1979
    15.2, 15.4, 16.1, 15.7, 15.0, 14.9, 15.2, 15.2, 15.0, 15.0,  # 1980-1989
    15.1, 15.4, 15.0, 15.0, 14.8, 14.9, 14.7, 14.5, 14.4, 14.5,  # 1990-1999
    14.6, 15.0, 15.1, 15.0, 14.9, 15.1, 15.1, 15.6, 16.2, 16.6,  # 2000-2009
    16.0, 15.8, 15.7, 15.9, 15.9, 15.9, 16.0, 16.1, 16.1, 16.2,  # 2010-2019
    17.0, 16.3, 16.5, 16.6, 16.5                                   # 2020-2024
]

# BEA Proprietors' Income as % of GDI (A041RE1A156NBEA)
bea_prop = [
    7.3, 7.3, 7.5, 7.9, 7.3, 7.1, 7.1, 7.0, 7.1, 6.9,  # 1970-1979
    6.1, 5.7, 5.1, 5.2, 5.7, 5.6, 5.7, 6.0, 6.2, 6.1,  # 1980-1989
    6.0, 5.8, 6.2, 6.4, 6.4, 6.4, 6.8, 6.8, 7.0, 7.2,  # 1990-1999
    7.3, 7.8, 7.9, 7.8, 7.9, 7.5, 7.5, 6.9, 6.6, 6.6,  # 2000-2009
    7.4, 7.9, 7.9, 8.0, 7.7, 7.3, 7.2, 7.3, 7.3, 7.2,  # 2010-2019
    7.5, 7.7, 7.2, 7.1, 7.0                             # 2020-2024
]

# BEA Wages and Salaries only as % of GDI (W270RE1A156NBEA)
# This excludes supplements (benefits, employer social insurance)
bea_wages = [
    51.6, 50.6, 50.2, 49.9, 50.2, 48.7, 48.5, 48.2, 48.1, 48.5,  # 1970-1979
    48.8, 47.7, 47.6, 46.9, 46.2, 46.3, 46.7, 46.9, 46.6, 46.3,  # 1980-1989
    46.7, 46.4, 46.3, 45.9, 45.3, 45.3, 45.1, 45.2, 45.8, 46.1,  # 1990-1999
    46.6, 46.3, 45.3, 44.7, 44.2, 43.4, 43.1, 44.2, 44.8, 43.7,  # 2000-2009
    42.5, 42.4, 42.2, 42.0, 42.1, 42.7, 43.1, 43.3, 43.2, 43.4,  # 2010-2019
    44.5, 43.5, 42.7, 42.7, 42.7                                   # 2020-2024
]

# Penn World Table Labor Share (LABSHPUSA156NRUG) - 1970-2019 only
# Note: PWT uses different methodology (imputes self-employment labor income)
pwt_years = list(range(1970, 2020))
pwt_labsh_raw = [
    0.6490, 0.6376, 0.6394, 0.6407, 0.6410, 0.6256, 0.6216, 0.6216, 0.6223, 0.6226,  # 1970-1979
    0.6243, 0.6142, 0.6167, 0.6039, 0.6020, 0.6023, 0.6077, 0.6160, 0.6207, 0.6119,  # 1980-1989
    0.6152, 0.6151, 0.6200, 0.6142, 0.6080, 0.6074, 0.6071, 0.6096, 0.6230, 0.6260,  # 1990-1999
    0.6371, 0.6403, 0.6296, 0.6214, 0.6171, 0.6056, 0.6055, 0.6040, 0.6041, 0.5911,  # 2000-2009
    0.5880, 0.5927, 0.5951, 0.5931, 0.5943, 0.5956, 0.5938, 0.5962, 0.5943, 0.5971   # 2010-2019
]
pwt_labsh = [x * 100 for x in pwt_labsh_raw]  # Convert to percentage

# === CALCULATED MEASURES ===

# Net Labor Share = Compensation / (100 - Depreciation)
# This is labor's share of Net Domestic Income (NDI = GDI - Depreciation)
net_labor_share = [comp / (100 - dep) * 100 for comp, dep in zip(bea_comp, bea_dep)]

# Adjusted Labor Share (with 2/3 of proprietors' income allocated to labor)
# Following Gollin (2002) methodology
alpha = 0.67
adj_labor_share = [comp + (alpha * prop) for comp, prop in zip(bea_comp, bea_prop)]

# Supplements (benefits + employer social insurance) = Compensation - Wages
supplements = [comp - wage for comp, wage in zip(bea_comp, bea_wages)]

# === EMPLOYER SOCIAL INSURANCE SHARE CALCULATION ===
# Note: BEA "employer contributions for government social insurance" is broader than FICA alone -
# it includes FICA (Social Security + Medicare) plus smaller programs (unemployment insurance, etc.)
# We use FICA rates as a proxy since FICA is the dominant component (~90%+ of the total)
# Historical employer FICA rates (OASDI + Medicare combined)
# Source: SSA.gov, Tax Policy Center, milefoot.com
# These are statutory rates; actual share is lower due to wage base cap
employer_fica_rates = {
    1970: 4.80, 1971: 5.20, 1972: 5.20, 1973: 5.85, 1974: 5.85,
    1975: 5.85, 1976: 5.85, 1977: 5.85, 1978: 6.05, 1979: 6.13,
    1980: 6.13, 1981: 6.65, 1982: 6.70, 1983: 6.70, 1984: 7.00,
    1985: 7.05, 1986: 7.15, 1987: 7.15, 1988: 7.51, 1989: 7.51,
}
# From 1990 onward, rate stabilized at 7.65% (6.2% OASDI + 1.45% Medicare)
for y in range(1990, 2025):
    employer_fica_rates[y] = 7.65

# Calculate employer FICA share of GDI
# Formula: employer_fica_share ≈ rate × (wages_share / 100) × adjustment_factor
# The adjustment factor (~0.92) accounts for the Social Security wage base cap
# Calibrated to match 2024 actual data: $866B FICA / $29,002B GDI = 2.99%
# Theoretical 2024: 7.65% × 42.7% = 3.27%, so adjustment = 2.99/3.27 = 0.91
WAGE_CAP_ADJUSTMENT = 0.91

employer_fica_share = []
for i, year in enumerate(years):
    rate = employer_fica_rates[year] / 100  # Convert % to decimal
    wages_share_decimal = bea_wages[i] / 100
    theoretical = rate * wages_share_decimal * 100  # Back to % of GDI
    adjusted = theoretical * WAGE_CAP_ADJUSTMENT
    employer_fica_share.append(adjusted)

# Compensation excluding employer FICA (wages + benefits only)
# This is "pre-payroll-tax" labor share - excludes employer portion of FICA
comp_ex_fica = [comp - fica for comp, fica in zip(bea_comp, employer_fica_share)]

# === TAXES ON PRODUCTION (approximate, for capital share calculation) ===
# BEA Taxes on Production and Imports less Subsidies as % of GDI
# Source: BEA NIPA Table 1.11 (estimated from available years)
taxes_on_prod = [
    7.0, 6.9, 6.9, 6.7, 7.2, 7.2, 7.1, 6.9, 6.8, 6.7,  # 1970-1979
    6.8, 7.0, 7.0, 7.0, 6.9, 6.8, 6.6, 6.6, 6.5, 6.4,  # 1980-1989
    6.4, 6.6, 6.6, 6.6, 6.6, 6.6, 6.5, 6.4, 6.5, 6.4,  # 1990-1999
    6.3, 6.3, 6.5, 6.5, 6.5, 6.6, 6.6, 6.6, 6.3, 6.1,  # 2000-2009
    6.3, 6.4, 6.5, 6.4, 6.4, 6.5, 6.5, 6.5, 6.5, 6.6,  # 2010-2019
    6.4, 6.4, 6.5, 6.6, 6.7                             # 2020-2024
]

# === CORPORATE PROFITS (before and after tax) ===
# BEA Corporate Profits with IVA and CCAdj, domestic industries as % of GDI (A445RE1A156NBEA)
# These are PRE-corporate income tax
corp_profits_pretax = [
    7.4, 7.6, 8.0, 8.8, 7.0, 7.2, 8.0, 8.2, 8.3, 7.9,  # 1970-1979
    6.2, 6.6, 5.3, 5.9, 6.7, 6.2, 5.8, 6.4, 6.8, 6.5,  # 1980-1989
    6.0, 5.8, 5.7, 6.4, 7.1, 8.0, 8.2, 8.3, 7.6, 7.5,  # 1990-1999
    7.3, 6.6, 6.8, 7.5, 8.6, 9.6, 10.2, 8.2, 6.9, 8.2,  # 2000-2009
    9.6, 9.6, 10.2, 10.2, 10.0, 9.3, 9.1, 9.4, 9.4, 9.5,  # 2010-2019
    9.3, 11.4, 11.2, 11.4, 11.5                          # 2020-2024
]

# BEA Corporate Profits AFTER tax with IVA and CCAdj as % of GDI (W273RE1A156NBEA)
corp_profits_aftertax = [
    4.7, 4.9, 5.2, 5.8, 4.2, 4.4, 5.1, 5.3, 5.4, 4.9,  # 1970-1979
    3.8, 4.2, 3.2, 3.9, 4.5, 4.0, 3.6, 4.3, 4.7, 4.4,  # 1980-1989
    4.0, 3.8, 3.8, 4.4, 5.1, 5.9, 6.1, 6.3, 5.7, 5.6,  # 1990-1999
    5.4, 4.6, 4.9, 5.7, 6.8, 7.7, 8.2, 6.3, 5.0, 6.5,  # 2000-2009
    7.7, 7.6, 8.2, 8.2, 7.9, 7.3, 7.2, 7.5, 7.5, 7.6,  # 2010-2019
    7.8, 9.4, 8.9, 9.2, 9.2                              # 2020-2024
]

# === CAPITAL SHARE CALCULATIONS ===
# Net Operating Surplus (NOS) = GDI - Compensation - Depreciation - Taxes on Production
# This is capital income BEFORE corporate income taxes (includes profits, interest, rent)
nos_share = [100 - comp - dep - tax for comp, dep, tax in zip(bea_comp, bea_dep, taxes_on_prod)]

# Net Operating Surplus after corporate income taxes (rough approximation)
# NOS_aftertax ≈ NOS - (Pretax profits - Aftertax profits)
corp_tax_share = [pre - post for pre, post in zip(corp_profits_pretax, corp_profits_aftertax)]
nos_aftertax_share = [nos - ctax for nos, ctax in zip(nos_share, corp_tax_share)]

# Depreciation-adjusted capital share = NOS / NDI
# Where NDI = GDI - Depreciation
nos_depr_adjusted = [nos / (100 - dep) * 100 for nos, dep in zip(nos_share, bea_dep)]

# === HISTORICAL CONTEXT (for reference in text, not in main chart) ===
# 1929 values for comparison (mentioned briefly in analysis)
hist_1929 = {
    'compensation': 49.5,
    'depreciation': 10.0,
    'proprietors': 13.5,
    'wages': 48.6,
}

# === CHART STYLING ===
plt.style.use('seaborn-v0_8-whitegrid')

# Color palette
COLORS = {
    'gross': '#2563eb',      # Blue - BEA Gross
    'net': '#dc2626',        # Red - Net (depreciation-adjusted)
    'pwt': '#16a34a',        # Green - Penn World Table
    'adjusted': '#9333ea',   # Purple - With proprietors' adjustment
    'ex_fica': '#db2777',    # Pink/Magenta - Compensation ex-social insurance (distinct from green)
    'wages': '#f59e0b',      # Amber - Wages only
    'depreciation': '#6b7280' # Gray - Depreciation
}

# === INCREASED SIZES FOR BETTER READABILITY ===
LINE_WIDTH = 7.0          # Much thicker lines (doubled from 3.5)
LINE_ALPHA = 0.75         # Semi-transparent for overlapping visibility
MARKER_SIZE = 10          # Bigger markers
TITLE_SIZE = 22           # Bigger title
AXIS_LABEL_SIZE = 18      # Bigger axis labels
TICK_SIZE = 16            # Much bigger tick labels (year numbers, percentages)
LEGEND_SIZE = 16          # Much bigger legend
ANNOTATION_SIZE = 14      # Bigger annotations
SOURCE_SIZE = 12          # Bigger source note


def create_main_chart():
    """
    Figure 1: Gross Labor Share Comparison (1970-2024)
    Focus on the post-war peak to present period
    """
    fig, ax = plt.subplots(figsize=(16, 10))

    # Plot main series (with alpha for transparency where lines overlap)
    ax.plot(years, bea_comp, '-', linewidth=LINE_WIDTH, color=COLORS['gross'],
            label='BEA: Total Compensation / GDI (Gross)', marker='o', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    ax.plot(pwt_years, pwt_labsh, '-', linewidth=LINE_WIDTH, color=COLORS['pwt'],
            label='Penn World Table: Labor Share', marker='s', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    ax.plot(years, adj_labor_share, '-', linewidth=LINE_WIDTH, color=COLORS['adjusted'],
            label='Adjusted: + ⅔ Proprietors\' Income', marker='d', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    ax.plot(years, comp_ex_fica, '-', linewidth=LINE_WIDTH, color=COLORS['ex_fica'],
            label='Wages + Benefits (excl. employer social insurance)', marker='P', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    ax.plot(years, bea_wages, '-', linewidth=LINE_WIDTH, color=COLORS['wages'],
            label='Wages Only (excl. all supplements)', marker='^', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    # Reference lines
    ax.axhline(y=50, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)
    ax.axhline(y=55, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)
    ax.axhline(y=60, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)

    # Annotations
    ax.annotate('1970 Peak\n(58.4%)', xy=(1970, 58.4), xytext=(1974, 62),
                fontsize=ANNOTATION_SIZE, color=COLORS['gross'], ha='center', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['gross'], lw=2))

    ax.annotate('2024\n(51.9%)', xy=(2024, 51.9), xytext=(2020, 48),
                fontsize=ANNOTATION_SIZE, color=COLORS['gross'], ha='center', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['gross'], lw=2))

    # Formatting
    ax.set_xlabel('Year', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    ax.set_ylabel('Labor Share of GDI (%)', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    ax.set_title('Figure 1. Labor Share Declined Across All Measures Since 1970 Peak\n(U.S. Gross Labor Share of GDI, 1970-2024)',
                 fontsize=TITLE_SIZE, fontweight='bold', pad=20)

    # X-axis: every 5 years
    ax.set_xlim(1968, 2026)
    ax.set_xticks(range(1970, 2030, 5))
    ax.set_xticklabels([str(y) for y in range(1970, 2030, 5)], fontsize=TICK_SIZE)

    # Y-axis
    ax.set_ylim(40, 70)
    ax.set_yticks(range(40, 75, 5))
    ax.tick_params(axis='y', labelsize=TICK_SIZE)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    # Legend
    ax.legend(loc='upper right', fontsize=LEGEND_SIZE, framealpha=0.95)

    # Source note
    fig.text(0.5, 0.02,
             'Sources: BEA NIPA Table 1.11 (FRED: A4002E1A156NBEA, W270RE1A156NBEA, A041RE1A156NBEA); '
             'Penn World Table 10.01 (FRED: LABSHPUSA156NRUG)',
             ha='center', fontsize=SOURCE_SIZE, color='#555')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.10)

    plt.savefig('labor_share_gross.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('labor_share_gross.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    print("Saved: labor_share_gross.png/pdf")


def create_depreciation_chart():
    """
    Figure 2: Gross vs Depreciation-Adjusted Labor Share (1970-2024)
    Simple comparison - single y-axis, no dual-axis nonsense
    """
    fig, ax = plt.subplots(figsize=(16, 10))

    # Plot gross and depreciation-adjusted series (with alpha for transparency)
    ax.plot(years, bea_comp, '-', linewidth=LINE_WIDTH, color=COLORS['gross'],
            label='Gross Labor Share (Compensation / GDI)', marker='o', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    ax.plot(years, net_labor_share, '-', linewidth=LINE_WIDTH, color=COLORS['net'],
            label='Depreciation-Adjusted (Compensation / NDI)', marker='^', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    # Reference lines
    ax.axhline(y=55, color='gray', linestyle=':', alpha=0.4, linewidth=1.5)
    ax.axhline(y=60, color='gray', linestyle=':', alpha=0.4, linewidth=1.5)
    ax.axhline(y=65, color='gray', linestyle=':', alpha=0.4, linewidth=1.5)

    # Annotations
    ax.annotate('Gross: 58.4% → 51.9%\n(−6.5 pp decline)',
                xy=(1970, 58.4), xytext=(1978, 54),
                fontsize=ANNOTATION_SIZE, color=COLORS['gross'], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=COLORS['gross'], alpha=0.95),
                arrowprops=dict(arrowstyle='->', color=COLORS['gross'], lw=2))

    ax.annotate('Depreciation-Adjusted:\n67.0% → 62.2% (−4.8 pp decline)',
                xy=(1970, 67.0), xytext=(1978, 70),
                fontsize=ANNOTATION_SIZE, color=COLORS['net'], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=COLORS['net'], alpha=0.95),
                arrowprops=dict(arrowstyle='->', color=COLORS['net'], lw=2))

    # Key insight annotation
    ax.annotate('The gap widened because depreciation\nrose from 12.8% to 16.5% of GDI',
                xy=(2010, 58), fontsize=ANNOTATION_SIZE, color='#333', style='italic',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f0f0', edgecolor='#999', alpha=0.95))

    # Formatting
    ax.set_xlabel('Year', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    ax.set_ylabel('Labor Share (%)', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    ax.set_title('Figure 2. Depreciation-Adjusted Labor Share Also Declined, But Less Steeply\n(Gross vs. Depreciation-Adjusted, 1970-2024)',
                 fontsize=TITLE_SIZE, fontweight='bold', pad=20)

    # X-axis: every 5 years
    ax.set_xlim(1968, 2026)
    ax.set_xticks(range(1970, 2030, 5))
    ax.set_xticklabels([str(y) for y in range(1970, 2030, 5)], fontsize=TICK_SIZE)

    # Y-axis
    ax.set_ylim(48, 72)
    ax.set_yticks(range(50, 75, 5))
    ax.tick_params(axis='y', labelsize=TICK_SIZE)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    # Legend
    ax.legend(loc='lower left', fontsize=LEGEND_SIZE, framealpha=0.95)

    # Source note
    fig.text(0.5, 0.02,
             'Sources: BEA NIPA Table 1.11 (FRED: A4002E1A156NBEA, A262RE1A156NBEA). '
             'NDI = GDI − Depreciation (Consumption of Fixed Capital).',
             ha='center', fontsize=SOURCE_SIZE, color='#555')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.10)

    plt.savefig('labor_share_net_vs_gross.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('labor_share_net_vs_gross.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    print("Saved: labor_share_net_vs_gross.png/pdf")


def create_capital_share_chart():
    """
    Figure 3: Capital Share (Net Operating Surplus) 1970-2024
    Shows capital's share after deducting labor costs, depreciation, and production taxes
    """
    fig, ax = plt.subplots(figsize=(16, 10))

    # Plot capital share measures (with alpha for transparency)
    ax.plot(years, nos_share, '-', linewidth=LINE_WIDTH, color='#059669',  # Emerald green
            label='Net Operating Surplus / GDI (pre-corporate tax)', marker='o', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    ax.plot(years, nos_aftertax_share, '-', linewidth=LINE_WIDTH, color='#0d9488',  # Teal
            label='Net Operating Surplus / GDI (post-corporate tax)', marker='s', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    ax.plot(years, corp_profits_pretax, '--', linewidth=LINE_WIDTH-1, color='#6366f1',  # Indigo
            label='Corporate Profits / GDI (pre-tax)', marker='^', markersize=MARKER_SIZE-2,
            markevery=5, alpha=0.7)

    # Reference lines
    ax.axhline(y=20, color='gray', linestyle=':', alpha=0.4, linewidth=1.5)
    ax.axhline(y=25, color='gray', linestyle=':', alpha=0.4, linewidth=1.5)

    # Annotations
    ax.annotate(f'NOS: {nos_share[0]:.1f}% → {nos_share[-1]:.1f}%\n(+{nos_share[-1]-nos_share[0]:.1f} pp)',
                xy=(1975, nos_share[5]), fontsize=ANNOTATION_SIZE, color='#059669', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#059669', alpha=0.95))

    ax.annotate(f'Corporate Profits:\n{corp_profits_pretax[0]:.1f}% → {corp_profits_pretax[-1]:.1f}%',
                xy=(2010, 12), fontsize=ANNOTATION_SIZE, color='#6366f1', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#6366f1', alpha=0.95))

    # Formatting
    ax.set_xlabel('Year', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    ax.set_ylabel('Share of GDI (%)', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    # Title removed - heading is in README above the figure

    # X-axis: every 5 years
    ax.set_xlim(1968, 2026)
    ax.set_xticks(range(1970, 2030, 5))
    ax.set_xticklabels([str(y) for y in range(1970, 2030, 5)], fontsize=TICK_SIZE)

    # Y-axis
    ax.set_ylim(0, 32)
    ax.set_yticks(range(0, 35, 5))
    ax.tick_params(axis='y', labelsize=TICK_SIZE)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    # Legend
    ax.legend(loc='upper left', fontsize=LEGEND_SIZE, framealpha=0.95)

    # Source note
    fig.text(0.5, 0.02,
             'Source: BEA NIPA Table 1.11 via FRED. NOS = 100% − Compensation − Depreciation − Taxes on Production. '
             'Corporate tax = pretax profits − after-tax profits.',
             ha='center', fontsize=SOURCE_SIZE, color='#555')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.10)

    plt.savefig('capital_share.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('capital_share.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    print("Saved: capital_share.png/pdf")


def create_combined_chart():
    """
    Figure 4: Combined overview (for backward compatibility with original README)
    """
    fig, ax = plt.subplots(figsize=(16, 10))

    # Plot all main series (with alpha for transparency)
    ax.plot(years, bea_comp, '-', linewidth=LINE_WIDTH, color=COLORS['gross'],
            label='BEA: Compensation / GDI (Gross)', marker='o', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    ax.plot(pwt_years, pwt_labsh, '-', linewidth=LINE_WIDTH, color=COLORS['pwt'],
            label='Penn World Table', marker='s', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    ax.plot(years, net_labor_share, '-', linewidth=LINE_WIDTH, color=COLORS['net'],
            label='Depreciation-adjusted', marker='^', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    ax.plot(years, adj_labor_share, '-', linewidth=LINE_WIDTH, color=COLORS['adjusted'],
            label='Adjusted: + ⅔ Proprietors\' Income', marker='d', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    # Reference lines
    ax.axhline(y=50, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)
    ax.axhline(y=60, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)

    # Annotations
    ax.annotate('1970 Peak', xy=(1970, 58.4), xytext=(1975, 55),
                fontsize=ANNOTATION_SIZE, color=COLORS['gross'], fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['gross'], lw=2))

    # Formatting
    ax.set_xlabel('Year', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    ax.set_ylabel('Labor Share (%)', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    ax.set_title('U.S. Labor Share of GDI: Multiple Measures (1970-2024)',
                 fontsize=TITLE_SIZE, fontweight='bold', pad=20)

    # X-axis: every 5 years
    ax.set_xlim(1968, 2026)
    ax.set_xticks(range(1970, 2030, 5))
    ax.set_xticklabels([str(y) for y in range(1970, 2030, 5)], fontsize=TICK_SIZE)

    # Y-axis
    ax.set_ylim(48, 72)
    ax.tick_params(axis='y', labelsize=TICK_SIZE)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    # Legend
    ax.legend(loc='upper right', fontsize=LEGEND_SIZE, framealpha=0.95)

    # Source note
    fig.text(0.5, 0.02,
             'Sources: BEA NIPA Table 1.11; Penn World Table 10.01 via FRED',
             ha='center', fontsize=SOURCE_SIZE, color='#555')

    # Methodology note
    note_text = ("Gross = Comp/GDI  |  Net = Comp/(GDI−Depreciation)  |  "
                 "Adjusted = Comp + ⅔×Proprietors' Income")
    fig.text(0.5, 0.05, note_text, ha='center', fontsize=SOURCE_SIZE, color='#444', style='italic')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12)

    plt.savefig('labor_share_comparison.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('labor_share_comparison.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    print("Saved: labor_share_comparison.png/pdf")


def print_summary_stats():
    """Print key statistics for the README"""
    print("\n" + "="*60)
    print("KEY STATISTICS (1970-2024)")
    print("="*60)

    # 1970 and 2024 values
    idx_1970 = 0
    idx_2024 = -1

    print(f"\nGross Labor Share (Compensation/GDI):")
    print(f"  1970: {bea_comp[idx_1970]:.1f}%")
    print(f"  2024: {bea_comp[idx_2024]:.1f}%")
    print(f"  Change: {bea_comp[idx_2024] - bea_comp[idx_1970]:+.1f} pp")

    print(f"\nNet Labor Share (Compensation/NDI):")
    print(f"  1970: {net_labor_share[idx_1970]:.1f}%")
    print(f"  2024: {net_labor_share[idx_2024]:.1f}%")
    print(f"  Change: {net_labor_share[idx_2024] - net_labor_share[idx_1970]:+.1f} pp")

    print(f"\nDepreciation Share:")
    print(f"  1970: {bea_dep[idx_1970]:.1f}%")
    print(f"  2024: {bea_dep[idx_2024]:.1f}%")
    print(f"  Change: {bea_dep[idx_2024] - bea_dep[idx_1970]:+.1f} pp")

    print(f"\nWages Only (excl. supplements):")
    print(f"  1970: {bea_wages[idx_1970]:.1f}%")
    print(f"  2024: {bea_wages[idx_2024]:.1f}%")
    print(f"  Change: {bea_wages[idx_2024] - bea_wages[idx_1970]:+.1f} pp")

    print(f"\nSupplements (benefits + employer social insurance):")
    print(f"  1970: {supplements[idx_1970]:.1f}%")
    print(f"  2024: {supplements[idx_2024]:.1f}%")
    print(f"  Change: {supplements[idx_2024] - supplements[idx_1970]:+.1f} pp")

    print(f"\nEmployer Social Insurance Share (estimated from FICA rates):")
    print(f"  1970: {employer_fica_share[idx_1970]:.1f}%")
    print(f"  2024: {employer_fica_share[idx_2024]:.1f}%")
    print(f"  Change: {employer_fica_share[idx_2024] - employer_fica_share[idx_1970]:+.1f} pp")

    print(f"\nCompensation ex-Social Insurance (Wages + Benefits only):")
    print(f"  1970: {comp_ex_fica[idx_1970]:.1f}%")
    print(f"  2024: {comp_ex_fica[idx_2024]:.1f}%")
    print(f"  Change: {comp_ex_fica[idx_2024] - comp_ex_fica[idx_1970]:+.1f} pp")

    print(f"\nHistorical Reference (1929):")
    print(f"  Gross labor share: {hist_1929['compensation']:.1f}%")
    print(f"  Net labor share: {hist_1929['compensation']/(100-hist_1929['depreciation'])*100:.1f}%")
    print(f"  Depreciation: {hist_1929['depreciation']:.1f}%")

    print("\n" + "="*60)


if __name__ == "__main__":
    print("Generating labor share charts...")
    print("-" * 40)

    create_main_chart()
    create_depreciation_chart()
    create_capital_share_chart()
    create_combined_chart()

    print_summary_stats()

    print("\nAll charts generated successfully!")
