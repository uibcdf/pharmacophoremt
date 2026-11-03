---
summary: Public greedy refinement with both angular policies and valid checkpoint retention.
issue: uibcdf/pharmacophoremt#29
status: resolved
opened: 2026-10-03
closed: 2026-11-03
verification: measured
area: [screening, modeling, validation, attribution]
guard: tests/test_rigid_refinement.py
normative: devguide/rigid_refinement_workflow.md
blocked_by: []
supersedes: []
---

# Public rigid refinement and orientation policies

## Source/API acceptance resolved — 2026-11-03

Clean producer **96f917a7287fdd69e2a8b1a7c6600f975a745e6a** passes
**1020 complete local source tests**, zero failures/errors/skips, after
165 owning refinement/workload/modular/consensus/geometry/seed controls pass.
No runtime or test change is needed. All five cookbook blocks execute; all six
original policy comparisons reproduce their unchanged counts and full scientific
reports with tracking off/on and actual G3PS policy attribution. The strict
isolated cookbook page renders with an adjacent ranked-seed link-target stub;
full-site navigation/rendering is outside that check.

Physical loaded-module/source/native/helper/test/input identities and actual module versions are equal in every phase. Full-run distribution-metadata lookups instead switch to older canonical PHMT, MolSysMT, Viewer and DepDigest records. Strict full equality remains false for that run; focused, cookbook and comparison full equality remain true. The original differences are retained separately, without claiming clean dependency closure.
The [new receipt](../evidence/rigid_refinement_acceptance_20261103_summary.json) retains full test cases,
original logs, runners, exact source/native/input identities, complete comparison
and cookbook reports, bibliography and actual credits. Original October scientific
and timing/RSS archives are unchanged. No new performance benchmark is claimed.

The controls retain angular recovery favoring final (four matches versus no
placement), blocking favoring each_step (five versus no placement), and valid
three-match checkpoint retention by both. Rejected trials do not replace the
last accepted geometry; budgets count initial/trial fits and failures propagate.
Selected/observed matching and fit anchors remain separate. Both policies stay
available and ordinary consensus placement remains the default.

The durable guard is `tests/test_rigid_refinement.py`, with expanded workload
controls in `tests/test_rigid_refinement_workloads.py` and the maintained
[workflow](../rigid_refinement_workflow.md). This closes supplied-seed source/API
acceptance, not clean installed/public/Conda/platform, biological or performance
qualification. The owned #69 venv retains ordinary editable PHMT runtime 404aa38;
its tracked runtime/support/test/tool/workflow trees equal measured clean main
96f917a. Providers/native bytes and the canonical prefix are unchanged. Shared
conflicts remain MolSysSuite #82; exact final-head hosted receiving stays #9 and
public delivery #23/#10. Earlier review/incorporation wording below is historical
and superseded by this dated acceptance.


## What

Expose pair evaluation and greedy refinement independently, with final and
each_step angular policies. Retain alternatives even if particular tests or
benchmarks favor one; record comparisons under their declared conditions.

## How

The [maintained contract](../rigid_refinement_workflow.md) separates growth anchors,
final injective matches, public consumers and MolSysMT geometry. Preserve the
best fully evaluated accepted state and actual per-seed/trial evidence.

## Why

An angularly invalid intermediate state can become valid after further fitting.
Conversely, positional growth can lock pair choices that early angular rejection
would avoid. Neither policy is universally preferable. A public tool permits
different proposal families and consumers to reuse both variants.

## What is measured and what is assumed

Primary G3PS sections 2.2.2, 2.2.4 and 3.4 establish the methodological basis and
postprocessing/future angular distinction. Real MolSysMT exploratory controls
show both directions of policy preference and preservation of a valid checkpoint.
All 26 new controls passed; the 35 existing rigid/modular controls also passed.
The full scientific suite passed 274 tests in 246.00 s on Python 3.14.7 with
installed providers and no PYTHONPATH overrides. Its only warnings remain the
intentional optional-attribution failure and legacy unit-stripping control.
All five cookbook code blocks executed, and the isolated strict Sphinx cookbook
build passed with existing Python 3.13 documentation tooling. Reporting/index,
Ruff and whitespace checks pass.

All six separately recorded analytical policy controls passed with stable
scientific traces between uncredited and actual attributed calls; source hashes
were unchanged during execution. The [retained evidence](../evidence/README.md)
records source/extension hashes, exact inputs, counts and actual policy citations.
This original six-control comparison takes no runtime/memory measurements.
No biological or universal-speed improvement is assumed.

The expanded workload guard `tests/test_rigid_refinement_workloads.py` passes
22 controls spanning seeds, tolerances, mixed classical families, reflection
and six/twelve-donor arrangements in 3D. The full suite now passes 296 tests
in 282.81 s on Python 3.14.7 with the same two known warnings. The cookbook
strict Sphinx build passes with the existing 3.13 documentation tooling. The
opt-in isolated runtime/memory driver has a separate contract in the maintained
refinement workflow; it does not change scientific defaults.

All 22 expanded benchmark comparisons passed: one warmup, three measured calls
and a separate actual attributed call per workload/policy, with stable full
scientific traces, unchanged inputs/provider sources and identical worker
source/extension identities. All actual captures credit the reached policy.
The retained full archive and summary record exact expanded fixtures, fits,
returned alternatives, timing samples, scoped worker RSS and checksums.
Test/documentation builds completed before measurement. The twelve-donor
positive control recovers all sites under both policies with ten fits; seeds
and tolerance changes also alter coverage. Neither a universal winner nor
biological performance is inferred. Original evidence archives remain unchanged.
These expanded results are synchronized in
[the benchmark evidence comment](https://github.com/uibcdf/pharmacophoremt/issues/29#issuecomment-5969866080).

Implementation, tests and measured policy evidence are synchronized in
[the owning issue's evidence comment](https://github.com/uibcdf/pharmacophoremt/issues/29#issuecomment-5969575749).
The issue remains open pending review and incorporation of the working changes.

## Alternatives and refuted paths

Rejecting every current angular failure as proven impossibility is unjustified.
Checking orientations after a fit does not optimize them. Joint optimization,
reconsideration, invariant filtering and branching need separate contracts.
Requiring final min_matches at every intermediate state prevents legitimate growth.

## Scope and exclusions

Public pair evaluator/refinement tool, explicit consumer composition, real attribution,
frozen analytical controls and cookbook. No translation rescue, exclusion correction,
orientation-aware fit, preparation, essential-site semantics, distributed execution
or full-G3PS claim. Default consensus behavior remains ordinary placement.

## Acceptance criteria

Both policy counterexamples and checkpoint retention pass; malformed evidence,
failed providers and exhausted resources never become scientific negatives.
Actual fit counts survive consensus and saved summaries. Cite reached method
stages, execute the cookbook, and pass full scientific and reporting checks.
