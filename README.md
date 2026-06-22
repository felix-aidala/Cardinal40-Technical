# Cardinal40 — "Founders as the Next Offset" — Economist Technical Assignment

Research and data backbone for an essay arguing that America's entrepreneurial
(founder) class is its best strategic asset in the techno-economic competition
with China. This repository contains all code, data, and documentation used to
produce the exhibits in the accompanying exhibit document.

**Author:** Felix Aidala
**Prepared for:** Cardinal40 (Economist role)
**Date:** June 2026

---

## Repository structure

```
.
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── code/                      # One script per exhibit (pull → clean → plot)
├── data/
│   ├── raw/                   # Raw downloaded data (or download instructions)
│   └── processed/             # Cleaned, analysis-ready data
├── exhibits/                  # Output figures + the exhibit document
└── logs/
    └── ai_interaction_log.md  # Deliverable 3: log of LLM interactions
```

## Planned exhibits

| # | Working title | Argument it serves |
|---|---------------|--------------------|
| 1 | Share of U.S. STEM PhDs entering academia vs. industry over time | The locus of frontier innovation has shifted from the academy to industry/founders — the "multi-industry moment." |
| 2 | Event study: effect of a founder's exit on firm productivity (Lee, Kim & Bae 2020) | Founders are not interchangeable managers; their departure measurably hurts the firm — why founders matter. |
| 3 | Venture/startup failure rates, U.S. vs. China | The U.S.'s high-churn, "ruthless capitalist" model vs. China's state-supported industry — and why selecting the right founders is the fund's value-add. |

> Exhibit definitions are preliminary and subject to revision after scoping discussion.

## Reproducing the exhibits

Each exhibit is produced by a self-contained script in `code/`. From the repo root:

```bash
pip install -r requirements.txt
python code/exhibit1_stem_phd_pathways.py
python code/exhibit2_founder_exit_event_study.py
python code/exhibit3_venture_failure_rates.py
```

Each script reads from `data/`, writes a figure to `exhibits/`, and prints the
key figures it computes. Data sources, access dates, and any redistribution
restrictions are documented at the top of each script and in the exhibit document.

## Methodological transparency

The goal of this repo is reproducibility and trust, not coding elegance. Anyone
reading it should be able to trace exactly how each exhibit went from raw data
to final figure. Key methodological choices (variable construction, sample
restrictions, deflators, etc.) are documented inline and in the exhibit document.

## AI tool usage

Per Deliverable 3, `logs/ai_interaction_log.md` records substantive interactions
with LLM tools, how they were used, and how AI-generated claims (statistics,
citations) were independently verified.
