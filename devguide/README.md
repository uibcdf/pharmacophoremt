# Developer Guide - PharmacophoreMT

Welcome to the official developer guide for **PharmacophoreMT**. This directory is the "source of truth" for the toolkit's architecture, standards, and planning.

## Strategic Vision

1. [Vision and Scope](vision_and_scope.md): The project's "Constitution" and the four pillars of innovation.
2. [Roadmap](roadmap.md): Long-term strategic milestones from Gen 1b to Gen 4.
3. [Checkpoint](checkpoint.md): **Start here!** State as of 2026-11-03: #41's observed donor-vector caller is migrated to MolSysMT with shared receiving validation. Clean code 6a7537b passes 418 modern and 14 original-public-payload controls plus composition/CCD drivers; all phase identities are stable. Next accept #34 aromatic queries. #41's supported-public/installed migration and final old-provider fallback removal remain partial (review 2026-11-11). #66 awaits four original methods; #60 is available for a concrete variant. Quota/resource retirement and earlier #82 limits are explicit; hosted/public gates remain separate. Public release stays 0.4.0.

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
