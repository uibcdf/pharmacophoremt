# PharmacophoreMT developer guide

This directory is the team's maintained development context. Start with
**[onboarding](onboarding.md)** when joining or moving machines, then the
**[current checkpoint](checkpoint.md)**. Owners LMMV/dprada; handoff reviewed
2026-11-06 under #107. Code and documentation are English; team discussion may
use Spanish. Repository/suite instructions retain their authority.

## Find the right document

| Need | Read |
| --- | --- |
| Join the team / build a fresh context | [Onboarding](onboarding.md), [machine migration](machine_migration.md) |
| Understand current work and next action | [Checkpoint](checkpoint.md), [decisions/workstreams](decisions_and_workstreams.md), [roadmap](roadmap.md) |
| Know what actually works | [Capability inventory](capability_inventory.md), [core architecture](core_architecture.md), [vision/scope](vision_and_scope.md) |
| Change an API or integration | [API standards](api_design_standards.md), [support boundaries](support_library_boundaries.md), registered root guides |
| Reproduce independent saved-result reading | [Public run contract](public_prepared_runs.md), [released-support receiving](reader_public_provider_receiving.md) |
| Choose tests / assess scientific claims | [Testing/validation](testing_and_validation.md), [evidence collection](validation_collection.md), [case template](templates/evidence_case.md) |
| Work on receptor validation | [#103 plan](pending_proposals/qualify_receptor_screening_studies.md), [study1 admission](receptor_study1_admission_protocol.md), [BRD4 method/next plan](receptor_study2_primary_method.md) |
| Propose or assess a chemical library | [Public registry](https://github.com/uibcdf/pharmacophoremt/discussions/109), [provider research](public_library_support_research.md), [tool/workflow comparison](pharmacophore_library_workflow_survey.md), [#108 workflow](pending_proposals/qualify_public_library_workflow.md) |
| Propose or study a pharmacophore tool | [Tool registry guidance](pharmacophore_tools_registry.md), [#128 proposal](pending_proposals/study_pharmacophore_tools.md), [comparative survey](pharmacophore_library_workflow_survey.md) |
| Design the library workflow and public API | [Architecture proposal](public_library_architecture.md), [worked native contracts](public_library_contract_examples.md), [#108 scope](pending_proposals/qualify_public_library_workflow.md) |
| Understand the audit/backlog | [Audit](audit_20261104.md), [review addendum](audit_20261104_review.md), active issue indexes below |
| Prepare an intermediate release | [#95 readiness](release_0_5_0_readiness.md), [publication controls](../devtools/conda-build/README.md), #9/#10/#23 |
| Update user docs | [Documentation contributor guide](../docs/README.md), [cookbook](../docs/content/cookbook/index.md), [validation collection](../docs/content/validation/index.md) |
| Recover why a decision changed | [Checkpoint history](checkpoint_history_20261106.md), [roadmap history](roadmap_history_20261106.md), owning issue and Git history |

## Authority and evidence

Current checkpoint and capability inventory summarize the present; owning code,
contracts, issue state and original receipts prove narrower details. Dated old
"current/next" observations are historical, not the live queue. Historical
controls retain their exact source/provider/native identities. A correct cache,
geometry, archive or build is not biological validation or public delivery.

Actual release plan/latest Release is0.4.0; proposed0.5 is not frozen. Both #103
biological studies remain unfinished. Deliberate destination resumption now
[receives the published BRD4 capacity plan](receptor_study2_label_capacity_receiving.md):
AID1805333 stops with32 eligible weak SIDs against50 required. No receptor/model/
score or release follows; individual activity rows remain private.
The [follow-on lineage review](receptor_study2_source_lineage_review.md) identifies
a coupled report, and the [third-source method review](receptor_study2_third_source_method_review.md)
retains unresolved original units/material. The [separate PDF recovery](receptor_study2_pdf_recovery.md)
now verifies the original document and reviews bounded pages/PCT table images,
preserving the earlier failed gate without admitting activities or guessed units.
The [fourth-source review](receptor_study2_fourth_source_method_review.md) supports
AID1797167's AlphaLisa method context and its own table's micromolar units;
experimental material and individual-row provenance remain pending. Both sources
stay unadmitted. The [fifth-source review](receptor_study2_fifth_source_method_review.md)
supports AID 2061300's FP-derived Ki in nM and incorporated PCT wording, corrects our
historical title characterization, and retains unresolved material/tracer/row
authority. The [sixth-source review](receptor_study2_sixth_source_method_review.md)
supports AID 1798835's BD1 TR-FRET Ki in µM, preserves the BD2 boundary conflict
and leaves material/probe Kd/row authority pending. No activities follow;
The [final three reviews](receptor_study2_remaining_sources_review.md) complete
bounded review of the nine fixed leads. Original data/material authority remains
pending, including 1805218's experimental/predicted contradiction; no activities
follow. Draft curator questions are prepared, not sent; unresolved-domain sources
retain their separate status.

The [19-source metadata continuation](receptor_study2_unresolved_domain_receiving.md)
now preserves complete fresh coverage/identity without resolving domain assignment
or admitting activities. The user also requests powerful, friendly management of
public libraries for both retrospective validation and new screening. The
[provider research and proposed workflow](public_library_support_research.md)
separate discovery catalogs, activity references, drugs, natural products and
benchmarks, with explicit access/3D/readiness boundaries.

All general molecular formats/inspection/preparation/analysis belong to MolSysMT.
PharmacophoreMT owns the pharmacophore and its evaluation. Proposed TopoMT,
DockingMT, dynamics/MSM/AI and accelerated integrations are not delivered APIs.
The detailed [classical catalogue](classical_workflow.md), [I/O planning](io_and_formats.md),
[modeling strategies](modeling_strategies.md), [dynamics](dynamics_and_msm.md),
[specialized modeling](specialized_modeling.md), [AI](ai_and_data_science.md) and
[visualization planning](visualization_strategies.md) must be read in that scope.

## Issue-backed records

- [Open defects](pending_bugs/README.md)
- [Open proposals](pending_proposals/README.md)
- [Permanent archive](archive/README.md)
- [Reporting protocol](reporting_protocol.md)

Open an owning issue before an independently closable report. Regenerate indexes
with `python devtools/devguide_index.py` and verify `--check`; archive closed
records rather than deleting them. See root/local AGENTS and the suite guide
before contributor actions, direct pushes, external reports or releases.
