---
summary: Implement the cold read-only feature-asset view and qualify an owned wheel.
issue: uibcdf/pharmacophoremt#189
status: active
opened: 2026-11-11
verification: asserted
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

## Source checkpoint

The public source reader and explicit unshipped study export now pass98selected
source controls; see the [format](../feature_archive_format.md) and
[source receipt](../evidence/feature_asset_view_source_20261111.json). The next
gate is an exact owned wheel and installed/cold/no-new-credit receiving.
