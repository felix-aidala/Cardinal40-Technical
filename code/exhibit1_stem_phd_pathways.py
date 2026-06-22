"""
Exhibit 1 — Where do new U.S. science & engineering PhDs go to work?
The shift of frontier talent from the academy to industry, 1994-2024.

Argument served
---------------
The "founders as the next offset" thesis rests on the claim that the locus of
frontier innovation has moved out of the university and into industry and
company-building. New-doctorate employment commitments are a clean, leading
indicator of where the most highly trained technical talent is choosing to do
its work. For science & engineering (S&E) doctorates as a whole, industry has
gone from trailing academia by ~7 points (1994) to leading it by ~22 points
(2024) -- the two lines cross in the 2009-2014 window.

Data source
-----------
NCSES, Survey of Earned Doctorates (SED), 2024 cycle. Table 2-6, "Employment
sector of research doctorate recipients with definite postgraduation
commitments for non-postdoc employment in the United States, by trend broad
field of doctorate: Selected years, 1994-2024." (NSF 25-349)
https://ncses.nsf.gov/pubs/nsf25349/assets/data-tables/tables/nsf25349-tab002-006.pdf
Accessed 2026-06-22. Raw values transcribed to data/raw/sed_table2-6_employment_sector.csv.

Methodological notes
--------------------
* Universe: doctorate recipients who reported a *definite* (signed) non-postdoc
  employment commitment IN THE UNITED STATES. Postdocs are excluded by
  construction, which is appropriate here -- we want first destinations into the
  permanent workforce, not training holding-patterns. It does mean the academic
  pipeline (postdoc -> faculty) is understated as a *share of all graduates*;
  the trend in the academe-vs-industry split among those who go straight to work
  is what this exhibit measures, and that is the relevant quantity.
* "Industry or business" includes self-employment (i.e., founders).
* The SED switched to a modified CIP field taxonomy in 2021, so field-level
  series have a small comparability break vs. pre-2021. The aggregates plotted
  here ("All S&E") are the most robust to that break; field detail is reported
  in the printout with the caveat.
* Selected years only (1994, 1999, ... 2024) are published in the trend table.

Run:  python code/exhibit1_stem_phd_pathways.py
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "sed_table2-6_employment_sector.csv"
PROCESSED = ROOT / "data" / "processed" / "exhibit1_se_academe_vs_industry.csv"
FIG = ROOT / "exhibits" / "exhibit1_stem_phd_pathways.png"

ACADEME = "#1f4e79"   # deep blue
INDUSTRY = "#c55a11"  # burnt orange


def load() -> pd.DataFrame:
    df = pd.read_csv(RAW, comment="#")
    df["year"] = df["year"].astype(int)
    return df


def main() -> None:
    df = load()

    # Headline series: all science & engineering fields combined.
    se = df[df["field"] == "Total S&E"].sort_values("year").reset_index(drop=True)
    se.to_csv(PROCESSED, index=False)

    # ---- key computed figures (printed, and used in the annotation) ----
    first, last = se.iloc[0], se.iloc[-1]
    print("Exhibit 1 — U.S. S&E doctorate first-destination employment commitments")
    print("-" * 70)
    print(f"  {int(first.year)}: academe {first.academe_pct:.1f}%  vs  industry {first.industry_pct:.1f}%"
          f"   (academe leads by {first.academe_pct - first.industry_pct:+.1f} pts)")
    print(f"  {int(last.year)}: academe {last.academe_pct:.1f}%  vs  industry {last.industry_pct:.1f}%"
          f"   (industry leads by {last.industry_pct - last.academe_pct:+.1f} pts)")
    print(f"  Swing in the academe-minus-industry gap: "
          f"{(first.academe_pct - first.industry_pct) - (last.academe_pct - last.industry_pct):+.1f} pts")

    # Durable crossover: the last year academe still leads, after which industry
    # leads in every subsequent published year. (Early years wobble because only
    # selected years are published, so a first-flip rule would mislead.)
    se["academe_leads"] = se["academe_pct"] >= se["industry_pct"]
    last_academe_lead = se[se["academe_leads"]].year.max()
    after = se[se["year"] > last_academe_lead]
    if not after.empty and not after["academe_leads"].any():
        nxt = int(after.year.min())
        print(f"  Industry takes a durable lead between {int(last_academe_lead)} and {nxt} "
              f"(industry leads in every published year thereafter).")

    print("\n  Field detail, 2024 (industry share, % of definite U.S. commitments):")
    for fld in ["Engineering", "Computer and information sciences",
                "Physical sciences", "Mathematics and statistics",
                "Biological and biomedical sciences"]:
        row = df[(df.field == fld) & (df.year == 2024)].iloc[0]
        print(f"    {fld:<38} {row.industry_pct:5.1f}%  (academe {row.academe_pct:.1f}%)")
    print("  [Field detail has a CIP-taxonomy break in 2021; treat pre/post-2021 with care.]")

    # ---- figure ----
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(se.year, se.academe_pct, "-o", color=ACADEME, lw=2.5, label="Academia")
    ax.plot(se.year, se.industry_pct, "-o", color=INDUSTRY, lw=2.5,
            label="Industry / business")

    # endpoint value labels
    for col, color, dy in [("academe_pct", ACADEME, 10), ("industry_pct", INDUSTRY, -16)]:
        for x, y in [(se.year.iloc[0], se[col].iloc[0]), (se.year.iloc[-1], se[col].iloc[-1])]:
            ax.annotate(f"{y:.0f}%", (x, y), textcoords="offset points",
                        xytext=(0, dy), ha="center", color=color, fontsize=10,
                        fontweight="bold")

    ax.set_title("New U.S. science & engineering PhDs now go to industry, not academia",
                 fontsize=12.5, fontweight="bold", pad=30, loc="left")
    ax.text(0.0, 1.025,
            "Share of S&E doctorate recipients with a definite U.S. non-postdoc job commitment, by sector",
            transform=ax.transAxes, fontsize=9.5, color="#444444")

    ax.set_ylabel("Share of definite U.S. employment commitments")
    ax.set_ylim(0, 65)
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.set_xticks(se.year)
    ax.grid(axis="y", color="#dddddd", lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="center left", frameon=False, fontsize=11)

    ax.text(0.0, -0.16,
            "Source: NCSES, Survey of Earned Doctorates 2024, Table 2-6 (NSF 25-349). "
            "Postdocs excluded; 'industry' includes self-employment.\n"
            "Selected years shown. Accessed 2026-06-22.",
            transform=ax.transAxes, fontsize=7.5, color="#666666", va="top")

    fig.tight_layout()
    fig.savefig(FIG, dpi=200, bbox_inches="tight")
    print(f"\n  Figure written to {FIG.relative_to(ROOT)}")
    print(f"  Processed series written to {PROCESSED.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
