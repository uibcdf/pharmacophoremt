---
summary: Complete cached inspection and comparison argument contracts.
issue: uibcdf/pharmacophoremt#204
status: resolved
opened: 2026-11-12
closed: 2026-11-13
verification: measured
area: [api, modeling]
guard: tests/test_cached_inspection_controls.py
normative: devguide/cached_inspection_argument_controls.md
blocked_by: []
supersedes: []
---

# Cached inspection and comparison contracts

The [owning contract](../cached_inspection_argument_controls.md) completes three
missing explicit controls and defining contracts at 878864e. Native model,
threshold and required-center guards remain active under bypass. Empty tables
gain their fixed columns; nonempty object-cell identity stays unchanged.

The original probe rejects all six explicit False/True calls with TypeError,
accepts negative/NaN/infinite/bool tolerances as ordinary scores and observes an
empty table with no columns. All 57 original new guards fail before
implementation. The separately discovered ordered-similarity limitation is #205;
its numerical loop is preserved and its scope made explicit here.

Acceptance: the declared independent geometry/table/legacy-score/refusal guards,
nm/pm public recipes, existing regressions and source/exact-owned/public-provider
receiving with complete failed-attempt and resource evidence. Broader #6 and all
full supported source/installed/public/scientific gates remain separate.

Source receiving passes234 selected cases (65new), six guide blocks and13
quality operations. See [source evidence](../evidence/cached_inspection_controls_source_20261112.json).
The exact-owned artifact and actual public-provider receiving follow freeze.

## Executed resolution — 2026-11-13 local date

[Combined receiving](../evidence/cached_inspection_controls_20261112.json)
passes234 selected source/owned cases each (65new), 65 actual public-ArgDigest
cases per context, public PUW0.28.1/Pytest Receptor1.2.2 and18 guide blocks.
All240 payloads/185 runtime bodies and167 target-only observed modules verify
with actual SDK support staging and the unchanged f44e41b source/tests. No
installed correction/overlay/provider/native-data workaround is required.

The guard protects explicit controls, native threshold/model/geometry refusals,
empty-table schema, source custody, object ownership and original greedy results.
Original57 red failures/probe remain measured. This closes#204; #205 stays open
for the unimplemented symmetric method, and broader#6/full qualification remain
separately owned.
