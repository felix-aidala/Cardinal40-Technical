"""
Exhibit 2 — Founders are not interchangeable managers.
Event study: firm innovation around a founder-CEO -> professional-CEO switch.

Argument served
---------------
The thesis treats the founder as the irreplaceable unit of the offset. The
skeptic's reply is that a competent professional manager can run the company
just as well once it is built. Lee, Kim & Bae's event study is the cleanest
visual answer: tracking firms that switch from a founder-CEO to a professional
CEO, innovation output is flat and high through the founder years, then drops
sharply at the switch and keeps falling. The flat pre-trend is the point -- the
decline starts AT the handover, not before it, which is hard to explain as the
firm simply being on the way down already.

What this figure is (and an honest sourcing note)
-------------------------------------------------
This is a faithful redraw of *Figure 2, "Switching from Founder CEO to
Professional CEO,"* from the working-paper version of the study ("Are Founder
CEOs Better Innovators? Evidence from S&P 500 Firms"; S&P 500, 1993-2003). The
y-axis is the coefficient-plus-constant from a firm fixed-effects panel OLS of
ln(1 + citation-weighted patent count) on year-relative-to-switch dummies (so it
is on a log scale); year 0 is the switch. Values were digitized from the
published chart -- see data/raw/lee_kim_bae_fig2_event_study.csv -- so this
PRESENTS the authors' figure rather than reproducing the estimation (their data
are not redistributable).

The peer-reviewed version (Lee, Kim & Bae, 2020, Research Policy 49(1), "...
Evidence from CEO sudden deaths in public firms") sharpens identification using
CEO sudden deaths and reports the headline ~43.8% drop in citation-weighted
patents; that figure is annotated on the chart as corroboration.

Source
------
Lee, J.M., Kim, J., & Bae, J. "Are Founder CEOs Better Innovators? Evidence from
S&P 500 Firms" (Wharton Mack Institute working paper), Figure 2. Published
version: Research Policy 49(1), 103862 (2020), DOI 10.1016/j.respol.2019.103862.
Accessed 2026-06-22.

Run:  python code/exhibit2_founder_ceo_innovation.py
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "lee_kim_bae_fig2_event_study.csv"
FIG = ROOT / "exhibits" / "exhibit2_founder_ceo_innovation.png"

FOUNDER = "#1f4e79"   # founder era / central line
PRO = "#c0392b"       # professional era accent
BAND = "#9fb3c8"      # confidence band


def main() -> None:
    df = pd.read_csv(RAW, comment="#").sort_values("year_rel").reset_index(drop=True)

    pre = df[df.year_rel < 0].coef_plus_constant.mean()
    post_last = df[df.year_rel == df.year_rel.max()].coef_plus_constant.iloc[0]
    at_event = df[df.year_rel == 0].coef_plus_constant.iloc[0]

    print("Exhibit 2 — Event study: founder -> professional CEO switch")
    print("-" * 60)
    print(f"  Founder years (-5..-1) average level (log cit-wtd patents): {pre:.2f}")
    print(f"  At the switch (year 0): {at_event:.2f}")
    print(f"  Five years after (year +5): {post_last:.2f}")
    print(f"  Raw endpoint gap, founder-era avg -> year +5: {(post_last - pre):.2f} log points "
          f"(descriptive only, not the causal estimate).")
    print("  Cleanly-identified effect (published sudden-death design): "
          "~43.8% drop in citation-weighted patents.")

    # ---- figure ----
    fig, ax = plt.subplots(figsize=(9.4, 5.7))

    # shaded eras
    ax.axvspan(-5.5, 0, color=FOUNDER, alpha=0.05)
    ax.axvspan(0, 5.5, color=PRO, alpha=0.05)
    ax.axvline(0, color="#555555", lw=1.2, ls="--")

    # confidence band
    ax.fill_between(df.year_rel, df.ci_low, df.ci_high, color=BAND, alpha=0.45,
                    lw=0, label="95% confidence interval")
    # central path
    ax.plot(df.year_rel, df.coef_plus_constant, "-D", color=FOUNDER, lw=2.6, ms=6,
            label="Citation-weighted patent output (coef. + constant)")

    # era labels
    ax.text(-2.5, 2.92, "Founder-CEO years", color=FOUNDER, fontsize=11,
            fontweight="bold", ha="center")
    ax.text(2.75, 2.92, "After switch to professional CEO", color=PRO, fontsize=11,
            fontweight="bold", ha="center")

    ax.set_title("When a founder-CEO is replaced, firm innovation drops — and keeps dropping",
                 fontsize=12.5, fontweight="bold", loc="left", pad=26)
    ax.text(0.0, 1.035,
            "Citation-weighted patent output (log scale) of firms in the years around a founder → professional-CEO switch",
            transform=ax.transAxes, fontsize=9.5, color="#444444")

    ax.set_xlabel("Year relative to CEO change")
    ax.set_ylabel("Citation-weighted patent output")
    ax.set_xticks(range(-5, 6))
    ax.set_xlim(-5.5, 6.4)
    ax.set_ylim(0, 3.1)
    ax.grid(axis="y", color="#e6e6e6", lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower left", frameon=False, fontsize=9.2)

    fig.text(0.012, -0.03,
             "Source: Lee, Kim & Bae, \"Are Founder CEOs Better Innovators? Evidence from S&P 500 Firms\" (Wharton working paper), "
             "Figure 2; values digitized from the chart.\nThe peer-reviewed version (Research Policy 49(1), 2020, DOI "
             "10.1016/j.respol.2019.103862) identifies off CEO sudden deaths and reports a ~43.8% drop. Accessed 2026-06-22.",
             fontsize=7.5, color="#666666", va="top")

    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(FIG, dpi=200, bbox_inches="tight")
    print(f"\n  Figure written to {FIG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
