# Core Architecture

This document defines the foundational design patterns, data structures, and ecosystem integration standards for PharmacophoreMT.

## 1. MolSysSuite Integration
PharmacophoreMT is a citizen of the MolSysSuite ecosystem and must adhere to the following standards:

### Infrastructure & Robustness
- **argdigest**: All public API boundaries must use `@arg_digest` to ensure input normalization and strict contracts.
- **smonitor**: Centralized diagnostics. All errors/warnings must be cataloged with `PHMT` codes for traceability.
- **depdigest**: Managing soft dependencies. Features requiring heavy external libraries (e.g., specific XML parsers for LigandScout) must be lazy-loaded.
- **pyunitwizard**: The "unit customs". No raw floats are allowed for physical magnitudes; everything must be a `Quantity`.

### Molecular Data & Analysis
- **molsysmt**: The unique source of truth for molecular data. PharmacophoreMT will not implement its own topology or coordinate handling; it will use `molsysmt` to query and manipulate systems.
- **topomt**: Used in structure-based workflows to identify cavities, pockets, and tunnels. These analytical results inform the placement of "Included" and "Excluded" volume elements.
- **elasnetmt**: Integration for stability analysis. Using Elastic Network Models to evaluate the local flexibility of the receptor around a pharmacophore feature, helping to score or weight features based on their structural persistence.
- **molsysviewer**: The visual hub. PharmacophoreMT communicates with Mol* via the dedicated `molsysviewer-pharmacophoremt` addon for high-performance vectorized rendering.

## 2. Element Composition Pattern
A pharmacophore point is the union of a `Feature` (Chemical property) and a `Shape` (Geometric representation). 
- **Atomic Design**: This separation allows adding new shapes (e.g., Density Isosurfaces) or features (e.g., Covalent Warheads) without modifying the core element logic.

## 3. MolSysMT Form Contract
The `Pharmacophore` class will be registered as a native MolSysMT form. This enables interoperability:
- `msm.get(pharmacophore, n_elements=True)`
- `msm.convert(pharmacophore, to_form='molsysmt.MolSys')` (when applicable).

## 4. MolSysViewer Addon: molsysviewer-pharmacophoremt
Visualization is handled by a dedicated addon for `molsysviewer`.
- **Vectorized Rendering**: Uses Mol* primitives for high-performance rendering of large ensembles.
- **Protocol**: Communication happens via JSON messages over `anywidget`.
- **Mapping**: standard colors and kinds (donor, acceptor, aromatic, etc.) are synchronized with `pharmacophoremt` feature names.
