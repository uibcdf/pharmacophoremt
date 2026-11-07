# Incremental prepared-library reference prototype

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108).
This implements increment B of the [library architecture](public_library_architecture.md)
in [`phmt_test_support/prepared_library_reference.py`](../phmt_test_support/prepared_library_reference.py).
Its unshipped names and outcome envelope are experimental, not a public API or
persistence commitment. Existing runtime APIs and batch behavior are unchanged.

## Composition and identity

`screen_prepared` receives an existing `PoseEvaluator`, `RigidPoseSearch` or
`ConformerScreening`, an explicit score criterion and producer-prepared entries.
The native public empty-batch `run` preflights decidable options before requesting
an iterator from the source. Actual molecular work uses public single-input
`evaluate`; scoring uses `get_screening_score`. The prototype reuses PHMT's
internal score resolver and failure-record helper. An empty preflight cannot
establish provider-dependent molecular selection validity.

Each `PreparedInput` carries three opaque producer-supplied keys:

| Key | Meaning and multiplicity |
| --- | --- |
| `work_key` | Unique declared evaluation work item; also the explicit native `pose_id` |
| `source_key` | Original source record reference; may repeat across occurrences/work items |
| `occurrence_key` | Source occurrence reference; can group work expanded from that occurrence |

Keys must be nonempty strings when encountered. The producer establishes work-key
uniqueness and mapping; the prototype retains no collection-sized uniqueness set
and infers no molecular equivalence. Repeated object references/source records
remain separate declared work. Provider aliases, state expansion and assay
aggregation remain outside this control. Work counts are not independent-compound
counts. Existing saved-results ordinal/sample maps require their separate contracts.

Prepared objects and the constructed evaluator/query, including method/settings,
must remain unchanged during consumption. A frozen entry wrapper does not freeze
its molecule, authenticate a prepared artifact or implement a snapshot. MolSysMT
retains molecular reading, preparation, state/frame mapping and identity ownership.
No acquisition, parser, conformer generation, index or dependency is introduced.

## Consumption and outcomes

The ordinary outer function performs preflight immediately and returns a generator.
Creation performs no source pull or preview sampling. Each pull requests one entry,
completes its native evaluation, then yields one portable outcome. Adapter state is
bounded by a current input/result and fixed options. Individual molecular workload
and caller accumulation remain outside that collection-length bound. This is a
structural execution contract, not a throughput or allocation benchmark.

The caller owns source replay and closure. Closing the result generator stops
pulling and releases adapter-held references; it does not call `close()` on the
source. A caller-owned generator can still finalize when its last reference
disappears under normal Python lifetime rules. Callers must retain/manage readers
they intend to reuse. No automatic reopening is claimed.

Outcomes contain the three keys, complete `native_result`, explicit `ranking_score`
and versioned score criterion. They contain no molecular handle and add no invented
native ordinal `input_index`. Native frame/state/assignment/error fields remain
untouched; passing the work key into evaluation preserves nested IDs. Encounter
order is retained; global ranking is a distinct consumer/storage operation.

Options are copied at construction. Native option names/value constraints remain
owned by ArgDigest at existing tool boundaries. Outer and per-frame policies use
the same explicit `on_error`; digestion bypass and embedded policy overrides are
refused. Existing catalog exceptions supply diagnostics. No new public argument,
optional-backend or physical-quantity conversion boundary is added. Native tools
retain those integrations and actual attribution evidence.

With `on_error='record'`, native `PoseEvaluationError` becomes the existing unscored
failure record and iteration can continue. Reader, mapping and programming errors
propagate. Raising remains the default. Yielded results belong to the caller;
there is no facade cache or publication transaction. Inspect native status
independently of coverage/score:

- A completed no-fit seeded negative has `fit_value=None` and score zero.
- A failed/unresolved calculation has score `None`, even with a best observation.
- A hit can retain failed frames and still have a proven maximum score.
- Unit coverage alone does not satisfy every essential-site constraint.

## Development use

Given already prepared inputs and a compatible existing query:

```python
from contextlib import closing

from phmt_test_support.prepared_library_reference import PreparedInput, screen_prepared
from pharmacophoremt.screening import PoseEvaluator

entries = (
    PreparedInput(work_key, source_key, occurrence_key, molecular_system)
    for work_key, source_key, occurrence_key, molecular_system in prepared_records
)
outcomes = screen_prepared(
    entries,
    PoseEvaluator(query),
    score_method="checked_pose_coverage",
    evaluation_options={"selection": [0, 1, 2]},
    on_error="record",
)
with closing(outcomes):
    for outcome in outcomes:
        consume(outcome)
```

`prepared_records`, `query` and `consume` belong to the caller. This example
provides neither preparation nor persistence. The selection must suit the declared
prepared input contract.

## Qualification and next boundary

The [declared placement amendment](evidence/public_library_incremental_support_plan_20261107.json) and
[execution receipt](evidence/public_library_incremental_support_20261107_summary.json)
link producer overlay, selected tests, environment, resource limits and original
outputs. The focused guard is
[`tests/test_prepared_library_reference.py`](../tests/test_prepared_library_reference.py).
These are analytical software controls: no chemical acquisition, activity labels,
competitor execution, benchmark or biological validation.

The declared run passed all **26 cases**, with zero failures/errors/skips.
Source/support files and the MolSysMT native artifact were unchanged across the
run. Enforced limits were CPU 19/100% quota, 512 MiB memory, no swap, 32 tasks,
nice 19, idle I/O and one backend thread. Whole-cgroup peak was 344,678,400 bytes,
with no OOM/max events. This includes the controller/tests and is not per-input
allocation. Python was 3.14.10; exact provider versions/origins are in the receipt.

The migrated workspace lacked the optional default `.molsyssuite` administrative
checkout. A first help/preflight launch failed before scientific execution. An
isolated local checkout of the already accepted SDK pin restored declaration
checking through `PHARMACOPHOREMT_SUITE_ROOT`; no pin or shared environment changed.
Declaration checking is separate from installed dependency closure.

The first passing 26-case run used the original test module under `devtools/tests`.
Before publication, source inspection found that this directory is imported by
dependency-light administrative unittest discovery. The controls were moved into
the default scientific `tests/` selection; a second execution also passed all 26
cases. Final integration additionally moves the unchanged implementation into
`phmt_test_support`, declares its exact bytes for existing private installed-test
staging, and changes only the test module's import. A third declared execution
qualifies this support layout. Both earlier outputs/source overlays and the
[first receipt](evidence/public_library_incremental_20261107_summary.json) remain
preserved. These are collection/support-boundary corrections, with no analytical
assertion, oracle or scientific-method change.

The affected distribution/staging suite passes **24 controls** with scientific
imports actively forbidden. The new guard verifies private helper bytes and
namespace resolution without importing the helper or exposing checkout runtime
packages. Reporting (3) and archive (18) controls and full Ruff check/format also
pass. No installed artifact or full matrix is qualified by staging alone.

A broader administrative discovery was OOM-killed at its 512-MiB limit during
an existing ESR1 evidence-restoration test. The original partial log and later
systemd confirmation are retained; it has no passing full-suite count. The focused
24-control recovery uses the same limits and passes without OOM events. Broader
administrative coverage remains tracked in #9; no resource cap was raised.

Increment C remains separate: saved query/input/plan identities, single-writer
journal, committed-outcome integrity, interrupted recovery and linked retry runs.
Closing a generator is cancellation of future work, not a durable checkpoint.
Producer-declared keys alone do not prevent duplicates after restart. The
architecture's authoritative committed-failure rule is unchanged. Public
guided/expert names, real-provider receiving and reusable search assets remain
unqualified; full source/installed/platform and release gates remain separate.
