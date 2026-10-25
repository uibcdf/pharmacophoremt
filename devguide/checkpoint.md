# Development Checkpoint

## Native saved-result reporting complete — 2026-10-24

**#65's local API and real-consumer criteria are complete.** Implementation
`e32c80e0cbc9837e8badcda2b7c93f22d30f1ddc` is pushed to main. Public
`validation.summarize_screening_results` and `compare_screening_results` compose
existing score/metric tools, retain all original indices/classes/unscored causes
and recompute paired metrics on exactly the common scored subset. No molecular
operation moves into PHMT. The [API](../docs/api/saved_results.md),
[recipe](../docs/content/cookbook/retrospective_validation.md) and
[resolved owner report](archive/native_retrospective_result_summaries.md) document
the reusable contracts, ambiguous-input rejection and attribution separation.

A new clean-head consumer reads the immutable #64 archive and reproduces all
64/45/19 counts, original mappings, native scores, arm metrics, common AUC delta
and binary missing-score sensitivity. The
[derived summary](evidence/esr1_saved_summary_replay_20261024_summary.json) qualifies
the new result, raw SHA-256
`d8104d4019c908dfd01345158e7440880d2a26c3e356662248b5322196005da4`.
Original query/input/search outputs, producer and source attribution are retained
unchanged. New attribution records only the newly reached summary/scoring/metric
operations. The old case-specific ledger remains solely for historical replay;
new statistical consumers use the public tool.

Canonical Python 3.14.7 passes 84 selected scientific tests; the final complete
administrative run passes 50 tests plus 26 subtests, including strict Sphinx and
the new replay archive guard. Three reporting tests, indexes, Ruff and whitespace
checks pass. The replay
records current editable provider versions/origins separately from the original
scientific providers. No extra environment, molecular experiment, complete new
hosted/installed matrix or public package/release is claimed.

**Next:** inspect exact implementation/final-head CI through #9; implementation
CI 40147016165 is queued, policy 40147016265 / Conda governance 40147016227
succeed at this observation. Older fc9f14b CI 40145759546 remains in progress.
Keep public-delivery/installed receiving separate. Before stronger biological
claims, review endpoint and fresh data suitability and predeclare an unexposed
evaluation set; these 64 outcomes cannot be reused as unseen validation after
tuning. Receive molecular identity/scaffold/conformer/state tools through #41
and their provider issues, without local replacements. Addon, broader release
infrastructure and a new release remain deferred.

## Native saved-result summaries implemented; clean receipt pending — 2026-10-24

#65 now has public `validation.summarize_screening_results` and
`validation.compare_screening_results`, documented in the
[API](../docs/api/saved_results.md) and
[recipe](../docs/content/cookbook/retrospective_validation.md).
They compose the existing native score reader and metrics with explicit original
cohort, index mapping and upstream causes. Native evaluation failures retain
their own cause/evidence; unavailable inputs never become negatives. Repeated
source IDs remain distinct original samples. New metric attribution stays
separate from immutable source attribution. No molecular-provider code changes.

Local canonical Python 3.14.7: 84 saved-result/metric tests pass, including real
Ackredit and optional-provider controls; 49 administrative/documentation tests
plus 24 subtests pass, including strict Sphinx. Three reporting tests, generated
indexes, whole-tree Ruff and whitespace checks pass. A preliminary derived replay
of #64 reproduces all counts, scores, original mappings, metrics and missing-score
sensitivity. Permanent clean-producer receipt is still pending. No full source
matrix, installed/public package or new molecular experiment is claimed.

**Immediate next action:** commit this implementation, execute
`python -m phmt_test_support.replay_esr1_saved_results --output /new/path.json`
from that clean head, retain its new derived evidence separately, then finish
#65's owning report/issue. Historical #64 results/drivers remain unchanged.
Follow #9 for the implementation head's hosted receiving. No extra environment
has been created; public 0.4.0 and its MolSysSuite notice remain unchanged.

## Paired comparison complete; next native reporting segment — 2026-10-24

**#64 is complete as a bounded exploratory comparison.** Clean producer
`012544472e8eca27d1646a6e8065ee22872d4368` uses both committed queries and all
64 unchanged evaluation inputs, without new training, parameter changes or
replacement. 45 SDFs are available and all pass public MolSysMT preparation;
19 HTTP 404 responses remain unscored (4 active / 15 inactive). Both arms
score the same 45 prepared systems: 12 actives / 33 inactives, no search failures.

| Common-subset result | Reference | Consensus |
| --- | ---: | ---: |
| AUC | 0.4848484848 | 0.5530303030 |
| BEDROC, alpha 20 | 0.1757153729 | 0.4589315704 |
| Tie-aware EF10% | 0.8181818182 | 1.6829268293 |
| Active / inactive geometric hits | 0 / 1 | 2 / 2 |

Descriptive AUC difference is +0.0681818182 on those same 45 inputs. Missing-
binary-score hypothetical full-cohort AUC ranges are 0.3333–0.6146 and
0.3854–0.6667, not imputed observations or confidence intervals. The observed
difference is modest; 12 scored actives, ties, unavailable structures, supplied
single conformers/states, a cellular rather than direct-binding endpoint and
unqualified chemical-series independence prevent predictive acceptance. These
64 outcomes are now exposed development evidence for any further method tuning.

The [paired summary](evidence/esr1_paired_evaluation_20261024_summary.json)
qualifies full original output (raw SHA-256
`610b418d88707132d40b4ef5fd534a04498c1389f8b73c5e1ca1d4db39c1d1f9`),
preparation and both-arm journals, acquisition/execution logs and qualification/
cleanup records. All 64 original responses, exact query input copies and receipt
are portable under `tests/data/esr1_consensus_comparison/paired_evaluation_20261024/`.
Original training declarations/stops/ready query and earlier #62/#63 outputs
remain unchanged. The [case](../docs/content/validation/esr1_consensus_comparison.md)
and [resolved owner report](archive/esr1_consensus_comparison.md) explain the full
ledger versus native prepared-batch index mapping and all failure denominators.

Actual library/provider files match qualified training exactly; before/after
producer audit and public MolSysMT state/coordinate/atom integrity checks pass.
The unchanged library metadata remains `0.4.0+17.g25a49f5`; the evaluation driver
has its separately committed source identity. Linux/Python 3.14.9 retains all
325 Conda records, MolSysMT 0.23.0 and PyUnitWizard 0.29.0. Actual Ackredit:
60 items / 89 uses. Independent pairwise AUC, boundary-tie EF and exponential-
rank BEDROC oracles confirm both arms/common subset and missing-score scenarios.
All 103 selected scientific controls pass with 312 historical public MolSysMT
warnings retained. No new full hosted/installed matrix, public package or timing
benchmark is claimed; native receiving remains #9.
Closeout passes 49 administrative/documentation tests plus 24 subtests, including
strict Sphinx and the independent paired-result oracle, plus three reporting
tests, whole-tree Ruff, generated-index and whitespace checks.

The environment previously retained at
`/tmp/phmt64-readiness-20261024-4ceLcb/environment` is now retired after evidence
verification. Its creation prefix and 325 records were checked before scoped
filesystem removal of only that task-owned directory; no uninstall hooks,
shared-environment target/repair or global-cache cleanup runs. The earlier native
hook investigation remains MolSysSuite #139. Raw inputs/results/logs remain in
the owned training and `/tmp/phmt64-paired-20261024-qKYX7C` roots and permanent
archives. Recreate the recorded providers/library/driver separately for a new
historical replay, as documented; archive reading needs no molecular execution.

Previously pending training head `30de2b9bdce57658d445ec53265fd0144ae4afe3`
now has CI 40142394506 reporting/all eight scientific jobs and their actual
test steps successful; policy 40142394713 and Conda governance 40142394824
succeed. This does not qualify the new evaluation/archive head. Follow #9 for
its own native receiving and Documentation when available.

**Next concrete product work: [#65](https://github.com/uibcdf/pharmacophoremt/issues/65).**
Review and expose reusable native retrospective summaries of saved evaluations
with an explicit original cohort, upstream unscored causes and native/original
index mapping. Compose existing score/metric tools and common-subset comparison
without rerunning molecular search; preserve actual producer attribution. This
belongs in PHMT validation and needs no MolSysMT implementation change. #64's
case-only ledger is an explicitly tracked interim consumer; owners LMMV/dprada,
review 2026-11-07, migrate future consumers when the public contract is qualified
while retaining immutable historical driver commits.

Further biological claims require a newly declared unexposed evaluation set.
MolSysMT owns identity/scaffold (#447), conformer/state/stereo and general
preparation capabilities; receive them through #41 rather than filling gaps
here. Addon, broader docs/release infrastructure and a new public release stay
deferred; delivered public 0.4.0 and its original notice are unchanged.

## Consensus query ready; evaluation unopened — 2026-10-24

**#64 attempt 2 has a usable frozen training query.** Clean producer
`25a49f5322a06c1deeff95b396cf194fc5d8f9b6` executes the separate 12-candidate
readiness declaration, reusing all three original responses and making only
nine new requests. Eight SDFs are available; all eight prepare and pass every
MolSysMT preservation check. Four original 404 responses are retained.
The fixed first-success rule selects **31477, 6293, 9818306**, pivot 31477.
All candidate outcomes remain recorded; no score/feature-count filtering occurs.

Native consensus completes 146 fits, two layouts and three hypotheses. The
declared model ordering selects model 0, `layout_00000 / hypothesis_00000`:
two acceptors and one aromatic site, jointly supported by 31477/9818306.
All sites are essential with weight one and radius 0.15 nm. Training-only
seed-hit readiness scores are 1, 0, 1. The zero-scoring active 6293 is unplaced
to the pivot within this finite proposal family; it is not erased from source
evidence or the three-input denominator. No alternate trio/pivot/model is tried.

The outcome is `ready`, `training_complete`, **evaluation unopened**. No structure
or score from the 64 reserved inputs is acquired/computed. Original attempt 1
and all #62/#63 outputs remain intact. This is training readiness, not biological
discrimination, affinity or predictive acceptance.

Use the existing checksum reader to restore the two frozen query archives:

- Baseline: `evidence/esr1_activity_pilot_20261023_summary.json`,
  `saved_query_archive`, raw SHA-256
  `c165f3755e1a76603a69f7fd1c24259e8f4706c20407eb3fdf653a4b5f7804f3`.
- Consensus: `evidence/esr1_consensus_readiness_training_20261024_summary.json`,
  `saved_query_archive`, raw SHA-256
  `f80a09a68e21a8826a399467bb449082765e10328c8480717811049aa1d93a6d`.

The [new summary](evidence/esr1_consensus_readiness_training_20261024_summary.json)
qualifies original full output (raw SHA-256
`608b0f41f7ee181785cccbfcde65bf758e7dd056b0b179815d4991028144d8f6`),
query, logs, native environment creation and test receipt. All 12 original
response identities and failures are portable under
`tests/data/esr1_consensus_comparison/readiness_training_20261024/`, with notice.
Actual Ackredit captures retain 26 items / 86 uses, with no evaluation credit.
The [case](../docs/content/validation/esr1_consensus_comparison.md) explains both
attempts and their distinct scientific limits.

Actual Linux/Python 3.14.9 uses the same exact 325 public Conda records, MolSysMT
0.23.0, PyUnitWizard 0.29.0 and editable PHMT `0.4.0+17.g25a49f5`. Source/native
hashes and before/after producer audit are stable. All 51 selected scientific
controls pass with 232 historical public MolSysMT warnings retained. No new
full hosted/installed suite or public package is claimed.
Closeout passes 46 administrative/documentation tests plus 24 subtests, including
strict Sphinx and the frozen-query/selection guard; three reporting tests,
whole-tree Ruff, generated-index and whitespace checks pass. The original
attempt/declaration archive guards remain active. No new full scientific suite
is inferred from these selections.

**Next:** after committing these query/training records, implement/execute the
unchanged paired evaluation on all 64 reserved inputs. Native PHMT loads the
checksum-restored queries; public MolSysMT owns all molecular I/O/preparation
and fits. Keep exact declared screening settings, retain every acquisition/
preparation/search failure without replacement or inactivity imputation, and
report per-arm plus common-evaluable counts/metrics and missing-score sensitivity.
No tuning on evaluation outcomes. #64 remains partial for that comparison.

The owned public-provider environment is retained for this pending phase at
`/tmp/phmt64-readiness-20261024-4ceLcb/environment`, with raw logs/inputs beside it.
It is intentionally still useful; no retirement hook or shared/global-cache
cleanup is run. MolSysSuite #139 remains the owning cleanup diagnostic. Recheck
actual source/runtime identity before the next calculation; do not confuse the
base PHMT 0.4.0 Conda record with the editable source overlay.

Previously pending `cca31420cecb64c21bfeeff735d02fa2e443e9ce` now has CI
40134459469 reporting/all eight scientific jobs green, with actual dependency-
context/install/import/test steps verified; policy 40134459652 and Conda
governance 40134459644 succeed. This historical receiving does not qualify the
new training/archive head; follow #9 for its separate native checks/Documentation.
No addon, new release or broader documentation infrastructure is introduced.

## Second training attempt predeclared — 2026-10-24

The [new declaration](../tests/data/esr1_consensus_comparison/readiness_declaration.json)
fixes a 12-candidate training pool and provider-readiness policy under #64.
SHA-256 `b8ff6305ed7527289dad6ee13f7992b74928d93738c6f290fbdeff4099b1757e`.
It preserves the original 64 evaluation entries, baseline query, molecular
preparation route, native consensus/scoring parameters and model selection.

Reuse all three original acquisition responses exactly, including the 404;
request only the other nine predeclared candidates. Prepare all 12 with public
MolSysMT and retain failures. Select the first three successful preparations
in fixed order, without feature-count, geometry, support or score thresholds.
No alternate trio/pivot/model or increased budget follows failure. A valid
selected query and full training receipt must be committed before evaluation
acquisition/scoring. Attempt 1 remains terminal and its files are unchanged.

The [protocol](esr1_consensus_comparison.md)
links commands, source identity, cap and stop rules. The existing runner accepts
the two frozen declarations explicitly and checks original response reuse.
New guards protect unchanged evaluation/methods, the fixed candidate order,
exactly nine new requests, retained failures and score-free eligibility.
All 45 administrative/documentation tests plus 24 subtests, three reporting
tests, strict Sphinx, whole-tree Ruff and generated-index checks pass.

Next is executing only this new training stage in the same exact public-provider
environment, then archiving its measured outcome. Evaluation remains unopened;
this declaration itself produces no molecular/scoring result.

## Original training attempt stopped — 2026-10-24

**#64's declared training gate has executed and stopped honestly.** Clean source
`5242ca63eb239aaecb95ae782304dbeca7b53135` acquires only the three fixed training
inputs: PubChem supplies SDFs for 31477 and 6293, but 24633 returns HTTP 404
`PUGREST.NotFound`. Both available systems prepare successfully with public
MolSysMT 0.23.0 and pass every byte/state/atom/stereo/coordinate preservation
check. This is an unavailable acquisition, not a MolSysMT rejection or inactivity.

The all-three requirement stops this attempt at `stage='preparation'`.
**No consensus call, selected query, readiness score or evaluation exists.**
All 64 reserved evaluation CIDs remain without acquired structures or scores.
Do not replace CID 24633, relax parameters or assign a missing input a negative
score. The original declaration and original prior #62/#63 outputs remain intact.

The [summary](evidence/esr1_consensus_training_20261024_summary.json) qualifies
the full original output (raw SHA-256
`98f8320431c0b12397729f69034623cc80b41c8ca973e76915d79605443c6df6`),
execution/acquisition logs, environment creation, qualification and cleanup.
Both original SDFs, the 82-byte 404 and acquisition receipt are retained in
`tests/data/esr1_consensus_comparison/training_20261024/`, with a scoped notice.
The [case](../docs/content/validation/esr1_consensus_comparison.md) states the
measured preparation counts, zero evaluation denominator and actual 12-item /
14-use Ackredit payload without unexecuted consensus/screening credit.

Linux/Python 3.14.9 uses the same explicit 325-package public provider set as
the prior seeded replay, with exact editable source installed after provisioning.
Actual PHMT metadata `0.4.0+13.g5242ca6`, module origins, all source/native hashes
and unchanged before/after producer audit are retained. This is not a new public
package. All 51 selected rigid-consensus/scoring controls pass; 232 historical
public MolSysMT Pandas warnings remain recorded. A separate exposed-reference
control reproduces archived counts/features/states/RMSD after sharing the prior
preparation orchestration. No full scientific suite is rerun for this case-only
change or new hosted/installed matrix inferred.
Closeout passes 43 administrative/documentation tests plus 24 subtests, including
the archived-stop guard and strict Sphinx; three reporting tests, whole-tree
Ruff, generated-index and whitespace checks pass.

The owned environment is retired; raw responses/logs remain under the recorded
owned `/tmp/phmt64-training-20261024-SxBHSJ` root and are portable in the archives.
Retirement reports native success and removes its prefix, but the OpenCL hook
attempts a shared active-prefix path; the file is absent and deletion fails.
The original mixed log/JSON receipt is retained and routed to
[MolSysSuite #139](https://github.com/uibcdf/molsyssuite/issues/139). Do not treat
native cleanup success as proof of hook scope or infer a root cause. No shared
repair/global-cache cleanup is attempted; molecular results are unaffected.

Previously pending `b4565a15d211b162acff6be88e7c68620a4386ba` now receives CI
40129944533 with reporting and all eight Linux/macOS Python 3.11–3.14 science
jobs successful; their actual dependency-context/install/import/test steps are
verified natively. Policy 40129944770 and Conda governance 40129944824 succeed.
Declaration head `d53654fad6a448105f26d344f6c99bc306988e23` CI 40132174230 is
still running, with policy 40132174354 and Conda governance 40132174378 green.
These do not qualify the final training/archive head; follow #9 for its own
native receiving, including Documentation when available.

**Next:** #64 remains partial because no discrimination comparison was possible.
The original attempt is terminal under its frozen declaration. Predeclare a
distinct attempt with a bounded training-candidate/readiness policy before any
new acquisition, preserving the still-unopened evaluation cohort and scientific
method parameters. Readiness must use provider-owned molecular operations; do
not silently substitute an input, generate conformers locally or tune against
evaluation. MolSysMT #447 remains a separate molecular-overlap proposal and is
not the cause of this stop. New addon/release infrastructure stays deferred.

## Training-only comparison declared — 2026-10-24

The next scientific segment is [#64](archive/esr1_consensus_comparison.md).
Its [protocol](esr1_consensus_comparison.md) and
[frozen declaration](../tests/data/esr1_consensus_comparison/declaration.json)
are fixed **before new structure acquisition or molecular scoring**. They
compare the unchanged original #62 query against one native rigid consensus
learned from three new actives. All molecular work remains MolSysMT-owned.

The source is the original archived AID 743075 v2 concise response. Exclude all
4,402 CIDs in the entire Bath table and all 370 assay CIDs with conflicting
outcomes, including inconclusive. Use lowest-SID representatives and a distinct
SHA-256 order. Of 338 eligible actives / 2,749 inactives, reserve three actives
for training (31477, 24633, 6293); the next 16 actives and first 48 inactives are
the 64 evaluation inputs. All 67 CIDs are distinct. Labels inform stratification;
new molecular features/scores have not been examined. Same-assay CID separation
does not establish chemical-series or independent-assay validation.

The method, finite budgets, training-only model choice, readiness check,
failure/no-replacement rules, baseline query hash and comparison denominators
are frozen in the JSON. The standard-library declaration driver reproduces it
from checksum-qualified original sources and refuses output overwrite. Two
offline guards verify that mechanism, synthetic label conflicts, row-order
independence and changed-source refusal. This is not a scientific run; no new
conformer, query, evaluation score or public artifact is produced.
The declaration SHA-256 is
`a1a476e7e94fd3480ee3845fbc5cca138221c4052eb7165a254499fd526ff647`.
All 40 administrative/documentation tests plus 24 subtests and three separate
reporting tests pass; strict Sphinx, whole-tree Ruff and generated-index checks
pass. No molecular suite or original scientific output is rerun for this slice.

**Next action:** acquire only the three training SDFs, retain their original
responses/failures and qualify preparation with public MolSysMT 0.23.0 in an
owned environment. Execute the declared native consensus and save all original
evidence. A valid selected query and training receipt must be committed before
evaluation structures or scores are opened. If training prerequisites fail,
retain the outcome and keep evaluation unopened; do not replace inputs or tune
the declared method. The protocol links the existing exact provider environment
and source-overlay route; no new environment has been created yet.

Source/issue inspection identified a missing reusable molecular identity/scaffold
overlap route; the proposal is
[MolSysMT #447](https://github.com/uibcdf/molsysmt/issues/447). It does not block
this explicitly CID-only comparison. Do not implement that molecular analysis in
PHMT or promote the split into a chemical-series independence claim.

Previous head `b4565a15d211b162acff6be88e7c68620a4386ba` receiving remains partial:
CI 40129944533 has reporting and both Python 3.14 science cells green, with six
remaining science cells running. Policy 40129944770 and Conda governance
40129944824 succeed. Documentation was not yet listed. Local declaration checks
do not establish this or the next head's full hosted matrix; follow #9 receipts.
Addon, additional release and wider documentation work remain deferred.

## Portable pilot inputs — 2026-10-24

**#62's bounded activity pilot is complete.** The exact original 35-file input
bundle is now portable in this repository, with its original SHA-256 and a
[scoped rights/attribution notice](evidence/esr1_activity_pilot_inputs_20261023_NOTICE.md).
The [snapshot summary](evidence/esr1_activity_pilot_inputs_20261023_summary.json)
qualifies the 12,495,338-byte archive and the unchanged original query archive.
Old manifests/results and their dated narrower publication statements are not
rewritten. The [resolved report](archive/esr1_activity_pilot.md) records closeout.

The current unshipped driver restores 35 inputs plus the original saved query
without network or molecular dependencies:

```bash
python phmt_test_support/esr1_activity_pilot.py \
  --data-dir /tmp/esr1-original-inputs --restore-archive
```

Use a new destination. The operation checks the compressed/raw archive and all
original file identities, rejects substitutions and preserves all five failed
HTTP responses. It reuses the existing evidence reader; molecular operations
remain in MolSysMT. Seven offline case guards pass, including reconstruction of
the original Bath split and primary-assay labels. This does not rerun or upgrade
the dated scientific evidence. The [case](../docs/content/validation/esr1_activity_pilot.md)
now shows how current offline restoration feeds each recorded scientific producer.
Verification totals: 38 administrative/documentation tests plus 24 subtests,
18 archive-reader tests and three reporting tests pass in their separate CI
process contexts. Strict Sphinx, whole-tree Ruff and generated-index checks pass.

**Next:** declare a new scientific comparison with prepared training inputs and
an actually unexposed evaluation cohort. #62 is exposed development data; its
binary replay is not new biological validation. Keep provider receiving under
#41 and conformer/stereo/H needs in MolSysMT. The addon and further release or
documentation infrastructure remain deferred; public 0.4.0 is unchanged.
The detailed #63 source/environment checkpoint below remains applicable.

Hosted receiving for source `481855e7e9de745793d8cd36296ff9be81e99094` is still
partial at this inspection: CI 40127949298 has reporting and Linux/macOS Python
3.14 green; the six Python 3.11–3.13 science cells are running. Documentation
40128123736, Conda governance 40127949565 and suite policy 40127949623 succeed.
Do not claim full-matrix qualification until native completion. This retention
change will receive its own unskipped push and native checks.

## Current MVP checkpoint — 2026-10-24

**#63 is implemented and locally qualified.** Its
[resolved report](archive/rigid_negative_ranking_contract.md) and
[contract](seeded_ranking_workflow.md) separate raw checked-pose coverage from
explicit `search_method='seeded_hit'` molecular ranking. The new criterion tests
fitted triplet seeds only: hit one, completed negative zero, failed/unresolved
input unscored. It excludes the arbitrary supplied placement. Negative ties
do not use partial coverage. When no pose is fitted, no coverage or coordinates
are invented. This is a bounded binary search criterion, not a graded partial
optimum, exhaustive continuous-pose search, affinity or predictive qualification.

The direct compatibility search defaults remain. Retrospective/facade consumers
now require explicit `score_method='checked_pose_coverage'` to rank legacy
rigid/conformer evidence; placed evaluation retains its declared-frame default.
Public `get_screening_score` is reused across consumers. Exports distinguish
criterion, molecular score and raw `fit_value`. All molecular operations stay in
public MolSysMT; no provider implementation or dependency requirement is changed.

Clean implementation/replay producer is
`c80325c5c3851691bcc0a993d1e73eaf294654f6`. The complete source suite passes
**949 tests** on Linux/Python 3.14.9 with public MolSysMT 0.23.0, PyUnitWizard
0.29.0 and the declared test extras. All 223 recorded runtime/test/support Python
hashes remain unchanged through the source commit and suite. Warnings are
retained, including historical public MolSysMT deprecations and intentional
attribution-failure controls. The new code is **development source after 0.4.0**;
no new package/release is produced and public 0.4.0 keeps its original API.

The [replay summary](evidence/esr1_seeded_hit_replay_20261024_summary.json) qualifies
original full output, preparation journal/log, unchanged original query archive
and source qualification receipt. Its declaration was fixed before new scores.
All 32 input identities/order and query bytes are unchanged: 25 evaluate (6 active
/ 19 inactive), six remain unscored (1 / 5), and the same active CID 24964624 hits.
Binary AUC is 0.5833333333, BEDROC(alpha=20) 0.6496274186 and EF at 10%
1.9675925926. Twenty-four scores tie at zero; 23 valid negatives have no fitted
pose. The original continuous-coverage run is preserved. These are different
criteria and recorded runtimes on exposed data, not a biological improvement or
fresh independent holdout.

Actual source origins/hashes distinguish the editable PHMT overlay from the base
Conda package record. Editable version metadata was generated before the source
commit; it is not executed-source identity. The 325-package
[Linux explicit environment](evidence/seeded_ranking_environment_20261024_explicit.txt)
retains public URLs and SHA-256, is parsed in a successful native Mamba dry run,
and must be followed by installing the recorded source producer. Do not treat
that base environment as a new PHMT public artifact.

### Where to continue

1. **#62:** resolve portable long-term original-input retention. Originals remain
   in `/tmp/phmt-ligand-pilot-20261023`, including the hashed 35-file bundle in
   the prior checkpoint. Raw input redistribution is not claimed; strict restore
   refuses refreshed upstream bytes. Original and replay outputs are archived
   independently here with checksum-qualified readers.
2. Declare the next scientific comparison on reviewed prepared training inputs
   and a genuinely unexposed evaluation set. Do not tune against #62's observed
   outcomes or call the development replay independent validation. Binary hit
   classification is now usable; graded partial ranking is not supplied by #63.
3. **#41 / provider receiving:** qualify newer molecular contracts separately.
   Existing conformer/stereo needs remain MolSysMT #219/#215/#299. Environmental
   H refinement #323 and newer directional-contract #375 receiving do not block
   this completed local scoring slice. Do not fill their molecular gaps here.
4. New addon work and broader documentation/release infrastructure remain deferred.
   The only documentation changes here explain the delivered source contract and
   executed scientific cases. Public 0.4.0 / MolSysSuite #131 is unchanged.

The previously pending source `29000c36a9375082e7f950ff78210dd7f7bdc27a` receiving
is now verified: CI 40019851558 has all eight science cells and reporting green;
policy 40019851935, Conda governance 40019852035 and Documentation 40019903965
succeed. That does not qualify this new implementation/final head. The final
unskipped push receives its own native gates; local receipts do not claim their
completion. Follow the owning #63/#9 run receipts for unfinished hosted evidence.

Temporary qualification prefix/output ownership and retirement are recorded in
the replay summary. The shared development environment and caches are not cleanup
targets. Recreate an environment from the explicit provider file and overlay the
recorded source when replaying; keep original data and original output archives.

## Current MVP checkpoint — 2026-10-23

The maintainer resumed the scientific MVP and deferred deeper documentation and
addon work. [#62](archive/esr1_activity_pilot.md) now has an executed,
pre-score frozen ligand-reference ERα signaling-assay pilot. The protocol/driver
producer is `ee064102f3701a280297e01ec0c549207f10bfd3`; the runtime is installed
public PharmacophoreMT 0.4.0 / MolSysMT 0.23.0, Linux/Python 3.14.9, with all
311 Conda records and native-extension identities in the full output. No runtime
or molecular-provider code is changed.

The [summary](evidence/esr1_activity_pilot_20261023_summary.json) qualifies the full
result, saved query, preparation journal and log. Four contradictory-label CIDs
were excluded before any scores. Of the 32 selected inputs, one is the reference;
seven active and 24 inactive inputs are held out. Five lack PubChem 3D records;
MolSysMT rejects one further stereo interpretation. **25 inputs are evaluated
(6 active / 19 inactive), six remain unscored (1 / 5)**. AUC is 0.5614, EF at
10% 1.69, one active hits and 23 scores tie at zero. The missing-score hypothetical
AUC range is 0.4494–0.6280. This is weak exploratory evidence, not a predictive
qualification; exact CID disjointness does not establish independent series.

The [case](../docs/content/validation/esr1_activity_pilot.md) supplies executable
commands, original labels and method/units/attribution boundaries. Three cheap
offline guards check original identities, failures/denominators and independent
pairwise AUC/tie-aware EF arithmetic. They do not rerun molecular science.

### Next steps

**First local MVP priority is now [#63](archive/rigid_negative_ranking_contract.md).**
A separate source control reproduces partial negative coverage 1/3 → 0 under
MolSysMT translation of the same propane input. Both searches remain completed
negatives. Define/qualify the molecular ranking contract before expanding activity
claims; this is local PharmacophoreMT work, not blocked by MolSysMT. The
[original probe](evidence/rigid_negative_frame_probe_20261023.json) is distinct
from the frozen public-runtime assay experiment and does not overwrite it.

1. Preserve the frozen query and original run. Do not tune it on the exposed
   held-out outcomes. The native reference has two acceptors and one aromatic
   site; no donor is emitted, and no donor-bearing query acceptance is inferred.
2. Resolve portable long-term retention of original input bytes under #62. The
   owned `/tmp/phmt-ligand-pilot-20261023` retains source archives, primary assay
   description/table and 27 SDFs; the committed manifest has URLs/hashes. Raw
   input redistribution is not claimed. Strict restore refuses refreshed
   responses; preserve originals if upstream bytes change.
3. Follow consumer evidence in provider-owned MolSysMT #219 (missing conformers)
   and #215/#299 (explicit stereo rejection); do not repair molecules here.
4. Declare a distinct next comparison using reviewed training/evaluation data,
   conformer policy and frozen parameters. These exposed outcomes are development
   evidence, not a fresh independent test set. No addon is needed for this step.

Provider handoffs are delivered in [MolSysMT #219](https://github.com/uibcdf/molsysmt/issues/219#issuecomment-6373946367)
and [#215](https://github.com/uibcdf/molsysmt/issues/215#issuecomment-6373947311).
Original inputs are additionally bundled locally as
`/tmp/phmt-ligand-pilot-20261023/original-inputs-20261023.tar.gz` (35 files,
12,495,338 bytes; SHA-256
`fc6a5295bbf4dbd9743f31a7f54d396b09578e60754ebcabd4388a588252e995`).
This is local retention, not public redistribution or a long-term archive service.

Local acceptance passes: three pilot guards, 18 existing archive-reader tests,
three reporting tests, all 33 administrative controls with immutable SDK
`1c248b67d1daea256ed7c7f6172c6addb3f0b08f`, whole-repository Ruff and complete
strict Sphinx build (one test, 7.73 s). The first SDK control run caught the new
guard importing the unshipped namespace before its staging test; loading the
canonical standalone reader without namespace registration repairs isolation.
No scientific rerun or data/score change is involved.

The isolated environment has been **retired after successful execution**; all
27 original SDF checksums were reverified before cleanup. Original inputs and
outputs remain in the owned directory, with portable output archives committed.
No shared environment/cache is touched by cleanup. Prior public 0.4.0 delivery
and central follow-ups remain
unchanged; no new release or MolSysSuite availability notice is required here.

Native receiving at scientific/evidence source
`598d3744dc5348b497747d68f3a22a4c5d14ae53`: policy **40018408199**, Conda
governance **40018408302** and Documentation **40018949108** succeed. CI
**40018407677** has successful reporting governance; its eight scientific cells
are still in progress at this observation. The push-only daily backlog detector
is inapplicable/skipped, not executed acceptance. Do not claim eight-cell or
exact-final-head completion from this snapshot. The documentary qualification
and #63 inventory change pass all 33 local administrative controls, reporting,
Ruff and complete strict Sphinx (7.81 s); the final unskipped push receives its
own native gates. Follow the owning runs/#9 for unfinished native evidence.

## Current documentation outcome — 2026-10-23

The first documentation foundation is complete. The inherited identity (#4) and
reader-entry work (#61) are resolved in the [identity archive](archive/documentation_project_identity.md)
and [entry-point archive](archive/documentation_reader_entry_points.md).
About, landing, user/developer/showcase portals and the cookbook introduction now
describe PharmacophoreMT's delivered routes and point to the existing recipes,
API and evidence. The theme/configuration and runtime code are unchanged.

The [local receipt](evidence/documentation_foundations_20261023.json) records the
complete strict Sphinx guard, six rendered page checks and preserved notebook
execution material. The [native receipt](evidence/documentation_publication_20261023.json)
binds source `7aa33cd88806dcde05a01a9416df11d844cb9b62` to successful Documentation
40011094526, policy 40011098877, Conda governance 40011103894 and administrative
probe 40011110286. Six pages were read from immutable gh-pages
`c869f6ed18a4dc8ee510efea4d5cf979e8cc0ef0`; Pages reports the site built.
The probe omits science, and this work executes no notebook or molecular workload.
No new package, scientific/provider, visual/browser or documentation-badge
acceptance is inferred. The closure commit changes only reports/indexes/evidence;
the published documentation content remains that reviewed source.

Next local documentation work can develop the user guide's concepts and worked
routes beyond these portals, with new examples executed only in an explicitly
qualified context. Reuse the existing cookbook/validation collection; keep
molecular operations with MolSysMT. #41/provider receiving and #20/#22 scientific
validation retain their independent scopes; new addon work remains deferred.
Public 0.4.0 and its central delivery follow-ups remain in the prior checkpoint.

Local HTML and review records remain in the owned
`/tmp/phmt-docs-foundations-20261023` directory for optional human preview. Durable
JSON receipts are committed here; there is no new environment, cache or server to
keep running. Documentary skip/recovery remains tracked under #9.

## Prior documentation preparation — 2026-10-23

The maintainer resumed documentation work using MolSysMT/MolSysViewer's existing
Sphinx/MyST/PyData pattern as reference. #4 owns the inherited PocketMT identity;
#61 owns reader entry points. About now describes PharmacophoreMT and its molecular
ownership boundary; landing/user/developer/showcase pages lead into existing
recipes, API and evidence. `docs/README.md` supplies the local contributor route.

The complete strict Sphinx guard passes after including that new guide in the
developer toctree. The landing notebook's code, outputs and metadata are preserved;
no notebook or molecular calculation is executed for this narrative slice. Native
publication and report archival are the next closeout steps. These are documentation
controls, not a new release or an extension of the scientific/provider acceptance
record. New addon work remains deferred.

This documentation checkpoint uses a conditional `[skip ci]` after the local
strict/rendering and reporting checks; native documentation publication and
administrative checks follow on its committed head. Full scientific backlog
remains #9's scope and is not cleared by those documentation controls.

## Prior delivery checkpoint — 2026-10-23

**0.4.0 is public**: [GitHub Release](https://github.com/uibcdf/pharmacophoremt/releases/tag/0.4.0)
and [official Conda package](https://anaconda.org/uibcdf/pharmacophoremt).
The tag points to original producer
`60b21b7d183217d50c29ea3e6bc0d05fb5b797a2`. One original
`pharmacophoremt-0.4.0-py_0.tar.bz2` was promoted from staging to main with SHA-256
`e5ed3a7c20ec36b9938fee51a6a9e0dc1654d7709d0d26ad75e49babac5d59a4`.
Historical tags are unchanged. The maintainer's requested availability notice is
[MolSysSuite #131](https://github.com/uibcdf/molsyssuite/issues/131).

The [source/staging receipt](evidence/conda_040_staging_20261023_summary.json)
retains all eleven required executed source/control jobs, recipe tests, producer
39996616723 and the independently downloaded original archive. The
[delivery receipt](evidence/conda_040_delivery_20261023_summary.json) retains
installed run 39997342556 (**8/8 cells, 921 passing items each**), all four required
phases, eight support execution/cleanup receipts, promotion/public-verifier run
40002784859 and fresh normal public receiving on Linux/Python **3.14.9**.
Normal Python bounds are honored. SDK call reports include unittest subtests and
are distinct from the reported 921 test items. Existing warnings are retained.

Producer and installed workflow head
`c0f6ac65aad6fa7e1018636e6b0756668aed5459` adds only contributor/guide notices;
the source, workflows, tests and support remain those of the original producer.
The native binding and common verifier explicitly retain both identities. The
accepted SDK remains `1c248b67d1daea256ed7c7f6172c6addb3f0b08f`; no later SDK
capability or newer MolSysMT development API is adopted by this release.

### What remains and where to resume

1. **MolSysSuite #131 / #45:** receive the delivery and triage the automatic
   Release-event route. Run 40004204755 is **failure**: the shared publisher rejects
   a staged plan at the metadata-freeze guard. Build and upload steps are skipped;
   this is separate from successful staging, installed science and promotion.
   #10 remains partial for that route disposition; do not rebuild/overwrite 0.4.0
   or move its tag to make this extra event green.
2. **MolSysSuite #131 / #51 and local #23:** review central public Python admission
   and generated badge/inventory updates. Four-minor installed evidence is now
   delivered; the existing centrally admitted badge is retained pending disposition.
3. **Local #41 / MolSysMT #375:** qualify the newer H-bond namespace/directional
   contract separately, using provider-owned geometry. The release's qualified
   public molecular-provider context is MolSysMT 0.23.0. Its retained pandas
   warnings belong to the historical public version; #431/#386 have source fixes
   and this receipt does not establish a regression against them. Environmental
   hydrogen refinement #323 remains independent upstream work.
4. **#20/#22:** continue the independent scientific/biological validation with
   declared inputs and controls. New addon work remains deferred; #58 and its
   viewer-owned blocker are not closed by package publication.

Read the current owning issues before starting another segment. Public release
availability does not establish biological/activity discrimination, newer-provider
compatibility, public PyPI delivery or live-browser/hardware acceptance.

### Closeout evidence and resources

The final public receiving succeeds after an owned disk-quota cleanup and two
corrections to the one-off audit script (external-provider recursion and optional
test-extra metadata). These failed attempts are retained separately; no runtime
package code, required gate or warning filter was changed to obtain the result.

Completed historical/current receiving and build environments/caches were retired
under the task-owned temporary roots. Shared user environments/caches are untouched.
Original archive, clean producer clone and receipts remain under
`/tmp/phmt-conda-040-20261023`; the accepted SDK and historical wheel/receipts remain
under `/tmp/phmt-installed-qualification-1wwqno5j`. The old `public-env`, build envs
and caches listed in the dated pause below no longer exist. Durable compressed
receipts are committed here, so resumption does not depend on `/tmp` surviving.

This documentation/evidence closeout uses `[skip ci]` after its applicable local
checks. Ordinary CI debt and nightly/weekly/manual recovery remain owned by #9;
it does not acquire the exact-source qualification of `60b21b7`. Current native
documentation/coordination receipts are linked from #10 and MolSysSuite #131.

## Prior resumption checkpoint — 2026-10-23

The maintainer resumed work and confirmed the proposed **0.4.0** candidate by
instructing continuation after the explicit version question. The active segment
remains #10/#9/#23; new addon work stays deferred. The reviewed real
[`release_plan.toml`](../devtools/conda-build/release_plan.toml) selects version
0.4.0, build 0, one noarch archive and the staged route. Its eight installed cells
and eleven required source/control jobs preserve the existing contracts.
`dependencies_public = false` conservatively retains unqualified candidate
closure; the prior public-provider wheel result is not candidate qualification.

Next, obtain exact-source native gates for the committed plan, establish staging
access, build one original archive and execute the eight installed cells before
reviewing public promotion. Candidate SHA, filename, digest and native run IDs
will be recorded after execution; no public tag or GitHub Release is selected by
this plan commit. Follow [publication operations](../devtools/conda-build/README.md)
and the ordered steps in the dated pause record below.

During the pause, MolSysSuite independently received the source/helper milestone;
see [the central receipt](https://github.com/uibcdf/molsyssuite/blob/338a4fceb81a11e3eec89635bb9d8ae0b054de65/devguide/rollouts/pharmacophoremt_support_receiving_45_20261021.json).
The source gates and support hashes were verified; central did not reinstall the
original wheel or qualify a Conda candidate. Shared #92 advance notices are
available for later deliberate review; they do not require replacing the
already-qualified immutable SDK for this candidate.

## Prior pause checkpoint — 2026-10-20

The maintainer requested a pause. Resume with this section and the
[current roadmap](roadmap.md), then consult the
owning reports linked below. No build, test, upload or publication task needs to
continue during the pause. New addon work remains deferred.

### What we were doing

The active segment is distribution and installed qualification under
[#10](pending_proposals/noarch_distribution_adoption.md), with source CI in
[#9](pending_bugs/full_ci_routes_and_skipped_push_recovery.md) and public/Python
delivery in [#23](pending_proposals/adopt_required_python_314.md).
The implementation is committed as `636373d3c5c24a1eff6d2bec5f3eceb6ce018ba4`;
the subsequent evidence-only checkpoint is
`63b9ef67e54102a83b688b5cbf2dea79e054a57d`. Both are on upstream main. This pause
update changes documentation only; it does not acquire the implementation's
exact-source CI identity. Its `[skip ci]` handoff retains ordinary CI debt and
daily/weekly/manual recovery under #9; local index/reporting checks cover this
documentation change.

- Packaging metadata #57 is resolved and archived, with isolated sdist/wheel
  builds using setuptools 77.0.3 and 84.2.0; see
  [the result](archive/packaging_license_metadata.md).
- MolSysSuite #117 is adopted at
  `1c248b67d1daea256ed7c7f6172c6addb3f0b08f`. Scientific helpers are explicitly
  staged from the unshipped `phmt_test_support` namespace. The real isolated
  development wheel passes **921 tests** on Linux/Python 3.14.8 with public
  providers, including MolSysMT 0.23.0. All 179 runtime paths match and staged
  support resources/imports are retired; see
  [the receiving receipt](evidence/installed_support_adoption_20261020_summary.json).
  The separate preparation record preserves the original six failed cases.
- Source CI at `636373d` passes **8/8** Linux/macOS arm64 × Python 3.11–3.14
  scientific cells plus reporting, policy and Conda governance: eleven required
  executed jobs. See [the exact-source receipt](evidence/source_ci_receiving_20261020_summary.json).
  CI run 39478128959, policy 39478129327 and Conda governance 39478129573 belong
  to that implementation, not to later documentation commits.

### Decision still pending

The maintainer initially selected **0.1.0**, but that upstream tag already points
to historical commit `f0810257a8ed05897643d6303e264adb2697b727`. Remote inspection
on 2026-10-20 confirms tags 0.1.0, 0.2.0 and **0.3.0** (the highest version;
`efb18c28b23e8c017a9c420fa7cf91dc54997ace`), with no GitHub Releases listed.
**0.4.0 is proposed, not approved.** Confirm the maintainer's collision-free
version choice on resumption; preserve the historical tags.

There is still no actual `devtools/conda-build/release_plan.toml`, original Conda
candidate, staged upload, eight-cell installed Conda result or public promotion.
The example's 0.0.0 is illustrative. Repository-level inspection found no
`ANACONDA_UIBCDF_TOKEN`; inherited organization access and validity remain
unknown. Source CI and the development wheel do not qualify a Conda candidate.

### Resume in this order

1. Check the worktree and upstream main for changes, read the current #10/#9/#23
   issue updates and confirm the version choice. Read
   [publication operations](../devtools/conda-build/README.md) and
   [release titles](release_titles.md) before preparing the real plan.
2. Commit a reviewed `release_plan.toml` with the selected version, actual build
   number, staged route, responsible maintainer/date and required gates. Obtain
   the required source gates for that exact new candidate SHA; do not reuse
   `636373d` as if it contained the new plan.
3. Establish staging access and build/upload one original archive using
   `build_and_upload_conda_packages.yaml` with the reviewed `candidate_sha` and
   `version`. Retain the original filename, SHA-256 and producer receipts.
4. Run `test_installed_conda_package.yaml` for that exact SHA/file/digest across
   all eight supported cells. Require installation, installed-file validation,
   complete scientific tests and the post-test provenance recheck in every cell.
5. Review the publication decision only after qualification. Promotion preserves
   those exact bytes; public-label/index and clean receiving checks remain
   separate #10/#23 evidence. Update owning reports/issues with actual results.

The maintainer permits direct commits/push to main; no PR is required for this
internal route. General molecular manipulation remains MolSysMT-owned and
missing provider capabilities are proposed through provider issues.

### Independent follow-ups and local resources

[#41](pending_proposals/retire_legacy_molecular_operations.md) remains partial:
the newer sibling MolSysMT source moved H-bond APIs to `interactions.hbonds` and
exposes directions, but that namespace/directional contract is not yet qualified
by PHMT. Its exploratory shared-editable run failed; use the report's provider
identity and evidence when reviewing migration. Do not treat it as the passing
public MolSysMT 0.23.0 context or restore local molecular algorithms. Provider
#375 qualification and environmental H refinement #323 are separate follow-ups.
After the distribution segment, #20/#22 retain independent scientific-validation
work; addon #58 remains lower priority with its provider-owned viewer blocker.

Owned temporary resources are intentionally retained at
`/tmp/phmt-installed-qualification-1wwqno5j` (also recorded by
`/tmp/phmt-installed-qualification-path`): `public-env`,
`build-envs/phmt-candidate-build`, `sdk-installed`, `support-artifacts` and
`final-receptor`. Their presence was checked at pause. The build environment was
created with qualified Mamba 2.9.0/declared-only channels. Recheck these resources
before reuse; `/tmp` can disappear. Durable receipts are committed under
`devguide/evidence/`, so resumption does not depend on those directories.
Review owned temporary-resource cleanup when the candidate segment closes.

## Prior pause checkpoint — 2026-10-13

The implementation checkpoint is `eca174b`, published on the official
`uibcdf/pharmacophoremt` main branch. Use the [current roadmap](roadmap.md)
and the [pending issue indexes](pending_proposals/README.md) for resumption;
the chronological observations below preserve their original dates and scopes.

The minimal viewer addon (#56) and panel feedback/teardown (#59) are resolved.
#59's [archived report](archive/viewer_panel_feedback.md) links the final
14-control live-browser record and 23 native addon tests. #58 remains partial:
its [current-provider receipt](evidence/current_viewer_addon_20261013_summary.json)
reproduces the molecular-free workspace blocker owned by MolSysViewer #240.
The later panel run uses the development provider and does not change that
installed-provider record or qualify public browser delivery.

At this checkpoint, policy and Conda governance runs for `eca174b` succeeded;
[scientific CI 38438999594](https://github.com/uibcdf/pharmacophoremt/actions/runs/38438999594)
was observed queued, so its complete matrix is not claimed to have passed.
This is a dated observation, not a current run-status monitor.

Remaining work is already owned: #57 packaging metadata, #10/#23 installed/public
delivery with MolSysSuite #117 helper isolation, and #58 receiving after the
MolSysViewer fix. Molecular preparation and remaining #41 geometry delegation
stay with MolSysMT. No development task needs to remain running during the pause.

## Historical implementation observations

**Original status (2026-10-03):** Gen 1b classical consolidation. The immediate
priority is executing traditional workflows, with the growth contracts needed
for later scientific methods and measured acceleration.

## Verified local scope

The [observed-complex route](placed_pose_workflow.md) consumes native MolSysMT
hydrophobic/H-bond, [ionic observations](ionic_interaction_workflow.md) and
[pi-pi/cation-pi observations](aromatic_interaction_workflow.md).
The [reference-ligand route](reference_ligand_workflow.md)
builds queries from six classical chemical families. Both use public MolSysMT
recognition; aromatic planes and charge geometry also come from MolSysMT.
Pose evaluation has explicit essential, weight, direction/normal and exclusion
semantics. Native JSON preserves the delivered definitions and provenance.
The [rigid-search route](rigid_search_workflow.md) composes reusable correspondence
and alignment tools with that evaluation. MolSysMT performs molecular fitting
and coordinate installation. Unresolved search budgets retain failure state. The
[prepared-conformer route](conformer_screening_workflow.md) searches requested
frames and retains their states, pose coordinates and failures. Only resolved
molecule scores enter retrospective metrics.

Metrics and retrospective accounting now distinguish scientific negatives from
failed calculations and preserve input identity and ranking ties. Guards are
`tests/test_pose_evaluation.py`, `tests/test_reference_ligand.py`,
`tests/test_retrospective.py`, `tests/test_validation_metrics.py`,
`tests/test_contracts.py`, `tests/test_rigid_search.py` and
`tests/test_conformer_screening.py`. Verification uses pinned provider source trees
with existing scientific dependencies; see the workflow documents for limits.
The complete local suite passed 118 tests; the reference-ligand, rigid-search and
prepared-conformer documentation examples and offline reporting/quality checks
also passed.
User-facing executable recipes now live in the
[cookbook](../docs/content/cookbook/index.md), linked from the documentation
navigation and user guide.

After native Ackredit integration, the complete local suite passed **132 tests**
(including 14 attribution controls) on Python 3.13.14 with the controlled source
providers. Both attribution cookbook code blocks executed successfully. Ackredit
is pinned to `584328de6efc07cee3a5ddf3ecda2d2e08cc72b4` for controlled development
verification; this is not published-wheel or hosted-matrix closure.
The isolated cookbook Sphinx build passed with nitpicky checking and warnings
treated as errors. This is a cookbook build, not full-site build acceptance.
Cross-provider failure isolation under warnings-as-errors awaits the observed
MolSysMT attribution-warning correction in `uibcdf/molsysmt#295`.

The first native [aligned-ligand consensus](aligned_consensus_workflow.md) is now
implemented locally: reusable fixed-frame feature matching and explicit-group
aggregation feed a reference-anchored model builder. It retains one contribution
per declared ligand, correspondence/source evidence, mean feature centers,
reference orientations, dispersion, rejected groups and Ackredit metadata.
After this slice the full local suite passed **149 tests**, including 17 consensus
controls. Both aligned-consensus cookbook blocks executed successfully; the
independent reporting/index checks and Ruff also passed.

These local changes await review. They do not establish published-wheel,
hosted-matrix, free-screening or biological-pilot success. Historical existence
of the legacy modelers and utilities is not evidence of complete consolidation.

## Owning work and next steps

Issues `#12`, `#13`, `#14` and `#15` own ranking/accounting, the first native complex
slice, native reference-ligand construction and native rigid pose search.
`#2`, `#6`, `#9` and `#10` retain diagnostic, support-library, CI and distribution work.
Issue `#16` tracks the locally corrected zero-angle normalization-roundoff defect.
Issue `#17` owns prepared-conformer screening and per-frame score resolution.
Issue `#18` owns the measured legacy distance/clique defects and native consensus
replacement; the [literature and ownership review](clique_consensus_review.md)
and bounded executable audit are delivered locally. Issue `#19` owns deferred
native Ackredit capture, detached bibliography and report integration, now
implemented with real-provider controls and a cookbook recipe. Distribution and
hosted-matrix acceptance remain pending.
Issue `#20` records the future decision between a documentation validation/
benchmark section, dedicated website or common evidence collection with both
views, including reproducible notebooks and publication/update policy.
Issue `#21` owns the reference-anchored aligned consensus, its independently
reusable matching/aggregation tools and the executed cookbook recipe.
Issue `#22` owns the [ERalpha input audit and native validation gate](eralpha_validation.md).
The checksum-qualified real fixture has incomplete declared chemistry; public
PDB-text/RDKit conversion does not supply supported bond orders. Native recognition
rejects it explicitly. Molecular template application is tracked in
`uibcdf/molsysmt#298`; positive native ERalpha validation and verified derivation
from the historical 1QKU dataset label remain pending. The case now has an audit
guard and a cookbook notebook, distinct from the retained legacy regression.
The two ERalpha tests passed with the controlled source providers; the notebook's
three code cells executed successfully and its schema/output checks passed.
The audit CLI emitted valid JSON, the isolated cookbook build passed strict
Sphinx checking, and the three reporting tests, generated indexes and Ruff passed.
The latest complete-suite result remains the 149-test run above; this slice was
verified with its focused tests and documentation rather than a new full run.

On **2026-10-03**, the next slice added independently acquired RCSB 1QKU/CCD EST
source bytes with URLs, checksums, entry revision and exact ligand identity.
The selected label chain D (author chain A, residue 600) has 20 observed heavy
atoms; the CCD definition also has 24 H whose complex coordinates remain absent.
Native chemical preparation is still pending. The minimum read-only assessment
and transactional template-application contract is now specified in the owning
MolSysMT #298 proposal; it is not an implemented public API.
All **three ERalpha tests** passed under the controlled source providers, and the
updated cookbook notebook executed **four code cells** without errors. Both
repositories' generated proposal indexes/guide checks and the three local
reporting tests passed; the strict isolated cookbook build, Ruff and whitespace
checking also passed. No new full-suite,
positive native ERalpha or biological result is claimed.

On **2026-10-03**, the independent next slice added
[aligned clique consensus](aligned_clique_consensus_workflow.md), owned by #24.
Reusable feature-clique discovery, aggregation/hypothesis packaging and the
prepared-ligand model builder discover sites absent from a reference and retain
alternative models. Hypotheses require disjoint occurrences and a common ligand
support intersection. NetworkX owns generic enumeration; optional Ackredit credits
the executed Bron--Kerbosch/Tomita implementation references and the provider's
description/software versions, with detached bibliography in each saved model.
The executed cookbook exposed a provenance defect (#25): literal IDs such as
`a` and `b` were parsed as units. The owning copier now preserves strings before
quantity-object sealing, guarded against the original IDs rather than only output
roundtrip equality. The final complete local suite passed **177 tests** in 114.94 s,
including 25 clique controls and the literal-string/quantity regression. Two
warnings remain: the deliberate Ackredit-failure control and the existing legacy
screening unit-stripping path; neither is new clique-method failure evidence.
All **three aligned-clique cookbook code blocks** executed successfully. The strict
isolated cookbook Sphinx build passed, as did the three offline reporting tests,
generated indexes, Ruff and whitespace checks. This verifies the source checkout
under the existing controlled provider pins; it does not establish whole-site,
installed-wheel, hosted-matrix or biological acceptance. Molecular preparation
remains with MolSysMT #298/#300.

On **2026-10-03**, #26 adds [prepared rigid unaligned consensus](rigid_consensus_workflow.md)
with an explicit pivot and reusable association-clique or typed-triplet proposals.
All molecular fits/transforms remain in MolSysMT. Absolute post-fit geometry and
injective matching are checked; accepted alternatives feed separate aligned
consensus layouts. Unplaced ligands retain source evidence and input support
denominators. The [primary-source strategy survey](pharmacophore_search_strategies.md)
compares efficient published alternatives and records G3PS, safe RDP/frequent-clique
conformer discovery, triangle indexing and Gaussian overlap as distinct future
comparisons. Runtime Ackredit credits executed clique/assignment solvers and the
provider-documented Kabsch criterion, rather than unimplemented design references.
The complete suite passed **202 tests** in 180.84 s, including 25 new rigid consensus
controls. The two new cookbook blocks executed successfully. The isolated strict
cookbook build, three reporting tests, generated indexes, Ruff and whitespace
checks passed. The same two pre-existing warnings remain. Source-provider pins
are unchanged; these are analytical/integration controls, not comparative timing,
biological, installed-wheel, whole-site or hosted-matrix acceptance.

On **2026-10-03**, #27 adds the public
`from_feature_inventory()`, `get_rigid_feature_placements()` and
`summarize_rigid_consensus()` tools. Native consensus calls the placement tool;
cached queries avoid molecular reads, explicit proposals remain selectable and
saved summaries add no scientific credit. The [modular cookbook recipe](../docs/content/cookbook/modular_rigid_tools.md)
executed all three blocks. The complete scientific suite passed **225 tests**
on Python 3.14.7 in 194.15 s using the installed development environment's
providers without PYTHONPATH overrides; the earlier controlled Python 3.13 run
passed 225 in 218.11 s. These durations use different providers and are not an
interpreter performance comparison. The two previously described warnings remain.

The workspace now uses `molsyssuite@uibcdf_3.14`. Ordinary no-dependency editable
installation succeeds with metadata `>=3.11,<3.15`. The relevant published #23
adoption changes are incorporated across CI, recovery, recipes and installed
qualification, preserving the scientific changes. Nine focused CI/recovery/
reporting tests passed after incorporation. Public-delivery qualification remains
with #23; earlier hosted matrix evidence does not certify this scientific checkout.

All **12 analytical strategy controls** passed in isolated sequential workers,
with one warmup, three timed calls, stable outputs, identical provider hashes and
separate real Ackredit capture for completed calls. The [retained evidence](evidence/README.md)
and [comparison contract](rigid_strategy_comparison.md) record costs and limitations.
The warped square produces zero models from maximal mappings and 16 three-site
alternatives from triplets. Same-domain RMSD controls protect the objective
distinction; those baseline calls execute no G3PS stage. The strict isolated cookbook build passed
with the existing 3.13 Sphinx tools because Sphinx is absent from the 3.14 runtime
environment. This is neither whole-site nor biological acceptance.

On **2026-10-03**, #28 adds [G3PS seed-stage tools](ranked_seed_workflow.md):
`get_feature_pair_dissimilarities()` compares typed distance environments and
`rank_rigid_feature_correspondences()` ranks supplied triplets. The named
ranked_triplet_seeds consumer composes them with existing proposals, MolSysMT
placement and consensus. Default methods are preserved. All seeds retain the
original triplet family; a finite n_seeds records scientific selection, rather
than avoiding an exhausted computation budget. A real-provider reflected typed
tetrahedron proves that one selected seed can miss an existing four-feature fit.
Ackredit credits the adapted G3PS section 2.2.1 and actual SciPy assignment,
with excluded refinement/rescue stages identified in the citation context.

All **22 new controls** passed, including an independent permutation oracle;
the complete scientific suite passed **248 tests** in 209.61 s on Python 3.14.7
using the installed environment providers without PYTHONPATH overrides. The
same two existing warnings remain. The new cookbook executed **four blocks**,
and the isolated strict Sphinx build passed with the existing 3.13 documentation
tools. Index/reporting guards, Ruff and whitespace checks also passed. A controlled
comparison passed all 14 controls, including the intentional baseline budget
failure and ranked selection false negative. Stable outputs, matching worker
source/extension hashes, timings and real citations are retained in
[the evidence archive](evidence/README.md) and the owning workflow. No complete
G3PS, biological, hosted-matrix or public-package acceptance is established.

On **2026-10-03**, #29 delivers [public greedy refinement](rigid_refinement_workflow.md)
and explicit-pair geometric evaluation, shared with ordinary placement. Both
final and each_step angular policies remain available; their counterexamples
favor different policies. Best fully evaluated accepted checkpoints are preserved.
Consensus selects refinement explicitly and summaries count every initial/trial
fit against the remaining global allowance. Actual Ackredit records G3PS section
2.2.2 with the executed policy and excluded rescue/fitting stages.

The complete suite passed **274 tests** in 246.00 s on Python 3.14.7, including
**26 new controls**, with the same two existing warnings. The recipe executed
**five blocks** and the isolated strict Sphinx build passed with existing 3.13
documentation tooling. All **six scientific policy comparisons** passed with
stable traces, unchanged source hashes and real citation capture; their
[retained evidence](evidence/README.md) is a count comparison, not a timing or
memory benchmark. No full-G3PS, biological or public-delivery claim is added.

The expanded refinement validation now passes **22 workload controls**, bringing
the full suite to **296 tests** in 282.81 s on Python 3.14.7 with the same two
known warnings. Eleven workloads vary seeds, angular/spatial tolerances, mixed
classical families, reflection and six/twelve-donor 3D arrangements. All **22
runtime/memory comparisons** passed with one warmup, three timed calls and a
separate real attributed call, stable traces, unchanged inputs/provider sources
and identical worker source/extension identities. The
[measured table and contract](rigid_refinement_workflow.md#measured-expanded-controls-python-3147)
record coverage beside fits, timing and scoped worker RSS. The new retained
archive supplements the original count-only comparison. Both policies remain
available; no universal winner or biological claim is added. Cookbook rendering
passes with the existing 3.13 documentation tooling.

Issue `#30` now owns [prepared real-ligand CCD controls](prepared_ccd_validation.md).
Untouched ideal EST/DES SDFs have source URLs and checksums, and explicit
MolSysMT preparation preserves atom/hydrogen identity, declared stereo/charge,
connectivity and coordinates. Native input recognition retains its missing
aromatic-metadata rejection; the public sanitizing conversion supplies a ready
reference system. Twenty-three new guards bring the full suite to **319 tests**
in 346.44 s on Python 3.14.7 with the same two known warnings. Both refinement
policies recover the selected 5/6 self features. Public consensus and prepared
frame screening work with these real chemical components; three declared
cross-ligand hypothesis choices have different outcomes. All **12 scientific
comparisons** pass with attribution-independent science, preserved inputs,
unchanged sources and actual whole-workflow resource/method citations. Four
new cookbook blocks execute and strict rendering passes with 3.13 tooling.
This retained evidence is count-only and uses ideal reference coordinates;
experimental receptor/preparation, conformer-energy and biological acceptance
remain separate gates.

The observed 1QKU EST ligand now consumes the provider's public chemical-template
assessment/application tools under #22. The frozen MolSysMT-curated artifact
preserves 20 heavy-atom identities and deposited coordinates. The selected
acceptor/aromatic hypothesis has three essential sites; self-placement,
displacement, normal-sign/orthogonal-normal and molecular/query persistence
controls pass. Eight new guards cover preparation, failure, units and actual
Ackredit input/analysis references. The complete suite passes **327 tests** in
333.34 s on Python 3.14.7 with the same two known warnings. Three cookbook blocks
execute on Python 3.14,
with strict isolated rendering using the existing 3.13 tooling. Both host-tracking
profiles produce identical science; full evidence and actual bibliography are
retained in [the evidence archive](evidence/README.md). Stored H counts do not
provide donor geometry; #300 remains the provider's fixed-state H-placement gate.
Receptor, biological and historical OpenMM derivation acceptance remain open.

The next observed-ligand slice consumes the resolved MolSysMT #300 fixed-state
RDKit operation. It adds 24 H to the declared EST state, preserving the 20 observed
heavy-atom identities/coordinates, and returns 44 atoms/47 bonds with two indexed
directional donors. The five essential donor/acceptor/aromatic sites pass self,
position/normal/direction, heavy-only missing-geometry and persistence controls.
Both rigid angular policies recover all five matches in three fits. The expanded
copy's B-factor drop is explicit; original source annotations remain available.
No environment or energy refinement occurs.

The independent eligibility defect under #31 was found and corrected: numerical
mean-centering could treat co-located features as non-collinear at a shifted origin.
Six public-proposal controls now reject those anchors and retain valid identities.
Eleven donor-route guards bring the complete suite to **344 passing tests** in
348.54 s on Python 3.14.7. Six warnings comprise the two existing warnings and four
expected B-factor-drop diagnostics. All 25 focused controls and five new cookbook
blocks pass; strict rendering uses the existing 3.13 tools. Actual bounded Ackredit
captures and identical tracking-independent science are retained in the seventh
evidence archive. Original archives remain unchanged. The provider's legacy session
role/context omission is handed to its existing #27 integration theme; the native
H report retains its original roles/versions. Receptor readiness, environmental
H orientation and biological acceptance remain open under #22.

The observed receptor audit now consumes the resolved MolSysMT #217/#218 public
diagnostics. Label-chain A has 1,990 atoms and 250 groups: 247 assessed and three
heavy-incomplete groups. All 12/19/23 residues in 0.4/0.5/0.6 nm observed-ligand
shells have no reported heavy gap, but still lack complete declared chemistry.
Receptor-only recognition and two full-source detector calls remain genuinely
blocked, with original diagnostics and unevaluated counts. No preparation,
protonation, ligand reinsertion or biological result is inferred. This locates
the next provider requirement in #298: reusable residue/polymer/terminal chemical
assignment, explicit states, inter-group coverage, conflicts and source maps.

Eight new guards bring the complete suite to **352 passing tests** in 376.12 s
on Python 3.14.7, with the same six warnings. Twenty-seven focused receptor/
template/H controls and the final eight receptor guards pass. Three new cookbook
blocks execute on 3.14, and strict isolated rendering passes with existing 3.13
tools. Ruff and offline reporting/index/whitespace checks pass. Actual observed-
data-only Ackredit capture, source preservation and tracking-independent science
are retained in the eighth archive; all seven earlier original archives verify.
No runtime/memory is measured. The library remains installed editable in
`molsyssuite@uibcdf_3.14`; receptor/biological acceptance and review remain open.

The public `get_excluded_volume_sites()` builder under #32 now constructs
independent Sphere constraints from cached native heavy-atom inventories. It
performs no molecular access, enforces explicit uniform radius choices and
retains source correspondence, detached geometry/report data and actual producer
versions independent of optional attribution. Composition reuses public query
methods and the existing strictly-inside heavy-center veto, with no positive
fit weight. Molecular geometry/selection/physical radii remain MolSysMT's domain.

Twenty-two constructor and four observed controls pass. The 153 heavy atoms in
the 19-residue receptor shell yield 153 spheres. A 0.1 nm choice admits observed
EST; a controlled O3-to-OE2 translation is vetoed by one clash while retaining
five positive matches. A 0.35 nm choice vetoes the reference with 12 clashes.
The broad 0.4 nm positive radius isolates this analytical effect; neither radius
is physically or biologically validated. Both alternatives remain explicit.
Native query persistence and source/ligand preservation pass. Receptor chemistry
and successful interaction recognition remain under MolSysMT #298/#22.

The complete suite passes **378 tests in 473.81 s** on Python 3.14.7 in the
confirmed editable `molsyssuite@uibcdf_3.14` environment. Eight warnings are the
six previous warnings plus two expected B-factor drops from the new H-prepared
controls. The final 26 focused controls also pass after adding producer versions
to construction reports independent of optional tracking. Three cookbook blocks
execute on 3.14 and strict isolated rendering passes with existing 3.13 tooling;
Ruff and offline reporting/index/whitespace checks pass. Both driver profiles
preserve science and producer/input identities; the enabled capture retains
15 items/39 uses, including three actually used input datasets. No G3PS or receptor
interaction detector runs. The ninth original evidence archive is retained and
all eight earlier archives verify. No runtime/memory is measured. Review and
public dependency qualification remain open.

The native [ionic observation continuation](ionic_interaction_workflow.md) under
#33 now constructs positive/negative spheres through the shared public feature
inventory. Whole participant membership and geometry membership remain separate;
compound centers, state, actual charge and source geometry mapping are retained.
Repeated contacts aggregate into one site. Existing pose evaluation, persistence
and the independent public exclusion builder compose without a new screening
implementation. Molecular recognition/detection/centroid calculation remain in
MolSysMT; incompatible definitions, cut centers and nonzero images are rejected.

Twenty-four ionic controls bring the complete local suite to **402 passing tests
in 401.75 s** on Python 3.14.7, with the same eight warnings. The expanded 77-test
set passes in 46.14 s. All three cookbook blocks execute under 3.14; strict
isolated rendering passes with existing 3.13 tools. Ruff, reporting/index, three
offline reporting tests and whitespace checks pass. The editable installation
in `molsyssuite@uibcdf_3.14` is confirmed without a PYTHONPATH override.

The driver retains atomic/carboxylate/guanidinium controls in both ligand roles:
six queries and 18 pose evaluations per tracking profile, all reference/round-trip
positives at fit one and displacement negatives at zero. Both profiles preserve
scientific results, coordinates and producer sources. Enabled capture records
9 items/18 uses, without a named ionic-criterion paper; cached detector origin
retains its original bibliography without a new detection claim. The tenth
original archive is retained and all earlier archives verify. No biological or
runtime/memory claim follows. Native aromatic interaction construction remains
the next observed-complex extension; receptor preparation remains with MolSysMT.

The native [aromatic observation continuation](aromatic_interaction_workflow.md)
under #34 now converts pi-pi/cation-pi observations from seven declared profiles.
It reuses public feature inventory construction and the existing placed-pose
evaluator; exact ring membership and explicit singleton-to-compound cation
mapping preserve original roles, charges and observation criteria. The query
geometry remains the shared classical contract, distinct from detector planes
and all-atom cation points. Undefined diagnostic quantities persist through the
supported sealed PyUnitWizard record encoding (#35); site geometry remains finite.

The focused 97-test run passes in 59.37 s on Python 3.14.7. Three cookbook blocks
execute on 3.14 and strict isolated cookbook rendering passes with existing 3.13
tooling. The driver retains 14 case/profile combinations, 28 successful queries
and 84 pose evaluations per tracking profile, plus a separately retained strict
compound-cation conversion failure. Source atom identity, chemical state and
coordinates, as well as producer source hashes, are unchanged. Tracking off/on
preserves science with 6 items/11 uses and 14 items/30 uses respectively, including
the provider-declared method references where actually used. The eleventh original
archive is retained; all ten earlier originals verify. These controls establish
no biological accuracy, universal fused-ring mapping or performance ranking.

The complete local suite now passes **444 tests in 436.36 s** on Python 3.14.7
with the same eight known warnings (six structural B-factor drop controls, one
optional tracking failure and one legacy unit warning). Ruff, reporting indexes,
three offline reporting tests and whitespace checks pass. The editable
`molsyssuite@uibcdf_3.14` installation is confirmed without a PYTHONPATH override.
Review and public dependency qualification remain open; receptor preparation
continues under MolSysMT #298. Combining multiple interaction families in a
prepared complex is a natural next classical composition step.

## Joint native interaction composition (2026-10-04)

The [composition continuation](interaction_composition_workflow.md) under #36
provides independent public `compose_pharmacophores()` and
`from_interaction_collection()`. The latter calls the existing native adapter
and standalone composer; the dispatcher exposes `interaction-collection`.
Default native participant reuse preserves one compatible constraint/weight and
all labeled observations. Generic `keep` remains available. Source/constraint
conflicts raise without silent averaging, weight inflation or partial hypotheses.
Copies and component snapshots are independent; no molecular access occurs during
cached model composition. Molecular operations remain in MolSysMT.

The driver passes actual five-family detection, an alternative pi-pi profile and
a covered-empty ionic analysis: seven analyses, 23 observations and nine reused
constraints, compared with eleven explicit kept constraints. Both tracking
profiles retain nine independent pose/persistence/veto evaluations; producer
sources, declared atom identity/state/coordinates and metadata remain unchanged.
Real capture retains 5 items/21 uses off and 13 items/50 uses on, including
actually reached provider references. The twelfth original evidence artifact is
retained. Three cookbook blocks execute on Python 3.14.7 and strict isolated
rendering passes with existing Python 3.13 tooling. These disconnected controls
are not a chemical ligand or biological binding complex.

The corrected complete local tree passes **476 tests in 452.91 s** on Python
3.14.7, including all 32 composition controls, with the same eight known warnings.
Ruff, generated indexes, three offline reporting tests, whitespace checks and all
twelve original archive hashes pass. The editable `molsyssuite@uibcdf_3.14`
installation is confirmed without a PYTHONPATH override. Review/incorporation,
public dependency delivery and biological complex acceptance remain separate.

## Complete CCD interaction continuation (2026-10-04)

The [complete CCD continuation](ccd_interaction_workflow.md) under #37 applies
the existing public observation, collection/composition and pose-evaluation tools
to full EST/DES graphs in two explicit rigid-copy placements. Public MolSysMT
owns source preparation, shared feature geometry, translation, merge and component
projection. Both full molecule roles preserve states, explicit H, atom identity,
bonds, coordinates and source bytes. Six named analyses retain neutral empty
ionic/cation-pi families and original alternative ring-profile evidence. No new
product API, molecular reconstruction or borrowed placement/composition citation
is introduced.

The four pairs produce 10/11 EST and 16/18 DES sites in either role. Positive
references fit one; displacement gives zero. Keep and participant reuse remain
explicit different hypotheses. Donor-H negatives fail one directional essential
while the unchanged acceptor role passes. DES ring-offset retains its actual
single .05 nm exclusion clash in both roles despite full positive fit; the radius
is not changed to force acceptance. These designed ideal-coordinate pairs are
not protein complexes or biological benchmarks.

Thirty controls pass on Python 3.14.7 in 129.47 s. Concurrent live MolSysMT edits
invalidate the source-stability gate of the initial driver runs despite passing
science. A complete-file-verified temporary MolSysMT package snapshot therefore
qualifies the definitive evidence; installed version metadata alone does not
identify its dirty origin. The same 30 controls pass there in 137.39 s.
PharmacophoreMT remains the editable package in `molsyssuite@uibcdf_3.14`.

The definitive driver passes eight primary role hypotheses and 48 pose evaluations
per tracking profile, with identical science, unchanged producer sources,
input fingerprints and metadata. Actual captures retain 9 items/28 uses off and
17 items/57 uses on, including consumed CCD data and reached method references.
The thirteenth original evidence artifact and summary are retained; all thirteen
archives verify. Three cookbook blocks execute on 3.14 and strict isolated cookbook
rendering passes with existing Python 3.13 tooling. Provider source identity and
scope are recorded in the [evidence index](evidence/README.md).

The complete live-checkout suite passes **506 tests in 634.91 s** with the same
eight known warnings. Its explicit source audit fails because MolSysMT changed
during the run; the supplemental audit/log preserve this result, which is not
fixed-provider qualification. The definitive driver and 30 focused controls use
the independently verified stable snapshot. Ruff, generated indexes, three offline
reporting tests and whitespace checks pass. Review/incorporation, public dependency
delivery and the actual ERalpha complex acceptance gate under MolSysMT #298 remain
open.

The next classical steps also include provider-supported conformer preparation and
ligand/complex consensus. Prepared multi-conformer screening is delivered locally;
conformer and chemical-state generation remain the molecular provider's
responsibility.
Reference-anchored consensus over prepared aligned ligands is delivered locally.
Bounded aligned clique discovery with alternative jointly supported models is
also delivered locally. The first explicit-pivot rigid unaligned workflow is now
delivered with two baseline proposal families and explicit ranked-triplet selection.
Review these contracts and compare tolerance-valid coverage and resource costs
before expanding to translation rescue or prepared
multi-conformer consensus. Global continuous/multiple-pivot alignment and geometric
deduplication need independently declared methods and controls.
Structure-based hypotheses need the TopOMT/MolSysMT boundary. Direct molecular
operations remaining in legacy code must be migrated to MolSysMT; missing
provider capabilities must be tracked there, never copied here.

The [roadmap](roadmap.md) gives the current implementation order.
[Growth contracts](extensible_modeling_contracts.md) record the accepted separation
of scientific method, compute backend and execution plan. Dynamic, specialized
and generative approaches remain objectives after the classical acceptance gate.

## Cached-model curation continuation (2026-10-04)

The [curation contract](pharmacophore_curation_workflow.md) under #38 introduces
public local-site selection, independent copying, extraction and explicit
constraint editing. Class setters delegate to the editor. Molecular-system links
remain references; no molecular query, copy or transformation runs in curation.
Extraction/editing retain complete native source snapshots, mappings and original
observations/bibliography, invalidate score, and nest earlier changes. Copying
preserves score. Atomic input validation, independent shape geometry, actual
radius versus Gaussian width and essential/weight/exclusion meanings are guarded.

The focused run passes 54 tests in 42.68 s on Python 3.14.7, including 36 new
curation controls. Three cookbook blocks execute with stable recorded producer
sources. Strict isolated rendering passes with existing Python 3.13 documentation
tooling. The fourteenth original evidence artifact retains complete original and
edited models, seven evaluations, actual capture, original logs and the exact
executed runner. Pure cached steps add no new citation use; length editing
captures two items/two uses, with original bibliography retained in history.

Native YAML controls additionally exposed NumPy literal strings emitted as Python
objects. The #25 correction normalizes builtin text at the shared portable
boundary and uses safe YAML output, preserving literal content and quantity
objects independently. No existing saved record is rewritten. These are local
curation controls, not biological validation, automatic weight fitting or a
performance ranking. Bounded native participant reuse precedes curation; generic
keep composition retains explicit curated alternatives.

The complete tree passes **542 tests in 730.39 s** on Python 3.14.7, with eight
existing warnings. Its explicit source audit fails because Ackredit changes
during the run; PharmacophoreMT, the verified MolSysMT snapshot and PyUnitWizard
remain unchanged. This successful test run is not four-provider fixed-source
qualification. The original failed audit and passing test log are retained
separately from the stable cookbook result. All fourteen original archives verify;
the editable installation is confirmed without a PYTHONPATH override. Review,
public distribution and biological acceptance remain separate.

## Publication integration checkpoint (2026-10-06)

The accumulated native modeling/screening/attribution/curation work, ERalpha
pilot, cookbook, frozen inputs and fourteen original evidence archives are
integrated with the sixteen intervening upstream governance commits. The current
canonical guides, suite-policy caller and Python 3.11–3.14 contract are preserved.
Git attributes retain checksum-qualified input/evidence bytes, including original
logs; all fourteen archives and original input/evidence bytes verify unchanged.

Owner adoption of #39 separates invariant chemistry from appended operation
history and strengthens the original-source guard. Current MolSysMT #346 query
vocabulary is consumed through public between_selections; detector selection
semantics and saved scientific metadata are unchanged. CI source pins identify
the current providers selected for native integration without bypassing metadata.

The three ERalpha pilot modules pass 27 controls in the initial selection, which
also exposes ten curation setup errors from the retired query name. After its
migration, all 164 affected interaction/composition/CCD/curation controls pass
in 231.78 s. The strengthened repeat-H guard and six CI controls pass seven
tests in 7.26 s. Ruff, reporting/index and whitespace checks pass. Execution uses
normal editable installation in molsyssuite@uibcdf_3.14 without PYTHONPATH overrides.
The original logs and provider/file identities are retained in
`evidence/publication_20261006.json`. Historical full-suite results remain dated;
today's selected checks do not certify the new full hosted matrix.

Whole-workspace pip check reports unrelated installed auxiliary-package conflicts,
handed to the owning shared workspace in MolSysSuite #52. Its
[receipt](https://github.com/uibcdf/molsyssuite/issues/52#issuecomment-6026983063)
does not identify a PharmacophoreMT dependency failure or qualify the canonical
environment recipe. Hosted exact-head evidence remains tracked by #9/#23;
public package delivery and biological acceptance remain separate.

## Working references

Read the repository tooling guides and [API standards](api_design_standards.md).
Use the active issue-backed queues for current work and the reporting protocol
for acceptance/archival. The older detailed classical specification retains a
backlog catalog; its local chemistry/automatic preparation directions are
superseded by the current ownership contracts.
