# Installation

PharmacophoreMT **0.4.0** is available from the official `uibcdf` Conda channel.
The package and source metadata require Python `>=3.11,<3.15`.

## Public Conda package

Create an environment with the qualified molecular-provider context:

```bash
conda create -n pharmacophoremt --strict-channel-priority -c uibcdf -c conda-forge pharmacophoremt=0.4.0 molsysmt=0.23.0
conda activate pharmacophoremt
python -c 'import pharmacophoremt; print(pharmacophoremt.__version__)'
```

The explicit MolSysMT pin reproduces the qualified molecular-provider contract.
Receiving its newer development H-bond APIs remains separate work in
[PharmacophoreMT #41](https://github.com/uibcdf/pharmacophoremt/issues/41).
Molecular preparation and manipulation remain MolSysMT responsibilities.

The original `noarch/pharmacophoremt-0.4.0-py_0.tar.bz2` passed installed
qualification on Linux x86_64 and macOS arm64 with Python 3.11, 3.12, 3.13 and
3.14, with 921 passing tests in each cell. The same bytes were promoted to the
public channel and independently checked against its solver index. A fresh
ordinary public installation on Linux/Python 3.14.9 also passed version, native
JSON, explicit-unit and runtime-origin controls. A noarch declaration alone is
not platform evidence; see the [delivery receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/conda_040_delivery_20261023_summary.json)
for exact identities, dependency versions, warnings and scope limits.

[Release 0.4.0](https://github.com/uibcdf/pharmacophoremt/releases/tag/0.4.0) links
the source, original file/digest and native qualification runs. Central public
Python admission and generated badge/inventory disposition are tracked in
[MolSysSuite #131](https://github.com/uibcdf/molsyssuite/issues/131) and
[PharmacophoreMT #23](https://github.com/uibcdf/pharmacophoremt/issues/23).
Broader biological/activity and live-browser/hardware validation remain separate.

PyPI is not a qualified delivery route for this release. `pocketmt` is a different
package and is not an installation route for PharmacophoreMT.

## Development source

Use a reviewed dependency environment before installing the local source:

```bash
git clone https://github.com/uibcdf/pharmacophoremt.git
cd pharmacophoremt
python -m pip install --no-deps --editable .
```

This command does not resolve dependencies. Required runtime names/bounds live
in `pyproject.toml`; routine development uses Python 3.14 in the declared workspace.
Scientific CI installs the exact seven provider revisions in
`devtools/requirements/controlled_suite_dependencies*.txt` without dependency
resolution. Ackredit and MolSysViewer are integration sources, not new direct
required runtime dependencies. The selected source context is checked before
science; source qualification and newer sibling APIs do not extend the public
artifact's measured compatibility automatically.
