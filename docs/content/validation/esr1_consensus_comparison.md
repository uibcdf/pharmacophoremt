# ERα frozen consensus and paired evaluation

The completed paired comparison scores the same 45 available/prepared compounds
from 64 fixed evaluation inputs. Consensus AUC is **0.5530**, versus **0.4848**
for the original reference query; the descriptive difference is **+0.0682**.
Nineteen inputs lack the requested PubChem 3D record and remain unscored. This
is a modest observed subset difference in one selected cellular-assay cohort,
not predictive qualification or an independent chemical-series benchmark.

The measured phases below preserve the original stop, separate ready-training
attempt and final evaluation without rewriting their inputs or outcomes.

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
At that training checkpoint the owned environment was retained for the pending
phase; no retirement hooks or shared-cache cleanup ran. This readiness stage has
no ROC AUC, enrichment or predictive-performance result.

## Completed paired evaluation — 2026-10-24

Case `esr1-consensus-paired-20261024-01` uses the exact 64 evaluation entries
and both already committed query hashes. Clean execution producer is
`012544472e8eca27d1646a6e8065ee22872d4368`. The PHMT library and MolSysMT file
hashes match qualified training exactly; the library metadata remains
`0.4.0+17.g25a49f5`, while the new case driver has its own recorded identity.
The unchanged 325-provider environment uses Linux/Python 3.14.9, MolSysMT 0.23.0
and PyUnitWizard 0.29.0. Original data/query/state/source identities remain stable.

All 64 CIDs receive one acquisition attempt: 45 SDFs are available and 19
requests return HTTP 404 (4 of 16 actives / 15 of 48 inactives). All 45 available
systems pass the same MolSysMT preparation/preservation checks, so both arms
score the **same 12 actives and 33 inactives**. No molecular preparation or
native search fails. Read-only public MolSysMT observations confirm unchanged
coordinates, chemical states, atom IDs and elements before/between/after arms.

| Metric or accounting | Original reference | Frozen consensus |
| --- | ---: | ---: |
| Original evaluation inputs | 64 | 64 |
| Evaluated active / inactive | 12 / 33 | 12 / 33 |
| Unscored active / inactive | 4 / 15 | 4 / 15 |
| Active / inactive geometric hits | 0 / 1 | 2 / 2 |
| AUC on common 45-input subset | 0.4848484848 | 0.5530303030 |
| BEDROC, alpha 20 | 0.1757153729 | 0.4589315704 |
| Tie-aware EF at 10% | 0.8181818182 | 1.6829268293 |
| Hypothetical missing-binary-score AUC range, all 64 | 0.3333–0.6146 | 0.3854–0.6667 |

The primary descriptive AUC difference is **0.0681818182**, calculated on the
common-evaluable subset without another molecular search. Reference has one
inactive hit (CID 33255) and 44 zero ties. Consensus hits two assay actives
(87250, 5280961) and two assay inactives (70425, 11193251), with 41 zero ties.
At the top-five cutoff, boundary ties share fractional selection credit;
enrichment is not computed by choosing a favorable tie ordering.

The 19 missing inputs are never assigned observed negative scores or fabricated
native failures. Their original acquisition causes remain in the full 64-input
ledger. Native `RetrospectiveValidator` counts/indices refer to its prepared
45-input batch; an explicit mapping preserves original study indices and class
counts. Hypothetical binary 0/1 extremes yield sensitivity bounds on the full
cohort. Those values are neither imputed observations nor confidence intervals.

The positive difference is exploratory. Only 12 actives were scored, many
results tie, 19 requested structures are unavailable, supplied states/one
computed conformer are assumed, the endpoint is a cellular reporter rather than
direct binding, and chemical-series independence remains unqualified. This
single selected comparison does not establish predictive improvement. All 64
outcomes are now exposed; future query/model changes need fresh declared
evaluation data instead of retuning and reusing this cohort as unseen.

### Original outputs and checks

The [paired summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/esr1_paired_evaluation_20261024_summary.json)
qualifies the full original output, preparation journal, both complete arm
journals, execution/acquisition logs, qualification and cleanup records. Full
output decompressed SHA-256 is
`610b418d88707132d40b4ef5fd534a04498c1389f8b73c5e1ca1d4db39c1d1f9`.
[All original inputs and notice](https://github.com/uibcdf/pharmacophoremt/tree/main/tests/data/esr1_consensus_comparison/paired_evaluation_20261024)
retain the 45 SDFs, 19 error bodies, acquisition receipt and exact query input
copies. Actual enclosing Ackredit contains 60 items and 89 uses from the reached
data/preparation/search/retrospective/metric branches. Saved reading registers
no new scientific use.

The offline guard independently checks pairwise AUC, boundary-tie EF and
exponential-rank BEDROC, both missing-score scenarios, source/native/original
index mapping, all failures, query hashes and before/after input integrity.
The public-provider selection additionally passes 103 scientific controls;
312 historical MolSysMT Pandas warnings are retained in its log. These do not
qualify a new complete hosted matrix, installed artifact or timing benchmark.

The owned environment is retired after evidence capture and verification,
removing only the verified task-created prefix through scoped filesystem
cleanup. No uninstall hooks, shared-environment repair or global cache cleanup
run. [MolSysSuite #139](https://github.com/uibcdf/molsyssuite/issues/139) remains
the separate investigation of the earlier native unlink-hook attempt.

### Replaying the recorded science

Read the archived result with the existing checksum reader for integrity-only
inspection. A new calculation keeps the exact 325-provider file and installs
the **training library producer** separately from the **evaluation driver**;
the driver refuses changed product/provider files before scoring.

```bash
mamba create -p /tmp/esr1-paired-env \
  --file devguide/evidence/seeded_ranking_environment_20261024_explicit.txt
git worktree add --detach /tmp/esr1-library-source 25a49f5322a06c1deeff95b396cf194fc5d8f9b6
git worktree add --detach /tmp/esr1-evaluation-source 012544472e8eca27d1646a6e8065ee22872d4368
/tmp/esr1-paired-env/bin/python -m pip install --no-deps --editable /tmp/esr1-library-source
python -c "import shutil; shutil.copytree('tests/data/esr1_consensus_comparison/paired_evaluation_20261024', '/tmp/esr1-paired-inputs')"
/tmp/esr1-paired-env/bin/python -I /tmp/esr1-evaluation-source/phmt_test_support/esr1_consensus_evaluation.py \
  --data-dir /tmp/esr1-paired-inputs --output /tmp/esr1-paired-new-run.json
```

Use new paths, preserve original outputs and record a distinct new run identity.
Installation/native-byte differences fail the historical qualification check;
do not bypass it or call current-head execution the original producer. No source
reacquisition or molecular workflow runs when merely reading these archives.

### Derive new summaries without repeating the molecular experiment

The reusable native [saved-result tools](../../api/saved_results.md) now provide
original-cohort accounting and common-scored-subset comparison. A separate
[derived verification](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/esr1_saved_summary_replay_20261024_summary.json)
from clean implementation `e32c80e0cbc9837e8badcda2b7c93f22d30f1ddc` reproduces
all original 64/45/19 counts, native/original mappings, scores, metrics and binary
missing-score sensitivity using only the saved evidence. The original #64
scientific result retains its own producer and attribution. New summary/metric
attribution records only operations actually recomputed; no molecular preparation,
recognition, fitting or source acquisition is repeated.

```bash
python -m phmt_test_support.replay_esr1_saved_results --output /tmp/esr1-new-derived-summary.json
```

Use an unused output path and the qualified implementation checkout. This new
result provides API-consumer verification, not new activity observations or
stronger biological acceptance.
