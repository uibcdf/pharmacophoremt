# Developer Guide - PharmacophoreMT

Welcome to the official developer guide for **PharmacophoreMT**. This directory is the "source of truth" for the toolkit's architecture, standards, and planning.

[Second-receptor source review](receptor_study2_source_review.md), #106, records
BRD4/HSP90 metadata and original-method feasibility. BRD4 BD1 is prioritized
for further admission; no second target or experimental cohort is accepted.


[Current source receiving — 2026-11-06](source_suite_receiving_20261106.md) records #102's corrected schema-envelope guards, 111 passing selected controls and the complete/incomplete hosted/local evidence without merging their scopes. Start with the [checkpoint](checkpoint.md) for current gates.

[Prepared-receptor admission audit](receptor_preparation_admission_audit.md) and [study1 protocol](receptor_study1_admission_protocol.md), 2026-11-06, record the first #103 preparation/capability receiving. #104 passes nine source controls; #105 now receives native aromatic-N geometry through an [explicit experimental profile](public_cached_aromatic_n_generation.md). Both biological studies remain pending.

## Strategic Vision

[Architectural, scientific and product audit — 2026-11-04](audit_20261104.md)
records the discussed list of 17 improvement areas, priorities,
completion criteria and evidence limits. #73 is now fixed; continue with the
[current capability inventory](capability_inventory.md), scoped #6 contracts and
scientific study design. Native schema/writer checks are now received under #76;
live references/variants are now qualified under #60; legacy merge #77 is now fixed through public composition; nested facade
admission is now received, with broader #6 adoption still partial. Scientific
semantics/provenance under audit items 8–9 now has a [qualified native slice](native_constraint_semantics.md) under #79 and a [consensus support/redundancy review](consensus_support_review.md) under #80; broader coverage stays partial. [Native I/O diagnostics/dependencies](native_io_diagnostics.md) are now repaired under #81/#6.
[Native I/O ArgDigest receiving](native_io_argdigest_receiving.md), #82, now
receives published 0.17.1, protects literal keyword/source identity and activates
four native codec contracts. 500 unique selected controls pass; broader #6,
canonical guide distribution and full installed/public closure remain separate.
[Native batch contracts](native_batch_contracts.md), #99, now reject empty-batch
typos before input consumption and retain scientific/caching/error accounting;
206 unique selected controls pass. Broader #6 remains partial; the checkpoint
records remaining saved-result/retrospective contract work and provider gates.
[Saved-result/retrospective contracts](retrospective_result_contracts.md), #100,
now reuse existing settings validation to prevent EF report-key overwrite;
168 unique selected controls pass. Native option ownership and cohort/failure
accounting remain. Broader #6 and public/current-candidate full gates stay separate.
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
3. [Checkpoint](checkpoint.md): **Start here!** State as of 2026-11-05: #95's post-review consolidation now covers fbe6677, including #82/#99/#100 and #101's unchanged source-name policy. All 46 changed runtime files/nine original argument-signature changes are reviewed; 59 private input hashes match. Fresh main/index checks still identify received MolSysMT 0.23.0/ArgDigest 0.17.1; closed #255/#431 source work is distinct from public delivery/#375. Strict local 62-document/two-image render passes with execution off. Next receive supported public molecular bytes, select the exact candidate and execute #9/#10/#23 gates. Actual plan/tag/Release stays 0.4.0; no freeze/publication/addon work. Serial one-CPU/1-GiB/no-swap commands preserve shared resources.

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
