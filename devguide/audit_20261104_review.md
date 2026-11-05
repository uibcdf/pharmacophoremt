# Audit evidence, priorities and verification — 2026-11-04 addendum

## Relationship to the initial audit

This addendum operationalizes the [initial 17-area assessment](audit_20261104.md).
It preserves that dated text and its numbering. It does not claim that the
proposed improvements have been implemented or that an exhaustive audit has
been completed. Source reviewed: 9ea3f30077e29226a62e3dd14f39850e64eebcf3;
documentation baseline: 61e2507ceab5e4fe7f1c930e969d1b49c0b12dcc. The latter
commit changes documentation only. Accountable maintainers: LMMV and dprada.

Method: inspect selected public entry points, read their maintained scientific
contracts, locate regression controls, and review existing receipt summaries.
Evidence below distinguishes implementation inspection from recorded execution.
No scientific suite, biological experiment, installation matrix, performance
measurement or external method comparison was executed for this addendum.
Receipts retain their original producer identities and limitations; listing a
test here is not a new passing result. Their full archives were not independently
revalidated as part of this documentary review.

Two clarifications refine the initial assessment. Native metrics already handle
ties; item 14 concerns correct use and interpretation, not a missing tie engine.
Independent assignment and consensus oracles already exist; item 11 concerns
coverage gaps, not replacing those tests. Public 0.4.0 installed qualification
remains valid within its recorded scope, independently of current development.

## Coverage and exclusions

| Boundary | Review depth and evidence | Not established by this review |
| --- | --- | --- |
| Public construction and dispatch | Selected source inspection: [model dispatch](../pharmacophoremt/modeler/dispatcher.py), [site](../pharmacophoremt/interaction_site/interaction_site.py), [native geometry configuration](../pharmacophoremt/_private/arg_digestion/native_geometry.py), E01/E03 | Exhaustive admission/alias analysis of every callable |
| Persistence and formats | Selected native serializer/reader and facade inspection, E02/E04; external-format tests located | Complete external-format round trips, malformed-input robustness or security certification |
| Molecular boundary and state | Ownership contracts, explicit copy/curation controls and open #60, E05 | New audit of every MolSysMT call, provider implementation or cache invalidation path |
| Scientific methods | Contract and existing-control review represented in the method matrix below | Line-by-line mathematical verification of every algorithm or new numerical equivalence experiments |
| Predictive validation | Metric implementation, retrospective accounting, collection policy and #66 context, E08/E09 | New accepted assay cohort, independent predictive result or broad applicability claim |
| Installation and release | Existing declarations and qualification records, E10 | New clean installation, all-platform receiving or current hosted completion |
| Resources and maintenance | Materialized-batch behavior, bounded-search contracts and existing test-run duration, E11/E12 | Peak-memory/scaling benchmark, concurrency safety, recovery guarantees or proof of redundant tests |
| Documentation and usability | Entry points, checkpoint/roadmap and explicit versus aspirational capabilities, E06/E07 | User study, accessibility review or live addon/browser qualification |

Security of hostile input, optional dependency supply chains, sustained parallel
execution and large-scale operational reliability remain unassessed here. These
are coverage limits, not findings that a vulnerability or failure exists. Broader
review should be driven by intended deployment and actual supported use cases.

## Evidence register

These IDs support the findings and acceptance tables. Local links identify the
reviewed files; use the source/documentation baseline above to recover the exact
revision after later changes. Issue links are coordination records, not frozen
scientific evidence.

| ID | Concrete anchor | Observation and evidence status |
| --- | --- | --- |
| E01 | [Geometry receiving receipt](evidence/native_geometry_contract_receiving_20261104_summary.json), [guards](../tests/test_native_geometry_contracts.py) | Recorded: 1093 actual full-run cases pass; public/development focused scopes and exact overlays retained. This is controlled source receiving, not full public installation qualification. |
| E02 | [Native loader report](archive/native_loader_ignored_options.md), [facade](../pharmacophoremt/io/__init__.py), E01 archived load_options_probe.py/results | Confirmed historical reproduction: native JSON/YAML discard unknown facade keywords while direct readers refuse them. #73 owns the fix. |
| E03 | [Dispatch](../pharmacophoremt/modeler/dispatcher.py), [screening facade](../pharmacophoremt/screening/virtual_screening.py), [support boundaries](support_library_boundaries.md) | Inspected: method-dependent forwarding, explicit native choices, inert legacy parameters and scoped contracts. No general dispatcher defect is asserted. |
| E04 | [Native persistence](../pharmacophoremt/io/phmt/__init__.py), [contract tests](../tests/test_contracts.py), [curation tests](../tests/test_curation.py), [format specification](io_and_formats.md) | Inspected: software version field, explicit native units, shape branches and existing persistence controls. Schema evolution and complete format fidelity require a separate audit. |
| E05 | [Curation contract](pharmacophore_curation_workflow.md), [copy/alias tests](../tests/test_curation.py), [#60](https://github.com/uibcdf/pharmacophoremt/issues/60) | Existing guards cover detached site evidence and atomic edits; live molecular references and independent molecular variants remain a separately owned boundary. |
| E06 | [Shapelet](../pharmacophoremt/interaction_site/shape/shapelet.py), [growth contract](extensible_modeling_contracts.md), [core architecture](core_architecture.md) | Inspected: a shape name/constructor exists while its renderer is unimplemented; broader growth requirements are explicitly future work. This supports a capability inventory, not implementing Shapelet now. |
| E07 | [Guide entry](README.md), [checkpoint](checkpoint.md), [roadmap](roadmap.md), [historical workflow](classical_workflow.md) | Inspected: maintained priorities coexist with extensive historical and superseded plans. Onboarding cost is a reasoned concern, not a measured usability result. |
| E08 | [Metrics](../pharmacophoremt/validation/metrics.py), [metric tests](../tests/test_validation_metrics.py), [retrospective tests](../tests/test_retrospective.py), [seeded contract](seeded_ranking_workflow.md) | Existing tie-aware EF/AUC/BEDROC and failed-input accounting; seeded_hit is binary, checked coverage is pose-specific. Affinity prediction is not their contract. |
| E09 | [Collection policy](validation_collection.md), [binding-method handoff](esr1_binding_pool3_methods.md), [#66](https://github.com/uibcdf/pharmacophoremt/issues/66) | Recorded source-readiness limitations and exposure history. No independent predictive validation is established by this audit. |
| E10 | [Installation guide](../docs/content/about/installation.md), [metadata](../pyproject.toml), [#10](https://github.com/uibcdf/pharmacophoremt/issues/10), [#23](https://github.com/uibcdf/pharmacophoremt/issues/23) | Public 0.4.0 qualification and later development requirements have distinct identities. New source receiving cannot automatically promote installed support. |
| E11 | [Batch facade](../pharmacophoremt/screening/virtual_screening.py), [search contract](rigid_search_workflow.md), [ranked-seed contract](ranked_seed_workflow.md) | Inspected: inputs are materialized and algorithms expose bounded work. No workload-specific memory defect or unbounded-runtime claim is established. |
| E12 | E01, [test policy](testing_and_validation.md), [CI](../.github/workflows/CI.yaml), [#71](https://github.com/uibcdf/pharmacophoremt/issues/71) | Recorded full run: 1401.42 s, 1093 actual cases versus raw aggregate 1110. This single duration is not a benchmark or proof that the suite is inefficient. |

## Classified findings and priority rationale

Classification: **D** confirmed defect; **O** observed behavior or limitation
whose adequacy depends on the intended use; **R** risk/question requiring a
targeted audit; **P** proposed study or improvement. An R/P row is not a defect
report. Priority is qualitative, not a numerical risk estimate: **P1** next action
or immediate parallel prerequisite; **P2** consolidation before expanding claims;
**P3** conditional on a measured need. No critical vulnerability is inferred.

| Initial item | Class/status | Priority and potential impact | Basis |
| --- | --- | --- | --- |
| 1 | D — reproduced, open #73 | P1: silent option loss can invalidate user intent without an error | E02 |
| 2 | O + P — capability limits observed; matrix proposed | P1: prevent unsupported scientific use and scope confusion | E06/E07 |
| 3 | O + R — mixed API generations; audit pending | P1: wrong method/options can undermine reproducible interpretation | E03/E01 |
| 4 | R — no universal format defect established | P2: potential scientific information loss on save/load or conversion | E04 |
| 5 | O + R — partial guarantees; #60 open | P2: possible unintended cross-object effects or stale result reuse | E05 |
| 6 | O + P — release evidence exists; current receiving separate | P2: prevent reliance on unsupported installation combinations | E10/E01 |
| 7 | O + P — history/entry-point complexity observed | P1, bounded: make current capabilities and valid workflow discoverable | E07 |
| 8 | R — consistency audit pending; contracts exist | P2: prevent scientific meaning changing between methods/formats | E03/E04/E08 and method matrix |
| 9 | R — provenance controls exist; full decision tracing unaudited | P2: prevent inference being represented as direct observation | Method matrix: reference, observed and receptor routes |
| 10 | O + P — experimental readiness unresolved | P1 in parallel: endpoint ambiguity or leakage can invalidate evaluation | E09 |
| 11 | P — extend only demonstrated gaps | P2: protect mechanisms without duplicating independent oracles | Method matrix and E01 |
| 12 | P — study not executed here | P2 after protocol/development split: parameter/search opportunity bias | E09/E11 |
| 13 | R + P — redundancy concern not a demonstrated current defect | P2: avoid overstating consensus support or essentiality | Consensus rows in method matrix |
| 14 | O + P — score/tie contracts exist; study interpretation pending | P1 for protocol, P2 for experiments: prevent misleading ranking claims | E08 |
| 15 | P — no new independent prediction result | P2 after data/model freeze: establish utility and applicability | E09 and method-specific limits |
| 16 | O + P — materialization observed; scaling unmeasured here | P2 measurement, P3 optimization: assess practical resource limits | E11 |
| 17 | O + P — suite/evidence cost observed, redundancy unproven | P2: improve iteration cost while preserving required assurance | E12 |

## Scientific evidence matrix by method

All rows describe the reviewed implementation/contract and **existing** evidence.
Analytical controls and prepared molecular cases do not establish experimental
predictive accuracy. Receipt links retain historical environment, reuse and
metadata caveats; they are not uniform fresh executions on today's head.

| Method family | Meaning and assumptions | Existing controls / recorded evidence | Limit and next scientific question |
| --- | --- | --- | --- |
| Reference ligand | Features of a selected prepared ligand become query hypotheses; recognition/geometry come from MolSysMT | [Contract](reference_ligand_workflow.md), [tests](../tests/test_reference_ligand.py), [receipt](evidence/reference_ligand_acceptance_20261103_summary.json): six families, charge membership, aromatic axes, units and persistence | Feature presence does not establish binding importance. Evaluate selection/essentiality choices on independent data. |
| Observed interactions and complex construction | Convert declared native observations from a prepared source; contact existence differs from favorable energy or essentiality | [Contract](complex_based_workflow.md), [pose controls](../tests/test_pose_evaluation.py), [ERalpha receipt](evidence/eralpha_acceptance_20261104_summary.json) | Prepared-fragment evidence has environmental-H/full-receptor limits. Assess observation-to-constraint decisions, without local chemistry repair. |
| Receptor projections | Caller specifies hypotheses from cached receptor inventories in a declared frame | [Contract](structure_based_workflow.md), [projection tests](../tests/test_receptor_projections.py), [prepared receptor case](prepared_receptor_workflow.md) | Projection direction/distance are hypotheses, not inferred optimal ligand poses. Test sensitivity and applicability of chosen projections. |
| Composition and exclusions | Combine declared common-frame models; same-participant merging has explicit identity/geometry conditions; exclusions veto otherwise matching poses | [Composition contract](interaction_composition_workflow.md), [tests](../tests/test_interaction_composition.py), [composition receipt](evidence/composition_acceptance_20261103_summary.json), [exclusion receipt](evidence/exclusion_acceptance_20261103_summary.json) | Declarations do not authenticate a shared molecular origin. Exclusion radii are not independently validated interaction energies. Audit provenance assumptions and constraint redundancy. |
| Aligned reference consensus | Prepared inputs share a frame; reference-based correspondence yields support and dispersion | [Contract](aligned_consensus_workflow.md), [tests](../tests/test_aligned_consensus.py), [receipt](evidence/aligned_reference_acceptance_20261103_summary.json): bounded exhaustive assignment oracle, centroid/dispersion controls | Reference dependence and sampling redundancy limit interpretation. Support frequency does not prove essentiality. |
| Aligned clique consensus | Discover compatible patterns and joint supporting hypotheses in a common frame | [Contract](aligned_clique_consensus_workflow.md), [tests](../tests/test_aligned_cliques.py), [receipt](evidence/aligned_clique_acceptance_20261103_summary.json): subset oracles, absent-first-ligand patterns, pairwise versus joint support | Pattern enumeration has explicit resource limits; chemical-series balance is a study design question. Evaluate redundancy and model selection. |
| Rigid unaligned consensus | Propose feature correspondences and fit prepared ligands with MolSysMT under explicit pivot/strategy and budgets | [Contract](rigid_consensus_workflow.md), [tests](../tests/test_rigid_consensus.py), [receipt](evidence/rigid_consensus_acceptance_20261103_summary.json): injective oracle, rigid recovery, reflection/ambiguity/budget controls | No general continuous optimum or conformational search claim. Assess reference/strategy dependence at comparable search opportunities. |
| Ranked seeds and greedy refinement | Declared adaptations rank proposals and refine supplied correspondences; molecular fits remain provider-owned | [Ranked contract](ranked_seed_workflow.md), [refinement contract](rigid_refinement_workflow.md), [ranked receipt](evidence/ranked_seed_acceptance_20261103_summary.json), [refinement receipt](evidence/rigid_refinement_acceptance_20261103_summary.json) | Not full G3PS; excluded stages and angular policies remain explicit. Compare equivalent workloads/returned alternatives before claiming superiority. |
| Placed-pose evaluation | One-to-one compatible assignments in a declared pose; essential sites and steric vetoes constrain acceptance; fit is weighted coverage | [Contract](placed_pose_workflow.md), [tests](../tests/test_pose_evaluation.py), [receipt](evidence/placed_pose_acceptance_20261103_summary.json): motion, direction, zero-weight essential and exclusion controls | Coverage is not affinity. Disk matching is center/axis based, not physical disk intersection. Evaluate parameter robustness and constraint contribution. |
| Rigid pose search and seeded_hit | Finite compatible seeds are fitted/evaluated; seeded_hit reports binary success, compatibility coverage retains different semantics | [Search contract](rigid_search_workflow.md), [seeded contract](seeded_ranking_workflow.md), [tests](../tests/test_rigid_search.py), [receipt](evidence/rigid_search_acceptance_20261103_summary.json) | Seed eligibility includes non-collinear essential centers; a discrete negative is not proof of nonbinding. No exhaustive continuous optimum. Audit fair budgets and tie interpretation. |
| Prepared conformer screening | Evaluate requested prepared frames/states and preserve failed-frame evidence; preparation/generation belong to MolSysMT | [Contract](conformer_screening_workflow.md), [tests](../tests/test_conformer_screening.py), [receipt](evidence/conformer_acceptance_20261103_summary.json): state/selection, ordering, partial failures and no-score controls | Not a thermodynamic ensemble probability. More conformers provide more search opportunities. Study preparation/count dependence under a declared protocol. |
| Retrospective metrics | Evaluate labeled inputs using the chosen score; failures retain accounting; ties handled by the native metrics | [Implementation](../pharmacophoremt/validation/retrospective.py), [metric tests](../tests/test_validation_metrics.py), [retrospective tests](../tests/test_retrospective.py), E08/E09 | Known synthetic rankings verify calculations, not prediction. Experimental endpoints, independent splits, baselines and uncertainty remain study requirements. |

Matrix coverage is the reviewed classical method families, not every exported
API. Curation, persistence and attribution have their own evidence (E04/E05 and
[attribution receipt](evidence/attribution_acceptance_20261104_summary.json));
they do not independently validate prediction. No new comparison to an external
implementation, new literature-method adjudication or fresh target-generalization
study is claimed.

## Operational acceptance and dependencies

These are proposed completion checks, not new passing results. LMMV/dprada are
accountable for each row; the issue column identifies existing coordination,
not an assignment of unaccepted work to another component. A dash means the
work remains a planning item: select its bounded scope and owning issue before
implementation or a queued report. A documented no-change conclusion is valid
when supported by the specified review.

| Item | Reviewable deliverable and completion check | Dependency / existing coordination |
| --- | --- | --- |
| 1 | Actual JSON/YAML facade regressions reject unknown options; valid reads pass; assess other native routes and preserve molecular delegation | #73; start now |
| 2 | Enumerated public capability table links each supported combination to a contract/test or marks it unsupported/experimental; verify exports against the table | E06; — |
| 3 | Per-method accepted-option/default/alias table; exercise representative valid, invalid and legacy calls with public ArgDigest; document any deprecation | #6; item 2 |
| 4 | Per-format field-preservation and schema-version table; round-trip supported fields; refuse unsupported schemas or document explicit migration/loss; test malformed cases selected by review | Item 2; #73 only covers facade admission; broader issue to be scoped |
| 5 | Mutation/copy matrix covers sites, metadata and molecular references; two-way changes verify declared sharing/independence and cache validity | #60; MolSysMT for molecular copy behavior |
| 6 | Exact package/env identity and a source-free workflow run with expected outputs and recorded failures on the required supported cells | #10/#23; chosen candidate and its dependency routes |
| 7 | One short current-state entry and one runnable user path; all links resolve; preserved history is clearly separated; recipe scope matches installed/development availability | Items 2/6; — |
| 8 | Map terms and method identifiers across construction, matcher, scorer and formats; add focused controls only for actual inconsistencies or uncovered semantics | Items 2/3/4; — |
| 9 | For representative ligand, observed-contact and projection models, recover source, method, parameters, frame/state and essential/weight decisions after persistence | Items 4/8; #19 attribution and #22 prepared case retain their own scope |
| 10 | Freeze source eligibility, endpoint, labels, grouping/split, exposure ledger, budgets, baselines and planned analyses before evaluation; document source access or a justified alternative | #66; can start in parallel now |
| 11 | Mechanism-to-oracle inventory names covered/uncovered cases; each selected new guard has an independent expected answer and detects its intended failure | Method matrix; —; retain existing passing controls |
| 12 | Prespecified development-only parameter/preparation/search sweep; record every setting, failure and stability measure; verify final holdout remains unused | Item 10; provider-produced molecular variants |
| 13 | Compare support/model decisions under declared series balancing and controlled redundancy; report model size and performance on development data | Items 10/12; molecular grouping through MolSysMT |
| 14 | Declare score semantics, tie policy, thresholds and original/evaluated denominators; existing tie controls plus study-specific failure sensitivity; no affinity language for coverage | Items 8/10; E08 and existing seeded-ranking contract |
| 15 | Freeze selected model and protocol, then evaluate holdout once under declared rules; report baselines, uncertainty, errors, component comparisons and applicability limits | Items 6/10/12–14; #66; further targets only for broader claims |
| 16 | Representative workload-size series records all timing/memory samples, environment and returned coverage; introduce batching/optimization only for a demonstrated limitation and verify equivalence | Workload from items 2/6; existing algorithm budgets remain authoritative |
| 17 | Change-to-check matrix selects fast/integration/scientific/release checks with rationale; measure validation cost; preserve required gates and reconcile count evidence separately | #9/#23/#71; optimize process without weakening assertions |

Proposed statistical choices (uncertainty estimator, minimum useful effect,
sample-size adequacy, grouping and baseline selection) must be justified in the
study protocol before outcome inspection. This audit invents no universal
performance threshold or dataset size. If the data cannot support the planned
claim, narrow the claim or retain an unresolved outcome rather than moving the
acceptance threshold after evaluation.

## Decision and maintenance record

Immediate action: #73, followed by a bounded #6 API review and a concise
capability entry. Start item 10 concurrently; its source access gate does not
block local API improvements. Items 4/5/8/9 consolidate information and semantic
integrity. Items 12–15 form the study sequence, with model tuning restricted to
development data. Item 16 measurement and item 17 process review can accompany
those streams. Addon/advanced methods remain deferred.

On completing a row, append date, disposition (fixed, adequate, deferred,
blocked or superseded), issue, exact revision and evidence link. A deferral needs
reason and reassessment trigger; a negative scientific result can satisfy the
study's execution criterion. No blanket 17-issue implementation campaign or
automatic closure is implied. Keep original observations and failed attempts.
All reusable general molecular operations remain MolSysMT-owned; provider gaps
are proposed in their owner's repository.

## Progress — 2026-11-04: item 1 fixed (#73)

The [archived resolution](archive/native_loader_ignored_options.md) and
[receipt](evidence/native_loader_dispatch_20261104_summary.json) record the fix
on base 4a471bc2630d3db95bc9009689450391f1987f91 with exact accepted source/test
hashes: five pharmacophore routes refuse unknown keywords; molecular options
and original provider errors remain MolSysMT-owned. Six regression guards fail
the original implementation; 77 focused checks pass after correction. Initial
fixture failures remain recorded. This resolves E02/item 1 only; it does not
qualify broader persistence, scientific prediction or the complete 17-area plan.
Next: items 2–3, an actual capability inventory and bounded #6 dispatcher review.

## Progress — 2026-11-04: capability map delivered; API contracts partial (#6)

Audit item 2 now has a maintained [capability inventory](capability_inventory.md)
with implemented/partial/planned boundaries, inputs/outputs, scientific limits,
provider ownership and control links. It is a core product map, not an exhaustive
format-fidelity or release-compatibility matrix.

Item 3 receives the generic model facade's method-dependent domain and existing
source aliases. Conflicting source names are refused instead of silently replacing
an input; unknown options fail before endpoint execution. The [receipt](evidence/model_dispatch_contract_20261104_summary.json)
records exact accepted bytes on base 1c6a03479bd0514a5d5988a8134b8359bca837b9,
290 passing focused controls and all failed/corrected attempts. No scientific
method or MolSysMT implementation changes. #6 stays partial; nested consensus/
screening contracts and broader API review remain. Next bounded work is item 4,
native persistence field/schema fidelity. Initial audit observations are preserved.

## Progress — 2026-11-04: item 4 reader repair and ownership correction

[Field/schema review](persistence_fidelity.md) and #75's [receipt](evidence/native_persistence_validation_20261104_summary.json)
record 207 passing focused controls and exact accepted bytes on base 83e13bd.
External native files now reuse public scientific value validation. This fixes
one measured defect; native schema/unknown-field/writer policy remains open work.
Existing SDF container handling directly uses RDKit and is architectural debt,
now tracked in #74 with a MolSysMT #215 handoff. Previous semantic tests establish
payload fidelity within their scope, not correct molecular ownership. No new
molecular routines/provider changes or predictive/installed claims are made.

## Progress — 2026-11-04: item 4 native schema/writer slice fixed (#76)

[Native contract](native_schema.md) and [receipt](evidence/native_schema_writing_20261104_summary.json)
record 265 passing focused cases and exact bytes on base 0413e6c. New JSON/YAML
have explicit native schema/field admission; untagged legacy compatibility remains.
Validation and encoding happen before destination opening, preserving previous
bytes on those failures. No atomic OS/crash/concurrency guarantee. SDF source/
private payload unchanged; six tests now compare equal complete pharmacophore
payloads with their distinct schema envelopes. #74/provider and per-translator
fidelity remain incomplete. Next independent theme: #60 live references/variants,
with molecular copying and inspection delegated to public MolSysMT.

## Progress — 2026-11-04: item 5 native-reference scope adequate; legacy merge open

[#60 contract](live_reference_ownership.md) and [receipt](evidence/live_reference_ownership_20261104_summary.json)
qualify existing curation/live-reference and explicit public MolSysMT eager-copy
semantics with 199 source controls, without production changes. Provider #121 is
now closed; exact receiving provider 0faf1584 is distinct from inspected sibling
71fbe4f. No full-suite/installed/platform/predictive promotion. Eight initial NaN-
comparison test failures and their correction remain visible. This does not clear
all library ownership: #77 independently tracks confirmed legacy merge metadata
loss and measured site aliases needing a settled compatibility contract. Next #77.

## Progress — 2026-11-04: legacy merge repair (#77)

[Merge contract](pharmacophore_merge.md) and [receipt](evidence/pharmacophore_merge_20261104_summary.json)
record delegation to existing keep-policy composition, independent site occurrences
and both component metadata histories. Name/description/first live molecular
reference remain; root metadata is structured provenance, output score/ref_mol
None and common declared frame retained. Frame conflicts now refuse visibly.
This is an explicit compatibility migration, not a second scientific engine.
Original metadata loss is fixed; original site-sharing observation was not a
historically promised independence violation. All attempts and exact bytes are
retained. No molecular/provider operation added or full-suite/installed/predictive
promotion. Next #6 nested facade admission; other audit studies retain their scope.

## Progress — 2026-11-04: nested facade contracts partial adoption (#6/#78)

[Nested contract](nested_facade_contracts.md) and [receipt](evidence/nested_facade_contracts_20261104_summary.json)
record 167 passing controls, definition-owned signature-derived constructor domains
and #78's repaired local skip-control handling. Valid scientific behavior and
run/cache order remain. Two legacy option-error expectations migrate to earlier
ArgDigest refusal; three intentional run warnings remain visible. All attempts/
identities preserved; no full-suite/installed/predictive claim. #6 stays partial.
Next product review: items 8–9, existing multi-feature/shared-participant semantics
and observation-to-constraint provenance; molecular operations stay in MolSysMT.

## Progress — 2026-11-04: native matching semantics qualified (#79)

[Constraint contract](native_constraint_semantics.md) and
[receipt](evidence/native_constraint_semantics_20261104_summary.json) record
368 passing cases, including 40 new real-provider analytical controls. Any-of
Point/Sphere kinds, unique typed-record capacity, shared donor/acceptor atoms,
distinct indexed-H identity, shape restrictions and correspondence/alignment
admission are explicit. Existing donor identity was preserved, not repaired.
Two additive result criteria explain the unchanged matching method.

Representative recognized, observed and explicit-projection origins plus
essential/weight curation decisions survive native JSON/YAML and non-default
units. Construction defaults and contact multiplicity are not empirical binding
importance. Direct attribute edits do not automatically explain decisions.
Both attempt identities and all original outcomes are retained. No molecular
implementation, provider/prefix/dependency or algorithm/default changes.

Items 8–9 stay partial outside this native slice; no full-suite, installed,
all-platform or predictive promotion. Next review consensus support and
redundancy (8/13) with existing independent oracles, then parameter/constraint
sensitivity (12). #66, #74/MolSysMT #215 and broader #6 retain independent gates.

## Progress — 2026-11-04: consensus support and controlled redundancy (#80)

[Method/support matrix](consensus_support_review.md) and
[receipt](evidence/consensus_support_review_20261104_summary.json) retain the
supported no-algorithm-change conclusion: 126 selected cases pass, including
28 new cross-method/support/multiplicity/persistence controls. Independent
injection, clique, package and rigid oracles stay unchanged and green. Both
original probe and selected runtime/native/test/input/metadata identities pass.

Marginal site support in reference consensus does not guarantee minimum common
support across the whole query. Clique packages enforce joint intersection;
rigid layouts reuse that rule. A known repeated source under a new ID can affect
eligibility, frequency and site mean while weights remain one. Native metadata
retains member/constraint evidence; shared atoms across distinct roles are not
reused typed occurrences. No molecular, provider, dependency or runtime change.

Items 8–9/13 remain partial beyond this analytical native slice. Real series
balancing, predictive complexity and binding-importance claims require a defined
development cohort/protocol and molecular-provider preparation. Next define
bounded development-only parameter/constraint sensitivity (12), keeping the
reserved holdout unused. #66, #74/MolSysMT #215 and installed/hosted gates retain
independent scope. Original audit text remains unchanged before this addendum.

## Progress — 2026-11-04: native I/O support-library consistency (#81/#6)

[Contract](native_io_diagnostics.md) and [receipt](evidence/native_io_diagnostics_20261104_summary.json)
record 243 passing controls (45 new), all six stable attempt identities, coded
owned refusals retaining ValueError/TypeError inheritance and original provider/
parser/filesystem behavior. Exact concrete types/wording migrate explicitly;
scientific PHMT-E102, admission rules, schema and writer protection remain.

nglview classification now agrees with its mandatory package contract. Existing
native YAML imports have a direct PyYAML>=5.1 requirement (sort_keys API floor),
matching metadata, recipe and three regenerated ordinary environments. Actual
PyYAML 6.0.3 is source-qualified; floor/public/installed/platform delivery remains
separate. No molecular implementation, sibling/prefix, source pin, SDF container
or scientific algorithm changes. Original tests/failures/configuration attempts
are retained; original audit text remains a prefix.

#6 stays partial. Next scope native I/O ArgDigest admission, then return to the
planned development-only sensitivity protocol. #10/#23/#9, #66 and #74/MolSysMT
#215 retain their separate gates; this does not complete the scientific audit.

## First receptor sensitivity slice — 2026-11-04

[#83](https://github.com/uibcdf/pharmacophoremt/issues/83) qualifies the first
[analytical receptor protocol](receptor_sensitivity_protocol.md). The complete
45-cell grid plus one failed frame per unit policy predates execution. All 92
attempts are retained. #84 fixes two unit-roundoff radius equalities with an
explicit bounded positive-site comparison policy; physical tolerances, strict
exclusions, assignment and scoring remain. The original expected table is
unchanged, and original faulty guard assumptions/failures are retained separately.

245 selected cases pass in 198.40 s, including 49 new guards; all five pytest and
one standalone-recorder source/native/test/input identity checks are stable.
The documented recorder executes the same full matrix, preserving coordinates,
inventories, curation inputs, unit policy and actual attribution. See the
[receipt/full evidence](evidence/receptor_sensitivity_20261104_summary.json) and
[case](../docs/content/validation/receptor_sensitivity.md).

Audit item 12 remains partial beyond analytical receptor geometry. Next
prespecify a cached prepared-receptor development extension; molecular direction/
preparation variants remain MolSysMT-owned (#375/#323), actual pockets TopoMT-owned.
No activity labels, held-out data, empirical importance, optimal biological
parameters, performance or installed/public/full-suite claim. #66, #74/MolSysMT
#215, #82/ArgDigest #47/#48 and broader #6 retain their independent gates.

## Prepared ERalpha sensitivity slice — 2026-11-04

[#85](https://github.com/uibcdf/pharmacophoremt/issues/85) applies the
[prespecified receptor protocol](prepared_receptor_sensitivity_protocol.md) to
#52's unchanged real prepared fragment: 64 attempts per matrix, including two
actual failed/unscored frames. 288 selected controls pass (43 new), with all three
recorded source/native/test/input identity checks stable; final pytest/CLI add
NumPy/SciPy/RDKit native identity to the inherited provider footprint. Original
41-pass/two-failure guard and exact envelope correction are retained; independent
oracles and every expected setting stay fixed. Runtime/provider/prefix/dependency,
source coordinates/history/contacts, curation inputs and old evidence stay intact.

The [receipt/full evidence](evidence/prepared_receptor_sensitivity_20261104_summary.json)
and [case](../docs/content/validation/prepared_receptor_workflow.md#prepared-receptor-sensitivity-extension)
distinguish geometric controls from physical/biological parameter justification.
Audit item 12 remains partial for real cohorts and preparation/search uncertainty.
Next inventory actual TopoMT pocket/MolSysMT geometry contracts before declaring
receptor hypothesis generation; missing reusable tools belong in provider issues.
#375/#323, #66, #74/MolSysMT #215, #82/ArgDigest #47/#48 and broader #6 retain their
independent gates. No full-suite, installed/public/all-platform, hosted,
predictive or performance promotion follows.

## Cached receptor hypothesis generation — 2026-11-04

[#86](https://github.com/uibcdf/pharmacophoremt/issues/86) qualifies the
[fixed donor/ring generation pilot](receptor_hypothesis_pilot_protocol.md):
eight separate two-site hypotheses, explicit position-only acceptor omission,
and budgets 8/3/0 with remaining 0/5/8. **110 selected controls pass (34 new)**;
the standalone command also completes both unit policies. Independent raw-input
geometry and synthetic supplied-pair controls, JSON/YAML and full native source
custody pass. The three original harness failures and actual identities remain
in the [receipt/full evidence](evidence/receptor_hypothesis_pilot_20261104_summary.json).
No production runtime/provider/dependency/preparation or original evidence changes.

This is unshipped case support, not a public automatic receptor-modeling API or
biological validation. Audit 12 remains partial. Next design the explicit cached
public contract; further direction chemistry belongs to MolSysMT #375 and optional
pockets to TopoMT #101. Environmental H refinement #323, #66, #74/#215,
#82/ArgDigest #47/#48, broader #6 and installed/public/hosted gates stay separate.

## Public cached receptor generation — 2026-11-05

[#87](https://github.com/uibcdf/pharmacophoremt/issues/87) delivers the explicit
[public source builder](public_receptor_generation.md), with multiple donor/ring
occurrences, separate faces, unit-bearing choices and bounded lazy enumeration.
**192 selected controls pass (54 new)**; 52 fast controls pass after a docstring
clarification. Four recipe blocks and a captured prepared replay execute; native
source/chemical history/cached observations, unit policy and provenance stay intact.
[Original evidence](evidence/public_receptor_generation_20261105_summary.json)
retains initial integration/guard failures. MolSysMT owns all molecular work.

This accepts one explicit geometric profile, not binding validity, preparation,
pockets or installed/public delivery. Next compose optional cached receptor
exclusions. Further acceptor profiles stay MolSysMT #375, optional pockets TopoMT
#101, and environmental H refinement #323. Wider audit 12/#6, #66, #74/#215 and
#82 remain independent; ArgDigest #47/#48 are source-fixed but await public receiving.

## Generated receptor exclusions — 2026-11-05

[#88](https://github.com/uibcdf/pharmacophoremt/issues/88) adds optional paired
cached heavy-atom exclusions to the public receptor generator, sharing existing
facade validation/construction. [Contract](receptor_generation_exclusions.md)
and [original evidence](evidence/receptor_generation_exclusions_20261105_summary.json)
retain 217 passing selected cases (61 new), two-policy strict-boundary controls,
prepared 0/42 clash-pair oracles, unchanged positive fit/enumeration and native
recovery/actual credit. The quota-interrupted attempt remains distinct from final
passing qualification. All molecular operations stay in MolSysMT; declared cache
context checks cannot authenticate source identity or complete heavy coverage.

Audit item 12 remains partial. Next prespecify broader donor/ring/joint/exclusion
development comparisons before evaluating new parameters. These analytical
settings are not independent ligands, physical radii or biological evidence.
Further provider directions, environmental refinement, optional pockets, #66,
ArgDigest published-fix receiving #82 and delivery/hosted gates remain separate.

## Receptor contribution prespecification — 2026-11-05

[#89](https://github.com/uibcdf/pharmacophoremt/issues/89) freezes a
[paired analytical protocol](receptor_contribution_protocol.md) and explicit
60-cell matrix for donor/ring/joint/exclusion contributions, fixed tolerance
and budget blocks. Actual public MolSysMT eligibility finds seven eligible PHE
regions and deterministically retains 337/367/404. Input/custody, actual credit,
all attempts and exact producers remain in the
[receipt](evidence/receptor_contribution_plan_20261105_summary.json).
Eight offline guards protect the prospective declaration. No new model/pose
comparison or biological validation is executed; 342 models/1,710 primary
evaluations are planned workloads. Audit12/15 remains partial. Next #90 executes
the fixed declaration with independent geometry/clash oracles and full failure/
completion accounting. Molecular work remains MolSysMT-owned; provider/data/
delivery and broader chemical/biological gates remain separate.

## Receptor contribution execution — 2026-11-05

[#90](https://github.com/uibcdf/pharmacophoremt/issues/90) measures #89's frozen
60-cell paired experiment: 342 models, 1,710 primary/108 recovery evaluations,
30 unscored zero-budget slots. [Case](../docs/content/validation/receptor_contribution.md)
and [evidence](evidence/receptor_contribution_20261105_summary.json) retain exact
geometry/fit/clash oracles, physical-policy agreement, full source custody and
actual input/operation credit. The 1e-12 distance-record guard correction and
saved-fixture Path import failure are preserved; inputs/helper/plan/results stay
unchanged. Passing evidence covers all 20 scientific mechanisms and eight plan
guards, with 26 final reanalysis passes and previously passing optional controls.

Audit12/15 remains partial beyond this analytical PHE/single-protein slice.
.20 nm exclusions veto PHE337 (two pairs) while preserving positive fit one;
PHE367/404 remain accepted. .40 nm gives 33/20/21 pairs and vetoes all three.
Neither these radii nor the disconnected candidate establish physical binding
or optimal parameters. New chemistry/preparation needs a separate declaration;
biological #66, provider and public/installed/hosted gates remain independent.
All molecular operations remain MolSysMT-owned; production runtime is unchanged.


## Native TYR dual-donor continuation — 2026-11-05

[#91](https://github.com/uibcdf/pharmacophoremt/issues/91) adds a separately frozen
N/O donor chemistry slice: outcome-independent source-order eligibility, 12 cells,
20 models, 100 primary/24 recovery evaluations. All eight scientific mechanisms
and four plan guards have passing evidence; original oracle type/orientation
failures and exact-output reanalysis remain in the
[case](../docs/content/validation/tyr_cardinality.md) and
[receipt](evidence/tyr_cardinality_20261105_summary.json). Two optional-provider
simulations and the unchanged existing overlapping-site control pass separately.
The scientific driver/plan/inputs/answers remain unchanged during guard repair.
All four identity phases and source/chemistry/observation/candidate/unit custody
remain stable; all molecular operations stay in MolSysMT.

Audit12/15 remains partial. Native targets are separated by 1.288/.746 nm at
.02 nm radius: lost-target partial fits do not isolate overlapping-record reuse
prevention, nor establish biological essentiality. No affinity/physical-ligand/
optimal-offset/performance/target-breadth claim follows. Next receive exact
MolSysMT #375 acceptor geometry/input identities and declare independent angular
controls before another projection profile. No production/provider/dependency/
release changes; #66/#82/#74/#215 and hosted/installed/public gates stay separate.


## Carbonyl acceptor receiving declared — 2026-11-05

[#92](https://github.com/uibcdf/pharmacophoremt/issues/92) reviews the existing
experimental MolSysMT #375 admission and freezes a carbonyl-only receiving study.
[Protocol](carbonyl_acceptor_receiving_protocol.md) and
[receipt](evidence/carbonyl_acceptor_plan_20261105_summary.json) retain exact
source/doc/API/model/test identities, zero new molecular direction/model/pose
execution and eight passing offline declaration guards with stable identities.
The source contract is enough to design controlled receiving; neither a new
provider reply nor stable public delivery or energetic/biological validation is
inferred. Original provider tests are inspected, not rerun.

[#93](https://github.com/uibcdf/pharmacophoremt/issues/93) must execute the fixed
12-model/72-primary/24-recovery matrix before a public acceptor profile proposal.
Two carbonyl lobes are separate one-site donor hypotheses, with explicit target
axis -u, repeated source positions, external support and unit/missing-state
controls. Molecular representations/inspection/geometry/transforms stay in
MolSysMT; runtime/default feature/profile/provider/dependency/release and prior
#89–#91 scientific evidence remain unchanged. Audit12/15 and the existing data,
provider/refinement/pockets and hosted/installed/public gates remain partial.


## Experimental carbonyl source receiving measured — 2026-11-05

[#93](https://github.com/uibcdf/pharmacophoremt/issues/93) executes the unchanged
#92 declaration: 12 models, 72 primary/24 recovery evaluations, two positive
provider calls and four unsupported/undefined source queries without scores.
All37 selected controls pass (29 scientific/receiving, eight declaration),
including independent source/query/candidate/assignment oracles, sparse repeated-
position/source/role mappings, units, custody, native recovery and actual credit.
[Case](../docs/content/validation/carbonyl_acceptor_receiving.md) and
[receipt](evidence/carbonyl_acceptor_receiving_20261105_summary.json) preserve the
initial unit-map API adapter failure before directions/models/poses and its
same-unit conversion fix. Both full identity phases remain stable; original
scientific plan/protocol/answers remain unchanged. Optional absence/failure
simulations each retain their own two-model/12-primary/four-recovery subset.

Audit12/15 stays partial beyond one-aldehyde analytical receiving. Separate lobes
are alternative one-site donor hypotheses; unsupported water and undefined
carbonyl remain unscored. This is not broader chemistry, electronic/energetic,
biological, target-breadth, performance or installed/public qualification.
All molecular operations remain MolSysMT-owned. No production/default/profile/
provider/prefix/pin/dependency/release change. Next#94 designs/qualifies explicit
public cached-carbonyl generation; existing provider/data/delivery gates persist.
