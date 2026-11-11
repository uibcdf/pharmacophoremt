# Single reviewed MolSysMT acquisition in source CI

Owners LMMV/dprada; PHMT#197/#9/#23/#95; selected 2026-11-11 UTC.
This is a PHMT workflow correction, not an upstream MolSysMT scientific defect.

## Original observed failure

Later [native/local receiving](evidence/ci_molsysmt_acquisition_20261111.json)
verifies the old failed job and exact one-step removal, with all other parsed
workflow structure/source/context/environment/policy records equal. The new guard
fails before correction; nine route controls and ten quality checks pass after it.
Current guide equality and 3,420 collected cases/127 expected coverage paths
prepare the [corrected checkpoint](source_0_6_0_acquisition_recovery.md), not a
hosted/full acceptance. Original governance inventory/workflow-review failures
remain retained; #197 stays active until corrected hosted receiving.

Source4766946/run43084105668/attempt1, job130743901579, installs the exact pinned
MolSysMT source successfully in `Install pinned suite dependencies`. The later
`Install tested MolSysMT source` step force-reinstalls the identical source on
Python3.11–3.13. Its second git clone fails before PHMT installation and tests:
`could not read Username for 'https://github.com': Device not configured`.
Git exits128 and pip exits1. The remote cause is unknown; the original failure,
skipped scientific steps and earlier successful cells remain original evidence.

## Corrected acquisition contract

Remove only that duplicate workflow step. Both controlled requirements files
retain their exact reviewed source pins, including
MolSysMT0faf1584d05ac47ddcebfc20d9c9978b7f4f230e. For every supported minor,
the existing `devtools/dependency_routes.toml` context identifies its one source
route and requirements input. Acquire it in `Install pinned suite dependencies`
once through the selected requirements file. No second direct VCS install,
force-reinstall, generic retry or credential-policy modification is introduced.

Keep mandatory installed Git-context verification through the immutable reviewed
SDK after acquisition and before PHMT installation/full scientific tests. Retain
the original source pin, SDK SHA, environments, all eight Linux/macOS arm64 ×
Python3.11–3.14 cells, full pytest/assertions/coverage and cancellation semantics.
This removes avoidable repeated acquisition/build work without claiming measured
speed or immunity to external-service failures on the required first acquisition.

## Guard and receiving

Extend `tests/test_ci_routes.py` with one route assertion that fails on the old
direct VCS step. Inspect the declared route for every supported minor, require
one matching pinned requirement, the reviewed install block and unconditional
preflight ordering. Retain existing full matrix/scientific-command guards and
distribution/preflight controls; do not replace native evidence with YAML tests.

Reclassify the changed CI workflow in the dependency-route inventory only after
reviewing that exact removal and unchanged source/context records. Preserve the
guard against unreviewed inline source drift: its fixture now inserts a floating
source override rather than editing the deliberately removed duplicate command.
The issue-backed reporting inventory also admits #197 explicitly. Neither change
relaxes the original drift/report assertions or scientific case selection.

Run targeted routes, dependency declarations, reporting/archive and appropriate
quality checks serially. Before selecting a corrected checkpoint, collect its
actual case count/expected coverage and freeze exact configuration identities.
The corrected source needs one deliberate exact-source validation checkpoint;
never relabel old successful jobs, rerun successful cells or cancel original
work to hide failure. #192 remains active until its supported receiving is real.
No version/tag, public package or documentation publisher is selected here.
