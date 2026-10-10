# Explicit native ligand-based modeler

Reviewed transition: 2026-10-07, owned by
[#18](https://github.com/uibcdf/pharmacophoremt/issues/18).
`LigandBasedModeler` is now a consumer of the existing public native tools.
The audited recursive distance-partitioning builder is retired. Its original
counterexamples remain executable through `devtools/audit_legacy_cliques.py`.

## Method and input contract

Every constructor call must explicitly select `consensus_method`:

| Choice | Public tool | Scientific scope |
| --- | --- | --- |
| `aligned_cliques` | `from_aligned_ligand_cliques()` | Prepared ligands in a caller-declared common frame; maximal compatible site cliques and jointly supported feasible packages |
| `rigid` | `from_rigid_ligands()` | Prepared rigid frames, explicit pivot, proposed injective correspondences, public MolSysMT proper fitting and verified placement alternatives |

Neither choice is numerical compatibility with the retired algorithm, a
published RDP implementation, an affinity ranking or unrestricted conformer
discovery. See the [aligned contract](aligned_clique_consensus_workflow.md),
[rigid contract](rigid_consensus_workflow.md) and
[refinement contract](rigid_refinement_workflow.md) for correspondence,
orientation and finite search-family definitions.

Inputs are an iterable of at least two prepared systems, or an iterable of
records throughout. Raw systems get positional IDs `ligand-0`, `ligand-1`, ...,
frame zero, all atoms and the reference chemical state. Records require unique
nonempty `ligand_id` and `molecular_system`; optional fields are `selection`,
`structure_index` and `chemical_state`. MolSysMT resolves selections and states.
The collection is materialized once, including generators. A repeated raw object
is refused; record IDs are explicit declarations, not chemical deduplication.
Different conformers or copies of one compound must not inflate distinct-ligand
support. The caller owns dataset/chemical identity across distinct objects/IDs.

Each record supplies one prepared frame. There is no hidden sanitization,
hydrogen addition, state enumeration, conformer generation or alignment in the
aligned method. Source readiness, recognition and fitting failures propagate.
Molecular operations stay in MolSysMT; generic clique enumeration stays in
NetworkX; PHMT's existing reusable tools own pharmacophoric compatibility,
support, hypotheses and Feature + Shape construction.

## Constructor migration

The class name, historical positional arguments and `build()` list return stay.
Their scientific meanings follow the explicitly selected native tool:

| Historical argument | Native meaning |
| --- | --- |
| `n_points=3` | `min_sites`: minimum jointly supported sites, not exact-size subsets; a returned model can have more sites |
| `min_actives=None` | `min_support`: joint distinct-ligand count, default all inputs; feature-empty ligands remain in the denominator |
| `n_conformers=50` | Inert historical default; any other value is refused |
| `conformer_rmsd_threshold=0.5` | Inert historical default; any other value is refused |

Prepare requested conformers separately through a provider-supported operation.
Accepted inert defaults do not imply generated coordinates. Method-specific
options are forwarded to the selected tool, including feature families,
explicit units, strategies, tolerances, radii and search budgets. Unsupported
options are refused; `min_sites`/`min_support` cannot override the historical
names. Consumers preferring native argument names can call the public tools
directly. `skip_digestion=True` cannot enable the retired route or bypass these
transition guards.

`phmt.model(ligands, method='ligand-based', consensus_method='rigid', ...)`
routes the collection before single-system conversion/unwrapping. Global
`ligand_selection`/`receptor_selection` are refused; use each record's selection.
No other dispatch method is migrated by this change.

## Results, limits and attribution

`build()` returns the native `models` list in deterministic hypothesis order.
No legacy distance-RMSD score or dummy empty model is assigned. Model `score`
is unset; hypothesis order is not affinity order. Inspect support, placements,
criteria and native completion evidence before selecting a hypothesis.

After success, `modeler.result` retains the complete native dictionary and
`modeler.report` is its report. Both start as `None` and are cleared before
every build, including failed rebuilds. Completed empty analysis returns `[]`
with native `complete=True`; provider failure or resource exhaustion raises
without a successful/negative result. Native budgets bound their declared
stages and do not promise a total execution time or memory ceiling.

The facade neither opens an attribution session nor credits the retired method.
The delegated native calculation contributes to the application's optional
Ackredit session and retains original detached bibliography/producer metadata
in the result and each model. Native JSON readers preserve this evidence.

`LeaveOneOutValidator` receives the explicit modeler choice and now requires
an `evaluator_factory` for a prepared-native screening tool (#45). It retains
the first returned hypothesis; see [the screening transition](virtual_screening_workflow.md).
Affinity-based hypothesis selection and activity-based validation remain separate.

## Guard and evidence

`tests/test_ligand_based_facade.py` protects explicit selection, iterable
dispatch, support/minimum mapping, duplicate declarations, inert historical
options, original sources, evaluated-empty results, proper-fit reflection
rejection, propagated provider/limit failures, non-default units, frame/atom
selection and native model/bibliography persistence. It also asserts the
unchanged historical audit outcomes. The #45 follow-up now refuses non-default
conformer-generation options in screening as well as modeling.

Existing independent native oracles in `tests/test_aligned_consensus.py`,
`tests/test_aligned_cliques.py` and `tests/test_rigid_consensus.py` protect
injective assignment, boundary eligibility, feature/source permutations,
repeated types, maximal-clique/package support and proper geometric fitting.
They validate the declared native families, not the retired filter.
The frozen helper fixture records its original source revision/hash; it has no
molecular access or public build method and is only an executable defect record.

The [recipe](../docs/content/cookbook/ligand_based_modeler.md) consumes the frozen
prepared EST/DES CCD fixtures. The dated review receipt is
`devguide/evidence/ligand_based_facade_review_py314.json`. This is focused
Linux/Python 3.14 source evidence, not full hosted/installed qualification or a
biological benchmark. MolSysMT #323 remains the separate environmental-H
refinement blocker for local #22; no provider code is modified here.
