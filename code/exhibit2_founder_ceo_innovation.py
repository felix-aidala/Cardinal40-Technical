"""
Exhibit 2 — Founders are not interchangeable managers.
What happens to innovation when a founder-CEO is (exogenously) replaced.

Argument served
---------------
The thesis treats the founder as the irreplaceable unit of the offset. The
natural skeptic's reply is that a good professional manager can run the company
just as well once it is built. Lee, Kim & Bae (2020) is the cleanest available
test of that claim: they use the SUDDEN DEATH of a CEO as a natural experiment,
so the switch from a founder to a professional manager is plausibly unrelated to
how the firm was already doing. Innovation output falls sharply -- and not
because the new managers spend less on R&D, but because they manage and retain
innovative talent less well.

Why this is a "present the published estimate" exhibit, not a reproduction
-------------------------------------------------------------------------
The identifying dataset (hand-collected CEO sudden-death events, 1979-2002,
matched to patent records) is not redistributable, so reproducing the event
study from scratch is neither feasible nor honest. This exhibit faithfully
visualizes the paper's *published* headline estimate and its mechanism findings.
All numbers are the authors'; see data/raw/lee_kim_bae_2020_estimates.csv.

Source
------
Lee, J.M., Kim, J., & Bae, J. (2020). "Founder CEOs and innovation: Evidence
from CEO sudden deaths in public firms." Research Policy, 49(1), 103862.
DOI: 10.1016/j.respol.2019.103862. Abstract accessed via publisher / RePEc
(https://ideas.repec.org/a/eee/respol/v49y2020i1s0048733319301817.html),
2026-06-22.

Run:  python code/exhibit2_founder_ceo_innovation.py
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "lee_kim_bae_2020_estimates.csv"
FIG = ROOT / "exhibits" / "exhibit2_founder_ceo_innovation.png"

FOUNDER = "#1f4e79"
PRO = "#9aa3ad"
DROP = "#c0392b"


def main() -> None:
    est = pd.read_csv(RAW, comment="#")
    pct = float(est.loc[est.metric == "citation_weighted_patent_change", "value"].iloc[0])

    founder_idx = 100.0
    pro_idx = founder_idx * (1 + pct / 100.0)  # 43.8% lower -> 56.2

    print("Exhibit 2 — Lee, Kim & Bae (2020), Research Policy 49(1)")
    print("-" * 60)
    print(f"  Headline estimate: exogenous founder -> professional CEO transition")
    print(f"    => {pct:.1f}% change in citation-weighted patent count (controls for R&D).")
    print(f"  Indexed to founder-led = {founder_idx:.0f}: professional-led = {pro_idx:.1f}.")
    print( "  Mechanisms (directional, from the paper):")
    print( "    + founder-led firms produce more patents at BOTH quality tails & more explorative patents")
    print( "    + inventor employees leave after a founder is replaced (worse talent retention)")
    print( "    - no evidence founder-led firms simply spend MORE on R&D (it's management, not money)")

    # ---- figure: two-panel. Left: indexed bar comparison. Right: mechanisms. ----
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 5.6),
                                   gridspec_kw={"width_ratios": [1.15, 1]})

    # Left panel: bars
    bars = axL.bar([0, 1], [founder_idx, pro_idx],
                   color=[FOUNDER, PRO], width=0.62, zorder=3)
    axL.set_xticks([0, 1])
    axL.set_xticklabels(["Founder-CEO\nled", "Professional-CEO\nled\n(after sudden death)"],
                        fontsize=10.5)
    axL.set_ylim(0, 118)
    axL.set_ylabel("Citation-weighted patent output\n(founder-led firm = 100)", fontsize=10.5)
    axL.set_yticks([0, 25, 50, 75, 100])
    axL.grid(axis="y", color="#e3e3e3", lw=0.8, zorder=0)
    axL.spines[["top", "right"]].set_visible(False)

    axL.text(0, founder_idx + 3, "100", ha="center", fontweight="bold",
             color=FOUNDER, fontsize=12)
    axL.text(1, pro_idx + 3, f"{pro_idx:.1f}", ha="center", fontweight="bold",
             color="#5a6066", fontsize=12)

    # drop annotation
    axL.annotate("", xy=(1, pro_idx), xytext=(1, founder_idx),
                 arrowprops=dict(arrowstyle="-|>", color=DROP, lw=2.2))
    axL.text(1.34, (founder_idx + pro_idx) / 2, f"{pct:.1f}%",
             color=DROP, fontweight="bold", fontsize=15, va="center", ha="left")
    axL.text(1.34, (founder_idx + pro_idx) / 2 - 8, "fewer\ncitation-weighted\npatents",
             color=DROP, fontsize=8.5, va="top", ha="left")
    axL.set_xlim(-0.6, 2.1)

    axL.set_title("Replacing a founder cuts innovation",
                  fontsize=11.5, fontweight="bold", loc="left", pad=10)

    # Right panel: mechanism findings as a clean text block
    axR.axis("off")
    axR.set_title("Why — the mechanisms", fontsize=11.5,
                  fontweight="bold", loc="left", pad=10)
    items = [
        ("Identification",
         "Natural experiment: CEO sudden deaths at U.S. public\nfirms, 1979-2002. The switch is unrelated to firm prospects."),
        ("It's management, not money",
         "Effect holds controlling for R&D spend. Founder-led firms\ndo NOT out-spend on R&D — they manage innovation better."),
        ("Talent walks",
         "After a founder is replaced, inventor-employees leave —\nfounders retain innovative minds better."),
        ("Bolder bets",
         "Founder-led firms produce more explorative patents and\nmore at both quality tails (the home-runs and the misses)."),
    ]
    y = 0.86
    for head, body in items:
        axR.text(0.02, y, "●", color=FOUNDER, fontsize=11, va="top")
        axR.text(0.08, y, head, fontweight="bold", fontsize=10.5, va="top")
        axR.text(0.08, y - 0.055, body, fontsize=9.2, va="top", color="#333333")
        y -= 0.235

    fig.suptitle("Founders are not interchangeable managers",
                 fontsize=14.5, fontweight="bold", x=0.012, ha="left", y=1.01)

    fig.text(0.012, -0.02,
             "Source: Lee, Kim & Bae (2020), \"Founder CEOs and innovation: Evidence from CEO sudden deaths in public firms,\" "
             "Research Policy 49(1), 103862,\nDOI 10.1016/j.respol.2019.103862. Figure presents the paper's published estimates "
             "(not an independent reproduction). Accessed 2026-06-22.",
             fontsize=7.6, color="#666666", va="top")

    fig.tight_layout(rect=[0, 0.02, 1, 0.97])
    fig.savefig(FIG, dpi=200, bbox_inches="tight")
    print(f"\n  Figure written to {FIG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
