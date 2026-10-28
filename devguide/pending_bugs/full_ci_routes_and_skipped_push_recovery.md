---
summary: Complete contributor full-CI routes and skipped-push recovery.
issue: uibcdf/pharmacophoremt#9
status: partial
opened: 2026-09-30
closed:
severity: medium
verification: measured
area: [governance, ci]
guard: tests/test_ci_backlog.py
normative:
blocked_by: []
supersedes: []
---

# Full-CI contributor routes and skipped-push recovery

## Terminal receiving of the previously pending runs — 2026-10-28

The [new native observation](../evidence/ci_receiving_20261028.json) preserves
the earlier pending snapshot and verifies terminal outcomes. Pool-2 closeout
`8e83a64` CI 40388775895 passes all eight actual Linux/macOS Python 3.11–3.14
test cells. Scheduled 40353440186 attempt 2 succeeds; its retried macOS/Python
3.13 job 121791848676 completes Run tests successfully. The original attempt-1
ambermd timeout remains unchanged, separately retained failure evidence.

Published governance source `9eb6787` CI 40612031912 also passes all eight actual
test cells; policy 40612032102 and Conda governance 40612032124 succeed. Later
nightly 40711753014 succeeds in governance/decision and intentionally omits the
scientific matrix. No matrix is inferred from that decision-only success, and
none of these historical runs qualifies a later changed head or public artifact.
#9 remains partial for its broader original acceptance scope.

## Exact-source receiving and later scheduled infrastructure failure — 2026-10-26

59c98d63999accab0decbc5edfed1287fb4480ba original push CI 40150094066 now
verifies governance and all eight actual Linux/macOS Python 3.11–3.14 test
steps successful; policy 40150094121 and Conda governance 40150094315 also
succeed. The [native observation](../evidence/ci_receiving_20261026.json)
retains job/test-step identity separately from later scheduled failures.

Scheduled run 40353440186 attempt 1 at the same source fails overall: macOS/
Python 3.13 cannot download ambermd/noarch/repodata.json.zst (libmamba error 28,
low-transfer timeout), and no tests run in that cell. Cleanup then reports a
missing micromamba-shell. The other seven science jobs and governance passed.
The original raw job log remains at `/tmp/phmt-ci-40353440186-macos313.log`,
with identity in the observation. No scientific failure is reproduced here.

Native `gh run rerun --failed` requests attempt 2 without changing workflow,
channels, pins or scientific code. It remains in progress at observation and
cannot be called successful from the earlier green run. New pool-2 source and
closeout commits require their own receiving; installed/public claims stay
separate. This existing issue remains partial for its broader original scope.

Later native observation of attempt 2: macOS/Python 3.13 job 121791848676 has
successfully completed Setup conda env and is executing Run tests. This confirms
the reattempt passed the earlier metadata-download point, not that the run is
already green. Pool-2 local source controls subsequently pass 62 tests / 56
subtests; their final pushed head still needs independent hosted receiving.

## What

Implement uibcdf/molsyssuite#39 in PharmacophoreMT. At d0215fa, main is
unprotected and no conditional daily recovery exists for authorized internal
skip-CI pushes. Complete unfiltered push/PR and weekly/manual CI already cover
Python 3.11–3.13 on Linux/macOS, with an independent reporting job.

## How

Retain unfiltered complete push/PR collection and each minor-specific Conda
environment, controlled suite source revision and separately tested MolSysMT
source pin. Pin macOS to macos-15 and assert arm64 and each Python minor.
Retain the independent Reporting governance check and its standard-library
report/index validation; add backlog/route guards using independent pip tools.
Only that new tool bootstrap uses published pytest-receptor 1.0.0; scientific
Conda pytest-receptor 0.6.0 and all science commands stay unchanged.

Keep unconditional weekly Monday 09:00 UTC/manual complete execution. Add
conditional daily recovery at 02:07 America/Mexico_City and a typed
probe_backlog=true dispatch that omits heavy jobs. Uncertain history/API
results run the complete matrix; a failed decision job also runs full coverage.
Protect main with explicit PRs, zero mandatory approvals and eight strict
checks: existing Reporting governance, policy / conformance (including Ruff),
and six supported full test jobs. dprada/LMMV retain administrative direct pushes.

A debt watermark requires a successful ancestral main push/schedule/manual
run with all three supported Linux jobs and their successful actual Run tests
steps. PRs, other branches, probes, failed runs and skipped tests cannot clear
skipped commits. The detector filters main locally in unfiltered API listings.
Skipped commits remain due across ordinary commits and calendar boundaries.

## Why

External integration needs complete required coverage; internal iteration
keeps direct pushes and explicit skip-CI without repeated full matrices at
every step. Historical green science does not discharge newer skipped commits.
Governance remains independently testable during early component development.

## What is measured and what is assumed

Fresh API lists main unprotected and only dprada/LMMV, both admins. GH Run
Receptor 1.0.0 preserved success for weekly CI 36457546833 at 98ecb45;
native job/step metadata confirms all six actual Run tests steps succeeded,
plus independent reporting. No installed-artifact/platform support claim is
inferred. The new route guard first failed against old workflow_dispatch,
which had no probe input, before the implementation.

## Alternatives and refuted paths

A successful administrative probe cannot certify full science or clear debt.
Looking only at today's commits loses unpaid earlier skips. Weakening full
pytest selection or tolerating failing cells would hide component results.
No new bounded-smoke exception is needed for the existing full routine lane.

## Scope and exclusions

CI routing, debt guards, architecture evidence, protection and reporting only.
Science implementation, assertions, source/environment pins, releases and
support range remain component-owned. Ecosystem adoption remains separately
tracked in uibcdf/pharmacophoremt#6; existing SMonitor rendering defect remains
uibcdf/pharmacophoremt#2. Core MolSysMT/MolSysViewer science reviews are deferred
at the user's direction.

## Acceptance criteria

- Verify explicit PRs, strict checks and internal administrative bypass.
- Run independent hosted governance/probes and retain debt after skipped pushes.
- Observe the complete supported source matrix and preserve actual outcomes;
  the current contract has eight Linux/macOS Python 3.11–3.14 cells.
- Observe actual daily recovery and hosted external PR execution before adoption.
- Review publication-platform claims separately.
- Retain tests/test_ci_backlog.py and tests/test_ci_routes.py as durable guards.

## Provenance

2026-09-30; isolated clone based on d0215fa, preserving original worktrees.
Hosted weekly baseline: https://github.com/uibcdf/pharmacophoremt/actions/runs/36457546833.
New implementation execution/protection evidence is recorded below when observed.

## Local implementation verification

Eight administrative tests passed with Python 3.13 and pytest-receptor llm;
the required standard-library reporting invocation also passed three tests.
Ruff lint/format, report-index validation and central component conformance
passed. The full scientific test selection and all dependency/source pins
are unchanged. The PR/recovery route guard failed before the fix and passed
after it. Hosted execution and protection are recorded below after publication.

## Hosted governance and first backlog evidence

Source efc27e3 was published through the authorized internal skip-CI route.
GitHub reported bypass of the explicit PR rule and all eight required checks.
Protection API confirms strict checks, zero mandatory PR approvals, admin
exemption, and no force pushes/deletions.

Probe [36764937398](https://github.com/uibcdf/pharmacophoremt/actions/runs/36764937398)
passed both independent Reporting governance and the detector; native steps
confirm reporting/index checks and all CI guards actually succeeded. It
recognized the executed weekly 98ecb45 full matrix and found exactly two
pending skipped commits: d0215fa (guide distribution) and efc27e3 (this
implementation). Heavy jobs were intentionally omitted. Probe success did
not erase these skips. Suite policy (including Ruff)
[36764942903](https://github.com/uibcdf/pharmacophoremt/actions/runs/36764942903)
passed at the same source.

The issue and review remain partial. Actual daily execution, hosted external
PR execution and installed-artifact/publication-platform claims remain
unreviewed. A complete manual lane and post-run debt probe will be dispatched
on the published record revision; their actual evidence belongs in the owning
issue and the central adoption record. Scientific outcomes are preserved and
no successful complete result is assumed.

## Independent receiving checkpoint — 2026-10-09

The September implementation observations above retain their three-minor
scope. Current published source is `95487103a4ad5e97971c93ae97bc85484872705c`.
[Push CI 37977232408](https://github.com/uibcdf/pharmacophoremt/actions/runs/37977232408)
independently verifies all nine required executed source/reporting jobs:
eight Linux/macOS arm64 Python 3.11–3.14 cells plus Reporting governance.
Every context/dependency preflight, installation, import, interpreter/architecture
and full-test step passes; both 3.14 representatives report 626 passed. Its
daily/probe-only detector is intentionally inapplicable/skipped, not executed
recovery evidence. Exact-source policy and Conda controls also pass.

Actual daily schedule
[37950055123](https://github.com/uibcdf/pharmacophoremt/actions/runs/37950055123)
at `2132fa0ba6013b9adaf4615e1d055a1899f86cd6` independently verifies the
executed detector and Reporting governance. Its original detector log reports
zero skipped commits since full source `2132fa0`; the full matrix is intentionally
omitted. This resolves the actual daily observation gap, without counting the
omitted matrix as tests or asserting anything about later debt.

PR [37578072679](https://github.com/uibcdf/pharmacophoremt/actions/runs/37578072679)
at `7326f47aa7406268905e11d857b0f4ae0940c2af` retains overall **cancelled**
status. Native selected-job verification observes success in all eight then-current
source cells and Reporting governance, including executed full tests and
architecture assertions. That older PR predates the new dependency preflight;
its successful selected jobs are neither a complete accepted PR gate nor evidence
for those later operations. PRs and cancelled runs cannot become debt watermarks.
The current complete accepted PR observation therefore remains pending.

Fresh protection retains **ten** strict checks: eight full source cells, Reporting
governance and policy conformance. PRs require zero approvals; the only listed
collaborators `dprada` and `LMMV` remain administrators with direct-push bypass.
No setting is changed. Current unfiltered push/PR routing, matrices and recovery
match helper-adoption `448e47e`; the sole workflow delta adds independent
evidence-archive reporting tests and its reviewed inventory hash.

#9 remains partial for an accepted current PR and independent installed/public
platform review alongside #10/#23. No new scientific suite dispatch, release,
package operation, provider pin, support badge or science implementation changes.
This documentary checkpoint uses scoped reporting/index guards and exact-head
manual administrative gates. Its CI skip retains full-suite debt under this
issue and unchanged daily/weekly/manual recovery; administrative checks do not
clear that debt. Central receipt:
`uibcdf/molsyssuite:devguide/rollouts/pharmacophoremt_ci_receiving_39_45_20261009.json`.

## Weekly failure diagnosis — 2026-10-20

Weekly [39283601619](https://github.com/uibcdf/pharmacophoremt/actions/runs/39283601619),
attempt 1 at `a1ea9cc4025fefdbff5e30f3ecced2bcdfacd83d`, succeeds in seven
scientific cells. macOS 15 / Python 3.13 fails before tests while cloning the
unchanged pinned MolSysMT source: `curl 56` receive timeout, early EOF and an
invalid index-pack result. The [native-log excerpt and identity](../evidence/ci_failure_20261019_review.json)
retain the actual failure without changing scientific inputs or tests.

Daily [39431023758](https://github.com/uibcdf/pharmacophoremt/actions/runs/39431023758)
passes its reporting/backlog selection with science skipped. It is not a full
green matrix. Earlier [38440541291](https://github.com/uibcdf/pharmacophoremt/actions/runs/38440541291)
at `f0d96ae` separately retains eight successful source cells. New source and
installed-artifact evidence must remain bound to their own revisions and runs.

### Complete implementation source matrix — 2026-10-20

The authorized internal direct push at
`636373d3c5c24a1eff6d2bec5f3eceb6ce018ba4` completes
[39478128959](https://github.com/uibcdf/pharmacophoremt/actions/runs/39478128959),
attempt 1, with **all eight scientific cells successful** on Linux/macOS and
Python 3.11–3.14. Every required provider-context preflight and full `Run tests`
step succeeds. Reporting governance, independent policy run 39478129327 and
Conda governance run 39478129573 also succeed: eleven required executed jobs on
the same source. GH Run Receptor 1.0.0 returns PASS with GitHub success.

The [native-source receipt](../evidence/source_ci_receiving_20261020_summary.json)
verifies actual job/run/attempt/SHA and required-step identity. The daily/probe
backlog detector is inapplicable/skipped for this push; optional coverage-upload
steps are not scientific tests. The previous timeout retains its failed result.
This is the maintainer's direct-push source checkpoint, not accepted external PR
evidence or a Conda installed/public matrix. #9 retains its independent remaining
scope alongside #10/#23; no PR is introduced for the internal maintainer route.

The final evidence/documentation-only handoff uses `[skip ci]` after local
reporting/index and archive-envelope checks. It retains ordinary CI debt and
daily/weekly/manual recovery under #9; it does not certify its own later SHA or
authorize a release. The complete source result remains bound to `636373d`.

### Exact 0.4.0 candidate and documentation closeout — 2026-10-23

New original source `60b21b7d183217d50c29ea3e6bc0d05fb5b797a2` independently
passes source run 39990974160 (all eight scientific cells and reporting), policy
39990974580 and Conda governance 39990974884: eleven executed required jobs.
The [0.4.0 staging receipt](../evidence/conda_040_staging_20261023_summary.json)
retains native source proof. Eight installed artifact cells, public promotion/
receiving and tag/Release identity are separate in the
[delivery receipt](../evidence/conda_040_delivery_20261023_summary.json).

The final documentation/evidence-only closeout uses `[skip ci]` with applicable
local reporting/archive/index checks. Ordinary backlog recovery remains owned
here; no later documentation SHA acquires the candidate's scientific result.
The automatic Release-event publisher is a distinct failed workflow at a shared
staged-route guard (#10 / MolSysSuite #131); its build/upload steps are skipped.
Do not call it green, repeat publication, or conflate it with the successful source
and installed scientific matrices. Required external-PR/recovery scope remains open.
