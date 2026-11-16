---
summary: Preserve inclusive clique distance boundaries across equivalent length units.
issue: uibcdf/pharmacophoremt#237
status: resolved
opened: 2026-11-15
closed: 2026-11-15
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

## Resolution — 2026-11-15

[Receiving](../evidence/clique_argument_controls_20261115.json) receives source
3a405bdc4dda69cbc5f233d55be5e1959a25a5ef and exact private wheel `0.6.0+38.g3a405bd`:
identical serial **191/25/189/99-case source/owned groups**, **504 distinct cases
per context including 115 admission and 76 numerical boundary controls**, zero
failures/errors/skips. All 246 payloads/191 source-equal nongenerated Python bodies
verify; all four groups load 173 target-only PHMT modules. Actual immutable SDK
staging has pre-work journals/checking and import/resource/both-link retirement.
Strict owned HTML docs, 27 current distribution controls and reporting/archive/
index/generated-environment/declared-route/Ruff checks pass (559 formatted files).
The accepted focused source group keeps its original label without reexecution.
Package footprint/provider requirements remain unchanged.

The direct guard retains all 74 original numerical assertions and appends two
positive margin controls. Nominal inclusive boundaries pass under both input/
application units at three scales; 32-epsilon negatives and tiny-distance
negatives remain rejected. The independent original clique oracle also passes.
No provider defect or general comparison-policy qualification is asserted.
