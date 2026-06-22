"""
Exhibit 3 — The flip: China's rise to the critical-technology research frontier,
2003-2023.

Argument served
---------------
Jane's essay opens on the stakes: "as late as 2007 the United States led China in
the overwhelming majority of these categories. Today the numbers have flipped."
This exhibit is the evidence for that sentence, using the dataset she names (ASPI's
Critical Technology Tracker). Across 64 critical technologies, the U.S. led 60
(China 3) in 2003-2007; two decades later China leads 57 and the U.S. just 7. The
time series shows the switch was gradual and consistent, not a single jump.

Why this measure, and the nuance that sets up the rest of the essay
-------------------------------------------------------------------
ASPI ranks countries by their share of the world's HIGH-IMPACT research (the top
10% most-cited publications) in each technology -- a *leading* indicator, upstream
of patents, products, and deployed capability. So this chart shows where the
frontier *ideas* are being generated, not who is currently winning in the market.
That gap -- leading in research vs. turning research into dominant companies -- is
exactly where the "founders as the next offset" argument lives (Exhibits 1-2).

A note on data availability (honesty)
-------------------------------------
The published report states China's count at four windows across the two decades
(3 -> 28 -> 52 -> 57) but the U.S.'s at only the two endpoints (60 -> 7); the
intermediate U.S. counts are not in the report (they sit in ASPI's interactive
tool). The U.S. line is therefore drawn DASHED between its two known endpoints and
is not presented as interpolated data. China's line connects four real points.

Data source
-----------
ASPI, "ASPI's two-decade Critical Technology Tracker," released Aug 2024. 64
technologies; leadership = highest national share of top 10% most-cited research
over a rolling 5-year window. Values + per-point sourcing in
data/raw/aspi_critical_tech_tracker.csv.
https://www.aspi.org.au/report/aspis-two-decade-critical-technology-tracker/
Accessed 2026-06-22.

Run:  python code/exhibit3_critical_tech_leadership.py
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "aspi_critical_tech_tracker.csv"
FIG = ROOT / "exhibits" / "exhibit3_critical_tech_leadership.png"

US_BLUE = "#1f4e79"
CN_RED = "#c0392b"
TOTAL_TECHS = 64


def main() -> None:
    df = pd.read_csv(RAW, comment="#").sort_values("mid_year")
    us = df[df.country == "United States"]
    cn = df[df.country == "China"]

    print("Exhibit 3 — ASPI critical-technology research leadership (of 64)")
    print("-" * 60)
    for _, r in df.iterrows():
        print(f"  {r.window}  {r.country:<14} leads {int(r.techs_led):>2} of {TOTAL_TECHS}")
    print(f"\n  Switch: U.S. {int(us.techs_led.iloc[0])}->{int(us.techs_led.iloc[-1])}, "
          f"China {int(cn.techs_led.iloc[0])}->{int(cn.techs_led.iloc[-1])} (of {TOTAL_TECHS}).")

    # ---- time series ----
    fig, ax = plt.subplots(figsize=(9.5, 6))

    # US: only the two endpoints are published -> dashed connector, not data
    ax.plot(us.mid_year, us.techs_led, "--", color=US_BLUE, lw=2, zorder=2)
    ax.plot(us.mid_year, us.techs_led, "o", color=US_BLUE, ms=11, zorder=3)
    # China: four published points -> solid line
    ax.plot(cn.mid_year, cn.techs_led, "-", color=CN_RED, lw=3, zorder=2)
    ax.plot(cn.mid_year, cn.techs_led, "o", color=CN_RED, ms=11, zorder=3)

    # value labels
    for _, r in us.iterrows():
        ax.annotate(f"{int(r.techs_led)}", (r.mid_year, r.techs_led), xytext=(0, 13),
                    textcoords="offset points", ha="center", color=US_BLUE,
                    fontsize=11, fontweight="bold")
    # China value labels: nudge the two near-coincident recent points apart
    cn_offsets = {2005: (0, -20), 2015: (0, 14), 2020: (-15, 8), 2021: (12, 6)}
    for _, r in cn.iterrows():
        ax.annotate(f"{int(r.techs_led)}", (r.mid_year, r.techs_led),
                    xytext=cn_offsets.get(r.mid_year, (0, 13)),
                    textcoords="offset points", ha="center", color=CN_RED,
                    fontsize=11, fontweight="bold")

    # series labels near the lines (lines cross, so label each near its own side)
    ax.text(2006.2, 55, "United States", color=US_BLUE, fontsize=12, fontweight="bold",
            ha="left", va="top")
    ax.text(2018.4, 60, "China", color=CN_RED, fontsize=12, fontweight="bold",
            ha="right", va="bottom")
    ax.text(2012.8, 10, "U.S.: report gives only\nthe two endpoints (dashed)",
            color=US_BLUE, fontsize=8.2, ha="left", va="center", style="italic")

    ax.set_title("China's gradual rise to the critical-technology research frontier",
                 fontsize=13, fontweight="bold", loc="left", pad=26)
    ax.text(0.0, 1.04,
            f"Number of {TOTAL_TECHS} critical technologies in which each country leads the world, "
            "by share of the most highly-cited research",
            transform=ax.transAxes, fontsize=9.5, color="#444444")

    # Label only the well-separated windows; the 2018-2022 window (x=2020)
    # overlaps 2019-2023, so it gets a plotted point but no x-tick label.
    ax.set_xticks([2005, 2015, 2021])
    ax.set_xticklabels(["2003–2007", "2013–2017", "2019–2023"], fontsize=10)
    ax.set_xlim(2003, 2023)
    ax.set_ylim(0, TOTAL_TECHS)
    ax.set_yticks([0, 16, 32, 48, 64])
    ax.set_ylabel(f"Critical technologies led (of {TOTAL_TECHS})")
    ax.grid(axis="y", color="#ececec", lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)

    fig.text(0.012, -0.01,
             "Source: ASPI, \"ASPI's two-decade Critical Technology Tracker\" (released Aug 2024). Leadership = highest national "
             "share of the top 10% most-cited\nresearch publications in a technology (rolling 5-year window). Measures research "
             "leadership, not manufacturing or deployed capability.\nWindows plotted at their midpoints; the report publishes "
             "China at four windows but the U.S. only at the endpoints. Accessed 2026-06-22.",
             fontsize=7.4, color="#666666", va="top")

    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(FIG, dpi=200, bbox_inches="tight")
    print(f"\n  Figure written to {FIG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
