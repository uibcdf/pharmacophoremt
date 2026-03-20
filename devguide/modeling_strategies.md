# Modeling Strategies

This document details the fundamental approaches for pharmacophore generation and the classical 3D canon supported by PharmacophoreMT.

## 1. Core Methodologies

### Ligand-Based Modeling
- **Alignment-driven**: Generation from sets of active molecules.
- **Negative Modeling**: Using inactive molecules to define **Excluded Volumes** where ligand atoms should not be present.
- **Pseudo-receptors**: Building hypothetical binding pockets (van der Waals envelopes) based on ligand overlays when the receptor structure is unknown.

### Structure-Based (Receptor) Modeling
- **Pocket Analysis**: Using `topomt` to identify cavities and potential interaction sites.
- **Water Network Analysis**: Deriving features from high-energy hydration sites.
- **Volume Constraints**: Defining the receptor's boundary to ensure ligands do not clash with the protein.

### Complex-Based Modeling
- **Direct Interactions**: Identifying H-bonds, hydrophobic contacts, and pi-stacking from protein-ligand complexes.
- **Ensemble Consensus**: Merging interaction patterns from multiple static structures (X-ray, NMR) to find conserved (intersection) or alternative (union) binding modes.

## 2. The 3D Modeling Canon

PharmacophoreMT implements the following classical high-level concepts:

- **InteractionSite Essentiality**: Support for **Boolean Logic** (Essential vs. Optional sites) and **Weighting** (prioritizing specific interactions).
- **Geometric Constraints**: Explicitly defining required distances, angles, and dihedrals between specific `InteractionSites`.
- **Shape-Based Matching**: Using the molecular "envelope" or volume as a global shape constraint, complementing the discrete interaction sites.
- **Fragment-Based Anchors**: Minimalist, high-precision models (2-3 sites) designed for fragment-based drug discovery (FBDD) and scaffold hopping.

## 3. Hybrid Strategies
PharmacophoreMT allows for merging these approaches (e.g., validating a ligand-based model against a receptor-derived pocket) to create highly robust and biologically relevant models.
