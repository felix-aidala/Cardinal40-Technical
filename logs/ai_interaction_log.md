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
