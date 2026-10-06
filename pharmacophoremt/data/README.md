# Data Arsenal - PharmacophoreMT

This directory contains the core knowledge bases and validation datasets for the toolkit.

## 1. Knowledge Bases

- **`smarts.py`**: Patterns used by legacy modelers. Native classical recognition is supplied by MolSysMT under the declared `classical_atomic_formal@1` definition.
- **`zinc.py`**: Mapping definitions for ZINC database tranches (MW and LogP bins).
- **`pdb_to_smi.pickle`**: A dictionary mapping PDB ligand IDs to canonical SMILES, used by `utils.chemistry.fix_bond_orders` to correct chemical identities from PDB files.

## 2. Validation Metadata

- **`datasets.yaml`**: The "Compass" for scientific validation. It links PDB codes to target families (Kinases, Nuclear Receptors, etc.) and provides bibliographical references for the expected pharmacophore models.

## 3. Reference Systems

### Complexes (`complexes/`)
Standard protein-ligand systems for `ComplexBasedModeler` testing:
- **`tests/data/eralpha_complex.pdb`**: Prepared OpenMM snapshot historically labeled ERalpha/estradiol. It is a legacy feature-presence regression fixture. Its chemical declarations are insufficient for the native workflow, and derivation from the historical 1QKU dataset label is unverified. See `tests/data/eralpha_audit.json`, the cookbook input-audit notebook and [issue #22](https://github.com/uibcdf/pharmacophoremt/issues/22).
- **`tests/data/eralpha_rcsb/`**: Independently acquired 1QKU and CCD EST inputs with URLs, checksums, entry revision and explicit ligand identity. Observed ligand coordinates contain 20 heavy atoms; chemical-template application and hydrogen-coordinate preparation remain pending.
- **`tests/data/prepared_ccd/`**: Untouched official ideal SDFs for EST and DES, with explicit hydrogens, source/checksum manifest and public MolSysMT preparation controls. These independent ligand reference geometries support native workflow checks; they are not experimental binding poses or a repair of the 1QKU ligand. See `devguide/prepared_ccd_validation.md` and issue #30.
- **`1m7w`, `4mww`, `1xdn`, `2reg`**: Diverse complexes covering various interaction types (Halogens, Metals, etc.).

### Ligand Sets (`ligand_sets/`)
Aligned and diverse molecule sets for `LigandBasedModeler` (Consensus) and `VirtualScreening` testing:
- **`hiv/`, `dhfr/`, `thrombin/`**: Classic drug-discovery benchmarks.
- **`Components-smiles-stereo-oe.smi`**: A large database of SMILES for high-throughput screening benchmarks.

### Dynamics and Ensembles (`dynamics/`)
Data for `DynamicModeler` and MSM testing:
- **`alanine-dipeptide.pdb`**: The "Hello World" of MD/MSM.
- **`igf_ligand_trajectory.sdf`**: A trajectory of conformers extracted from a molecular dynamics simulation of the Insulin Growth Factor.

## Usage in Tests
Most of these files are automatically accessed by the test suite in `tests/`. Developers can use them for demos via `phmt.io.load(phmt.data.PATH_TO_FILE)`.

The observed EST template integration uses `tests/data/eralpha_template`, a frozen
MolSysMT-curated chemical artifact without coordinates. Its acquisition manifest
links the provider origin and SHA-256 to the independently retained 1QKU/CCD
inputs. Public MolSysMT application preserves the deposited heavy-atom pose;
stored hydrogen counts do not provide donor-H geometry. See the observed EST
cookbook and `devguide/eralpha_validation.md` for the bounded controls.
