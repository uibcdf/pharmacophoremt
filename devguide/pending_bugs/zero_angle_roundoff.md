---
summary: Zero-angle direction checks rejected their own source because normalization roundoff became a real angle.
issue: uibcdf/pharmacophoremt#16
status: active
opened: 2026-10-02
closed:
severity: medium
verification: measured
area: [screening, geometry]
guard: tests/test_rigid_search.py::test_zero_angle_tolerance_matches_its_source_and_preserves_rigid_invariance
normative:
blocked_by: []
supersedes: []
---

# Zero-angle comparison roundoff

## Observed mechanism

An indexed donor-H vector with three nonzero components was normalized several
times across construction/validation/extraction. Its dot product with the query
direction could be slightly below one. Applying arccos produced a nonzero angle
and rejected the original reference at zero degrees. A rigid transform of the
same input could pass, violating the intended physical invariance.

The analytical fixture uses H=[0.07, 0.56, 0.04] nm and donor=[0, 0.5, 0] nm.
Before correction, direct source evaluation returned not_matched, while rigid
search after a shared proper motion returned matched.

## Local correction and evidence

PoseEvaluator compares direction cosines to the cosine of the requested angular
tolerance, allowing eight float64 epsilons for numerical normalization roundoff.
The result declares this dimensionless comparison slack. The same rule covers
unoriented aromatic normals. This corrects finite-precision evaluation of the
existing criterion rather than changing its physical angle definition.

The guard checks that the original and fitted rigidly transformed source both
match at unit coverage with zero degrees. Real-provider scientific controls also
retain donor/angular and orthogonal aromatic negatives. The change remains local
and uncommitted; keep the report active for review with the rigid-search slice.
On 2026-10-02 the full local suite passed 98 tests, including the new zero-angle
guard and existing directional/aromatic negative controls, with the published
provider source pins declared in `../rigid_search_workflow.md`.
