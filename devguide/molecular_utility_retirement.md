# Retired molecular utilities and library reader

Owned by [#46](https://github.com/uibcdf/pharmacophoremt/issues/46), under the
broader molecular ownership audit #41. General molecular preparation, recognition,
geometry, transformations and molecular codecs belong in MolSysMT. After the
native consumer transitions, the following orphaned implementations are removed;
their import paths no longer supply operations or silent compatibility fallbacks.

| Retired module | Removed operations | Current consumer/provider route |
| --- | --- | --- |
| `utils.conformers` | H addition, RDKit embedding/minimization/RMSD pruning | Supply prepared frames to `ConformerScreening`; reusable fixed-state generation remains MolSysMT #219 |
| `utils.preparation` | Salt/charge/stereo changes, sanitization, SMILES parsing, descriptors and implicit library filters | Molecular conversion through MolSysMT; optional explicit standardization requested in #366. No native descriptor/filter replacement is claimed |
| `utils.chemistry` | PDB-ID lookup and bond-order assignment with silent fallback | Prepared declared chemistry and public MolSysMT assessment/template application; #298 is delivered |
| `utils.alignment` | RDKit fitting, principal axes and ligand embedding | PHMT's public correspondence/alignment/search tools delegate molecular fitting and transforms to MolSysMT |
| `utils.maths` | Molecular ring normal, angle/distance/projection and orphaned bin helper | Native consumer geometry calls public MolSysMT tools; no generic geometry compatibility is promised |
| `data.ligand_sets.read_sdf` | RDKit multi-record parsing and conformer assembly grouped only by `_Name` | Collection/property fidelity and atom correspondence need a provider-owned contract (#215 follow-up / #223); no collection replacement is claimed |

The empty `utils/__init__.py` is removed too. Pure NumPy arithmetic in
pharmacophoric hypothesis/assignment tools is a separate PHMT responsibility.
This retirement neither forbids NumPy/RDKit imports generally nor relocates PHMT's
feature/shape model into a molecular provider.

## Source and historical consumers

Inspection of the preceding source
`0f5819d79877288c7436ba2daf4cb6d222cd9cbe` found no package runtime callers of the
five utilities. The #45 screening test was the only utility test consumer; it now
guards against loading a retired backend rather than preserving its implementation.

`data/ligand_sets/thrombin.ipynb` still contains `from read_sdf import read_sdf`
and invokes it conditionally. All three ligand-set notebooks use historical
`openpharmacophore` APIs. They are retained unchanged as archives, not current
executable PHMT preparation or biological validation workflows. The reader's
removal is an explicit incompatibility for that historical workflow. A future
current recipe must establish collection identity, source atom maps, declared
states and prepared frames through qualified provider tools. Equal record names
do not establish one molecule or valid conformer correspondence.

The old code remains inspectable in Git at the preceding source and its original
hashes/source are retained in the owning review evidence. Molecular fixtures and
historic notebook outputs are not rewritten. The old PDB-to-SMILES dictionary
is retained historical data and has no current utility caller.

## Kept PHMT contracts and remaining work

`io.rdkit` and the annotated `io.sdf` format encode pharmacophore virtual sites,
features and shapes. They remain PHMT-owned; they are not replacements for
molecular library ingestion/export. Existing model codec controls remain applicable;
annotated SDF semantic loss is independently reproduced and tracked in #47, with
no full-shape/constraint-fidelity claim from this retirement.

Dated follow-up (2026-10-10): #47 defines and guards the separate versioned
[persistence contract](pharmacophore_sdf_persistence.md). The original unversioned
SDF defect and #46 measurement remain historical evidence; only the new versioned
carrier preserves its explicitly supported scientific fields.

Native prepared modeling/screening remain the routes documented in
[the modeler contracts](ligand_based_workflow.md),
[complex construction](complex_based_workflow.md),
[receptor projections](structure_based_workflow.md) and
[screening](virtual_screening_workflow.md). Removing unused utilities does not
generate prepared inputs or qualify a biological dataset.

The complete distribution resource inventory removes exactly seven paths;
all retained files stay inventoried. Installed-package checks use that current
inventory; local source checks do not prove a released/installed artifact.
`tests/test_molecular_ownership.py` guards retired imports/runtime callers and
retained consumer/codec availability; existing native tests guard actual behavior.

#41 remains partial for donor-H displacement/normalization inside native feature
extraction. Public donor-pair geometry is requested in MolSysMT #375, with the
existing bounded review/retention conditions in the owning audit. The source
retirement does not resolve environmental H refinement (#323), aromatic rejected
candidate diagnostics (#350), arbitrary-fit degeneracy (#367), preparation or
molecular collection gaps. Provider improvements must be developed in their
repositories and consumed here after contract qualification.
