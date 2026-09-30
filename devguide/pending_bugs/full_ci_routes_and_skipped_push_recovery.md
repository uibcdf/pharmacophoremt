---
summary: Complete contributor full-CI routes and skipped-push recovery.
issue: uibcdf/pharmacophoremt#9
status: active
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
- Dispatch the complete six-cell lane and preserve actual outcomes.
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
