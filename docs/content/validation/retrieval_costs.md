# Equivalent native retrieval costs

This computational calibration, owned by LMMV/dprada under
[issue184](https://github.com/uibcdf/pharmacophoremt/issues/184), compares a
prepared-inventory scan and the existing unshipped pair-index composition on the
same [six-family analytical problem](typed_retrieval.md). The
[receipt/full original archive](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/retrieval_cost_20261110.json)
retains all samples, complete correspondence outputs and actual attribution.

## Fixed problem and measurement boundaries

Eleven work occurrences retain ten original captured byte strings from four
analytical parents, including short/empty and repeated inputs. Twelve queries
cover full three/four-point mappings and the previously qualified numerical
candidate band. No new molecular preparation, chemical library or activity data
is used. Every returned mapping and original work/feature join is checked against
frozen #182 outputs, preserving its boundary disagreements with the physical
pair-distance oracle. This measures the native proposal stage, not final fitting,
orientation acceptance, biological activity or complete screening.

The [declaration](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/retrieval_cost/declaration.json)
fixes width 1 angstrom, source/exact-owned218 contexts, nm/pm policies, one full
warmup per strategy and three paired samples per stratum: twelve primary pairs.
Orders alternate and reverse across unit policies; each three-pair stratum has
a 2:1 first-position imbalance, while the complete six-pair context is balanced.
A preceding one-pair nm calibration admits resources and is excluded from the
comparative statistics. No performance threshold selects or rejects a sample.

Common file reading and native reconstruction are measured separately. Both
strategies share that prepared pool and verify current original byte/work bindings
on every query. Index construction includes the unchanged wrapper's repeated
validation/reconstruction and its own record/settings hashing. Both call the same
public native reference. The first query runs on a new strategy object; the next
batch performs the full twelve queries, including the first query again. There
is no query-result memoization.

Timers record wall/CPU nanoseconds with attribution explicitly enabled equally.
Capture setup/export, scientific comparisons and checkpoint writes stay outside
timed windows. Profilers, tracing and allocation measurement are rejected during
timing. A separate tracemalloc sample covers reconstruction, route construction
and one batch from already loaded original bytes. It is not complete native
memory or incremental RSS. These are warmed-process measurements with uncontrolled
OS caches, not fresh-process startup or OS-cold costs.

## Original results — 2026-11-10 UTC

All 38 focused guards pass per tested context. All original complete mappings and
joins agree across the calibration, twelve pairs, warmups and separate allocation
samples: 3768 actual native reference calls in those benchmark bodies. A twelve-
query batch uses 132 calls for scan and 31 for index. Prefilter/cardinality negatives
remain distinct from native evaluated-empty outcomes. Scientific runtime and the
214-payload owned artifact remain unchanged; 159 runtime bodies, 4594 provider
Python files/native and 67 case files verify.

Median wall time in milliseconds, with three samples in each row:

| Context / unit | Scan build + first | Index build + first | Scan reused batch | Index reused batch |
| --- | ---: | ---: | ---: | ---: |
| source / nm | 111.70 | 125.24 | 1263.46 | 594.24 |
| source / pm | 131.40 | 136.47 | 1487.82 | 648.33 |
| installed / nm | 115.04 | 128.65 | 1311.03 | 610.54 |
| installed / pm | 134.60 | 140.56 | 1498.75 | 668.85 |

Shared file reading/native reconstruction are excluded from these columns and
retained separately in the archive. Build-plus-first medians are computed from
per-sample sums, rather than sums of separate medians. All original wall/CPU
samples, ranges, preparation phases and per-phase portable attribution remain
available in the receipt.

In all twelve pairs, index build plus the first query costs more than scan:
index/scan ratios range 1.027–1.141. In the subsequent twelve-query batches, scan/
index wall-time ratios range 2.100–2.307. This demonstrates a setup/reuse tradeoff
in this tiny fixed workload. It neither identifies a universal crossover nor
selects a production default for other query mixes or corpus sizes.

Separate traced peaks are approximately 1.163–1.166 MB for scan and
1.264–1.265 MB for index (decimal MB), excluding preloaded raw bytes. Original
snapshot bytes total 166473 by work occurrence or 149646 across ten unique hashes.
Actual persisted-index size is **unknown/null**: this prototype has no persisted
index representation. A debug encoding or Python object size is not substituted.

Hardware: shared Linux x86_64, Intel Xeon E5-2630 v4 at its declared 2.20 GHz model,
20 logical CPUs/~65 GB physical RAM; one CPU/backend thread was used with low
CPU/I/O priority and unchanged conservative resource stops. Actual frequency,
other jobs and OS caches were uncontrolled. Python 3.14 and original source/
editable/owned producer versions, provider/native hashes and scoped import
qualification remain in the evidence. No broader supported-platform claim follows.

## Reproduce and maintain

The [contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/retrieval_cost_workloads.md),
[guard](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/test_retrieval_cost_workloads.py)
and [driver](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/benchmark_retrieval_cost.py)
link the frozen inputs, expected original outputs and admission boundaries.
Admit a compatible environment and shared resources, choose a new output and
supply your own verified execution-context hash:

```bash
python -m pytest --receptor=llm tests/test_retrieval_cost_workloads.py
python -m devtools.benchmark_retrieval_cost --snapshot-context source \
  --sample calibration --output calibration.json \
  --admission-sha256 YOUR_FROZEN_CONTEXT_SHA256
python -m devtools.benchmark_retrieval_cost --snapshot-context source \
  --sample paired --output paired.json \
  --admission-sha256 YOUR_FROZEN_CONTEXT_SHA256
```

Review calibration resources before admitting paired samples. Preserve each run
identity and every original result; changed inputs, native/provider bodies or
measurement boundaries require a new run. Checkpoint retention follows
[the interruption controls](retrieval_checkpoints.md). No old result is rewritten.

Next define persisted search-asset identity/lifetime requirements and broader
query-mix/corpus workloads before production-index selection. Real persistence,
process/OS-cold costs, complete native memory, molecular collection ownership,
human usability and full public/platform/release gates remain open. #148/#165
remain stopped. This calibration does not establish general screening throughput.
