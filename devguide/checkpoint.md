# Development Checkpoint

**Current Status**: `Gen 1: Foundation (COMPLETED)`

This is a living document. Use it to quickly catch up on the project's state and identify the next tasks.

## 1. What's Done
- **Brand Transition**: Successfully renamed the package and updated all internal references.
- **Ecosystem Setup**: Integrated `pyunitwizard`, `argdigest`, `smonitor`, and `molsysmt`.
- **Source of Truth**: Completed the `devguide/` with the "Tank" vision and technical standards.
- **Base Architecture**: Implemented the `InteractionSite` (Feature + Shape) composition pattern.
- **High-Resolution Arsenal**: Added new Features (Halogen, Metal, Cation-Pi) and Shapes (Disk, Cylinder).
- **Modeling Engines**: Implemented `ComplexBasedModeler`, `LigandBasedModeler` (Consensus), and `StructureBasedModeler` (Projections).
- **Interoperability**: Completed translators for Pharmer, LigandScout, RDKit, SDF, and PHMT (JSON/YAML).
- **Rescue Operation**: 100% of the logic and data from legacy repositories has been migrated and refined.
- **Visual Integration**: Official programmatic bridge with `molsysviewer` implemented (RFC-001 compliant).

## 2. Current Focus (Ongoing)
- **Scientific Validation**: Expanding the test suite using the `tests/data/` benchmarks.
- **Documentation**: Finalizing the "Showcase" examples in the docs.

## 3. Up Next (To-Do for Gen 2: Dynamics)
- [ ] **Task 1**: Implement the `TrajectoryExtractionPipeline` to generate pharmacophore lists from MD.
- [ ] **Task 2**: Design the native MSM engine for metastable state discovery.
- [ ] **Task 3**: Create the specialized UI Add-on `molsysviewer-pharmacophoremt`.

## 4. How to Continue
- Read `devguide/vision_and_scope.md` for the big picture.
- Check `devguide/api_design_standards.md` before writing code.
- Coordinate with the team for the Gen 2 architecture.
