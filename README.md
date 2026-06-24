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
| 2 | Founders are not interchangeable managers — event study (Lee, Kim & Bae) | Firm innovation is flat through the founder years, then drops sharply at a founder→professional-CEO switch (published sudden-death design: ~44%). |
| 3 | Financing the swing: U.S. venture capital dwarfs the rest of the G7 | America doesn't just produce valuable founders — it funds them at a scale no peer economy approaches, which is why the U.S. (not its allies) is the one equipped to challenge China. |

**Scoping changes from the initial sketch** (see `logs/ai_interaction_log.md`):
- *Exhibit 1* was extended back to the early 1970s using historical SED report
  vintages; this required switching from S&E-only to an all-fields measure (the
  only one comparable that far back). The sharper S&E shift is cited in the
  annotation.
- *Exhibit 2* displays the authors' own **event study** (the dynamic figure from
  the working-paper version), with the peer-reviewed sudden-death magnitude
  (~44%) cited as the rigorously-identified number. We present the published
  figures; the data are not redistributable.
- *Exhibit 3* went through two scoping moves. It first pivoted from raw "venture
  failure rates" (not cross-country comparable in how "failure" is defined) to a
  U.S.-vs.-China **exit-market depth** chart. That direct U.S.–China comparison
  was then dropped: it leaned on Chinese market-structure data that is hard to
  vouch for, and it was the only exhibit carrying a head-to-head comparison
  (Exhibits 1 and 2 are both U.S. series). The final exhibit instead measures the
  "finance the swing" leg directly — **U.S. venture capital as a share of GDP vs.
  the rest of the G7** (OECD) — making the point that even among America's closest
  peers, the U.S. is uniquely resourced to fund founders, and is therefore the
  country positioned to challenge China. The China contrast stays in the prose.

## Reproducing the exhibits

Each exhibit is produced by a self-contained script in `code/`. From the repo root:

```bash
pip install -r requirements.txt
python code/exhibit1_stem_phd_pathways.py
python code/exhibit2_founder_ceo_innovation.py
python code/exhibit3_vc_gdp.py
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
