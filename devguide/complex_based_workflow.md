# Complex modeler: explicit prepared native observations

The #42 transition retains `ComplexBasedModeler`, the `complex-based` method
name and its single-/multiple-frame return shape. It replaces the scientific
contract of the former RDKit inference/detection engine. Original runtime and
#5 assertions remain in commit `1198af1c410621deb1477a4fc8b8f5ea3c46b376`;
the [dated #5 archive](archive/complex_pdb_feature_recovery.md) preserves its
measured history. No scientific equivalence with the retired heuristics is claimed.

## Ownership and input contract

Supply the same unchanged prepared molecular system used to calculate a
nonempty **named mapping of native `molsysmt.Interactions`** and an explicit
`ligand_selection`. Molecular I/O, selection, preparation, chemical state,
recognition and geometry belong to MolSysMT. Detection is an explicit prior
provider operation; the observations themselves define the partner boundary.
The facade performs no ligand inference, hydrogen addition, bond-order recovery,
implicit receptor selection, detection or molecular conversion/unwrapping.

`ComplexBasedModeler(source, ligand_selection=ligand,
interaction_collection=analyses)` delegates each requested frame to the existing
public `from_interaction_collection()`. `phmt.model()` still defaults to
`method='complex-based'`, but requires those same explicit inputs. There is no
fallback when inputs are missing or native evidence fails. `skip_digestion=True`
does not bypass the required ligand/collection/boundary checks.

The underlying [interaction composition contract](interaction_composition_workflow.md)
governs source axes/maps/identity, evaluated frames, chemical states, native
profiles, participant completeness and periodic-image limits. It accepts the
supported hydrophobic, H-bond, ionic, pi-pi and cation-pi observations and preserves
their original evidence. Unsupported types fail rather than receiving a local
detector. The caller must ensure that the source has not changed since detection;
the facade does not manufacture proof of historical source identity.

## Parameters and return

Constructor options are `radius`, `name`, `cation_mapping` and `duplicate_policy`,
passed unchanged to the public adapter. The radius is a query matching tolerance,
not a detection cutoff. `duplicate_policy='same_participant'` reuses compatible
constraints for the same declared participant without increasing weight;
`'keep'` retains them separately. It does not spatially merge different atoms.

`build()` selects frame zero. An integer or one-element sequence returns one
`Pharmacophore`; multiple unique nonnegative indices return a list in the supplied
order. The high-level dispatcher accepts `structure_indices` for the build step.
Declare evaluated local indices explicitly; `'all'`, duplicates, booleans, empty
sequences and negative/fractional indices are refused. All analyses must have
evaluated each requested frame. `result` is initially `None`, stores a successful
return, and is cleared before each build, including a failed rebuild. A later
frame failure raises without publishing the earlier models as a partial result.

Evaluated-empty families retain their labels and native evidence. If every
supplied analysis was evaluated and contains no interactions, the nonempty named
mapping produces a zero-site model, not a failed calculation or a meaningful
positive-weight screening query. An empty/missing mapping, failed conversion, mismatched
state/maps/profile or uncovered frames raise. Original method/profile criteria,
source context, preparation provenance and optional attribution remain in the
model/component/site metadata. Saved readers do not rerun detection or register
new scientific usage. The facade does not open an Ackredit session; applications
choose whether to capture attribution.

## Breaking migration

Old calls with only a PDB/path/system and selections now fail. Prepare through
public MolSysMT tools, choose detection methods/profiles/cutoffs there, retain
the native analyses and pass the same source to the modeler. Do not translate
old `RULES`, mutable `params` or threshold keywords into an allegedly equivalent
native model. `receptor_selection` is refused; calculate the intended provider
selection before construction. The [executable recipe](../docs/content/cookbook/complex_based_modeler.md)
shows all three public entry points. The prepared ERα interface recipe documents
a separate biological fragment with explicitly chosen chemical states.

## Guards and qualification limits

`tests/test_complex_based_facade.py` exercises actual native observations through
the class, named method and default dispatcher; independent nine-site expectations,
reuse/weight/radius, refusal before molecular operations, evaluated-empty versus
uncovered frames, ordered multiple frames, clearing failed results, persistence
and actual optional citation capture. `tests/test_eralpha_interface.py` reuses
the declared prepared 304–550/EST fragment: six hydrophobic sites, retained empty
H-bond/pi-pi families and unchanged coordinates, native histories and analyses.
Its existing frozen participant/distance oracle independently validates contacts.

This transition does not qualify full-receptor preparation or biological affinity.
MolSysMT #323 environmental H geometry, #350 rejected-pair diagnostics and #367
arbitrary-fit validation remain separate. Structure-based modeling, legacy
screening and molecular utilities remain in the broader partial #41 retirement.

## Executed transition evidence — 2026-10-10

The corrected normal editable Python 3.14.7 tree passes **712 tests** in 1336.82 s,
including all 31 facade controls and the prepared-fragment continuation. The
three recipe blocks execute, Ruff and strict isolated recipe/navigation rendering
pass, and twenty historical evidence archives remain unchanged. The
[final review summary](evidence/complex_based_facade_review_py314_summary.json)
links original full output, JUnit, scientific source/fixture hashes, binary
identities and saved analytical models. Scientific inputs and provider source
are unchanged; its conservative repository-status flag records added diagnostic
artifacts separately and is explicitly qualified. Initial wrong-fixture failure
history remains inspectable and excluded from acceptance. Twelve warnings retain
their declared origins, including the still-reachable legacy screening unit strip.
This local run does not qualify other interpreter/platform matrix cells or the
remaining #41 routes; their actual state belongs on the owning issues.

**2026-10-10 follow-up (#45):** Structure and screening have since transitioned
to explicit prepared-native contracts. The warning/caller state in the executed
#42 record above remains historical; #45 removes the legacy screening unit-strip
path and requires explicit validation tools. Remaining #41 scope is unused
generic utilities/library ingestion and donor geometry delegation (#375).
