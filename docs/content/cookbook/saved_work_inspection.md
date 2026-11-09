# Inspect saved screening work

Start with `python -m pharmacophoremt_results RUN.sqlite3 --summary` to see the
saved counts. Then select work by status or source and inspect a literal work key using
the commands below. Each command opens its own verified snapshot.

## Inspect a selected prefix in one Python snapshot

Use the public view when the counts, selected entries and details must describe
the same saved state. Set the four input parameters, then run this complete
example:

```python
from contextlib import closing
from itertools import islice

from pharmacophoremt_results import ScreeningRunView

run_path = "RUN.sqlite3"
status = "failed"
limit = 10
allow_legacy = False

with ScreeningRunView.open(run_path, allow_legacy=allow_legacy) as view:
    configuration = view.configuration
    progress = view.progress()
    print("Run:", configuration["run_id"])
    print("Declared work:", progress["counts"]["declared_work"])
    print("Selected work:", progress["counts"][status + "_work"])
    with closing(view.work_items(status=status)) as work:
        for mapping in islice(work, limit):
            detail = view.work_item(mapping["work_key"])
            print(
                mapping["manifest_ordinal"],
                repr(mapping["work_key"]),
                detail["status"],
                detail["attempts"],
            )
```

Choose `failed`, `pending`, `matched` or `not_matched`, and a positive page
limit. `Selected work` counts all entries with that status in the snapshot;
the loop displays at most `limit` of them, retaining their original ordinals.
Keys pass directly to `work_item()`; spaces, Unicode and leading dashes retain
their literal meaning. `repr()` keeps whitespace visible in the display.
An empty selection prints the three summary lines and no detail rows.

The nested context closes the work iterator even when only a prefix is consumed;
the outer context closes the view. The last `detail` value, when there was a
selected entry, remains detached after closure. Its `outcome` contains the full
original confirmed evidence or `None` while pending. The display above prints
only mapping/status/attempt information. Staged and never-started entries both
remain pending; a confirmed failure stays a failure. Reading these records
does not retry work or establish that a worker is running.

Set `allow_legacy = True` only when deliberately reading a legacy reference file.
Close this view before reopening a writer. After more work is published, open a
fresh view and start selection again. The limit bounds displayed entries; opening
still verifies the entire file, status selection can scan outcomes and each
confirmed detail can contain a large original payload.

## Find failed or pending work

Select the saved status directly when you need to locate entries:

```bash
python -m pharmacophoremt_results RUN.sqlite3 --work-items --status failed
python -m pharmacophoremt_results RUN.sqlite3 --work-items --status pending --limit 10 --offset 0
```

You can also select `matched` or `not_matched`. Each record retains its original
manifest ordinal and work/source/occurrence keys; it contains no native geometry
or draft. Staged and never-started work both remain pending. Use an exact key
from the selected page for the detail command below.

Filtered responses use `pharmacophoremt.screening-work-selection@1`. `status`
states the exact filter, `declared_work` counts all declared entries and
`selected_work` counts those matching that status in the same verified snapshot.
`offset` and `next_offset` address the **selected** stream; record ordinals remain
global. Use `next_offset` for another page; `null` means no later selected work.
The default page limit is ten; offsets beyond the selected count return no rows.

Each command opens its own read-only snapshot. After resuming a writer, start
selection again at offset0: confirmed/pending membership may have changed.
These offsets are not durable cursors across new confirmations. In Python, keep
one caller-owned view open and iterate `view.work_items(status="failed")` or
`view.work_items(status="pending")` for its fixed snapshot. The default
`view.work_items()` and command without either selection retain all original mappings
and their ordinary page response.

The status filter applies only to `--work-items`; it does not choose a ranking
criterion or assign activity labels. Counts describe work, not independent
compounds. Complete opening/count work and confirmed filtering can scan saved
outcomes; pagination alone does not establish indexed or large-library speed.

## Find all work for one original source

Copy an exact `source_key` from a saved work page. A source may have several
occurrences, conformers or work items; all remain separate and keep their global
manifest ordinals. Select the source alone, or combine it with a status:

```bash
python -m pharmacophoremt_results RUN.sqlite3 --work-items --source-key=SOURCE_KEY
python -m pharmacophoremt_results RUN.sqlite3 --work-items --source-key=SOURCE_KEY --status failed --limit 10 --offset 0
```

Replace `SOURCE_KEY` with the original literal value. Use shell quoting for spaces
or shell characters, and attach a leading dash value with `=`, for example
`--source-key='--source α'`. Empty/whitespace-only keys are invalid. Other
whitespace, case, Unicode and punctuation are preserved. An unknown source
returns an empty selection. This is identity selection; it infers no compound,
PubChem CID alias or chemical grouping.

Source-selected responses use `pharmacophoremt.screening-work-selection@2`.
They include the exact `source_key`, `status` (or `null` when unrestricted),
global `declared_work`, and `selected_work` for their intersection. Offsets address
that selected stream; records keep their original four mapping fields. Status-only
commands retain work-selection@1 and unfiltered commands retain work-page@1.

In Python, keep a caller-owned view open and consume
`view.work_items(source_key=source_key, status="failed")`, closing a partly consumed
iterator as shown above. Omit `status` to include every work state for the source;
`source_key=None` leaves source unrestricted. To inspect original confirmed
evidence, pass a selected mapping's `work_key` to `view.work_item()`.

The CLI finishes one selected stream in one verified snapshot to count the
intersection, retaining only the requested page. A late read or close failure
produces no success JSON. Opening still verifies the complete file, including
other sources. Source selection excludes unrelated outcome payloads from the
subsequent selection decoder; it adds no index or scale guarantee. The displayed
limit does not bound complete admission/count work or the largest decoded payload.
Restart paging after publishing more results. Reading neither retries work nor
creates new scientific credit.

## Inspect the original confirmed evidence

Use this route to understand one declared work item without repeating screening.
First find its exact `work_key` in the
[manifest preview](recoverable_prepared_screening.md#inspect-declared-work-in-pages),
then request its detail:

```bash
python -m pharmacophoremt_results RUN.sqlite3 --work-key WORK_KEY
```

Replace `RUN.sqlite3` with your saved run and `WORK_KEY` with a literal work key.
Use shell quoting for spaces or other shell characters. Source and occurrence
keys do not substitute for the work key; repeated source entries remain distinct.
An unknown key is an error, rather than a pending or negative result.

For a key beginning with a dash, attach the value to the option using `=`;
quoting a separated value alone does not prevent option parsing. For example,
this selects the literal key `--failed key α`:

```bash
python -m pharmacophoremt_results RUN.sqlite3 --work-key='--failed key α'
```

The response uses `pharmacophoremt.screening-work-item@1`. It retains the
original `run_id`, `run_format`, ordered-work checksum `work_sha256` and exact
`work_item` mapping, including its manifest ordinal. Interpret the result as:

| `status` | `confirmed` | `outcome` |
| --- | --- | --- |
| `matched` | `true` | Original confirmed match, including its saved score and native evidence |
| `not_matched` | `true` | Original confirmed nonmatch; a valid zero score stays scored |
| `failed` | `true` | Original failed native result and recorded error information; score remains absent |
| `pending` | `false` | `null`, including never-started work and staged but unpublished attempts |

`attempts` counts retained started, staged and committed attempts for this work.
Those counts do not prove that a worker is still running. Unpublished payloads
are not returned as results. Confirmed failure is distinct from pending work and
does not become a negative compound or an automatic retry.

Detail deliberately includes the **complete original confirmed evidence**, which
can contain geometry and portable attribution. Choose what you share. Original
fields and unit declarations are preserved without recomputing scores, interpreting
chemistry or creating scientific credit. Opening checks the entire saved run;
detail selection does not bypass corruption elsewhere in the file.

In Python, use `view.work_item(work_key)` on an open, caller-owned
`ScreeningRunView`. The result is detached; changing it does not change the view
or original file. See the [public API](../../api/users/api_users.rst) for the method.
Close the view before reopening a writer. Legacy reference files need the explicit
`--allow-legacy` command flag or `allow_legacy=True` in Python.

Detail cannot be combined with `--summary`, `--work-items`, outcome exports,
`--score-method`, `--limit` or `--offset`. Handled admission/storage/close errors
exit2 without a success JSON document. For all-work counts or complete confirmed
outcome exports, use the [other saved-view operations](recoverable_prepared_screening.md#inspect-and-export-the-saved-view).
These source-development features retain their separately documented installation
scope; a successful read establishes saved consistency, not biological validity.
