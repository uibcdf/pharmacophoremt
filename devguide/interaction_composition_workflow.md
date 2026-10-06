# Common-frame hypothesis composition

Owned by [#36](https://github.com/uibcdf/pharmacophoremt/issues/36).
`compose_pharmacophores()` combines named cached hypotheses without molecular
access. `from_interaction_collection()` converts named native MolSysMT analyses
using public `from_interactions()` and calls the standalone composition tool.

## Standalone composition

`compose_pharmacophores(pharmacophores, duplicate_policy='keep', name=None)`
accepts a nonempty named mapping in insertion order. Inputs declare a common
coordinate frame; conflicting known reference-frame indices raise. No molecular
access, recognition, alignment or transformation occurs. Output sites and metadata
are independent copies. Input names, descriptions, scores and reference fields
remain component evidence; the output score is not computed from them.

`keep` preserves every constraint and supports generic Feature + Shape models,
including independently built exclusions. Essential one-to-one assignment remains
authoritative; one candidate participant cannot satisfy duplicate essential sites.

`same_participant` is an explicit bounded alternative for native
`observed_interactions` models. All components must declare matching source ID,
atom/structure maps, ligand selection, frame and explicit integer state. Site
source correspondence must agree with the maps. Source declarations cannot
authenticate molecular origin. Identity is the feature plus whole atom membership,
never center proximity. Distinct coincident participants remain distinct.

Compatible duplicates retain one shape, flag and weight. Shape kind, geometry
members, original charge, center, radius and orientation must agree. Weights and
essential flags agree exactly. Absolute representation tolerance is 1e-12 nm/
dimensionless with zero relative tolerance; it is not a spatial clustering radius.
Orientation vectors are normalized for comparison. Disk normal reversal is
equivalent; donor direction reversal is not. Conflicts raise instead of selecting
the first, averaging geometry, adding weight or weakening the constraint. The
`keep` alternative remains available for intentional independent hypotheses.

`metadata.components` retains detached input snapshots; `metadata.site_map`
maps each component's local site index to the output index with `added`/`reused`.
Each site's `composition_contributions` retains original site metadata. Native
observations additionally carry component labels: relation/occurrence indices
remain local to that analysis. Nested generic composition preserves prior snapshots.
Empty components remain visible; all-empty output remains an invalid evaluation query.

## Named native collection

`from_interaction_collection(source, collection, ligand_selection, ...)` checks
common native source axes/maps and one explicitly declared state, calls public
`from_interactions()` for each named result and the public composer with
`same_participant` by default. `keep` is explicit. The dispatcher exposes
`method='interaction-collection'`, `interaction_collection` and `ligand_selection`.

Radius and cation mapping are common explicit conversion choices. For individually
edited flags, weights or radii, construct component models and use the standalone
composer. Per-analysis profiles, criteria, units, producer versions, execution
records and original bibliography remain in their component records. No heterogeneous
result is flattened into an invented detector. Any future general native result
combination belongs in MolSysMT.

Atomic H-bond/hydrophobic conversion currently uses the source reference state;
the collection requires these analyses to declare it. Ionic/aromatic adapters keep
their explicit state contracts. Covered-empty results remain zero-site components.
Uncovered frames or any failed child conversion raise without a partial hypothesis
or zero fit. Completed child credits can remain in an application capture; they
do not prove successful overall construction.

## Attribution, quantities and ownership

Application-owned Ackredit captures record actual detector work when detection
runs inside them. Cached composition preserves original bibliographies without
claiming another detection, recognition or fit. The collection's public conversion
children may recognize molecular features through MolSysMT. Provider absence or
failure preserves completed science with host diagnostics and detached producer
context. Saved readers add no scientific credit. Composition has no borrowed paper;
provider references and the evaluator's assignment criterion are credited when
reached. No new external engine, hooks, enrichment or installer route is introduced.

Native JSON keeps the fixed-unit shape protocol and sealed quantity metadata,
including undefined original aromatic measures. A pm/fs/degrees regression builds,
persists and evaluates the joint model, and composes stored components without the
original molecular object. Generic composition performs no molecular operations.
Molecular preparation and recognition implementations remain provider-owned.

## Analytical validation

`devtools.interaction_collection_cases` declares disconnected prepared benzene,
sodium, indexed donor and neutral carbon controls plus partner components. This
selection is not a chemical ligand or biological binding complex. Public MolSysMT
independently detects five families, an alternative pi-pi profile and a covered-empty
ionic analysis: seven named analyses, 23 observations, 11 constraints before reuse
and nine unit-weight sites after charge/ring reuse.

The product guard `tests/test_interaction_composition.py` has 32 controls covering
both policies, public-tool consumption, no molecular access during cached composition,
detached ownership, constraint/source/state incompatibilities, empty/uncovered cases,
independent geometry/veto controls, non-default units, persistence, actual optional
attribution, lazy imports and genuine absence. The dispatcher and method-contract
gate passes 16 controls in 7.57 s on Python 3.14.7; final full integration is recorded
below after execution.

`python -m devtools.validate_interaction_composition --output composition.json`
passes tracking off/on with nine pose evaluations each. Reference, round-trip and
modular reuse fit one. Displacement fits zero; donor-H reversal fits 8/9 with an
essential failure. Keeping 11 constraints fits 9/11 with two missing essentials.
At a controlled cation collision, broad positives still fit one; an independent
exclusion produces a veto with that positive fit unchanged. Producer sources,
declared atom identity/state/coordinates and persisted metadata remain unchanged.
These are policy semantics, not a ranking of equivalent strategies.

The [cookbook](../docs/content/cookbook/interaction_composition.md) has three executed
blocks on Python 3.14.7. Biological accuracy, affinity, receptor preparation,
runtime/memory, universal fused-ring mapping and public distribution qualification
remain outside these controls. Review and incorporation remain open.

The twelfth original evidence artifact and compact summary are retained in
`devguide/evidence/interaction_composition_py314.*`, with file identities and scope
in the [evidence index](evidence/README.md). Tracking off/on captures contain
5 items/21 uses and 13 items/50 uses respectively, including actual provider
detector references. The scientific projections are identical. Strict isolated
cookbook rendering passes with existing Python 3.13 documentation tooling.

The corrected complete local tree passes **476 tests in 452.91 s** on Python
3.14.7, including all 32 composition controls. The same eight known warnings
remain: six structural B-factor drop controls, one optional tracking-failure
control and one legacy unit warning. The editable installation in
`molsyssuite@uibcdf_3.14` is confirmed without a PYTHONPATH override. Ruff,
reporting indexes, three offline reporting tests, whitespace checks and all
twelve original archive hashes pass. This is local source evidence, not a
published-wheel or hosted-matrix qualification.
