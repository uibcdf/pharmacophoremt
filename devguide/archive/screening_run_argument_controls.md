---
summary: Validate the screening facade run control while preserving native admission timing.
issue: uibcdf/pharmacophoremt#213
status: resolved
opened: 2026-11-14
closed: 2026-11-14
verification: measured
area: [screening, api, arguments]
guard: tests/test_screening_run_controls.py
normative: devguide/screening_run_argument_controls.md
blocked_by: []
supersedes: []
---

# Screening-run facade admission

The [owning contract](../screening_run_argument_controls.md) retains the legacy
signature, cache reset/materialization/native delegation and independent child
checks. Add the missing public ArgDigest plan and actual facade-owned boolean
control. Invalid control values become explicit pre-entry refusals; existing
native failures retain their post-entry cache semantics. Receive source/exact
owned controls before closing. Broader #6 remains partial.

## Resolution — 2026-11-14

[Receiving](../evidence/screening_run_controls_20261114.json) receives 3050a78
and its exact owned wheel: the same 230 selected cases per source/owned context,
including 52 new controls, 244 payloads/189 source-equal bodies, actual SDK support
staging/retirement and strict owned docs. The module guard protects real literal-
True/NumPy behavior, legacy positional calls, pre-entry refusal custody, borrowed
input materialization, opaque/literal keyword identity, native post-reset refusals,
empty cohorts and unsuccessful publication under independent child admission.
The original signature/run body remain AST-equal. Original baseline 19 failures/
33 preservation passes and controlled provider/native limits stay recorded.
Broader #6 and full source/installed/public acceptance remain separate.
