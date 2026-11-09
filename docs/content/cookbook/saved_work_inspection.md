# Inspect one saved input

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
`view.work_items()` and command without `--status` retain all original mappings
and their ordinary page response.

The status filter applies only to `--work-items`; it does not choose a ranking
criterion or assign activity labels. Counts describe work, not independent
compounds. Complete opening/count work and confirmed filtering can scan saved
outcomes; pagination alone does not establish indexed or large-library speed.

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
