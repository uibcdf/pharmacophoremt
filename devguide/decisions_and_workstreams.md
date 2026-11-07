# Decisions and active workstreams

Handoff reviewed 2026-11-07 UTC. Use the [checkpoint](checkpoint.md) for current
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
| The active destination is a mature pre-1.0 0.x | Liliana accepts seven capability milestones and as many useful intermediate versions as needed (2026-11-07). The final minor may be0.23,0.40 or another0.x; versions group delivered work, and the1.0 decision is separate and later | [Accepted staircase](roadmap.md#accepted-destination-a-mature-pre-10-0x), [readiness](release_0_5_0_readiness.md), #95 |
| Every implementation increment leaves a usable developer-guide checkpoint | Liliana requires actual implementation/evidence/limits and the next concrete action to remain recoverable from devguide. Update the owning contract/workstream with changed facts and preserve historical measurements; a plan or narrow green check is not completion evidence | Maintainer instruction2026-11-07, [checkpoint](checkpoint.md), [local instructions](../AGENTS.md) |
| Each intermediate release solves a usable public task | Guided use, detailed public composition, documentation and checked installation grow together. Integrate, simplify or retire prototypes after their decision evidence is sufficient; validation and product work proceed in parallel | [Milestone acceptance](roadmap.md#accepted-destination-a-mature-pre-10-0x), #108/#95 |
| Addon work is deferred | Source/payload code exists; live-browser qualification remains separate | #58, [viewer planning](visualization_strategies.md) |
| Principal-maintainer delivery uses direct commit/push and deliberate CI checkpoints | Liliana explicitly authorizes this route and requests `[skip ci]` for routine/small commits (2026-11-06); batch pushes and retain scope-appropriate local checks, with pending exact-head evidence under #9 | [Local instructions](../AGENTS.md#principal-maintainer-delivery-instructions), [checkpoint policy](../MOLSYSSUITE_GUIDE.md#direct-pushes-and-validation-checkpoints), #9 |
| Controlled source is distinct from public delivery | A passing subset/provider source cannot qualify a public package or full installed/platform matrix | [Public receiving](public_dependency_receiving.md), #10/#23/#95 |

## Current workstreams

| Lane | Actual state | Next evidence |
| --- | --- | --- |
| Mature pre-1.0 0.x staircase | Public runs/released-reader support, guided/expert parity and API/CLI complete exports received in bounded contexts | Deliberate exact-head validation of accumulated changes; retain every unresolved gate in [roadmap](roadmap.md) and [checkpoint](checkpoint.md) |
| #103 receptor-to-screening studies | Objective accepted; neither full biological study is complete | Admit original methods/data/cohort/preparation, freeze receptor/comparator/evaluation and execute |
| #66 ERalpha binding | Frozen source pools/exposure persist; original Sun2006, Xin2023, Gungor2006 and Scott2023 methods unresolved | New authorized access lead; don't repeat exhausted routes or alter frozen queries/thresholds |
| #106 second-target admission | Nine fixed leads reviewed; capacity/coupled outcomes and seven held sources remain separate | Resolve original material/data/curation authority; further unresolved-domain review needs a new declaration; no activities admitted |
| #108 public-library workflow | Public runs, released reader support, guided/expert parity, exports and [criterion-independent progress](saved_run_progress.md) received in bounded source/owned installed contexts | Retain completed frozen4616c78 CI separately. Broader usability/source operations and [MolSysMT #624](https://github.com/uibcdf/molsysmt/issues/624) remain; no blanket connector/index/durability/biological promise |
| #128 tool-study registry | Dedicated public index, one [executed Pharm3D analytical comparison](rdkit_bounds_comparison.md) and nine documentary records | Public RDKit projection fields are source-qualified under#140; next receive the same owned installed artifact and retain independent broader comparison/benchmark/biological gates |
| Molecular providers | #105 receives native aromatic-N; carboxylate, constrained H refinement and grouping retain specific gaps | MolSysMT#375/#323/#447; supported provider operations, no local replacement |
| #95 intermediate release | Proposed0.5 reviewed; actual plan/tag/Release0.4.0 | Public provider capability and exact source/installed/public gates before a freeze |
| #9/#10/#23 CI/support/distribution | [Frozen4616c78 gates](accumulated_ci_checkpoint.md) pass all8 source cells/2259 tests each plus governance; coverage XML#141 corrected locally | Receive later-head coverage/runtime and full installed/public/package gates separately; no repeated frozen run |
| #6/#41/#74 ecosystem debt | Partial support adoption; bounded old-provider donor compatibility and SDF container migration remain | Receive owning provider contracts; annotated-SDF delegation is MolSysMT#215 |
| #43 historical resources | Some `/tmp` producers/papers are absent; tracked support is intact | [Migration inventory](machine_migration.md): distinguish reconstruction from original recovery |

TopoMT pockets are optional to current cached hypotheses. DockingMT integration,
dynamics/MSM/AI and accelerated/distributed methods are future lanes, not hidden
prerequisites or delivered functionality. Support libraries follow their canonical
guides; [support boundaries](support_library_boundaries.md) tracks actual adoption.

## Resume science deliberately

Migration alone does not execute a scientific plan. Deliberate resumption now
received #106's declared single-AID capacity, after verifying the published plan
and unchanged source identities. Strong IC50≤0.5 versus weak IC50>5 micromolar
remain assay-specific reported potencies, not general inactivity or independent
molecules. AID1805333 stops:32 eligible weak SIDs cannot meet50 per class. Preserve
the91 missing relations rather than assuming equality, and record the stop before
a new source nomination. A passing later raw count would still need MolSysMT
chemical/state/series grouping, preparation, and complete PHMT material/exposure/
interference admission before receptor/comparator choices and scores are frozen.
Do not pool patents, tune on outcomes, relax labels or replace failures. Both
studies remain open until the complete declared evidence actually exists.

The [follow-on review](receptor_study2_source_lineage_review.md) records shared
publication evidence for AID 1795677 without transferring the earlier class
counts or asserting molecular equivalence. AID 1797292's original method is now
received, but original table units and material/species are unresolved; a failed
PDF receiving attempt does not qualify a page or authorize unit/species transfer.
A [separate recovery](receptor_study2_pdf_recovery.md) now verifies the complete
PDF and bounded visual review; original table-unit and actual material authority
still require source clarification before activities.
The [fourth-source review](receptor_study2_fourth_source_method_review.md) reuses
the originalUS9763922 HTML and verifies fresh1797167 metadata. Its exact AlphaLisa
method correspondence and explicit FormulaII table units are positive documentary
evidence; experimental material and individual-row mapping remain unresolved.
The [2061300 review](receptor_study2_fifth_source_method_review.md) now supports
original FP-derived inhibitor Ki in nM, distinct from tracer Kd. The incorporated
PCT states Ki/30 min; historical metadata hashes support a dated correction
of our old "KD title" description without changing original KO/US `30 mM` bytes.
Material, tracer and individual-row authority remain pending. The
[1798835 review](receptor_study2_sixth_source_method_review.md) now supports the
BD1 K57–E168 TR-FRET Ki column in µM and preserves the separate BD2/cellular
contexts and literal BD2 boundary conflict. Actual material, probe Kd/calculation
and row authority remain pending; unrelated curator annotations do not fill them.
The [last three reviews](receptor_study2_remaining_sources_review.md) now cover
1805218/1805772/1804941. Source 1805218 has conflicting predicted/experimental
prose and a 134-record numeric table; no three-record capacity bound follows.
Actual material/controls/curation and source-specific interval transfer remain
pending. All nine fixed leads have bounded outcomes, with no newly admitted
activities. Draft authority questions remain unsent; 19 unresolved-domain records
are not silently excluded or promoted.

## Public libraries and complete unresolved metadata receiving — 2026-11-06

The [19-source receiving](receptor_study2_unresolved_domain_receiving.md) verifies
all source identities/fields in one response; all remain domain-unresolved and
the nine earlier outcomes stay intact. No new activity cohort is admitted.
The user also requests both retrospective validation and new-library screening.
[Provider research](public_library_support_research.md) proposes a common library
workflow and records access/3D/implementation limits. It is a product design
input, not implemented library support, new scoring or retrospective acceptance.
Generic molecular collection reading/preparation remains MolSysMT-owned.
