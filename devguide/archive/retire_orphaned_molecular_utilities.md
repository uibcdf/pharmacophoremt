---
summary: Retire unused molecular utilities and the name-grouped archival SDF reader.
issue: uibcdf/pharmacophoremt#46
status: resolved
opened: 2026-10-10
closed: 2026-10-10
verification: measured
area: [architecture, data, distribution]
guard: tests/test_molecular_ownership.py
normative: devguide/molecular_utility_retirement.md
blocked_by: []
supersedes: []
---

# Molecular utility and legacy library-reader retirement

## What

Independently retire `utils/{alignment,chemistry,conformers,maths,preparation}.py`,
the empty utilities initializer and `data/ligand_sets/read_sdf.py` after #18,
#42, #44 and #45 migrated their library consumers. #41 remains partial for the
native donor geometry gap requested in MolSysMT #375.

## How

Remove orphaned implementations and the name-grouped SDF reader, without adding
a replacement molecular kernel or compatibility shim. Update distribution's
complete resource inventory and replace the old test-only conformer dependency
with a guard against loading retired backends. Document external import changes
and the exact historical notebook consumer. Preserve data/notebook bytes and
prior scientific evidence. Keep PHMT's pharmacophore/virtual-site codecs.

## Why

The utilities perform general preparation, descriptor calculation, fitting,
embedding and molecular geometry. Those operations belong in MolSysMT. The reader
assembles conformations by `_Name`, which is not a declaration of molecular graph
or atom correspondence. Leaving importable orphaned kernels invites new callers
to bypass the explicit native contracts.

## What is measured and what is assumed

Source inspection at `0f5819d79877288c7436ba2daf4cb6d222cd9cbe` finds no library
runtime consumers of the five utility modules. The sole test reference poisons
the old conformer generator. `thrombin.ipynb` does import and invoke `read_sdf`
while using historical `openpharmacophore`; it is an archival consumer. This is
not an unused-everywhere claim, fresh execution of that notebook or a new SDF
defect reproduction. Focused import/native regression and complete distribution
checks will qualify this removal; upstream/public/biological qualification is separate.

## Alternatives and refuted paths

Do not reimplement standardization, descriptors or a collection codec locally.
Do not forward the reader to a single-record adapter and claim collection/property
equivalence. Do not mutate historic notebooks or remove valid pharmacophore
codecs merely because they import RDKit. Existing molecular issues are reused,
not duplicated or broadened beyond their provider-owned acceptance.

## Scope and exclusions

Seven code files, their inventory paths, bounded guards and maintained guidance.
Molecular datasets and all archived output are retained. No provider modifications,
dependency/source pin changes, release selection or scientific method extension.
The independently reproduced annotated pharmacophore SDF semantic loss is #47;
its PHMT codec repair remains outside this retirement's acceptance.

## Acceptance criteria

Retired module imports fail, no package runtime import targets them, native
modeler/screening and PHMT codec regressions pass, retained data/previous evidence
remain byte-identical, the current complete distribution inventory and reporting
gates pass, and external/archival consumers have an explicit retirement contract.

## Executed resolution — 2026-10-10

The seven source files and all seven distribution inventory paths are removed;
no shim or generic molecular replacement is added. The normal editable Python
3.14.7 tree passes **249 focused tests in 126.92 s**, covering retired imports,
runtime caller scanning, all three modeler facades, placed/rigid/prepared-conformer
screening, retrospective accounting, optional attribution and retained PHMT
model codecs. One pytest warning belongs to the deliberately failed optional
Ackredit provider. The earlier 35-test guard also passes.

Five actual native cookbook examples execute: prepared conformers/facade (4
blocks), retrospective validation (1), ligand modeler (2), complex modeler (3)
and receptor projections (3). Original wrapper output retains two provider
warnings that the unchanged ligand SDF fixtures are tagged 2D despite nonzero Z.
No full-site or new scoped renderer result is claimed. Reporting/index/archive,
23 administrative distribution/helper guards, 7 CI-route guards, declared
provider/environment routes and Ruff/format pass. The complete inventory is
**171 committed files plus generated version = 172 paths**.

The [original review summary](../evidence/molecular_utility_retirement_review_py314_summary.json)
links the immutable gzip archive with retired source bytes/hashes, baseline,
full test/admin output, JUnit, driver, source/fixture identities, provider heads
and native binary inventory. Sources/binaries/recorded inputs remained unchanged
during measurement; all **66 retained data/notebook files** and **24 previous
gzip archives** remain byte-identical. The owned review context includes both
pytest base directories and the SDK clone, all removed on exit. The
[completion receipt](../evidence/molecular_utility_retirement_completion.json)
retains full wrapper output and post-archive reporting/cleanup evidence.

#47 remains independently open for the measured annotated pharmacophore SDF
field loss. Its probe's producer provenance was recorded after execution; the
unchanged codec is verified against the source base and the original source/output
is retained. This retirement does not certify SDF semantic fidelity, full hosted
matrices, installed/released artifacts, biological results or performance.
#41 remains partial for native donor geometry requested in MolSysMT #375.
