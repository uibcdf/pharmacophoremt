# ERα training gate: a retained unavailable-input outcome

Case `esr1-consensus-training-20261024-01`, owned by
[#64](https://github.com/uibcdf/pharmacophoremt/issues/64), maintainers `LMMV`
and `dprada`. Evidence class: scientific input/preparation readiness control.
**The declared attempt stops before consensus:** one of its three fixed
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
