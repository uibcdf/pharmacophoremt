# Release notes

## 0.5.0 — draft consolidation

This is a proposed release, not a published tag or package. The source review
compares 0.4.0 with commit
[`3d26b28ae072c106784299ee96d3a50f0edebc91`](https://github.com/uibcdf/pharmacophoremt/commit/3d26b28ae072c106784299ee96d3a50f0edebc91).
The exact release candidate, version plan and installed/public qualification
remain pending under [#95](https://github.com/uibcdf/pharmacophoremt/issues/95).
Use the [installation guide](installation.md) for the delivered 0.4.0 package.

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
  discordances. Reading saved results performs no molecular calculation. See
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
   do not bypass native scientific checks. ArgDigest 0.17.0 is the declared
   minimum; PyYAML >=5.1 is now an explicit required dependency, and the existing
   required NGLView dependency is consistently classified.

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

MolSysMT owns molecular representations/formats, preparation, recognition,
geometry and transformations. Current-source donor vectors are delegated to its
public geometry tools. The labeled historical compatibility route remains scoped
under [#41](https://github.com/uibcdf/pharmacophoremt/issues/41) /
[MolSysMT #375](https://github.com/uibcdf/molsysmt/issues/375); newer source
capabilities do not imply compatibility with every published provider version.

### Remaining qualification before publication

The release must identify an exact source/closure and pass its required hosted
source and installed-candidate gates. Historical/local selected passes are not
a complete 0.5.0 release qualification. The Linux/macOS arm64 Python 3.11–3.14
installed matrix and independent public receiving remain separate under #10/#23.
The installed-test declaration repair in #96 supplies three receptor-study
helpers and their frozen plans without shipping test support as runtime code.

ArgDigest [0.17.1](https://github.com/uibcdf/argdigest/releases/tag/0.17.1) now
publishes the #47/#48 corrections. Its exact Conda file is present under main
and in the solver index; it has not been installed or qualified by this review.
PHMT #82 still needs receiving with that artifact, including the measured
literal-kwargs model-source routing regression. Molecular
SDF fidelity/ownership, hydrogen refinement, pockets and broader scientific
validation keep their owning issues. This draft does not claim them repaired.
The viewer addon, dynamics and AI are outside this consolidation's required scope.

Further pre-1.0 releases can include 0.10.0, 0.11.0 and later minors. Readiness
for 1.0.0 depends on the agreed scope, contracts and evidence, not reaching 0.9.

## 0.4.0 — published 2026-10-23

See the [original release](https://github.com/uibcdf/pharmacophoremt/releases/tag/0.4.0)
and [installed/public delivery evidence](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/conda_040_delivery_20261023_summary.json).
Those immutable source/package identities and their qualification retain their
original scope; this draft does not change historical artifacts or support claims.
