# Release notes

## 0.5.0 — draft consolidation

This is a proposed release, not a published tag or package. The source review
now includes changes through commit
[`fbe6677f5a770a2123a2512fc3367a93209456ae`](https://github.com/uibcdf/pharmacophoremt/commit/fbe6677f5a770a2123a2512fc3367a93209456ae),
extending the initial `3d26b28` review. This is a reviewed source snapshot.
The exact release candidate, version plan and installed/public qualification
remain pending under [#95](https://github.com/uibcdf/pharmacophoremt/issues/95).
Use the [installation guide](installation.md) for the delivered 0.4.0 package.

### Later development after the reviewed snapshot

The independent reader now receives exact released support payloads separately
from scientific execution. SMonitor>=0.22.1 is required to preserve visible coded
errors through nested filtered/silenced observations; older0.19 can retain the
exception while losing its diagnostic event. Controlled source routes select the
same published correction. This does not qualify a new complete PHMT artifact
or the full supported installation/platform matrix.

Recoverable prepared runs and the independent `pharmacophoremt_results` reader
pass selected source controls, original-input and bounded owned installed
receiving. The
[recipe](../cookbook/recoverable_prepared_screening.md) separates new confirmed
deliveries from the authoritative complete saved view, and preserves terminal
failures, attempts and original producer evidence. Public writing uses a new
versioned format; reading an experimental legacy run is explicit and does not
migrate it. This later API delta needs its own candidate review and actual
source/installed/public gates before release.

Public `screening.PreparedInput` and `screen_prepared` now evaluate prepared
inputs incrementally and export all mapped outcomes in encounter order. The
[recipe](../cookbook/prepared_incremental_screening.md) loads a query, reads
prepared files lazily and writes fresh JSONL/CSV outputs. Readers stay under
application ownership; failures remain unscored and valid negatives retain zero.
This adds no public resume/journal or managed collection contract and leaves
`VirtualScreening.run`'s ranked hit list unchanged. Source and bounded owned-wheel
receiving pass; full supported installed/public delivery remains pending.

#105 adds the explicitly selected
`donor_aromatic_carbonyl_aromatic_n_experimental` profile: native model2 carbonyl
and model3 aromatic-N alternatives, preserving the older profiles. Its
[contract and receiving](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/public_cached_aromatic_n_generation.md)
include analytical controls and real HIS524 cache consumption. This later source
delta needs exact candidate/scope review under #95; it does not freeze0.5.0 or
qualify biological utility or public provider delivery.

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

### Remaining qualification before publication

The release must identify an exact source/closure and pass its required hosted
source and installed-candidate gates. Historical/local selected passes are not
a complete 0.5.0 release qualification. The Linux/macOS arm64 Python 3.11–3.14
installed matrix and independent public receiving remain separate under #10/#23.
Installed tests privately stage their receptor-study helpers/plans and cached
scaling inputs. Test support is not shipped as runtime code.

ArgDigest [0.17.1](https://github.com/uibcdf/argdigest/releases/tag/0.17.1) now
publishes the #47/#48 corrections. Its exact Conda file is present under main
and in the solver index. PHMT #82 now receives its verified bytes in an owned
overlay and passes 500 selected source controls. The model-source replacement
regression is repaired; the four native JSON/YAML codecs use definition-owned
signature admission. Ordinary unknown-option errors now carry ARG-ERR-CONTRACT-001
while remaining catchable as TypeError, replacing incidental Python message text.
Later public-provider receiving on immutable source `9c16365` passes its selected
controls, retaining modern-capability skips. A fresh registry/index check still
finds MolSysMT 0.23.0 as the highest numeric version under the public main label;
its historical workflows do not qualify the absent modern chemical-state/vector/
direction APIs. Resolve the supported delivery boundary and receive actual bytes
before freezing this full proposed scope. MolSysMT #255/#431 are closed source
work, separate from public delivery. The broader direction proposal #375 remains
with MolSysMT. Provider performance proposals add no candidate gate.

Molecular SDF fidelity/ownership, hydrogen refinement, pockets and broader scientific
validation keep their owning issues. This draft does not claim them repaired.
The viewer addon, dynamics and AI are outside this consolidation's required scope.

Further pre-1.0 releases can include 0.10.0, 0.11.0 and later minors. Readiness
for 1.0.0 depends on the agreed scope, contracts and evidence, not reaching 0.9.

## 0.4.0 — published 2026-10-23

See the [original release](https://github.com/uibcdf/pharmacophoremt/releases/tag/0.4.0)
and [installed/public delivery evidence](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/conda_040_delivery_20261023_summary.json).
Those immutable source/package identities and their qualification retain their
original scope; this draft does not change historical artifacts or support claims.
