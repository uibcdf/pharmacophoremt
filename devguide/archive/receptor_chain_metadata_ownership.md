---
summary: Delegate deposited receptor chain metadata inspection to public MolSysMT getters.
issue: uibcdf/pharmacophoremt#104
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: medium
verification: measured
area: [architecture, integration, tests]
guard: tests/test_eralpha_receptor.py::test_author_chain_inspection_is_delegated_to_public_molsysmt
normative: devguide/receptor_preparation_admission_audit.md
blocked_by: []
supersedes: []
---

# Receptor chain metadata ownership

## Resolution

The fixed-source helper now requests chain_id/chain_name through public MolSysMT get and assembles only its existing case-report mapping. It no longer converts to Pdbx DataContainer or traverses atom_site/getObj/getValue/getRowCount. The real deposited-file getter preserves labels A–I and author names A/B/C repeated three times, including D/auth A.

The guard fails on the original helper, verifies actual public getter use after the change and preserves the full scientific projection. The first changed selection has eight passes/one test-layout NameError; two pre-existing assertions had accidentally moved into the new test. They are restored to their original test without changing scientific expectations. Final **nine controls pass**. Consumer inputs and physical source/native identity remain stable; inherited distribution-metadata changes are retained separately.

[Audit and limits](../receptor_preparation_admission_audit.md), [original receipt](../evidence/receptor_admission_audit_20261106_summary.json). The private stager declaration already includes the helper, but initially refuses its stale source digest. Only the reviewed helper pin is updated; both selected inventory/staging controls then pass. All58 other support inputs remain byte-identical. The complete mapping is independently retained in both verified historical receptor reports. No provider implementation, detector, molecular preparation, scientific input, historical output or public runtime API changes.

## What, how and why

The historical audit decoded mmCIF through the provider, then interpreted label/auth chain fields locally. The user's molecular-ownership rule includes every representation and format, including unshipped scientific helpers. A measured public getter route already exists, so the consumer should compose it rather than retain direct format traversal. This case is separate from #74's frozen SDF migration and does not qualify every other helper or source form.

## Acceptance

Use the provider's public chain metadata, preserve source scientific results and custody, forbid the reported direct-traversal mechanism, and retain existing frame/unit/blocked-calculation/source-index controls. New formats/chemistry remain provider-owned; installed/public/platform gates stay independent.
