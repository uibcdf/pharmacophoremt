# Native screening argument and batch contracts

Owner LMMV/dprada; [#99](https://github.com/uibcdf/pharmacophoremt/issues/99),
bounded follow-up to [#6](https://github.com/uibcdf/pharmacophoremt/issues/6).
Received 2026-11-05 from main `9132f12` plus the recorded source overlay.
[Original receipt](evidence/native_batch_contracts_20261105_summary.json).

## Admission and compatibility

PoseEvaluator, RigidPoseSearch and ConformerScreening now use definition-owned
ArgDigest FunctionContracts for `__init__`, `evaluate` and `run`. Closed signatures
remain their own domains. Each run's additional option domain reads its defining
evaluate signature lazily, after class creation, avoiding circular imports and
duplicated option lists. These are PHMT-native contracts, not molecular APIs.

| Native batch | Evaluate options admitted in addition to the run signature |
| --- | --- |
| PoseEvaluator.run | selection, structure_index, chemical_state, pose_id |
| RigidPoseSearch.run | selection, structure_index, chemical_state, pose_id |
| ConformerScreening.run | selection, structure_indices, chemical_state, pose_id, on_error |

`pose_id` remains admitted to its existing **explicit refusal**: batch IDs are
input indices. ConformerScreening forwards on_error to its per-frame evaluator;
the other methods keep that control at batch level. Existing value digesters,
standardizer, defaults and attribution/diagnostic decorators remain active.
Literal `skip_digestion=True` retains its established internal bypass; explicit
batch ID/error-policy checks still run. Bypassed calls do not receive a new
guarantee of domain validation.

With normal digestion, unknown options, literal `kwargs`/`evaluation_options`
and wrong-method frame keywords now raise public ArgDigest UnknownArgumentError
(TypeError family) **before consuming native batch input**, including empty
batches. Previously empty batches returned an empty result and nonempty batches
refused only during evaluate, after iterable consumption. The irrelevant
missing-digester warning is removed for these refused names. Valid scientific
calls and owned pose-failure diagnostics/causes are unchanged.

Inherited implementations retain the defining native contract and application
diagnostic identity. A subclass adding scientific evaluate parameters must own
its corresponding run API/contract; inherited native run no longer accidentally
admits arbitrary application extensions. There is no dynamic domain derived from
self, local signature-validation engine or provider modification.

VirtualScreening.run is byte-identical: it clears both caches, materializes the
input once and delegates to the selected native batch. Admission stays after
that reset. Its materialization order is not the native batch's early-admission
guarantee. Selection, coordinates, states, transforms and molecular formats
remain MolSysMT-owned.

## Measured receiving

The 45 new controls initially produce 33 failures/12 passes on original
production. Nine failures are new declaration requirements. Two initial facade
failures used an invalid implicit compatibility ranking; corrected seeded_hit
fixtures on original production independently confirm all three empty-facade
typo failures. Both attempts remain in the archive; they are not 33 independent
scientific defects.

The existing public prefix (Python 3.14.10, ArgDigest 0.17.1, public MolSysMT
0.23.0) passes **84** focused controls: 45 new and 39 nested-facade controls,
6.79 s, no warnings. Current PHMT source is explicitly imported from this
checkout; this is not an installed current PHMT artifact qualification.

The existing controlled modern MolSysMT source environment (Python 3.14.7,
MolSysMT `0faf1584d`, published ArgDigest 0.17.1 extracted into an already-owned
overlay) passes **167** controls in 70.18 s. This includes the same 45 new tests
and 122 existing pose, rigid, conformer, facade, retrospective and saved-result
tests. One intentional optional-attribution failure warning remains visible.
There are **206 unique passing selectors**, not 251 distinct tests. No skips or
failures in either final run. Actual source/native/metadata identities of all
eight selected providers match the prior #82 receipt and stay stable during
each run; public-prefix origins/identities are retained separately.

Only nine decorator configurations and their imports change in the three
scientific modules: removing exactly those additions reproduces their complete
original ASTs. The batch helper, facade, root digestion configuration, metadata,
recipe, source pins and release plan remain byte-identical. One new runtime
declaration file is added to the existing Conda resource inventory; the private
installed-support declaration is unchanged.

All heavy runs execute serially on allowed CPU 19 with CPUQuota=100%,
MemoryMax=1 GiB, MemorySwapMax=0, TasksMax=32, nice=19, idle I/O and six numerical
thread limits of one. Actual process affinity/priority/cgroup limits and
memory/pressure snapshots are retained. No continuing process is required.
Capsule `build/phmt-native-batch-20261105-fjqyejoy`, owner LMMV/dprada, review
2026-11-19 or relevant change; borrowed environments/providers are not edited.

Broader #6 and audit item 3 remain partial. Full source/support/installed/public
and platform gates remain #9/#10/#23; modern public molecular delivery remains
#95/MolSysMT #375/#255. PyUnitWizard #141/SMonitor #63 performance handoffs and
experimental binding-method access #66 retain their separate scope. No new
scientific method, optimization, dependency floor, package, tag or Release.


## Administrative closeout

23 distribution, 18 archive-reader and three reporting controls pass. The initial
reporting check correctly refuses the missing #99 expected inventory entry;
adding only that identity repairs it, without weakening validation. Both logs
are preserved. Declared dependency routes/generated environments, full-repository
Ruff/format (372 files), index and whitespace checks pass; the changed reporting
inventory has its own final Ruff/format checks. These are administrative results,
not another full scientific run or installed/platform qualification.
