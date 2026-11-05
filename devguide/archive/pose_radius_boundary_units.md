---
summary: Preserve inclusive positive-site radius decisions across application units.
issue: uibcdf/pharmacophoremt#84
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: medium
verification: measured
area: [screening]
guard: tests/test_receptor_sensitivity.py
normative: devguide/receptor_sensitivity_protocol.md
blocked_by: []
supersedes: []
---

# Placed-pose radius boundary and unit roundoff

## What, how and why

The prespecified #83 matrix reveals two exact-boundary physical placements
which match under nm but fail under pm. At center .625 nm, candidate .5 nm and
radius .125 nm, ordinary conversion yields .49999999999999994 and
.12499999999999999 nm; the strict raw comparison refuses the resulting residual.
The .75/.5/.25 nm cell similarly flips. Identical physical choices should retain
their inclusive pharmacophoric interpretation within bounded float64 roundoff.

## Ownership and correction

This is PHMT's matching decision, not evidence of a defective molecular or unit
provider. Compare the excess distance to eight float64 epsilons times the site
radius/Point tolerance. Use a difference test without expanding the radius,
preserving refusal of nonfinite distances at extreme finite radii. Record
`position_comparison_relative_slack` in criteria. This is a fixed numerical
allowance, not another physical tolerance or calibrated biological parameter.

Assignment, weights, essentiality, score, molecular geometry and the method ID
remain unchanged. Strict steric-interior and angular comparison semantics remain.
No local molecular/quantity engine, source/prefix/dependency change or alteration
of the prespecified expected transitions is used.

## Evidence and acceptance

Corrected guards on the original runtime have three failures/32 passes. Of the
initial 23 failures, 21 were wrong new serialized-field expectations and two
exposed the boundary defect; correcting the fields also lets the cross-policy
guard reach that same defect. These are not three separate production bugs. The final
scope passes 245 selected cases, including 49 new guards and independently
resolved just-inside/equal/just-outside Point/Sphere controls. All 92 declared
attempts remain, including two failed/unscored frames. Source/input custody,
application policy, original #83 declaration, curation history and actual
attribution are preserved. Exact output/source and every failure are in the
[receipt/full evidence](../evidence/receptor_sensitivity_20261104_summary.json).

The allowance handles the measured conversion-scale residual; it does not
certify arbitrary ill-conditioned/huge-coordinate geometry or every matcher.
Biological sensitivity, provider chemistry and installed/public/hosted
qualification remain independent. No physical preference is inferred.
