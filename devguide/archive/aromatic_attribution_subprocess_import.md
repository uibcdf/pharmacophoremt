---
summary: Aromatic attribution-absence subprocess assumed an eagerly imported screening namespace.
issue: uibcdf/pharmacophoremt#48
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: measured
area: [testing, attribution, ci]
guard: tests/test_aromatic_interactions.py::test_genuine_absence_does_not_prevent_aromatic_science
normative:
blocked_by: []
supersedes: []
---

# Explicit screening import in the attribution-absence subprocess

## What

The full scientific CI at `def2248251a3e544b90ec1ce5d291482c99914a0` reports
one failure and 812 passes on Ubuntu Python 3.14.8, in
`test_genuine_absence_does_not_prevent_aromatic_science`. Its fresh subprocess
calls `phmt.screening.PoseEvaluator` without importing the screening namespace.
The root package does not promise that eager import. The original
[run](https://github.com/uibcdf/pharmacophoremt/actions/runs/38039753343) and
job `114177461859`, step `Run tests`, identify the hosted failure.

## How

A local isolated execution reproduces the same `AttributeError` in the normal
editable Python 3.14.7 environment. Import `PoseEvaluator` from its supported
`pharmacophoremt.screening` namespace inside the subprocess and call that name.
Parent-process imports cannot initialize a separate process's namespace.

## Why

The guard should test unavailable optional attribution alongside successful
aromatic science, rather than fail on an unrelated implicit import assumption.
No scientific implementation, root eager-import policy, shared CI contract or
molecular provider routine is changed.

## What is measured and what is assumed

The hosted diagnostic excerpt and local failing guard are retained. The corrected
isolated guard and neighboring aromatic/attribution checks are executed in the
[new review](../evidence/aromatic_attribution_import_review_py314_summary.json).
The subprocess still blocks Ackredit imports, asserts an unavailable attribution
payload, evaluates a matched pose and confirms Ackredit remains unloaded. This
is not a full-suite/matrix result or a released-artifact/provider qualification.
The original #47 SDF review remains separate and unchanged.

## Alternatives and refuted paths

Do not add an eager root scientific import just to satisfy this test. Do not
classify this import error as a MolSysMT capability gap or as proof that missing
Ackredit prevents the scientific operation.

## Scope and exclusions

One isolated test's supported import and its maintained failure record. The
full matrix must recover through the normal exact-head hosted gates; local
focused checks do not retroactively change the failed run's conclusion.

## Acceptance criteria

Keep the original failure identity/output; pass the corrected real absent-provider
subprocess and neighboring aromatic/attribution controls; leave runtime/provider
source unchanged. The existing guard protects these assertions in a fresh process.
