# ERα signaling: a frozen ligand-reference activity pilot

Case ID `esr1ago-reference-20261023-01`, measured 2026-10-23 under
[#62](https://github.com/uibcdf/pharmacophoremt/issues/62). Scientific owners:
PharmacophoreMT maintainers `LMMV` and `dprada`. Evidence class: exploratory
retrospective screening with experimentally assigned assay outcomes.

This case asks whether a fixed native reference pharmacophore discriminates
held-out active and inactive assay compounds when each has one supplied computed
conformer. **The result is weak:** evaluated-subset ROC AUC 0.5614. It establishes
an executed activity-labeled workflow and its failure accounting; it does not
establish a validated activity predictor, binding affinity or prospective utility.

## Original data, split and preparation

The [Bath dataset](https://doi.org/10.15125/BATH-01496), by James Proudfoot,
Toby Lewis-Atwell and Matt Grayson (2026), provides the ESR1ago table under
[CC BY-SA 4.0](https://researchdata.bath.ac.uk/1496/). The selected, attributed
labels are adapted by the filtering/split below; they retain that source license.
Its 4410 rows contain 12 active and 4398 inactive substance records. This table
is a derivative population, not the original complete
[LIT-PCBA benchmark](https://doi.org/10.1021/acs.jcim.0c00155).

Selected SID, CID and outcome are independently checked against original
[PubChem AID 743075](https://pubchem.ncbi.nlm.nih.gov/bioassay/743075), version 2.
The endpoint is a cellular ERα signaling agonist reporter assay. These labels
are experimental assay outcomes, not demonstrated direct receptor binding.
Neither docking scores nor the table's processed/imputed potency fields are used.

The [frozen manifest](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/esr1_activity_pilot/manifest.json)
records acquisition, URLs, hashes, the original conflicting rows and all 32
selected inputs. Before any scores, four CIDs with opposite outcomes in different
substances were excluded: 2662, 5361202, 6128 and 17113. Remaining unique CIDs
are ordered by SHA-256 of `phmt-esr1ago-pilot-v1:<CID>`. The first active,
CID 9821849, is the sole reference. Seven other actives and the first 24
inactives are held out, without replacement after any failure. Exact CID overlap
is excluded; chemical-series/near-analog independence is **not established**.

Structures are single published PubChem computed 3D SDF records, acquired with
`record_type=3d`; they are not experimental bound conformations. Supplied
hydrogens, chemical state and stereo declarations are retained without pH
adjustment or conformer generation. Public MolSysMT reads SDF with explicit
`stereo_engine='rdkit'`, then converts through its sanitizing `rdkit.Mol` route
back to `molsysmt.MolSys`. No consumer-side molecular parser, state inference,
stereo repair, conformer generation or coordinate transformation is introduced.

For each successfully prepared system, the archive retains chemical-state
payloads, atom/bond counts, feature inventories and checks on unchanged original
bytes/state/coordinates, preserved atom IDs/elements/charge/stereo and coordinate
RMSD below 1e-12 nm. These are input-preservation controls, not independent proof
of the biological chemical state. Five selected CIDs return PubChem HTTP 404;
MolSysMT rejects CID 6842999's unsupported stereo interpretation. All remain
recorded, unscored inputs.

Raw SDF and source archives are retained in the owned acquisition directory,
outside this repository. The [NCBI molecular-data policy](https://www.ncbi.nlm.nih.gov/home/about/policies/#data)
places no additional NCBI restrictions while retaining possible submitter rights;
this case does not assert that every PubChem field has a blanket public-domain
license. Only URLs/hashes, attributed selected labels and measured outputs are
published here. Strict reacquisition checks exact hashes and refuses changed
upstream bytes; if responses refresh, replay requires the retained originals.
Portable long-term input archival remains a follow-up in #62.

## Method and executable record

The pre-score protocol and driver are committed at
`ee064102f3701a280297e01ec0c549207f10bfd3`. The
[opt-in driver](https://github.com/uibcdf/pharmacophoremt/blob/ee064102f3701a280297e01ec0c549207f10bfd3/phmt_test_support/esr1_activity_pilot.py)
uses the installed public PharmacophoreMT **0.4.0** and MolSysMT **0.23.0**,
on Linux/Python **3.14.9**. Its clean producer identity, driver hash, runtime
origins, Python/provider versions, native extension hash and 311 Conda records
are retained in the full result. This is local scientific evidence, not a new
release or qualification of newer MolSysMT development APIs.

```bash
# Create an owned environment using the ordinary public channel route:
mamba create -p /tmp/phmt-esr1-env -c uibcdf -c conda-forge \
  --strict-channel-priority python=3.14 pharmacophoremt=0.4.0 \
  molsysmt=0.23.0 ackredit beartype pip

# Reacquire only exact frozen inputs; upstream changes fail closed.
python phmt_test_support/esr1_activity_pilot.py \
  --data-dir /tmp/phmt-esr1-inputs --restore

# Execute by file path so installed runtime packages take precedence.
/tmp/phmt-esr1-env/bin/python phmt_test_support/esr1_activity_pilot.py \
  --data-dir /tmp/phmt-esr1-inputs --output /tmp/phmt-esr1-run.json
```

The reference requests donors, acceptors and aromatic sites. Its actual inventory
emits **two acceptors and one aromatic site**, all essential and weight one,
radius 0.15 nm. Thus this run does not test a donor-bearing query. Native
`RigidPoseSearch` uses 10000 raw trials, 0.10 nm point tolerance, 30-degree
direction tolerance and minimum fit zero. There is no held-out parameter tuning.
The saved query precedes held-out scoring; its reference self-fit is 1.
All 25 evaluable triplet enumerations complete, with at most 256 raw trials.
That does not guarantee exhaustive continuous-pose or conformational coverage.

## Measured outcomes and limits

| Accounting or metric | Original result |
| --- | ---: |
| Selected held-out active / inactive | 7 / 24 |
| Evaluated active / inactive | 6 / 19 |
| Unscored active / inactive | 1 / 5 |
| Active hits / inactive hits | 1 / 0 |
| Evaluated scores tied at zero | 23 of 25 |
| ROC AUC, evaluated subset | 0.5614035088 |
| BEDROC, alpha 20, evaluated subset | 0.5994951770 |
| Tie-aware EF at 10%, evaluated subset | 1.6908212560 |

The hit is CID 24964624; inactive CID 135430996 has partial fit 2/3 without
satisfying all essential sites. Other evaluable inputs score zero. EF uses three
top positions (`ceil(0.10 * 25)`) and fractional credit across the large boundary
tie. It is not full-library enrichment at the original assay prevalence.

The six failures never receive zero scores or inactive labels. Their original
preparation causes remain in the record; the native batch explicitly evaluates
unavailable-file placeholders for those inputs, so its failure list must be read
alongside preparation records. No search-budget failure occurred. Conditional
metrics exclude the six failures and do not characterize those missing outcomes.

An independent pairwise calculation bounds AUC at **0.4494–0.6280** if every
unscored active/inactive is hypothetically given the least/most favorable bounded
score. These are missing-score sensitivity scenarios, not imputed observations
or confidence intervals. Small deterministic sampling, unqualified series overlap,
one conformer and extensive ties prevent a general predictive claim. Population
uncertainty and runtime/memory comparisons are not measured.

**Subsequent qualification, 2026-10-23:** a separate analytical source control in
[#63](https://github.com/uibcdf/pharmacophoremt/issues/63) confirms that a completed
negative's partial coverage can change under a rigid translation of the same
molecule when no triplet placement is fitted (1/3 to zero in the control). This
is not a rerun of the public-runtime assay case. The original metrics above are
preserved as outputs of the declared method; they must not be interpreted as
ranking with a demonstrated frame-independent partial-match score. That local
scoring contract is the next MVP task before expanding discrimination claims.

## Original outputs and maintenance

The [summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/esr1_activity_pilot_20261023_summary.json)
qualifies the [full original result](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/esr1_activity_pilot_20261023.json.gz),
saved query, preparation journal and execution log by compressed/raw SHA-256 and
byte count. The full result's decompressed SHA-256 is
`954550324a1f9fd805e2aa4e6eb919ab7a855e2628d4ff8f96019c04b997b145`.
The actual enclosing Ackredit capture retains 42 items and 72 uses, including
input data and reached software/methods; native result payloads also retain
their attribution. The LIT-PCBA literature reference above describes dataset
lineage and is separate from executed-method credit.

The [offline guards](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/tests/test_esr1_activity_pilot.py)
check split ambiguity/leakage, original archive/query/runtime identities,
preparation preservation, all denominators and independent pairwise AUC/tie-aware
EF arithmetic. Archive checks execute no molecular workload. Scientific changes
require a new opt-in run identity; preserve these outputs and declared failures.

Next: resolve portable original-input retention, receive provider-owned conformer
and stereo capabilities, and declare the next training/evaluation comparison
before measuring it. Retrospective reuse of these observed outcomes is development
evidence, not a fresh independent validation set. Receptor refinement #323 and
newer-provider #375 receiving remain separate; no viewer addon is required here.
