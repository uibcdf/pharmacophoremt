# Native ionic observation workflow

Owning issue: [PharmacophoreMT #33](https://github.com/uibcdf/pharmacophoremt/issues/33).
The public `modeler.from_interactions()` tool now consumes MolSysMT
`ionic_contact` observations alongside hydrophobic/H-bond observations.
This extends the native traditional complex-based route with charge sites.

## Ownership and reusable composition

MolSysMT owns chemical-state recognition, complete charge-center membership,
minimum-distance contact detection, coordinates, source selections and molecular
transformations. `get_features()` already owns the shared pharmacophoric feature
inventory and calls public MolSysMT charge recognition and `structure.get_center`.
The extended consumer calls that tool; no local charge recognizer, centroid
kernel or ionic detector is introduced.

`from_interactions()` owns observation-to-hypothesis interpretation, repetition
aggregation and Feature + Shape construction. `PoseEvaluator` reuses the same
inventory definition for candidate recognition; its assignment code is unchanged.
The independently public exclusion builder and native query persistence compose
with the resulting model without an ionic-specific screening implementation.
The new private helpers validate the consumer's bounded input contract; they are
not independent scientific tools or an extension registration API.

## Bounded contract

- Same unchanged molecular source, local atom/frame axes and evaluated frame as
  the supplied native `Interactions`. Axis lengths cannot authenticate origin.
- `participant_definition='formal_charge'`,
  `recognition_rule_version='formal_charge_centers@1'`,
  `charge_source='chemical_states.formal_charge'`, and an explicit nonnegative
  integer `chemical_state_index`. Selection and recognition use that state.
- Exactly two nonempty disjoint participants with roles `positive` and `negative`.
  Only whole participants crossing the ligand boundary contribute. A selection
  cutting a compound center raises; it cannot turn a subgroup into a new feature.
- The ligand participant must match current provider recognition in that state;
  its recorded elementary-charge measurement must agree. This validation does not
  authenticate historical coordinates or all partner chemistry.
- Positive or negative charge sphere, essential with weight one, at the uniform
  centroid of the provider's geometry members. The caller supplies a positive
  scalar matching radius, independent of the contact detection threshold.
- Aggregate repeated occurrences of a ligand center into one site; retain all
  selected occurrence/relation indices, participants, evidence and measurements.
- Nonzero periodic images raise; no imaging, charge inference, preparation,
  protonation, energy estimation or coordinate generation occurs. Unsupported
  interaction families still raise when selected. Zero-image observations retain
  their original periodic criteria; they do not establish a prepared whole system.
- An evaluated frame with no qualifying contacts yields an empty model and retains
  coverage/criteria. That model is invalid for `PoseEvaluator`.

The shared bounded provider definition includes carboxylate/guanidinium and literal
formal-charge atoms/clusters. It does not establish universal charge delocalization
or an experimentally populated protonation state. Compound membership and geometry
membership are separate: carboxylate includes C/O/O but its center uses O/O;
guanidinium's recorded group geometry uses the provider's nitrogen members.

## Evidence and persistence

Model metadata retains the full observation parameters, actual producer versions,
source atom/structure maps, coverage and execution records. `ionic_feature_inventory`
retains detached recognition and geometry evidence from the shared tool. Charge
site metadata adds geometry atom indices and their source mapping, elementary
charge, state, recognition rule and uniform-centroid method.
Measurements and all quantity metadata use PyUnitWizard QuantityRecord interchange.
The public native query writer/reader preserve this evidence and pose behavior.
No output claims a source fingerprint verification merely because maps align.

## Actual attribution

The existing deferred Ackredit client captures the actual constructor and shared
feature tool in the application's session. Cached observation criteria and
bibliography retain their original records; construction does not rerun or credit
another ionic detector. An enclosing capture observes a detector when the workflow
actually invokes it. Imported/read results do not claim another calculation.

The current native MolSysMT minimum-distance criterion declares executed MolSysMT
software without a named method article. This mapping adopts no new paper-specific
algorithm; do not invent a ProLIF, salt-bridge or G3PS attribution for it.
Actual NumPy/PyUnitWizard/PharmacophoreMT software is credited on successful
construction. Pose evaluation additionally reaches its assignment references.
All original observation metadata remains even when optional host tracking is off.
Absence or diagnosed tracking failure preserves the scientific result.

## Analytical acceptance controls

`tests/test_ionic_interactions.py` covers Na/Cl in both ligand roles, compound
carboxylate with two contacts aggregated at the independently specified oxygen
centroid, and guanidinium at its independently specified nitrogen centroid.
Negatives include displacement, unchanged-geometry neutralization and opposite
sign. Additional guards cover cut centers, incompatible definitions/states,
stale membership/charge, actual public geometry-tool reuse without rerunning the
ionic detector, source mappings, detached persistence, empty/internal/uncovered
observations, nonzero images and rotated geometry under pm/fs/degrees policy.

The exclusion composition guard holds the positive charge match at fit one while
two explicit heavy-atom overlaps veto the candidate. Original geometry remains
unchanged. Real Ackredit guards cover repeated/empty results in an enclosing
session, cached origin, absence/failure, genuine fresh-process absence and a fresh
detached bibliography reader excluding molecular scientific engines.

The reproducible driver `python -m devtools.validate_ionic_interactions --output FILE`
executes atomic/carboxylate/guanidinium cases with both selections, reference,
displaced and persisted-query controls, and host tracking off/on. It retains
complete query, observation, pose and capture reports with input geometry,
producer source identities and loaded molecular extension identities. It checks
science equality after removing attribution and does not measure timing/memory.
The [cookbook](../docs/content/cookbook/ionic_interactions.md) exposes construction,
actual citation capture/persistence and independent exclusion composition.

These are prepared analytical controls. They do not resolve MolSysMT receptor
preparation #298, qualify a biological pilot, prove binding energies, or establish
wheel/hosted-matrix/public provider compatibility. Aromatic interaction families
remain a subsequent classical extension.

## Local verification — 2026-10-03

All 24 ionic guards pass within the expanded 77-test set (46.14 s). The complete
suite passes 402 tests in 401.75 s on Python 3.14.7, with the same eight expected/
known warnings. Three cookbook blocks execute under 3.14; strict isolated Sphinx
rendering uses existing 3.13 documentation tools. Ruff and offline reporting/
index/whitespace checks pass. The library remains installed editable in
`molsyssuite@uibcdf_3.14`, without a PYTHONPATH source override.

The tenth [original evidence archive](evidence/README.md#prepared-analytical-ionic-workflows-on-python-314)
retains both actual driver profiles, source identities and captures. It reports
six selected queries/18 pose controls per profile, identical tracking-independent
science and nine items/18 uses when host tracking is enabled. All ten original
archives verify. Review, immutable providers, hosted-matrix and distribution
qualification remain separate from this local evidence.
