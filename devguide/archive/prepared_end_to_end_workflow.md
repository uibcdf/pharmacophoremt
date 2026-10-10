---
summary: Qualify construction, curation, persistence and placed screening on a public prepared CCD control.
issue: uibcdf/pharmacophoremt#49
status: resolved
opened: 2026-10-10
closed: 2026-10-10
verification: measured
area: [modeling, screening, validation, io]
guard: tests/test_prepared_workflow.py
normative: devguide/prepared_end_to_end_workflow.md
blocked_by: []
supersedes: []
---

# Prepared end-to-end pharmacophore workflow

## What

Review one complete native chain from a selected prepared feature inventory to
declared cached hypotheses, saved models and a ranked placed-input batch.
The owning issue is #49; collection maintenance follows #20.

## How

Reuse the frozen public CCD EST SDF and existing MolSysMT fixture client.
Select hydrophobic/aromatic families explicitly, construct with
`from_feature_inventory`, reorder with `extract_pharmacophore` and declare
essential flags, weights and radii with `edit_pharmacophore`. Save/read JSON,
YAML and versioned pharmacophore SDF under different unit contexts, then invoke
`VirtualScreening(screening_method='placed')`. A fresh reader preserves detached
evidence without calculating new molecular features or registering new credits.

## Why

Separate tool tests do not qualify their composed behavior. Independent controls
must preserve site/source mappings, invalidated scores, optional weighted support,
obligatory constraints, exclusion vetoes, ordered ties, valid negatives and failed
inputs through persistence.

## What is measured and what is assumed

The declared original contains nine hydrophobic participants and one aromatic
ring. A fixed 0.05 nm translation lies outside 0.02 nm hydrophobic/narrow-ring
radii and inside the alternative 0.10 nm ring radius. The ring contributes
3/(3+9) coverage; a 2 nm translation is a valid zero-coverage negative. A zero-weight
optional exclusion at the frozen atom-zero coordinate vetoes exact self placement.
An unprepared input must retain failure and no fit score. These expectations are
analytical and are not activity labels.

## Alternatives and refuted paths

No private pilot inputs, unpublished scientific hypotheses or reference answers
are copied. A target discovery program requires its own readiness and evidence.
No new molecular geometry/preparation or collection codec is implemented here.
MolSysMT #375 is not required by the selected feature families; #323 remains a
separate environmental-refinement requirement.

## Scope and exclusions

CCD ideal geometry is a prepared workflow control, not an observed binding pose,
activity validation, docking result, qualified conformer ensemble or performance
benchmark. Hosted/installed/public acceptance remains #23. Maintainers LMMV/dprada
own the case and review changed preparations, tolerances and expected outcomes.

## Acceptance criteria

The focused independent guards, executable recipe and full dated driver output
must agree; retain immutable inputs, encoded artifacts, original result history,
actual attribution, provider/source hashes and fresh-reader evidence. Verify
archive integrity separately from scientific reexecution and preserve prior
archives byte-for-byte.

## Measured completion — 2026-10-10

The prepared chain passes all declared variant/codec expectations and gives
identical scientific fields with host tracking disabled/enabled. Fifteen focused
controls pass in 26.20 s, including two existing default all-feature preparation
cases; the shared projection's existing tracking-equivalence guard separately
passes in 11.57 s. Both executable cookbook blocks pass. Initial test-expectation
errors are retained in the original archive and corrected with the delivered
history operation names and an explicit 1e-12 geometry tolerance; no runtime
scientific repair was needed.

The [original summary](../evidence/prepared_workflow_py314_summary.json) retains
Python/provider/native extension identities, complete input/preparation/curation
and evaluation records, original encoded artifacts, executed source overlay,
fresh-process reader evidence, initial test output and 28 unchanged prior archives.
The later completion receipt records final documentation/governance checks.
Only developer fixture orchestration, shared scientific-output projection and
tests/guidance changed. Molecular reading/recognition/translations remain public
MolSysMT operations. No provider or runtime molecular routine is added.

This closes the bounded analytical workflow case. Biological validation, other
methods, MolSysMT #375/#323 and required hosted/public delivery gates keep their
independent ownership and remain outside this closure.
