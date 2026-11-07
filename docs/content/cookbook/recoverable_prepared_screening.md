# Save, interrupt and resume prepared screening

This development-source recipe extends
[incremental prepared screening](prepared_incremental_screening.md) with a saved
run. It uses public PHMT/MolSysMT operations and an independent saved-result
reader. Selected source controls and one bounded owned-wheel receiving pass;
full supported installed/public qualification remains pending. Use a qualified
installation context and your own authorized,
unchanged prepared artifacts.

Supply `records` with `path`, `work_key`, `source_key` and `occurrence_key`, a
native saved `query_path`, and fresh `manifest_path`, `run_path`, `jsonl_path`
and `csv_path` destinations. Supply `compatibility` with explicit JSON values
for all six boundaries: `prepared_snapshot`, `preparation`, `features`, `index`,
`grouping` and `numerical`. `index` may be `None` when no index is used. These
are declarations from the qualified producer, not molecular authentication.
Here `records` is a re-iterable sequence of metadata: manifest creation and each
reopened molecular pass traverse it separately. A one-pass source needs its own
explicit reopen operation. An occurrence, state or conformer is not automatically
an independent compound.

The example chooses native rigid `seeded_hit` search with a finite10000-trial
budget and frame/state0. Keep query, prepared data and settings unchanged while
consuming. The application owns reader and optional attribution lifetimes.

```python
import json
from contextlib import closing
from pathlib import Path

import molsysmt as msm
from pharmacophoremt.screening import (
    PreparedInput, PreparedScreeningRun, build_prepared_run_plan,
)
from pharmacophoremt_results import ScreeningRunView


def prepared_entries(records):
    for record in records:
        yield PreparedInput(
            **{key: record[key] for key in (
                'work_key', 'source_key', 'occurrence_key',
            )},
            molecular_system=msm.h5msm.read(str(record['path'])),
        )


def plan_for(query_path, compatibility):
    return build_prepared_run_plan(
        str(query_path), screening_method='rigid', score_method='seeded_hit',
        compatibility=compatibility,
        constructor_options={'search_method': 'seeded_hit', 'max_trials': 10000},
        evaluation_options={'structure_index': 0, 'chemical_state': 0},
        on_error='record',
    )


def start_partial_run(records, query_path, compatibility, manifest_path, run_path):
    # Admit the query/settings before consuming metadata or creating the manifest.
    plan = plan_for(query_path, compatibility)
    # The producer retains the exact manifest for a later compatible restart.
    with Path(manifest_path).open('x', encoding='utf-8') as manifest:
        for record in records:
            mapping = {key: record[key] for key in (
                'work_key', 'source_key', 'occurrence_key',
            )}
            manifest.write(json.dumps(mapping, sort_keys=True, separators=(',', ':')) + '\n')
    with PreparedScreeningRun.create(
        str(run_path), plan=plan, manifest_path=str(manifest_path),
        run_id='prepared-screening:example:1',
    ) as run:
        entries = prepared_entries(records)
        with closing(entries), closing(run.resume(entries)) as outcomes:
            first = next(outcomes, None)
    # A controlled stop: any confirmed first outcome is already saved.
    with ScreeningRunView.open(str(run_path)) as view:
        return view.summary(score_method='seeded_hit@1')


def resume_and_export(
    records, query_path, compatibility, manifest_path, run_path,
    jsonl_path, csv_path,
):
    plan = plan_for(query_path, compatibility)
    newly_confirmed = 0
    with PreparedScreeningRun.open(
        str(run_path), plan=plan, manifest_path=str(manifest_path),
    ) as run:
        entries = prepared_entries(records)  # Replay the declared sequence.
        with closing(entries), closing(run.resume(entries)) as outcomes:
            for outcome in outcomes:
                newly_confirmed += 1
    # Export the authoritative complete view, including earlier confirmations.
    with ScreeningRunView.open(str(run_path)) as view:
        summary = view.summary(score_method='seeded_hit@1')
        exports = {
            'jsonl': view.to_jsonl(jsonl_path),
            'csv': view.to_csv(csv_path),
        }
    return {'newly_confirmed': newly_confirmed, 'saved': summary, 'exports': exports}
```

```python
partial = start_partial_run(
    records, query_path, compatibility, manifest_path, run_path,
)
summary = resume_and_export(
    records, query_path, compatibility, manifest_path, run_path,
    jsonl_path, csv_path,
)
```

To continue an existing run in another session, define the functions and call
only `resume_and_export` with the same compatible query, manifest, declarations
and prepared sequence. Creation and export refuse existing destinations. Each
export publishes a complete file after writing; the two exports are separate
operations. If the second fails, the first remains complete. Inspect its returned
receipt or use a fresh destination for a later export; do not resume science just
to export saved results. The database retains query bytes and attempt history.

Export needs an existing output directory and filesystem support for exclusive
hard links. Before publication, failure leaves no new destination and attempts to
remove its private staging file. After publication, a cleanup failure raises
`ScreeningRunError` with `published=True`, `receipt` and `temporary_path` in
`error.extra`; the destination is complete. Cleanup failures remain visible.
Receipts retain original configuration, actual bytes/SHA-256 and pending counts.
Use fresh export destinations rather than appending generator deliveries.

Query and setting admission precede manifest creation and metadata traversal.
A missing or invalid query leaves those destinations available for a corrected
retry. A failure after manifest writing starts can still leave a partial file;
inspect that file and use a fresh destination when needed.

For expert composition, `ScreeningRunStore` receives `plan.query_bytes`,
`plan.context` and the same ordered manifest, and `resume_prepared_run` consumes
the prepared entries. `PreparedScreeningRun` composes those public operations.
Both routes expose the same effective settings and native evidence; separate
run identifiers retain their own journal identities.

The resume iterator yields only new confirmations. A stop after commit but before
delivery can hide a result from that iterator's consumer; saved `results()` still
recovers it. Confirmed failures remain unscored and are not retried in that run.
Changed settings, queries or a deliberate failure retry require a new run identity,
optionally linked with `parent_run_id`, retaining the original evidence.

Saved inspection works independently of the main scientific package:

```bash
python -m pharmacophoremt_results RUN.sqlite3 --score-method seeded_hit@1 --limit 10
```

Exporting an existing run needs only the saved database and fresh output paths;
it does not require reopening its molecular inputs or resuming science:

```python
from pharmacophoremt_results import ScreeningRunView

with ScreeningRunView.open(run_path) as view:
    native_receipt = view.to_jsonl(jsonl_path)
    table_receipt = view.to_csv(csv_path)
```

The companion requires the declared ArgDigest/SMonitor support dependencies,
without loading molecular/numerical or attribution providers. It reads stored
evidence and creates no new scientific credit. The command emits scalar observed
results; full `results()` and `query_bytes` can contain geometry and remain under
the caller's storage/export authority. Legacy experimental runs require explicit
`allow_legacy=True` in the reader or `--allow-legacy` in the command; public
resume never implicitly migrates them.

Observed rankings cover scored work only, with manifest-order ties. Valid negative
scores are zero; terminal failures are `None`, exported as JSON null/empty CSV
cells. Work completion can include failures. Native search budgets and coverage
remain inspectable; geometric evidence does not establish biological activity.

Reexecution checks exact saved query/settings and conservative software identity.
Relocation of identical code/data is separate from a code change. A refused
software binding does not imply changed chemistry. Reading preserves original
versions and does not require original producer versions or molecular files.
Managed collections, scientific cross-version compatibility and platform/power-loss
durability retain their separate qualification.
