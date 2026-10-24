# ERα training gates and a frozen consensus query

Case `esr1-consensus-training-20261024-01`, owned by
[#64](https://github.com/uibcdf/pharmacophoremt/issues/64), maintainers `LMMV`
and `dprada`. Evidence class: scientific input/preparation readiness control.
**The original declared attempt stops before consensus:** one of its three fixed
training compounds has no record at the requested PubChem 3D endpoint.
No comparison of activity discrimination was executed.

## Question, inputs and separation

The [frozen declaration](https://github.com/uibcdf/pharmacophoremt/blob/d53654fad6a448105f26d344f6c99bc306988e23/tests/data/esr1_consensus_comparison/declaration.json)
compares the unchanged original [pilot query](esr1_activity_pilot.md) against one
native rigid consensus learned from three new actives. It was committed before
new structure acquisition or scoring. The
[protocol](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/esr1_consensus_comparison.md)
fixes the source population, selection, native methods, finite budgets,
training-only model choice and stop rules.

Labels come from the original archived PubChem AID 743075 v2 U.S. Tox21 ERα
signaling assay. Exclude the entire prior Bath table's 4,402 CIDs and every
assay CID with contradictory outcomes, including inconclusive. Hash ordering
and lowest-SID representatives select three training actives (31477, 24633,
6293), plus 16 other actives and 48 inactives reserved for evaluation. No
replacement is permitted after failures. These are different external CIDs
from the same assay; molecular/chemical-series independence is unqualified.
Reusable molecular overlap analysis is proposed in
[MolSysMT #447](https://github.com/uibcdf/molsysmt/issues/447).

Only the three training `record_type=3d` PubChem responses were requested.
The exact originals, including the HTTP error, are retained with their
[acquisition receipt and notice](https://github.com/uibcdf/pharmacophoremt/tree/main/tests/data/esr1_consensus_comparison/training_20261024).
They are computed conformers in their supplied state, not experimental bound
poses. The scoped notice credits NCBI/PubChem and the original U.S. Tox21 assay,
preserves the NCBI contributor-rights limitation and does not infer a uniform
license for all PubChem contributions. No molecular repair, conformer generation,
state adjustment or substitute input is introduced.

## Measured preparation and stop

| Training CID | Acquisition | MolSysMT preparation | Atoms / bonds / frames | Donor / acceptor / aromatic features |
| --- | --- | --- | --- | --- |
| 31477 | Computed 3D SDF | Completed | 49 / 49 / 1 | 2 / 5 / 1 |
| 24633 | HTTP 404 `PUGREST.NotFound` | Unavailable input; not attempted | — | — |
| 6293 | Computed 3D SDF | Completed | 26 / 28 / 1 | 2 / 4 / 2 |

Public MolSysMT 0.23.0 reads each available SDF with explicit
`stereo_engine='rdkit'` and `discard_properties=True`, then converts through
`rdkit.Mol` back to `molsysmt.MolSys`. For both available systems, the original
bytes/state/coordinates remain unchanged; atom IDs, elements, charge, unpaired
electrons and stereo are preserved; coordinate RMSD is below 1e-12 nm.
All molecular reading/conversion/coordinate operations belong to MolSysMT.
The case driver only composes those operations and records preservation checks.

The original 82-byte response for CID 24633 says no records were found for the
requested CID. It does not establish molecular inactivity, a MolSysMT defect
or an unsuccessful consensus algorithm. The run represents this as a failed
preparation prerequisite caused by frozen acquisition failure, not a provider
stereo/read rejection. The predeclared rule requires all three training inputs.

The retained outcome is `status='stopped'`, `stage='preparation'`,
`evaluation_opened=False`. **Consensus calls, new queries and held-out
scores are all zero.** No readiness search is executed. All 64 reserved
evaluation compounds remain without acquired structures or computed scores;
there are no AUC, enrichment or paired-comparison metrics. Missing inputs are
not assigned negative scores.

## Executable record and provenance

The clean acquisition/training producer is
[`5242ca63eb239aaecb95ae782304dbeca7b53135`](https://github.com/uibcdf/pharmacophoremt/commit/5242ca63eb239aaecb95ae782304dbeca7b53135).
The [standalone driver](https://github.com/uibcdf/pharmacophoremt/blob/5242ca63eb239aaecb95ae782304dbeca7b53135/phmt_test_support/esr1_consensus_training.py)
has no evaluation acquisition/scoring mode. It verifies the original declaration
and all acquisition bytes, refuses output overwrite and retains stop outcomes.
The source/runtime audit remains stable through the run.

Execution uses Linux/Python 3.14.9, public MolSysMT 0.23.0, PyUnitWizard 0.29.0,
RDKit 2026.9.1, NumPy 2.5.4 and actual editable PHMT
`0.4.0+13.g5242ca6`. The full record retains package origins, source/native hashes
and 325 Conda records. The base PHMT 0.4.0 package record is overwritten by this
editable producer; this is not a new public package. The
[explicit provider environment](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/seeded_ranking_environment_20261024_explicit.txt)
and recorded source reproduce the provider route. The owned temporary environment
is retired after evidence capture. An OpenCL unlink hook attempted an active
shared-prefix path; the target was absent and deletion failed. The original
cleanup log is retained and the shared-tooling investigation is
[MolSysSuite #139](https://github.com/uibcdf/molsyssuite/issues/139); no shared
repair or global-cache cleanup was attempted.

The [summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/esr1_consensus_training_20261024_summary.json)
qualifies the original full output, execution/acquisition logs, native environment
creation and qualification receipt. The decompressed full output SHA-256 is
`98f8320431c0b12397729f69034623cc80b41c8ca973e76915d79605443c6df6`.
The actual Ackredit payload retains 12 items and 14 uses from reached
data/preparation/software branches; no unexecuted consensus, rigid-fit or
screening algorithm is credited. Reading this archive does not register new use.

The qualification receipt retains 51 passing rigid-consensus/scoring controls
and their 232 historical public MolSysMT Pandas warnings, plus a control showing
that the shared preparation orchestration reproduces the already exposed
original reference's archived states/counts/features/RMSD. That reference is
not a fourth training ligand. These checks do not qualify a new full hosted
matrix or establish biological performance. This is not a timing benchmark.

The [offline guards](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/tests/test_esr1_consensus_training.py)
protect input identity, three-only acquisition, fixed model selection and this
archived stop without importing molecular providers. A future method/provider
change requires a distinct measured run; preserve this outcome and its original
HTTP response. A later attempt needs a separately declared training-readiness
policy before acquiring new candidates; it cannot silently replace CID 24633
or open this evaluation set under the stopped declaration.

## Attempt 2: bounded readiness and a frozen query

Case `esr1-consensus-training-20261024-02` is a distinct, predeclared attempt,
not a replacement of the original stop. The
[second declaration](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/esr1_consensus_comparison/readiness_declaration.json)
fixes 12 training candidates before new acquisition, preserving all original
evaluation records, baseline query, preparation, consensus/scoring parameters
and model choice. Its SHA-256 is
`b8ff6305ed7527289dad6ee13f7992b74928d93738c6f290fbdeff4099b1757e`.
All three original responses, including the known 404, are reused unchanged;
only nine further fixed training URLs are requested. These known training
observations are development data, not fresh validation.

Eligibility requires completed acquisition and successful public MolSysMT
preparation/preservation/feature extraction, without thresholds on feature count,
geometry, support or score. All candidates are retained. The first three
successful preparations, in fixed order, become the only consensus inputs;
failure cannot trigger another trio, pivot, model or budget.

| Training-stage accounting | Result |
| --- | ---: |
| Fixed candidates | 12 |
| Original responses reused / new requests | 3 / 9 |
| Available SDFs / preserved HTTP 404 responses | 8 / 4 |
| Successful MolSysMT preparations / molecular preparation rejections | 8 / 0 |
| Selected training ligands | 3 |
| Native fits / placement layouts | 146 / 2 |
| Consensus hypotheses | 3 |
| Selected query sites / jointly supporting ligands | 3 / 2 |
| Evaluation structures acquired / compounds scored | 0 / 0 |

The selected trio is **31477, 6293, 9818306**, with pivot 31477. All eight
available SDFs pass the same state/atom/stereo/coordinate preservation controls.
Unavailable CIDs are 24633, 17701, 6327657 and 70400; none is replaced outside
the pool or assigned a negative score. Native consensus completes its declared
finite family and retains three alternatives. All have three sites and joint
support two; the declared identifier tie-break chooses model 0,
`layout_00000 / hypothesis_00000`, supported by 31477 and 9818306.

The frozen query contains **two acceptors and one aromatic site**, all essential
with weight one and radius 0.15 nm. Training-only seed-hit readiness scores are
1 for 31477, 0 for 6293 and 1 for 9818306. The second training ligand has no
accepted direct placement to the pivot within this finite proposal family;
its source inventory is retained and it remains in the three-input support
denominator. Its zero score is not assay inactivity: all three are training
actives. There is no alternate model/trio selection based on those scores.

The outcome is `ready`, `training_complete`, `evaluation_opened=False`.
This qualifies a usable frozen training query, not biological discrimination.
The [new summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/esr1_consensus_readiness_training_20261024_summary.json)
qualifies full original output, query, logs, environment creation and test
receipt, with all actual 26 Ackredit items / 86 uses. Clean producer
`25a49f5322a06c1deeff95b396cf194fc5d8f9b6` remains stable through execution.
Linux/Python 3.14.9 uses the same 325 public provider records, MolSysMT 0.23.0,
PyUnitWizard 0.29.0 and actual editable PHMT `0.4.0+17.g25a49f5`.
No new package/release or independent biological validation is implied.

The saved query's raw SHA-256 is
`f80a09a68e21a8826a399467bb449082765e10328c8480717811049aa1d93a6d`;
the full training output's is
`608b0f41f7ee181785cccbfcde65bf758e7dd056b0b179815d4991028144d8f6`.
The [original pool responses and notice](https://github.com/uibcdf/pharmacophoremt/tree/main/tests/data/esr1_consensus_comparison/readiness_training_20261024)
retain every success and failure. The offline guard independently reconstructs
candidate eligibility/model ordering, verifies original response/query identities
and preserves zero evaluation counts without rerunning molecular science.

Next is the separately recorded paired evaluation on the unchanged 64 reserved
inputs, after this query/training receipt is committed. Use the checksum reader
to restore both original baseline and new consensus query; native PHMT loads
them. Retain all evaluation failures and per-arm/common-subset denominators.
The owned environment remains available for that pending phase; no retirement
hooks or shared-cache cleanup run in this closeout. This readiness stage has
no ROC AUC, enrichment or predictive-performance result.
