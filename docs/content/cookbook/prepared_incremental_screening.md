# Screen prepared inputs incrementally

Use `PreparedInput` and `screen_prepared` to evaluate prepared inputs one at a
time, retain their source correspondence and export every outcome. They are
development-source public APIs; verify that the selected package and provider
context include them. This recipe alone does not establish installed/public or
platform qualification.

`screen_prepared` yields outcomes in input order, including valid nonmatches and
unscored native failures. `VirtualScreening.run` continues to provide its existing
globally ranked hit list and complete facade caches. The iterator retains no
molecular handles in its outcomes and does not accumulate a result collection.

## Provide prepared files and a saved query

The example accepts four application-provided values:

- `query_path`: an authorized saved native pharmacophore JSON file.
- `records`: an iterable of declarations for authorized prepared H5MSM files.
- `jsonl_path` and `csv_path`: fresh output paths in an existing owned directory.

Each record supplies these fields. They are application metadata, rather than a
new PharmacophoreMT manifest format:

| Field | Meaning |
| --- | --- |
| `path` | Prepared H5MSM file readable through public MolSysMT operations. |
| `work_key` | Producer-declared unique evaluation identity; also the native pose ID. |
| `source_key` | Original source record identity; may repeat across declared work. |
| `occurrence_key` | Source occurrence identity; may relate several work items. |

Keys are nonempty strings. Declare work-key uniqueness and retain the original
mapping/order; the iterator does not build a collection-sized uniqueness set or
infer molecular equivalence. Repeated source IDs and molecular objects do not
become independent compounds or assay samples automatically.

The chosen query must have at least three non-collinear essential centers for
the explicit `seeded_hit` search below. Every file is evaluated at frame0 and
chemical state0. Other stored frames/states remain outside this declared task;
there is no preparation, hydrogen addition or conformer generation.

## Load, screen and export through public operations

Run these blocks in order after providing the four values above. The function
opens one prepared molecular input when it is requested, and closes its own
entry generator, outcome generator and output files explicitly.

```python
import csv
import json
from contextlib import closing
from pathlib import Path

import molsysmt as msm
from pharmacophoremt.io import load_json
from pharmacophoremt.screening import PreparedInput, RigidPoseSearch, screen_prepared


def prepared_entries(records):
    for record in records:
        yield PreparedInput(
            work_key=record['work_key'],
            source_key=record['source_key'],
            occurrence_key=record['occurrence_key'],
            molecular_system=msm.h5msm.read(str(record['path'])),
        )


def export_prepared_files(records, query_path, jsonl_path, csv_path):
    query = load_json(str(query_path))
    evaluator = RigidPoseSearch(
        query, search_method='seeded_hit', max_trials=10000,
    )
    entries = prepared_entries(records)
    counts = {'outcomes': 0, 'matched': 0, 'not_matched': 0, 'failed': 0}
    fields = [
        'work_key', 'source_key', 'occurrence_key',
        'status', 'ranking_score', 'score_method',
    ]
    with closing(entries), closing(screen_prepared(
        entries, evaluator, score_method='seeded_hit', on_error='record',
        evaluation_options={'structure_index': 0, 'chemical_state': 0},
    )) as outcomes:
        with Path(jsonl_path).open('x', encoding='utf-8') as native_output, \
             Path(csv_path).open('x', encoding='utf-8', newline='') as table:
            writer = csv.DictWriter(table, fieldnames=fields)
            writer.writeheader()
            for outcome in outcomes:
                native_output.write(json.dumps(outcome, allow_nan=False) + '\n')
                status = outcome['native_result']['status']
                writer.writerow({
                    'work_key': outcome['work_key'],
                    'source_key': outcome['source_key'],
                    'occurrence_key': outcome['occurrence_key'],
                    'status': status,
                    'ranking_score': outcome['ranking_score'],
                    'score_method': outcome['score_method'],
                })
                counts['outcomes'] += 1
                counts[status] += 1
    return counts
```

```python
summary = export_prepared_files(records, query_path, jsonl_path, csv_path)
```

Fresh-file mode refuses existing destinations. JSONL preserves the complete
native evidence, including assignments, search budgets, units, failures and
producer attribution when captured. CSV is a scalar view in the same encounter
order. Neither file is a transactional run journal or a public resume protocol;
a reader/export/programming error propagates and can leave partial output.

## Interpret the outcomes

Each yielded dictionary has six fields: `work_key`, `source_key`,
`occurrence_key`, `native_result`, `ranking_score` and `score_method`. The native
result retains its own versioned evidence and completion semantics. This Python
envelope does not introduce a separate versioned persistent-file contract.

With the explicit seed-only method, a verified fitted hit has score1 and a
completed valid nonmatch has score0. A recorded native evaluation failure has
score `None`: JSONL writes `null`, while this CSV export leaves the score cell
empty. Inspect `status` and the full native cause; an empty score is not zero.
The recorded criterion is `seeded_hit@1`. Geometric scores do not establish
activity, affinity, molecular independence or exhaustive continuous-pose search.

Only native `PoseEvaluationError` failures are recordable. Missing/invalid input
files, reader failures, malformed mappings and programming errors propagate;
they are not converted to negative scores. Already exported outcomes remain
caller-owned evidence. The returned counts concern work items from this supplied
iterator, not complete chemical-space or assay coverage.

`PoseEvaluator` and `ConformerScreening` can also be supplied to `screen_prepared`.
Choose a compatible native score criterion and one common options mapping for the
run. Native option admission is checked before requesting the source iterator;
molecular selection validity still requires actual input access. The factory
copies options, and the prepared inputs, query and evaluator settings must stay
unchanged during consumption. Per-input option changes are a separate task.

## Own the readers and attribution lifetime

The application owns its readers. Closing the outcome generator stops further
pulls and releases its held references; it does not explicitly close a supplied
source. The example closes both generators because it creates them. If `records`
is itself a resource-owning reader, manage that reader's lifetime at the outer
application boundary too. A retained result contains no molecule, but one native
evaluation and caller accumulation still have their own memory cost.

For requested attribution, keep the application's Ackredit session and
`pharmacophoremt.attribution()` context active while consuming outcomes, for
example around the call to `export_prepared_files`. Native evaluations then
capture the operations actually reached. Creating an unconsumed iterator does
not earn calculation credit. Exporting or reading saved evidence does not rerun
the original molecular calculation; see the [attribution recipe](attribution.md).

The unshipped recovery/inspection experiments retain their separate contracts.
This public iterator does not download a library, authenticate a prepared
snapshot, group chemical identities, rank the whole collection or guarantee
durable publication. Molecular formats, preparation and collection ownership
remain with supported MolSysMT operations.
