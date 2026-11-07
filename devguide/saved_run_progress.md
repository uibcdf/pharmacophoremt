# Saved-run progress without a ranking criterion

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108), mature-0.x milestone2.
This contract and its [prospective plan](evidence/saved_run_progress_plan_20261107.json)
precede implementation/receiving. The
[source receipt](evidence/saved_run_progress_source_20261107.json) passes102
distinct selected cases. The [sealed receiving receipt](evidence/saved_run_progress_20261107_summary.json)
also receives the same57 library bodies and16 documented commands from one
exact owned installed wheel outside the checkout.

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

Frozen producer: `1950421b94ae9933a2790aa18a56f619034f6d51`.
The one wheel is `pharmacophoremt-0.4.0+144.g1950421-py3-none-any.whl`,4515659
bytes, SHA-256 `f473a3503f13d9f26fcce5da86dbdd6e9dc8730e28b2bad8c95785086d6cd97d`.
All209 non-RECORD payload files match their installed bytes;154 nongenerated
runtime files match the source. The shared editable metadata/cache remains at
its earlier134 identity; provider prefixes, pins and molecular native code are
unchanged. No wheel is rebuilt or published during receiving.

The source-free receiving starts with `-I -S -B` and only the owned installed
file, original authenticated public ArgDigest0.17.1/SMonitor0.22.1/DepDigest0.11
payloads and standard-library roots. All57 library bodies pass with no skips or
unexpected failures. The51 fresh children have no forbidden scientific,
attribution or development-support import. Expected error-path commands retain
their nonzero statuses; they are not successful science. The synthetic legacy
fixture uses the installed standard-library storage core, not a checkout shim.

The four actual documented commands execute on each of four original source/
installed-complete, source-partial and explicit legacy databases. All16 succeed.
Progress matches both API output and independently read original SQLite work,
status and attempt counts. Existing ranks, full native JSONL, CSV scalar fields,
configuration and file hashes also agree. Original database bytes remain
unchanged. The partial run retains one zero confirmation and two pending items;
the three complete originals each retain three outcomes. This is saved evidence
receiving, without new molecular preparation, scoring or attribution.

Original controls, child outputs, guard snapshots, databases and full native
receipts remain in ignored `build/phmt-saved-progress-20261107-7m2ihh2r` and owned
`/tmp/phmt-saved-progress-20261107-f0rwxode`. Published archive content is limited
to owned control/code text and scalar/hash receipts; native/query/database bodies
and third-party payloads stay local. Owners review retained resources by2026-11-20.
Execution is serial on CPU19, one backend thread, nice19/idle I/O, with entry
pressure checks. Source/receiving use per-process512MiB address-space limits;
build uses a512MiB data limit to permit Git mappings. No own systemd runtime
exists, so aggregate memory, no-swap, task or CPU-quota limits are not enforced.

The [later native observation](evidence/accumulated_ci_observation_20261107_progress.json)
has five science jobs successful, two executing and one queued. The live
accumulated source CI42399097757/attempt1 belongs to frozen4616c78;
it cannot qualify this later runtime increment. Follow its existing handles
without duplicate dispatch. New exact-head debt remains #9-owned; full
source/dependency/installed/public/platform/release and mature-0.x gates retain
their separate requirements. No milestone is completed by this small increment.
