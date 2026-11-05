---
summary: Compose optional native receptor exclusions into bounded generated hypotheses.
issue: uibcdf/pharmacophoremt#88
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: measured
area: [modeling, screening]
guard: tests/test_receptor_generation_exclusions.py
normative: devguide/receptor_generation_exclusions.md
blocked_by: []
supersedes: []
---

# Generated receptor exclusions

Extend #87 with optional paired cached heavy-atom inventory and explicit radius.
Reuse #32/#44's validation/construction through shared private PHMT composition
helpers, keeping molecular operations in MolSysMT. Each generated model receives
independent zero-weight exclusions and real local/global source correspondence.
Context equality checks declarations, not molecular-source authenticity or
complete coverage. Uniform radii are query choices, not physical atomic radii.

Acceptance includes empty/budget/malformed/context cases, blocked molecular
access, source/metadata independence, native recovery, actual attribution,
strict-boundary placed controls and unchanged prepared PHE404 clash oracles
under two unit policies. No hypothesis pruning, new geometry engine, provider
or dependency change. Current implementation is pending executed qualification.

## Resolution — 2026-11-05

217 selected controls pass (61 new). The guard protects paired/context/empty/invalid
inputs, independent ownership, unchanged enumeration/weights, optional attribution,
native recovery and strict-boundary/prepared clash oracles under two unit policies.
Five recipe blocks and a captured prepared replay execute. Exact identities, full
results and the quota-aborted attempt are retained in
[the receipt/full evidence](../evidence/receptor_generation_exclusions_20261105_summary.json).
The final stable run is source-only qualification; provider/delivery/biological
gates retain their separate scope. Molecular work remains MolSysMT-owned.
