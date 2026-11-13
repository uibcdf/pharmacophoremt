---
summary: Complete cached inspection and comparison argument contracts.
issue: uibcdf/pharmacophoremt#204
status: active
opened: 2026-11-12
closed:
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
