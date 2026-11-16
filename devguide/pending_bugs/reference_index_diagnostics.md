---
summary: Attribute invalid reference_index values to reference_index while preserving structure_index admission.
issue: uibcdf/pharmacophoremt#235
status: active
opened: 2026-11-15
closed:
severity: medium
verification: asserted
area: [arguments, diagnostics, modeling]
guard: tests/test_reference_index_diagnostics.py
normative: devguide/aligned_model_argument_controls.md
blocked_by: []
supersedes: []
---

# Reference-index diagnostic ownership

The first #234 implemented guard has 93 passes and six failures: invalid
reference_index values (-1, True, 0.5) under both controls correctly refuse but
name structure_index. The shared reference digester delegates directly to the
structure digester's hard-coded error. This is PHMT ownership, not a provider bug.

Reuse the nonnegative-integer predicate with an explicit owning name, preserving
both digesters' value domains, Python-int normalization and ArgumentError family.
Keep the unchanged public guards and direct invalid/valid Python/NumPy controls,
including large unsigned normalization. Source-frame/alignment consumers and
source/exact-owned receiving retain scientific behavior. Preserve original red
guards and the model increment's partial #6/full qualification boundaries.
