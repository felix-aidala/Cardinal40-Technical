"""
Exhibit 1 — Where do new U.S. PhDs go to work?
The half-century shift from the academy to industry, early 1970s-2024.

Argument served
---------------
The "founders as the next offset" thesis rests on the claim that the locus of
frontier innovation has moved out of the university and into industry and
company-building. New-doctorate employment commitments are a clean, leading
indicator of where the most highly trained talent chooses to work. In the early
1970s academia took two-thirds of new U.S. PhDs with a job in hand and industry
barely one in eight; by 2024 the two are even (~40% each) -- and within science &
engineering specifically, industry has pulled far ahead (see annotation).

Data sources (one consistent measure, three report vintages)
------------------------------------------------------------
All three measure the same thing: the employment SECTOR of new U.S. research
doctorate recipients who report a definite U.S. EMPLOYMENT commitment (postdocs
are a separate "study" commitment and are excluded), with "industry" including
self-employment and "academe" = academic employment.

  1970-74  : NSF/SRS (2006), "U.S. Doctorates in the 20th Century" (NSF 06-319),
             Table 6-3.  [five-year average, plotted at 1972]
  1986,1991: NORC/NSF, "Doctorate Recipients from U.S. Universities: Summary
             Report 2006," Table 30 (selected years 1986-2006).
  1994-2024: NCSES, Survey of Earned Doctorates 2024, Table 2-6 (NSF 25-349).

The series agree where they meet (1991 = 52.6/21.4 vs 1994 = 51.2/21.1),
supporting the splice. See the two raw CSVs in data/raw/ for per-point sourcing.
For the 1994-2024 stretch we use the single current NCSES trend table (Table
2-6) rather than mixing vintages, so that segment is internally consistent.

Methodological notes
--------------------
* Universe: doctorate recipients with a *definite* (signed) non-postdoc U.S.
  employment commitment. Postdocs excluded by construction.
* "industry" includes self-employment (i.e., founders).
* Selected years only are published; the early-1970s point is a five-year
  average. A straight segment across the 1972-1986 gap slightly understates that
  the academic drop was concentrated in the 1970s (academe was near 50% by the
  early 1980s and then roughly flat for two decades).

Run:  python code/exhibit1_stem_phd_pathways.py
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
RAW_MODERN = ROOT / "data" / "raw" / "sed_table2-6_employment_sector.csv"
RAW_HIST = ROOT / "data" / "raw" / "sed_historical_employment_sector_allfields.csv"
PROCESSED = ROOT / "data" / "processed" / "exhibit1_allfields_academe_vs_industry.csv"
FIG = ROOT / "exhibits" / "exhibit1_stem_phd_pathways.png"

ACADEME = "#2e7d32"   # forest green
INDUSTRY = "#c55a11"  # burnt orange


def build_series() -> pd.DataFrame:
    """All-fields academe-vs-industry series, early 1970s -> 2024."""
    modern = pd.read_csv(RAW_MODERN, comment="#")
    modern = modern[modern.field == "All fields"][["year", "academe_pct", "industry_pct"]].copy()
    modern["plot_year"] = modern["year"].astype(int)

    hist = pd.read_csv(RAW_HIST, comment="#")
    hist = hist[hist.field == "All fields"][["plot_year", "academe_pct", "industry_pct"]].copy()

    out = pd.concat([hist[["plot_year", "academe_pct", "industry_pct"]],
                     modern[["plot_year", "academe_pct", "industry_pct"]]],
                    ignore_index=True)
    out = out.sort_values("plot_year").drop_duplicates("plot_year").reset_index(drop=True)
    return out


def main() -> None:
    s = build_series()
    s.to_csv(PROCESSED, index=False)

    first, last = s.iloc[0], s.iloc[-1]
    print("Exhibit 1 — U.S. doctorate first-destination employment commitments (all fields)")
    print("-" * 74)
    print(f"  {int(first.plot_year)}: academia {first.academe_pct:.1f}%  vs  industry {first.industry_pct:.1f}%"
          f"   (academia leads by {first.academe_pct - first.industry_pct:+.1f} pts)")
    print(f"  {int(last.plot_year)}: academia {last.academe_pct:.1f}%  vs  industry {last.industry_pct:.1f}%"
          f"   (gap {last.academe_pct - last.industry_pct:+.1f} pts)")

    s["industry_leads"] = s.industry_pct >= s.academe_pct
    if s["industry_leads"].any():
        flip = int(s[s["industry_leads"]].plot_year.min())
        prev = int(s[s.plot_year < flip].plot_year.max())
        print(f"  Industry pulls even with / overtakes academia between {prev} and {flip} (all fields).")

    # S&E-specific endpoints (not plotted) for the annotation: the shift is sharper.
    hist = pd.read_csv(RAW_HIST, comment="#")
    se70 = hist[(hist.field == "Science and engineering")].iloc[0]
    modern = pd.read_csv(RAW_MODERN, comment="#")
    se24 = modern[(modern.field == "Total S&E") & (modern.year == 2024)].iloc[0]
    print("\n  For science & engineering specifically (not plotted; cited in annotation):")
    print(f"    academia {se70.academe_pct:.1f}% (1970-74) -> {se24.academe_pct:.1f}% (2024);"
          f"  industry {se70.industry_pct:.1f}% -> {se24.industry_pct:.1f}%.")

    # ---- figure ----
    fig, ax = plt.subplots(figsize=(9.2, 5.5))
    ax.plot(s.plot_year, s.academe_pct, "-o", color=ACADEME, lw=2.5, ms=5)
    ax.plot(s.plot_year, s.industry_pct, "-o", color=INDUSTRY, lw=2.5, ms=5)

    # direct labels at the START of each line (in lieu of a legend); the two
    # series are far apart in 1972, so they sit cleanly to the left of the points.
    fx = int(first.plot_year)
    ax.text(fx - 1.5, first.academe_pct, "Academia",
            color=ACADEME, fontsize=11, fontweight="bold", va="center", ha="right")
    ax.text(fx - 1.5, first.industry_pct, "Industry",
            color=INDUSTRY, fontsize=11, fontweight="bold", va="center", ha="right")

    ax.set_title("Since the 1970s, industry has caught up with academia for new U.S. PhDs",
                 fontsize=12.5, fontweight="bold", pad=26, loc="left")
    ax.text(0.0, 1.035,
            "Share of new U.S. research-doctorate recipients with a definite U.S. employment commitment, by sector (all fields)",
            transform=ax.transAxes, fontsize=9.5, color="#444444")

    ax.set_ylabel("Share of definite U.S. employment commitments")
    ax.set_ylim(0, 72)
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.set_xticks([1970, 1980, 1990, 2000, 2010, 2020])
    ax.set_xlim(1963, int(last.plot_year) + 1)  # room on the left for start labels
    ax.grid(axis="y", color="#dddddd", lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)

    ax.text(0.0, -0.16,
            "Sources: 1970-74 from NSF \"U.S. Doctorates in the 20th Century\" (NSF 06-319, Tbl 6-3); 1986 & 1991 from "
            "NORC/NSF Summary Report 2006 (Tbl 30);\n1994-2024 from NCSES Survey of Earned Doctorates 2024 (Tbl 2-6, "
            "NSF 25-349). Postdocs excluded; 'industry' includes self-employment. Accessed 2026-06-22.",
            transform=ax.transAxes, fontsize=7.3, color="#666666", va="top")

    fig.tight_layout()
    fig.savefig(FIG, dpi=200, bbox_inches="tight")
    print(f"\n  Figure written to {FIG.relative_to(ROOT)}")
    print(f"  Processed series written to {PROCESSED.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
