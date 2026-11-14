---
summary: Name skip_digestion in shared boolean-control refusals.
issue: uibcdf/pharmacophoremt#212
status: active
opened: 2026-11-14
closed:
severity: low
verification: reproduced
area: [arguments, diagnostics]
guard:
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
