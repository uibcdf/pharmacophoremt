# Development Checkpoint

**Current Status**: `Gen 1: Foundation (In Progress)`

This is a living document. Use it to quickly catch up on the project's state and identify the next tasks.

## 1. What's Done
- **Brand Transition**: Successfully renamed the package and updated all internal references.
- **Ecosystem Setup**: Integrated `pyunitwizard`, `argdigest`, `smonitor`, and `molsysmt`.
- **Source of Truth**: Completed the `devguide/` with the "Tank" vision and technical standards.
- **Base Architecture**: Implemented the Feature + Shape composition pattern for basic interaction sites.

## 2. Current Focus (Ongoing)
- **I/O Hardening**: Finalizing the Pharmer JSON translator and preparing the LigandScout parser.
- **Unit Testing**: Implementing the first set of physical invariance tests.

## 3. Up Next (To-Do for new developers)
- [ ] **Task 0**: Refactor `Element` to `InteractionSite` in the codebase (modules, classes, and variables) to align with the new terminology.
- [ ] **Task 1**: Implement `to_ligandscout` and `from_ligandscout` in `pharmacophoremt/io/ligandscout.py`.
- [ ] **Task 2**: Create the `_argdigest.py` configuration and apply it to the `Pharmacophore` class constructor.
- [ ] **Task 3**: Draft the `_smonitor.py` diagnostic catalog for common I/O errors.

## 4. How to Continue
- Read `devguide/vision_and_scope.md` for the big picture.
- Check `devguide/api_design_standards.md` before writing code.
- Pick a task from the **Up Next** list and coordinate with the team.
