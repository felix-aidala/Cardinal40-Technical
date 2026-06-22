# Exhibit Document — "Founders as the Next Offset"

**Deliverable 1.** Three exhibits supporting the argument that America's founder
class is its decisive asset in the techno-economic competition with China. Each
entry contains the exhibit, a plain-English annotation written for a smart
non-economist, and a full source citation. Figures are reproducible from the
scripts in [`code/`](../code); see the repository [README](../README.md).

**Author:** Felix Aidala · **Prepared for:** Cardinal40 (Economist role) · **Date:** June 2026

The three exhibits trace one logical chain:

1. **Where frontier talent now works** — innovation has moved from the academy into industry and company-building (the "multi-industry moment").
2. **Why the founder specifically matters** — founders are not interchangeable managers; remove them and innovation measurably falls.
3. **Why America's system wins** — the U.S. has a vastly deeper exit machine to finance, reward, and recycle those founders than China does.

---

## Exhibit 1 — Since the 1970s, industry has caught up with academia for new U.S. PhDs

![Exhibit 1](exhibit1_stem_phd_pathways.png)

**Annotation.** Over half a century, the destination of new U.S. PhDs who take a
definite job (not a postdoc) has been transformed: academia's share fell from
about two-thirds (67%) in the early 1970s to ~40% in 2024, while industry's rose
from ~12% to ~40% — the two are now essentially even. The headline for the
writer: the academic career has gone from *the* default to one of two co-equal
paths, as the country's most highly trained talent steadily reallocates toward
industry and company-building. **The nuance that strengthens the thesis:** this
chart is *all fields*; within **science & engineering specifically**, the shift
is far sharper — industry rose from 22% (1970–74) to **52%** (2024) while
academia fell from 58% to **30%**, so in exactly the technical fields the offset
depends on, industry has *decisively* overtaken the university. **What not to
overclaim:** this measures *first destinations* of those going straight to work
(postdocs excluded), not *where the best science happens*; the 2004 academic
uptick is a real post-dot-com blip, not noise; and the pre-1994 points come from
earlier SED report vintages (same measure — the series agree where they meet),
with the academic decline concentrated in the 1970s.

**Sources.** Three vintages of the same NSF/NCSES measure (sector of new research
doctorate recipients with a definite U.S. employment commitment; postdocs
excluded; "industry" includes self-employment):
(1) **1970–74** — NSF/SRS (2006), *U.S. Doctorates in the 20th Century*, NSF
06-319, Table 6-3 (five-year average). 
(2) **1986, 1991** — NORC/NSF, *Doctorate Recipients from U.S. Universities:
Summary Report 2006*, Table 30 (selected years 1986–2006).
URL: https://www.norc.org/content/dam/norc-org/pdfs/SED_Sum_Rpt_2006.pdf
(3) **1994–2024** — NCSES, *Survey of Earned Doctorates 2024*, Table 2-6, NSF
25-349.
URL: https://ncses.nsf.gov/pubs/nsf25349/assets/data-tables/tables/nsf25349-tab002-006.pdf
All accessed 2026-06-22. The 1994–2024 segment uses the single current NCSES
trend table (no vintage-mixing within it). Per-point sourcing in
[`data/raw/sed_table2-6_employment_sector.csv`](../data/raw/sed_table2-6_employment_sector.csv)
and
[`data/raw/sed_historical_employment_sector_allfields.csv`](../data/raw/sed_historical_employment_sector_allfields.csv).

---

## Exhibit 2 — Founders are not interchangeable managers

![Exhibit 2](exhibit2_founder_ceo_innovation.png)

**Annotation.** Using CEO *sudden deaths* at U.S. public firms (1979–2002) as a
natural experiment — so the change of leadership is unrelated to how the firm was
already doing — Lee, Kim & Bae (2020) find that an exogenous switch from a
founder-CEO to a professional CEO is associated with a **43.8% drop in
citation-weighted patent output**, even after controlling for R&D spending. The
headline for the writer: this is the cleanest available answer to the skeptic who
says "a good manager can run the company once it's built" — the data say no, the
founder is doing something that does not transfer. The mechanism matters and is
quotable: the effect is *not* that founders spend more on R&D (they don't); it's
that they manage and **retain** innovative people — inventors leave after a
founder is replaced. **Nuance not to overclaim:** this is one well-identified
study of *public* firms over a historical window, about *patent-based* innovation
specifically; it is strong evidence that founders matter, not proof that every
founder should stay forever. We **present the paper's published estimates** — we
did not re-run the study (its sudden-death dataset is hand-collected and not
redistributable).

**Source.** Lee, Joon Mahn; Kim, Jongsoo; Bae, Joonhyung (2020). "Founder CEOs
and innovation: Evidence from CEO sudden deaths in public firms." *Research
Policy* 49(1), 103862. DOI: 10.1016/j.respol.2019.103862.
Record: https://ideas.repec.org/a/eee/respol/v49y2020i1s0048733319301817.html
Accessed 2026-06-22. *Method:* event-study/natural-experiment using exogenous
CEO sudden deaths; outcome is citation-weighted patent count, controlling for R&D.
Reported estimates transcribed to
[`data/raw/lee_kim_bae_2020_estimates.csv`](../data/raw/lee_kim_bae_2020_estimates.csv).

---

## Exhibit 3 — America's exit machine: far deeper capital markets than China's

![Exhibit 3](exhibit3_exit_market_depth.png)

**Annotation.** Deep, liquid public-equity markets are the backbone of the exit
ecosystem founders depend on — the place companies IPO and the currency that
funds acquisitions — and on this measure the U.S. dwarfs China: U.S. stock-market
capitalization is ~216% of GDP vs. China's ~63% (3.4× deeper relative to the
economy) and ~$62 trillion vs. ~$12 trillion in absolute size (~5× larger) in
2024. The headline for the writer: America's structural advantage isn't only that
it produces founders — it's that it can *finance the swing, reward the win, and
recycle the capital*, which is exactly the flywheel a thinner exit market starves.
**The nuance a reader (and a careful critic) might miss:** we deliberately use
market-cap *depth*, not trading volume — China's share turnover is actually
*higher* than the U.S. (≈186% vs. 148% of GDP in 2024), but that reflects retail
speculation, not exit capacity, so it would mislead. Two further caveats: public
markets are a *proxy* for the whole exit ecosystem (M&A and secondaries also
matter), and a large share of China's listed value is state-owned with capital
controls limiting exit and repatriation — so China's *usable* exit depth for a
private investor is arguably thinner still.

**Source.** World Bank, *World Development Indicators* (underlying data: World
Federation of Exchanges / Refinitiv). Indicators CM.MKT.LCAP.GD.ZS (market
capitalization, % of GDP), CM.MKT.LCAP.CD (market capitalization, current US$),
and CM.MKT.TRAD.GD.ZS (stocks traded, % of GDP — context only). Pulled via the
World Bank API, accessed 2026-06-22; snapshot cached in
[`data/raw/worldbank_market_depth.csv`](../data/raw/worldbank_market_depth.csv).
*Coverage:* United States and China, 2003–2024 (absolute market cap available
through 2025). API docs: https://datahelpdesk.worldbank.org/.

---

### How to reproduce

```bash
pip install -r requirements.txt
python code/exhibit1_stem_phd_pathways.py
python code/exhibit2_founder_ceo_innovation.py
python code/exhibit3_exit_market_depth.py   # add --refresh to re-pull World Bank data
```

Each script prints the key figures it computes and writes its figure to this
folder. Methodological choices are documented at the top of each script and in
the annotations above.
