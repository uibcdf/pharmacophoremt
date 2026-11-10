# Inspect saved screening work

Check the installed distribution before following development-reader examples:

```bash
python -m pharmacophoremt_results --version
```

The output labels installed `pharmacophoremt` distribution metadata. This option
needs no saved file, score criterion or molecular provider. Missing or invalid
metadata is an explicit error. An editable/source checkout can have metadata
from a different build; this version alone does not identify its current code
or qualify its capabilities. Help and ordinary inspection do not query version
metadata. Use the [installation context](../about/installation.md) when reporting
a version or comparing artifacts.

Start with `python -m pharmacophoremt_results RUN.sqlite3 --summary` to see the
saved counts. Then select work by status or source and inspect a literal work key using
the commands below. Each command opens its own verified snapshot.

## Browse the original sources

List the exact source labels before choosing one for inspection:

```bash
python -m pharmacophoremt_results RUN.sqlite3 --sources
python -m pharmacophoremt_results RUN.sqlite3 --sources --limit 10 --offset 10
```

Each record contains `source_key`, `first_manifest_ordinal` and `declared_work`.
Sources follow their first occurrence in the original work manifest. Repeated
occurrences share their literal label's work count; pending, failed, matched and
unmatched entries all count. These are source labels and work entries, not a
count of independent compounds or chemically equivalent molecules.

The response format is `pharmacophoremt.screening-source-page@1`. Its run ID,
run format and `work_sha256` identify the original manifest; `declared_work`
counts all work and `declared_sources` counts distinct literal labels. `offset`
and `next_offset` address the **source** stream, while each record's first
manifest ordinal remains global. `next_offset=null` means no later source.
Empty inventories and offsets beyond the end return no rows. Limits must be
positive and offsets nonnegative; the default limit is ten.

Copy an exact `source_key` from a page and use
`--work-items --source-key=SOURCE_KEY` below. Case, spaces, Unicode and punctuation
remain literal; aliases and compound identities are not inferred. Publishing
more outcomes does not change this inventory: the declared manifest is immutable.
Use a new run/hash as a new paging context. Status-selected work pages have their
own offsets and can change membership after a writer publishes new outcomes.

In Python, iterate `view.source_items()` in an open caller-owned
`ScreeningRunView`; close an iterator when consuming only a prefix. Records are
detached and contain no native or draft payload. Source browsing requires no
ranking criterion or scientific provider. The source mode cannot be combined
with work/status/key filters, ranking, summary or exports. Legacy files require
explicit admission. Each page still verifies the complete file and counts all
sources; a display limit bounds returned records, not all processing or storage.
Handled read/count/close errors produce no success JSON.

## Discover a source and inspect its work in one snapshot

Use this complete example when you want to discover an original source and
review its work without copying a key between separate snapshots. Set the five
inputs. `source_index = 0` chooses the first source in manifest encounter order:

```python
from contextlib import closing

from pharmacophoremt_results import ScreeningRunView

run_path = "RUN.sqlite3"
source_index = 0
status = "failed"
limit = 10
allow_legacy = False

with ScreeningRunView.open(run_path, allow_legacy=allow_legacy) as view:
    configuration = view.configuration
    declared_sources = 0
    selected_source = None
    with closing(view.source_items()) as sources:
        for index, source in enumerate(sources):
            declared_sources += 1
            if index == source_index:
                selected_source = source
    print("Run:", configuration["run_id"])
    print("Declared work:", configuration["work_count"])
    print("Declared sources:", declared_sources)
    if selected_source is None:
        print("Source index not found:", source_index)
    else:
        source_key = selected_source["source_key"]
        selected_work = 0
        selected_prefix = []
        with closing(view.work_items(source_key=source_key, status=status)) as work:
            for mapping in work:
                selected_work += 1
                if len(selected_prefix) < limit:
                    selected_prefix.append(mapping)
        print("Source:", repr(source_key))
        print("Source declared work:", selected_source["declared_work"])
        print("Status:", status)
        print("Selected work:", selected_work)
        for mapping in selected_prefix:
            detail = view.work_item(mapping["work_key"])
            print(
                mapping["manifest_ordinal"],
                repr(mapping["work_key"]),
                detail["status"],
                detail["attempts"],
            )
```

Choose a nonnegative source index, one of `failed`, `pending`, `matched` or
`not_matched`, and a positive detail limit. The source index is a zero-based
position in the **source** stream; it is different from a work item's global
manifest ordinal. It follows the same source order as `--sources` pages above.
An empty inventory or an index beyond its end prints the run counts and an
explicit missing-index message. A present source with no work in the selected
status prints `Selected work: 0` and no details.

`Declared sources` counts all literal source labels. `Source declared work`
counts every original occurrence for the chosen label. `Selected work` counts
the complete source/status intersection; the detail loop displays only its
first `limit` entries. Repeated source/occurrence labels preserve their separate
work keys and original global ordinals. No trimming, alias or compound grouping
is applied. `repr()` keeps spaces and opaque key characters visible.

One caller-owned view binds discovery, selection and details to the same saved
snapshot. Both iterator contexts close on early exit or failure, and the outer
context closes the view. A displayed `detail` remains detached after closure
and retains its complete original confirmed `outcome`, or `None` while pending.
The display prints scalar status/attempt information only. Unpublished drafts
remain pending; reading does not retry work or prove a worker is running.

Set `allow_legacy = True` only for a deliberately admitted legacy reference file.
After publishing more work, reopen a view and select again: status membership
can change although the original source manifest stays immutable. The example
retains one selected source and at most `limit` work mappings, but still verifies
the complete file, counts both full streams and may decode a large original
detail. This is no indexed or large-library performance guarantee.

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

## Inspect one source in one Python snapshot

Use this complete example when a source's count and displayed details must refer
to the same saved state. Set the five input parameters first:

```python
from contextlib import closing

from pharmacophoremt_results import ScreeningRunView

run_path = "RUN.sqlite3"
source_key = "SOURCE_KEY"
status = "failed"
limit = 10
allow_legacy = False

with ScreeningRunView.open(run_path, allow_legacy=allow_legacy) as view:
    configuration = view.configuration
    selected_work = 0
    selected_prefix = []
    with closing(view.work_items(source_key=source_key, status=status)) as work:
        for mapping in work:
            selected_work += 1
            if len(selected_prefix) < limit:
                selected_prefix.append(mapping)
    print("Run:", configuration["run_id"])
    print("Declared work:", configuration["work_count"])
    print("Source:", repr(source_key))
    print("Status:", status)
    print("Selected work:", selected_work)
    for mapping in selected_prefix:
        detail = view.work_item(mapping["work_key"])
        print(
            mapping["manifest_ordinal"],
            repr(mapping["work_key"]),
            detail["status"],
            detail["attempts"],
        )
```

Copy the exact nonempty `source_key` from a saved work page. Choose `failed`,
`pending`, `matched` or `not_matched`, and a positive display limit. `Selected work`
counts the **complete source/status intersection**, while `Declared work` counts
the whole run. The global status counts returned by `view.progress()` include
other sources and cannot supply this source-specific total. An unknown source
prints the five summary lines, a selected count of zero and no detail rows.

The count consumes the selected iterator once, retaining at most `limit` original
mapping records. It closes that iterator before inspecting the retained keys in
the same open view. Repeated occurrences remain separate; ordinals stay global.
Keys pass directly between public tools, without normalization; `repr()` makes
spaces, Unicode and leading dashes visible. This is the public expert composition
of the same source selection and detail operations used by the guided journey.

The display prints scalar mapping/status/attempt information. Each `detail`
contains the complete original confirmed `outcome`, or `None` while pending.
When a row was displayed, the last detached `detail` remains available after the
view closes; choose what to share from that full evidence. Staged or never-started
work stays pending, unpublished failures stay pending, and a confirmed failure
stays distinct from a valid zero score. Inspection does not retry work or create
scientific credit.

The display limit bounds retained mappings, not the cost of opening/counting the
full selection or the size of one original outcome. Opening verifies the entire
file, including other sources. Use `allow_legacy=True` only for deliberate legacy
reading. Close the view before reopening a writer; after new confirmations, open
a fresh view and repeat the selection. Separate CLI commands open separate
snapshots; use the single-view example when counts and details must agree.

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
