# Accumulated progress, projection and coverage source checkpoint

Owners LMMV/dprada; declared2026-11-07;
[#9](https://github.com/uibcdf/pharmacophoremt/issues/9),
[#23](https://github.com/uibcdf/pharmacophoremt/issues/23),
[#141](https://github.com/uibcdf/pharmacophoremt/issues/141).
Status: dispatched at exact489be1213a92e33be84204d2e0fd2f5f9b9c10e1/attempt1.
The [initial native receipt](evidence/projection_ci_initial_20261107.json)
records source CI42416657424 with eight running science cells and successful
reporting; policy42416661473 and publication governance42416665708 complete their
required steps successfully. Source test counts and corrected XML acceptance
remain pending. These are dated observations, not whole-gate acceptance.

This deliberately batches accumulated saved-progress runtime, the qualified
[RDKit projection](rdkit_projection.md) and the
[coverage XML identity correction](coverage_xml_identity.md). The old
[4616c78 checkpoint](accumulated_ci_checkpoint.md) is complete for its own source;
it is not rerun or reassigned. Owned installed projection producer1040dbb and its
wheel0.4.0+148 retain separate source/build identity and actual receipts.

Use the three existing manual workflows, with their complete selections and
reviewed source acquisition/policy pins unchanged:

- `CI.yaml`, `probe_backlog=false`: reporting governance and all eight Linux/
  macOS arm64 Python3.11–3.14 scientific cells, normal preflight and full tests.
- `molsyssuite-policy.yml`: the unchanged frozen policy-v1.5.4 caller, including
  conformance/lint/import/format steps. Current guide/instruction adoption has
  its own audit; frozen-policy success does not substitute for it.
- `conda_publication_governance.yaml`: existing publication controls and declared
  no-build resources/recipe checks. Do not trigger a build, upload, tag or release.

Before every dispatch, verify clean reviewed local source, remote candidate and
existing exact-head workflow runs. Reuse an existing matching run rather than
launching a duplicate. Dispatch each selected workflow at most once and record
native run/attempt identities; observation timeouts do not authorize restarts.
The skipped manual backlog probe is intentional, distinct from scientific cells.

Accept the source gate only after all required native jobs/steps and the actual
full test commands/results are terminal and verified. Receive actual interpreter,
architecture, package/dependency and test counts from original logs; do not
predict counts from selected bodies or multiply platform repeats into independent
scientific cases. Preserve failed/partial attempts and provider identities.

Receive the corrected XML separately: both package-qualified initializers,
companion API/storage/export classes and unique repository-relative filenames
must survive in actual hosted XML. Keep branch measurement, zero-hit source
discovery and original private omission. Native Codecov upload success does not
independently establish public-server freshness. Preserve the original4616c78
aggregates and the source regression's before/after identities. #141 remains open
until this declared hosted mapping qualification completes.

Use registered GH Run Receptor1.4.0 for the initial capture and completed evidence;
native fallback is only for capabilities absent from the plugin/receiver, including
manual dispatch. Keep raw logs/API bodies local and publish reviewed scalar/hash
facts. Network/Git inspection uses serial CPU19/backend1/nice19/idle I/O and
appropriate per-process DATA limits; no own aggregate cgroup is available.

This receives a source candidate, not a new full public dependency solve, installed
package/platform/minor matrix, biological validation, benchmark or mature0.x release.
While remote jobs run, continue independent owning work and keep this candidate
distinct from subsequent runtime or receipt heads. Routine pushes retain `[skip ci]`.
