---
summary: Name skip_digestion in shared boolean-control refusals.
issue: uibcdf/pharmacophoremt#212
status: resolved
opened: 2026-11-14
closed: 2026-11-14
severity: low
verification: measured
area: [arguments, diagnostics]
guard: tests/test_screening_export_controls.py::test_skip_control_error_names_the_supplied_argument
normative: devguide/screening_export_argument_controls.md
blocked_by: []
supersedes: []
---

# Correct the shared skip-control argument label

At b60573d, `digest_skip_digestion(None)` raises the host ArgumentError naming
`essential`. The cached-curation registry also aliases the skip control directly
to `digest_essential`. A new diagnostic control reproduces the wrong message.
This is PHMT-owned validation, not a defect in the ArgDigest provider.

The [contract](../screening_export_argument_controls.md) preserves Python/NumPy
boolean acceptance, canonical bool return and the essential argument's existing
diagnostic. Change only the supplied argument's label and the cached alias.
Receive the shared and public cached/export refusals, literal-True behavior and
existing argument/scientific controls before closing this bounded defect.

## Resolution — 2026-11-14

[Receiving](../evidence/screening_export_controls_20261114.json) qualifies exact
source 9fe608a and its private wheel in the bounded scope: 370 selected cases
per source/owned context, 41 minimum-Pandas controls, strict owned docs and
243 verified payloads/188 equal Python bodies. Actual SDK support verifies and
retires. The declared guard protects the supplied skip label, the independent essential label and the public cached-curation alias.
Broader #6 and full source/installed/public gates remain separate. Original
red outputs and controlled provider/native limitations are retained.
