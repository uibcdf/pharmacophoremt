# Saved-run inspection and export scaling

Case `saved-reader-scaling-20261107`; owners LMMV/dprada;
[#144](https://github.com/uibcdf/pharmacophoremt/issues/144).
This engineering profile uses synthetic saved-format records, with no molecule
prepared or evaluated. Its source parent is f2bd4cf, with the frozen uncommitted
case overlay and all nine unchanged reader source files recorded in the receipt. It measures the current public reader/writer/export
operations before selecting a cache or index. It does not measure molecular
screening throughput or biological activity.

The [declared protocol](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/saved_run_scaling.md)
and [original receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/saved_run_scaling_20261107_summary.json)
retain exact sources, all samples, resource limits, the preparation timeout and
separate public recovery. The fixed driver is `devtools.profile_saved_run`;
`tests/test_saved_run_profile.py` protects independent answers and failed records.

## Workload and answers

Each ten-record block contains7confirmed outcomes: four positives with tied
scores, two zero negatives and one unscored failure. Three work items remain
pending, including a staged unpublished outcome and a begun-only attempt.
Publication order is reversed; ranking ties must retain original manifest order.
Full JSONL/CSV exports retain every confirmed outcome, including zeros/failure.

The declared 100/1,000/10,000 entries therefore contain 70/700/7,000 confirmed outcomes.
No count represents an independent compound or an experimental activity. Every
normal open retains full saved-record verification, including nonranked/staged
corruption guards. Inputs and exports pass exact independent count/order/payload
oracles and original DB/manifest bytes remain unchanged.

## Measurements and scope

Repeated columns are five-sample wall-time medians after one warmup. First-open
has one post-import observation per fresh process. OS page-cache state is
uncontrolled; whole-process RSS includes imports and oracles.

| Declared / committed | First verified open (ms, one observation) | Progress (ms) | Top10 (ms) | Top100 (ms) | JSONL (ms) | CSV (ms) | Whole-process peak RSS (MiB) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 100 / 70 | 30.559 | 6.234 | 6.464 | 6.339 | 8.025 | 7.477 | 36.88 |
| 1000 / 700 | 166.758 | 52.214 | 48.739 | 49.570 | 58.946 | 53.115 | 37.96 |
| 10000 / 7000 | 1165.287 | 477.277 | 486.369 | 493.320 | 586.131 | 526.387 | 40.61 |

Actual execution uses Linux/Python 3.14.10 on one logical CPU of an Intel Xeon
E5-2630 v4, one backend thread, low priority and 512 MiB AS per process. It uses the
qualified source/provider environment, not a newly solved public installed
artifact. Every sample, spread and actual source/import identity is retained;
there is no speedup or memory-complexity claim.

The original 10,000-work preparation reaches the 180 s child deadline. Its raw run
stays failed, with the partial DB/journal/manifest unchanged. A separately declared
owned-copy recovery preserves 6,784 confirmed outcomes and fills 216 more through the
public store API; its reader then completes. The 10,000 row is a recovered-fixture
reader measurement, not a successful one-shot preparation under 180 s. Original
100/1,000 preparation takes 1.796/18.082 s wall; neither timing isolates storage or
scheduling causes.

Progress and both Top-K sizes have similar cost in this fixed case. That motivates
reviewing the common scan/verification path and immutable snapshot reuse before
adding a ranking index. Full admission, live-writer freshness and detached count
semantics must survive any future change. No cache, index, new molecular collection
or broader delivery qualification follows from this profile.

## Reproduce

Review the owning protocol and apply the shared workstation limits before:

```bash
python -m devtools.profile_saved_run --output NEW-profile-directory
```

The fixed driver currently requires Linux `/proc` memory/pressure admission.
Destinations must be fresh; failures and partial outputs remain preserved. The
original recovery controller and measured producer remain in the sealed case
evidence. The [reusable recovery receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/saved_run_recovery_20261107_summary.json)
now qualifies this explicit command on a fresh owned copy:

```bash
python -m devtools.profile_saved_run --recover-from FAILED-profile-directory --output NEW-recovery-directory
```

It preserves original report/DB/journal/manifest bytes, rejects ineligible or linked
inputs, and uses public store recovery without duplicate attempts. The new run
reports only recovery and its reader phase; the original preparation remains failed.
Its extra samples are separate from the baseline table. All 22 independent case
controls pass, including provenance, exact metadata types and staged-data conflicts.
No timing threshold is part of routine CI.


Owners LMMV/dprada review this case when the reader, store, export, preparation or
provider context changes. A new execution receives a new identity and preserves
these original samples, source overlay and failure. This case invokes no optional
scientific attribution or molecular calculation. Broader source/installed/public/
platform and release acceptance keep their separate gates.
