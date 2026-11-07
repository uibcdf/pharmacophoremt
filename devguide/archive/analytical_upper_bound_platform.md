---
summary: Diagnose the exact upper-bound analytical comparison failure on macOS.
issue: uibcdf/pharmacophoremt#143
status: resolved
opened: 2026-11-07
closed: 2026-11-07
severity: medium
verification: reproduced
area: [comparison, geometry, ci]
guard: tests/test_rdkit_bounds_comparison.py
normative: devguide/rdkit_bounds_comparison.md
blocked_by: []
supersedes: []
---

# Exact upper-bound comparison across platforms

Frozen489be12 source CI42416657424/attempt1 reports2338pass/1fail on macOS3.13
and3.14, in exact_upper_bound. Three Linux cells pass at initial observation;
remaining cells are not yet accepted. Preserve original run/job/log/source and
case identities. #9 comment6713743759 records the initial failure observation.

The decimal0.3/0.4nm reference scaled to0.44999999999999996/0.6000000000000001nm
and0.125nm tolerance may not define the exact same native floating endpoint on
all backends. This is a hypothesis, not an established provider defect. Identify
which expectation and numeric operands differ before changing input or code.
A new exactly representable fixture would be a separately declared input with an
independent oracle; historical receipts are never rewritten. Preserve strict
RDKit/inclusive native definitions, all assignments and meaningful negatives;
no threshold relaxation, hidden epsilon, skipped test or output normalization.

Next: receive terminal native evidence, inspect the own comparison/fixture and
native distance predicate, declare a focused diagnostic before execution. Later
hosted acceptance of a corrected producer remains separate from local tests.


## Local diagnosis and correction, 2026-11-07

The original upper/lower binary64 inputs exceed the stated0.25nm endpoint by
approximately3.33066907387547e-17/5.55111512312578e-18nm under an independent
100-digit scalar calculation. That establishes a fixture exactness defect;
precise macOS numerical operands were not emitted by the old harness. Do not
promote this observation into an upstream numerical bug.

The two prospective exact-rational guards fail on the unchanged fixture. Only
the two boundary records now use exact3/4/5nm geometry and1.25nm tolerance, with
half/one-and-a-half scaling. Eight interior records and production code are
unchanged. All14focused guards and the ten-case/186-assignment complete driver
pass; original native2/1and RDKit0/0boundary mapping counts remain. The
[receipt](../evidence/rdkit_boundary_correction_20261107_summary.json) preserves
old/new inputs, resource limits and failures. Corrected hosted acceptance is
pending before closing this cross-platform issue. #9/#23 retain broader gates.


## Hosted resolution received, 2026-11-07

Frozen8db2a53f91a3686088874f965d389e636003d990 source42421360591/attempt1 passes
2357tests in every Linuxx86_64/macOSarm64 Python3.11–3.14 cell, with no reported
skips/failures. Actual full commands/interpreter/architecture/acquisition/job/step
and XML identities are in the [terminal receipt](../evidence/boundary_ci_terminal_20261107.json).
Policy42421364958/publication governance42421369303 pass independently. Corrected
XML retains105unique qualified paths in all eight cells; native Linux3.13 uploads
pass, without a public-server freshness claim.

The module guard includes exact Fraction endpoint checks and the ten actual
comparison controls. Both rational checks fail on the original binary inputs;
the revised controls preserve native inclusive/RDKit strict definitions and
interior inputs. All four formerly failing macOS cells now execute the corrected
source successfully. Original489be12/source42416657424 failure and original
fixtures/receipts remain unchanged. No matching threshold, provider, public
artifact, biological or performance result is silently substituted.

This closes#143's declared cross-platform fixture defect. Later profiling/recovery
helpers and tests have their own local evidence; they are not relabeled as part
of frozen8db2a53. Current-head#9, installed/public/platform#23 and mature0.x gates
remain separate.
