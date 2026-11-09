---
summary: Require all new Pharmer helper modules in the Conda payload inventory.
issue: uibcdf/pharmacophoremt#168
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: medium
verification: measured
area: [distribution, governance]
guard: devtools/tests/test_distribution_contract.py::TestDistributionContract::test_complete_current_core_data_and_private_resources_are_inventoried
normative: devtools/conda-build/resources.toml
blocked_by: []
supersedes: []
---

# Complete the Pharmer Conda resource inventory

## What

Source1f6dfb0 fails the existing complete-resource guard in reporting job129280430569
of deliberate run42651970337: the Conda declaration omits the new I/O helpers
`io/_pharmer_profile.py`, `io/_projection.py` and private argument digester
`_private/arg_digestion/pharmer_io.py`. All are committed runtime files from#163.
The administrative job reports160tests with one failure. The original job-only
GH Run Receptor capture and native failure are retained in the checkpoint capsule.

## How

Add the three exact installed paths to the owning `required_paths` declaration.
Reuse the existing source-completeness and archive-validation tests and immutable
shared SDK. Preserve the assertion, runtime, provider pins and package contents.

## Why

An incomplete declaration weakens future Conda artifact completeness checks.
This does not establish a newly published broken package: no new public artifact
was built/published, and owned203receiving verifies all214payload/159runtime files.

## What is measured and what is assumed

The exact-head source checkpoint fails its administrative job. Its remaining
scientific cells are cancelled to avoid spending resources on a candidate that
cannot qualify. Original handles/conclusions and the local post-request file-name
collision are retained; no request is replayed. The [local correction receipt](../evidence/numerical_reader_ci_recovery_20261109.json)
receives the original25-case/one-failure reproduction,160administrative passes
after correction and25final distribution passes after the workflow update. The
required inventory grows206→209unique paths; runtime/wheel/provider bytes stay
unchanged. A corrected exact-head checkpoint remains pending.

## Alternatives and refuted paths

Do not drop the completeness guard, ignore private modules, invent a new archive
checker, modify provider/SDK code or reclassify a source-gate failure as success.

## Scope and exclusions

A PHMT distribution declaration defect. No runtime/API/scientific change,
new environment/acquisition, package publication or#148/#165retry. The corrected
source candidate receives its own identity; earlier failed evidence is preserved.

## Acceptance criteria

The original guard fails before and passes after the declaration correction;
relevant distribution/dependency and local report/index controls pass, and actual
old/new checkpoint states remain explicit. Archive this declaration fix only with
measured local controls; complete source/public/platform gates remain separate.

The local declaration fix resolves this report. The [owning checkpoint](../numerical_reader_ci_checkpoint.md)
retains the original failed/cancelled source gate and independent corrected-candidate
requirements; no new public package, installed matrix or source gate is accepted.
