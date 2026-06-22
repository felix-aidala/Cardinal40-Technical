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
