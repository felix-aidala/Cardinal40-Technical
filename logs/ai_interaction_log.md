# AI Interaction Log — Cardinal40 Economist Assignment

**Deliverable 3.** An overview of how I used AI tools on this assignment: what I
used them for, where I deliberately did not, and how I verified anything AI
produced. The detailed, commit-by-commit trail is preserved in this repository's
Git history; this document is the high-level account.

**Tool.** Claude (Cowork mode), model `claude-opus-4-8`, run locally with access
to the shell, the filesystem, and the web.

## How I used AI

I treated AI as a research assistant and pair-programmer, not as a source of
facts. Concretely, I used it to:

- **Brainstorm and scope** the three exhibits — pressure-testing framings,
  surfacing alternatives, and talking through which version of each argument was
  most defensible. Exhibit 3 in particular went through several rounds before
  settling on U.S. venture capital vs. the G7.
- **Find and retrieve primary sources** — locating the relevant NCSES/SED tables,
  the Lee–Kim–Bae founder-CEO paper, and the OECD venture-capital series, then
  downloading and parsing the underlying PDFs, JSON, and API responses
  (`pdfplumber`, the World Bank and OECD APIs).
- **Write code and prose** — drafting the self-contained Python scripts that pull,
  clean, and plot each exhibit, and drafting the annotations and repository
  documentation, which I then edited myself.
- **Catch errors in my own framing** — using the data itself to overrule
  plausible-but-wrong narratives (see below).

## Verification discipline (the part that matters)

Every statistic and citation that appears in an exhibit traces to a primary
source — NCSES, the published paper, the World Bank, or the OECD — with URLs and
access dates recorded in the exhibit document and each script header. No number
originates from an AI assertion. A few examples where verification actually
changed the work:

- **A citation check caught real errors.** Before building Exhibit 2, I verified
  the founder-CEO paper against primary records. The paper is real, but the
  initial description of it was wrong on two points: the identification is *CEO
  sudden deaths* (not voluntary exits) and the outcome is *citation-weighted
  patents* (not "productivity" generically). I read the abstract verbatim to
  confirm the ~43.8% magnitude and its R&D control. Because the data are
  hand-collected and not redistributable, I present the authors' published
  estimates rather than re-running the analysis — and say so on the exhibit.
- **The data overruled the framing, twice.** In an earlier version of Exhibit 3,
  the data showed Chinese stock *turnover* is actually higher than the U.S.
  (retail churn), so I dropped trading volume as a headline metric. In the final
  Exhibit 3, the OECD data showed the U.S. is *not* first worldwide on VC/GDP —
  Israel is — so I scoped the chart to the G7 and acknowledged Israel explicitly
  rather than quietly omitting it.
- **Transcription and splicing were checked by hand.** Figures parsed from source
  PDFs were transcribed into the raw CSVs and spot-checked; where Exhibit 1
  splices three historical SED vintages, I confirmed the series agree at the
  seams and excluded one table whose definition (postdocs counted as academia)
  was not comparable.

## What I did not use AI for

- As a source of any statistic, magnitude, or citation — all are traced to
  primary data and checked by hand.
- To reproduce analyses whose underlying data are not redistributable (Exhibit 2
  is presented as published, not re-estimated).

## Honest limitations

- Exhibit 2 presents published results rather than an independent reproduction
  (the authors' data are not redistributable).
- Exhibit 3 measures venture capital specifically — one channel of startup
  finance, not the whole exit ecosystem.
