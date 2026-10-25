---
summary: Qualify a fresh ERα binding endpoint and cohort before new scoring.
issue: uibcdf/pharmacophoremt#66
status: partial
opened: 2026-10-24
closed:
verification: inspected
area: [validation, screening, mvp]
guard: devtools/tests/test_esr1_binding_readiness.py::TestEsr1BindingReadiness::test_exclusions_cover_entire_read_source_and_failed_requested_inputs
normative: devguide/esr1_binding_evaluation_plan.md
blocked_by: [uibcdf/molsysmt#447]
supersedes: []
---

# Fresh ERα binding evaluation readiness

## What and why

The #62/#64 observations are exposed development evidence. #65 now supplies
reusable native saved-result accounting; a stronger biological challenge needs
new suitable data, a declared endpoint and traceable molecular independence.
The [protocol](../esr1_binding_evaluation_plan.md) fixes those decisions before
new individual activity or structure acquisition. It keeps both #64 queries,
binary native scoring, original denominators and failures unchanged.

## Inspected source evidence

Nine original metadata responses are retained in the task-owned
`/tmp/phmt66-binding-metadata-20261024/`, with exact identities/URLs in
`tests/data/esr1_binding_evaluation/source_inventory.json`. Public projections
and checksums do not claim full raw redistribution. Source-specific terms remain
explicit in the protocol. Keep this root while source qualification needs it;
owners LMMV/dprada, review 2026-11-07. No environment is created or removed.

The bounded PubChem review rejects AID625258 as a primary human binding cohort:
homologous target assignment, no explicitly inactive CIDs and overlapping
aggregate categories (835 total, 20 active, 818 unspecified). Never manufacture
inactives from unspecified or total-minus-active. AID2051711 has only one
unspecified CID. AID1223 has 17 active / 46 inactive CIDs, but is permeabilized-cell
competition following primary-hit selection, so it remains a secondary-format
candidate rather than an automatic isolated-protein replacement.

ChEMBL_37 discovery metadata spans all 1,485 returned human CHEMBL206/B/9 assay
records in two pages. This does not mean all were manually qualified. The flags
are insufficient: CHEMBL1954678 describes coactivator recruitment. Nominated
CHEMBL3382763 and CHEMBL3705057 require document/endpoint and activity-schema review
under the fixed rules. No candidate has yet qualified as a fresh cohort.

## Exclusion and molecular boundary

The case reader collects all 8,099 valid CIDs in the complete previously read
Tox21 table, not merely scored molecules or active labels. All 4,402 Bath CIDs
and prior #62/#64 requested inputs, including unavailable structures, are inside
that universe. Another 149 source rows have no CID; their row indices/SIDs remain
unresolved historical identities, not fabricated extra compounds. This is literal ID
accounting, with no chemistry, scaffold or normalization routine.

MolSysMT #447 remains open and owns exact identity/scaffold annotation. New
ChEMBL identifiers cannot be asserted disjoint by comparing their strings with
CIDs. #219/#366/#375 remain provider-owned; new coordinate/state/direction work
is not implemented here. Dataset/source review can continue while those provider
contracts are pending; stronger independence/scoring readiness cannot be claimed.

## Implementation and next stage

`phmt_test_support/esr1_binding_readiness.py` verifies frozen metadata hashes,
pagination and original source identities, then produces a metadata/exclusion
review only. It has no activity/structure acquisition or molecular calculation
route. These are case-specific source/sampling decisions, not a new public
scientific API or general provider workaround. No new optional engine/attribution
boundary is introduced. Existing transport/archive and later score/metric tools
are reused rather than copied into the library.

The offline guard protects the full historical exclusion universe and all prior
requested inputs, including failures and inconclusive outcomes. Clean-head
metadata/exclusion evidence and local qualification are still pending.

The initial complete administrative run passes 51 tests plus 26 subtests in the
canonical Python 3.14.7 workspace, including strict Sphinx and the new source-ID
guard. Three reporting tests, generated indexes, Ruff and whitespace checks pass.
Clean-head metadata/exclusion evidence remains pending; no scientific runtime
module changes, installed-package proof or new full matrix is inferred.

Next review the two source documents and then acquire their individual activity
tables under this committed protocol, retaining all quality/threshold/duplicate
decisions. Fix the exact cohort only after endpoint, source rights and provider
identity/scaffold gates pass; prepare molecular inputs only through MolSysMT.
No new cohort, molecular input or score is currently acquired. No predictive
validity, complete new CI matrix, installed package or public release is claimed.

## Acceptance

Retained source identities and measured metadata triage; a committed pre-data
protocol; complete conservative historical exclusions; original/derived data
rights and producer identities; explicit endpoint/classification/provider/cohort
readiness gates. Actual cohort acquisition and scoring remain separate later
stages, with full native #65 accounting and no missing-input replacement.
