# Reviewed Conda environment operations

The thin owner tools call MolSysSuite's optional environment operator at immutable
commit `8f00e6d9de943b6e4710ea62936e2ebea00fad24` (406 central tests and hosted
qualification). Set `PHARMACOPHOREMT_SUITE_ROOT` to that clean SDK checkout or put
it at `.molsyssuite`; the loader verifies the commit and administrative import
origin. This is independent of the existing publication SDK pin `2d32048…`.

## Generate or check ordinary documents

```bash
python devtools/broadcast_requirements.py --check
python devtools/broadcast_requirements.py
```

`devtools/environment_tools.toml` selects **only** production, development,
documentation, setup and build documents. Metadata owns Python and all runtime
requirements; `devtools/requirements.yaml` now contains tools only (including
NumPy as a retained setup/build bootstrap). Scientific test documents, the
historical importable fixture, recipes, plans and fixed Git manifests stay outside
this selection. All outputs are validated before writes; drift checks do not
write. Keep specialized native/scientific requirements in their reviewed routes.

## Explicit creation or active update

Run from the repository root with root-relative registered environment paths:

```bash
python devtools/conda-envs/create_conda_env.py \
  devtools/conda-envs/development_env.yaml --python-minor 3.14 \
  --manager mamba --name pharmacophoremt-dev
conda activate pharmacophoremt-dev
python devtools/conda-envs/update_conda_env.py \
  devtools/conda-envs/development_env.yaml --python-minor 3.14 \
  --manager conda --prefix "$CONDA_PREFIX"
```

Create requires a new unoccupied name; update requires the exact active Conda
prefix and matching interpreter. There is no fallback from failed create to
update and no implicit `--prune`. The manager/path is explicit. Complete Python
minor selection must fit metadata and the existing document, and scientific Git
contexts additionally require their reviewed minor. Management neither rewrites
the original YAML nor silently installs a different source provider.

`bash devtools/start_dev_env.sh --manager mamba --name pharmacophoremt-dev` is a
thin creation convenience for routine Python 3.14. Activate explicitly afterward.
The old import-time helpers and broad startup flags (`--mode`, arbitrary
`--python`, `--env-yaml`, automatic update/kernel registration) are retired;
use the explicit commands above. No scientific package API has changed.

After creation/update, install the intended local clone with
`python -m pip install --no-deps --editable .`, then verify `pip check`, installed
dependency bounds and import origins. Use `devtools/check_dependency_routes.py`
with the actual matching context for its source/public provenance check. A manager
exit or administrative guard alone does not prove transitive closure, native
backends or scientific tests. Routine workspace development remains
`molsyssuite@uibcdf_3.14`; these optional owner environments do not replace it.

Contract: [shared environment-tool guide](https://github.com/uibcdf/molsyssuite/blob/8f00e6d9de943b6e4710ea62936e2ebea00fad24/devguide/conda_environment_tools.md).
Tracking: uibcdf/pharmacophoremt#10 and uibcdf/molsyssuite#108; actual scientific
and public receiving qualification remain owner work.

## Ordinary environment review — 2026-10-10

Three new isolated Linux x86_64 environments were created with the reviewed
operator: production/development on Python 3.14.8 and docs on Python 3.12.15.
They use public Conda dependencies and an editable, exact PharmacophoreMT source
copy, with no sibling source overlays or Python admission bypass. Each passes
`pip check`, its registered installed-context preflight and a native placed-pose
positive/displacement-negative check. These are selected compatibility checks,
not a full platform matrix or a public PharmacophoreMT artifact.

The manager inherited an additional local `ambermd` channel. All installed files
are nevertheless from `uibcdf`/`conda-forge`; a separate strict, exclusive-channel
dry solve reproduces every original name/version/build. Strict priority alone
does not exclude inherited channels. Keep that distinction in future receipts.
Shared effective-channel reporting is proposed in `uibcdf/molsyssuite#116`.

The ordinary development document does not include optional Ackredit. Tests that
require it were qualified separately after adding public Ackredit 0.12.0 to the
temporary development environment, with all prior Conda records unchanged.
ArgDigest's optional Beartype extra is absent in the original environments;
its diagnostics explicitly report disabled runtime type checks.

The full documentation build uses the installed ordinary environment, without
notebook execution. The same warning-free gate can be run in the development
environment, which supplies both Pytest and the documentation tools:

```bash
python -m pytest devtools/tests/test_documentation_build.py
```

Original attempts, failures, corrected verification and dependency inventories:
`devguide/evidence/ordinary_environment_review_20261010_summary.json`.

## Separate complete-test inputs — 2026-10-10

The #55 review uses a new production-based public environment plus the shared
installed-test tool installer, exact PHMT editable source and public MolSysViewer
0.24.0/Ackredit 0.12.0/Beartype 0.22.9/OpenMM 8.6.1. The bounded input declaration
belongs to `devtools/conda-build/resources.toml`; it does not add optional test
integrations to ordinary runtime requirements. An editable-install build backend
is installed separately, without bypassing `Requires-Python`.

[Original records and results](../../devguide/evidence/public_test_dependencies_20261010_summary.json)
separate source science on Linux/Python 3.14 from eight simulated dependency
solves. They do not qualify every ordinary environment for the complete suite,
an installed PHMT artifact, native macOS execution or browser rendering.
