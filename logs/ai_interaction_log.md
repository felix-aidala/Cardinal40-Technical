# AI Interaction Log — Cardinal40 Economist Assignment

**Deliverable 3.** A running log of substantive interactions with LLM tools used
on this project, what each was used for, and how AI-generated claims were
verified. Entries are appended chronologically. The division of labor follows
the assignment's own guidance: AI is used for synthesis, drafting, scaffolding,
and brainstorming — **never** as an unverified source of statistics or
citations. Every number and source that lands in an exhibit is traced back to a
primary source and checked by hand.

**Tool:** Claude (Cowork mode), model `claude-opus-4-8`.

---

## Session 1 — Project setup & exhibit scoping — 2026-06-22

**Goal.** Stand up project infrastructure (this log + a reproducible Git
repository) and capture the candidate's three preliminary exhibit ideas before
detailed scoping.

**What the AI did**
- Read the briefing package (`Cardinal40_Economist_Package.docx`): technical
  assignment, client brief, and intake transcript. Summarized the core thesis
  ("founders as the next offset") and the three required deliverables.
- Confirmed the toolchain: `git` available locally; no `gh` CLI or GitHub
  credentials in the environment, and no GitHub MCP connector. Decision: build a
  complete, committed local repo and hand off two push commands rather than
  transmit any credentials.
- Scaffolded the repository (`README.md`, `.gitignore`, `requirements.txt`,
  `code/`, `data/raw`, `data/processed`, `exhibits/`, `logs/`).

**Decisions made with the user**
- GitHub: local repo + manual push (credentials stay with the user).
- Analysis language: Python (pandas / matplotlib).

**Preliminary exhibit ideas captured (to be scoped next)**

1. **STEM PhD career pathways over time** — A time series of the share of U.S.
   STEM PhD graduates entering academia vs. industry. Purpose: illustrate the
   shift of frontier innovation from the academy to industry/founders. Framing
   the user offered: Oppenheimer built the bomb as an academic on leave; today's
   equivalent leaders sit in industry (e.g., Anthropic is run by PhDs).
   *Likely sources to vet:* NSF Survey of Earned Doctorates (SED) /
   National Center for Science & Engineering Statistics (NCSES).

2. **Founder-exit event study** — An event-study figure using Lee, Kim & Bae
   (2020) showing the effect of a founder's departure on firm productivity.
   Purpose: evidence that founders are not interchangeable — they matter.
   *To verify:* exact citation, what the paper actually estimates, sample,
   and whether the underlying data are redistributable or must be reconstructed.

3. **Venture failure rates, U.S. vs. China** — A figure comparing startup/VC
   failure rates in the U.S. against China (data permitting). Purpose: contrast
   the U.S.'s high-churn "ruthless capitalism" with China's more heavily
   state-supported industry, and underscore that picking the right founders is
   the fund's value-add.
   *To verify:* comparability of "failure" definitions across the two countries —
   this is the main analytical risk and must not be glossed.

**Verification notes / open risks**
- No statistics have been produced yet; nothing to verify this session.
- Flagged for next session: (a) confirm the Lee, Kim & Bae (2020) citation is
  real and says what we think — high hallucination risk on academic citations;
  (b) U.S.–China failure-rate comparability is the key methodological hazard for
  Exhibit 3.

**Next steps.** Scope each exhibit with the user, then locate and vet primary
data sources before writing any analysis code.

---

## Session 2 — Source verification & building the three exhibits — 2026-06-22

**Goal.** Clear the two flagged verification hazards, then build all three
exhibits (code + data + figures + annotations) and the exhibit document.

**Verification done FIRST, before any code (the important part)**

1. *Exhibit 2 citation (flagged high hallucination risk).* The AI proposed
   "Lee, Kim & Bae (2020)" on a founder *exit* event study. Verified against
   primary records: the paper is **real** but the earlier description was
   **wrong in two ways**. Correct citation: Lee, Joon Mahn; Kim, Jongsoo; Bae,
   Joonhyung (2020), "Founder CEOs and innovation: Evidence from CEO sudden
   deaths in public firms," *Research Policy* 49(1), 103862,
   DOI 10.1016/j.respol.2019.103862. (a) Identification is **CEO sudden
   deaths**, 1979–2002 — not voluntary exits. (b) Outcome is
   **citation-weighted patent count** (−43.8% on a founder→professional
   transition), not "productivity" generically. The verbatim abstract was read
   from the publisher/RePEc record to confirm the 43.8% figure, the "controls
   for R&D" qualifier, and the mechanism findings. **Consequence:** because the
   dataset is hand-collected and not redistributable, we do **not** reproduce
   the event study; we present the paper's published estimates and label them as
   such. This is exactly the AI-misuse the assignment warns about (confusing
   studies / inventing methods), caught by checking the primary source.

2. *Exhibit 3 comparability (flagged key methodological hazard).* "Venture
   failure rates, U.S. vs. China" cannot be built honestly because "failure" is
   not defined comparably across the two systems. Decided with the user to pivot
   to **exit-market depth**, which is the defensible, better-sourced version of
   the same argument (and the one the client emphasized in the intake).

**What the AI did (and how each number was checked)**

- *Exhibit 1.* Located NCSES SED Table 2-6 (the authoritative 1994–2024 trend
  table). The summary numbers a web tool returned (52%→33% academe, 2002→2022)
  came from a *different* SED cycle; rather than trust that paraphrase, the
  actual Table 2-6 PDF was downloaded and parsed with `pdfplumber`, and the
  transcribed values were written by hand into the raw CSV. All plotted/printed
  figures derive from that transcription, not from any LLM-stated statistic.
- *Exhibit 2.* Built a figure from the paper's own reported magnitude (−43.8%,
  indexed to founder-led = 100 → 56.2) plus its qualitative mechanism findings.
  No statistic originates with the LLM.
- *Exhibit 3.* Pulled market-cap series live from the **World Bank API**
  (CM.MKT.LCAP.GD.ZS, CM.MKT.LCAP.CD, CM.MKT.TRAD.GD.ZS) for USA/CHN and cached
  a snapshot. While inspecting the data the AI caught that stock *turnover* is
  actually higher in China (retail churn) — so headlining "trading volume" would
  have been misleading. Switched the headline metric to market-cap depth and
  documented the turnover nuance in the annotation. (Example of using the data
  itself to overrule a plausible-but-wrong framing.)

**Division of labor.** AI was used for: locating candidate sources, parsing
PDFs/JSON, drafting code and annotations, and catching framing errors. AI was
**not** used as a source of any statistic — every number in an exhibit traces to
NCSES, the published paper, or the World Bank, with URLs and access dates in the
exhibit document and in each script header.

**Open items / honest limitations**
- Exhibit 2 is a presentation of published results, not an independent
  reproduction (data not redistributable) — stated plainly in the exhibit.
- Exhibit 3 uses public-equity depth as a proxy for the whole exit ecosystem;
  M&A and secondary-market depth would strengthen it but lack a single clean,
  free, cross-country source. Flagged in the annotation.

**Next steps.** Optional: commit and push to GitHub (Deliverable 2) — repo is
local; hand off push commands so credentials stay with the user.

---

## Session 3 — Extending Exhibit 1 back to the 1970s — 2026-06-22

**Goal.** User asked whether Exhibit 1 could go farther back than 1994.

**What the AI did**
- Established first that the *exact* current series (S&E-only, definite
  non-postdoc commitments) is only *published* back to 1994: NCSES labels Table
  2-6 a "trend" table starting in 1994, and older published sector tables aren't
  S&E-specific. Going earlier in S&E would require restricted microdata (RDAS /
  WebCASPAR).
- Identified a longer, *different* series (academic share of the employed S&E
  doctoral workforce, from the Survey of Doctorate Recipients) and flagged that
  splicing a stock measure onto our flow measure would be the same comparability
  sin we avoided in Exhibit 3 — so it was offered only as labeled context.
- After the user chose to extend with comparable data, **downloaded and parsed
  three historical SED report PDFs** (`pdfplumber`): NSF "U.S. Doctorates in the
  20th Century" (NSF 06-319) and the NORC/NSF Summary Reports 1998 & 2006.
  Found the same measure (sector among new doctorates with a definite U.S.
  *employment* commitment; postdocs are a separate "study" commitment) in:
  Table 6-3 (1970–74 and 1995–99) and Table 30 (selected years 1986–2006).

**Verification / comparability checks (the important part)**
- Confirmed all three vintages define "industry" to include self-employment and
  measure the same employment-commitment base — so they are comparable.
- **Seam check:** Table 30's 1991 (academe 52.6 / industry 21.4) flows smoothly
  into Table 2-6's 1994 (51.2 / 21.1); and the 20th-century report's 1995–99
  averages (49.4 / 26.6) match Table 2-6's 1999 (48.8 / 27.5). Independent
  vintages agreeing at the seams is strong evidence the splice is valid.
- **Caught a false-comparability trap:** the 1998 Summary Report's sector table
  (academe 50.0%) *includes postdocs in academe* (its footnote 20), unlike the
  modern non-postdoc measure — so that particular table was NOT used. Only the
  employment-commitment tables (which exclude postdocs, same as Table 2-6) were.
- To avoid mixing vintages within one stretch, used the single current NCSES
  table for all of 1994–2024; older vintages only supply pre-1994 points.

**Decision with the user.** Because a strictly-comparable pre-1994 series exists
only for *all fields* (not S&E-only), the user chose to **switch Exhibit 1's
headline to the all-fields measure, 1970s–2024**. The sharper S&E-specific shift
(industry 22%→52%, academia 58%→30%) is cited in the annotation, sourced to the
same tables.

**Result.** Exhibit 1 now runs early-1970s → 2024 (academia ~67%→40%, industry
~12%→40%), built from three documented sources with per-point provenance in
`data/raw/sed_historical_employment_sector_allfields.csv`.

---

## Session 4 — Exhibit 2 as an event study — 2026-06-22

**Goal.** User asked to display the study's actual *event study*.

**What the AI did**
- Confirmed the published Research Policy paper's headline is a single regression
  estimate (−43.8%); the dynamic event-study figure lives in the working-paper
  version ("Are Founder CEOs Better Innovators? Evidence from S&P 500 Firms").
  Downloaded that PDF and located **Figure 2**, "Switching from Founder CEO to
  Professional CEO" — coefficient-plus-constant from a firm fixed-effects panel
  OLS of ln(1 + citation-weighted patents) on year-relative-to-switch dummies.
- Rendered the figure page to an image and **digitized** the central line and
  95% CI for years −5…+5 into `data/raw/lee_kim_bae_fig2_event_study.csv`.
  Cross-checked the reads by confirming the CI is symmetric about the central
  line at every point (a sanity check that the digitization is internally
  consistent). Flagged ±~0.03 reading error.
- Redrew the event study (flat founder-era pre-trend, break at year 0, continued
  decline) with the eras shaded and the switch marked.

**Honest sourcing notes recorded on the exhibit**
- The event-study figure is the **working-paper** version (S&P 500, 1993–2003);
  the **peer-reviewed** version (sudden deaths, 1979–2002) supplies the cleanly
  identified ~43.8% magnitude. Both are cited; the chart shows the dynamics, the
  caption carries the rigorous number.
- This **presents the authors' figure** (digitized), not a re-estimation — their
  data are not redistributable. The widening post-switch CI is called out so the
  later points are not over-read.

---

## Session 5 — Rotating Exhibit 3 to the ASPI "flip" — 2026-06-22

**Goal.** User asked to rotate Exhibit 3 to something easier to explain — a
U.S.-vs-China technological-innovation comparison.

**What the AI did**
- Flagged a framing consequence up front: a US-vs-China innovation comparison
  serves the *stakes* pillar (China is ahead) rather than the *US-advantage*
  pillar the old exit-market exhibit served — a deliberate, useful rebalance.
- After the user chose the "who leads critical technologies" angle, used the
  **ASPI Critical Technology Tracker** — the dataset the client names by name in
  the intake transcript. Verified the headline figures against ASPI's own
  Strategist write-up: across 64 technologies, the U.S. led 60 (China 3) in
  2003–2007, vs. the U.S. 7 (China 57) in 2019–2023. Confirmed release date
  (Aug 2024) and the metric.

**Verification / honest framing**
- Pinned down exactly what "leading" means: highest national share of the world's
  **top 10% most-cited publications** in a technology over a 5-year window. This
  is **research leadership — a leading indicator — not manufacturing or deployed
  capability.** That distinction is stated on the chart and in the annotation,
  and it is the bridge to the founder thesis (leading in research ≠ turning
  research into dominant companies).
- Noted that the 64 total is not fully split between US and China (a small
  remainder is led by other countries), so the exhibit avoids implying a strict
  two-way partition.

**Removed** the prior exit-market Exhibit 3 (script, figure, World Bank raw and
processed data) to keep the repo to exactly the three current exhibits.

**Time-series version.** User then asked for a time series instead of two grouped
periods. Parsed the full report PDF and recovered the counts ASPI actually
publishes: China at four windows (3 in 2003–07, 28 in 2013–17, 52 in 2018–22, 57
in 2019–23) but the U.S. at only the two endpoints (60, 7). The report's figures
are per-technology research-share charts, not a count-led-over-time series, and
the full window-by-window data sits behind ASPI's (partly gated) interactive
tool. Rather than fabricate the missing U.S. points, the chart plots China's four
real points as a solid line and the U.S.'s two endpoints as a **dashed** connector
explicitly labeled "endpoints only." Used only the 2024 two-decade report (a
single consistent 64-technology framework) — deliberately not the 2023 report,
which tracked 44 technologies and would not be comparable.

---

## Session 6 — Reverting Exhibit 3 to the exit-machine version — 2026-06-22

**Goal.** User decided to go back to the original Exhibit 3 — the U.S.-vs-China
capital-market-depth ("exit machine") figure showing America's enduring funding
advantage — and drop the ASPI critical-technology "flip."

**What the AI did**
- Briefly considered a third option the user floated (an H-1B-applicants time
  series for "human-capital advantage endures"); flagged two honest points before
  building anything: H-1B is a *non-immigrant work visa*, not green-card
  immigration, and approvals are flat by the 85k statutory cap so the signal
  lives in *demand* (registrations), which is also distorted by FY2024 lottery
  gaming. User then opted to restore the prior exit-market exhibit instead, so the
  H-1B chart was not built.
- Recovered the original Exhibit 3 from git history (commit 71049f5): the
  `exhibit3_exit_market_depth.py` script, its processed data, and the cached
  World Bank raw snapshot. Removed the ASPI files (script, figure, raw CSV).
- Re-ran the script; figure reproduces the documented numbers exactly (U.S.
  market cap 216% of GDP vs. China 63%, 3.4× deeper; $62T vs. $12T, ~5× larger,
  2024). Restored the Exhibit 3 annotation/source in the exhibit document and the
  Exhibit 3 row, scoping note, and reproduce command in the README.

**Note.** Session 5's ASPI work is left in this log as an honest record of the
detour; the repo again contains exactly three exhibits, with Exhibit 3 back to
exit-market depth.
