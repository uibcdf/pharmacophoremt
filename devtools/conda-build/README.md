# PharmacophoreMT Conda publication

Owning review: uibcdf/pharmacophoremt#10; coordination: uibcdf/molsyssuite#45.
This is a prepared noarch publication route with partial adoption and unconfirmed
publication access. It does not select a release.

All four publication wrappers and the dependency preflight pin qualified SDK
`2d32048457c6d37093ae509f5626d00a5cda121b`. The existing
`ANACONDA_UIBCDF_TOKEN` mapping is retained; its availability/validity remains
unconfirmed. Follow the [shared noarch workflow guide](https://github.com/uibcdf/molsyssuite/blob/main/devguide/noarch_conda_workflow.md).

## Candidate and file identity

Review and commit an actual `release_plan.toml` before selecting a candidate.
`release_plan.example.toml` has illustrative version 0.0.0 only. It requires eleven
executed jobs: eight full supported source cells with installed-context preflight,
independent governance, policy/lint/format and Conda governance. A passing recovery
probe with omitted science cannot authorize publication.

The inventory includes 177 committed package files plus the generated version
module, covering private diagnostics, current modules and committed runtime data.
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

Production/development/docs declarations now include all ten direct requirements;
their source-free actual installed invocations remain pending. The legacy
broadcaster and Conda helpers are unqualified inputs under #10: do not use them to
approve or regenerate a candidate. They can widen Python or overwrite recipe
controls; every proposed result must pass the separate recipe/dependency/source
checks. Shared reusable replacement is tracked in uibcdf/molsyssuite#108;
keep reviewed metadata/environments plus existing shared preflight until its
qualified owner adoption replaces these legacy paths. Real plan/access/artifact, public receiving evidence
and Python admission remain outstanding; configuration alone proves none of them.

## Environment helper adoption — 2026-10-07

Ordinary environment generation and checked create/update now call the additive
qualified SDK `8f00e6d9de943b6e4710ea62936e2ebea00fad24`, as does source/context
preflight. Existing publication wrappers retain their separately accepted
`2d32048457c6d37093ae509f5626d00a5cda121b` pin. See
[environment operations](../conda-envs/README.md); generation cannot rewrite this
recipe/plan or the scientific files. This source adoption does not prove an
actual manager operation, full science matrix or public installed artifact.
