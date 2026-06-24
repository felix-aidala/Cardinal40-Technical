"""
Exhibit 3 — Financing the swing: U.S. venture capital vs. the rest of the
developed world.

Argument served
---------------
Exhibits 1 and 2 establish that frontier talent now sits in industry and that
founders specifically are not interchangeable managers. This exhibit closes the
arc on the *system* side of the thesis: America does not merely produce valuable
founders, it funds them at a scale no other large economy approaches. Venture
capital is the fuel for the "finance the swing" leg of the argument -- the money
that lets a founder take an expensive, uncertain shot at building a frontier
company. Measured against the size of the economy, U.S. VC investment dwarfs the
other large advanced economies.

What the figure shows
---------------------
Left  — VC investment as % of GDP over time, United States vs. the band spanned
        by the other G7 economies (UK, Germany, France, Italy, Japan, Canada).
        The U.S. line sits far above the entire rest-of-G7 range, and the gap
        widens markedly after ~2018.
Right — VC investment as % of GDP in the latest fully-reported year, across the
        G7 (the largest advanced economies), U.S. highlighted.

Nuance the writer must respect (and that pre-empts the obvious critique)
-----------------------------------------------------------------------
* The U.S. is NOT first on this metric *worldwide*. **Israel** invests a far
  larger share of its GDP in VC (~1.8% vs the U.S. ~0.5% in 2024). The chart is
  therefore scoped to the G7 -- the largest advanced economies, where the U.S.
  is first and Israel (a small economy) is not a peer -- and Israel is
  acknowledged in a footnote rather than hidden. The per-GDP lead also reverses
  on absolute capital: the U.S. deployed ~$156B of VC in 2024 vs Israel's ~$10B,
  roughly 16x larger. Both facts are printed below.
* This is venture capital specifically, not all startup or growth financing; the
  OECD re-aggregates national venture-association data to a common stage
  definition, so cross-country levels are comparable but not identical to any one
  national association's headline number.

Data source
-----------
OECD Entrepreneurship Financing Database, "Venture capital investments (market
statistics)" (dataflow DSD_VC@DF_VC_INV), business development stage = Total.
Units used: percentage of GDP, and US dollars (exchange-rate converted) for the
absolute comparison. Pulled live from the OECD SDMX API; a snapshot is cached in
data/raw/. Accessed 2026-06-24.
Data Explorer: https://data-explorer.oecd.org/vis?df[id]=DSD_VC@DF_VC_INV

Run:  python code/exhibit3_vc_gdp.py            (uses cached snapshot if present)
      python code/exhibit3_vc_gdp.py --refresh  (re-download from the OECD API)
"""

import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "oecd_vc_gdp.csv"
PROCESSED = ROOT / "data" / "processed" / "exhibit3_vc_gdp.csv"
FIG = ROOT / "exhibits" / "exhibit3_vc_gdp.png"

OECD_URL = ("https://sdmx.oecd.org/public/rest/data/"
            "OECD.SDD.TPS,DSD_VC@DF_VC_INV,1.0/all?format=csvfilewithlabels")

US_BLUE = "#1f4e79"
BAND_GRAY = "#9aa6b2"
ISRAEL_GOLD = "#b8860b"
OTHER_GRAY = "#c7ced6"

G7_EX_US = ["United Kingdom", "Germany", "France", "Italy", "Japan", "Canada"]
BAR_SET = ["United States", "Canada", "United Kingdom",
           "France", "Germany", "Japan", "Italy"]


def download() -> pd.DataFrame:
    import requests
    import io
    txt = requests.get(OECD_URL, timeout=120).text
    return pd.read_csv(io.StringIO(txt))


def load() -> pd.DataFrame:
    refresh = "--refresh" in sys.argv
    if RAW.exists() and not refresh:
        return pd.read_csv(RAW, comment="#")
    df = download()
    cols = ["Reference area", "Business development stage", "Unit of measure",
            "TIME_PERIOD", "OBS_VALUE"]
    df = df[cols].rename(columns={
        "Reference area": "country", "Business development stage": "stage",
        "Unit of measure": "unit", "TIME_PERIOD": "year", "OBS_VALUE": "value"})
    with RAW.open("w") as f:
        f.write("# OECD Entrepreneurship Financing DB, 'Venture capital investments\n"
                "# (market statistics)', dataflow DSD_VC@DF_VC_INV. Total stage only,\n"
                "# % of GDP and absolute US$ (millions). Accessed 2026-06-24.\n")
        df.to_csv(f, index=False)
    return df


def main() -> None:
    df = load()
    tot = df[df["stage"] == "Total"].copy()
    pct = (tot[tot["unit"] == "Percentage of GDP"]
           .pivot_table(index="year", columns="country", values="value"))
    usd = (tot[tot["unit"].str.startswith("US dollars")]
           .pivot_table(index="year", columns="country", values="value"))

    # latest year with U.S. + the full bar set reported
    candidates = [y for y in pct.index
                  if pct.loc[y, [c for c in BAR_SET if c in pct.columns]].notna().all()]
    latest = max(candidates)

    pct.to_csv(PROCESSED)

    us_p = pct["United States"]
    print(f"Exhibit 3 — U.S. venture capital vs. the developed world (latest fully-reported: {latest})")
    print("-" * 70)
    print(f"  {latest} VC investment, % of GDP:")
    for c in BAR_SET:
        rank = pct.loc[latest].rank(ascending=False)[c]
        mult = us_p[latest] / pct.loc[latest, c]
        tag = "  <-- United States" if c == "United States" else (
            f"   (US is {mult:.1f}x)" if mult >= 1 else f"   (US is {1/mult:.1f}x SMALLER)")
        print(f"    {c:<16} {pct.loc[latest, c]:5.2f}%   rank {int(rank):>2}/{int(pct.loc[latest].notna().sum())}{tag}")
    us_abs = usd.loc[latest, "United States"] / 1e3
    il_abs = usd.loc[latest, "Israel"] / 1e3
    print(f"\n  Absolute scale, {latest}: US ${us_abs:,.0f}B  vs  Israel ${il_abs:,.0f}B "
          f"(US is {us_abs/il_abs:.0f}x larger in dollars -- Israel leads per-GDP, US leads in capital).")

    # ---- figure ----
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 5.6),
                                   gridspec_kw={"width_ratios": [1.45, 1]})

    # Left: U.S. vs the band of the other G7 economies, over time
    g7 = pct[[c for c in G7_EX_US if c in pct.columns]]
    yrs = [y for y in pct.index if y >= 2006 and g7.loc[y].notna().any()]
    g7 = g7.loc[yrs]
    band_lo, band_hi = g7.min(axis=1), g7.max(axis=1)
    axL.fill_between(yrs, band_lo, band_hi, color=BAND_GRAY, alpha=0.45, lw=0,
                     label="Other G7 (range)")
    axL.plot(yrs, us_p.loc[yrs], "-o", color=US_BLUE, lw=2.6, ms=4, label="United States")
    yv = us_p.loc[max(yrs)]
    axL.annotate(f"{yv:.2f}%", (max(yrs), yv), textcoords="offset points",
                 xytext=(8, 0), color=US_BLUE, fontweight="bold", fontsize=10, va="center")
    axL.set_title("The U.S. sits far above every other G7 economy",
                  fontsize=12, fontweight="bold", loc="left")
    axL.set_ylabel("Venture capital invested (% of GDP)")
    axL.yaxis.set_major_formatter(PercentFormatter(decimals=1))
    axL.grid(axis="y", color="#e3e3e3", lw=0.8)
    axL.spines[["top", "right"]].set_visible(False)
    axL.legend(loc="upper left", frameon=False, fontsize=10.5)
    axL.set_xlim(2006, max(yrs) + 1.5)
    axL.set_ylim(0, max(us_p.loc[yrs].max(), band_hi.max()) * 1.15)

    # Right: latest-year cross-section, G7 + Israel
    bar = pct.loc[latest, [c for c in BAR_SET if c in pct.columns]].sort_values()
    colors = [US_BLUE if c == "United States" else OTHER_GRAY for c in bar.index]
    ypos = range(len(bar))
    axR.barh(list(ypos), bar.values, color=colors, zorder=3)
    axR.set_yticks(list(ypos))
    axR.set_yticklabels(bar.index, fontsize=10)
    for i, (c, v) in enumerate(bar.items()):
        axR.text(v + 0.015, i, f"{v:.2f}%", va="center", fontsize=9.2,
                 fontweight="bold" if c == "United States" else "normal",
                 color=US_BLUE if c == "United States" else "#555555")
    axR.set_title(f"VC investment, {latest} (% of GDP) — G7", fontsize=12,
                  fontweight="bold", loc="left")
    axR.set_xlim(0, bar.max() * 1.18)
    axR.xaxis.set_major_formatter(PercentFormatter(decimals=1))
    axR.grid(axis="x", color="#e3e3e3", lw=0.8, zorder=0)
    axR.spines[["top", "right"]].set_visible(False)

    fig.suptitle("Financing the swing: U.S. venture capital dwarfs the rest of the G7",
                 fontsize=14.5, fontweight="bold", x=0.012, ha="left", y=1.0)
    fig.text(0.012, 0.945,
             f"Venture capital invested as a share of GDP. In {latest} the U.S. invested "
             f"~{us_p[latest]:.1f}% of GDP — 3x the U.K., 6x France, ~8–9x Germany and Japan.",
             fontsize=9.3, color="#444444", ha="left")
    fig.text(0.012, -0.02,
             "Source: OECD Entrepreneurship Financing Database, 'Venture capital investments (market statistics)', "
             "stage = Total; accessed 2026-06-24. Compared here against the rest of the G7 (the largest advanced "
             "economies).\nAmong smaller economies Israel invests a larger share of GDP (~"
             f"{pct.loc[latest, 'Israel']:.1f}%), but only ~\\${il_abs:,.0f}B in absolute terms vs the U.S.'s ~\\${us_abs:,.0f}B. "
             "VC is one channel of startup finance, not all of it.",
             fontsize=7.5, color="#666666", va="top")

    fig.tight_layout(rect=[0, 0.02, 1, 0.92])
    fig.savefig(FIG, dpi=200, bbox_inches="tight")
    print(f"\n  Figure written to {FIG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
