# Developer Guide - PharmacophoreMT

Welcome to the official developer guide for **PharmacophoreMT**. This directory is the "source of truth" for the toolkit's architecture, standards, and planning.

## Strategic Vision

[Architectural, scientific and product audit — 2026-11-04](audit_20261104.md)
records the discussed list of 17 improvement areas, priorities,
completion criteria and evidence limits. #73 is now fixed; continue with the
[current capability inventory](capability_inventory.md), scoped #6 contracts and
scientific study design. Native schema/writer checks are now received under #76;
live references/variants are now qualified under #60; legacy merge #77 is now fixed through public composition; nested facade
admission is now received, with broader #6 adoption still partial. Scientific
semantics/provenance under audit items 8–9 now has a [qualified native slice](native_constraint_semantics.md) under #79 and a [consensus support/redundancy review](consensus_support_review.md) under #80; broader coverage stays partial. [Native I/O diagnostics/dependencies](native_io_diagnostics.md) are now repaired under #81/#6.
[Native I/O ArgDigest receiving](native_io_admission_readiness.md) is now gated
under #82 by the published ArgDigest #47/#48 issues; legacy compatibility passes
do not fix the measured current model-source replacement defect.
Its [evidence and verification addendum](audit_20261104_review.md) records review
coverage, classified findings, method-level scientific limits and actionable checks.
The first [receptor projection sensitivity protocol](receptor_sensitivity_protocol.md)
is now qualified under #83; #84 repairs a measured unit-policy radius-boundary
defect. Audit item 12 remains partial beyond this analytical slice.
The [prepared ERalpha sensitivity extension](prepared_receptor_sensitivity_protocol.md)
under #85 now applies that methodology to the original cached receptor geometry.
The first [cached receptor hypothesis-generation pilot](receptor_hypothesis_pilot_protocol.md)
under #86 now qualifies eight donor/ring alternatives and explicit enumeration
budgets, using MolSysMT geometry without a new public API. Further direction
profiles and optional pockets are requested in MolSysMT #375 and TopoMT #101.
Its [public cached builder](public_receptor_generation.md), #87, now supports
multiple donor/ring occurrences and explicit bounded alternatives in development
source, with 192 passing selected controls (54 new). Molecular geometry remains
MolSysMT-owned; public delivery and broader scientific qualification are separate.
Optional [cached generation exclusions](receptor_generation_exclusions.md), #88,
now preserve separate hypotheses and explicit veto semantics (217 selected cases,
61 new); source-declaration compatibility remains distinct from source authenticity.

1. [Vision and Scope](vision_and_scope.md): The project's "Constitution" and the four pillars of innovation.
2. [Roadmap](roadmap.md): Long-term strategic milestones from Gen 1b to Gen 4.
3. [Checkpoint](checkpoint.md): **Start here!** State as of 2026-11-05: #94 delivers explicit experimental public cached-carbonyl generation, with 295 unique passing selected controls across preserved scopes (final run 114), unchanged 12-model/72-primary/24-recovery replay and three executed cookbook blocks. Molecular operations remain MolSysMT-owned; default feature/profile compatibility and prior science are preserved. Next #95 consolidates the proposed [0.5.0 candidate](release_0_5_0_readiness.md) along the [release staircase](roadmap.md). Latest observed tag/Release remains 0.4.0; no new publication. Wider scientific/data/hosted/installed/public gates stay separate.

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
