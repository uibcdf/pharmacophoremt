# Typed neighborhood comparison and ranked rigid seeds

Owned by [#28](https://github.com/uibcdf/pharmacophoremt/issues/28), following
[the modular comparison](rigid_strategy_comparison.md). This implements the
first stage of Permann, Seidel and Langer's
[G3PS paper](https://doi.org/10.3390/molecules26237201), section 2.2.1.
It is a separately named PHMT adaptation, not a complete G3PS alignment.

## Ownership and public composition

MolSysMT owns molecular recognition, feature geometry, fitting, copies and
coordinate transformations. PHMT owns typed feature environments and seed
selection. SciPy owns generic assignment; no assignment solver is copied here.
`get_feature_pair_dissimilarities()` compares existing native inventories without
molecular access. `rank_rigid_feature_correspondences()` ranks supplied triplets
against that comparison; it does not enumerate or fit them. Existing public
proposal and placement tools supply those operations.

`get_rigid_feature_correspondences(correspondence_strategy='ranked_triplet_seeds')`
composes the two public operations with the same feasible typed non-collinear
triplet family as `triplet_seeds`. `from_rigid_ligands()` consumes these proposals
through the existing public placement boundary. Defaults remain unchanged.
The [cookbook](../docs/content/cookbook/ranked_seeds.md) executes the composition.

## Declared mathematical adaptation

For each same-type focal pair, exclude both focal features and compare their
neighbors' kinds and distances from the focal centers. With a uniform positional
tolerance tau, same-type neighbor cost is
`min(abs(reference_distance - candidate_distance) / (2*tau), 1)`.
Different neighbor types and unmatched neighbors cost one. Square padding makes
the unmatched penalty explicit; the paper does not specify padding conventions.
SciPy minimizes the resulting neighbor assignment cost. Divide its sum by the
larger **whole inventory** feature count, as in the paper's normalization.

Different focal types are marked incompatible independently of their numeric
cost. Singleton same-type focal pairs have cost zero. Empty axes succeed with
zero assignments. Reported costs are finite, dimensionless and on [0, 1].
Indices refer to the inventories' original order. Distances concern pharmacophoric
feature relationships; this function never obtains or manipulates a molecular
system. The reference/source inventories must share the intended feature definition;
the tools retain the existing native classical inventory validation boundary.

Sum three focal costs to score each supplied triplet. Canonical pair order,
then supplied index, breaks ties deterministically. Duplicates remain independent
supplied alternatives. The ranking reader accepts saved comparison JSON, checks
axes/cost/mask completion and rejects incompatible or out-of-range pairs. The
caller owns evidence identity; cached matrices cannot authenticate their source.
Prior attribution is detached into `source_attribution`, separately from newly
executed ranking credit.

`n_seeds=None` retains all supplied/proposed guesses. A positive integer selects
at most that many ranked guesses and records omitted counts and
`selection_exhaustive=False` if anything was omitted. It is a scientific strategy
parameter, not a failure budget. `complete=True` concerns completed ranking and
this declared selection; it never means global alignment completeness. Supplying
n_seeds to another proposal family raises rather than silently ignoring it.
`summarize_rigid_consensus()` now retains ranked/omitted counts and per-source
proposal selection exhaustiveness.

## Resources and scientific checks

Triplet candidate-product exhaustion still raises PHMT-E107 before ranking.
Neighborhood comparison preflights each distance, pair or padded neighbor-cost
matrix against max_matrix_entries. Counts retain assignment calls, cumulative
neighbor matrix entries and the largest matrix. This is not a runtime or total
input/temporary-memory guarantee. Existing fit/layout/assignment/hypothesis budgets
and post-fit directional/normal tests remain in force. Scientific selection never
clips work merely to avoid an exhausted budget.

With all seeds retained, ranked and unranked families contain identical mappings;
placement and hypothesis order may differ. Limiting seeds can miss an existing
match. The frozen reflected tetrahedron contains two positive and two negative
charge features. A different same-type pairing permits a proper four-feature
alignment, but its first ranked triplet does not. With n_seeds=1, completed
consensus is empty; all 16 seeds give eight four-site alternatives. This guards
against treating a heuristic negative as complete continuous incompatibility.
Symmetry, mirrored inputs and directional constraints can be invisible to a
distance-only environment descriptor. Dissimilarity is not a safe rejection test.

## Attribution and next G3PS stages

Real optional Ackredit capture credits DOI 10.3390/molecules26237201 with role
`methodological_basis`, paper section, uniform-tolerance/padding/tie adaptations
and excluded stages. Neighbor assignment separately credits executed SciPy and
its modified Jonker–Volgenant reference. No unused G3PS stage is credited as
executed; empty comparisons record no G3PS method credit. Shared application
sessions and portable bibliography follow the existing attribution boundary.

The primary paper's section 2.2.2 fits three-pair guesses, forbids reused rows and
columns, attempts the nearest remaining same-type pair, refits, preserves the
previous accepted alignment after rejected additions and optionally applies
translation rescue. Section 2.2.3 adds exclusion-volume corrections. These are
independent operations. [Public greedy refinement](rigid_refinement_workflow.md)
is now delivered under #29 with both angular policies and best-state retention.
Translation rescue and exclusion corrections remain future stages. The paper does not specify the translation-rescue
solver; full replication cannot be inferred from its mention. Reviewed generic
point-set/constraint geometry should be reused from an identified provider,
including MolSysMT where applicable, before adding a molecular implementation.
MolSysMT's inspected public tools provide least-RMSD fit and translation, but no
documented tolerance-constrained translation-rescue API was identified in this
checkout. No local molecular rescue solver is introduced by this stage.

## Verification and optional comparison

`tests/test_ranked_seeds.py` uses an independent bounded permutation oracle,
unit/motion/permutation controls, incompatible/empty/unequal inventories,
input/report ownership, malformed saved reports, failure budgets, consumer calls,
real-provider selection false negatives and actual Ackredit reuse. Timing
thresholds are absent. `tests/data/ranked_seed_cases.json` extends the original
analytical family with explicit per-strategy n_seeds=1 settings and expectations.
The optional driver keeps the original two-strategy default and accepts named
strategy subsets and strategy-specific fixture parameters:

```bash
python -m devtools.benchmark_rigid_consensus --cases tests/data/ranked_seed_cases.json --strategies triplet_seeds ranked_triplet_seeds --repetitions 3 --warmups 1 --output /tmp/ranked-comparison.json
```

Compare scientific outcomes, selected/omitted counts and total work as well as
times. Reduced fits with fewer returned alternatives do not establish an equivalent
faster algorithm. Record the genuine false negative. Earlier evidence files retain
their producer hashes and must not be relabeled as measurements of this code.

## Recorded local comparison — 2026-10-03

The [retained evidence](evidence/README.md) contains 14 sequential case/strategy
records, all passing their expectations. Python 3.14.7 used the editable checkout
and installed providers without PYTHONPATH overrides. Each worker used one
warmup, three timed calls and a separate attribution call; scientific outputs
were stable and source/loaded-extension hashes identical across all workers.
Tests and documentation builds finished before measurement began.

The ranked variant explicitly used **n_seeds=1**. Times are median seconds for
the entire from_rigid_ligands call, not descriptor-only speed. Model counts retain
accepted proposal/layout alternatives, including potentially identical geometry.

| Analytical case | Fits: triplet / ranked | Models: triplet / ranked | Maximum joint sites: triplet / ranked | Median seconds: triplet / ranked |
| --- | --- | --- | --- | --- |
| Proper typed rigid motion | 11 / 1 | 7 / 1 | 5 / 5 | 6.412 / 1.320 |
| Typed reflection | 11 / 1 | 0 / 0 | 0 / 0 | 3.662 / 0.870 |
| Symmetric triangle | 6 / 1 | 6 / 1 | 3 / 3 | 2.555 / 0.626 |
| Warped square | 16 / 1 | 16 / 1 | 3 / 3 | 9.010 / 0.913 |
| Empty source | 0 / 0 | 0 / 0 | 0 / 0 | 0.547 / 0.539 |
| Reflected typed tetrahedron | 16 / 1 | 8 / 0 | 4 / 0 | 5.222 / 0.431 |

The seventh case enforces max_fits=1. The baseline correctly fails with PHMT-E107
before fitting its six scheduled proposals (median failure-call time 0.093 s).
The ranked strategy legitimately schedules one scientifically selected proposal
and completes with one three-site model (0.624 s). A failed calculation and a
completed selected result are not performance equivalents.

Whole-worker peak RSS after measured calls spans 452.0–531.6 MiB and includes
imports, fixtures and warmups; it is not incremental call allocation. Completed
calls captured actual Ackredit evidence. The G3PS stage DOI appears in ranked
nonempty comparisons and is absent from both baselines and empty comparisons.
The archive retains individual samples, provider/source/extension identity,
scientific hashes, geometry and actual usage trees.

These measurements demonstrate reduced work with changed alternatives and a
real false negative. They do not justify a default seed limit or equivalent-recall
speed claim. Provider source/extension identity differs from the earlier #27
measurement; timings across those two artifacts cannot isolate strategy or code
performance. This comparison is local analytical evidence, not biological or
external-tool benchmarking. All-seed family equivalence is tested separately;
all-seed ranked execution was not timed in this comparison.
