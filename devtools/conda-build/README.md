# PharmacophoreMT Conda publication

Owning review: uibcdf/pharmacophoremt#10; coordination: uibcdf/molsyssuite#45.
This is a prepared noarch publication route with partial adoption and unconfirmed
publication access. It does not select a release.

The four publication wrappers pin qualified SDK
`2d32048457c6d37093ae509f5626d00a5cda121b`; dependency/environment preflight
separately pins `8f00e6d9de943b6e4710ea62936e2ebea00fad24`. The existing
`ANACONDA_UIBCDF_TOKEN` mapping is retained; its availability/validity remains
unconfirmed. Follow the [shared noarch workflow guide](https://github.com/uibcdf/molsyssuite/blob/main/devguide/noarch_conda_workflow.md).

## Candidate and file identity

Review and commit an actual `release_plan.toml` before selecting a candidate.
`release_plan.example.toml` has illustrative version 0.0.0 only. It requires eleven
executed jobs: eight full supported source cells with installed-context preflight,
independent governance, policy/lint/format and Conda governance. A passing recovery
probe with omitted science cannot authorize publication.

The inventory includes 171 committed package files plus the generated version
module, covering private diagnostics, current modules and committed runtime data.
Register new package modules/resources in `resources.toml`'s `required_paths`.
The existing complete-tree guard in `devtools/tests/test_distribution_contract.py`
checks this inventory; run the administrative tests with the accepted immutable
SDK before publishing a new module.
Package discovery includes only `pharmacophoremt*`, excluding checked-out tooling
and test namespaces. Recipe/metadata parity and synthetic archive guards inspect
missing resources and stale version identity; they do not prove built/installed
scientific behavior or optional native backend compatibility.

Stage the one original noarch file, qualify it outside both sources on the eight
Linux/macOS arm64 × Python 3.11–3.14 cells, and require all four steps: exact-file
installation, installed-file validation, complete local tests and the post-test
provenance recheck. The manual installed wrapper never runs on ordinary pushes.
Missing/skipped/failed evidence blocks promotion. An optional administrative
`qualification_sha` is separate from the original `candidate_sha`, file and digest.
Promote those same bytes without rebuilding or replacing the archive. No actual
build, installed scientific dispatch, promotion or public delivery occurred here.

## Dependency routes

```bash
PHARMACOPHOREMT_SUITE_ROOT=/path/to/accepted/sdk python devtools/check_dependency_routes.py --declared-only
# In the actual resolved scientific interpreter before tests:
PHARMACOPHOREMT_SUITE_ROOT=/path/to/accepted/sdk python devtools/check_dependency_routes.py --context ci-3.14
# Administrative guards, outside the scientific tests selection:
PHARMACOPHOREMT_SUITE_ROOT=/path/to/accepted/sdk python -m unittest discover -s devtools/tests -p test_distribution_contract.py
```

The optional @3 inventory covers seventeen routes, fourteen source records, two
unchanged source manifests and seven contexts. Every source cell checks actual
repository/full commit/version before science. Ackredit and MolSysViewer are
integration sources; the other five are required metadata providers. The existing
repeated MolSysMT installation on older minors uses the same declared immutable
revision and is retained. Special scientific environments, backend bounds, test
commands, matrix, triggers and recovery remain intact. Checker libraries are
isolated under `.molsyssuite-tools`, visible only to the preflight process.

Production/development/docs declarations include all ten direct requirements.
All three ordinary environments were created and checked with public runtime
providers on 2026-10-10: production/development on Python 3.14.8 and docs on
3.12.15. See the [executed environment receipt](../../devguide/evidence/ordinary_environment_review_20261010_summary.json)
and [environment operations](../conda-envs/README.md). The shared replacement
under uibcdf/molsyssuite#108 is adopted; generation cannot rewrite the publication
recipe or plan. These observations concern an editable PharmacophoreMT source,
not a built/installed public PharmacophoreMT artifact. Real plan/access/artifact,
complete installed science and public receiving evidence remain outstanding.

## Environment helper adoption — 2026-10-07

Ordinary environment generation and checked create/update now call the additive
qualified SDK `8f00e6d9de943b6e4710ea62936e2ebea00fad24`, as does source/context
preflight. Existing publication wrappers retain their separately accepted
`2d32048457c6d37093ae509f5626d00a5cda121b` pin. See
[environment operations](../conda-envs/README.md); generation cannot rewrite this
recipe/plan or the scientific files. This source adoption does not prove an
actual manager operation, full science matrix or public installed artifact.

## Installed candidate readiness — 2026-10-10

Local #54 aligns the required final step with the actual frozen workflow:
`Recheck installed provenance after scientific tests`. The administrative guard
uses the provider's workflow bytes and actual shared verifier; this repair
preserves all four phases and eight installed cells.

Before building/selecting a candidate under #10:

- Public scientific test inputs are declared and qualified under #55 through
  the existing `installed_tests.conda_dependencies` provider contract; see the
  dated dependency review below. This source qualification does not establish
  an installed artifact's complete science matrix.
- Resolve direct scientific `devtools.*` helper imports through the reusable
  support proposal [MolSysSuite #117](https://github.com/uibcdf/molsyssuite/issues/117).
  Actual isolated runner controls fail with both the frozen provider and the
  accepted all-root provider. Adding the checkout to scientific imports would
  invalidate the installed boundary.
- Review distribution of the existing `molsysviewer_pharmacophoremt` addon.
  Discovery and inventory currently include only the main package, while the
  addon test inserts the checkout into `sys.path`. It cannot establish installed
  addon behavior. Include intended payload roots and review adoption of the
  [qualified all-root guard](https://github.com/uibcdf/molsyssuite/issues/110#issuecomment-6035399970)
  before actual installed qualification; current publication pins remain fixed.

The [readiness receipt](../../devguide/evidence/installed_candidate_readiness_20261010_summary.json)
retains controlled reproductions and source identities. These administrative
fixtures are distinct from a real candidate's installed scientific matrix.

## Public scientific test inputs — 2026-10-10

Local #55 supplies `installed_tests.conda_dependencies` through the existing shared
resolver: MolSysViewer 0.24.0, Ackredit 0.12.0, Beartype 0.22.9 and OpenMM 8.6.1.
These are exact observed public versions, not inferred compatibility minima.
The component's ten runtime requirements and scientific source CI remain unchanged.
The guards compare imported integration providers and the source matrix's explicit
native bootstrap tools with the actual shared resolved test inputs.

The qualification uses a separate public Conda environment on Linux x86_64 with
Python 3.14.8 and exact editable PHMT source `3424f3e`. Public provider origins and
Ackredit/MolSysViewer archive hashes are checked. The eight dependency dry solves
cover Python 3.11–3.14 on Linux and macOS arm64; macOS simulations explicitly
assume macOS 15. They are not executed macOS science. The baseline manager still
inherits `ambermd` (MolSysSuite #116), although installed package URLs are only
`uibcdf`/`conda-forge`; test-tool operations and dry solves use exclusive channels.

See [the original dependency receipt](../../devguide/evidence/public_test_dependencies_20261010_summary.json)
for the 899 passing complete source tests, the separate 28 integration controls
and complete original records. Helper isolation
under MolSysSuite #117, addon distribution, the real candidate and the complete
installed/public receiving matrix remain independent prerequisites. No browser
rendering or installed addon support is established by a source addon test.
