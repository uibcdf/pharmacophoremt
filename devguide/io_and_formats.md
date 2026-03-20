# I/O and External Formats

This document defines the architecture for interoperability between PharmacophoreMT and external pharmacophore modeling software.

## 1. The Translator Pattern
To avoid complex conditional logic, PharmacophoreMT uses a **Translator** pattern:
- **Reader**: Converts external data (JSON, XML, etc.) into a list of internal `Element` objects (Feature + Shape).
- **Writer**: Maps internal `Element` objects back to the external software's specific feature definitions and coordinate systems.

## 2. Feature Mapping Tables
Each translator must maintain a mapping table to ensure chemical consistency.
- **Pharmer**: Mapping `Aromatic` to `AromaticRingSphereAndVector`.
- **LigandScout**: Mapping `H-Bond Donor` to `HBDonorSphereAndVector`.

## 3. Coordinate System and Units
- All external coordinates MUST be converted to internal standard units using `pyunitwizard` during the reading phase.
- Translational or rotational offsets in external formats must be normalized to ensure the pharmacophore is correctly aligned with the `molecular_system` (via `molsysmt`).

## 4. Supported Formats (Current & Planned)
- **Pharmer (.json)**: Native support for reading/writing.
- **LigandScout (.pml)**: Planned support for XML-based models.
- **MOE**: Future research for feature-based integration.
