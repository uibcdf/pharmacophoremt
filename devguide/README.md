# Developer Guide - PharmacophoreMT

Welcome to the official developer guide for **PharmacophoreMT**. This directory is the "source of truth" for the toolkit's architecture, standards, and planning.

## Strategic Vision

[Architectural, scientific and product audit — 2026-11-04](audit_20261104.md)
records the discussed list of 17 improvement areas, priorities,
completion criteria and evidence limits. #73 is now fixed; continue with the
[current capability inventory](capability_inventory.md), scoped #6 contracts and
scientific study design. The first dispatch contract is now received; persistence
field/schema fidelity is the next bounded review.
Its [evidence and verification addendum](audit_20261104_review.md) records review
coverage, classified findings, method-level scientific limits and actionable checks.

1. [Vision and Scope](vision_and_scope.md): The project's "Constitution" and the four pillars of innovation.
2. [Roadmap](roadmap.md): Long-term strategic milestones from Gen 1b to Gen 4.
3. [Checkpoint](checkpoint.md): **Start here!** State as of 2026-11-04: capability inventory published; scoped modeling dispatch domain/aliases received with 290 focused checks. #73 remains fixed; #6 remains partial. Next: native persistence field/schema fidelity, then nested facade contracts. Molecular operations remain MolSysMT-owned; public/installed/platform/hosted gates stay separate. Addon deferred, public release still 0.4.0.

## Classical Workflow Specification

4. [Classical Workflow](classical_workflow.md): **The complete specification** of what must be implemented for a robust, scientifically rigorous classical pharmacophore pipeline — from molecular preparation through post-screening analysis. Read this before working on any Gen 1b task.

## Technical Standards

5. [Naming Conventions](naming_conventions.md): Rules for namespaces and brand transition.
6. [Core Architecture](core_architecture.md): Ecosystem standards, composition patterns, and viewer spec.
7. [API Design Standards](api_design_standards.md): Guidelines for `argdigest`, `smonitor`, and documentation.
8. [I/O and External Formats](io_and_formats.md): Interoperability with Pharmer, LigandScout, and others.
9. [Testing and Validation](testing_and_validation.md): Scientific rigor, physical invariance, enrichment factors, and ROC.

## Modeling Domains

10. [Modeling Strategies](modeling_strategies.md): Ligand, Structure, and Complex-based approaches — full specification including Gen 1b requirements.
11. [Dynamics and MSM](dynamics_and_msm.md): Dynophores, kinetics, and Markov State Models (Gen 2).
12. [Specialized Modeling](specialized_modeling.md): Peptides, Covalent inhibitors, and Water networks (Gen 3).
13. [AI & Data Science](ai_and_data_science.md): Graph exports, Diffusion blueprints, and 3DPFs (Gen 4).
14. [Visualization Strategies](visualization_strategies.md): Programmatic and Add-on integration with MolSysViewer.

---

**Current priority:** Gen 1b — Classical Consolidation. See [checkpoint.md](checkpoint.md) and [classical_workflow.md](classical_workflow.md).

**Philosophy:** Interoperability, Physical Rigor, Atomized Design, AI-Ready.

## Issue records

Open defects are listed in [pending_bugs](pending_bugs/README.md), and open
proposals in [pending_proposals](pending_proposals/README.md); resolved reports
remain in the permanent [archive](archive/README.md). Follow the
[local reporting protocol](reporting_protocol.md), which implements the
[MolSysSuite reporting protocol](https://github.com/uibcdf/molsyssuite/blob/main/devguide/reporting_protocol.md).
