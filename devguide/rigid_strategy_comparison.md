# Modular rigid tools and analytical comparison

Tracked by [#27](https://github.com/uibcdf/pharmacophoremt/issues/27), building on
[rigid consensus](rigid_consensus_workflow.md) and the
[primary-source survey](pharmacophore_search_strategies.md). Publication packaging
remains [#20](https://github.com/uibcdf/pharmacophoremt/issues/20).

## Public steps and ownership

1. `modeler.get_features()` obtains chemical participants and geometry through
   MolSysMT, retaining the source occurrence/state/frame domain.
2. `modeler.from_feature_inventory()` constructs a Feature + Shape query from a
   nonempty native inventory, without molecular access or repeated recognition.
   It supports classical features and included heavy-atom volumes, checks
   orientation consistency and detaches source evidence. `from_ligand()` now calls
   this tool and retains its molecular link/reference metadata. Supply native
   quantity objects; this function does not decode detached inventory JSON.
3. `screening.get_rigid_feature_correspondences()` supplies independently chosen
   association-clique or typed-triplet proposals.
4. `screening.get_rigid_feature_placements()` fits **explicitly supplied mappings**
   through MolSysMT, re-extracts features and verifies seed positions/orientations
   and injective full-inventory matching. It returns every accepted molecular copy
   and native inventory, plus a detached accepted/rejected report. Proposal indices
   retain supplied order. Duplicates remain separate; generation and early stopping
   are not implicit. `complete=True` covers only supplied mappings. Consumers must
   independently propagate proposal-generation incompleteness. Pharmacophoric
   acceptance belongs to PHMT; all molecular geometry and transformations remain
   in MolSysMT. Provider failures never invoke a local molecular solver.
5. Existing aligned matching/clique/hypothesis tools consume placed inventories.
   `from_rigid_ligands()` owns pivot selection, global fit budget, unplaced-source
   accounting and layout combinations, and now calls the public placement tool.
   Scheduled mappings are checked before fitting each source batch.
6. `validation.summarize_rigid_consensus()` reads a completed detached report,
   including saved JSON, without molecular access or new attribution. It reports
   proposal/fit/alternative counts, maximum accepted and observed matching
   separately, and hypothesis joint support/geometry. Incomplete or inconsistent
   retained counts are rejected, not interpreted as scientific negatives.

Reused source inventories must come from the unchanged source with the same
selection/frame/state and feature-family request. Axis checks cannot authenticate
origin or geometry. Accepted live systems are omitted from portable reports;
native placement inventories remain directly reusable. Detached reports have
independent ownership. Cached query construction retains previous source capture
in source_attribution, if present, while recording only newly reached construction
operations. Summary reading adds no credit. Placement composition shares the
existing capture and reached Kabsch/assignment references. These two baselines
execute no G3PS method. The separate [ranked-seed stage](ranked_seed_workflow.md)
now implements and credits its declared section 2.2.1 adaptation; its measurements
are retained separately from this original comparison.

## Objective counterexample

The `warped_square` case declares four alternating acceptor/positive-charge centers
in the yz plane at y/z coordinates ±1 nm. Candidate centers have alternating x
displacements ±0.11 nm. Fragment chemistry and analytical atom coordinates are
declared inputs; there is no bound-state or conformer-energy claim.

Invariant filtering retains maximal four-pair mappings. MolSysMT's full-mapping
fit has RMSD **0.11 nm**, yet zero reference features match at **0.10 nm** position
tolerance. A triplet fit yields **three valid matches**, despite larger RMSD over
the **same four pairs**. Comparing a three-anchor RMSD with a four-anchor RMSD
would not prove this objective difference; the regression compares one domain.

The association family completes with zero models; the triplet family retains
16 placements/layouts and 16 three-site models. These are proposal alternatives,
not 16 distinct physical binding modes. This is #26's documented excluded-submapping
limitation, not a completion-contract violation or a continuous-optimality proof.
It supplies a precise coverage acceptance control for future G3PS work.

## Frozen controls and optional execution

`tests/data/rigid_consensus_cases.json` records chemistry, atom coordinates, nm
units, feature requests, tolerances, minimum matches/sites, budgets and expected
outcomes for rigid-motion recovery, reflection, three-feature symmetry, the warped
square, an empty candidate and intentionally exhausted fit budget.
`devtools.rigid_consensus_cases` constructs them exclusively through MolSysMT; it
is a task-specific fixture builder, not a preparation backend. The modular-tool
and strategy-comparison tests contain no timing thresholds.

Run from a source checkout with compatible dependencies:

```bash
python -m devtools.benchmark_rigid_consensus --repetitions 3 --warmups 1 --output /tmp/rigid-comparison.json
```

Use repeated `--case` options for a subset, `--cases` for another declared JSON
file and `--timeout` to bound each worker. One worker per case/strategy runs in
sequence. Thread environment variables are set to one before imports; the public
MolSysMT configuration selects CPU/one-thread policy. Observed settings are stored;
provider-private algorithms are not inferred.

Imports/fixture construction and warmups are recorded separately. Measured times
cover from_rigid_ligands only, excluding summaries, between-repeat garbage
collection and a separate identical attribution call. Scientific summaries must
remain identical across repetitions and the attribution call. Failed calls retain
their own status/code/context and duration, separate from completed-empty cases.
Expected resource failure is a passed control, never a successful calculation.
Unexpected failure, timeout, output drift or expectation mismatch yields nonzero
CLI exit.

Memory evidence is whole-worker high-water RSS before/after measured calls, in
bytes on Linux/macOS, including imports, fixtures and warmups. It is not incremental
per-call memory or Python-only allocation. Unsupported platforms report null;
high-water differences are not presented as peak allocation.

Output includes fixture/driver/builder hashes, checkout HEAD/dirty state, package
Python-source hashes, loaded MolSysMT extension hashes, observed versions,
platform/CPU/thread settings, samples/min/median/max, scientific summaries and
separate reached attribution. Source hashes do not qualify published packages or
complete binary dependency closure. Actual producer versions remain unmodified.

Run timings without another known local test/benchmark load and repeat before
claiming stable performance. These fragment controls establish objective differences
and observed local costs, not a universal winner, biological validation or global
alignment completeness. Result publication remains a separate #20 decision.

## Recorded local comparison — 2026-10-03

The [retained evidence](evidence/README.md) contains the complete compressed
driver output and a reviewable JSON projection. All 12 controls passed with
one warmup and three measured calls per isolated worker on Python 3.14.7 in
`molsyssuite@uibcdf_3.14`. Scientific summaries were unchanged across warmups,
repetitions and a separate captured-attribution call. Provider Python-source
and loaded molecular-extension hashes were identical across workers.

| Analytical case | Association fits / models / max sites | Triplet fits / models / max sites | Median call seconds: association / triplet |
| --- | --- | --- | --- |
| Rigid typed five-feature recovery | 1 / 1 / 5 | 11 / 7 / 5 | 1.326 / 7.973 |
| Reflected typed features | 1 / 0 / 0 | 11 / 0 / 0 | 0.890 / 4.097 |
| Three-charge symmetry | 6 / 6 / 3 | 6 / 6 / 3 | 2.777 / 2.594 |
| Warped square | 4 / 0 / 0 | 16 / 16 / 3 | 1.244 / 8.552 |
| Empty source | 0 / 0 / 0 | 0 / 0 / 0 | 0.425 / 0.528 |
| Intentionally exhausted fit budget | failed PHMT-E107 | failed PHMT-E107 | 0.032 / 0.112, failed calls |

Whole-worker high-water RSS after measurements ranged from approximately
452 to 531 MiB. NumPy was 2.4.6, SciPy 1.18.1 and NetworkX 3.7; observed MSM
policy was CPU, parallel=False and one thread. Original MolSysMT version
`0.22.4+24.g42b487869`, PyUnitWizard `0.27.0` and Ackredit
`0.8.0+52.g15b1958.dirty` are recorded with their source hashes. Provider
working trees were used directly; these are not the older controlled 3.13 pins.

Association mapping reduces fits on the rigid typed control; triplets retain
coverage missed by maximal-mapping fits in the warped square. Equivalent seeds
remain separate alternatives. The small symmetry timing difference does not
establish a winner. Documentation building overlapped the beginning of the run;
repeat measurements without that load before making performance decisions.
This evidence motivates an independently specified coverage-oriented G3PS
comparison and larger prepared-inventory workloads, rather than default changes
or native acceleration based on these small controls.
