# Cached receptor-generation scaling

This computational baseline belongs to
[PharmacophoreMT #97](https://github.com/uibcdf/pharmacophoremt/issues/97),
owners LMMV/dprada, 2026-11-05. It follows audit item 16: measure a declared
workload before optimizing. It evaluates the existing public cached donor/ring
hypothesis generator. No molecular system or biological data is used.

## Declaration and reproducibility

The [protocol](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/cached_generation_scaling_protocol.md)
and [frozen plan](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/cached_generation_scaling/plan.json)
define ten workloads before timing. The
[opt-in driver](https://github.com/uibcdf/pharmacophoremt/blob/main/phmt_test_support/benchmark_cached_generation.py)
and plan are frozen at `d2fc819929a93fe0273c7b2b68e0ff9d27d708a2`.
The driver runs against the borrowed, previously received public dependency
prefix; actual PHMT source is immutable `9c163654375c5933be6400282105b89376f03578`.
Runtime code is unchanged. This is a new measurement with an explicit helper,
not a new clean installation or a PHMT release artifact.

Synthetic typed PHMT feature records supply donor/ring directions and centers,
source-correspondence tokens and optional exclusion centers. They do not encode
a prepared molecule, infer chemistry or claim authentic molecular source data.
No MolSysMT preparation/recognition/geometry/format operation is invoked.
Numerical hypotheses use explicit nm offsets/radii; all input caches remain intact.
The repository license applies to these original numerical fixtures. Molecular
variants, experimental acceptor directions and real-receptor cost need separate
provider-backed cases. There are no activity endpoints, class labels or holdouts.

Two donor distances and two distances on each ring face give exactly
`2**donors * 4**rings` alternatives. An independent mixed-radix oracle checks
every returned model's roles, centers, normal, radius, choice/source indices,
weights and essentiality, plus exact visited/returned/remaining/completion counts.
Tolerance is 1e-12 in the explicitly requested nm/dimensionless values.
Budget-zero output remains incomplete; it is not a scientific negative.

## Measurement boundary and shared resources

Each case/mode uses a fresh serial worker and one warmup. Five uninstrumented
elapsed samples cover only the public generator call, including admission,
materialized models and detached metadata. Imports, cache creation, garbage
collection, oracle checks, serialization and persistence are outside the timer.
Garbage collection is disabled only during the call. A separate worker measures
one current/peak traced-allocation sample with tracemalloc; those bytes are not
RSS or total native memory, and instrumented elapsed times are not reported.

The shared-machine execution uses one allowed logical CPU (19), six numerical/
backend thread limits of one, CPUQuota=100%, a combined 1 GiB memory cap, zero
swap allowance, nice=19 and idle I/O priority. Effective kernel values are
recorded before execution. All own tests/builds finish before timing. Admission
requires at least 4 GiB available RAM and no current full-memory stalls; longer
pressure averages and machine conditions remain in the receipt. Other users and
processes remain active, so elapsed spread is descriptive and machine-specific.

Optional attribution is explicitly disabled in workers. The receipt retains
actual loaded software/native identities; no portable bibliographic capture or
data/method references are fabricated. Costs with active citation tracking need
their own declared measurement.

## Original results — 2026-11-05

All ten cells complete both modes: **20 workers, 50 timing samples, ten separate
traced-allocation samples and 20 warmups**. All 80 calls agree with the independent
oracle; caches/unit policy and selected source/provider/native identities remain
stable. The [summary and original archive](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/cached_generation_scaling_20261105_summary.json)
retain every sample, command, worker outcome and actual resource receipt.

| Donors/rings/exclusions | Budget | Possible / returned | Median elapsed (min–max), ms | Peak traced MiB |
| --- | ---: | ---: | ---: | ---: |
| 1/1/0 | 8 | 8 / 8 | 524 (522–646) | 0.593 |
| 2/2/0 | 8 | 64 / 8 | 1,024 (1,014–1,497) | 1.005 |
| 4/4/0 | 8 | 4,096 / 8 | 3,196 (1,836–4,097) | 1.832 |
| 8/8/0 | 8 | 16,777,216 / 8 | 3,954 (3,763–5,123) | 3.480 |
| 2/2/0 | 0 | 64 / 0 | 21 (20–22) | 0.081 |
| 2/2/0 | 1 | 64 / 1 | 148 (137–155) | 0.212 |
| 2/2/0 | 32 | 64 / 32 | 4,217 (3,997–5,658) | 3.698 |
| 2/2/0 | 64 | 64 / 64 | 8,527 (8,326–8,863) | 7.283 |
| 2/2/16 | 8 | 64 / 8 | 1,327 (1,310–1,342) | 1.923 |
| 2/2/64 | 8 | 64 / 8 | 2,097 (2,074–2,110) | 4.568 |

Only the first and budget-64 rows exhaust their alternatives. The spread,
particularly the 4/4 row, limits causal scaling interpretation. These are warmed
API calls on the recorded shared host with explicit resource restrictions;
fresh workers do not imply a cold operating-system file cache. No comparison
against a different implementation or unconstrained machine is measured.

Twenty-four unique workload/oracle guards have passing evidence across retained
scopes. Initial checks expose a test-only implicit unit strip and a later raw-list
normal-corruption fixture; both are corrected before timing, preserving their
outputs. The corrected normal guard passes with the new resource limits; the
other 23 passing guards remain applicable. The original full guard suite is not
represented as newly reexecuted under those limits. No production algorithm or
scientific setting changes.

## Interpretation and maintenance

The workload axes vary feature/site counts, finite budget and exclusions. Rows
with different returned hypotheses or site counts do not establish an
equivalent-work speedup. Exact theoretical totals do not mean all alternatives
were visited. This case makes no affinity, chemical-model, real-receptor,
asymptotic-complexity or broad performance claim and introduces no optimization.

The oracle/control tests are
`tests/test_cached_generation_scaling.py`; no benchmark runs in routine CI.
Reexecute after generator, provider, workload, instrumentation, resource limit
or machine changes. Preserve earlier measurements and all failed attempts.
#95's public modern-provider delivery and #9/#10/#23's full source/installed/
platform/release gates remain independent.
