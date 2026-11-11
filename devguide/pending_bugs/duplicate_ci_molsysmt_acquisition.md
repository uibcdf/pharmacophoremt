---
summary: Remove redundant MolSysMT VCS acquisition after the reviewed source install.
issue: uibcdf/pharmacophoremt#197
status: active
opened: 2026-11-11
closed:
severity: medium
verification: measured
area: [ci, dependencies]
guard: tests/test_ci_routes.py
normative: devguide/ci_molsysmt_acquisition.md
blocked_by: []
supersedes: []
---

# Duplicate MolSysMT acquisition in controlled source CI

Frozen 4766946, source43084105668/attempt1, macOS/Python3.11 job130743901579
successfully builds and installs reviewed MolSysMT0.23.0+370.g0faf1584 with the
other pinned providers. The following older-minor-only force-reinstall repeats
the same VCS URL/commit. Its git clone exits128 with an unavailable interactive
username prompt. The exact server/authentication cause is not observed.
Dependency preflight, PHMT installation/import, tests and coverage are skipped.
This is acquisition failure before scientific execution, not a failing test.

Both controlled requirements files and all four reviewed CI contexts already
declare that same source. The [bounded correction](../ci_molsysmt_acquisition.md)
removes the second install while preserving exact-source verification, scientific
commands, full matrix and failure semantics. No provider or network retry patch.
Record original failure and corrected-source receiving separately under #9/#23/#95;
do not accept frozen4766946 or close #192 from a passing subset.

Acceptance: the route guard must detect the old duplicate, then pass for every
supported minor after removal; installed-context verification remains mandatory
after reviewed acquisition and before PHMT installation/tests. Full corrected
source receiving is separate and pending until actually executed. No source pin,
SDK revision, scientific selection/assertion or resource constraint is relaxed.

## Locally corrected; hosted receiving pending — 2026-11-11 UTC

[Local/native receiving](../evidence/ci_molsysmt_acquisition_20261111.json) verifies
the old failed job and exact one-step removal. Nine route controls, ten quality
checks and unchanged source/context/environment/policy comparisons pass.
The report inventory admits #197 and the unreviewed-source fixture now inserts
a floating override, preserving its rejection assertion. Current guide equality
and 3,420 collected cases/127 expected coverage paths prepare the
[corrected checkpoint](../source_0_6_0_acquisition_recovery.md). This report stays
active until corrected-source receiving; collection/local workflow inspection
does not qualify a supported source/platform/public gate.
