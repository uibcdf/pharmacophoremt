---
summary: Preserve inclusive clique distance boundaries across equivalent length units.
issue: uibcdf/pharmacophoremt#237
status: active
opened: 2026-11-15
closed:
severity: medium
verification: measured
area: [modeling, consensus, geometry, units]
guard: tests/test_clique_distance_boundary.py
normative: devguide/clique_argument_controls.md
blocked_by: []
supersedes: []
---

# Inclusive clique distance boundary

The first #236 control implementation preserves the original scientific body
but exposes two genuine pm-boundary failures: nominally 0.125 nm / 125 pm
coordinates/tolerance can round to different sides of a raw float inequality.
The independent subset oracle expects the inclusive three-member clique; the
raw comparison splits it into two maximal pairs. This is a PHMT comparison
policy issue, not a provider defect.

Retain the original 115-case control baseline/guard and 109-pass/six-failure
implemented run. Four failures are separate authored assertions that omitted
SMonitor's extra source links; their correction checks all five owned diagnostic
fields without prohibiting those links. The other two require a numerical fix,
not a changed clique expectation.

Specify inclusive distance comparison with a relative roundoff allowance of
eight machine epsilons times the declared length threshold, zero absolute
allowance. Direct nominal boundaries under nm/pm input and application policies,
multiple scales and meaningful beyond-roundoff negatives protect the fix.
Preserve default/bypassed admission, maximality, occurrence ordering, budgets,
other methods and original failures. Broader comparison-policy consistency is
not qualified here; #143's historical RDKit fixture issue retains its different
inputs, source and resolution.
