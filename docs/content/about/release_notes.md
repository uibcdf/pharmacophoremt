# Release notes

## Unreleased — toward 0.6.0

- Expose explicit keyword-only `skip_digestion=False` on `modeler.get_features`
  and `FeatureInventoryPayload.from_inventory`. Default/False retain ordinary
  normalization; True requires canonical arguments and keeps scientific/native
  checks active, including explicit payload-profile admission. Existing inventory
  and wire schemas retain their contracts. See [expert controls](../user/feature_capture.md#expert-argument-controls).
- Add [`modeler.capture_features`](../user/feature_capture.md) to retain the
  effective requested families, completed/evaluated-empty coverage, native
  atom/frame/state maps and original observed extraction software around one
  extraction. `FeatureInventoryPayload.from_capture` saves that observation
  without repeating the evaluated-family declaration. `get_features()` keeps
  its existing signature and ordinary inventory.
- Add [native feature archive v2](../user/native_feature_archives.md) with
  explicit record assembly, original source/global-ordinal lineage, guarded
  subset rebasing and the existing publication/recovery lifecycle. Cold layout
  inspection and explicit native reuse remain separate. Historical v1 stays
  unchanged; implicit or mixed-format migration is refused.
- Add standalone [native feature payloads](../user/native_feature_payloads.md)
  for already captured complete inventories: explicit evaluated families, original
  maps/geometry/references, sealed quantities, cold metadata and fresh native
  reconstruction. Public native records compose these payloads with native-v2
  archive assembly and the same guarded publication/recovery tools.
- Add [writer-owned feature archives](../user/feature_archive_writing.md) that
  preserve whole original generations, stage and validate immutable candidates,
  publish against explicit expected-current identity and expose retained attempts
  with metadata inspection and linked recovery. Native-v2 archives also admit
  explicit caller-assembled records and subsets with retained source lineage.
- Add explicit [native feature reconstruction](../user/native_feature_reuse.md)
  from admitted historical snapshots, with fresh unit/geometry validation,
  generation and original metadata checks, full maps/provenance and bounded batches.
  PyUnitWizard >=0.28.1 supplies the qualified quantity-record capability.
- Run controlled interruption/recovery tests in fresh spawned processes,
  preserving original committed progress, publication visibility and attribution.
- Preserve completed science when an optional attribution error cannot be
  rendered as text. Respect the application's SMonitor capture policy before
  inspecting that text; saved original references and enclosing sessions remain
  independent of later serialization.

### Compatibility and admission

Historical native inventories still require explicit actual evaluated families
and producer declarations through `from_inventory`; feature presence cannot
establish evaluated-empty coverage. Existing inventory and persisted schemas keep
their contracts. Native-only archive v2 uses the explicit `native-classical-v1`
profile; implicit, mixed and cross-profile migration is refused. Captures retain
included-volume evaluations as native inventories, while classical persistence
refuses them, including empty evaluations.

The capture/native payload profile admits at most 256 total source atoms,
64 features and 2 MiB of sealed content, with bounded finite provenance. Each
archive/reuse operation has its own documented quotas and ownership. Digests bind
content and every native read validates quantities/maps afresh; neither authenticates
a molecular source or establishes biological accuracy. Keep prepared sources
unchanged throughout capture. Molecular collection/preparation stays MolSysMT-owned.

The required quantity provider is now **PyUnitWizard >=0.28.1** for the received
QuantityRecord capability. New capture operations expose standard boolean
argument-digestion controls; a bypass does not skip native/content validation.
The existing `get_features` and `from_inventory` signatures remain unchanged.

Selected source/exact-owned receiving is recorded under #193–#196. Complete
supported source qualification, installed/public delivery and the next version/tag
decision retain their separate evidence. This section describes development;
the public installation instructions still refer to the qualified 0.4.0 package.

## 0.5.0 — source-only consolidation

Delivered 2026-11-11 as immutable [source tag 0.5.0](https://github.com/uibcdf/pharmacophoremt/tree/0.5.0)
at `2bff5dcf454bc5230f473237a49939215a60aab2`. All eight controlled Linux/macOS
arm64 × Python 3.11–3.14 source cells pass 3,088 cases each, with zero skipped
scientific cases and 115 qualified coverage paths. Source and tag conformance
also pass. This cut includes no GitHub Release, Conda/PyPI package or hosted-
documentation publication. Exact evidence and the reviewed decision are tracked
in [#95](https://github.com/uibcdf/pharmacophoremt/issues/95)
and the [source-cut contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/release_0_5_0_source_cut.md).
The [installation guide](installation.md) still describes the independently
qualified public 0.4.0 package. Further feature development continues toward 0.6.0.

### Prepared screening and independent saved evidence

- Public `screening.PreparedInput` and `screen_prepared` consume explicitly
  prepared inputs incrementally, preserve literal work/source/occurrence mappings
  and export outcomes in encounter order. Valid negatives retain zero; failures
  remain unscored. See [incremental screening](../cookbook/prepared_incremental_screening.md).
- `PreparedRunPlan`, `build_prepared_run_plan`, `PreparedScreeningRun` and
  `resume_prepared_run` provide explicit plan/create/open/resume composition.
  Friendly run ownership and expert store operations use the same decisions.
  [Recoverable screening](../cookbook/recoverable_prepared_screening.md) separates
  confirmed deliveries, original attempts and the complete saved view.
- The same-distribution `pharmacophoremt_results` namespace and its CLI inspect
  saved progress, plans, source/work identities, selections and original details
  without importing the scientific stack. Protected JSONL/CSV exports retain
  original configuration/byte identities and explicit pending counts. Historical
  experimental formats require explicit legacy admission and are not migrated.
- `validation.summarize_screening_run` and `compare_screening_runs` use an
  explicitly mapped original cohort, retain full summaries and recompute paired
  metrics on common scored work. See [saved analysis](../cookbook/saved_run_analysis.md)
  and [comparison](../cookbook/saved_run_comparison.md). Pending, failed and upstream
  unavailable work remain distinct; a readable run is not scientific-resume admission.
- The new same-distribution `pharmacophoremt_features.FeatureAssetView` reads a
  pinned metadata archive, pages declared coverage and returns exact opaque
  original bytes. The [guide and analytical download](../user/feature_archives.md)
  demonstrate literal selections, global ordinals and evaluated-empty versus
  unobserved families. Counts remain producer declarations. Native payload
  decoding, quantity validation, source/query admission and public writers are
  separate future capabilities.

`PreparedRunPlan.describe()` exposes exact captured query byte identity and a
detached original context. Console display remains bounded and omits raw query/
context bodies. Source/version changes can require a new linked execution run
under the conservative software binding, while historical reading stays available.

The explicitly selected receptor profile
`donor_aromatic_carbonyl_aromatic_n_experimental` adds model2 carbonyl and model3
aromatic-N alternatives while retaining older profiles. Its
[bounded evidence](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/public_cached_aromatic_n_generation.md)
includes analytical controls and original HIS524 cache consumption, separately
from biological utility or public molecular-provider delivery.

### New capabilities since 0.4.0

- **Bounded cached receptor generation:** `modeler.from_receptor_features`
  builds separate donor/aromatic hypotheses with explicit physical choices,
  exact Cartesian-product counts, finite budgets and optional cached exclusions.
  The separately selected `donor_aromatic_carbonyl_experimental` profile consumes
  native MolSysMT carbonyl-direction evidence. It requires explicit structure
  position, distances and target donor orientation. Alternative lobes remain
  separate hypotheses; unsupported/undefined geometry stays visible. See the
  [recipe](../cookbook/structure_based_modeler.md) and
  [public carbonyl analytical case](../validation/public_carbonyl_generation.md).
- **Explicit molecular-ranking criterion:** rigid and prepared-conformer search
  can select `search_method="seeded_hit"`. This tests fitted triplet seeds and
  supplies a binary `ranking_score`, separately from a checked pose's
  `fit_value`. `screening.get_screening_score` reads the declared criterion
  without recomputing molecular observations.
- **Saved-result analysis:** `validation.summarize_screening_results` and
  `compare_screening_results` account for the original cohort, explicit input
  mappings, failures/unscored inputs, evaluated-subset metrics and paired
  common-subset statistics/deltas. Reading saved results performs no molecular calculation. See
  the [saved-result recipe](../cookbook/retrospective_validation.md#summarize-saved-results-against-the-original-cohort).

Reference-ligand, interaction/complex-based, consensus, placed-pose and rigid
workflows already existed in 0.4.0. Subsequent receiving studies and contract
repairs strengthen their stated scope; they are not all new 0.5.0 algorithms.

### Behavior and migration

1. **Select the ranking criterion for rigid/conformer facades.** For binary
   seed-only ranking, pass `search_method="seeded_hit"` to `VirtualScreening`
   with `screening_method="rigid"` or `"conformers"`. To retain the compatibility
   search's checked-pose coverage, explicitly pass
   `score_method="checked_pose_coverage"`. `RetrospectiveValidator` applies the
   same distinction. Placed evaluation retains checked-pose coverage. Direct
   `RigidPoseSearch` still defaults to `placed_and_triplets`.
2. **Read score fields by meaning.** Hit records and table exports now expose
   `ranking_score` and `score_method` alongside `fit_value`. A completed seed-only
   negative can have score zero and `fit_value=None` because no pose was fitted.
   A failed or unresolved evaluation remains unscored. Binary ties retain input
   order; the criterion is not a continuous-pose optimum or binding affinity.
3. **Validate native records on input.** New JSON/YAML writes declare
   `schema="pharmacophoremt.native@1"`; readers also accept valid historical
   untagged records. Versioned records reject missing/unknown envelope and shape
   fields. Readers validate physical values, units, shapes, feature/shape
   compatibility and metadata. Malformed records previously admitted by internal
   bypasses can now fail. Native format diagnostics retain ValueError
   compatibility.
4. **Expect I/O options to be checked.** `io.load` forwards options to the chosen
   reader. Closed pharmacophore readers reject extra keywords; molecular options
   and original conversion failures reach MolSysMT unchanged. Native writers
   validate/serialize before opening the destination, protecting an existing
   file from scientific admission/encoding failures. This does not promise an
   atomic filesystem transaction.
5. **Treat merged models as independent results.** `Pharmacophore.merge`
   delegates to public composition with `duplicate_policy="keep"`. Result sites
   and metadata no longer alias input sites. Both components' metadata/scores/
   references are retained under the labeled `metadata["components"]` records;
   root score and `ref_mol` are unset. Conflicting declared frames are refused.
   Supply models in a common coordinate frame; equal indices do not authenticate
   molecular origin. In-place edits of a shared site must select every occurrence.
6. **Use explicit supported options.** Definition-owned ArgDigest contracts
   constrain modeling, ligand-consensus, screening and native geometry options.
   Unknown/method-incompatible keywords fail earlier. Generic digestion bypasses
   do not bypass native scientific checks. The ArgDigest
   minimum is now >=0.17.1 for the received binding/error-family repairs;
   PyYAML >=5.1 is an explicit required dependency, and the existing
   required NGLView dependency is consistently classified.
7. **Check native batch options even for empty input.** With normal digestion,
   `PoseEvaluator.run`,
   `RigidPoseSearch.run` and `ConformerScreening.run` refuse unknown or wrong-method
   options before native input consumption. Use `structure_index` for a single
   pose/rigid frame and `structure_indices` for prepared conformers.
   `VirtualScreening` still clears its result caches before delegating. Applications
   adding `evaluate` parameters must own their corresponding batch API/contract.
8. **Choose EF fractions with distinct report keys.** `RetrospectiveValidator`
   now uses the same settings validation as saved-result summaries. Fractions
   formatting to the same `EF@...%` key raise before cohort materialization or
   native evaluation, including internal digestion bypass. Previously one result
   could overwrite another. Valid fractions, defaults and metric formulae remain.
9. **Keep the existing source-name policy.** Direct single-source APIs use
   `molecular_system`. The `model()` dispatcher also accepts one declared
   `system` or `mol_sys` alias and refuses competing names. This clarification
   does not introduce aliases to other closed APIs; unknown names already fail
   before molecular access.

Default chemical acceptors remain position-only. The original donor/aromatic
generation profile remains available; it does not silently select carbonyl
geometry. Prepared inputs, states, selections, frames and physical settings remain
explicit caller responsibilities.

### Scientific evidence and limits

The [validation collection](../validation/index.md) now includes receptor
sensitivity, constraint contribution, native TYR cardinality and experimental
carbonyl receiving/public-generation controls. These distinguish independent
geometric expectations, alternative hypotheses, typed-record assignment,
essential sites, exclusions, unit policies, native recovery and input custody.
The carbonyl result covers one neutral aldehyde and analytical donor witnesses;
it is not broad chemical, energetic, biological or performance validation.

Positive-site radius boundaries now allow eight float64 epsilons relative to
the radius/tolerance to avoid reversing equality during unit conversion. The
allowance is recorded in criteria; physical radii and strict inside-exclusion
semantics remain distinct. Point/Sphere feature lists mean alternatives, and
one-to-one matching applies to typed feature records, which may share atoms.

The ERalpha development studies preserve original preparation failures, exposure
and evaluated-subset limits. They do not establish independent activity prediction.
Optional attribution retains actual reached method/provider evidence and reports
tracking/diagnostic failures without erasing completed scientific results.

The [cached-generation scaling case](../validation/cached_generation_scaling.md)
records fixed synthetic workloads, independent geometry/count checks and bounded
resource measurements. A subsequent fixed-work profile motivates provider-owned
PyUnitWizard/SMonitor proposals. The measurements retain their original inputs
and environments; no runtime optimization or general speed guarantee follows.

MolSysMT owns molecular representations/formats, preparation, recognition,
geometry and transformations. When the provider exposes the qualified vector
capability, donor geometry is delegated to it. The labeled historical compatibility route remains scoped
under [#41](https://github.com/uibcdf/pharmacophoremt/issues/41) /
[MolSysMT #375](https://github.com/uibcdf/molsysmt/issues/375); newer source
capabilities do not imply compatibility with every published provider version.

### Unit-policy compatibility

Importing PHMT after an application has already created a Pint quantity preserves
that registry and its cache setting. The absent suite policy is still initialized;
an existing application unit policy is retained. This removes a late cache request
and its warning without changing unit conversion arithmetic or dependency pins.

### Interchange and numerical corrections

RDKit conversion exposes explicit point/feature representation, radius and loss/
report options. Pharmer point reading preserves original enabled-point mappings
with an explicit loss policy; unsupported query constructs remain visible. See
[RDKit](../user/rdkit_interoperability.md) and [Pharmer](../user/pharmer_interoperability.md).
These projections do not claim complete pharmacophore-query equivalence.

Essential-triplet candidate pruning now retains the declared float64 roundoff
band. The rigid pair-distance association correction preserves compatible native
maps before final matching. Candidate admission does not enlarge physical radii,
replace final pose predicates or establish an index/performance default.

### Source qualification and separate package delivery

The tag requires the exact committed candidate's complete source matrix and
conformance/publication-governance checks; selected historical local/owned-wheel
passes do not substitute for them. Receive actual counts, skips and qualified
coverage identities across all three core/reader namespaces. The
[source-cut decision](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/release_0_5_0_source_cut.md)
and #95 retain the accepted source and terminal run evidence.

No 0.5.0 package delivery is claimed. Complete public dependency closure, exact
installed Linux/macOS arm64 Python 3.11–3.14 candidate gates and fresh public
installation stay #10/#23-owned. Earlier public-provider observations and
capability skips remain historical; controlled source pins do not establish a
new published provider minimum. ArgDigest >=0.17.1, SMonitor >=0.22.1 and PyYAML
>=5.1 retain their actual declared requirements. Saved reading creates no new
scientific attribution or molecular calculation.

Public native feature reconstruction/writers, generic molecular collections,
production indexing/scale, wider receptor/retrospective science and representative
human receiving remain future work. SDF ownership/fidelity, hydrogen refinement
and pockets keep their owning issues. The viewer addon, dynamics and AI are not
prerequisites for this consolidation. #148/#165 remain stopped under their
recorded resource limits.

Further pre-1.0 releases can include 0.10.0, 0.11.0 and later minors. Readiness
for 1.0.0 depends on agreed scope, contracts and evidence, not reaching 0.9.

## 0.4.0 — published 2026-10-23

See the [original release](https://github.com/uibcdf/pharmacophoremt/releases/tag/0.4.0)
and [installed/public delivery evidence](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/conda_040_delivery_20261023_summary.json).
Those immutable source/package identities and their qualification retain their
original scope; this draft does not change historical artifacts or support claims.
