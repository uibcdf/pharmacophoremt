# Worked native contracts for the library design

Owners LMMV/dprada; 2026-11-06; [#108](https://github.com/uibcdf/pharmacophoremt/issues/108).
Companion to the [architecture proposal](public_library_architecture.md).
The [frozen compatibility plan](evidence/public_library_native_contract_plan_20261106.json)
selects 14 existing test functions. Their source/support hashes and expected
scope were recorded before execution. These are native/analytical software
controls, not a new library, streaming API, checkpoint implementation, benchmark
or biological screening study.

## Inputs and method boundaries

The cases reuse explicit-coordinate small molecular fixtures constructed through
MolSysMT in existing tests/support. They do not acquire chemical data, enumerate
a production collection's states/conformers or introduce a preparation policy.
Helpers in `phmt_test_support.absence_inputs` and the test modules are analytical
fixtures, not proposed public preparation APIs. Native inputs are controlled and
unchanged; that precondition does not authenticate a reusable immutable molecular
snapshot.

The public operations under study already exist: `PoseEvaluator.evaluate/run`,
`RigidPoseSearch.evaluate/run`, `ConformerScreening.evaluate/run`,
`VirtualScreening.run` and `get_screening_score`. Selecting new collection/iterator
names, persistence schemas or journal stores remains separate design work.

## Independently expected outcomes

| Case | Existing prepared setup / explicit method | Expected evidence the new workflow must preserve |
| --- | --- | --- |
| N01 placed positive | `system()` and `model_from_source`; `PoseEvaluator`, selection `[0,1,2]` | Matched; coverage 1; selected source atom and explicit pose ID retained; checked-pose score 1 |
| N02 placed negative | Same query, fixture translated by 2 nm; same selection | Valid nonmatch; coverage 0 and checked-pose score 0. This is a placement-dependent negative, not a rigid-search claim |
| N03 seeded positive | Ionic fixture with an optional site; `search_method='seeded_hit'`, `max_trials=6` | Matched; coverage approximately 0.75; binary score 1; one fitted pose; incomplete enumeration can terminate at a proven binary hit |
| N04 no-fit seeded negative | Collinear prepared `CCC` fixture and the existing hydrophobic query | Valid nonmatch; binary score 0, `fit_value=None`, `pose_evaluated=False`; complete seed enumeration, no identity-pose test or invented assignment |
| N05 invalid source | Placed batch `[source, invalid, source]`, `on_error='record'` | Matched/failed/matched; distinct ordinal occurrences; failed coverage/score None with PHMT-E103. Provider wording is not the oracle |
| N06 unresolved finite budget | Explicit rigid-search trial exhaustion | Failed/unscored with search-budget evidence; never recast as a completed negative |
| N07 partly failed ensemble with proven maximum | `ensemble(moved_coordinates(), COORDINATES)` and `ConformerScreening(max_trials=1)`, record errors | Failed/matched frames; observed best frame 1, checked-pose coverage 1, resolved/proven maximum but `ensemble.complete=False` |
| N08 unresolved partial negative | Existing distorted/invalid-frame ensemble, record errors | Failed/unscored; best observed nonmatch does not establish a definitive score; unresolved ensemble evidence retained |
| N09 requested-frame tie | Two identical prepared frames; request `[1,0]` | Selected observed best frame 1 and requested tie order retained. This does not establish order under future parallel or recovered execution |
| N10 repeated-source ranking | Placed partial/full/partial fixtures with a weighted optional site | Ranked hit ordinals `[1,0,2]`, scores `[1,.25,.25]`; evaluation order `[0,1,2]` remains separate from ranked order |
| N11 zero-weight essential site | Existing placed query with an additional unassigned essential site of weight 0 | Coverage can be1 while status is not_matched. Hit status must not be inferred from score alone |

Case numbers describe distinct semantic expectations, not independent biological
samples or necessarily one test each. The frozen test selection and its actual
parameterized results determine the executed count. Expected values derive from
known fixture geometry and existing assertions, not from copying a newly measured
output into a baseline.

Canonical sources:

- [Placed fixture and index/unit/provenance controls](../tests/test_pose_evaluation.py).
- [Rigid search and finite-budget controls](../tests/test_rigid_search.py).
- [Per-frame coverage/failure controls](../tests/test_conformer_screening.py).
- [Seeded score/no-pose/coverage distinction](../tests/test_seeded_scoring.py).
- [Facade order, repeated references, ranking and essential-site controls](../tests/test_virtual_screening.py).
- [Shared explicit prepared fixtures](../phmt_test_support/absence_inputs.py).

Always obtain the declared score through `get_screening_score`; `fit_value` alone
is insufficient to classify failure or reconstruct a ranking criterion. A binary
seeded result is not affinity or optional-site coverage. A selected observed
witness need not be the earliest tied witness among frames that failed or were
never evaluated.

## Mapping requirements not established by these controls

Native batch ordinals/pose IDs are local to the batch. Repeated batches reset
those namespaces. A collection adapter must preserve opaque source/work keys and
native IDs independently, including nested conformer/error evidence; do not offset
only the outer input index. Current summary APIs additionally require their
nonnegative integer one-to-one original/native mapping.

These controls show repeated object references, not supplier-alias persistence or
provider molecular equivalence. State expansion, source alias grouping, stable
identity through partitions and interrupted/reordered execution still need explicit
adapter tests. No many-variant-to-original summary mapping is accepted implicitly.

## Recovery scenarios for the first prototype

The selected native tests do not implement or qualify these proposed scenarios:

1. Preview/query validation leaves a one-pass source untouched unless an explicit
   sampling operation advertises its consumption/replay policy.
2. Incremental execution retains bounded in-flight state and preserves all native
   evidence and stable source occurrence keys.
3. Before outcome commitment, interruption can cause recomputation; after verified
   commitment, resume exposes that work item once. Conflicting committed payloads
   fail visibly.
4. A committed terminal failure stays authoritative in that run. Retrying it uses
   a new linked run, while ordinary resume handles only uncommitted/interrupted work.
5. A changed query/input/preparation/feature/method/budget or incompatible index
   rejects resume or creates a new linked run.
6. A second query reopens the same qualified collection without consumed-reader
   surprises; failed refresh preserves the old usable snapshot.
7. Guided and expert composition resolve to the same effective scientific settings
   and declared results; physical units, ties and failure counts remain explicit.

The architecture's next implementation slice must test these mechanisms rather
than claim them from the existing batch evaluators. Current native writers do not
supply checkpoint transactions. Large-library, index and predictive experiments
remain distinct later work with their own frozen questions and resource plans.

## Execution record and maintenance

The selected native compatibility measurement retains exact commands, source and
native-extension hashes, environment/origins, cgroup limits and original test
outputs in its linked receipt. The first controller launch failed during collection
because the repository root was absent from its import path; its output is retained.
A separate attempt corrects only the process-local path, preserving selection,
source identities, expected results and resource limits.

The [original result and portable receipt](evidence/public_library_native_contract_20261106_summary.json)
record **14 passed, zero failures/errors/skips** in the corrected attempt on
Python 3.14.10, local MolSysMT `9e1f1b1ad8bf` and the unchanged recorded native
artifact. The first attempt had five collection errors and executed none of the
selected tests; it is not hidden in the passing total.

Actual limits were CPU 19/100% quota, 512 MiB, no swap, 32 tasks, nice 19, idle I/O
and one backend thread. Whole-cgroup peak was 420,802,560 bytes, with no OOM/max
events. This measures the controller/test process scope, not per-input allocation.

Elapsed time and process/cgroup memory are execution/resource observations, not
an equivalent-workload performance benchmark. No competitor is run. Reexecute
when these scientific/native/provider contracts or expectations change, using a new
measurement identity and retaining previous results; do not update an oracle merely
to obtain a pass. Full source/installed/platform and #103 scientific gates remain
separate.
