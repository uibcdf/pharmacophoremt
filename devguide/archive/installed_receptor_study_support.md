---
summary: Declare selected receptor-study helpers and frozen plans for installed tests.
issue: uibcdf/pharmacophoremt#96
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: measured
area: [distribution, testing]
guard: devtools/tests/test_distribution_contract.py::TestDistributionContract::test_receptor_study_helpers_and_frozen_plans_are_privately_staged
normative: phmt_test_support/README.md
blocked_by: []
supersedes: []
---

# Installed receptor-study test support

The #95 release-readiness review at source `3d26b28` finds three selected tests
importing helpers absent from the literal 51-file installed-support declaration:
`receptor_sensitivity`, `prepared_receptor_sensitivity` and
`receptor_hypothesis_pilot`. Each helper also reads its module-relative frozen
`tests/data/<study>/plan.json`, which needs explicit private staging.

The accepted MolSysSuite @1 operation deliberately copies only declared files;
it does not discover a fixture closure. A source import can conceal this local
metadata gap. Use the unchanged accepted shared staging/cleanup tool with the
checkout excluded from imports, preserve the initial failing guard, and declare
only these three helpers and three immutable plans. Existing declaration entries,
SDK/provider pins, runtime payloads, full installed selection, scientific settings
and original evidence remain intact. Molecular operations stay in MolSysMT.

Acceptance requires the durable shared-staging guard, an actual isolated helper
import/collection probe, retirement of private support and metadata/resource
checks. This repairs the component's declaration only; artifact installation,
the supported native matrix and public package qualification stay under #10/#23.

## Resolution — 2026-11-05

The shared-staging guard initially fails all three subcases: selected helper
module specs are absent. Adding exactly three helper/plan pairs with literal
SHA-256 fixes the same guard. The original 51 declarations and all six source
files retain their bytes; no SDK/provider/runtime/scientific change is needed.

A separate safe-path child uses the actual shared operation to import all three
helpers from private staging, compare module-relative plans and collect 126
selected tests without executing scientific fixtures/bodies. All 57 input hashes
remain stable. Namespace availability/loaded modules and owned staging resources
are retired after use. Actual editable runtime/provider origins remain recorded;
this is source import/collection qualification, not an installed artifact pass.
The [review receipt](../evidence/release_050_review_20261105_summary.json) retains
initial/repaired guard output, the actual probe/SDK, declaration and input hashes.
The [0.5.0 review](../release_0_5_0_review.md) retains the separate release gates.
