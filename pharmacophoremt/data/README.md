# Data Arsenal - PharmacophoreMT

This directory contains the core knowledge bases and validation datasets for the toolkit.

## 1. Knowledge Bases

- **`smarts.py`**: The definitive catalog of SMARTS patterns for chemical feature detection (Donors, Acceptors, Aromaticity, etc.).
- **`zinc.py`**: Mapping definitions for ZINC database tranches (MW and LogP bins).
- **`pdb_to_smi.pickle`**: A dictionary mapping PDB ligand IDs to canonical SMILES, used by `utils.chemistry.fix_bond_orders` to correct chemical identities from PDB files.

## 2. Validation Metadata

- **`datasets.yaml`**: The "Compass" for scientific validation. It links PDB codes to target families (Kinases, Nuclear Receptors, etc.) and provides bibliographical references for the expected pharmacophore models.

## 3. Reference Systems

### Complexes (`complexes/`)
Standard protein-ligand systems for `ComplexBasedModeler` testing:
- **`eralpha_complex.pdb`**: Estrogen Receptor alpha with Estradiol. A gold standard for H-bonds and hydrophobic stacking.
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
