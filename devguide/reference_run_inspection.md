# Read-only inspection of reference screening runs

The later [public prepared-run implementation](public_prepared_runs.md) is now
received in its declared source/owned installed contexts. Its independent reader uses
ArgDigest/SMonitor without molecular/numerical/citation imports. Explicit legacy
reading is separate from the new public writer; this page preserves the original
reference-format command, qualification and historical source identities.

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108).
This extends the unshipped [recovery experiment](prepared_library_recovery.md)
without freezing a runtime API or changing ledger schema/version, preparation,
scoring or recovery compatibility.

## Development command and composition

```bash
python phmt_test_support/reference_run_store.py RUN.sqlite3 \
  --score-method seeded_hit@1 --limit 10
```

The standard-library command emits work/attempt counts and at most ten scored
records: source/occurrence/work keys, manifest ordinal, saved criterion, score
and native status. It emits no query or molecular geometry. The criterion must
agree with saved execution and every committed outcome. Bad limits and missing,
incompatible or corrupt ledgers fail without partial result output; no database
is created, resumed or recalculated.

```python
from phmt_test_support.reference_run_store import ReferenceRunView

with ReferenceRunView.open("RUN.sqlite3") as view:
    progress = view.summary(score_method="seeded_hit@1")
    observed = view.top_results(score_method="seeded_hit@1", limit=10)
    producer = view.configuration
    for outcome in view.results():
        consume(outcome)  # Full original evidence, including terminal failures.
```

Returned dictionaries are detached; `configuration`, `query_bytes` and outcomes
retain original producer context. Reading needs no external manifest/query file,
current molecular providers or citation service. It executes no stored code and
recomputes neither scores nor attribution. Reexecution retains its separate
compatibility/input checks. Full native/query evidence can contain geometry;
the caller owns authorized storage/export. The command projects scalar fields.

## Ownership and integrity

`open` uses SQLite `mode=ro`, `query_only=ON` and a read transaction, reusing the
existing schema, configuration, checksum, mapping and full record/attempt checks.
It verifies data outside the requested ranking and unpublished attempts too;
matching hashes do not establish authenticity. It uses no `immutable` shortcut.
Close the exclusive writer before opening a view, and close the view before
resuming the writer. Contention fails immediately without retries.

The read transaction retains one view until closure. This is not a live progress
monitor, multiwriter protocol, power-loss guarantee or platform qualification.
Tested normal inspection preserves database bytes and creates no sidecars;
missing files remain missing. Invalid evidence is refused rather than repaired
or partially ranked.

## Counts and ranking

Counts refer to declared **work items**, not independent compounds or assays.
Confirmed outcomes partition into matched, not matched and failed work. Valid
zero-score nonmatches are scored; terminal failures remain unscored. Unpublished
attempts, including staged complete payloads, leave their work pending. Attempt
counts remain separate because one work item can have older attempts.

`manifest_work_complete` means every declared work item has a confirmed terminal
outcome. It can be true with failures or zero declared work. It establishes no
conformer/chemical/biological completion. Native coverage retains its own meaning;
the reader infers no assay labels, equivalence or aggregation.

Ranking orders scores descending, then original manifest ordinal ascending,
independently of publication order. Selected negatives must not be called hits.
Scope is always `observed_scored_work_only`; failed/pending work cannot be assumed
to rank below observations. Mixed criteria are refused even with zero limit.

Opening verifies the whole ledger; summary/ranking scan committed outcomes.
Selection retains at most K payloads plus the current record, independently of
collection length. Individual payloads, SQLite cache and caller accumulation
have separate costs. This is a structural bound, not an index, constant-time
progress call, throughput measurement or global top-K proof.

## Evidence and maintenance

The [prospective plan](evidence/reference_run_inspection_plan_20261107.json)
fixes guards and historical PubChem3D expectations before execution. The
[receipt](evidence/reference_run_inspection_20261107_summary.json) preserves exact
source overlays, resource limits, original logs and unchanged historical
database/directory identities. New analytical checks and reading the same three
old outcomes are separate observations; no molecule is downloaded or screened.
The guard is
[`test_reference_run_inspection.py`](../devtools/tests/test_reference_run_inspection.py).

Automatic review rejected suite-status fetch/prune. Explicit offline
`--no-fetch` status preserves provider refs/worktree; connected read-only GitHub
observation records remote state separately. The cached 32-behind count is not
asserted for the newer remote head. MolSysMT is not updated; its collection
contract remains [#624](https://github.com/uibcdf/molsysmt/issues/624).

New behavior needs separate evidence; full source/installed/public/platform
gates remain under #9/#23. The [PubChem3D case](pubchem3d_receiving_pilot.md) and
its original failures/quantity correction retain their identities and limits.
