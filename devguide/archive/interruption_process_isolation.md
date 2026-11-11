---
summary: Qualify interruption guards without forking from a threaded test parent.
issue: uibcdf/pharmacophoremt#192
status: resolved
opened: 2026-11-11
closed: 2026-11-11
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

## First supported source cell received — 2026-11-11 UTC

[Partial exact-source receipt](../evidence/source_060_partial_20261111.json)
verifies macOS arm64/Python 3.14.10 at 4766946: all 3,388 cases pass with no skips,
48 retained warnings and 127 qualified coverage paths. Its warning table contains
no DeprecationWarning and no controlled threaded-parent fork deprecation.
Preflight/install/import/architecture/full-command/coverage and original log
identities are verified. The other seven cells and required control workflows
remain unreceived; #192 stays active until complete supported receiving. This
single cell does not establish general thread/fork safety or public delivery.

## Three source cells and control gates received — 2026-11-11 UTC

The [resumed receipt](../evidence/source_060_resume_20261111.json) adds original
macOS/Python3.13 and Linux/Python3.14 job captures:3,388 passes/zero skips/48
warnings/127 qualified XML paths each, with no controlled fork deprecation.
Conformance and publication controls pass their required native steps. Five
scientific cells remain unreceived; this report stays active. Original source,
attempts and pending snapshots remain intact. Later7192041's argument controls
have independent full-source debt and do not alter this process-isolation scope.

## Corrected-source receiving pending — 2026-11-11 UTC

The original4766946 matrix cannot qualify the supported scope: macOS/Python3.11
fails a redundant second MolSysMT acquisition before tests. Its partial qualified
cells and actual warning observations remain original. The #197 route correction
is published at c5e952c with the same interruption assertions. Its
[independent receiving](../evidence/source_060_recovery_pending_20261111.json)
verifies source43109007084/attempt1: eight science cells in progress, reporting
success and both separate control workflows successful. This report stays active
until actual terminal supported-minor/platform counts/warnings/coverage receiving;
neither collection nor metadata success establishes interruption-test acceptance.

## Five corrected-source cells qualified — 2026-11-11 UTC

[Job-only receiving](../evidence/source_060_recovery_partial_20261111.json)
verifies c5e952c/43109007084/attempt1 on Linux/Python3.11/3.13/3.14 and
macOS/Python3.13/3.14:3420passes/0skips/48warnings/127qualified XML paths each.
All original interruption assertions remain in the full suite; no controlled fork
deprecation or DeprecationWarning is observed in these five warning tables.
At23:01UTC seven native jobs succeed, with macOS3.11 still running; both3.12
native successes still need qualified XML receiving. Keep this report active
until the complete supported scope is received. Original43084105668 terminates
with its acquisition failure; its successful subset cannot close this report.

## Resolved with complete corrected-source receiving — 2026-11-11 UTC

The [terminal receipt](../evidence/source_060_recovery_checkpoint_qualification_20261111.json)
accepts frozen c5e952cd3a1fe5b452be6fccbf85d2fb64c3f1eb, source43109007084/attempt1:
all eight Linux x86_64/macOS arm64 × Python3.11–3.14 cells execute the unchanged
full command and pass3420cases/0skips, retaining48warnings/127qualified XML paths
each. Required acquisition/preflight/install/import/architecture/coverage and
reporting3/18/9/161, frozen-policy43109015680 and publication-controls43109024769
verify successfully. All original failed/pending/partial receipts remain intact.

All eight native warning tables contain no DeprecationWarning or controlled
threaded-parent fork deprecation. The durable driver guard starts real spawned
children, interrupts actual native progress and checks original committed-prefix/
credit recovery; the separate store/workflow and live-parent-thread lease controls
remain in the full suite. This closes the declared supported interruption-test
scope, not generic process/thread safety or an installed/public platform promise.

No original job is rerun/cancelled. Later receiving heads, full supported
installed/public qualification, version/tag/publication and other scientific
workstreams retain separate gates. Original4766946 remains terminal failure.
