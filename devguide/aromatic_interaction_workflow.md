# Native aromatic observation workflows

Owned by [#34](https://github.com/uibcdf/pharmacophoremt/issues/34).
`from_interactions()` converts native MolSysMT `pi_pi` and `cation_pi`
observations into independently evaluable hypotheses. MolSysMT owns molecular
selection, recognition, charge membership, ring geometry and detection;
PharmacophoreMT calls public `get_features()` and `from_feature_inventory()`
for the shared Feature + Shape contract. Aromatic sites are essential disks;
positive centers are essential spheres. Both have unit weight by default.

## Observation profiles and query geometry

| Family | Native method | Native profile | Observation plane definition |
| --- | --- | --- | --- |
| pi_pi | centroid_angle_offset | least_squares | Unweighted orthogonal least squares |
| pi_pi | centroid_angle_offset | three_atom_plane | First three ring-basis atoms |
| pi_pi | plane_angle_intersection | aromatic_cycles | Centroid and first two ring-basis atoms |
| pi_pi | plane_angle_intersection | smarts_5_6 | Centroid and first two SMARTS ring atoms |
| cation_pi | centroid_angle_offset | least_squares | Unweighted orthogonal least squares |
| cation_pi | centroid_distance_offset | three_atom_plane | First three ring-basis atoms |
| cation_pi | centroid_distance_angle | smarts_5_6 | Centroid and first two SMARTS ring atoms |

The least-squares profiles are explicit-cutoff MolSysMT proposals. The other
profiles declare reference criteria from Mol*, MDTraj and ProLIF respectively.
The consumed canonical method/profile identifiers, plane definitions and source
references are those in the provider's native observations. Moving primary
documentation provides context: [ProLIF implementation](https://prolif.readthedocs.io/en/stable/_modules/prolif/interactions/interactions.html),
[Mol* interactions](https://molstar.org/docs/extensions/interactions/).
Provider-recorded pinned references remain the evidence contract; reading these
documentation pages does not independently verify the pinned source bytes.

Conversion uses the shared classical inventory geometry, recorded as
`shared_classical_geometry@1`: its aromatic plane is a least-squares disk and
its compound cation point is the provider-defined charge geometry centroid.
That point can differ from a detector's all-participant centroid. Detection
measurements, parameters and reference versions remain unchanged in provenance;
the query radius and direction tolerance are separate matching criteria.
The implementation never silently substitutes one detector for another.

## Participant mapping and prepared source contract

Use the same unchanged molecular source, state, atom axes and frame as the
observations. The existing adapter rejects uncovered frames, ambiguous mixed
states, partial selections and nonzero periodic images. Each selected relation
must have exactly one complete ligand-side participant. Ring membership always
requires exact correspondence with the shared aromatic inventory. Fused-ring
bases with different membership are not assumed equivalent.

`cation_mapping='exact'` is the default. Some ProLIF 2.2.2 SMARTS observations
represent a guanidinium cation using individual nitrogens, including resonance
atoms with zero formal charge. They do not exactly match the shared compound
positive center. The explicit alternative
`cation_mapping='containing_center'` permits only a singleton cation from that
declared profile to map to one uniquely containing shared positive center.
It does not relax ring membership or other profiles' compound contracts.

Conversion validates an exact cation's measured charge against the shared net
charge. For a containing-center mapping it validates the original singleton's
charge through public MolSysMT access, preserving zero-charge resonance
observations alongside the positive compound center. Repeated contacts become
one site with all original observations. Each has `participant_mapping` with
the original atoms, ligand role and chosen mapping policy. A rejected conversion
is a failed calculation with no fit value, not a geometric negative.

Model metadata retains `aromatic_feature_inventory` and
`aromatic_conversion_policy`. Site metadata retains source indices, geometry
members, state and original native observation measurements. The shared feature
inventory is reused once per construction; native detection is not rerun.

## Undefined measures and persistence

Parallel planes can have an undefined native `intersection_distance` represented
as NaN. The fix owned by [#35](https://github.com/uibcdf/pharmacophoremt/issues/35)
uses the supported PyUnitWizard sealed quantity record with base64 encoding for
nonfinite observation quantities. Finite quantities retain the existing JSON
encoding. Values, units and signs survive persistence without inventing a zero.
This changes provenance encoding only; molecular coordinates, site centers,
radii and normals must still be finite. The driver labels its detached native
quantity-column evidence explicitly; it is not an `Interactions.from_dict()`
input dictionary.

### Persistence review — 2026-10-09

The bounded consumer correction in #35 is reviewed and accepted. The existing
runtime implementation was published in `fdb57dcbe8e4d9d8364d1dcf5199a7945bfd9a2f`;
this review strengthens persistence guards without changing detection or provider
code. Four real parallel native profiles now exercise both public JSON and YAML
writers under pm/fs/degrees and readers under angstrom/ps/radians. They decode
the measurement from the saved model, preserve the undefined distance where
present, independently check the 0.02 nm radius and retain original source maps.
Source immutability is compared under the same conversion context, so ordinary
unit-conversion rounding cannot masquerade as molecular mutation.

The sealed-record guard preserves NaN, both infinity signs and negative zero,
retains the finite JSON representation and independently checks 1/2 angstrom as
0.1/0.2 nm. Nonfinite source coordinates still raise. The selected aromatic,
contract and pose-evaluation tests pass **73 tests in 35.25 s** on editable
Python 3.14.7. The existing driver passes both tracking settings with 14
case/profile combinations and both ligand roles per setting; its original full
output is retained as a distinct dated archive. All three cookbook blocks and
strict isolated rendering pass. Seven Python producer source snapshots remain
unchanged during execution, and all seventeen earlier gzip archives keep their
original bytes.

The [review receipt](evidence/nonfinite_provenance_review_py314_summary.json)
records source identities, loaded molecular extension hashes, archive checksums
and scope. The [resolved report](archive/nonfinite_observation_provenance.md)
preserves the earlier execution claims. This accepts the quantity-persistence
correction only; #34 workflow review and hosted/public-package qualification
remain separate.

## Scientific attribution

Detect inside an application-owned Ackredit session/capture to retain actual
provider credits. ProLIF, Mol* and MDTraj method references use their declared
DOIs: `10.1186/s13321-021-00548-6`, `10.1093/nar/gkab314` and
`10.1016/j.bpj.2015.08.015`. These are reference implementations; they are not
claimed as executed packages. The custom MolSysMT proposal has no borrowed
paper. Cached construction preserves the original observation bibliography
without recording another detection. Optional tracking failure/absence cannot
change scientific results, and JSON loading performs no new scientific work.

## Validation scope

`tests/test_aromatic_interactions.py` exercises both ligand roles, seven native
profiles, independent plane/displacement negatives, normal sign invariance,
compound/atomic cations, ambiguous memberships, stale observed charges, shared
public-tool reuse, unit/frame mappings, undefined measures, persistence and
real Ackredit capture/absence/failure. The focused integration run passed
97 tests on Python 3.14.7 in 59.37 s with two known attribution/legacy-unit
warnings. This does not establish a profile ranking.

`python -m devtools.validate_aromatic_interactions --output aromatic.json`
compares parallel/edge benzene pairs and atomic/compound cation controls across
14 case/profile combinations, both ligand roles, tracking on/off and JSON round
trips. The source fingerprint covers the declared atom identity, chemical state
and coordinates; these isolated inputs have no receptor chain domain. Retained
evidence must record versions, source hashes, measurement units and failed strict
mapping separately. These are prepared analytical controls, not binding-energy,
biological, universal fused-ring or performance benchmarks. Receptor preparation
for the deposited ERalpha complex remains provider-owned (MolSysMT #298).

The executed driver passes both tracking profiles: 28 queries and 84 evaluations
per profile, all self/round-trip positives at fit one and displaced negatives at
zero. Each profile retains the one expected exact compound-cation conversion
failure separately. Tracking off/on preserves science, declared source domains
and producer sources; actual captures contain 6 items/11 uses and 14 items/30
uses. The full original report and compact summary are retained in
`devguide/evidence/aromatic_interactions_py314.*`; hashes and limits are recorded
in the [evidence index](evidence/README.md). All eleven original archives verify.
The three cookbook blocks execute on Python 3.14.7 and strict isolated rendering
passes with existing Python 3.13 documentation tooling.

The complete local suite passes **444 tests in 436.36 s** on Python 3.14.7 in
the editable `molsyssuite@uibcdf_3.14` environment without a PYTHONPATH override.
The eight known warnings are six deliberate structural B-factor drops, one
optional-attribution failure control and one legacy stripped-unit warning.
Ruff, generated reporting indexes, three offline reporting tests and whitespace
checks pass. Review, full-site and published-dependency qualification remain open.
