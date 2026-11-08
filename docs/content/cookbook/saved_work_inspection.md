# Inspect one saved input

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
