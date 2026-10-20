---
summary: Use SPDX license metadata with a compatible setuptools backend and remove the stale Versioneer manifest entry.
issue: uibcdf/pharmacophoremt#57
status: resolved
opened: 2026-10-13
closed: 2026-10-20
severity: low
verification: reproduced
area: [packaging]
guard: devtools/tests/test_distribution_contract.py::TestDistributionContract::test_spdx_license_has_a_compatible_build_backend_and_included_file
normative:
blocked_by: []
supersedes: []
---

# SPDX license metadata and the build backend

## What

The old TOML license table and license classifier emitted setuptools deprecation
warnings. The manifest also named the absent `versioneer.py`, although this
component uses versioningit.

## How

Use the SPDX expression `MIT` and explicit `license-files = ["LICENSE"]`, remove
the redundant classifier and Versioneer entry, and align the setuptools host
requirement in the Conda recipe with the build-system minimum `77.0.3`.
The recipe also explicitly names `LICENSE`.

## Why

SPDX expressions and `license-files` require setuptools 77 or newer; keeping the
old minimum 61 would accept an incompatible backend. This component selects
77.0.3 as an exercised compatible floor, without changing the shared backend
profile, versioningit bound, runtime requirements or Python 3.11–3.14 support.
The [setuptools documentation](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)
documents the PEP 639 support introduced in version 77.

## What is measured and what is assumed

On Python 3.14.7, normal isolated sdist builds followed by wheels built from those
sdists passed with setuptools **77.0.3** and **84.2.0**, both using versioningit
2.3.0. All four archives contain the exact source LICENSE bytes and declare
`License-Expression: MIT`, `License-File: LICENSE` and the unchanged Python range.
The warnings targeted here are absent; unrelated unmatched global-exclude notices
remain. The 20 distribution-contract controls pass with the previously accepted
immutable SDK.

The [build receipt](../evidence/packaging_license_20261020_summary.json) retains
artifact identities, original build reports/logs and the precise uncommitted
overlay on source `28051a151d3db2c92be00d95b00b60f5e04c3a07`. These are development
artifacts, not a clean release candidate or an installed Conda matrix.

## Alternatives and refuted paths

Retaining setuptools >=61 while adopting SPDX metadata is incompatible. Raising
a runtime floor or migrating the backend is unnecessary for this correction.

## Scope and exclusions

No scientific behavior, publication, addon work or installed platform support is
claimed. Those remain separate work under #10, #23 and #58.

## Acceptance criteria

The guard protects the compatible backend floor, SPDX fields, explicit license
file, classifier removal and rendered Conda recipe. The measured archives verify
that the actual license bytes survive both build stages.
