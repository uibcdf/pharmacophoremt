---
summary: Repair ranking metrics and retain explicit retrospective input accounting.
issue: uibcdf/pharmacophoremt#12
status: resolved
opened: 2026-10-02
closed: 2026-10-07
severity: high
verification: measured
area: [validation, screening]
guard: tests/test_validation_metrics.py
normative: docs/content/cookbook/retrospective_validation.md
blocked_by: []
supersedes: []
---

# Ranking metrics and retrospective accounting

## What

A perfectly ordered balanced ranking returned AUC 0.5 and BEDROC approximately
0.00338 instead of 1. Retrospective validation associated results by object
identity, conflated skipped/failed calculations with negative scores and counted
hits using a threshold unrelated to the configured essential-site requirement.

## How

The local implementation uses pairwise ranking probability with half credit for
ties, normalized exponential rank sums for BEDROC, and fractional credit for
EF boundary ties. Tests compare untied rankings with RDKit's independent metric
implementation and test analytical tied rankings and parameter boundaries.

Batch records retain input indices, including repeated objects. Explicitly
recorded failures have no score and are excluded from metrics with original and
evaluated class counts retained. The default failure policy raises. The native
placed-pose evaluator supplies accepted-pose status; the legacy route retains
its own essential-weight threshold, evaluated over available conformers.

## What is measured and what is assumed

Local guards pass for analytical rankings, repeated inputs, generators,
single-class datasets and failed inputs. This verifies ranking/accounting, not
legacy feature chemistry, docking affinity or prospective screening accuracy.

## Scope and acceptance

The metric guard above and `tests/test_retrospective.py` protect the defects.
The implementation is under local review; no commit or hosted CI result is
claimed. Keep this report active until the reviewed change is accepted, then
archive it with the owning issue. See `../placed_pose_workflow.md` for the
bounded scoring semantics and dependency limits.

## Reviewed closure — 2026-10-07

The earlier local-review status above is historical. The implementation was
published in `fdb57dcbe8e4d9d8364d1dcf5199a7945bfd9a2f` and remains unchanged
in the reviewed source `a74a8ea83af343b12306aa964a07212822c41507`. This closure
adds scientific guards and retained review evidence, without another metric
implementation or changes to MolSysMT.

The original reported perfect ranking now gives AUC/BEDROC 1; the alternating
ranking gives AUC 0.75; reversed ranking gives AUC/BEDROC 0. The metric guard
compares all 20 five-input rankings with 1, 2 or 4 actives against public RDKit
AUC/BEDROC/EF, using three BEDROC alphas. A three-way boundary tie checks the
mean of independent reference tie resolutions and every input permutation.
Invalid shapes, nonfinite labels/scores and invalid alpha/fraction values retain
structured argument diagnostics. Single-class NaN behavior remains explicitly
different from the reference library's convention.

`tests/test_retrospective.py` guards both-class failures, repeated/generator
inputs, original versus evaluated denominators, a real valid zero-score negative,
failure records with no scores, default raising and empty/all-failed refusal.
A real placed pose with full positive coverage but an exclusion veto counts
as no accepted active. The actual legacy conversion route also preserves two
repeated inputs and excludes a conversion failure; its threshold adapter guard
retains the configured essential-match policy. This tests bounded accounting,
not general legacy feature chemistry or conformer preparation.

The combined metric, retrospective and placed-pose selection passes **62 tests
in 13.65 s**, without warnings, on normal editable Python 3.14.7. The retrospective
cookbook Python block executes successfully. The [review receipt](../evidence/ranking_retrospective_review_py314.json)
retains source/guard/reference checksums, actual original counterexample results,
commands and verification limits. Ruff, generated report indexes and the three
standard-library reporting guards pass.

The guards protect the reported normalization, tie and input-accounting
mechanisms. Public metric signatures and the retrospective failure-policy
contract are preserved. Required hosted CI and public installed qualification
remain separate; this closure does not establish affinity, biological enrichment
or ERα environmental H refinement, which remains provider #323 and local #22.
