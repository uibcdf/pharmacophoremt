# Decisions and active workstreams

Handoff reviewed 2026-11-06. Use the [checkpoint](checkpoint.md) for current
actions and [roadmap](roadmap.md) for order. Owning contracts/issues and original
evidence retain finer-grained authority than this orientation page.

## Decisions to retain

| Decision | Reason and consequence | Authority |
| --- | --- | --- |
| General molecular tools stay in MolSysMT | Chemistry/formats/preparation/geometry must serve other consumers; request missing tools in their owner | [Suite map](../MOLSYSSUITE_GUIDE.md#component-responsibility-map), [capabilities](capability_inventory.md) |
| Explicit native methods replace defective legacy automation | Prepared inputs and chosen rigid/aligned/cached methods prevent hidden scientific substitutions | [Ligand transition](ligand_based_workflow.md), #18; [structure workflow](structure_based_workflow.md), #44 |
| Hypotheses and completeness remain inspectable | Preserve alternatives, omissions, finite budgets and failures instead of silently switching methods | [Generation](public_receptor_generation.md), [semantics](native_constraint_semantics.md) |
| Cache consistency is not authenticated provenance | State/frame/unit/selection checks cannot prove the cache came from its claimed source | [Provenance](native_provenance_persistence.md), #89 |
| Separate analytical, preparation, biological and performance evidence | Correct geometry or a successful build cannot establish predictive power | [Collection](validation_collection.md), [audit](audit_20261104.md), [addendum](audit_20261104_review.md) |
| No mandatory favorable EF/AUC/LOO outcome | Scientific quality comes from declared labels, comparators, leakage controls, uncertainty and honest negative/inconclusive results | [Two-study objective](pending_proposals/qualify_receptor_screening_studies.md), #103 |
| Intermediate0.x releases remain possible |1.0 is agreed scientific/product scope, not a compulsory0.9-to1.0 jump;0.10/0.11 remain available | [Readiness](release_0_5_0_readiness.md), #95 |
| Addon work is deferred | Source/payload code exists; live-browser qualification remains separate | #58, [viewer planning](visualization_strategies.md) |
| Direct pushes retain exact-head CI/recovery duties | Principal-maintainer authorization persists; new contributors use owner-reviewed PRs | [Checkpoint policy](../MOLSYSSUITE_GUIDE.md#direct-pushes-and-validation-checkpoints), #9 |
| Controlled source is distinct from public delivery | A passing subset/provider source cannot qualify a public package or full installed/platform matrix | [Public receiving](public_dependency_receiving.md), #10/#23/#95 |

## Current workstreams

| Lane | Actual state | Next evidence |
| --- | --- | --- |
| #103 receptor-to-screening studies | Objective accepted; neither full biological study is complete | Admit original methods/data/cohort/preparation, freeze receptor/comparator/evaluation and execute |
| #66 ERalpha binding | Frozen source pools/exposure persist; original Sun2006, Xin2023, Gungor2006 and Scott2023 methods unresolved | New authorized access lead; don't repeat exhausted routes or alter frozen queries/thresholds |
| #106 second-target admission | BRD4 prioritized;1,780-AID census complete, nine isolated-BD1 leads, no admitted target/cohort | [Primary-method review](receptor_study2_primary_method.md), then prospective single-source necessary label capacity; no activities received yet |
| Molecular providers | #105 receives native aromatic-N; carboxylate, constrained H refinement and grouping retain specific gaps | MolSysMT#375/#323/#447; supported provider operations, no local replacement |
| #95 intermediate release | Proposed0.5 reviewed; actual plan/tag/Release0.4.0 | Public provider capability and exact source/installed/public gates before a freeze |
| #9/#10/#23 CI/support/distribution | Separate source, supported-platform/minor, installed and public backlogs | Exact run/attempt and artifact/dependency evidence; narrow checks cannot clear full gates |
| #6/#41/#74 ecosystem debt | Partial support adoption; bounded old-provider donor compatibility and SDF container migration remain | Receive owning provider contracts; annotated-SDF delegation is MolSysMT#215 |
| #43 historical resources | Some `/tmp` producers/papers are absent; tracked support is intact | [Migration inventory](machine_migration.md): distinguish reconstruction from original recovery |

TopoMT pockets are optional to current cached hypotheses. DockingMT integration,
dynamics/MSM/AI and accelerated/distributed methods are future lanes, not hidden
prerequisites or delivered functionality. Support libraries follow their canonical
guides; [support boundaries](support_library_boundaries.md) tracks actual adoption.

## Resume science deliberately

Migration does not execute the next scientific plan. When resumed, verify the
published plan/source identities first. #106 next checks private single-AID
capacity using strong IC50≤0.5 versus weak IC50>5 micromolar and50 eligible SID
upper bounds per class. Those are assay-specific reported potencies, not general
inactivity or independent molecules. A failed necessary gate stops that declared
source/design before a new nomination. A passing raw count still needs MolSysMT
chemical/state/series grouping, preparation, and complete PHMT material/exposure/
interference admission before receptor/comparator choices and scores are frozen.
Do not pool patents, tune on outcomes, relax labels or replace failures. Both
studies remain open until the complete declared evidence actually exists.
