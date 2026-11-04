---
summary: Consume VirtualScreening constructor digestion control at its own boundary.
issue: uibcdf/pharmacophoremt#78
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: medium
verification: measured
area: [api, screening]
guard: tests/test_nested_facade_contracts.py::test_virtual_skip_is_consumed_at_facade
normative: devguide/nested_facade_contracts.md
blocked_by: []
supersedes: []
---

# VirtualScreening digestion control leaks into evaluator options

## Resolution — 2026-11-04

The facade now has explicit keyword-only skip_digestion=False and consumes it
locally. Literal True bypasses optional preprocessing only; body scientific/method
checks and downstream native validation remain. Scoped constructor contracts in
#6 own method-specific extras. run/cache/scoring behavior is unchanged.

[Receipt](../evidence/nested_facade_contracts_20261104_summary.json) retains the
original nine-case probe, exact sources/tests and all attempts. Final 167 controls
pass with 39 new integration/admission cases. All three runtime identities stay
stable. #6 remains partial and broader public/installed/scientific gates separate.

## What

At 1742259, VirtualScreening succeeds when skip is omitted, but explicit False or
True fails for placed/rigid/conformers. The facade has no formal constructor skip
parameter, forwarding it through **native_options to a closed native constructor.

## How

Use a valid native three-site query; choose seeded_hit for rigid/conformers.
Omitted controls construct. False raises downstream UnknownArgumentError; True
raises downstream TypeError. All six explicit-boolean combinations reproduce.

## Why

A host decorator control must not be a scientific evaluator option. The existing
ArgDigest guide requires explicit local control with preserved scientific checks.

## What is measured and what is assumed

Real constructor execution with no molecular input on Linux/Python 3.14.7 using
public ArgDigest 0.17.0 extraction and inherited dependencies. No provider defect
or released package/platform/predictive qualification is inferred.

## Alternatives and refuted paths

Do not loosen native constructors to accept arbitrary options, remove their
checks, or add a local scientific/molecular backend. Consume the facade control.

## Scope and exclusions

VirtualScreening constructor admission/control only. Native endpoint control
signatures, instance-dependent run option declarations and complete #6 adoption
remain independently scoped. No conformer preparation, score or cache rewrite.

## Acceptance criteria

Actual omitted/False/True construction for all three methods; visible nonboolean
refusal; control never forwarded; explicit method/legacy preparation refusals
under bypass; existing real screening/scoring/cache tests and preserved failures.
