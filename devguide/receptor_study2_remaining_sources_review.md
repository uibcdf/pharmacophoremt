# BRD4 final three leads and nine-source disposition — 2026-11-06

Owners LMMV/dprada; [#106](https://github.com/uibcdf/pharmacophoremt/issues/106),
parent [#103](https://github.com/uibcdf/pharmacophoremt/issues/103). After the
[sixth-source review](receptor_study2_sixth_source_method_review.md), separate dated
plans nominate the final three leads in the fixed descending-raw-SID/ascending-AID
order: [1805218](evidence/brd4_seventh_source_method_plan_20261106.json),
[1805772](evidence/brd4_eighth_source_method_plan_20261106.json) and
[1804941](evidence/brd4_ninth_source_method_plan_20261106.json).
Each preceding disposition is recorded before the next nomination. No activity
balance or PHMT score enters selection, and earlier outcomes remain intact.

The [combined receipt](evidence/brd4_remaining_sources_20261106_summary.json)
retains distinct run identities, original byte hashes, executable documentary
checks, source contradictions, failed curator openings and private-exposure
identities. All nine declared method leads have now received bounded review.
This does not exhaust BRD4 sources: the census's 19 unresolved-domain records
remain unresolved, neither excluded nor admitted; a further review needs its
own declaration.

## Complete original receiving

Each source's description, summary and patent return HTTP 200: nine serial
requests, no retry. Version/revision/source identity/count gates pass; fresh
canonical Name/Description hashes match their original census projections.
The original bodies and derived prose/tables remain private.

| AID | Source/version/revision | Raw SID/CID | Original patent HTML: bytes / SHA-256 |
| --- | --- | --- | --- |
| 1805218 | BindingDB_9669_1, 3/2 | 124/124 | US10899769B2: 1,678,407 / `51c18dc0cf6b6b158f69e9783eea54f514b05e38c82d014548e63d435dc43770` |
| 1805772 | BindingDB_10057_2, 3/2 | 122/121 | US11058688B2: 1,410,744 / `812ca4cc90e1bf8f3de43f7f8f972312945f35c3cf7f9157893a26a521ef332f` |
| 1804941 | BindingDB_9475_1, 3/2 | 104/104 | US10807982B2: 2,297,528 / `673904f2d4e3e8079d077c97f2ce7d63789816dd4fd7cb358a090d44f46b8696` |

These source counts are not independent molecules, measured class balance or
evidence that every reported value is experimental.

## AID 1805218: experimental versus predicted provenance conflicts

[US10899769B2](https://patents.google.com/patent/US10899769B2/en) explicitly
reports GST-tagged CBP and BRD4 49–170 from BPS Bioscience. Its BRD4 AlphaScreen
procedure incorporates the original CBP procedure and uses a variable-slope
IC50 fit. Table 2 separates average CBP and BRD4 IC50 in nM.

The preceding prose illustrates assays for Examples 1–3 and describes other
listed compounds as not made and/or not tested, with predicted activity. Yet
Table 2 extends well beyond Example 3: direct documentary replay finds 135
HTML rows, one blank and **134 distinct numeric-result example records**.
These are literal report labels, not molecular identities or activity classes.
Each nonblank HTML row has a leading empty layout cell and three nonempty data
fields. An initial replay expected three raw cells and failed; the preserved
correction explicitly validates that layout before retaining all records.

The contradiction prevents authentication of experimental versus predicted
status and leaves correspondence with PubChem's 124 SIDs unexplained. It
establishes neither a three-record source capacity ceiling nor invalidity of
every curator record. No class balance or independent-group capacity is derived.
The source stays pending for original-data/curation authority.

The original buffer and metadata literally state 100 nM NaCl; the incorporated
negative-control text names GST-CBP. Neither becomes 100 mM or a BRD4-specific
control by inference. Actual experimental species/accession and a source-specific
protein catalogue/lot link remain open. A failed curator opening returns a tool
cache miss, not an accepted source body; indexed human annotations do not resolve
these questions.

## AID 1805772: incorporated method received, actual material still unqualified

[US11058688B2](https://patents.google.com/patent/US11058688B2/en) supplies the
full CBP procedure incorporated by its BRD4 49–170 AlphaScreen assay. GST tag
and BPS supplier are explicit; Table 1 reports average BRD4 IC50 in nM separately
from CBP. Here the introduction names Examples 1–126 and distinguishes other
predicted compounds. Do not transfer the preceding patent's Examples 1–3 claim,
record counts or results to this source. Shared protocol text proves neither
identical experiments nor independent chemical series.

The source again retains 100 nM NaCl and the CBP negative-control wording.
A bounded vendor search identifies a compatible human BRD4 49–170/GST product,
BPS catalogue 31040. The indexed datasheet describes a real vendor product;
the patent does not identify that catalogue/lot as its actual material. Product
compatibility therefore does not authenticate the assay protein or authorize
substitution of the vendor formulation for the assay buffer. Species/accession,
material linkage, control interpretation and individual-row authority remain
pending. The source-specific curator page also fails to open with a cache miss.

## AID 1804941: source-specific intervals and cited-material transfer

[US10807982B2](https://patents.google.com/patent/US10807982B2/en) reports
BRD4 BD1 AlphaScreen binding, 2 nM protein and 15 nM acetylated H4 peptide
explicitly final, and a four-parameter IC50 fit. Preserve the protein-name
literal `BREM` in both the original and metadata; no spelling repair or
different-protein inference is performed.

Table 3 separates the BRD4 binding column from Raji/HL-60/H460 cellular IC50.
Its legend states µM and the following source intervals:

| Original category | Reported IC50 interval |
| --- | --- |
| A | ≤0.5 µM |
| B | >0.5 to ≤5 µM |
| C | >5 µM |

These are author intervals, not exact numeric values, adopted PHMT labels or
evidence of class capacity. Earlier patents' thresholds are not transferred.

The patent cites the Nature 2010 method already received and reviewed in the
[original source review](receptor_study2_source_review.md). That work documents
human cDNA and His-BD1; it does not by itself authenticate the exact construct
or experimental transfer in this patent. Preserve that inference boundary,
the original name inconsistency and the separate row/curation/rights questions.
No paper/supplement acquisition, sequence correspondence or activity calculation
is repeated by this review.

## Current disposition of the fixed nine-lead list

| AID | Bounded outcome |
| --- | --- |
| 1805333 | Declared weak-class capacity below 50; source/design stop retained |
| 1795677 | Coupled original report; no transferred class counts or new independence claim |
| 1797292 | Original unit and actual material remain pending after PDF/PCT review |
| 1797167 | Original method/unit supported; actual material and row authority pending |
| 2061300 | Original FP-derived Ki/nM supported; actual material, tracer and row authority pending |
| 1798835 | Original BD1 TR-FRET Ki/µM supported; actual material, probe Kd/calculation and row authority pending |
| 1805218 | Experimental/predicted provenance contradiction, material and control authority pending |
| 1805772 | Incorporated original method/unit supported; actual material, controls and row authority pending |
| 1804941 | Original binding context/intervals supported; exact material transfer and row authority pending |

No source is newly admitted for activities, cohort preparation or scoring.
Both full #103 biological studies remain incomplete. An additional source search
must be a new declared review; it cannot silently change these outcomes or select
a source by favorable observed performance.

## Concrete authority questions and retention

The next evidence needed is source-specific clarification, not another automatic
activity download. Draft questions, **not sent**, are:

1. For entry 9669, which Table 2 records were actually measured, and which were
   predicted? How does that distinction map to the 124 curated SIDs?
2. For entries 9669/10057, which protein catalogue/lot, species, accession and
   construct were measured? What original authority resolves the NaCl and
   BRD4 negative-control wording?
3. For entry 9475, what establishes the exact assayed construct/material transfer
   from the cited 2010 method and the curation of source interval relations?

Source-curation/license version, interference/orthogonal confirmation and later
MolSysMT-owned identity/state/series eligibility remain separate obligations.
These drafts authorize no external contact or automatic admission.

All prior #66/#106 exposures remain additive. Original chemistry, numeric table
values, vendor/search snippets and nearby cellular text have been exposed;
no molecular aliases, class frequencies, labels or unseen-holdout claim follows.
Raw source/navigation/exposure stays private. Receiving is serial on CPU 19,
100% quota, 512 MiB/no swap, 32 tasks, nice 19, idle I/O and one backend thread;
actual per-source observations and failures are in the receipt. Offline review
uses one CPU/low priority and a 512 MiB address-space limit without a no-swap or
performance claim. Shared Conda/providers remain unchanged. The three owned
capsules named in the receipt are retained through 2026-11-20 or relevant change.
