---
summary: Add explicit public digestion controls to cached screening table and CSV export.
issue: uibcdf/pharmacophoremt#211
status: resolved
opened: 2026-11-14
closed: 2026-11-14
verification: measured
area: [screening, api, arguments]
guard: tests/test_screening_export_controls.py
normative: devguide/screening_export_argument_controls.md
blocked_by: []
supersedes: []
---

# Cached screening export controls

The [owning contract](../screening_export_argument_controls.md) defines two
bounded public boundaries under #6. Preserve Pandas destination/I/O ownership,
cached hit fields and existing subclass delegation. The 0.6.0 source lacks these
explicit controls. Source receiving precedes a committed exact owned wheel;
the broader public-adoption and full supported/public gates remain separate.

The independent host diagnostic #212 corrects the shared skip validator's
argument label while preserving boolean normalization and essential semantics.

## Resolution — 2026-11-14

[Receiving](../evidence/screening_export_controls_20261114.json) qualifies exact
source 9fe608a and its private wheel in the bounded scope: 370 selected cases
per source/owned context, 41 minimum-Pandas controls, strict owned docs and
243 verified payloads/188 equal Python bodies. Actual SDK support verifies and
retires. The declared guard protects public contracts, real bypass, destination identity, subclass delegation, cache/file custody and original exceptions.
Broader #6 and full source/installed/public gates remain separate. Original
red outputs and controlled provider/native limitations are retained.
