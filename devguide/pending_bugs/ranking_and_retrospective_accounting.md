---
summary: Repair ranking metrics and retain explicit retrospective input accounting.
issue: uibcdf/pharmacophoremt#12
status: active
opened: 2026-10-02
closed:
severity: high
verification: measured
area: [validation, screening]
guard: tests/test_validation_metrics.py
normative:
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
