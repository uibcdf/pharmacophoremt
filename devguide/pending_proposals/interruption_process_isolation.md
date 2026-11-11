---
summary: Qualify interruption guards without forking from a threaded test parent.
issue: uibcdf/pharmacophoremt#192
status: active
opened: 2026-11-11
closed:
verification: measured
area: [testing, execution]
guard: tests/test_driver_checkpoints.py
normative: devguide/interruption_process_isolation.md
blocked_by: []
supersedes: []
---

# Interruption-test process isolation

The completed [0.5.0 source receipt](../evidence/release_050_candidate_qualification_20261111.json)
receives 3,088 passing cases in every supported source cell. Python 3.12–3.14
emit 17 standard threaded-parent fork deprecations per cell; Python 3.11 does
not emit those warnings. No deadlock was observed. The warnings remain visible.

Before selecting spawn, forkserver or an explicit fresh-process fixture, identify
the inherited state required by the existing #183/#186/#187 interruption guards.
Preserve actual committed-prefix, before/after-publication, ownership, original
attribution and unknown-work assertions. Bound shutdown/wait behavior and kill
only owned children. Do not weaken or replace interruption with a mocked return.

Acceptance requires equivalent real interruption/recovery controls on affected
Python minors and Linux/macOS. This is follow-up test infrastructure for 0.6.0,
not a production multiprocessing feature or a generic thread/fork safety claim.
No isolation implementation or new execution was performed by this report.

## Implemented source increment — 2026-11-11 UTC

The later [isolation contract](../interruption_process_isolation.md) selects fresh
spawned children and retains all original committed-prefix/publication/credit
assertions. A real live-parent-thread lease probe also passes. All 103 source
controls pass on Linux/Python 3.14 with DeprecationWarning treated as error.
The former paragraph records the original proposal state. Exact owned receiving
and full supported Linux/macOS/minor gates are recorded separately; this report
stays active until its required platform receiving is completed.

The [combined receipt](../evidence/native_feature_reconstruction_20261111.json)
now receives the same 103 isolation/store/workflow cases in the exact owned wheel,
with the public PyUnitWizard 0.28.1 lower bound and no source fallback. All 271
selected source and owned cases pass with deprecations treated as errors. The
first owned launcher recursively prepared the harness during spawn; its original
17 failures are retained, and a guarded launcher passes with the same wheel and
unchanged resource limits. Supported hosted Linux/macOS/minor receiving remains
pending under #9/#192; no universal multiprocessing-safety claim follows.

## Supported-source checkpoint requested — 2026-11-11 UTC

Source47669463e8047f33c77537c5d7e010199cb411fd has one complete unchanged-matrix
request under [the declared checkpoint](../source_0_6_0_checkpoint.md):
source 43084105668/attempt 1. Actual [native receiving](../evidence/source_060_pending_20261111.json)
after approximately 20minutes still finds every scientific cell queued, with no
assigned runner. The 3,388-case inventory is collect-only, not platform execution;
no closure or replacement of the original source/owned evidence follows. Observe
the original handle and assess actual terminal counts/warnings/guards on every
supported minor and Linux/macOS. #192 remains partial until that receiving.

Later native job readback at 19:33 UTC starts macOS/Python 3.14; ten other required
jobs remain queued. Preserve the earlier queued observation and original handles;
this transition is not a passing scientific/complete-source gate.
