# Saved-run inspection and export scaling

Owners LMMV/dprada; declared2026-11-07;
[#144](https://github.com/uibcdf/pharmacophoremt/issues/144), mature0.x milestone5.
Status: fixed helper/driver and10independent guards implemented/passing;
three reader cells/75repeated samples are now qualified, with the original
10000-work preparation timeout retained. No speedup is claimed.

Measure the existing public `ScreeningRunStore` and `ScreeningRunView` operations.
The reader already scans SQLite rows and keeps at most K ranking payloads. That
implementation observation is not measured latency, incremental allocation or
an asymptotic experiment. Preserve complete verification before observing data,
including staged/failed records outside the retained Top-K.

## Fixed input and independent answers

Create fresh public-format stores through public create/begin/stage/publish,
with100,1000,10000 declared work entries and256ASCII bytes of synthetic payload
padding. Query bytes and producer context explicitly identify a reader-format
fixture. No molecule is prepared or evaluated. Work/source/occurrence keys remain
opaque identifiers; these records are not independent compounds or activities.

Each ten-record block declares this fixed pattern, in original ordinal order:

| Ordinal modulo10 | Outcome | State |
| --- | --- | --- |
| 0,6 | matched, score1 | committed |
| 1,7 | matched, score0.5 | committed |
| 2,8 | not_matched, score0 | committed |
| 3 | failed, scoreNone | committed |
| 4 | none | pending, never begun |
| 5 | matched, score1 | staged, unpublished |
| 9 | none | begun, unstaged |

Use `checked_pose_coverage@1` solely as the saved format's explicit criterion.
These synthetic values are not reconstructed native witnesses. Publish committed
records in reverse manifest order to test ordinal ties. Each block has7committed,
6scored,4matched,2not-matched,1failed,3pending; attempts9started/8staged/7committed.
Exact independent rank and export oracles derive from this table, not reader
output. Preserve zeros, failures and every committed record in manifest order.

## Phases and measurements

Record writer creation/population time and database/manifest bytes separately.
For each immutable store, use a fresh process to import the reader and then
measure its first verified open. Startup/import time is outside this phase.
Perform one unreported warmup, then five recorded repeats for progress, Top-K10,
Top-K100, full JSONL and full CSV. Each export has a new owned destination and
retains the original full/scalar contract. Record every wall/process CPU sample,
all file hashes/bytes and all failures; never silently omit a failed repeat.
Validation of results and exported files stays outside each timed operation.

The OS page cache is uncontrolled. First verified open does not mean cold disk
I/O. Whole-process peak RSS includes imports, preparation/oracles and recorded
operations; it is not incremental call allocation or a memory-complexity proof.
Use standard-library clocks/resource tools. No timing threshold runs in CI.
Retain fixed hardware/OS/Python/provider/source/import identities and actual
CPU/thread/priority/limits, memory/pressure/load observations and sample order.
Interpret sample spread before considering a performance change.

The shared development-tool catalogue was inspected: existing installed-origin
and reporting tools keep their purposes; no generic benchmark executor is
required for this component-owned fixed case. Reuse public store/view/export
operations and standard-library measurement, with only case-specific orchestration.
No database parser, molecular tool, matcher, index or cache is introduced.

## Resources and acceptance

Run heavy work serially on CPU19, one backend thread, nice19/idleI/O. Reader-only
Python uses512MiB per-process address space and180s per child, with available
memory>2GiB and pressureavg10<1 before entry. No owned aggregate memory/swap/tasks/
quota control exists. Defer under pressure; preserve exhausted attempts and do
not raise limits or quietly reduce declared sizes. Never change unrelated work.

Block molecular/numerical/main-library imports during actual reader profiling.
This first baseline may use the qualified source/provider environment; name its
actual origins and source hashes rather than claiming public installed delivery.
Keep old source/native/prefix state unchanged. Preserve DB bytes before/after
all read/export operations. Refuse corruption outside Top-K through normal open.

Independent input/accounting/ranking/export/immutability and corruption guards
must pass before interpreting timing. Original local ledgers/exports/samples
remain task-owned with review2026-11-20; publish only own control/scalar/hash
material. No molecular screening throughput, general collection, speedup,
biological, complete installed/public/platform or release claim follows.


## Implemented case and execution route

`phmt_test_support.saved_run_profile` owns only this synthetic fixture, independent
answers and measurement orchestration. `devtools.profile_saved_run` creates a
fresh output directory, launches separate preparation/measurement children for
each fixed size, records partial failures and rejects molecular imports. Source/
provider/import identities and each original DB/export remain recorded; this is
not installed-artifact evidence. Ten focused controls pass, including late
nonranked corruption and failed-call timing/retained earlier samples.

After reviewing this protocol and resource controls, run in the qualified source
context with a fresh owned destination:

```bash
python -m devtools.profile_saved_run --output NEW-profile-directory
```

The current execution applies CPU19/thread1/nice19/idleI/O and512MiB AS externally;
each child has a180s wall bound. The driver checks available memory/pressure
before phases and records actual inherited limits. It does not silently set a
larger budget, claim aggregate control or turn a timeout into a smaller workload.
All source/profile files remain frozen during timed execution.


## Measured result, 2026-11-07

The [receipt](evidence/saved_run_scaling_20261107_summary.json) retains every sample,
source/provider/window identity, original failure and recovery. Repeated columns
below are five-sample wall-time medians after one warmup. First-open has one
observation per fresh process after imports; OS cache is uncontrolled.

| Declared / committed | First verified open (ms, one observation) | Progress (ms) | Top10 (ms) | Top100 (ms) | JSONL (ms) | CSV (ms) | Whole-process peak RSS (MiB) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 100 / 70 | 30.559 | 6.234 | 6.464 | 6.339 | 8.025 | 7.477 | 36.88 |
| 1000 / 700 | 166.758 | 52.214 | 48.739 | 49.570 | 58.946 | 53.115 | 37.96 |
| 10000 / 7000 | 1165.287 | 477.277 | 486.369 | 493.320 | 586.131 | 526.387 | 40.61 |

The case uses Linux/Python3.14.10, IntelXeonE5-2630v4, CPU19/thread1/nice19/idleI/O
and512MiB per-process AS. Actual ArgDigest0.17.1+3.g0712641/SMonitor0.22.1+1.gc1b6ce2
source origins are recorded. All nine reader source files match across cells;
all seven forbidden scientific/main-package imports are refused in a fresh
adversarial control. The earlier Point receiving's full support-provider source
observation and the post-profile scan also match; that is a broader before/after
window, not a scan immediately before this profile. No Ackredit/scientific work
is invoked or credited.

All fixed counts, statuses, ties, full exports and original-byte checks pass.
N100/N1000 public preparation takes1.795938343/18.082459041s wall and
0.202077517/1.929602249s processCPU. The original10000preparation reaches its180s
child deadline and remains failed. Wall/CPU separation is observed; precise I/O/
scheduling causes were not profiled and no provider defect is inferred.

A [prospective recovery amendment](https://github.com/uibcdf/pharmacophoremt/issues/144#issuecomment-6714154733)
precedes a byte-verified owned copy and public store recovery. It preserves6784
confirmed outcomes, fills216confirmations and retains exactly9000started/8000staged/
7000committed attempts. The original DB/journal/manifest remain untouched. The
copied fixture recovery takes32.127564589s; only its previously unexecuted reader
phase then completes, under the same180s/512MiB controls. This is not successful
one-shot preparation under180s; preparation history differs and remains explicit.

At10000declared work, measured progress477.277ms, Top10486.369ms and
Top100493.320ms are close. Their sample ranges remain in the receipt. This
supports investigating shared payload scanning/verification and safe reuse of
immutable snapshot progress before adding a ranking index. It does not identify
a CPU call-level bottleneck, prove asymptotic complexity or measure molecular
screening throughput. Whole-process RSS includes imports/oracles and is not
incremental allocation. Live writer progress, immutable saved snapshots and the
full verification performed by every fresh reader open remain distinct.

The reusable recovery route below is now received. Preserve the original
benchmark producer/bytes and all existing measurements. Later work can declare
an equivalent immutable-progress reuse experiment; no cache is implemented or
selected by this baseline alone.


The execution driver is currently Linux-only: available-memory/pressure admission
uses `/proc`. The synthetic helper controls do not establish execution on another
platform. Full product/source/installed/public/platform gates remain separate.


## Reusable recovery route received, 2026-11-07

The [driver receipt](evidence/saved_run_recovery_20261107_summary.json) receives
one normal command on a fresh copy of the original partial10000-work fixture:

```bash
python -m devtools.profile_saved_run --recover-from FAILED-profile-directory --output NEW-recovery-directory
```

Only this fixed profile's declared preparation timeout is eligible. Require the
literal JSON boolean true, a supported integer size, expected regular database/
manifest/journal files and output outside the original profile. Never replay
saved commands or operate on linked input files. Verify the source report and
copied bytes, then recheck original identities after both phases. The new report's
completion describes copied-fixture recovery and its reader; the original run
remains failed and one-shot preparation is still unqualified.

Public recovery reuses existing attempt IDs, validates existing staged payloads,
preserves6784confirmed outcomes and fills216more. The table's9000/8000/7000attempt
counts and all original files survive. A fresh reader passes all exact checks and
25additional repeated samples. Those receiving samples are not pooled into the
original75-sample baseline. Per-child180s/512MiB AS/serial CPU19 controls remain;
no provider/library-runtime/native or package change occurs.

All22case guards pass, including original count/rank/export/immutability/corruption
controls, partial-state recovery, conflicting staged data, source provenance,
linked/inside-original output rejection, and exact timeout-flag admission. One
initial test incorrectly asked a read-only view for writer attempt inspection;
its1failure/11positive controls are preserved and the test uses the supported
store operation. A later8-case metadata guard preserves2failures/6controls before
rejecting truthy nonboolean flags. Two positive driver receivings retain their
own identities; the final one uses exactly the guarded corrected source bytes.
This closes#144's bounded baseline/reproducible-driver scope, with the failed
original preparation and all broader installed/public/platform/performance work
still explicit.

## Subsequent accumulated source receiving, 2026-11-08

The [5c3cd64/attempt1 source checkpoint](saved_run_ci_checkpoint.md) receives the
accumulated144/145/146implementation with2430passing cases in each of eight
Linux/macOS arm64 Python3.11–3.14cells, required reporting/policy/publication
steps and qualified106-file coverage. Original local measurements, failures and
owned installed artifacts retain their own source/version/byte identities.
This full source gate does not generalize performance, qualify fresh public
providers/installed platforms or cover later147runtime.
