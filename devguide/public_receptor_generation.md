# Public cached receptor hypothesis generation

Owner LMMV/dprada, [#87](https://github.com/uibcdf/pharmacophoremt/issues/87),
2026-11-05. `modeler.from_receptor_features` generalizes #86's admitted
donor/aromatic hypothesis policy. Molecular loading, formats, selection,
recognition, geometry and preparation remain MolSysMT responsibilities.

## Required choices and outputs

Provide a native chemical `get_features` inventory and explicitly choose
`receptor_profile='donor_aromatic_faces'`, nonempty lists/tuples of positive
scalar-length `donor_distances` and `aromatic_distances`, positive length `radius`
and finite nonnegative integer `max_hypotheses`. No physical parameter defaults
or automatic chemical profile selection are supplied. Both distance lists are
required even if a source family is absent. Each quantity has an explicit unit;
reported parameters/choices retain QuantityRecord manifests.

For every indexed donor record, choose one offset along its cached D→H direction
and emit a spherical ligand acceptor. For every aromatic record, choose an offset
and one face; emit a Disk with the cached axis declared as the parallel target
axis. An admitted record occurs exactly once in every joint hypothesis. Indexed
donor-H pairs retain separate identity even when a heavy atom is shared. All
sites start essential and weight one as construction assumptions.

Records retain inventory order. Distances retain caller order; ring choices are
distance-major then +1/−1 face. The rightmost feature changes fastest. Opposite
faces are separate models. Repeated equivalent caller choices remain separate
declared alternatives; there is no approximate deduplication or ranking. Axis
sign is a provider convention and can exchange face labels.

The lazy Cartesian product has an exact total; at most the explicit budget is
materialized. The result contains `method`, `models`, `report` and `complete`.
The report records parameters, source inventory, per-hypothesis choices and
`enumeration` with total/visited/returned/remaining, budget, completion and order.
An eligible zero-budget call is incomplete with no models. A cache without any
admitted record has status `no_supported_features`, total zero and complete=True;
it does not produce a positive empty query or establish inactivity.

Unsupported records are retained in `omitted` with indices, source atoms, kind
and reason. This first profile excludes position-only acceptors, charges,
hydrophobicity. Included volumes require a separate inventory and are refused
before construction, even with budget zero. Missing/invalid admitted directions or
axes raise before any model, including with budget zero. Empty or unsupported
cache results are distinct from invalid scientific inputs and failed operations.

## Ownership, validation and provenance

The tool composes existing `from_receptor_projections`; it never accesses a
molecular system or reconstructs a molecular vector, plane, chemical state,
format or pocket. Source/frame/state and origin evidence remain caller claims;
cached equality does not authenticate an unchanged molecular system. Native
quantities are required. Saved QuantityRecord metadata preserve evidence but
are not automatically rehydrated into a native inventory.

The explicit-projection constructor also declares the standard optional boolean
`skip_digestion` control; its scientific checks and existing facade behavior remain.
The new builder is a direct tool. Each model records its generation method,
underlying projection method, choices/parameters, omissions and the enumeration
that produced it. Reports/models/source data have independent mutable metadata.
JSON/YAML preserve full provenance and physical geometry; ordinary float64 unit
roundoff is assessed at the predeclared 1e-12 nm/unit tolerance.

ArgDigest owns signature admission and argument normalization through a
definition-owned contract. Scientific cache/profile/quantity/budget checks also
apply with explicit digestion bypass. SMonitor supplies the existing PHMT-E102
ArgumentError diagnostics. PyUnitWizard validates dimensions and encodes units.
No new optional backend/dependency exists, so no additional DepDigest availability
route is applicable. Optional Ackredit captures reached PHMT/NumPy/unit operations
and model results; cached provider credit is retained without rerunning or
crediting new molecular recognition. Provider absence/failure cannot erase science.

## Scientific qualification and remaining limits

Acceptance uses independent typed synthetic inventories and frozen prepared
PHE404 coordinates, multisite products, source/choice mapping, physical unit
agreement, blocked molecular access, invalid/unsupported/empty/budget outcomes,
bounded large products, metadata independence, native recovery and real optional
attribution. Historical #86 code, declarations and original evidence stay unchanged.

The profile is a geometric pharmacophoric hypothesis, without steric accessibility,
energetic preference, optimal distances, chemical realizability, affinity or
biological validation. No fitting, molecular pose search, TopoMT dependency or
automatic pocket occurs. Further acceptor chemistry needs its own MolSysMT #375
admission/receiving; environmental H refinement remains #323. Broader #6/#82,
#66, #74/#215 and installed/public/platform/hosted gates remain separate. ArgDigest
#47/#48 are fixed in source; public 0.17.0 and their consumer delivery gate remain
unchanged. This work does not raise a provider floor or adopt a source workaround.

## Optional cached exclusions — 2026-11-05

[#88](https://github.com/uibcdf/pharmacophoremt/issues/88) extends the signature
with paired `excluded_volume_inventory` and `excluded_volume_radius`, using the
existing separate heavy-atom input domain. The [contract](receptor_generation_exclusions.md)
defines declared context matching, mandatory validation even at zero budget,
independent per-model attachment, actual global indices and local root recipes.
The weight-one assumption above concerns positive sites; appended exclusions have
weight zero. The original positive method ID and enumeration remain unchanged.
No molecular operation, physical-radius assignment or generation pruning occurs.
[Original evidence](evidence/receptor_generation_exclusions_20261105_summary.json)
records 217 passing selected controls (61 new), boundary/prepared independent
oracles and the final source identities; #87's original evidence remains intact.

## Experimental cached carbonyl profile — 2026-11-05

[#94](https://github.com/uibcdf/pharmacophoremt/issues/94) adds the explicitly
selected `donor_aromatic_carbonyl_experimental` source profile. Its
[contract](public_cached_carbonyl_generation.md) requires a separate native provider
cache, structure position, acceptor distance choices and target donor orientation.
Original donor/aromatic behavior and default position-only features remain.
Only provider carbonyl model2/status1 is admitted; alternatives stay separate,
unsupported/undefined/known outside-profile omissions retain reasons, and source
consistency checks do not authenticate molecular coordinates. General molecular
operations remain in MolSysMT; installed/public delivery stays separate.
