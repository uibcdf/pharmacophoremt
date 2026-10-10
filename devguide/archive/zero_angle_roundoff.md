---
summary: Zero-angle direction checks rejected their own source because normalization roundoff became a real angle.
issue: uibcdf/pharmacophoremt#16
status: resolved
opened: 2026-10-02
closed: 2026-10-10
severity: medium
verification: measured
area: [screening, geometry]
guard: tests/test_rigid_search.py::test_zero_angle_tolerance_matches_its_source_and_preserves_rigid_invariance
normative: devguide/rigid_search_workflow.md
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


## Reviewed resolution — 2026-10-10

The correction is already committed in the current source. Review confirms that
placed matching uses cosine thresholds with a declared eight-float64-epsilon
allowance for both directed donors and unoriented aromatic normals; it does not
replace the caller's physical angular tolerance. The existing durable guard still
checks original/source rigid-motion invariance and unit coverage at zero degrees
through real MolSysMT recognition, fitting and transforms.

`tests/test_pose_evaluation.py::test_zero_angle_roundoff_does_not_hide_a_resolvable_tilt`
adds independent donor/planar-aromatic controls in nm/radian and angstrom/degree
contexts: aligned vectors match; a 0.0001-degree tilt fails at zero degrees and
passes at an explicit 0.0002-degree tolerance; a reversed donor fails while a
reversed aromatic normal matches. Matching, weighted coverage and missing mandatory
sites are asserted; source coordinates remain unchanged. Existing rigid/search
and placed negatives are retained. This bounds the numerical correction without
claiming exact-arithmetic discrimination below the declared float64 slack.

Original commands/output, JUnit and before/after producer/input/binary identities
are linked in the [closure review](../evidence/diagnostic_angle_closure_review_py314_summary.json).
The new test is a query criterion control, not a new molecular geometry engine.
Runtime PHMT and sibling sources are unchanged by this review. The historical
uncommitted/98-test checkpoint above retains its original date and provider scope;
this fresh resolved review supersedes its status, not its original run identity.
Molecular donor/local acceptor geometry migration (#41 / MolSysMT #375),
environmental H refinement (#323), full-matrix/public qualification and biological
validation remain separate work.
