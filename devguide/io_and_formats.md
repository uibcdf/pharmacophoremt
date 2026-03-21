# I/O and External Formats

This document defines the architecture for interoperability and the supported formats for PharmacophoreMT.

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

For large-scale data (MD trajectories, Dynophores, and MSM networks), PharmacophoreMT uses the **HDF5-based .h5phmt format**.

### Hierarchical Structure:
- `/metadata`: Global info, MolSysMT source, physical units.
- `/sites`: Definitions of InteractionSites (Features + Shape templates).
- `/dynamics`:
    - `coordinates`: `(n_frames, n_sites, 3)` dataset.
    - `weights`: Statistical occupancy data.
- `/msm`: Kinetic matrices, populations, and metastable macrostate centroids.

## 3. JSON / YAML Exchange Format Specification

For human-readable exchange, we use standard JSON or YAML files with an internal identity marker.

### Functions:
- `load_json`, `to_json`
- `load_yaml`, `to_yaml`

### Internal Identity Tag:
Any file MUST contain the following root keys to be recognized by these functions:
- `software: "pharmacophoremt"`
- `version: "0.1.0"` (or current version)

### Example (.yaml):
```yaml
software: pharmacophoremt
version: 0.1.0
name: "My Binding Model"
interaction_sites:
  - features: ["hb donor", "hb acceptor"]
    shape:
      type: sphere
      center: [1.2, 3.4, -0.5] # in nm
      radius: 0.15
    metadata:
      importance: 1.0
```

## 4. The Translator Pattern
Each format is handled by a specialized **Translator**:
- **Readers**: Extract data and convert Ångströms/degrees to internal standard Units (nm/dimensionless) using `pyunitwizard`.
- **Writers**: Map internal `InteractionSite` attributes back to the target format's specific nomenclature and coordinate systems.

## 5. Mapping Tables
A central registry in `pharmacophoremt.io.mapping` ensures that feature names are consistent across softwares (e.g., mapping our `hb donor` to LigandScout's `HBD` or Pharmer's `HydrogenDonor`).
