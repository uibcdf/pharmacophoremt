# Developer onboarding

Maintained 2026-11-07; owners LMMV/dprada, [#107](https://github.com/uibcdf/pharmacophoremt/issues/107).
Start here when joining the team or rebuilding a development machine. This
handoff does not claim that the destination installation has been executed.

## Read in this order

1. Root [AGENTS.md](../AGENTS.md), [MolSysSuite guide](../MOLSYSSUITE_GUIDE.md),
   local [instructions](AGENTS.md) and [reporting protocol](reporting_protocol.md).
2. [Checkpoint](checkpoint.md): current work, evidence and immediate next action.
3. [Decisions/workstreams](decisions_and_workstreams.md): why we work this way.
4. [Capability inventory](capability_inventory.md), [architecture](core_architecture.md)
   and [testing/validation](testing_and_validation.md): actual tools and limits.
5. [Migration checklist](machine_migration.md), then the setup route below.
6. [Roadmap](roadmap.md) and the owning issue/report/method contract before a change.

[Historical checkpoints](checkpoint_history_20261106.md) and
[historical roadmap](roadmap_history_20261106.md) preserve earlier decisions.
Their old "Next" paragraphs are not current instructions. Dated receiving
records describe their own producer and observation; newer results do not
retroactively qualify older artifacts. Git retains the exact earlier texts.

## Ownership and repository map

PHMT owns pharmacophore features/shapes/hypotheses, constraint interpretation,
matching/ranking and study orchestration. MolSysMT owns molecular representations,
formats, chemistry, inspection, preparation, selection, atom/state maps, geometry
and transforms, including PDBQT/SDF and sequence/construct interpretation. Reuse
its supported tools or report a concrete gap there. Existing #41/#74 migration
debt is not permission to add another molecular implementation here.

TopoMT owns pockets/surfaces, DockingMT docking and MolSysViewer rendering.
Read the registered root guides for ArgDigest, DepDigest, SMonitor, PyUnitWizard
and optional Ackredit before changing their integration boundaries.

| Location | Purpose |
| --- | --- |
| `pharmacophoremt/` | Distributed model/modeler, screening, validation, codec and support adapters |
| `pharmacophoremt_results/` | Distributed independent saved-run reader/writer; ArgDigest/SMonitor, no scientific-provider imports |
| `molsysviewer_pharmacophoremt/` | Distributed addon; browser qualification remains separate/deferred |
| `tests/`, `tests/data/` | Source contracts and frozen inputs |
| `phmt_test_support/` | Unshipped fixture/evidence clients; not a molecular engine |
| `devtools/` | Explicit tools, environments, dependency and publication wrappers |
| `devguide/evidence/` | Original receipts/archives and frozen plans |
| `pending_bugs/`, `pending_proposals/`, `archive/` | Issue-backed lifecycle; generated indexes |
| `docs/` | Sphinx user/API/cookbook/validation pages; build does not execute notebooks |
| `build/`, `.molsyssuite*`, `/tmp/` | Ignored/local resources absent from a fresh Git clone |

## Choose the environment before interpreting results

Routine Linux development follows the canonical
[suite workspace](https://github.com/uibcdf/molsyssuite/blob/main/devguide/development_workspace.md)
and its `molsyssuite@uibcdf_3.14` recipe/profile. Install eligible participating
clones editable; inspect suite cross-repo state before coordinated changes.
Preserve other developers' dirty/ahead/behind clones.

| Context | Authority | Meaning |
| --- | --- | --- |
| Shared workspace | Current suite recipe/profile | Routine eligible-clone development; verify origins/closure |
| Controlled source | `test_env_py314.yaml`, exact Git manifest, `ci-3.14` | Modern source contracts; rebuild native providers |
| Public providers | `public_test_env_py314.yaml`, `public-test-3.14` | Published dependency receiving; modern APIs may be absent |

Ordinary `development_env.yaml` is not the complete scientific context. The
public-provider receipt's203 selected passes/18 capability skips do not qualify
absent modern MolSysMT APIs. The historical controlled `/tmp` prefix is now
absent. A sibling's current `main` or a copied Conda directory does not recreate it.

### Receiving a new packaged namespace

Adding `pharmacophoremt_results` requires refreshing an older editable
registration: its generated finder may still expose only the two original
package roots. Reuse the canonical no-dependency editable-install route with the
declared build requirements, then verify a fresh interpreter outside the checkout,
without source-path overrides. Restart an existing interpreter to receive the
new registration.

The [2026-11-07 receiving](public_prepared_runs.md) first qualified the exact
owned wheel, then refreshed only PHMT editable metadata and its ignored generated
version cache to0.4.0+134.gee5d9fa. It used the verified cached versioningit2.3.0
build-only overlay to satisfy~=2.0; the shared3.3.0 was not substituted and no
provider was upgraded. Cold normal imports work, all154 Python files match the
qualified wheel, and identical-runtime source reopens the complete installed run
without new evaluations or writes. Earlier source/producer versions stay original.
This local receiving is distinct from full environment closure and release support.

## Fresh controlled-source setup

These are instructions for a new owned environment, not a destination receipt.
Clone with history/tags and enter the root. Review status before any checkout.

```bash
git clone https://github.com/uibcdf/pharmacophoremt.git
cd pharmacophoremt
git fetch origin --tags
git status --short --branch
git rev-parse HEAD
```

The wrappers require the clean SDK pinned in `devtools/check_dependency_routes.py`,
currently1c248b67d1daea256ed7c7f6172c6addb3f0b08f. Bootstrap an isolated SDK;
do not reset the team's mutable suite checkout to satisfy this requirement.

```bash
git clone https://github.com/uibcdf/molsyssuite.git .molsyssuite
git -C .molsyssuite checkout --detach 1c248b67d1daea256ed7c7f6172c6addb3f0b08f
git -C .molsyssuite status --short
python -m pip install --target .molsyssuite-tools "PyYAML>=6" "Jinja2>=3,<4" "packaging>=24"
```

Use a supported bootstrap Python. Checker-only libraries remain isolated under
this clone. Read [environment operations](../devtools/conda-envs/README.md).
Scientific YAML is registered for creation even though ordinary generation
excludes it. Ensure provider-native prerequisites, including MolSysMT's Rust/Cargo
toolchain, from each pinned provider's own instructions before source installation.
Run heavy creation/build/install steps with the resource controls in the migration
checklist, including `CARGO_BUILD_JOBS=1` for Rust builds. If a native build cannot
fit the agreed budget, defer it to its owning build/qualification route and keep
the failed/unexecuted gate explicit; do not raise limits or substitute providers.

```bash
python devtools/conda-envs/create_conda_env.py \
  devtools/conda-envs/test_env_py314.yaml --python-minor 3.14 \
  --manager conda --name pharmacophoremt-source-314
conda activate pharmacophoremt-source-314
python -m pip install --no-deps -r devtools/requirements/controlled_suite_dependencies_py314.txt
python -m pip install --no-deps --editable .
python -m pip check
python devtools/check_dependency_routes.py --context ci-3.14
python -c 'import sys, pharmacophoremt, molsysmt; print(sys.version); print(pharmacophoremt.__file__); print(molsysmt.__file__)'
```

The manifest/context inventory and CI own the pins; don't maintain another copied
requirements list here. Do not copy old native `_rust.abi3.so` binaries. Record
new source/native origins, builds and failures. A successful solve/import alone
does not qualify the full scientific suite or macOS. If solve/build/`pip check`/
preflight fails, retain the original failure and resolve its owner instead of
upgrading unrelated packages, hiding a source overlay or weakening assertions.

## First checks and first change

These standard-library checks need no molecular provider:

```bash
python -B devtools/devguide_index.py --check
python -B -m unittest discover -s tests -p test_reporting_protocol.py
python -B -m unittest discover -s tests -p test_evidence_archive.py
python -B -m devtools.evidence_archive devguide/evidence/brd4_primary_method_20261106_summary.json
```

After environment/preflight verification, select tests from the changed contract:

```bash
python -m pytest --receptor=llm tests/test_validation_metrics.py
ruff check .
ruff format --check .
```

This metrics example is a scoped software check, not biological evidence. Apply
[resource limits](machine_migration.md#shared-machine-execution) to heavy work.
Full `python -m pytest --receptor=llm tests` belongs to the qualified source route
and #9; earlier local whole-suite attempts reached1GiB, so do not retry them on
the shared machine. Hosted source, installed-file and public gates are separate.

Start with the owning issue/contract; preserve original results, update affected
capability/report/checkpoint and regenerate indexes. Authorized principal-
maintainer direct pushes remain available. New contributors do not inherit that
permission and normally use owner-reviewed PRs. A passing local check authorizes
neither a release nor an external report. See [decisions](decisions_and_workstreams.md).
