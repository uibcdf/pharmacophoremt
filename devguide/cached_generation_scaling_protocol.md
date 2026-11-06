# Cached receptor-generation scaling protocol

Declared 2026-11-05, owner LMMV/dprada, #97; audit item 16. Execute the unchanged
public `from_receptor_features` donor/ring profile on synthetic typed PHMT caches.
No molecular system, recognition, geometry calculation, prepared receptor,
scoring, affinity, holdout or experimental acceptor directions are involved.
Molecular operations remain MolSysMT-owned. #95's public modern-provider delivery
gate stays independent and no candidate/version/dependency policy changes.

## Frozen workload and oracle

[Plan](../tests/data/cached_generation_scaling/plan.json) fixes ten cells before
timing, SHA-256 `c60372071eb89aa20133c2964cfd0eff67ea12591f94d8c4589205c859b9d088`.
It fixes the following workload:
1/1, 2/2, 4/4 and 8/8 donor/ring occurrences at budget eight; separate
2/2 budget zero/one/32/64; and 2/2 budget eight with 16/64 exclusion records.
Each donor has two distances; each ring has two distances and two faces. The
exact total is `2**D * 4**R`. These cells change returned site counts or search
coverage; they are not equivalent-work alternatives or competing algorithms.

The independent oracle uses ordinal mixed-radix decoding, never the generator's
private choice/enumeration helpers. It checks total/visited/returned/remaining,
complete/incomplete including zero budget, roles, source indices, centers in nm,
ring normals, radii, choices, unit weights/essential flags and exclusion spheres.
All input caches and unit policy remain intact. It retains a compact digest of
all checked model geometry/order; no timing is interpretable after oracle failure.
Synthetic source indices are protocol correspondence tokens, not molecular data.

## Measurement boundary

Run [the opt-in driver](../phmt_test_support/benchmark_cached_generation.py) with
an absolute output path using the already received public Python 3.14 prefix:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 NUMBA_NUM_THREADS=1 RAYON_NUM_THREADS=1 \
systemd-run --user --scope -p CPUQuota=100% -p MemoryMax=1G -p MemorySwapMax=0 -p TasksMax=32 \
taskset -c 19 nice -n 19 ionice -c 3 \
/path/to/public-prefix/bin/python -I /path/to/repo/phmt_test_support/benchmark_cached_generation.py --output /owned/path/results.json
```

Each case/mode uses a fresh serial subprocess, one warmup and the fixed plan.
CPU 19 is an allowed local logical CPU in this receipt; select one allowed CPU
on another machine. Check resource admission below before running the command.
The five uninstrumented elapsed-time samples cover only the completed public
generator call, including admission, model materialization, detached metadata
and inactive optional-attribution wrappers. Imports/cache construction, warmup,
oracle, serialization, persistence and worker startup are outside the timer.
Release previous outputs and collect garbage before each measured call.
Disable collection only during the timed call and restore it immediately.

A separate fresh worker records one traced-allocation repeat per cell, using
tracemalloc around the same call after warmup. Current/peak traced bytes cover
allocations visible to tracemalloc; they are not RSS, total native memory or
incremental process memory. Instrumented elapsed times are never mixed with the
five timing samples. No threshold, speedup or optimization acceptance is defined.

Set the four plan thread variables to one in workers before imports. Record
platform, CPU, affinity where available, Python/import/distribution/source/native
identities, generator/helper/plan hashes, public closure identity and every
command/exit/failure. Freeze the tested driver/plan commit before timing. The
borrowed prefix and its editable PHMT source remain untouched; actual producer
version/source and helper location are explicit. No source-provider overlay.
Attribution activation is off in fresh workers; no tracking/enrichment/network
operation is part of the timed workload. Existing returned metadata remains.

Finish tests/builds before measurement. Workers run serially, with a 180-second
per-worker timeout. A timeout/exception/oracle/identity failure is retained as a
failed cell, never an omitted or zero-cost sample. Preserve all samples/order,
min/median/max spread and host/interference limits. This shared machine is not
reserved; no causal algorithmic-complexity inference or universal benchmark follows.

### Shared-machine execution amendment — 2026-11-05

Before any timing, the maintainer explicitly requires leaving RAM and processors
available for other uses. The frozen scientific plan remains unchanged. Run the
case under a standard user systemd scope: one allowed logical CPU, CPUQuota=100%,
MemoryMax=1 GiB, MemorySwapMax=0, TasksMax=32, nice=19 and idle I/O priority.
Keep the four plan thread limits and set NUMBA_NUM_THREADS/RAYON_NUM_THREADS=1.
Record the actual OS limits; an inability to enforce them is not a reason to
launch an unrestricted benchmark. Do not change or stop unrelated processes.

Before starting, require at least 4 GiB MemAvailable and no currently observed
full-memory stalls (Linux memory-pressure full avg10=0). Record remaining swap
and the longer pressure averages; these thresholds are conservative local
execution choices, not scientific acceptance or a general suite policy. Defer
measurement when admission fails. The complete scope includes the serial
controller and its worker, so combined cgroup-accounted memory stays bounded. A killed/
timed-out worker is a retained failure. No benchmark starts while own tests run.

## Acceptance and maintenance

Test the oracle on independent known geometry, non-default units, corrupted
geometry/choices/counts/inputs and budget/exclusion cases before timing. Add the
unshipped helper/plan to private installed-test support for the selected guard;
do not ship benchmark code as runtime or add a mandatory CI benchmark.

Publish original full results and checksum-qualified archive, linked summary and
one bounded computational case in the existing validation collection. Every
planned cell/mode must have an explicit outcome. Successful cells need stable
producer/input/native identities and passing independent checks. Report failures
without retuning the declaration. No benchmark output is a release/full-suite/
platform/public-artifact or biological qualification. Reassess after generator,
provider, instrumentation, workload or machine changes; retain earlier results.

## Executed baseline — 2026-11-05

Frozen helper/plan commit `d2fc819929a93fe0273c7b2b68e0ff9d27d708a2` executes
against unchanged borrowed PHMT source `9c163654375c5933be6400282105b89376f03578`
and the prior public dependency prefix. All 20 workers pass: 50 timing samples,
ten traced-allocation samples, 20 warmups and all 80 independent call checks.
Every source/provider/native identity, input-cache digest and unit-policy check
agrees. The [original receipt](evidence/cached_generation_scaling_20261105_summary.json)
and [computational case](../docs/content/validation/cached_generation_scaling.md)
retain every sample and narrower interpretation; no production optimization.

Resource admission observes about 8.3 GiB available RAM and zero full-memory
stalls over ten/60 seconds. Swap is nearly full and the longer pressure history
is retained; neither other processes nor host caches are modified. Effective
kernel proof confirms CPU affinity [19], quota one CPU, memory.max=1073741824,
memory.swap.max=0, pids.max=32, nice19 and idle I/O. Serial execution completes
in about 401 seconds of whole-controller wall time; that includes worker setup,
warmups, oracle, tracing and persistence, and is not a generator-call sample.

Twenty-four unique new guards pass across the 23-case final scope plus one
corrected normal-fixture case. The earlier provisional 24-case pass has 13
test-only unit-strip warnings; explicit dimensionless extraction removes them.
The next run correctly refuses a raw-list corrupted normal, so that fixture is
changed to a wrong unit-bearing normal to isolate geometric disagreement.
The final single case passes under the resource limits. Original attempts and
the private-staging module/directory-name assumption failure remain retained.
Only the test harness changes; the frozen workload/scientific answers and
production generator stay intact. Private support declares the helper/plan
through the unchanged shared stager (59 inputs); 23 distribution and the related
administrative checks pass. No new installed artifact/matrix claim follows.
