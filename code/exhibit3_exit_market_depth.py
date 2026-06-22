"""
Exhibit 3 — The American exit machine: how deep U.S. capital markets are
relative to China's.

Argument served
---------------
Jane's structural claim is that America's edge is not just producing founders
but *financing and recycling* them: "the deepest exit markets in the world --
IPOs, acquisitions, secondary markets -- that let you turn success into
liquidity and recycle that capital and talent into the next bet." A deep, liquid
public-equity market is the backbone of that exit machine: it is where companies
IPO, and it is the currency and price-discovery that powers acquisitions. This
exhibit measures that depth, U.S. vs. China, two ways: relative to the size of
the economy, and in absolute dollars.

Why market-cap DEPTH and not trading volume (an important nuance)
-----------------------------------------------------------------
A natural instinct is to compare stock-market *turnover* (value of shares traded
/ GDP). We deliberately do NOT headline that, because it would mislead: Chinese
exchanges have very high turnover (often >180% of GDP, periodically exceeding the
U.S.) driven by retail speculation, not by exit-market depth. Market
capitalization relative to GDP, and absolute market cap, are the cleaner measures
of how much company value the market can actually absorb and price -- i.e., how
big an exit the system can support. The turnover figures are printed below so the
contrast is transparent.

Caveats the writer should respect
---------------------------------
* This is public-equity depth as a *proxy* for the whole exit ecosystem (which
  also includes M&A and secondaries). It is the best single freely-reproducible
  cross-country measure; it is not the entire story.
* A large share of China's listed market cap is state-owned enterprises, and
  capital controls limit a foreign or VC investor's ability to exit and
  repatriate -- so China's "usable" exit depth for a private-market investor is
  arguably even thinner than the headline gap.

Data source
-----------
World Bank, World Development Indicators (source: World Federation of Exchanges /
Refinitiv). Indicators:
  CM.MKT.LCAP.GD.ZS  Market capitalization of listed domestic companies (% of GDP)
  CM.MKT.LCAP.CD     Market capitalization of listed domestic companies (current US$)
  CM.MKT.TRAD.GD.ZS  Stocks traded, total value (% of GDP)   [shown for context only]
Pulled live from the World Bank API; a snapshot is cached in data/raw/.
Accessed 2026-06-22. API docs: https://datahelpdesk.worldbank.org/

Run:  python code/exhibit3_exit_market_depth.py        (uses cached snapshot if present)
      python code/exhibit3_exit_market_depth.py --refresh   (re-download from API)
"""

import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "worldbank_market_depth.csv"
PROCESSED = ROOT / "data" / "processed" / "exhibit3_market_depth.csv"
FIG = ROOT / "exhibits" / "exhibit3_exit_market_depth.png"

INDICATORS = {
    "CM.MKT.LCAP.GD.ZS": "mktcap_pct_gdp",
    "CM.MKT.LCAP.CD": "mktcap_usd",
    "CM.MKT.TRAD.GD.ZS": "stockstraded_pct_gdp",
}
COUNTRIES = {"USA": "United States", "CHN": "China"}

US_BLUE = "#1f4e79"
CN_RED = "#c0392b"


def download() -> pd.DataFrame:
    import requests
    frames = []
    for code, name in INDICATORS.items():
        url = (f"https://api.worldbank.org/v2/country/USA;CHN/indicator/{code}"
               f"?format=json&per_page=1000")
        data = requests.get(url, timeout=60).json()[1]
        rec = [{"iso3": d["countryiso3code"], "year": int(d["date"]), name: d["value"]}
               for d in data if d["value"] is not None]
        frames.append(pd.DataFrame(rec).set_index(["iso3", "year"]))
    df = pd.concat(frames, axis=1).reset_index().sort_values(["iso3", "year"])
    return df


def load() -> pd.DataFrame:
    refresh = "--refresh" in sys.argv
    if RAW.exists() and not refresh:
        return pd.read_csv(RAW, comment="#")
    df = download()
    with RAW.open("w") as f:
        f.write("# World Bank WDI: market capitalization (% of GDP, current US$) and\n"
                "# stocks traded (% of GDP), USA & CHN. Source: World Federation of\n"
                "# Exchanges / Refinitiv via World Bank API. Accessed 2026-06-22.\n")
        df.to_csv(f, index=False)
    return df


def main() -> None:
    df = load()
    df = df[df.year >= 2003].copy()
    us = df[df.iso3 == "USA"].set_index("year")
    cn = df[df.iso3 == "CHN"].set_index("year")

    # Anchor the snapshot to the most recent year where every metric exists for
    # both countries (absolute market cap is published one year ahead of the
    # %-of-GDP and turnover series, so df.year.max() alone would give NaNs).
    common = [y for y in us.index if y in cn.index
              and us.loc[y, ["mktcap_pct_gdp", "mktcap_usd", "stockstraded_pct_gdp"]].notna().all()
              and cn.loc[y, ["mktcap_pct_gdp", "mktcap_usd", "stockstraded_pct_gdp"]].notna().all()]
    latest = max(common)
    keep = df[["iso3", "year", "mktcap_pct_gdp", "mktcap_usd", "stockstraded_pct_gdp"]]
    keep.to_csv(PROCESSED, index=False)

    print(f"Exhibit 3 — U.S. vs. China capital-market depth (through {latest})")
    print("-" * 64)
    for yr in [2014, 2019, latest]:
        if yr in us.index and yr in cn.index:
            print(f"  {yr}  market cap % of GDP:   US {us.loc[yr,'mktcap_pct_gdp']:6.1f}   "
                  f"China {cn.loc[yr,'mktcap_pct_gdp']:6.1f}   "
                  f"(US is {us.loc[yr,'mktcap_pct_gdp']/cn.loc[yr,'mktcap_pct_gdp']:.1f}x deeper rel. to GDP)")
    uy = us.loc[latest, "mktcap_usd"] / 1e12
    cy = cn.loc[latest, "mktcap_usd"] / 1e12
    print(f"  {latest}  market cap, absolute:  US ${uy:.1f}T   China ${cy:.1f}T   "
          f"(US is {uy/cy:.1f}x larger)")
    print(f"  [Context — turnover, stocks traded % of GDP, {latest}: "
          f"US {us.loc[latest,'stockstraded_pct_gdp']:.0f}  China {cn.loc[latest,'stockstraded_pct_gdp']:.0f}. "
          f"China's HIGH turnover is retail churn, not exit depth — hence not headlined.]")

    # ---- figure: left = depth %GDP over time; right = absolute size latest year ----
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 5.6),
                                   gridspec_kw={"width_ratios": [1.5, 1]})

    axL.plot(us.index, us.mktcap_pct_gdp, "-o", color=US_BLUE, lw=2.5, ms=4,
             label="United States")
    axL.plot(cn.index, cn.mktcap_pct_gdp, "-o", color=CN_RED, lw=2.5, ms=4,
             label="China")
    for series, color in [(us, US_BLUE), (cn, CN_RED)]:
        yv = series.loc[latest, "mktcap_pct_gdp"]
        axL.annotate(f"{yv:.0f}%", (latest, yv), textcoords="offset points",
                     xytext=(8, 0), color=color, fontweight="bold", fontsize=10, va="center")
    axL.set_title("Depth relative to the economy", fontsize=12, fontweight="bold", loc="left")
    axL.set_ylabel("Stock-market capitalization (% of GDP)")
    axL.yaxis.set_major_formatter(PercentFormatter())
    axL.set_ylim(0, 240)
    axL.grid(axis="y", color="#e3e3e3", lw=0.8)
    axL.spines[["top", "right"]].set_visible(False)
    axL.legend(loc="upper left", frameon=False, fontsize=11)
    axL.set_xlim(2003, latest + 2)

    axR.bar([0, 1], [uy, cy], color=[US_BLUE, CN_RED], width=0.6, zorder=3)
    axR.set_xticks([0, 1])
    axR.set_xticklabels([f"United States", "China"], fontsize=10.5)
    for x, v in [(0, uy), (1, cy)]:
        axR.text(x, v + uy * 0.02, f"${v:.0f}T", ha="center", fontweight="bold",
                 fontsize=12, color=US_BLUE if x == 0 else CN_RED)
    axR.set_title(f"Sheer scale, {latest}", fontsize=12, fontweight="bold", loc="left")
    axR.set_ylabel("Total stock-market capitalization (US$ trillion)")
    axR.set_ylim(0, uy * 1.18)
    axR.grid(axis="y", color="#e3e3e3", lw=0.8, zorder=0)
    axR.spines[["top", "right"]].set_visible(False)
    axR.text(0.5, uy * 1.10, f"US market is {uy/cy:.0f}x larger", ha="center",
             fontsize=10.5, color="#333333", style="italic", transform=axR.get_xaxis_transform() if False else axR.transData)

    fig.suptitle("America's exit machine: far deeper capital markets than China's",
                 fontsize=14.5, fontweight="bold", x=0.012, ha="left", y=1.0)
    fig.text(0.012, 0.945,
             "Stock-market capitalization is the backbone of the exit ecosystem founders rely on — where firms IPO and the "
             "currency that funds acquisitions.",
             fontsize=9.3, color="#444444", ha="left")

    fig.text(0.012, -0.02,
             "Source: World Bank, World Development Indicators (CM.MKT.LCAP.GD.ZS, CM.MKT.LCAP.CD; data from World Federation of "
             "Exchanges/Refinitiv), accessed 2026-06-22.\nMarket-cap depth shown, not trading volume: China's share turnover is "
             "higher than the U.S. (retail-driven) and is a poor measure of exit depth. Much of China's listed cap is state-owned.",
             fontsize=7.5, color="#666666", va="top")

    fig.tight_layout(rect=[0, 0.02, 1, 0.92])
    fig.savefig(FIG, dpi=200, bbox_inches="tight")
    print(f"\n  Figure written to {FIG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
