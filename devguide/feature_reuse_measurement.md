# Molecular feature-reuse measurement declaration

Owners LMMV/dprada; 2026-11-08 UTC;
[#148](https://github.com/uibcdf/pharmacophoremt/issues/148), within #108/#95.
This is a prospective computational experiment, **not an executed benchmark**.
The existing [native equality experiment](feature_inventory_reuse.md) retains
its original producer, six comparisons and limits. Its request counts and
whole-command duration do not establish a speed improvement.

## Fixed workload and offline control

The [declaration](evidence/feature_reuse_profile_plan_20261108.json) fixes three
original PubChem H5MSM snapshots and their hashes, the same two reference
geometries, explicit acceptor family, selection/frame/state and original native
settings. Four workloads distinguish one caffeine query, one aspirin query,
two mixed queries and eight alternating requests. The eight requests reuse two
geometries; they are not eight independent queries or molecules.

Each source/workload has four repeats. Fresh/reused order alternates by repeat,
with each arm first twice in every stratum. The complete schedule contains
48 pairs / 96 serial fresh-process arms and144 query requests per arm across
all strata. A separate two-process CID2244/two-mixed admission pilot must exercise
positive fitting and equivalent native outputs; it is outside those samples.
There are98 prospective arm processes including that pilot, not98 measurements.

[`devtools.feature_reuse_plan`](../devtools/feature_reuse_plan.py) regenerates and
checks this **fixed declaration** using only the standard library. It rejects
omitted/reordered cases, altered scientific settings or budgets and inserted
result claims. Optional file verification streams all three original snapshots
without decoding molecular contents, fetching data or importing scientific tools.
A relocated snapshot root is explicit and still requires the exact frozen bytes.
It neither launches the prospective commands nor admits an execution route.

```bash
python -B -m devtools.feature_reuse_plan --check devguide/evidence/feature_reuse_profile_plan_20261108.json
python -B -m devtools.feature_reuse_plan --check devguide/evidence/feature_reuse_profile_plan_20261108.json --verify-inputs
```

The second command requires the original local files. Use
`--snapshot-root ROOT` only with `--verify-inputs` for
`ROOT/cid-<CID>/prepared.h5msm`. Missing or changed files fail without acquisition
or creating a replacement. Writing a new declaration uses exclusive creation;
it cannot overwrite an existing plan. A checked declaration is not measured
performance or an execution permission.

## Equivalent scientific work and timing boundary

The future native driver must reuse the existing public feature extraction,
correspondence, placement, query construction, PoseEvaluator and score operations.
Native post-fit re-extraction/geometry checks stay inside both measured arms.
First canonical mapping only, proposal-family completion, omitted mappings and
checked-pose outcomes retain the original experiment's separate meanings. The
cross-reference omitted prefixes cannot become compound negatives.

Imports, snapshot loading and reference-inventory construction precede algorithm
timing; retain their costs separately and record whole-command time. Within each
fresh arm, each query includes source extraction. Within each reused arm, time
one inventory build, then charge it to the complete build-plus-queries total.
Record wall and process CPU nanoseconds for extraction, complete queries and
the total. Report the first request separately from subsequent requests. No
molecular warmup occurs inside the measured arm; a new process does not imply
a cold OS cache. Never flush machine caches.

Both arms retain the same complete detached native evidence. Cross-arm equality,
input/reference/inventory immutability verification and output hashing/writing
are outside the measured intervals; native validation is part of the operation.
Use the same explicit disabled optional attribution capture while timing, then
receive actual reached citations in a separate untimed application-owned session.
Do not infer missing provenance from capture being disabled.

Retain every planned sample, elapsed interval, failed process and incomplete
pair. Report descriptive median/min/max and all four raw paired observations
per source/workload, including order. A timing ratio requires scientifically
equal completed work; missing arms, truncated work or changed answers remain
visible in the complete denominator. A no-benefit or noisy result is valid;
there is no required speed threshold or population-level inference.

Record whole-process RSS and managed aggregate memory peak with distinct scopes.
Neither is incremental inventory allocation. Detached inventory JSON byte count
is a logical payload size, not persistent index/storage or memory-capacity proof.
Three small fixed conformers do not qualify large-library capacity or a general
amortization threshold. A later representative collection is a separate case.

## Execution admission and current disposition

The native measurement driver is **not implemented or qualified** by this
declaration increment. Actual provider/source/native identities must be verified
at admission; the old equality run's identity is not silently transferred to a
new process. Implement/reuse one scientific arm only after its appropriate
native verification route is available. Do not duplicate a fitter, matcher,
quantity decoder or provider geometry in this consumer.

The old equality run enforced512MiB aggregate cgroup memory, zero swap,32 tasks,
one CPU/quota, one backend thread and low priorities. The current process lacks
its own user bus; it must not borrow another user's scope. No container runtime
is installed. The latest [scheduler observation](https://github.com/uibcdf/uibcdf-infrastructure/issues/1#issuecomment-6716427494)
found an UP controller but no usable allocation: the local node was invalid
because configured memory exceeded reported memory; other nodes were unknown.
This is dated observation, not a permanent scheduler diagnosis or reservation.

Source inspection shows placement's public MolSysMT least_rmsd_fit calls rotate
and translate on coordinate quantities. That reaches the same native form/import
route implicated in the retained DATA512MiB/OpenMM mapping failure under #146.
The exhausted original case stays failed. Repeating it with the same limit,
silently raising that limit, skipping positive fits or using an empty-only
workload cannot qualify this benchmark. No native pilot or timing is launched.

Before the pilot, receive a usable scheduler allocation or owned managed memory
scope with the declared512MiB/zero-swap/32-task/one-CPU limits. Verify actual
enforcement, provider/native identity, remaining RAM after at least20%physical
reserve plus the complete own task budget, CPU/load, swap activity and PSI.
Monitor own work, retain partial output and stop it on significant pressure.
Reassess each process; free capacity is not a reservation. Do not configure the
host, change other sessions or implement a PHMT resource-management platform.
Mechanisms remain [infrastructure#1](https://github.com/uibcdf/uibcdf-infrastructure/issues/1)-owned;
execution architecture remains [MolI#96](https://github.com/uibcdf/moli/issues/96)-owned.

## Evidence and continuation

### Hosted scope probe, declared 2026-11-08 UTC

The [prospective recovery declaration](https://github.com/uibcdf/pharmacophoremt/issues/148#issuecomment-6717982897)
now has one manual-only [workflow](../.github/workflows/feature_reuse_resource_probe.yaml)
and a [fixed probe plan](evidence/feature_reuse_resource_probe_plan_20261108.json).
No hosted probe has yet been received. GitHub documents a
[fresh VM per configured job](https://docs.github.com/en/actions/how-tos/manage-runners/github-hosted-runners/use-github-hosted-runners).
This case invokes standard systemd-run only on that job's VM. It requests an own
short-lived unprivileged service with the same512MiB aggregate/zero-swap/32-task/
one-CPU budget, actual affinity, nice19/idleI/O and one backend thread. It must
verify its own kernel controls and child membership before a fixed24MiB
two-process smoke. Requested properties alone do not qualify enforcement.

The standard [systemd resource controls](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html)
own enforcement. This workflow is a case-specific boundary check, with no PHMT
executor/resource API or changes to the shared workstation. It imports no
molecular library and transfers no source/native/H5MSM payload. Local shell/YAML/
three-Python-body syntax and inline lint checks pass. Two initial import-spacing
failures are retained; entry/child ASTs are unchanged, and the parent differs
only in nested child-source whitespace. It does not run a
native driver, pilot or timing schedule. Support-library scientific/quantity/
public-argument boundaries are absent from this OS-only check.

Receive the actual exact-head run and native control output before accepting even
this bounded route. Missing/ineffective limits fail closed. Successful controls
would qualify only that observed hosted context and small smoke; every molecular
job still needs new admission, exact provider/native/input identity and the
separate declared pilot. Before remote molecular work, establish an authorized
delivery route for the exact frozen inputs under their original restrictions.
The current local route and original DATA failure retain their own dispositions.

The [declaration receiving receipt](evidence/feature_reuse_profile_declaration_20261108_summary.json)
records focused offline guards, actual input
hash verification and reporting/lint checks. These establish declaration and
integrity mechanics only. No molecular calculation, provider/prefix update,
performance claim, installed/public qualification or release follows. Full
native geometry-bearing outputs and H5MSM bodies stay local under their original
publication restrictions; published records contain owned controls and scalar
projections only.

Next receive a safe native execution route and qualify one shared scientific arm,
then run the declared pilot before considering the full schedule. While that
route is unavailable, continue independent public-workflow/source-operation
coverage work under #108, rather than repeatedly probing an exhausted native
case. Preserve #147's full-source debt and the source/public/provider, biological
and supported installed-platform gates of the mature0.x staircase.
