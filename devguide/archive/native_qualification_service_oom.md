---
summary: Replace an unsupported transient-service property while preserving native qualification bounds.
issue: uibcdf/pharmacophoremt#154
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: measured
area: [testing, resources]
guard: devtools/tests/test_feature_reuse_native_qualification.py::NativeQualificationTests::test_services_use_supported_group_oom_policy_and_owned_cleanup_root
normative: devguide/feature_reuse_measurement.md
blocked_by: []
supersedes: []
---

# Native qualification service assignment failure

The first manual run, 42460786720/attempt1 at cdb9d45, fails before service
admission: `Unknown assignment: MemoryOOMGroup=yes`. Binary setup succeeds;
environment creation and native tests do not execute. A secondary cleanup
ENOENT occurs because the private manager root does not yet exist. The original
[failure receipt](../evidence/feature_reuse_native_admission_failure_20261108.json)
retains exact run/job/source identities and local full-log hashes.

Use the documented
[OOMPolicy=kill](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html#OOMPolicy=)
to set the required memory.oom.group=1, instead of the unsupported assignment.
The client's actual kernel check and all memory/swap/CPU/task/time/pressure
bounds stay unchanged. Prepare only the owned temporary manager root before
binary installation so cleanup can operate after an early admission failure.
This fixes the PHMT caller; no systemd or shared-host change is needed.

The durable guard checks both actual service commands and owned-root creation
before the binary action, while retaining cleanup. Local guards establish the
reviewed correction, not real kernel admission. One newly reviewed exact-source
manual request must verify actual service entry; preserve the original failure
and never automatically redispatch an uncertain response. The separate
[recovery plan](../evidence/feature_reuse_native_qualification_recovery_plan_20261108.json)
retains the same scientific inputs and native budget. No private benchmark
snapshots, molecular pilot, performance or biological qualification follows.

## Actual corrected service receiving

At d95617d/run42461400749/attempt1 the bootstrap service enters successfully
with verified memory.max=2147483648, memory.swap.max=0, memory.oom.group=1,
pids.max=64 and one CPU/quota. Private-root and binary cleanup also pass. This
receives the caller correction; the native service is still not executed.

The later package transaction exhausts the unchanged bootstrap budget with
memory.max events, std::bad_alloc and a resource-unavailable thread message.
Dependency resolution completes; extraction fails. The whole run remains failed
and native tests remain skipped. The
[separate receipt](../evidence/feature_reuse_native_bootstrap_limit_20261108.json)
retains measured peaks, original source/run identities and uncertainty about
task-limit events. #148 owns a lower-concurrency acquisition investigation;
neither repeat the exhausted route nor increase its budget.
