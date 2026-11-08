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

### Serial acquisition limit received, 2026-11-08 UTC

[b1139d0/run42494894038/attempt1](evidence/feature_reuse_native_serial_limit_20261108.json)
is **failure**. Actual bootstrap controls and exact manager size/hash/version
verify, as do its effective extract_threads=1/download_threads=1 settings.
Resolution completes with 403 packages/rounded 1GB download, but extraction
still aborts with Resource temporarily unavailable. The SDK propagates SIGABRT/
exit1 and owned cleanup passes. All 87 native cases and their 512MiB scope remain
unexecuted; there is no provider/native-context or performance result.

Sampled kernel peak is 2166816768 bytes, tasks reach the declared 64 and
memory.max events reach 13920, with no kernel OOM kill or swap. Requested cap
and transiently overshooting observed peak remain distinct. Pids.events/final
lifetime peaks are not captured, so do not assign the exact failing resource
from task occupancy alone. Configuration recognition did not establish a bounded
total manager worker count or successful transaction.

Stop both exhausted profiles with this manager under these budgets. Hand the
actual controls and failures to MolSysSuite#108/infrastructure#1 for a distinct
reviewed acquisition strategy; do not enlarge budgets, repeat the profile or
substitute scientific inputs. Retain all three producers/run identities and raw
GHRR1.4 captures. Independent product work may continue; native admission, the
measured arm and original-input pilot remain pending.

### Serial acquisition prepared, 2026-11-08 UTC

The [separate fixed plan](evidence/feature_reuse_native_serial_acquisition_plan_20261108.json)
keeps every native/bootstrap budget, SDK/environment/source pin and original
scientific selector. Only manager acquisition concurrency changes: explicit
MAMBA_EXTRACT_THREADS=1/MAMBA_DOWNLOAD_THREADS=1, verified by the actual manager
before any installer. The client also checks the reviewed binary's size/hash
and version, then emits those actual bindings early enough to retain them after
a transaction failure. No alternative environment builder or solver is added.

All 46 focused administrative cases pass, including 21 admission guards.
Missing implicit settings, changed binary and effective default/malformed
configuration refuse work. The real consumer helper verifies the same official
1.5.10 binary/configuration using only metadata commands. These controls do not
qualify serial transaction resource use or native work. Publish/review the exact
source, inventory current handles and make at most one separately declared
request; retain both original failures and never increase the fixed budgets.

### Bootstrap admission and transaction limit, 2026-11-08 UTC

[Recovery 42461400749/attempt1](evidence/feature_reuse_native_bootstrap_limit_20261108.json)
at d95617d enters the own bootstrap service with verified 2GiB memory.max,
zero swap, memory.oom.group=1, 64 tasks and one CPU/quota. Low priorities and
declared numerical thread settings verify. Cleanup passes, resolving the
[#154 caller defect](archive/native_qualification_service_oom.md). The whole run
still fails; none of the 87 native cases or the 512MiB native scope executes.

Resolution completes with 403 packages/rounded 1GB download. During extraction,
memory.max events accompany std::bad_alloc and a resource-unavailable thread
message. Sampled cgroup peak is 2148343808 bytes, with at most 60 observed tasks,
no swap/OOM kill and ample host reserve. Requested kernel cap and transiently
overshooting observed peak remain distinct; sampled tasks do not establish a
final lifetime peak or pids-limit event, whose counter was not captured.
The client propagates failure; it does not acquire providers or reach context
checks. Actual manager hash/final installed identities remain unreceived.

Stop this exhausted acquisition route. Inspect supported exact-manager package
extraction/download concurrency and use the existing SDK/owner route for any
separately declared lower-consumption recovery. Do not enlarge budgets, replace
inputs/pins, transfer benchmark snapshots or manufacture a native/performance
result. The first admission failure and both complete GHRR captures retain their
own identities. The goal remains active through independent product work.

A separate local control verifies the checksum-published official Micromamba
1.5.10 binary (no environment creation or package operation). With rc files
disabled and only an owned root, its version/config commands report default
extract_threads=0/download_threads=5, then both settings equal one when their
MAMBA_EXTRACT_THREADS/MAMBA_DOWNLOAD_THREADS variables are explicit. This
qualifies recognition of settings, not lower-memory transaction behavior.
Implement/guard that fixed consumer configuration through the same SDK before
prospectively admitting a new bounded acquisition; keep budgets/pins unchanged.

### First native route attempt and correction, 2026-11-08 UTC

The first exact-source request at cdb9d45 is received as
[42460786720/attempt1, failure](evidence/feature_reuse_native_admission_failure_20261108.json).
Service creation rejects the caller's unsupported MemoryOOMGroup assignment;
the native step is skipped. The private manager root is still absent, causing
a separate post-cleanup ENOENT. No service/client admission, environment
acquisition, native fixture, pilot or timing is received. Original GHRR1.4
metadata/full captures and native job facts remain local. The generic compact
report names cleanup; bounded native step6 evidence establishes the primary cause.

[#154](archive/native_qualification_service_oom.md) replaces the assignment
with documented OOMPolicy=kill, which sets memory.oom.group=1, and creates only
the owned temporary manager root before setup. The actual kernel check and
every phase budget/source pin/scientific selector remain unchanged. Its durable
guard checks both actual service commands and cleanup preparation. The
[separate prospective recovery](evidence/feature_reuse_native_qualification_recovery_plan_20261108.json)
preserves the first declaration and failed producer. Publish/review its exact
source before at most one new request; observe the actual handle after an
uncertain response. That declaration preceded the recovery received above.
Recovery passes 42 focused administrative cases, including 17 admission guards,
three reporting cases and full Ruff/index checks under the unchanged local
512MiB DATA limit (whole-command child peak 67534848 bytes). These are controls,
not native or molecular-performance evidence.

### Native fixture admission prepared, 2026-11-08 UTC

The fixed [manual workflow](../.github/workflows/feature_reuse_native_qualification.yaml)
and unshipped [receiving client](../devtools/feature_reuse_native_qualification.py)
now implement the next boundary: acquire the existing ci-3.14 environment with
the pinned common SDK/source inputs, then execute all87original public-fixture
guards inside a new verified512MiB/zero-swap/32-task/one-CPU service. Its
[prospective plan](evidence/feature_reuse_native_qualification_plan_20261108.json)
keeps acquisition separate at2GiB/64tasks/oneCPU, with finite30minute versus
180second lifetimes. Both use low priorities, one backend/build thread, actual
kernel checks and five-second own-work monitoring. Pressure stops only owned
descendants. This is fixed case orchestration using standard OS tools, not an
arbitrary-command executor or a PHMT infrastructure API.

The reviewed Micromamba action installs only its1.5.10-0binary. The existing
MolSysSuite environment helper owns creation; configured strict channels are
separate from unsupported exclusive-channel qualification. The same seven Git
pins and SDK1c248b6 remain. Actual prefix/context/pip checks precede the native
phase, whose worker reuses the exact original OS probe, verifies installed native
artifact/source bindings and requires87passed/zero skipped or failed cases.
No original benchmark snapshot is submitted; ordinary public checkout retains
its existing fixtures. The measured arm, private-input pilot and timing remain
unimplemented/unexecuted by this preparation.

The [local receipt](evidence/feature_reuse_native_preparation_20261108.json)
retains154passing administrative cases,16offline admission guards within that
suite, full Ruff430/index/declaration checks and original failures. It resolves
the route-inventory omission#151 and wide-CSV memory defect#152 without increasing
the local512MiB limit, reducing data or changing scientific definitions. Source
cohort/exclusion/population/ambiguity metadata remain exactly archived. SQLite
warnings remain open under#153. Actual hosted native receiving is still pending;
neither local controls nor the earlier OS smoke qualify it.

### Hosted scope probe, declared 2026-11-08 UTC

The [prospective recovery declaration](https://github.com/uibcdf/pharmacophoremt/issues/148#issuecomment-6717982897)
now has one manual-only [workflow](../.github/workflows/feature_reuse_resource_probe.yaml)
and a [fixed probe plan](evidence/feature_reuse_resource_probe_plan_20261108.json).
The declaration preceded execution; terminal receiving is recorded below.
GitHub documents a
[fresh VM per configured job](https://docs.github.com/en/actions/how-tos/manage-runners/github-hosted-runners/use-github-hosted-runners).
This case invokes standard systemd-run only on that job's VM. It requests an own
short-lived unprivileged service with the same512MiB aggregate/zero-swap/32-task/
one-CPU budget, actual affinity, nice19/idleI/O and one backend thread. It must
verify its own kernel controls and child membership before a fixed24MiB
two-process smoke. Requested properties alone do not qualify enforcement.

The standard [systemd resource controls](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html)
own enforcement. This workflow is a case-specific boundary check, with no PHMT
executor/resource API or changes to the shared workstation. It imports no
molecular library and submits none of the declared benchmark's original
snapshots or molecular result bodies. Local shell/YAML/
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

The [terminal receipt](evidence/feature_reuse_resource_probe_20261108.json) now
receives exact9a0ed14/run42453432613/attempt1, with the native required step and
all job steps successful. Actual Ubuntu26.04/systemd259/Python3.14.10 observes
kernel memory.max536870912, memory.swap.max0, pids.max32 and cpu.max100000/100000.
Worker and child run as the job user in the same own service with actual CPU3,
nice19/idleI/O; DATA/AS are unlimited inside the aggregate512MiB cgroup. This is
a different controlled context, not a retry or repair of the original local
DATA512/OpenMM failure. No shared-workstation service is created.

The fixed16+8MiB page-touched payloads pass. Cumulative kernel peak at both
held-payload samples is38203392bytes, with two actual tasks, no memory-limit/OOM
events, zero observed swap activity/PSI and the declared RAM reserve/margin.
This is not final unit-lifetime peak, process RSS, stress or molecular performance.
Published GH Run Receptor1.4.0 full capture and offline replay pass; original
native API/log/control facts are retained locally, with reviewed scalars/hashes
published. Every later job needs its own admission; no declared benchmark input
has been submitted.
Next prepare the exact-provider/input-delivery decision and shared scientific arm
for a qualified molecular context before considering the declared pilot.
Publication review narrows the initial unpublished transfer wording: ordinary
checkout includes the existing public ERalpha H5MSM fixture; none of the three
original benchmark snapshots is submitted. The original projection and correction
remain local, without rerunning or changing the native control observations.

The [accumulated full source checkpoint](plan_api_ci_checkpoint.md) subsequently
receives27c1178/42451906584/attempt1:2505full-suite cases pass in all eight
Linux/macOS arm64 Python3.11–3.14cells, including the22offline declaration guards
and existing native fixture controls. It verifies those functional routes with
the pinned CI providers, not a512MiB native execution or the held local-provider
context. Before a shared measured arm, qualify the unchanged87public-fixture
native controls inside a newly verified512MiB scope with pinned bootstrap/provider
provenance. These controls are not a replacement for the declared original-input
two-arm pilot or timed schedule; all original snapshot restrictions remain.

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
