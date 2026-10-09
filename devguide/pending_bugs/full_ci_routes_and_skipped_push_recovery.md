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
