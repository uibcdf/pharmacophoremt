# Modeling Strategies and the Modeler Engine

This document defines the architecture for pharmacophore generation in PharmacophoreMT through the **Modeler** engine.

## 1. The Modeler Philosophy

PharmacophoreMT separates the **data storage** (`Pharmacophore` class) from the **modeling logic** (`Modeler` classes). This modularity allows for complex algorithms to evolve without bloating the core data structures.

### The Modeler Interface
All modeling engines follow a common workflow:
1. **Initialize**: Provide the molecular system and target entities.
2. **Configure**: Set distance cutoffs, feature types to include, etc.
3. **Build**: Execute the algorithm and return a `Pharmacophore` object.

## 2. Modeler Specializations

### LigandBasedModeler
- **Inputs**: Multiple molecules or conformations.
- **Goal**: Find the **Consensus Pharmacophore** (the common denominator of binding).
- **Features**: Alignment-driven, support for negative modeling (inactives), and weighting based on experimental affinity.

### ComplexBasedModeler
- **Inputs**: A protein-ligand complex.
- **Goal**: Extract interactions directly from the 3D contact geometry.
- **Features**: Distance and angle rules for H-bonds, salt bridges, and pi-stacking.

### StructureBasedModeler
- **Inputs**: A receptor structure (usually without a ligand).
- **Goal**: Identify potential interaction sites from the pocket topography.
- **Features**: Powered by `topomt` for cavity detection and water network analysis.

### DynamicModeler
- **Inputs**: Molecular dynamics trajectories (multiple frames).
- **Goal**: Discover **Metastable Pharmacophoric States** (Dynophores).
- **Features**: Integrated with the **MSM Engine** to identify kinetic arquetypes.

## 3. The High-Level API (phmt.model)

For zero-friction usage, a convenience function delegates to the appropriate Modeler:

```python
import pharmacophoremt as phmt

# Automatic detection of method based on input
ph = phmt.model(molecular_system, method='complex-based')
```

## 4. Automatic Entity Recognition

Modelers are designed to be "smart" by identifying the roles of molecules within a system automatically (rescuing logic from legacy `ligand.py` and `protein.py`):
- **Ligand Recognition**: Identifying small molecules based on atom count and residue naming.
- **Receptor Recognition**: Identifying protein/nucleic chains.
- **Cofactor/Ion Handling**: Deciding whether to include them as part of the receptor or ignore them.

## 5. Implementation Status

| Component | Status | Source/Legacy Reference |
| :--- | :--- | :--- |
| **Modeler Base** | Planned | New Suite Pattern |
| **LigandBased** | Rescuing | `pharmacophore/ligand_based/` |
| **ComplexBased**| Rescuing | `pharmacophore/ligand_receptor/` |
| **StructureBased**| Planned | Integration with `topomt` |
| **Dynamic** | Planned | New MSM native engine |
