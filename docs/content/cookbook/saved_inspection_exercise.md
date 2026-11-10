# Practice saved-run inspection

Use this small exercise to learn saved-source discovery, status selection and
original result inspection. It creates synthetic records through the public
writer: **no molecules are screened and no scientific result is validated**.
It uses development features received in the saved-reader workflow; the released
0.4.0 package does not gain them automatically. Start with the
[installation context](../about/installation.md) and
[saved-work guide](saved_work_inspection.md).

## Create a practice file

Download the {download}`setup script <../../_static/examples/saved_inspection_exercise.py>`.
Run it with the same Python environment as the reader, choosing a new directory:

```bash
python saved_inspection_exercise.py exercise
```

It writes `exercise/run.sqlite3`, the original `work.jsonl` manifest and a short
README. An existing directory is refused without replacement. If setup fails
partway, retain the files for inspection and choose a new directory after fixing
the cause. The script performs no download, molecular import or calculation.
For a source checkout, the script is also at
`docs/_static/examples/saved_inspection_exercise.py`.

## Try the tasks first

Use the saved file read-only. Record where you looked, help you needed, errors
and how you recovered. If comparing two interfaces, use the same file and
alternate which route participants try first; prior practice affects the result.

1. Find every original source label and the number of declared work entries.
   Explain whether a repeated label means an independent compound.
2. Choose the first source. Find all its pending work, show only its first row
   and retain the original global manifest ordinal. Explain why the full count
   may differ from the displayed row count.
3. Find the failed work for that source and inspect its full original detail.
   Preserve its literal work key, including spaces and Unicode.
4. Distinguish a staged, unpublished result from work that never started. State
   whether either is confirmed and whether inspection retries it.
5. Find the confirmed zero-score nonmatch and explain how it differs from a
   failed calculation or pending work.
6. Select an absent source and explain the empty result without treating it as
   an unreadable run.
7. Try the failed work key after trimming its outer spaces. Record the refusal,
   then recover by using the original key. Confirm that inspection changed no
   saved result.

A facilitator can use the separate
[answer sheet and observation template](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/saved_inspection_usability.md).
Technical dry-runs prepare this exercise; they do not establish that real users
can complete it unaided. Human observations remain separate evidence.

## CLI assistance

Consult `python -m pharmacophoremt_results --help`. These commands support the
same tasks; each command opens its own verified snapshot. For a changing real
run, restart status paging after a writer publishes more results.

```bash
python -m pharmacophoremt_results exercise/run.sqlite3 --summary
python -m pharmacophoremt_results exercise/run.sqlite3 --sources
python -m pharmacophoremt_results exercise/run.sqlite3 --work-items --source-key=' --source α ' --status pending --limit 1
python -m pharmacophoremt_results exercise/run.sqlite3 --work-items --source-key=' --source α ' --status failed
python -m pharmacophoremt_results exercise/run.sqlite3 --work-key=' --failed key α '
python -m pharmacophoremt_results exercise/run.sqlite3 --work-key='staged α'
python -m pharmacophoremt_results exercise/run.sqlite3 --work-key='never α'
python -m pharmacophoremt_results exercise/run.sqlite3 --work-key='negative zero'
python -m pharmacophoremt_results exercise/run.sqlite3 --work-items --source-key='absent'
```

Use `=` and shell quoting to preserve a value with a leading dash or spaces.
The following command deliberately uses the wrong, trimmed work key and exits
with an error. It prints no success JSON. Recover with the exact-key command
above; do not recreate or resume the run.

```bash
python -m pharmacophoremt_results exercise/run.sqlite3 --work-key='--failed key α'
```

## Expert API assistance

This complete example reads the same small exercise in one caller-owned snapshot.
It deliberately collects this fixture's short inventory; adapt retention for
larger inputs using the [bounded recipe](saved_work_inspection.md#discover-a-source-and-inspect-its-work-in-one-snapshot).
Only the run path needs changing if you used another setup directory.

```python
import json
from contextlib import closing

from pharmacophoremt_results import ScreeningRunError, ScreeningRunView

run_path = "exercise/run.sqlite3"

with ScreeningRunView.open(run_path) as view:
    progress = view.progress()
    with closing(view.source_items()) as inventory:
        sources = list(inventory)
    source_key = sources[0]["source_key"]
    with closing(view.work_items(source_key=source_key, status="pending")) as work:
        pending = list(work)
    with closing(view.work_items(source_key=source_key, status="failed")) as work:
        failed = list(work)
    failed_key = failed[0]["work_key"]
    failed_detail = view.work_item(failed_key)
    pending_details = [view.work_item(row["work_key"]) for row in pending]
    zero_detail = view.work_item("negative zero")
    with closing(view.work_items(source_key="absent")) as work:
        empty_selection = list(work)
    try:
        view.work_item(failed_key.strip())
    except ScreeningRunError as error:
        refusal_code = error.code
    recovered_detail = view.work_item(failed_key)

print(
    json.dumps(
        {
            "counts": progress["counts"],
            "sources": sources,
            "pending_count": len(pending),
            "pending_prefix": pending[:1],
            "failed": failed_detail,
            "pending_details": pending_details,
            "zero_nonmatch": zero_detail,
            "empty_selection": empty_selection,
            "trimmed_key_refusal": refusal_code,
            "recovered": recovered_detail,
        },
        ensure_ascii=False,
        indent=2,
        allow_nan=False,
    )
)
```

The detached details remain readable after the view closes. A staged payload is
not a confirmed outcome: both staged and never-started work remain pending,
while their retained attempt counts differ. A confirmed failure remains a
failure. Reading preserves the original synthetic producer rather than crediting
another calculation. Opening still verifies the complete saved file; a short
output alone is no indexed or large-library performance guarantee.
