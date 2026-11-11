---
summary: Implement the cold read-only feature-asset view and qualify an owned wheel.
issue: uibcdf/pharmacophoremt#189
status: resolved
opened: 2026-11-11
closed: 2026-11-11
verification: measured
guard: tests/test_feature_asset_view.py
normative: devguide/feature_archive_format.md
area: [screening, interoperability, api]
blocked_by: []
supersedes: []
---

# Read-only feature-asset view

Implement the first #188 reader API with a separately versioned bounded metadata
archive. Preserve original opaque payloads, declared extraction evidence, literal
keys/global ordinals, pages and pinned lifetime. Keep payload interpretation,
quantities, molecular authentication and query admission separate. Reject raw
study stores; receive explicit unshipped export as a new archive without rewriting
original evidence. Qualify registered argument/diagnostic behavior, cold source/
owned-wheel reading, corruption/bounds/close and actual no-new-credit reading.
Public native reconstruction, writing, full delivery and provider gates remain
separate.

## Resolution — 2026-11-11 UTC

The [format contract](../feature_archive_format.md) and
[completed receipt/archive](../evidence/feature_asset_view_20261111.json) receive
the public read-only namespace, explicit unshipped export, 54 reader guards plus
44 admission regressions in source and installed contexts, 221 exact owned-wheel
payloads/166 runtime Python bodies, two cold import readers, seven actual catalog
errors, restrictive application-policy preservation, eleven exact originals and
no-new-credit retained-reference reading. Three exact guide blocks run against
the downloadable analytical example. All 26 distribution controls pass; runtime
and selected support/input inventories include the new boundary.

The source-only receipt remains unchanged. First collection/controller corrections,
the pressure-interrupted first wheel build and one same-budget resume are retained.
The original installed fence refused after live MolSysMT Python/native changes;
its old native binary is unavailable. Installed tests instead use a separately
frozen current provider context, without relabelling original saved producer
versions or claiming scientific provider requalification. Cold readers use no
scientific providers. SDK QA dependency limitations remain MolSysSuite#176-owned.

This resolves the read-only metadata/original-byte slice. Native reconstruction,
quantity/source/query admission, public writing/recovery, scale, human usability
and full exact-head/public/platform/release gates remain separate. MolSysMT#624
unreceived; QuantityRecord provisional; #148/#165 stopped.
