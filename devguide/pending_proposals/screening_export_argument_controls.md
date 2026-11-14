---
summary: Add explicit public digestion controls to cached screening table and CSV export.
issue: uibcdf/pharmacophoremt#211
status: active
opened: 2026-11-14
closed:
verification: reproduced
area: [screening, api, arguments]
guard:
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
