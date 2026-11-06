---
summary: Retrospective EF settings must not overwrite colliding reported metric keys.
issue: uibcdf/pharmacophoremt#100
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: measured
area: [validation, contracts]
guard: tests/test_retrospective_contracts.py
normative: devguide/retrospective_result_contracts.md
blocked_by: []
supersedes: []
---

# Retrospective EF key collisions and public contracts

## What

At main 90beb1a, saved-result summaries reject EF fractions with identical
reported keys, while RetrospectiveValidator writes those keys directly. Two
distinct fractions can format as the same key yet select different ceil(f*N)
counts. This source-inspected finding will receive an analytical reproduction.
Prior metric/accounting repairs #12 and saved-result API #65 retain their scope.

## How

Reuse the existing PHMT saved-result settings validator before retrospective
materialization/evaluation. Declare definition-owned contracts for saved summary,
paired comparison and retrospective construction/run. Retrospective run delegates
to an instance-selected native evaluator; keep its forwarding explicitly open
with that reason, relying on native domains instead of a self-derived Domain.

## Scope and acceptance

Reject colliding keys without rounding/changing requested fractions or renaming
existing output fields. Preserve valid ranking/counts, unscored/native failures,
source identity, paired common-subset metrics, undefined statistics, scientific
methods and molecular ownership. Protect internal bypass, inheritance, closed
admission and native forwarding. Retain actual evidence/resources and all failed
attempts. No provider/dependency/release change or full #6 qualification.

## Resolution — 2026-11-05

The [contract](../retrospective_result_contracts.md) and
[original receipt](../evidence/retrospective_contracts_20261105_summary.json)
retain the two-sample original-production probe: fractions 0.5 and its next
float above require EF values 2 and 1 but collide as EF@50%, returning only 1.
Retrospective run now calls the unchanged saved-result settings validator before
materialization/evaluation, retaining early refusal even under internal bypass.
Four definition-owned ArgDigest contracts cover saved summary/comparison and
retrospective constructor/run. Instance-dependent forwarding remains explicitly
open with native option ownership; no derived domain or molecular logic.

Baseline new guards: eight failures/15 passes; four failures are new declarations.
The separate historical probe asserts the defect and adds one baseline pass.
Final public-prefix107/source84 controls pass, 168 unique selectors including23
new, with no skips or failures. The public scope retains one intentional
attribution-warning control. Guard assertions protect early collision refusal,
unchanged valid numerical values, original identities, failure denominators,
inherited declarations and existing native forwarding. Actual provider/resource
identities and precise source/public/full-gate limitations remain explicit.
