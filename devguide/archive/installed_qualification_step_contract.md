---
summary: Align installed qualification evidence with the actual frozen provider workflow.
issue: uibcdf/pharmacophoremt#54
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: measured
area: [distribution, compatibility]
guard: devtools/tests/test_distribution_contract.py::TestDistributionContract::test_eight_installed_cells_require_both_provenance_checks_and_science
normative:
blocked_by: []
supersedes: []
---

# Installed qualification step contract

## What

The installed descriptor requires `Recheck dependency provenance after installed
tests`, but the frozen MolSysSuite workflow executes `Recheck installed provenance
after scientific tests`. Exact-name verification rejects an otherwise successful
job, before it can authorize promotion.

## How

Correct the descriptor's final required step. Extend the existing distribution
guard to read the actual provider workflow and invoke the shared `verify_job`
operation with its step names. The accepted preflight SDK contains identical
workflow bytes to publication provider `2d32048457c6d37093ae509f5626d00a5cda121b`;
their SHA-256 is `7f08432e10a437d96c1c16bc40ae911dcaab9c817457c1e0a3bcb148768a2bb2`.
Binding these bytes avoids fetching historical commits from shallow CI checkouts.

## Why

A required phase must agree with the workflow that executes it. Checking a
duplicated consumer literal alone preserved the original mismatch.

## What is measured and what is assumed

The new guard fails against the original descriptor with the actual provider's
`MatrixError: required evidence step is missing, skipped or failed`. All fifteen
distribution controls pass after correction. Synthetic successful evidence uses
the real workflow step names; eight negative subcases still reject skipped or
failed required phases. This is administrative contract evidence, not an executed
installed matrix or a built PharmacophoreMT artifact.

The linked [readiness receipt](../evidence/installed_candidate_readiness_20261010_summary.json)
retains provider/source identity and controlled reproductions. The auxiliary
test namespace, scientific test dependencies and addon payload remain separate
under #10 and MolSysSuite #117.

## Alternatives and refuted paths

Removing the post-science check would weaken qualification. Renaming only the
local expected literal would still leave no guard against the actual provider
workflow. Neither alternative addresses the demonstrated contract mismatch.

## Scope and exclusions

The eight installed cells, four phases, source/file/digest bindings, publication
pins and runtime/scientific code retain their contracts. No candidate version,
real release plan, staged build, installed dispatch or publication is selected.

## Acceptance criteria

The actual shared verifier accepts the corrected descriptor against real provider
step names and rejects skipped/failed mandatory phases. The durable guard binds
the consumer wrapper and workflow bytes; the issue can close independently of
the remaining scientific installed-candidate readiness work.
