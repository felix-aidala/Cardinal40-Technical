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

## Exhibits

The final exhibit document is [`exhibits/Exhibit_Document.md`](exhibits/Exhibit_Document.md)
(Deliverable 1: each exhibit + plain-English annotation + source citation).

| # | Title | Argument it serves |
|---|-------|--------------------|
| 1 | Industry has caught up with academia as new U.S. PhDs' destination (1970s–2024) | The locus of frontier innovation has shifted from the academy to industry/founders — the "multi-industry moment." |
| 2 | Founders are not interchangeable managers (Lee, Kim & Bae 2020) | An exogenous founder→professional-CEO switch cuts citation-weighted patent output ~44% — founders measurably matter. |
| 3 | America's exit machine: capital-market depth, U.S. vs. China | The U.S. can finance the swing, reward the win, and recycle the capital — a far deeper exit ecosystem than China's. |

**Scoping changes from the initial sketch** (see `logs/ai_interaction_log.md`, Session 2):
- *Exhibit 2* presents Lee, Kim & Bae's **published estimates** rather than a
  reproduced event study — their sudden-death dataset is hand-collected and not
  redistributable, so re-running it is neither feasible nor honest.
- *Exhibit 3* pivoted from raw "venture failure rates" (which are not
  cross-country comparable in how "failure" is defined) to **exit-market depth**,
  the more defensible and better-sourced version of the same point — and the one
  the client herself emphasized.

## Reproducing the exhibits

Each exhibit is produced by a self-contained script in `code/`. From the repo root:

```bash
pip install -r requirements.txt
python code/exhibit1_stem_phd_pathways.py
python code/exhibit2_founder_ceo_innovation.py
python code/exhibit3_exit_market_depth.py   # add --refresh to re-pull World Bank data
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
