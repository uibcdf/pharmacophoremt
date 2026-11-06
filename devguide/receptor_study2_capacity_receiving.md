# BRD4 capacity census and endpoint review — 2026-11-06

Owners LMMV/dprada; [#106](https://github.com/uibcdf/pharmacophoremt/issues/106),
parent #103. This is source-feasibility evidence, not a receptor screening study.
The [original receipt](evidence/brd4_capacity_20261106_summary.json) preserves
the planning calculation, acquisition, manual decisions, exposure and limits.
No experimental source or cohort has been accepted.

## Published design and complete receiving

The [protocol](receptor_study2_capacity_protocol.md) and
[immutable machine plan](evidence/brd4_capacity_plan_20261106.json) were published
at `327a4161ae11321084fbcdb37bbc77805e6e391a` before these requests. The plan's
SHA-256 is `051798a1cac4ba72df51fb5e8fed0022466b8bddb43c5197834b24b8f528764e`.
The publication gate records a clean worktree and the independently observed
remote head. The original 1,780-AID gene-index body is recovered from the prior
verified archive, rather than a changed target query.

All **1,780 requested AIDs** were received in the declared **37 serial batches**,
with exact distinct AID coverage and typed nonnegative `SIDCountAll` values.
Every attempt returned HTTP 200; no retry, source replacement or access bypass
was needed. Original response hashes, byte counts, URLs, source versions,
revisions and last-change fields remain in the receipt. The first 20 description
versions match the earlier review. This is a dated series of source observations,
not an atomic snapshot of the entire PubChem database.

The preceding SciPy 1.18.1 planning calculation exhausts 144 possible success-count
intervals across n=20/30/40/50. With 50 independent groups per measured class,
the maximum Wilson 95% interval half-width is 0.1335548568317142, below the
declared 0.14 ceiling for a prespecified binary decision rate. These are planning
intervals, not tests or ligands. Actual chemical/series dependence and failed
inputs may prevent that precision; this is neither AUC-difference power nor a
generalization claim. The original result and actual Python/SciPy/native identities
are retained, with before/after equality. #66's separate design is unchanged.

## Capacity outcome and manual endpoint review

There are **84 records with at least 100 raw tested SIDs**. Three were already
excluded genetic sources, leaving **81** for the declared manual review. No SID
count establishes molecule identity, independence or measured class balance.

All **11 sources in the earlier first-20 sample** that were not already excluded
have at most **9 SIDs each**, including AID620195. They cannot supply 50 groups
per class under this design. Their earlier original-method review remains valid
within its scope, but chasing its unread incorporated reference cannot resolve
this capacity failure. This stops that bounded source sample for this design;
it does not reject every BRD4 source or relax the target size.

The later manual screen uses already received source fields, in descending SID
total and ascending AID order, without another HTTP request or activity ranking.
Its declaration records that the first 42 titles had already been inspected.
All 81 are accounted for; the archive contains each disposition, source/field
identity and reason.

| Disposition | Records | Meaning |
| --- | ---: | --- |
| Incompatible with isolated BD1 study | 53 | 46 genetic/cellular-response screens, one cellular NanoBRET target-engagement assay, two explicit BD2 assays and four tandem-domain assays |
| Isolated-BD1 method leads | 9 | Source text identifies isolated BD1 or compatible construct boundaries; human material, original methods and data remain unqualified |
| Unresolved | 19 | Mixed-domain/table assignment, unclear target/construct or insufficient method detail |

The nine leads, in the fixed capacity order, are:

| PubChem AID | Raw SIDs | Original-source lead |
| --- | ---: | --- |
| 1805333 | 499 | US10941160B2, His-BD1 peptide AlphaScreen |
| 1795677 | 494 | US10023592B2, His-BD1 peptide AlphaScreen |
| 1797292 | 300 | US10206931B2, His/Flag-BD1 peptide AlphaLisa |
| 1797167 | 283 | US9763922B2, His/Flag-BD1 peptide AlphaLisa |
| 2061300 | 195 | US12286435B2, BD1 tracer assay; KD/Ki wording needs resolution |
| 1798835 | 184 | US9957263B2, title assigns BD1 K57–E168; verify original column |
| 1805218 | 124 | US10899769B2, BRD4 49–170 peptide assay |
| 1805772 | 122 | US11058688B2, BRD4 49–170 assay incorporating CBP procedure |
| 1804941 | 104 | US10807982B2, BD1 peptide assay with source spelling inconsistency |

This is a lead list, not nine accepted human assays. Preserve original unit,
protein-name, boundary and KD/Ki inconsistencies until the primary source resolves
them. Shared methods, patent titles and related records do not establish dataset
independence; do not pool their SIDs or assume they supply independent series.

AID1806433 has 780 SIDs but remains unresolved: its generic HTRF description does
not identify the BRD4/BD1 construct or relevant reagent definitions, and its source
title concerns CBP/p300. AID1919427 explicitly lacks experimental detail in the
summary. AID743454's detailed fields are placeholders; its explicit RNAi title
and source ID support a genetic-screen exclusion, not a fully reviewed protocol.
Unresolved domain assignments are not silently promoted or discarded as BD2.

## Exposure, reproducibility and execution scope

The summary endpoint delivered full descriptions/protocols/comments and upstream
aggregate activity categories, in addition to total counts. Their original bodies
stay private with SHA-256/byte identities. Published artifacts contain our factual
projections and executable case controllers; they do not redistribute the source
protocol corpus. Source/redistribution rights still require review before a cohort.

Endpoint-bearing sections and titles of all 81 survivors were reviewed; this
does not claim every unrelated genetic protocol step was read. In AID1795677,
the source explicitly exposes Chemistry Example1, named
2-methyl-4-phenylisoquinolin-1-one, with IC50 2.782 micromolar. Record that exposure
without assigning a CID, molecular alias or study label. Other delivered source
sections and aggregate categories remain potentially exposed. No zero-activity-
exposure, blinded source selection or unseen-holdout claim follows. Earlier
ERalpha/#66 and #106 ledgers remain unchanged and additive.

No dedicated activity, compound or structure resource was requested; no molecular
operation, receptor/model construction or pharmacophore score was executed.
One read-only inspection initially used the wrong lower-case field spelling and
failed with `KeyError`; the corrected inspection used actual `AID`/`SIDCountAll`.
No acquisition was repeated. Truncated output was re-read in bounded windows
before making the manual decisions.

Acquisition ran on CPU19 with 100% CPU quota, 512 MiB memory, no swap, 32 tasks,
nice19, idle I/O and single backend threads. Its recorded peak was 24,969,216
bytes, with no memory-limit/OOM events. This is resource custody, not a performance
comparison. Owned capsule: `build/phmt-brd4-capacity-20261106-hvanytql`; review by
2026-11-20 or relevant change. Borrowed providers/environments remain unchanged.

Local verification uses index checks, the three reporting controls, 18 archive
controls, Ruff lint/format and whitespace checks. Archive reading verifies original
SHA-256/bytes without reexecuting science. Existing runtime scientific evidence
retains its earlier producer; these checks do not qualify a new complete source
suite, installed package, public release or supported-platform matrix.

## Next admission step

Nominate **AID1805333 / US10941160B2** for original-method acquisition: it has the
largest raw capacity among the explicitly isolated-BD1 method leads, independently
of activity categories or PHMT performance. First verify human species, complete
tagged construct, incorporated methods, peptide/reagent concentrations and endpoint
calculation, original result-table mapping, interference/counterscreens and rights.
Do not transfer the nearby patent's methods or assume experimental independence.
If it fails, record the outcome before a new dated nomination.

Only after method qualification, declare endpoint/units/censoring, class thresholds,
exposure/grouping/exclusions and deterministic cohort rules before dedicated
activity acquisition. Counts here do not prove the presence of 50 weak and 50
strong independent groups. MolSysMT owns later identity/scaffold (#447), formats,
preparation/state/H/water (#323), reusable directions (#375), geometry and transforms.
PHMT owns the pharmacophore and its declared study. Both #103 studies and #106 stay
open; actual release plan/tag/Release remains 0.4.0. No addon or publication follows.
