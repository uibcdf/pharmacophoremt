---
summary: Define and qualify native feature payload production and archive assembly.
issue: uibcdf/pharmacophoremt#195
status: open
opened: 2026-11-11
closed:
verification: asserted
area: [api, persistence, screening]
guard:
normative: devguide/public_feature_archive_store.md
blocked_by: []
supersedes: []
---

# Public native feature payloads

After #193's compatibility decoder and #194's first whole-generation writer,
choose an explicitly versioned native payload and public producer for already
captured native inventories. Review current model/IO contracts first; keep
test-support classes, molecular preparation and source authentication outside
this runtime boundary. MolSysMT#624 owns collection/source mapping authority.

Require the effective evaluated-family request, including evaluated-empty
families. Present features cannot establish what was evaluated. Preserve full
native geometry, participant/geometry maps, frame/state, recognition and original
extraction references/producer versions. New serialization observations must stay
separate; no new extraction credit follows from encoding existing features.

Use public PyUnitWizard records and explicit field/unit/dimension validation.
Define compatibility/profile admission, resources, malformed inputs, diagnostics
and original source/ordinal lineage before integrating arbitrary/subset assembly
with the existing expected-current publication/recovery tools. Keep metadata cold.

Acceptance requires the reviewed contract, native round-trip equality under
nondefault policies, empty/incomplete/unobserved coverage and wrong-unit/map
guards, real diagnostics/attribution and source/exact-owned executable examples.
No producer or new stable payload is implemented by this report. Supported/public/
platform, biological/human/scale gates and stopped #148/#165 remain separate.
