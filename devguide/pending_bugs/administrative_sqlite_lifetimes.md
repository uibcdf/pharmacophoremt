---
summary: Identify and close SQLite handles left open during administrative controls.
issue: uibcdf/pharmacophoremt#153
status: open
opened: 2026-11-08
closed:
severity: medium
verification: asserted
area: [testing, resources]
guard:
normative: devguide/public_prepared_runs.md
blocked_by: []
supersedes: []
---

# SQLite finalization warnings during administrative receiving

The full154case administrative suite passes under512MiB DATA, but original logs
emit ResourceWarning for unclosed sqlite3.Connection objects. Finalizer frames
include json/decoder.py and pharmacophoremt_results/_store.py:118; the creator
and whether it belongs to fixtures or a production failure path are unproven.
Retain warnings and originals rather than suppressing them or calling this fixed.

Trace a small selected control with allocation evidence, identify the actual
owned lifetime, then fix/guard explicit closure without changing caller ownership,
thread checks, saved immutability or original evidence. Never close unrelated
connections. This does not retract frozen27c1178 source receiving or establish
a molecular failure. Evidence is retained in the#148preparation capsule and
[scalar receipt](../evidence/feature_reuse_native_preparation_20261108.json).
