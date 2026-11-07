# Saved-run progress without a ranking criterion

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108), mature-0.x milestone2.
This contract and its [prospective plan](evidence/saved_run_progress_plan_20261107.json)
precede implementation/receiving. The
[source receipt](evidence/saved_run_progress_source_20261107.json) now passes102
distinct selected cases; exact owned installed receiving remains pending.

## Public task and ownership

A user should be able to ask how much saved work is confirmed or pending without
knowing the producer's ranking criterion. Add `ScreeningRunView.progress()` and
`ScreeningRunStore.progress()`, and expose the same read-only operation through:

```bash
python -m pharmacophoremt_results RUN.sqlite3 --summary
```

The methods share the existing storage inspection scan. Return detached
`run_id`, `parent_run_id`, `counts`, `attempts` and `manifest_work_complete`.
Counts retain declared, committed, scored, matched, not-matched, failed and
pending work. Attempts retain started, staged and committed counts. Staged
unpublished work remains pending; repeated attempts are not additional work.
Completion includes confirmed failures and describes declared work items, not
independent molecules, chemical coverage or biological validity. Empty declared
work is complete with zero counts.

Progress does not choose, combine or rank score values. It reports neither
`score_method` nor `ranking_scope`, and does not include native records, query
geometry or complete producer context. Existing criterion-specific `summary`
and `top_results` contracts remain unchanged, including disagreement rejection.
Explicitly admitted historical mixed-criterion evidence can be counted without
manufacturing a common scientific score. Public-format storage verification and
binary-score admission remain unchanged.

The CLI summary flag is mutually exclusive with both export flags and refuses
explicit `--score-method`/`--limit` before opening a database. Default ranked
inspection still requires a criterion; existing command responses are preserved.
Success prints one JSON document and exits0. Handled failures exit2 with empty
stdout. Missing/corrupt/closed readers fail visibly, without rewriting files.
Legacy reading still requires `--allow-legacy` and performs no migration.

The view owns its verified read snapshot; the store uses its existing owned
connection between writes. Opening still verifies every saved attempt/outcome,
including unpublished evidence, and progress scans confirmed evidence. This is
not constant-time polling, live inspection of a concurrently owned writer,
an index, throughput evidence or a durability improvement.

PHMT owns screening-result interpretation and presentation. Reuse the private
storage scan and definition-owned ArgDigest/SMonitor contracts; introduce no
molecular, quantity, attribution, acquisition or optional-engine operation.
`PreparedScreeningRun.summary()` already derives its own plan's criterion and
retains its existing behavior. No provider change or new dependency is needed.

## Receiving and remaining gates

Source receiving passes9 new progress controls and all48 existing
reader/export/CLI cases through published Pytest Receptor1.2.0. All24 affected
distribution,3 reporting and18 archive cases pass, as do full Ruff lint/format,
declared dependency routes, indexes and whitespace checks. No provider or
scientific implementation changes. Public methods use ArgDigest's existing
definition-owned standard contracts and SMonitor catalog orchestration.

Execute the prospective controls against source and one exact owned installed
wheel outside the checkout. Preserve original attempts, complete local receipts,
actual resource limits and original saved-file identities. Publish only owned
control text and scalar/hash evidence; full native/query/database bodies and
third-party support payloads remain local.

The live accumulated source CI42399097757/attempt1 belongs to frozen4616c78;
it cannot qualify this later runtime increment. Follow its existing handles
without duplicate dispatch. New exact-head debt remains #9-owned; full
source/dependency/installed/public/platform/release and mature-0.x gates retain
their separate requirements. No milestone is completed by this small increment.
