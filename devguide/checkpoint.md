# Development Checkpoint

**Current Status**: `Gen 1: Foundation (In Progress)`

This is a living document. Use it to quickly catch up on the project's state and identify the next tasks.

## 1. What's Done
- **Brand Transition**: Successfully renamed the package and updated all internal references.
- **Ecosystem Setup**: Integrated `pyunitwizard`, `argdigest`, `smonitor`, and `molsysmt` configurations and boilerplate.
- **Source of Truth**: Completed the `devguide/` with the "Tank" vision and technical standards.
- **Base Architecture**: Implemented the `InteractionSite` (Feature + Shape) composition pattern.
- **High-Resolution Arsenal**: Added new Features (Halogen, Metal, Cation-Pi) and Shapes (Disk, Cylinder).

## 2. Current Focus (Ongoing)
- **Compliance Application**: Decorating core classes and functions with `@arg_digest` and `@signal`.
- **I/O Hardening**: Finalizing the Pharmer JSON translator and preparing the LigandScout parser.


## 3. Up Next (To-Do for new developers)
- [ ] **Task 1**: Implement `to_ligandscout` and `from_ligandscout` in `pharmacophoremt/io/ligandscout.py`.
- [ ] **Task 2**: Implement specific digesters for `interaction_sites` and `molecular_system`.
- [ ] **Task 3**: Create the first set of physical invariance tests.

## 4. How to Continue
- Read `devguide/vision_and_scope.md` for the big picture.
- Check `devguide/api_design_standards.md` before writing code.
- Pick a task from the **Up Next** list and coordinate with the team.
