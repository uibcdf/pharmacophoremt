---
summary: Diagnose the exact upper-bound analytical comparison failure on macOS.
issue: uibcdf/pharmacophoremt#143
status: active
opened: 2026-11-07
closed:
severity: medium
verification: reproduced
area: [comparison, geometry, ci]
guard: tests/test_rdkit_bounds_comparison.py::test_declared_geometry_and_boundary_expectations
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
