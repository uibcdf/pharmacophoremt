# Installation

PharmacophoreMT is under active development. Its metadata and required source
matrix declare Python 3.11–3.14; routine development uses Python 3.14. Exact-source
scientific results and installed public delivery are tracked separately in
[uibcdf/pharmacophoremt#23](https://github.com/uibcdf/pharmacophoremt/issues/23).

## Development source

Use a reviewed dependency environment before installing the local source:

```bash
git clone https://github.com/uibcdf/pharmacophoremt.git
cd pharmacophoremt
python -m pip install --no-deps --editable .
```

This command does not resolve dependencies. Required runtime names/bounds live
in `pyproject.toml`; the declared public environments are not an executed clean
installation proof. Scientific CI currently installs the exact seven provider
revisions in `devtools/requirements/controlled_suite_dependencies*.txt` without
dependency resolution. Ackredit and MolSysViewer are integration sources, not
new required runtime dependencies. The selected source context is checked before
science; source qualification does not establish public dependency closure.

## Public package delivery

The official [Conda package API](https://api.anaconda.org/package/uibcdf/pharmacophoremt)
and [PyPI package API](https://pypi.org/pypi/pharmacophoremt/json) returned HTTP 404
at the 2026-10-07 review; the [GitHub release inventory](https://api.github.com/repos/uibcdf/pharmacophoremt/releases)
was checked separately. These observations do not prove historical absence.
`pocketmt` is a different package and is not an installation route for this project.

The prepared single-file `noarch: python` route is reviewed under
[uibcdf/pharmacophoremt#10](https://github.com/uibcdf/pharmacophoremt/issues/10).
Before advertising public installation, retain a reviewed real release plan,
complete successful exact-candidate evidence, authorized staging access, one
original archive, eight installed Linux/macOS arm64 × Python 3.11–3.14 cells,
same-byte public promotion and a clean public receiving check. The example plan
never selects a release; a noarch declaration does not prove installed platform
compatibility. See [the publication controls](https://github.com/uibcdf/pharmacophoremt/blob/2a800f51d3035bd29c5a02570c510fa02631c8af/devtools/conda-build/README.md).
