---
summary: Validate the screening facade run control while preserving native admission timing.
issue: uibcdf/pharmacophoremt#213
status: active
opened: 2026-11-14
closed:
verification: reproduced
area: [screening, api, arguments]
guard:
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
