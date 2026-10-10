---
summary: Declare public inputs needed by the complete installed scientific test selection.
issue: uibcdf/pharmacophoremt#55
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: measured
area: [distribution, compatibility]
guard: devtools/tests/test_distribution_contract.py::TestDistributionContract::test_installed_test_inputs_cover_imported_optional_integrations
normative:
blocked_by: []
supersedes: []
---

# Installed scientific test dependencies

## What

The installed descriptor selects all `tests` but declares no component-specific
Conda test inputs. Ackredit and MolSysViewer are explicit optional integration
imports; Beartype and OpenMM are explicitly supplied by source CI environments.
The ten runtime requirements and shared generic test tools alone do not express
this complete test environment.

## How

Use the existing shared `installed_tests.conda_dependencies` operation. Qualify
public dependencies in an isolated environment with an exact editable PHMT
source and no editable sibling providers. Declare only the four observed versions;
leave runtime requirements, source scientific CI and provider implementations
unchanged. Guard optional integration imports against the actual shared resolved
test inputs and require the source matrix's explicit native bootstrap tools.

## Why

Installed science must receive its declared inputs before failures can diagnose
consumer/provider behavior. Explicit test inputs also prevent optional integration
coverage from depending on incidental transitive installation.

## What is measured and what is assumed

The pristine source `3424f3ead0ef85ba9245a5edff4c58bb39d5fcfd` passes all
899 tests with public providers on Linux x86_64/Python 3.14.8, without failures or
omissions. A separate integration selection passes 28 controls, including all
13 source-addon tests. Eight dry solves succeed for Python 3.11–3.14 on Linux
and declared macOS 15 arm64. The original macOS simulation failures are retained
beside corrected solves; they lacked the virtual `__osx` requirement.

The [original receipt](../evidence/public_test_dependencies_20261010_summary.json)
retains full test output/JUnit, registry responses, provider origins and file
hashes, Conda records/history, immutable source hashes and driver sources. All
309 baseline Conda package identities are preserved when adding test tools and
the editable-install backend. Environment-create output was tool-truncated; the
receipt explicitly records that its complete original stdout is unavailable.
Four omission controls reject each missing integration/native input. A further
guard binds the declared exact versions to the observed public-version receipt.

JUnit retains 899 testcase elements and a tests counter of 916 (including
unittest subtest reports); the Receptor terminal result is 899 passed. These
original counters remain separate in the receipt. A source test of the addon
cannot establish installed payload or browser rendering. A cross-platform dry solve cannot establish executed science.

## Alternatives and refuted paths

Installing sibling source copies would not qualify public inputs. Expanding the
runtime requirements to include test integrations would change the consumer's
optional contract. Reimplementing the shared installer locally would duplicate
MolSysSuite's reusable tool. A single observed version cannot establish a minimum
compatible version or a broad supported interval.

## Scope and exclusions

This bounded dependency-input correction does not select a release, build or
publish PHMT. Scientific helper isolation (MolSysSuite #117), addon payload delivery,
the complete installed matrix and public receiving remain separate under #10/#23.

## Acceptance criteria

Public integration/scientific results and exact origins are retained with their
limits. The descriptor supplies the measured versions through the real shared
resolver. Durable controls fail when imported optional integrations or explicit
native bootstrap inputs are omitted. No provider molecular operation is implemented
locally.
