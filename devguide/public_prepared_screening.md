# Public incremental screening of prepared inputs

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108), mature-0.x milestone2.
This promotes the proved [incremental reference](prepared_library_reference.md)
into one public runtime implementation. It is a useful prepared-input task;
public recovery, managed collections and full installed/public qualification
retain separate gates.

## Public boundary

`pharmacophoremt.screening.PreparedInput` declares `work_key`, `source_key`,
`occurrence_key` and an already prepared `molecular_system` handle.
`screen_prepared(inputs, evaluator, *, score_method, on_error='raise',
evaluation_options=None)` returns an iterator. The implementation lives in
[`screening/prepared_screening.py`](../pharmacophoremt/screening/prepared_screening.py).
The old support module contains exact compatibility aliases, not another algorithm.

The frozen record freezes its fields, not the molecule. Nonempty opaque keys
are checked when encountered; global work-key uniqueness, source correspondence
and unchanged query/evaluator/input remain producer preconditions. Repeated
source/occurrence keys and molecular handles are permitted and establish no
chemical equivalence or independent assay denominator.

## Admission, consumption and ownership

The public factory has a closed definition-owned ArgDigest contract with explicit
value digesters. Its borrowed source digester returns the source unchanged:
neither `iter(inputs)` nor sampling occurs during construction. Common options
are copied. The selected native evaluator's empty-batch `run(())` owns option
admission; selection/chemistry still need actual molecular access. No duplicated
native option-name registry is introduced.

Each pull requests one entry and completes one native evaluation, setting its
work key as the native pose ID, including nested conformer/failure IDs. Results
contain exactly the three mapping keys, `native_result`, `ranking_score` and
resolved versioned `score_method`. All outcomes retain encounter order. The
envelope adds neither a live molecule nor a native batch `input_index`.

Only native `PoseEvaluationError` is recordable. Valid negatives retain zero;
failures stay unscored with native causes. Reader, mapping and programming errors
propagate. `ConformerScreening` receives the same explicit policy for its frames.
Native methods retain their coverage, witness and incomplete-search contracts.

The caller owns readers, replay and output publication. Closing the output stops
further pulls and releases adapter-held references; it never explicitly closes
the caller's source. Normal Python finalization can still close an unreferenced
source generator. Retain/manage readers intended for reuse. The adapter retains
the current item/result and fixed options; individual molecular work and caller
accumulation have separate costs. No collection-sized uniqueness set is built.

This Python envelope is not a new persistent-file/journal schema. No resume,
retry, source authentication, molecular preparation, indexing or durability
guarantee is implied. `VirtualScreening.run` keeps its ranked hit-only return and
complete caches. Its contract is not changed into an incremental stream.

## Diagnostics and attribution

SMonitor records the public factory boundary. Native scientific tools continue
to own calculation diagnostics and optional backend/unit/provider contracts.
There is no new molecular/physical-quantity parser or optional engine boundary.

The factory has no eager attribution decorator: creating or closing an unconsumed
iterator earns no completed calculation credit. Applications enable attribution
and own the Ackredit session while consuming. Native evaluations capture actual
operations; partial consumption and reader interruption retain completed evidence
and preserve the application session. No whole-stream completeness is inferred.

## Public task and source evidence

The [cookbook](../docs/content/cookbook/prepared_incremental_screening.md) uses
only public PHMT/MolSysMT and standard-library operations: load a native query,
read authorized prepared H5MSM files lazily, screen and export JSONL/CSV. The
application supplies paths and stable keys. Fresh output mode preserves existing
destinations; errors can leave a partial export, which is not a transactional run.

The [prospective plan](evidence/public_prepared_plan_20261107.json) was
[declared before qualification](https://github.com/uibcdf/pharmacophoremt/issues/108#issuecomment-6701668004).
The [source overlay](evidence/public_prepared_execution_20261107.json) fixes the
runtime/config/test/recipe bytes. The source selection passes89 scientific
cases: the26 original incremental controls now use public imports,14 new public
admission/export/attribution cases, and native recovery/facade regressions.
The actual scientific context/native identity and canonical event/JUnit records
remain in `build/phmt-public-prepared-20261107-bsuq6ue6`.

Both cookbook Python blocks execute from source against the original three
PubChem3D native files and saved caffeine query. JSONL/CSV preserve all three
source mappings/statuses with scores0/1/1; originals are unchanged. Actual native
attribution retains12 session items/27 uses. These are the same old supplied
conformers, not a new activity cohort or independent-compound count.

The same source increment also passes24 distribution,3 reporting and18 archive
cases:134 distinct selected local tests in total, without counting recipe blocks
as tests. Ruff check/format, developer-guide indexes and declared dependency
routes pass. Actual enforced limits remain one CPU/thread, nice19/idle I/O,
512MiB cgroup and no swap; selected scientific peak445,620,224 bytes. These
focused results do not replace the supported source/installed/public matrix.

## Delivery checkpoint

Owned installed-wheel receiving is **pending** at this source checkpoint. Build
from a frozen source commit in an isolated local clone, use declared build tools,
install into an owned target outside the checkout and execute the public recipe
with actual origin/artifact verification. The shared prefix has versioningit3.3;
the project requires~=2.0. A verified cached2.3.0 build-only overlay satisfies
that unchanged requirement without network or shared-environment modification.

The public helper migration changes experimental recovery source fingerprints.
Historical saved reading remains separate; incompatible reexecution must use a
compatible producer or a new linked run, without rewriting prior outcomes.
MolSysMT#624 still owns reusable molecular collection/lifetime/snapshot tools.
After bounded installed receiving, continue the selected public recovery/results
task with an explicit persistence/migration contract. Full #9/#23 supported
source/installed/public/platform and #95 release gates remain unexecuted here.
