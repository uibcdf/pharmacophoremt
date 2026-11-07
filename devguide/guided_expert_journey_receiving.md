# Guided and expert prepared-run journey receiving

Owners LMMV/dprada; 2026-11-07 UTC; [#108](https://github.com/uibcdf/pharmacophoremt/issues/108).
The [receipt](evidence/guided_expert_journey_20261107_summary.json) records a
controlled public workflow comparison and its concrete error-recovery correction.
It advances mature-0.x milestone 2; it is not a human usability study.

## Public task and observed barrier

The guided [cookbook](../docs/content/cookbook/recoverable_prepared_screening.md)
uses `PreparedScreeningRun`. The expert route composes public
`ScreeningRunStore` and `resume_prepared_run` with an independently built plan.
Both use the same three original prepared PubChem3D artifacts, saved caffeine
query, explicit compatibility declarations, rigid seeded-hit method, a budget of 10000 trials
and state/frame 0. No new acquisition, preparation or threshold selection.

The baseline demonstrates equal complete effective contexts/query bytes, full
native outcomes, observed ranks and JSONL/CSV bytes after interruption/resume.
Separate run IDs remain separate journal identities. Scores remain 0/1/1; a valid
zero nonmatch is the first confirmation, followed by two new confirmations.

It also reproduces a guided recovery trap: a missing query consumes all three
metadata rows and creates a manifest before query admission fails. A corrected
query then encounters `FileExistsError` at that same manifest destination.
The expert route admits its plan first and has no such metadata/file effect.

The cookbook now calls its existing public plan builder before manifest creation
and metadata traversal. Revised source and the same previously qualified owned
wheel each refuse the missing query with zero metadata pulls and no manifest/run
output, then successfully use those destinations for the corrected query.
Full settings/native/ranking/export equality with the completed expert reference
remains. Manifest-write/export failures retain their separately documented partial
file behavior; no atomic-publication or general source-recovery claim is added.

## Execution evidence and retained failures

The [prospective plan](evidence/guided_expert_journey_plan_20261107.json) was
[declared before execution](https://github.com/uibcdf/pharmacophoremt/issues/108#issuecomment-6703534288).
The [first overlay](evidence/guided_expert_journey_execution_20261107.json)
corrects an unexecuted attribution-field assumption from source inspection.
The [continuation](evidence/guided_expert_journey_execution_20261107_attempt2.json)
and [revised-recipe overlay](evidence/guided_expert_journey_execution_20261107_attempt3.json)
retain their distinct source/recipe identities. An incorrectly transcribed hash
in the declaration comment was [corrected before revised execution](https://github.com/uibcdf/pharmacophoremt/issues/108#issuecomment-6703600689).

| Phase | Query failure / metadata | Corrected query | Full parity |
| --- | --- | --- | --- |
| Original guided baseline | Leaves manifest; consumes 3 rows; valid retry blocked | Completed separately with fresh destinations | Original completed guided results retained |
| Expert baseline continuation | Plan admission precedes metadata/output | Partial/resume completes | Full settings/native/ranks/export bytes agree |
| Revised guided source | No manifest/run; consumes 0 rows | Same-destination retry and resume complete | Agrees with completed expert reference |
| Revised guided installed wheel | No manifest/run; consumes 0 rows | Same-destination retry and resume complete | Agrees with completed expert reference |

The first baseline completes the guided scientific work and then fails a harness
assertion requiring global Ackredit absence. The continuation reads that existing
run and executes only the unfinished expert route; it does not recompute the
guided results. Original source/log/failure receipt remain. All later phases
preserve the same native bodies and actual producer versions without normalization.
Authentic closed partial database copies are retained for this new case. They
do not replace the absent older historical partial files.

A separate cold import probe observes Ackredit absent after host imports, query
planning and prepared-file reading, then loaded by MolSysMT's actual recognition
attribution boundary. PHMT's default capture adds no top-level native attribution
field; it does not globally govern nested providers. MolSysMT retains its own
bibliography and provider behavior. The public activation/session clarification
request is [MolSysMT#292](https://github.com/uibcdf/molsysmt/issues/292#issuecomment-6703588216).
No provider flag, private implementation, optional dependency or session policy is
patched or suppressed. This observation establishes no scientific-result defect.

## Actual receiving scope

Package/runtime Python files and the MolSysMT native binary remain unchanged.
The same owned wheel, SHA-256
`df36ba5e2d8e726813d4ce16ae36ce9738ad897a3f25eb3a7f81f7b8c71aa6db`,
is used without rebuilding; 208 installed wheel payload files are reverified.
Installed recipe imports both PHMT namespaces from the owned `/tmp` target and
runs outside the checkout, with the same recorded scientific source providers.
This is bounded Linux/Python3.14 receiving, not a new PHMT artifact, complete
public dependency installation, supported platform matrix or release gate.

Heavy runs are serial: CPU 19/quota 100%, one backend thread, nice 19/idle I/O,
512 MiB/no swap/tasks 32 with pressure checks. Measured successful peaks:
231,198,720 bytes for the expert continuation, 231,829,504 for revised source,
231,448,576 for installed. No OOM/max events. The first failed harness did not
capture its terminal peak; no replacement value is invented. These observations
are not throughput or memory-efficiency benchmarks.

Whole original input/native/legacy-file identities remain unchanged. Full
query/database/native/attribution bodies stay local in
`build/phmt-guided-expert-20261107-ipd_7x6x`; only own controls/scalar/hash evidence
is archived. Repeated routes, the diagnostic probe and the same three artifacts
are not new independent compounds or extra distinct scientific tests.

The recipe correction uses existing public operations and adds no API, runtime,
dependency, schema or scoring change. Human usability, broader source operations,
MolSysMT#624 collections, both biological studies and representative scale remain
open. Next deliver public complete-view JSONL/scalar-CSV export so routine users
can reuse the existing result semantics without recreating their field projection.
