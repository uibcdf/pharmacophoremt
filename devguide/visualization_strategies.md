# Visualization Strategies

This document defines the integration roadmap between **PharmacophoreMT** and **MolSysViewer**, ensuring a high-performance and interactive experience.

## Strategy 1: Programmatic Native Bridge
*Target: Power users and developers working in Jupyter Notebooks.*

The core `Pharmacophore` class will implement a direct bridge to the Mol* engine via MolSysViewer.

### Implementation Plan:
1. **Vectorized Data Transfer**: Implement `Pharmacophore.add_to_molsysviewer(view)`. Instead of drawing sites one by one, it will prepare a single payload containing centers, radii, and directions for all sites.
2. **Dynamic Updates**: Ensure that if the pharmacophore is modified in Python, the viewer can update the specific "layer" or "tag" without reloading the whole scene.
3. **Smart Defaults**: Automatic mapping of `InteractionSite` features to the official `PHARM_COLORS` of the Suite.

## Strategy 2: Specialized UI Add-on (`molsysviewer-pharmacophoremt`)
*Target: End users performing interactive analysis and modeling.*

A dedicated Python package that extends the MolSysViewer interface with specific GUI components.

### Implementation Plan:
1. **Interaction Panel**: A side panel to list all `InteractionSites`, toggle their visibility by type, and adjust global parameters (e.g., "Show only essential sites").
2. **Contextual Actions**:
    - Right-click on a ligand: *"Generate Complex-Based Pharmacophore"*.
    - Right-click on a pocket: *"Extract Structure-Based Projections"*.
3. **Interactive Labeling**: Linking 3D glyphs to their biological origin (residues/atoms) via Mol* tooltips.

## Proposed Changes for MolSysViewer API

To maintain consistency with the new **InteractionSite** terminology, we propose the following changes to the `molsysviewer.shapes` module:

| Current Method | Proposed Method | Justification |
| :--- | :--- | :--- |
| `add_pharmacophore_features` | `add_interaction_sites` | "Feature" now refers only to the chemical identity. The visual glyph represents the whole "Site". |
| `PHARM_COLORS` | `INTERACTION_COLORS` | Align with the new naming convention. |

**Status**: These changes should be implemented in `molsysviewer` first to provide a clean API for `pharmacophoremt`.
