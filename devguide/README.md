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
| Choose tests / assess scientific claims | [Testing/validation](testing_and_validation.md), [evidence collection](validation_collection.md), [case template](templates/evidence_case.md) |
| Work on receptor validation | [#103 plan](pending_proposals/qualify_receptor_screening_studies.md), [study1 admission](receptor_study1_admission_protocol.md), [BRD4 method/next plan](receptor_study2_primary_method.md) |
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
biological studies remain unfinished. BRD4 source methods and a prospective
label-capacity plan are recorded, but no dedicated activities/class projection
has run. Migration itself starts no scientific acquisition, model or release.

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
