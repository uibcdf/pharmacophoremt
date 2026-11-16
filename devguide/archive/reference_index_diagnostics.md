---
summary: Attribute invalid reference_index values to reference_index while preserving structure_index admission.
issue: uibcdf/pharmacophoremt#235
status: resolved
opened: 2026-11-15
closed: 2026-11-15
severity: medium
verification: measured
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

## Resolution — 2026-11-15

[Receiving](../evidence/aligned_model_argument_controls_20261115.json) receives
source 48696d68cc9447f4f478f679d7e3a4bb14a4e749 and exact private wheel `0.6.0+36.g48696d6`:
identical serial **99/189/47/89-case source/owned groups**, **424 distinct cases per
context including 99 model and 18 direct diagnostic controls**, zero failures/
errors/skips. All 246 payloads/191 source-equal nongenerated Python bodies verify;
the respective groups load 173/173/171/173 target-only PHMT modules
(173 in their union). Actual SDK staging has pre-work journals/checking and
import/resource/both-link retirement. Strict owned HTML docs, 27 current
distribution controls and reporting/archive/index/generated-environment/declared-
route/Ruff checks pass (557 formatted files). The accepted focused source run
keeps its original label without another execution. Package footprint remains
equal to #233's corrected declaration; all earlier source/metadata identities stay.

The public guard preserves closed/local admission and reference-anchored model
semantics, real source/quantity/provenance custody and independent children.
Direct index guards preserve both value domains and Python-int normalization,
including large unsigned values, while distinguishing reference/structure labels.
Original red assertions are unchanged and pass after the owning shared-validator
repair. Existing frame/alignment consumers pass. #6 and full supported/public gates
stay partial; prior source/wheel/metadata/recovery ownership remains unchanged.
