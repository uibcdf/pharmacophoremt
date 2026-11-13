---
summary: Declare feature-snapshot input assets required by installed test helpers.
issue: uibcdf/pharmacophoremt#199
status: active
opened: 2026-11-12
closed:
severity: medium
verification: measured
area: [tests, packaging]
guard: devtools/tests/test_distribution_contract.py::TestDistributionContract::test_snapshot_helper_resolves_all_original_assets_in_provider_staging
normative: devguide/installed_snapshot_test_support.md
blocked_by: []
supersedes: []
---

# Installed snapshot test-support data

The declared `feature_snapshot_case` helper resolves five existing original files
relative to its own staged root, but the resource inventory omits those files.
The actual provider-owned staging route fails23/31 existing argument tests with
FileNotFoundError after source31/31passes. No ArgDigest/scientific defect follows.
The independent administrative guard fails on the original declaration.

Declare the unchanged snapshot declaration, parent manifest and three native
inputs with exact hashes; verify their readers and all original bytes through
the actual staged helper. Do not copy undeclared data or add source fallbacks.
The [owning contract](../installed_snapshot_test_support.md) records the recovery
and its old/new source/artifact identities. Full installed/public gates remain
independent from this bounded correction.
