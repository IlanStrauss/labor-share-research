#!/usr/bin/env python3
"""
Generate labor share comparison charts showing different measurement approaches.
Focus: 1970-2024 period (post-war peak to present)
Data sources: BEA NIPA (data/bea_nipa_extract.csv); Penn World Table 11.0 from DataverseNL
(data/pwt_labor_share.csv), both saved by fetch_data.py. Writes the plotted BEA series to
data/labor_share_measures.csv.

Charts produced:
1. Gross labor share comparison (main chart)
2. Net vs Gross labor share (depreciation effect)
"""

import csv
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bea_nipa import ROOT, load  # noqa: E402
from proprietors_split import labor_part  # noqa: E402

# === DATA: 1970-2024 (Annual), % of GDI ===
# BEA series come from the NIPA bulk file (bea_nipa.py); BEA series codes in brackets

START, END = 1970, 2024
years = list(range(START, END + 1))
d = load()


def gdi_share(*codes):
    return [100 * sum(d[c][y] for c in codes) / d['A261RC'][y] for y in years]


# Compensation of employees [A4002C]
# This is GROSS labor share - includes wages + supplements (benefits + employer social insurance)
bea_comp = gdi_share('A4002C')

# Depreciation (Consumption of Fixed Capital) [A262RC]
bea_dep = gdi_share('A262RC')

# Wages and salaries [W270RC]
# This excludes supplements (benefits, employer social insurance)
bea_wages = gdi_share('W270RC')

# Employer contributions for government social insurance [B039RC]
# Social Security and Medicare (FICA) plus smaller programs such as unemployment insurance
employer_social_insurance = gdi_share('B039RC')

# Penn World Table 11.0 labor share (labsh), from DataverseNL
# Note: PWT uses different methodology (imputes self-employment labor income)
with open(os.path.join(ROOT, 'data', 'pwt_labor_share.csv'), newline='') as f:
    pwt = {int(row['year']): float(row['labor_share_pct']) for row in csv.DictReader(f) if row['iso3c'] == 'USA'}
pwt_years = [y for y in sorted(pwt) if START <= y <= END]
pwt_labsh = [pwt[y] for y in pwt_years]

# === CALCULATED MEASURES ===

# Net Labor Share = Compensation / (100 - Depreciation)
# This is labor's share of Net Domestic Income (NDI = GDI - Depreciation)
net_labor_share = [comp / (100 - dep) * 100 for comp, dep in zip(bea_comp, bea_dep)]

# Adjusted Labor Share = compensation + the labor part of proprietors' income, which is split between
# labor and capital in the same ratio as the rest of the economy's income (Kravis's economy-wide basis;
# see proprietors_split.py)
adj_labor_share = [comp + 100 * labor_part(d, y) / d['A261RC'][y] for y, comp in zip(years, bea_comp)]

# Supplements (benefits + employer social insurance) = Compensation - Wages
supplements = [comp - wage for comp, wage in zip(bea_comp, bea_wages)]

# Compensation excluding employer social insurance (wages + benefits only)
comp_ex_fica = [comp - esi for comp, esi in zip(bea_comp, employer_social_insurance)]

# === HISTORICAL CONTEXT (for reference in text, not in main chart) ===
hist_1929 = {
    'compensation': 100 * d['A4002C'][1929] / d['A261RC'][1929],
    'depreciation': 100 * d['A262RC'][1929] / d['A261RC'][1929],
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
            label='Adjusted: + Labor Part of Proprietors\' Income', marker='d', markersize=MARKER_SIZE,
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
    ax.annotate(f'{START} Peak\n({bea_comp[0]:.1f}%)', xy=(START, bea_comp[0]), xytext=(START + 3.5, 67),
                fontsize=ANNOTATION_SIZE, color=COLORS['gross'], ha='center', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['gross'], lw=2))

    ax.annotate(f'{END}\n({bea_comp[-1]:.1f}%)', xy=(END, bea_comp[-1]), xytext=(END - 4, 47),
                fontsize=ANNOTATION_SIZE, color=COLORS['gross'], ha='center', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['gross'], lw=2))

    # Formatting
    ax.set_xlabel('Year', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    ax.set_ylabel('Labor Share of GDI (%)', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    # Title removed - heading is in README above the figure

    # X-axis: every 5 years
    ax.set_xlim(1970, 2024)
    ax.set_xticks(range(1970, 2025, 5))
    ax.set_xticklabels([str(y) for y in range(1970, 2025, 5)], fontsize=TICK_SIZE)

    # Y-axis
    ax.set_ylim(40, 70)
    ax.set_yticks(range(40, 75, 5))
    ax.tick_params(axis='y', labelsize=TICK_SIZE)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    # Legend
    ax.legend(loc='upper right', fontsize=LEGEND_SIZE, framealpha=0.95)

    # Source note
    fig.text(0.5, 0.02,
             'Sources: BEA NIPA bulk data (series A4002C, W270RC, B039RC, A041RC, A261RC, W056RC, A107RC, A262RC); '
             'Penn World Table 11.0 (DataverseNL)',
             ha='center', fontsize=SOURCE_SIZE, color='#555')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.10)

    plt.savefig(os.path.join(ROOT, 'figures', 'labor_share_gross.png'), dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(os.path.join(ROOT, 'figures', 'labor_share_gross.pdf'), bbox_inches='tight',
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
    ax.annotate(f'Gross: {bea_comp[0]:.1f}% → {bea_comp[-1]:.1f}%\n(−{bea_comp[0] - bea_comp[-1]:.1f} pp decline)',
                xy=(START, bea_comp[0]), xytext=(START + 8, 54),
                fontsize=ANNOTATION_SIZE, color=COLORS['gross'], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=COLORS['gross'], alpha=0.95),
                arrowprops=dict(arrowstyle='->', color=COLORS['gross'], lw=2))

    ax.annotate(f'Depreciation-Adjusted:\n{net_labor_share[0]:.1f}% → {net_labor_share[-1]:.1f}% '
                f'(−{net_labor_share[0] - net_labor_share[-1]:.1f} pp decline)',
                xy=(START, net_labor_share[0]), xytext=(START + 8, 70),
                fontsize=ANNOTATION_SIZE, color=COLORS['net'], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=COLORS['net'], alpha=0.95),
                arrowprops=dict(arrowstyle='->', color=COLORS['net'], lw=2))

    # Key insight annotation
    ax.annotate(f'The gap widened because depreciation\nrose from {bea_dep[0]:.1f}% to {bea_dep[-1]:.1f}% of GDI',
                xy=(2010, 58), fontsize=ANNOTATION_SIZE, color='#333', style='italic',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f0f0', edgecolor='#999', alpha=0.95))

    # Formatting
    ax.set_xlabel('Year', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    ax.set_ylabel('Labor Share (%)', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    # Title removed - heading is in README above the figure

    # X-axis: every 5 years
    ax.set_xlim(1970, 2024)
    ax.set_xticks(range(1970, 2025, 5))
    ax.set_xticklabels([str(y) for y in range(1970, 2025, 5)], fontsize=TICK_SIZE)

    # Y-axis
    ax.set_ylim(48, 72)
    ax.set_yticks(range(50, 75, 5))
    ax.tick_params(axis='y', labelsize=TICK_SIZE)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    # Legend
    ax.legend(loc='lower left', fontsize=LEGEND_SIZE, framealpha=0.95)

    # Source note
    fig.text(0.5, 0.02,
             'Source: BEA NIPA bulk data (series A4002C, A262RC, A261RC). '
             'NDI = GDI − Depreciation (Consumption of Fixed Capital).',
             ha='center', fontsize=SOURCE_SIZE, color='#555')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.10)

    plt.savefig(os.path.join(ROOT, 'figures', 'labor_share_net_vs_gross.png'), dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(os.path.join(ROOT, 'figures', 'labor_share_net_vs_gross.pdf'), bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    print("Saved: labor_share_net_vs_gross.png/pdf")


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
            label='Adjusted: + Labor Part of Proprietors\' Income', marker='d', markersize=MARKER_SIZE,
            markevery=5, alpha=LINE_ALPHA)

    # Reference lines
    ax.axhline(y=50, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)
    ax.axhline(y=60, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)

    # Annotations
    ax.annotate(f'{START} Peak', xy=(START, bea_comp[0]), xytext=(START + 5, 55),
                fontsize=ANNOTATION_SIZE, color=COLORS['gross'], fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['gross'], lw=2))

    # Formatting
    ax.set_xlabel('Year', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    ax.set_ylabel('Labor Share (%)', fontsize=AXIS_LABEL_SIZE, fontweight='bold')
    ax.set_title('U.S. Labor Share of GDI: Multiple Measures (1970-2024)',
                 fontsize=TITLE_SIZE, fontweight='bold', pad=20)

    # X-axis: every 5 years
    ax.set_xlim(1970, 2024)
    ax.set_xticks(range(1970, 2025, 5))
    ax.set_xticklabels([str(y) for y in range(1970, 2025, 5)], fontsize=TICK_SIZE)

    # Y-axis
    ax.set_ylim(48, 72)
    ax.tick_params(axis='y', labelsize=TICK_SIZE)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    # Legend
    ax.legend(loc='upper right', fontsize=LEGEND_SIZE, framealpha=0.95)

    # Source note
    fig.text(0.5, 0.02,
             'Sources: BEA NIPA bulk data; Penn World Table 11.0 (DataverseNL)',
             ha='center', fontsize=SOURCE_SIZE, color='#555')

    # Methodology note
    note_text = ("Gross = Comp/GDI  |  Net = Comp/(GDI−Depreciation)  |  "
                 "Adjusted = Comp + labor part of Proprietors' Income")
    fig.text(0.5, 0.05, note_text, ha='center', fontsize=SOURCE_SIZE, color='#444', style='italic')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12)

    plt.savefig(os.path.join(ROOT, 'figures', 'labor_share_comparison.png'), dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(os.path.join(ROOT, 'figures', 'labor_share_comparison.pdf'), bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    print("Saved: labor_share_comparison.png/pdf")


def write_csv():
    """Save the plotted BEA series, % of GDI except the NDI share (% of NDI)"""
    cols = [('compensation', bea_comp), ('wages_and_benefits_excl_employer_social_insurance', comp_ex_fica),
            ('wages', bea_wages), ('adjusted_with_labor_part_of_proprietors_income', adj_labor_share),
            ('compensation_pct_of_ndi', net_labor_share), ('depreciation', bea_dep)]
    with open(os.path.join(ROOT, 'data', 'labor_share_measures.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['year'] + [name for name, _ in cols])
        for i, y in enumerate(years):
            w.writerow([y] + [round(vals[i], 3) for _, vals in cols])
    print("Saved: data/labor_share_measures.csv")


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

    print(f"\nEmployer Social Insurance Share [B039RC]:")
    print(f"  1970: {employer_social_insurance[idx_1970]:.1f}%")
    print(f"  2024: {employer_social_insurance[idx_2024]:.1f}%")
    print(f"  Change: {employer_social_insurance[idx_2024] - employer_social_insurance[idx_1970]:+.1f} pp")

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
    create_combined_chart()
    write_csv()

    print_summary_stats()

    print("\nAll charts generated successfully!")
