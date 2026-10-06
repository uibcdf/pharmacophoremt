# Public greedy rigid refinement and orientation alternatives

Owned by [#29](https://github.com/uibcdf/pharmacophoremt/issues/29), following
[the ranked-seed stage](ranked_seed_workflow.md). This is a declared adaptation
of [G3PS section 2.2.2](https://doi.org/10.3390/molecules26237201), with supplied
seeds, deterministic ties, two angular policies and best-state retention.
It is not full G3PS: translation rescue, exclusion correction and seed skipping
are excluded. The original paper treats orientations after positional refinement;
its section 3.4 proposes incorporating them earlier as future work.

## Independently usable boundaries

`screening.evaluate_feature_correspondence()` evaluates any number of explicit
injective [reference, source] pairs, including zero, between native classical
inventories already in a common frame. It neither fits nor chooses assignments.
It reports separate kind, position and orientation tests, invalid pair lists,
RMSD and angular/displacement measurements as portable quantity records.
Incompatible kinds are scientific invalid pairs; malformed axes or missing
required geometry raise. Donor vectors are directed; aromatic normals are
unoriented axes. It shares the current matcher's angular cosine slack; positional
boundaries use inclusive floating comparisons without a new length slack.

`screening.refine_rigid_feature_correspondences()` consumes prepared molecular
source/context, target inventory and any supplied seed family containing at least
three injective compatible non-collinear pairs. Seeds need not be triplets or
come from ranked search. Existing `get_rigid_feature_placements()` also calls the
public pair evaluator. The shared fitting/extraction boundary uses public
MolSysMT alignment, copies, coordinates and recognition and verifies that feature
occurrence identity survives fitting. No local molecular rotation solver is added.

`modeler.from_rigid_ligands(refinement_strategy='greedy', orientation_policy=...)`
composes the public refinement tool with any existing correspondence strategy. Its
default refinement_strategy=None retains ordinary one-fit placement. An explicit
each_step policy without refinement raises. Summaries retain actual initial/trial
fit counts and accepted/rejected refinement steps, separately from proposal and
returned placement counts. Saved-report readers validate the retained counts.

## Growth and final matching are distinct

For each seed, fit the original unchanged source to its collected pairs. Accept
an initial state only if every collected pair meets the growth policy. Choose
the nearest remaining equal-kind pair in the last accepted placement; distance
ties use original reference/source indices. Add it temporarily, refit from the
unchanged original source and reevaluate every collected pair. Acceptance locks
its row/column. Rejection permanently forbids only that attempted pair for this
seed and preserves the previous accepted geometry and collected pairs.
The rejected pair is not reconsidered after later successful growth. This is a
declared greedy heuristic, not proof that no future placement could accommodate it.

- **final:** growth requires positional tolerance. All orientations are measured
  at every attempt but do not reject positional growth.
- **each_step:** initial and subsequent accepted states require both position and
  orientation tolerance for every collected pair.

Both policies independently obtain full-inventory injective matching with all
position/orientation constraints at every fitted state. Only accepted growth
states can become returned solutions. At each accepted state, preserve the best
solution meeting min_matches: greatest final match count, then smallest RMSD of
those matched centers, then earliest fit. The final matching is distinct from
the fit anchors; final-policy anchors need not all pass orientation or appear
in the final assignment. There is no per-feature essential/optional semantics
in this native inventory slice. A query-specific rule requiring particular
anchors must be independently declared, not inferred from their fitting role.

min_matches is final acceptance, not an intermediate growth threshold. A seed
with three pairs may grow to a required four or five. A later spatially accepted
state can have fewer angularly valid matches; its earlier valid checkpoint remains
available. At most one best placement per seed is returned. Duplicate seeds and
placements from different seeds remain independent alternatives; all accepted
intermediate states remain in evidence, not as extra consensus layouts.
No sufficient-match early stop or reuse-based seed skipping occurs.

## Resources, completion and evidence

All initial and trial fits count against max_fits. The minimum initial-seed count
is checked before fitting and each trial is checked before its provider call.
Consensus passes its remaining global allowance rather than resetting it per
source. max_matrix_entries retains the existing full-matching assignment bound.
Exhaustion raises PHMT-E107/PHMT-E106; provider errors propagate. No partial search
becomes an evaluated-empty result. Bound checks do not promise total memory or
wall time; retained traces and molecular copies also consume memory.

Rejections or row/column acceptance reduce the finite remaining pair set, ensuring
termination per seed. Reports distinguish selected, last accepted and rejected
states; include each fit's mapping, pair tests, full matching, previous accepted
step, actual provider evidence and reason for termination. Detached reports contain
no live molecular systems. complete=True covers this supplied seed family and
greedy policy; neither policy nor their union proves global alignment completeness.

Ackredit credits the reached G3PS refinement stage with paper section 2.2.2,
orientation_policy, adaptations and excluded stages. It reuses the existing DOI
identity so a bibliography can deduplicate the paper while keeping distinct
seed/refinement uses. Kabsch/provider and assignment citations retain their actual
execution boundaries. Empty refinement requests add no G3PS refinement credit.

## Frozen analytical controls and measured scientific outcomes

`tests/data/rigid_refinement_cases.json` declares explicit O–H donor fragments,
centers, directions, supplied seeds, tolerances and per-policy expectations.
`devtools/rigid_refinement_cases.py` builds them through MolSysMT. These are
analytical geometry controls, not physical conformations or biological evidence.

| Case and declared goal | final: fits / qualifying placements | each_step: fits / qualifying placements | Protected mechanism |
| --- | --- | --- | --- |
| Angular recovery; four matches required | 2 / 1 | 1 / 0 | Initial 45-degree donor error exceeds the 30-degree tolerance; later growth recovers all four pairs. |
| Blocked alternatives; five matches required | 3 / 0 | 5 / 1 | Early rejection frees cross-pair alternatives; positional-only growth locks the less useful pairs. |
| Valid checkpoint; three matches required | 2 / 1 | 2 / 1 | Adding a pair changes the fit and invalidates donor directions; both retain the valid initial three-match placement. |

No policy dominates these controls. Fewer fits can accompany a missed solution;
these counts do not measure runtime or establish a universal winner. Both variants
remain available. Document future comparisons with their exact inputs, objectives,
parameters, output alternatives and resources; an unfavorable measured result
alone does not justify removing a scientific strategy.

`tests/test_rigid_refinement.py` checks scalar geometry oracles, directed/axis
semantics, boundaries, invalid inputs, source immutability, these counterexamples,
rollback, valid checkpoint retention, empty/duplicate/nontriplet seeds, resource
and provider failure, public consumer composition, global counts and actual
Ackredit reuse. The [cookbook](../docs/content/cookbook/rigid_refinement.md) provides
an independently executable example. No timing thresholds enter the tests.

The initial implementation suite passed **274 tests** on Python 3.14.7, including 26 new
refinement controls. All five cookbook blocks executed and the strict isolated
Sphinx build passed using existing 3.13 documentation tooling. The
[retained six-control comparison](evidence/README.md) verifies identical scientific
traces with and without real attribution and unchanged producer source hashes.
It contains no runtime/memory measurements. Reproduce its counts and full evidence:

```bash
python -m devtools.compare_rigid_refinement --output /tmp/refinement-comparison.json
```

## Expanded validation and measurement contract

`tests/data/rigid_refinement_workloads.json` declares eleven workloads, each
evaluated with both policies by `tests/test_rigid_refinement_workloads.py`.
Existing controls retain their original inputs and expectations. Overrides are
expanded by a development fixture tool; declared chemistry and molecular motions
use the existing public MolSysMT builders. These are analytical prepared fragments,
not biological ligands or validated conformations.

The additional controls vary the recovery case's angular tolerance (60 degrees),
distance tolerance (.05 nm), and supplied seeds; start the checkpoint case with
all four anchors; compare mixed hydrophobic/donor/acceptor/positive-charge features
under proper motion and reflection; and grow asymmetric three-dimensional
arrangements of six and twelve donors with varied directions. Seeds must be
noncollinear in both systems. Donor and acceptor features can share a center, so
three different feature indices need not define a valid rotation.

The same public refiner and public pair evaluator protect output correctness and
source immutability. Expectations describe these supplied-seed greedy searches.
In particular, an empty result does not prove that every other seed would fail,
and multiple returned placements do not establish distinct binding modes.

The opt-in measurement driver runs a fresh sequential worker per workload/policy:

```bash
python -m devtools.benchmark_rigid_refinement --repetitions 3 --warmups 1 --output /tmp/refinement-benchmark.json
```

Each worker prepares native molecular systems and feature inventories, performs
one warmup, measures three public refinement calls with attribution disabled,
and performs a separate identical call with actual Ackredit capture. Full
scientific report hashes must agree across all five calls. Only the refinement
call is timed; imports, preparation, warmup, garbage collection, hashing,
serialization and citation rendering are excluded. Whole-worker high-water RSS
includes imports, preparation and warmup; it is not incremental call allocation.
No timing thresholds enter the test suite.

The driver retains expanded fixture inputs, fit counts, all trial geometry and
matching evidence, raw timing samples, memory scope, software/source/loaded
MolSysMT-extension identities and actual citations. It checks provider source
hashes before/after each worker, worker identities against one another, and input
file identities across the complete run. Worker/provider failures remain failed
calculations. Small local timing differences do not justify removing an option.

## Measured expanded controls (Python 3.14.7)

All 22 workload/policy comparisons passed with stable complete reports across
one warmup, three measured calls and a separate actual attributed call each.
Provider sources were unchanged during workers; source/loaded-extension identities
agreed across workers, and input files were unchanged across the run. Test and
documentation builds finished before measurement. The full suite passed **296
tests** in 282.81 s, with the same two known warnings; the strict isolated cookbook
build passed using the existing 3.13 documentation tooling.

Each solution cell is **returned placements / largest returned match count**;
an em dash means no placement satisfied min_matches. Counts do not denote distinct
binding modes. Fit and median-time columns list final / each_step respectively.
Times are local seconds per refinement call on already prepared inventories.

| Workload | final solutions | each_step solutions | Fits | Median seconds |
| --- | ---: | ---: | ---: | ---: |
| orientation_recovery | 1 / 4 | 0 / — | 2 / 1 | 0.614 / 0.330 |
| orientation_blocking | 0 / — | 1 / 5 | 3 / 5 | 0.917 / 1.449 |
| orientation_checkpoint | 1 / 3 | 1 / 3 | 2 / 2 | 0.598 / 0.601 |
| recovery_angle_60 | 1 / 4 | 1 / 4 | 2 / 2 | 0.615 / 0.609 |
| recovery_distance_005 | 0 / — | 0 / — | 2 / 1 | 0.542 / 0.319 |
| recovery_two_seeds | 2 / 4 | 1 / 4 | 4 / 3 | 1.139 / 0.908 |
| checkpoint_full_seed | 0 / — | 0 / — | 1 / 1 | 0.350 / 0.351 |
| rigid_mixed_5 | 1 / 5 | 1 / 5 | 3 / 3 | 1.183 / 1.263 |
| reflection_mixed_5 | 0 / — | 0 / — | 3 / 3 | 1.091 / 1.112 |
| rigid_donors_6 | 1 / 6 | 1 / 6 | 4 / 4 | 1.282 / 1.268 |
| rigid_donors_12 | 1 / 12 | 1 / 12 | 10 / 10 | 4.157 / 4.777 |

Relaxing the recovery angle admits the previously rejected seed; tightening its
spatial tolerance prevents the required match in both policies. An alternative
noncollinear seed restores each_step recovery at additional cost. Starting with
all four checkpoint anchors skips the valid three-anchor state and returns no
qualifying placement. These cases make seeds and tolerances part of the measured
scientific method, rather than interchangeable implementation details.

Both policies recover all sites under proper motion in the mixed-family and
larger donor controls. Twelve donors require ten fits under this
per-seed greedy extension contract, even though a qualifying full match is
already observed at the initial fit. It continues to compare accepted states;
any earlier stopping policy would require its own contract, evidence and option.

Whole-worker high-water RSS after measured calls ranges from **523.1 to 527.1
MiB**, including imports, preparation and warmup. This does not measure call
allocations or establish a memory-efficiency advantage. Three repeats on one
machine also do not isolate the cause of small timing differences or establish
statistical superiority. Comparing fewer fits must account for missed solutions
and different returned alternatives. Both scientific policies remain available.

The [retained benchmark evidence](evidence/README.md) includes every trial,
expanded fixtures, raw time samples, scoped memory, identities, checksums and
actual per-policy G3PS usage. Original count-only evidence remains unchanged.
Biological validation, other preparation/feature families and large workloads
remain future comparisons; full G3PS and acceleration are not established here.

## Future alternatives

Orientation-guided order, rejection reconsideration after changed states,
invariant angular necessary-condition filtering, bounded branching and joint
position/orientation optimization are separately declared strategies. Ordering
changes can affect greedy outcomes even without deleting input candidates.
Generic geometric solvers and molecular transformations belong in MolSysMT;
PHMT owns pharmacophoric constraints and method-specific search decisions.
Rust, GPU and distributed execution must preserve a chosen scientific contract.
