---
summary: Identify and close SQLite handles left open during administrative controls.
issue: uibcdf/pharmacophoremt#153
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: measured
area: [testing, resources]
guard: devtools/tests/test_reference_run_store.py::TestReferenceRunStore::test_corruption_fixtures_close_every_owned_sqlite_connection
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

## Allocation receiving and correction

Tracemalloc on the five original corruption controls identifies all 15 SQLite
warnings at their five direct fixture connections. The SQLite transaction
context commits/rolls back but does not close a connection. Wrap those same
transactions in standard contextlib.closing, preserving every original fixture
body, corruption and assertion. Production writer/reader code is unchanged.

The new durable guard runs all five actual fixture bodies with observed real
SQLite connections and asserts explicit closure of every owned handle; it
fails before the correction and cleans its own handles even after failure.
The same five allocation controls then pass without warnings, both complete
store/inspection modules pass 42 cases, and the complete administrative suite
passes 156 cases with ResourceWarning explicitly enabled and no unclosed-database
warning. All use the unchanged 512MiB DATA budget. The
[receipt](../evidence/administrative_sqlite_lifetimes_20261108.json) retains original
allocations/failure, source hashes and resource scope; none is molecular timing.
