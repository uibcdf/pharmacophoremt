# Explicit prepared-native virtual screening

Transition owned by [#45](https://github.com/uibcdf/pharmacophoremt/issues/45),
under the molecular ownership audit #41. `VirtualScreening` delegates to existing
public PHMT tools. MolSysMT supplies molecular recognition, source selections,
states, coordinates and fitting. No implicit preparation is performed.

## Choose the scientific method

| Explicit `screening_method` | Delegated tool | Prepared input contract |
| --- | --- | --- |
| `placed` | `PoseEvaluator` | A pose already in the query frame; `structure_index` selects one source frame |
| `rigid` | `RigidPoseSearch` | One rigid prepared frame; three essential non-collinear query anchors and finite triplet search |
| `conformers` | `ConformerScreening` | Requested prepared frames; the rigid method's restrictions apply to each frame |

There is no default choice. Constructor options such as `min_fit_value` and
method-specific `max_trials` reach the selected tool. `run()` options select
atoms/frames/declared states through that tool. See [placed evaluation](placed_pose_workflow.md),
[rigid search](rigid_search_workflow.md) and
[prepared conformers](conformer_screening_workflow.md) for their full contracts.
The facade does not verify biological suitability or physical preparation.

Historical `min_match_ratio=1.0` and `n_conformers=50` defaults are accepted but
inert; other values are refused. Essential sites must all be assigned, including
zero-weight sites. Each molecular participant fills at most one site. Donor
orientation uses the donor-H direction even for coincident centers; aromatic
orientation uses the native unoriented plane axis. Exclusions can veto full
weighted coverage. `min_fit_value` bounds total weighted coverage and does not
relax essential sites. Lengths and angles require explicit units.

These are deliberate method changes, not legacy numerical equivalence. The old
SMARTS centroids, reused participants, center-offset angular test and implicit
RDKit embedding/minimization are retired. Coordinates and chemical states must
arrive prepared; missing coordinates fail. Conformer generation remains the
provider-owned requirement [MolSysMT #219](https://github.com/uibcdf/molsysmt/issues/219).

## Records, failures and exports

`run()` materializes the input collection once and returns hit records sorted by
descending coverage with input-order ties. Each hit contains native evidence,
its original `mol` reference, `input_index` and `conf_id` (an alias of the native
source frame or best prepared frame). No `rd_mol` is manufactured. `evaluations`
keeps every native per-input record in input order; native conformer accounting,
selected indices/states, portable units, placements and optional attribution
survive. Hit evidence is detached from the cached evaluation; the `mol` reference
remains the original input. Source inputs remain unchanged.

Failures raise by default. Explicit `on_error='record'` keeps failed records with
`fit_value=None`; they are not negative observations or hits. A native ensemble
may have a resolved maximal hit and also failed frames: inspect `ensemble.complete`
and `score_resolved`, not only its top-level status. Both facade caches clear
before any entered run, including iterator, option and provider failures; they
publish only after the complete batch returns. The native tools validate the
forwarded evaluation options after that clearing step.

DataFrame/CSV contains `rank`, `input_index`, `fit_value`, `conf_id`, `status`.
Empty exports retain those columns. It does not infer names/SMILES, remove H,
generate molecular coordinates or include every negative/failure; inspect
`evaluations` for full accounting. `to_sdf()` now raises an actionable error
before opening a file. Collection/property fidelity and source atom correspondence
remain [MolSysMT #215](https://github.com/uibcdf/molsysmt/issues/215) /
[#223](https://github.com/uibcdf/molsysmt/issues/223). PHMT owns selection/ranking
and result annotations; it must not rebuild a molecular codec to fill this gap.

## Validation callers

`RetrospectiveValidator(query, evaluator=PoseEvaluator(query))` or an explicitly
configured native search is required. Its tool supplies hit status and score;
the old partial-essential threshold is refused. Original counts, recorded
failures, evaluated-subset denominators and metrics retain their contracts.

`LeaveOneOutValidator(..., evaluator_factory=RigidPoseSearch)` constructs a
native evaluator for each selected query. Additional run options reach that
tool. A nonempty native result list can contain a negative, so retrieval uses
`status`, not list length. Failed evaluation raises without producing recall.
LOO still selects the first returned hypothesis, and evaluated-empty training
consensus retains its historical no-query round. This transition does not qualify
hypothesis selection, activity splits, leakage or a complete biological pipeline.

## Guard and qualification scope

`tests/test_virtual_screening.py` covers real prepared placed/rigid/multi-frame
controls, essential/one-to-one matching, direction/exclusion veto, ordered ties,
units, optional attribution, missing preparation, failure/cache transactions,
scalar exports and native LOO retrieval. Existing native regression modules
protect the delegated chemistry/search. Original outputs are linked in the
owning report. Focused Linux/Python 3.14 source checks are separate from full
hosted matrices, installed artifacts, biological validation and benchmarks.

**#46 follow-up:** The unused molecular utilities and name-grouped library reader
are now retired; see [the contract](molecular_utility_retirement.md). Native donor
geometry delegation to MolSysMT #375 remains #41 work. The environmental-H blocker
#323 is independent of this screening facade transition.
