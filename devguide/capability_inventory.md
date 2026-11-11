# Current capability inventory

Reviewed 2026-11-04 against source base `1c6a03479bd0514a5d5988a8134b8359bca837b9`
and the scoped dispatcher contract overlay recorded in
[the receiving receipt](evidence/model_dispatch_contract_20261104_summary.json).
Owner: LMMV/dprada; audit items 2–3 and [#6](https://github.com/uibcdf/pharmacophoremt/issues/6).
This is a maintained product map, not a release, full API reference or predictive
validation certificate. Update the affected row when an entry point, scientific
contract or qualification boundary changes.

**Available** means an executable public route with named controls in its stated
scope. **Partial** means useful implementation with an explicit compatibility,
scientific or delivery limit. **Planned** means no qualified operational route is
identified here. Availability never implies experimental predictive accuracy.
Historical receipts retain their original revisions/environments; this review
executes only the selected dispatcher/compatibility controls.

The later [0.5.0 source cut](release_0_5_0_source_cut.md) qualifies the complete
controlled source suite at 2bff5dc (eight cells, 3,088 passes each), without a
new public package or a biological prediction claim. Later main commits and
the next [0.6.0 reconstruction proposal](archive/native_feature_reconstruction.md)
retain separate identities and qualification.

## Modeling routes

The [native-v2 archive integration](native_feature_archive.md), #194/#195, adds
public record factories, explicit assembly, retained source/global-ordinal lineage
and guarded subset rebasing through the existing publication/recovery. Source
receives 312 selected controls under actual public PyUnitWizard 0.28.1; source
nm/pm examples/strict docs pass, exact-owned receiving remains pending. Historical v1 remains original; no
cross-profile conversion, collection or molecular authentication is introduced.

The [standalone native payload producer](native_feature_payload.md), #195, is
implemented in development source: complete captured classical inventories,
explicit evaluated-empty/unobserved distinction, original maps/frame/state/
references, sealed quantities, cold metadata and fresh native reads. The
[receipt](evidence/native_feature_payload_20261111.json) receives 245 selected
source and exact-owned cases each under the actual public quantity floor,
including nondefault/first-activation policy and maximum admission. Source/owned
examples under nm/pm and strict full docs pass; 177 runtime bodies are source-equal.
Its later native-v2 integration above retains separate receiving; this adds no
collection, molecular authentication or public package.

Development after #193 also receives the
[first writer-owned archive](public_feature_archive_store.md): whole-generation
preservation, immutable candidates, expected-current publication and retained
attempt/linked recovery. The [source/owned receipt](evidence/feature_archive_writer_20261111.json)
receives 150 cases per context and executable guides. New native payload archive
admission and arbitrary/subset assembly remain later #195/#194 scope; no new public artifact,
collection, source authentication or broad performance claim follows.

Development after source tag 0.5.0 adds
[`screening.reuse_feature_inventories`](native_feature_reconstruction.md), with
explicit historical profile admission, fresh quantity/native geometry validation
and full original inventories. [Source/owned and public-floor receiving](evidence/native_feature_reconstruction_20261111.json)
passes in the declared scope; full supported delivery remains independent. This
operation performs no molecular extraction or query/source authentication.

The package-level `pharmacophoremt.model` is a facade. Method names below are
exact strings; there is no automatic method selection or implicit preparation.
Every molecular input, selection, recognition, geometry or transformation belongs
to MolSysMT. Cached observations must correspond to the unchanged prepared source;
a user declaration alone cannot authenticate that identity.

[Published ArgDigest 0.17.1 receiving](native_io_argdigest_receiving.md), #82,
now protects literal keyword/source identity and activates four closed native
codec contracts with TypeError-compatible diagnostics. ArgDigest >=0.17.1 is
required; broader #6 and installed/public dependency closure remain separate.

| Public route | State and input contract | Output and scientific limit | Owning controls / contract |
| --- | --- | --- | --- |
| `model(..., method="reference-ligand")`; `modeler.from_ligand`, `from_feature_inventory` | Available for prepared ligand or cached native inventory | One query; feature presence does not establish binding importance | [Workflow](reference_ligand_workflow.md), [tests](../tests/test_reference_ligand.py) |
| `method="interaction-based"`; `modeler.from_interactions` | Available for supplied native observations and explicit ligand selection | One query from cross-boundary observations; contacts are not interaction energies | [Tests](../tests/test_pose_evaluation.py), [ionic](../tests/test_ionic_interactions.py), [aromatic](../tests/test_aromatic_interactions.py) |
| `method="interaction-collection"`; `modeler.from_interaction_collection` | Available for named compatible analyses on one prepared source/frame | One composed query; source maps, duplicate policy and observation coverage matter | [Workflow](interaction_composition_workflow.md), [tests](../tests/test_interaction_composition.py) |
| `method="complex-based"` (default); `ComplexBasedModeler` | Available as explicit cached-collection facade; requires ligand selection and collection | One query for one frame; list for multiple requested frames. No automatic complex preparation/detection | [Workflow](complex_based_workflow.md), [tests](../tests/test_complex_based_facade.py) |
| `method="structure-based"`; `StructureBasedModeler`, `from_receptor_projections` | Available for cached receptor inventory and caller-declared projections | One hypothesis in the cached frame, optional explicit exclusions. No pocket discovery or inferred optimal ligand pose | [Workflow](structure_based_workflow.md), [tests](../tests/test_receptor_projections.py) |
| `modeler.from_receptor_features` | Available in development source for explicit donor/aromatic generation and the experimental cached-carbonyl and aromatic-N profiles, with physical distance/radius choices, finite budgets and optional cached exclusions | Separate hypotheses, exact completion/omissions and independent zero-weight exclusions; experimental acceptors require native MolSysMT directions and explicit structure position/orientation. Aromatic-N receiving admits the provider's defined models2/3, not unsupported carboxylates. Cache consistency does not authenticate source. No molecular operation, pruning, ranking or biological qualification | [Original contract](public_receptor_generation.md), [carbonyl contract](public_cached_carbonyl_generation.md), [aromatic-N contract](public_cached_aromatic_n_generation.md), [exclusions](receptor_generation_exclusions.md), [carbonyl controls](../tests/test_cached_carbonyl_generation.py), [aromatic-N controls](../tests/test_cached_aromatic_n_generation.py), [replay case](../docs/content/validation/public_carbonyl_generation.md) |
| `method="ligand-based"`; `LigandBasedModeler` | Available with explicit `consensus_method="rigid"` or `"aligned_cliques"` and prepared ligand records | List of models, possibly empty. Legacy conformer-generation options accept only inert defaults; no implicit chemical preparation | [Tests](../tests/test_ligand_based_facade.py), [workflow](prepared_consensus_workflow.md) |
| `modeler.from_aligned_ligands` | Available as a direct tool, outside the generic facade's six method names | Reference-based consensus in a declared shared frame; reference dependence remains | [Workflow](aligned_consensus_workflow.md), [tests](../tests/test_aligned_consensus.py) |
| `modeler.from_aligned_ligand_cliques`, `from_rigid_ligands` | Available as direct tools with explicit support/search budgets | Joint-support hypotheses; rigid fits delegated to MolSysMT, no exhaustive conformational optimum | [Aligned workflow](aligned_clique_consensus_workflow.md), [rigid workflow](rigid_consensus_workflow.md) |
| `modeler.compose_pharmacophores`, `copy_pharmacophore`, `extract_pharmacophore`, `edit_pharmacophore` | Available for native hypotheses with declared source/frame relations | Composition and curation; no molecular copying engine. [Live-reference ownership is qualified under #60](live_reference_ownership.md) | [Composition tests](../tests/test_interaction_composition.py), [curation tests](../tests/test_curation.py) |

## Matching, evaluation and supporting surfaces

| Public surface | State and demonstrated scope | Explicit limit / remaining work |
| --- | --- | --- |
| `screening.PoseEvaluator` | Available: fixed-pose typed-record one-to-one assignment, any-of Point/Sphere kinds, essential sites, weights, directions and exclusions; [contract/#79 controls](native_constraint_semantics.md) | Disk uses declared center/axis matching, not physical disk intersection. Geometry compatibility is not binding affinity |
| `RigidPoseSearch`; modular correspondence, placement, ranking and refinement tools | Available: finite rigid proposals with provider-owned fits; [search](../tests/test_rigid_search.py), [modular](../tests/test_modular_rigid_tools.py), [refinement](../tests/test_rigid_refinement.py) controls | `seeded_hit` is discrete search success; incomplete budget/coverage stays explicit. No global continuous optimum or docking engine |
| `ConformerScreening`, `VirtualScreening` | Available for explicitly supplied prepared frames and selected evaluation method; [conformer](../tests/test_conformer_screening.py), [facade](../tests/test_virtual_screening.py) controls | No hidden conformer generation. Failed evaluations remain unscored, not valid negatives; inert legacy parameters are not active algorithms |
| `screening.PreparedInput`, `screen_prepared` | Development source and bounded owned-wheel receiving: all-outcome incremental native evaluation with explicit work/source/occurrence maps; [contract/evidence](public_prepared_screening.md), [recipe](../docs/content/cookbook/prepared_incremental_screening.md), [controls](../tests/test_public_prepared_screening.py) | Preflight before source iteration; caller-owned readers; encounter order is not a global ranking. Public recovery/journal/collections and full supported installed/public/platform qualification remain separate |
| `screening.PreparedScreeningRun`, plan/expert resume; independent `pharmacophoremt_results` | [Versioned saved runs](public_prepared_runs.md), confirmed progress, interruption/resume, complete export and independent inspection;197 selected local cases, source/same-wheel owned installed recipes and normal editable receiving pass | Bounded Linux/Python3.14/source providers. New-format writing, explicit legacy reading and conservative binding are distinct; no snapshot authentication, cross-version scientific equivalence, multiwriter/power-loss or full public-platform claim |
| `validation.enrichment_factor`, `roc_auc`, `bedroc`; `RetrospectiveValidator` | Available: native tie-aware metrics and declared-label evaluation; [metric](../tests/test_validation_metrics.py), [retrospective](../tests/test_retrospective.py) controls | Metrics alone establish neither label validity nor external prediction. Independent protocol, leakage controls, baselines and uncertainty remain audit items 10–15/#66 |
| `validation.summarize_screening_run`, `compare_screening_runs`; `ScreeningRunView.work_items()` | [Single-run](saved_run_analysis.md) and [paired-run](saved_run_comparison.md) original-cohort analysis retain native evidence and separate pending/failure/upstream counts. #147 passes301distinct selected source cases and the same256original bodies/recipe in one owned installed artifact | Both complete arm summaries are materialized. Paired metrics use only common scored original samples, including zero scores; full source/public/platform, label/independence and biological qualification remain separate |
| `validation.LeaveOneOutValidator` | Partial: explicit modeler/evaluator orchestration and [native status/recall controls](../tests/test_virtual_screening.py) | Selects the first hypothesis; recall is internal self-consistency, not independent prediction. Grouping, model selection and leakage review remain necessary before a predictive claim |
| `Pharmacophore`, feature/shape objects | Available as native representation; Point/Sphere/SphereAndVector/Disk have [contract controls](../tests/test_native_geometry_contracts.py) | An exported shape class does not imply support by every matcher/serializer. Extension registration and richer relations remain planned |
| JSON/YAML; annotated SDF; RDKit/LigandScout/Pharmer translators | Partial across formats: implemented routes with [dispatch](../tests/test_io_dispatch.py), [SDF](../tests/test_io_sdf.py), [RDKit](../tests/test_io_rdkit.py), [LigandScout](../tests/test_io_ligandscout.py), [Pharmer](../tests/test_io_pharmer.py) controls | [First field/schema matrix](persistence_fidelity.md) records #75 reader validation and [#76 native schema/writer qualification](native_schema.md). Direct RDKit SDF container use is migration debt under #74 / MolSysMT #215. Generic `.sdf` loading is molecular MolSysMT conversion; annotated pharmacophore SDF uses `load_sdf` explicitly |
| `io.from_pharmer`, constructor and IO facade | [Supported Pharmer profile](pharmer_interoperability.md): enabled-point omission, vector activation and explicit warn/raise/ignore losses; same141source/exact owned wheel198cases pass with three ordinary profiles and complete P1driver | Required compatible fields only; optional/negated/size/unknown/settings meaning is reported rather than invented. Molecular delegation remains MolSysMT. External engine/export/perception/search equivalence and full supported delivery remain separate |
| Native Point center inspection | [Source/owned-wheel correction #142](native_geometry_inspection.md): canonical center alias, ordinary center/distance queries and empty (N,3) output | The same 338 library bodies pass in source and one owned Linux/Python3.14 wheel; full supported gates remain separate |
| `io.to_rdkit`, `io.load_rdkit` | [Source/owned-wheel projection](rdkit_projection.md): default point/fixed-radius routes, explicit sphere/radius exchange and detached field/loss/default reports | Same214 bodies pass in one owned Linux/Python3.14 wheel; public/full-platform gates remain separate. Field retention does not imply matching/embedding equivalence or pair-bound inversion |
| `attribution`, `attribution_report` | Partial delivery: optional scientific provenance and detached records implemented; [controls](../tests/test_attribution.py) | #19/#23 retain public-provider/installed qualification; recorded branches are distinct from reviewed literature |
| MolSysViewer rendering/addon | Partial integration with existing source payload/render paths | Browser acceptance remains #58; addon is deferred by maintainer priority, not represented as absent code |
| Public package/platform support | Separate delivery axis under #10/#23 | Existing public 0.4.0 and its exact installed receipts do not qualify every later source commit or all provider combinations |

## Planned capabilities and provider boundaries

The generation roadmap remains prospective. `.h5phmt`, general dynamical/MSM
pharmacophores, covalent/peptide/water-specific workflows, AI methods and native
accelerated/distributed backends have no qualified public route in this inventory.
Do not present the layouts in [I/O planning](io_and_formats.md) or advanced roadmap
chapters as implemented functionality. `Modeler` is an abstract scaffold, not a
seventh working method.

MolSysMT owns molecular preparation, chemistry, inspection and general molecular
calculations. Its missing capabilities go to its issue board (#323 and other
bounded receiving gates retain their original scope); PHMT must not fill them
with local molecular routines. Pocket analysis belongs to TopoMT, docking to
DockingMT and molecular rendering to MolSysViewer. Their ownership is not a claim
that the required provider API already exists.

## Dispatcher contract and next checks

The scoped ArgDigest declaration reads admitted keyword names from the actual
PHMT endpoint signatures. It keys on `method`, adds the builder's frame argument
for complex/structure routes, and admits the union of the two ligand consensus
routes. The ligand facade still enforces its narrower `consensus_method` contract
and compatibility restrictions. This is PHMT option routing, not a molecular
option registry. Adding an endpoint parameter updates admission automatically;
a new method still requires an explicit scientific route and tests.

`system` and `mol_sys` are the existing aliases of `molecular_system` at this
facade. Declared normalization rejects simultaneous names instead of silently
overwriting an input. It is scoped here; other callers retain their current hook.
Unknown keywords now raise ArgDigest `UnknownArgumentError` before endpoint work.
Unknown methods retain their existing `ArgumentError`; with explicit digestion
bypass the dispatcher retains `NotImplementedError`. Mandatory scientific checks
inside the builders are unchanged. `skip_digestion=True` is a deliberate internal
bypass, not a claim that arbitrary calls have been validated.

The [new contract guards](../tests/test_model_dispatch_contract.py) use endpoint
spies to verify boundary order/identity; existing real molecular workflow tests
provide the separate compatibility controls. They do not test predictive utility.

Current follow-up (2026-11-06): native persistence, ownership, merge, constraint
semantics and facade contracts retain their separately qualified source scopes.
The [receptor sensitivity matrix](receptor_sensitivity_protocol.md),
[prepared-source extension](prepared_receptor_sensitivity_protocol.md) and
[cached-generation pilot](receptor_hypothesis_pilot_protocol.md) remain analytical
or preparation controls, not biological studies. Cached exclusions are already
implemented under [#88](receptor_generation_exclusions.md), and the explicit
[aromatic-N profile](public_cached_aromatic_n_generation.md) is received under
#105 with250 unique selected passing controls. These counts retain their own
original producers and must not be added across overlapping selections.

Next scientific work is the separately declared source/cohort and preparation
admission under [#103](pending_proposals/qualify_receptor_screening_studies.md),
including #66's original ERalpha methods and #106's BRD4 qualification. Required
carboxylate/environmental-H and molecular/grouping gaps stay with MolSysMT
#375/#323/#447; optional pocket receiving stays with TopoMT #101. Broader #6
contracts, SDF ownership #74/MolSysMT #215 and public source/installed/package
qualification remain independent. The [checkpoint](checkpoint.md) identifies
the current next action; the dated sections below preserve their earlier scope.

## Persistence review — 2026-11-04

See [field/schema and ownership review](persistence_fidelity.md): #75 reader
validation is fixed with 207 focused checks; #74 explicitly tracks unqualified
SDF-container ownership until a public MolSysMT record/property API is received.

## Native schema/writer receiving — 2026-11-04

[#76 native contract](native_schema.md) records tagged JSON/YAML schema/field
admission, legacy compatibility and validation/encoding before destination opening.
265 focused controls pass. SDF private payload/container unchanged, with #74 /
MolSysMT #215 still pending. Remaining format-specific fidelity is separate.

## Ownership receiving — 2026-11-04

#60's [contract](live_reference_ownership.md) qualifies existing independent native
curation data, intentional live molecular references and explicit public MolSysMT
eager copies. 199 focused source controls pass, with no runtime/provider/floor
change or installed claim. Legacy Pharmacophore.merge remains separate #77.

## Merge facade received — 2026-11-04

[#77 contract](pharmacophore_merge.md) migrates legacy merge onto the existing
public keep-policy composer. Metadata from both components is retained;
independent sites and explicit frame/provenance/score behavior replace the old
shared-site/empty-metadata result. Molecular source remains an intentional live
reference; no molecular copying or new scientific composition method is added.

## Nested constructor receiving — 2026-11-04

[#6/#78 contract](nested_facade_contracts.md) records method-specific native
constructor admission and explicit local VirtualScreening skip controls. 167 source
controls pass; methods/scoring/cache/scientific constraints remain. Broader batch/
public provider/installed receiving stays separate. No molecular options registry
or new scientific backend is introduced.

## Native constraint interpretation — 2026-11-04

[#79 contract](native_constraint_semantics.md) makes any-of feature lists and
unique typed-record capacity explicit. Shared atom membership across distinct
roles is permitted; donor-H identity was already retained. 368 focused controls
pass, including 40 new semantics/provenance/persistence cases. Result criteria
are additive; the assignment algorithm, defaults and molecular provider are
unchanged. Audit 8–9 remains partial outside this bounded native slice.

## Consensus support/redundancy receiving — 2026-11-04

[#80 review](consensus_support_review.md) compares native reference, aligned-clique
and pivot-rigid methods with 126 selected passing controls (28 new). Reference
support is per site; clique/rigid hypotheses require common supporters, with rigid
scope per layout. Known input repetition changes counts/means, not unit weights.
No runtime/helper/provider or dependency source changes. Existing independent
oracles stay green; broader audit 8–9/13 and biological balancing remain partial.
Next define bounded development-only sensitivity/ablation (12) without holdout use.

## Native diagnostic receiving — 2026-11-04

[#81 contract](native_io_diagnostics.md) and
[receipt](evidence/native_io_diagnostics_20261104_summary.json) add coded owned
native I/O refusals (PHMT-E108/E109) while preserving ValueError/TypeError catch
compatibility, data admission and original parser/provider/filesystem errors.
243 selected cases pass; exact concrete types/wording migrate explicitly.
#6 dependency declarations align nglview and the existing direct PyYAML codec.
No native schema, scientific algorithm, molecular/SDF implementation or installed/
public qualification change; broader ArgDigest admission remains separate.


## Native batch admission consolidated — 2026-11-05

[#99](https://github.com/uibcdf/pharmacophoremt/issues/99) qualifies a bounded
item 3/#6 contract improvement: unknown/wrong-method/literal kwargs options fail
before native input consumption even for empty batches. Nine definition-owned
ArgDigest contracts preserve scientific ASTs, method-specific frames, pose IDs,
failure causes and facade cache order. [Contract](native_batch_contracts.md) and
[receipt](evidence/native_batch_contracts_20261105_summary.json) retain original
failures/two corrected scoring fixtures and 206 unique passing final selectors
(45 new), with public-prefix/modern-source scopes kept separate. Serial one-CPU/
1-GiB/no-swap/low-priority resource limits are verified from actual processes.
No scientific model, molecular implementation, provider/floor or release change.
Item 3/#6 remains partial: next review saved-result/retrospective admission;
provider delivery, broader science and #9/#10/#23 full gates remain separate.
