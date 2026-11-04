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

## Modeling routes

The package-level `pharmacophoremt.model` is a facade. Method names below are
exact strings; there is no automatic method selection or implicit preparation.
Every molecular input, selection, recognition, geometry or transformation belongs
to MolSysMT. Cached observations must correspond to the unchanged prepared source;
a user declaration alone cannot authenticate that identity.

| Public route | State and input contract | Output and scientific limit | Owning controls / contract |
| --- | --- | --- | --- |
| `model(..., method="reference-ligand")`; `modeler.from_ligand`, `from_feature_inventory` | Available for prepared ligand or cached native inventory | One query; feature presence does not establish binding importance | [Workflow](reference_ligand_workflow.md), [tests](../tests/test_reference_ligand.py) |
| `method="interaction-based"`; `modeler.from_interactions` | Available for supplied native observations and explicit ligand selection | One query from cross-boundary observations; contacts are not interaction energies | [Tests](../tests/test_pose_evaluation.py), [ionic](../tests/test_ionic_interactions.py), [aromatic](../tests/test_aromatic_interactions.py) |
| `method="interaction-collection"`; `modeler.from_interaction_collection` | Available for named compatible analyses on one prepared source/frame | One composed query; source maps, duplicate policy and observation coverage matter | [Workflow](interaction_composition_workflow.md), [tests](../tests/test_interaction_composition.py) |
| `method="complex-based"` (default); `ComplexBasedModeler` | Available as explicit cached-collection facade; requires ligand selection and collection | One query for one frame; list for multiple requested frames. No automatic complex preparation/detection | [Workflow](complex_based_workflow.md), [tests](../tests/test_complex_based_facade.py) |
| `method="structure-based"`; `StructureBasedModeler`, `from_receptor_projections` | Available for cached receptor inventory and caller-declared projections | One hypothesis in the cached frame, optional explicit exclusions. No pocket discovery or inferred optimal ligand pose | [Workflow](structure_based_workflow.md), [tests](../tests/test_receptor_projections.py) |
| `method="ligand-based"`; `LigandBasedModeler` | Available with explicit `consensus_method="rigid"` or `"aligned_cliques"` and prepared ligand records | List of models, possibly empty. Legacy conformer-generation options accept only inert defaults; no implicit chemical preparation | [Tests](../tests/test_ligand_based_facade.py), [workflow](prepared_consensus_workflow.md) |
| `modeler.from_aligned_ligands` | Available as a direct tool, outside the generic facade's six method names | Reference-based consensus in a declared shared frame; reference dependence remains | [Workflow](aligned_consensus_workflow.md), [tests](../tests/test_aligned_consensus.py) |
| `modeler.from_aligned_ligand_cliques`, `from_rigid_ligands` | Available as direct tools with explicit support/search budgets | Joint-support hypotheses; rigid fits delegated to MolSysMT, no exhaustive conformational optimum | [Aligned workflow](aligned_clique_consensus_workflow.md), [rigid workflow](rigid_consensus_workflow.md) |
| `modeler.compose_pharmacophores`, `copy_pharmacophore`, `extract_pharmacophore`, `edit_pharmacophore` | Available for native hypotheses with declared source/frame relations | Composition and curation; no molecular copying engine. Remaining live-reference ownership review is #60 | [Composition tests](../tests/test_interaction_composition.py), [curation tests](../tests/test_curation.py) |

## Matching, evaluation and supporting surfaces

| Public surface | State and demonstrated scope | Explicit limit / remaining work |
| --- | --- | --- |
| `screening.PoseEvaluator` | Available: fixed-pose typed one-to-one assignment, essential sites, weights, directions and exclusions; [controls](../tests/test_pose_evaluation.py) | Disk uses declared center/axis matching, not physical disk intersection. Geometry compatibility is not binding affinity |
| `RigidPoseSearch`; modular correspondence, placement, ranking and refinement tools | Available: finite rigid proposals with provider-owned fits; [search](../tests/test_rigid_search.py), [modular](../tests/test_modular_rigid_tools.py), [refinement](../tests/test_rigid_refinement.py) controls | `seeded_hit` is discrete search success; incomplete budget/coverage stays explicit. No global continuous optimum or docking engine |
| `ConformerScreening`, `VirtualScreening` | Available for explicitly supplied prepared frames and selected evaluation method; [conformer](../tests/test_conformer_screening.py), [facade](../tests/test_virtual_screening.py) controls | No hidden conformer generation. Failed evaluations remain unscored, not valid negatives; inert legacy parameters are not active algorithms |
| `validation.enrichment_factor`, `roc_auc`, `bedroc`; `RetrospectiveValidator` | Available: native tie-aware metrics and declared-label evaluation; [metric](../tests/test_validation_metrics.py), [retrospective](../tests/test_retrospective.py) controls | Metrics alone establish neither label validity nor external prediction. Independent protocol, leakage controls, baselines and uncertainty remain audit items 10–15/#66 |
| `validation.LeaveOneOutValidator` | Partial: explicit modeler/evaluator orchestration and [native status/recall controls](../tests/test_virtual_screening.py) | Selects the first hypothesis; recall is internal self-consistency, not independent prediction. Grouping, model selection and leakage review remain necessary before a predictive claim |
| `Pharmacophore`, feature/shape objects | Available as native representation; Point/Sphere/SphereAndVector/Disk have [contract controls](../tests/test_native_geometry_contracts.py) | An exported shape class does not imply support by every matcher/serializer. Extension registration and richer relations remain planned |
| JSON/YAML; annotated SDF; RDKit/LigandScout/Pharmer translators | Partial across formats: implemented routes with [dispatch](../tests/test_io_dispatch.py), [SDF](../tests/test_io_sdf.py), [RDKit](../tests/test_io_rdkit.py), [LigandScout](../tests/test_io_ligandscout.py), [Pharmer](../tests/test_io_pharmer.py) controls | [First field/schema matrix](persistence_fidelity.md) records #75 reader validation and remaining schema/writer policy. Direct RDKit SDF container use is migration debt under #74 / MolSysMT #215. Generic `.sdf` loading is molecular MolSysMT conversion; annotated pharmacophore SDF uses `load_sdf` explicitly |
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

Next bounded work: audit item 4, field/schema preservation across formats, beginning
with native JSON/YAML and explicit SDF. For #6, review the nested ligand-consensus
and screening facade contracts separately rather than extending this domain with
new scientific methods. Experimental study design under #66 can proceed alongside
API work; the original-method access gate remains unresolved.

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
