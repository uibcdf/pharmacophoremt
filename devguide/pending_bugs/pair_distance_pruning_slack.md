---
summary: Qualify triplet pair-distance pruning against accepted positional roundoff slack.
issue: uibcdf/pharmacophoremt#160
status: partial
opened: 2026-11-09
closed:
severity: medium
verification: measured
area: [science, screening, numerics]
guard: tests/test_pair_distance_pruning.py::test_original_binary_boundary_retains_a_public_proposal
normative: devguide/pair_distance_pruning.md
blocked_by: []
supersedes: []
---

# Candidate pruning and final numerical acceptance

Source review under#128 observes that `PoseEvaluator` permits eight float64
epsilons relative to each positive-site radius, while `get_correspondences`
compares internal pair-distance differences with the strict sum of the two
physical radii. A candidate condition described as necessary should cover the
final predicate's accepted numerical region as well as its physical tolerance.

At parent af110fd2c54df4076903e883e97e50a3d3c26e7c, inspect
`screening/pose_evaluation.py`'s positional predicate and
`screening/correspondence.py`'s pair filter. The prospective arithmetic case uses
exact binary nm values: r=1/8, delta=2^-52, q0=(0,0,0), q1=(1,0,0),
q2=(0,1,0), c0=(-r-delta,0,0), c1=(1+r+delta,0,0), c2=q2. Both displaced
sites reach the accepted numerical boundary, while the first pair exceeds2r.
Declare nominal-boundary and beyond-slack controls before checking this witness.

This is initially a source-derived suspected defect, not an executed public
native search. `checked_pose_coverage` also tests the original placement;
`seeded_hit` does not. Keep those routes and finite-method completeness limits
distinct. Molecular transforms/preparation stay MolSysMT-owned.

Investigate a conservative numerical policy for the PHMT-owned candidate filter
without changing physical radii, units, assignment, scoring or failure meanings.
Other pruning families need their own review. Closure requires an independent
guard against the actual owned operation and safely qualified public/native
source/installed receiving. Do not raise budgets or retry exhausted#148 profiles
for this issue. No implementation or broader scientific qualification is claimed.

## Arithmetic receiving — 2026-11-09

The [declared witness](../evidence/pruning_slack_arithmetic_20261109.json) now
passes all three stdlib controls with independent Fraction checks. At the accepted
boundary all three site predicates pass, while the pair difference is
`0x1.0000000000008p-2` versus a strict limit `0x1.0000000000000p-2`.
The nominal-radius control survives; the beyond-allowance control is rejected by
the site predicate. No PHMT/MolSysMT/NumPy/competitor import or fitting occurs.

This measures the literal predicate discrepancy only. Actual public/native
method reproduction, an implemented correction, a regression guard and same-file
installed receiving remain pending. Keep this issue open; the separate
[Pharmer study](../pharmer_query_pruning_review.md) is source-only evidence.

## Source correction receiving — 2026-11-09

The [owning numerical contract](../pair_distance_pruning.md) and
[source receipt](../evidence/pruning_slack_source_20261109.json) record the
conservative candidate band, independent public guard,116passing selected cases
and twelve unchanged ordinary outputs. The exact public ion body reaches final
acceptance with the original module and then fails candidate admission; the same
body passes with the correction. Final evaluation and physical tolerances remain
unchanged. Earlier AS512 mapping failures and the explicit local DATA512/AS1GiB/
observed-group-RSS512 amendment retain separate identities. This is not a kernel
MemoryMax qualification or#148retry. Same-file owned installed receiving remains
pending, so the issue is partial and open.
