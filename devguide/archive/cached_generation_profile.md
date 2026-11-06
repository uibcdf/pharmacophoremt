---
summary: Profile fixed-work cached generation and hand generic costs to their owners.
issue: uibcdf/pharmacophoremt#98
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: measured
area: [performance, validation]
guard: tests/test_cached_generation_scaling.py
normative: devguide/cached_generation_profile_protocol.md
blocked_by: []
supersedes: []
---

# Fixed-work cached-generation profile

## What and evidence

Following #97, frozen driver `80efdc5` profiles only the original budget 32 case:
two donors/two rings, 32 of 64 models, four sites, no exclusions or molecules.
One warmup, one cProfile call and two controls preserve every native model/report/
metadata field, independent geometry/order/coverage, input cache, unit policy
and producer/provider/native identity. No production or provider change.
[Protocol](../cached_generation_profile_protocol.md) and
[original receipt](../evidence/cached_generation_profile_20261105_summary.json)
retain full payloads, raw/JSON pstats, sources, reproductions and resource proof.

## Interpretation and ownership

The 9.357 s instrumented call reaches 22,672 quantity tests and 17,792 normal
probe-miss events. The probe-miss branch takes 6.116 s cumulative; nested catalog
configuration/path resolution accounts for 17,792 realpath/213,504 lstat calls.
Controls take 4.669/4.620 s; no speedup is measured and cumulative rows are not
additive shares. Two independent provider-only 100-call reproductions confirm
the repeated work without PHMT/molecular inputs. Current immutable source
inspection finds the same mechanism, with no current-main execution claim.

Generic quantity-probe behavior belongs to PyUnitWizard #141; warmed provider
registration belongs to SMonitor #63. The supported mechanism/compatibility is
theirs to decide. PHMT adds no local quantity detector, private provider patch,
global diagnostic suppression, scientific change or unqualified floor.

## Guard, resources and closeout

The existing independent mixed-radix guard protects geometry/roles/units/
coverage and malformed-output detection; the profile additionally asserts full
native payload/metadata identity across128 model exports and all four reports.
Existing #97 tests remain dated evidence; they are not claimed as new reruns.
The initial resource check refuses pressure. Later admitted execution uses one
CPU/1 GiB/no swap/nice=19/idle I/O with six thread limits and a 180 s scope bound.
The two small provider reproductions retain similarly bounded execution.
No other process, borrowed prefix/source or original #97 evidence is modified.

The bounded profile/owning-provider handoff is complete; no optimization or
provider adoption is claimed. Receive a supported answer/delivery and compare
this exact work before any adoption. These proposals do not add a 0.5.0 release
gate; #95/#9/#10/#23 retain their independent scope. No package/tag/Release,
new public installation, biological result or addon work.
