# I/O and External Formats

Current implementation/fidelity is defined by [capabilities](capability_inventory.md),
[native schema](native_schema.md) and [persistence matrix](persistence_fidelity.md).
The interoperability tiers and high-performance layout below are design plans,
not evidence that every translator or format is implemented.

## Native schema received — 2026-11-04

New native JSON/YAML use [pharmacophoremt.native@1](native_schema.md). Explicit
schema/field admission and validation/encoding-before-open are received under
#76; legacy untagged reads retain their documented scope. SDF container and
payload remain unchanged, with molecular ownership migration still #74.

## Ownership and validation review — 2026-11-04

See the [field/schema matrix and ownership review](persistence_fidelity.md).
#75 fixes native scientific-value validation. #74 tracks the existing SDF
container migration to MolSysMT #215; direct RDKit container code remains
frozen migration debt. Earlier semantic qualification does not establish
architectural compliance. No new molecular codec is added.

This document defines the architecture for interoperability and the supported formats for PharmacophoreMT.

## Current generic loader contract — 2026-11-04

`io.load(file_name, **kwargs)` requires a string path. It dispatches `.pml` to
LigandScout, `.json` to native JSON when `software == "pharmacophoremt"` and to
Pharmer otherwise, and `.yaml`/`.yml` to native YAML. Extra options reach the
selected reader; these readers currently have closed signatures, so unknown
keywords raise TypeError. JSON classification reads the file before this check.
Valid calls retain their existing results and parsing errors.

Other extensions delegate to `molsysmt.convert(..., to_form="molsysmt.MolSys",
**kwargs)`. MolSysMT owns their admitted options, molecular representation and
conversion. Provider exceptions propagate unchanged: callers must not rely on
the former blanket ValueError replacement. The facade does not auto-detect
PharmacophoreMT's annotated SDF; use explicit `load_sdf` for that format.

[Dispatch evidence](evidence/native_loader_dispatch_20261104_summary.json) covers
five pharmacophore routes and a real minimal molecular SDF through MolSysMT.
The priorities and format specifications below include planned capabilities;
they are not an implemented-capability inventory. Broader format fidelity and
schema admission remain audit items 2/4.

## 1. Interoperability Roadmap

PharmacophoreMT aims to be the universal bridge between pharmacophore modeling tools. We categorize external support into three priority tiers:

### Tier 1: High Priority (Gen 1 & 2)
Fundamental for the Python/Open-Source ecosystem and academic standards.
- **LigandScout (.pml)**: Structured XML. Support for projected sites and directional vectors.
- **Pharmit/Pharmer (.json)**: The ideal intermediate exchange format. Clean, hierarchical, and easily extensible.
- **RDKit (Objects)**: Direct in-memory transformation between `pharmacophoremt.Pharmacophore` and `rdkit.Chem.rdPharmacophore`.
- **JSON / YAML**: High-fidelity exchange format using standard extensions but identified by an internal `software: pharmacophoremt` tag.

### Tier 2: Medium Priority
Ensuring compatibility with legacy models and general-purpose tools.
- **ZINCPharmer (.phar)**: Lightweight text representation used by the ZINC database tools.
- **Annotated SDF (.sdf)**: A universal fallback where pharmacophore features are stored as molecular properties (SD tags).
- **OpenEye ROCS**: Support for hybrid shape-pharmacophore models.

### Tier 3: Low Priority (Industry Legacy)
Focus on conversion rather than direct native parsing of binary formats.
- **MOE (.ph4)**: Proprietary binary. Target: support via intermediate exporters or CLI converters.
- **Schrödinger Phase (.phypo)**: Proprietary binary. Target: extraction of hypotheses via CSV/JSON exports.
- **Discovery Studio (.chm, .pharm)**: Semi-structured legacy format.
- **Pharao**: Academic format focused on pharmacophore alignment.

## 2. High-Performance Storage: .h5phmt

An HDF5-based `.h5phmt` layout is proposed for future pharmacophore ensembles.
There is no qualified current reader/writer or runtime storage promise for this
layout. Molecular trajectory formats and operations remain MolSysMT-owned.

### Hierarchical Structure:
- `/metadata`: Global info, MolSysMT source, physical units.
- `/sites`: Definitions of InteractionSites (Features + Shape templates).
- `/dynamics`:
    - `coordinates`: `(n_frames, n_sites, 3)` dataset.
    - `weights`: Statistical occupancy data.
- `/msm`: Kinetic matrices, populations, and metastable macrostate centroids.

## 3. Current native JSON/YAML contract

Use `load_json`/`to_json` and `load_yaml`/`to_yaml` with the complete
[pharmacophoremt.native@1 schema](native_schema.md). New writes include the
schema marker, producing version, model/site/shape fields, explicit quantities
and metadata defined there. A `software`/`version` pair alone is not a complete
tagged record. Historical untagged admission retains only its documented
compatibility scope; do not create new files from an old illustrative sketch.
Use public writers and the [field-fidelity matrix](persistence_fidelity.md),
rather than a second hand-maintained payload example here.

## 4. The Translator Pattern
Each format is handled by a specialized **Translator**:
- **Readers**: Extract data and convert Ångströms/degrees to internal standard Units (nm/dimensionless) using `pyunitwizard`.
- **Writers**: Map internal `InteractionSite` attributes back to the target format's specific nomenclature and coordinate systems.

## 5. Mapping Tables
A central registry in `pharmacophoremt.io.mapping` ensures that feature names are consistent across softwares (e.g., mapping our `hb donor` to LigandScout's `HBD` or Pharmer's `HydrogenDonor`).
