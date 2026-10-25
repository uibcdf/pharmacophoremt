# ERα comparison: training-only consensus and previously unscreened CIDs

Owned by [#64](https://github.com/uibcdf/pharmacophoremt/issues/64), maintainers
`LMMV` and `dprada`. This is a **pre-score protocol**, not measured validation.
The [declaration](../tests/data/esr1_consensus_comparison/declaration.json) is the
parameter and input-ID authority. The standalone
[declaration driver](../phmt_test_support/esr1_consensus_declaration.py) reproduces
it from unchanged archived source bytes without scientific imports or network.

## Question and separation

Compare the unchanged original #62 query against one native rigid consensus
learned from three new active compounds. The primary descriptive comparison is
the difference in ROC AUC on the common successfully evaluated subset. Preserve
separate per-arm and paired denominators and all missing/failed outcomes.

Use original PubChem AID 743075 v2 assay outcomes, not docking/imputed potency.
Exclude all 4,402 unique CIDs in the complete Bath ESR1ago table, not just the
32 original pilot inputs. Exclude every assay CID with multiple outcome values,
including conflicts with Inconclusive. This removes 370 conflicting assay CIDs
globally. Among the remaining CIDs outside Bath there are 338 Active and 2,749
Inactive candidates. Select the lowest numeric SID for each consistent CID;
source row order cannot determine its representative or split.

Order each class by SHA-256 of `phmt-esr1-consensus-comparison-v1:<CID>`.
Training uses the first three actives: 31477, 24633 and 6293, in that order.
The next 16 actives and first 48 inactives are reserved for evaluation. There
are 67 distinct selected CIDs, no replacement after any failure. Labels are
used for stratified sampling; no new molecular features/scores or evaluation
outcomes have informed the protocol. This is the same assay, not independent
experimental replication; different CIDs do not establish chemical-series,
state, stereo or near-analog independence.

Molecular identity/scaffold annotation belongs in MolSysMT. The proposed reusable
capability is [MolSysMT #447](https://github.com/uibcdf/molsysmt/issues/447), after
source/issue inspection at sibling `48aba006fbe17336dfb5f564823711c2923f7e0b`.
No local RDKit identity, scaffold, normalization or similarity routine is added.
That proposal is not a blocker for the explicitly bounded CID-only study; it
is needed before making stronger molecular-independence claims.

## Training before evaluation

1. Commit this declaration before acquiring any new structure. Acquire only
   the three training PubChem computed 3D SDF responses first, retaining exact
   bytes/hashes, dates, attribution and failures. Do not retry with another CID.
2. Public MolSysMT reads/prepares the supplied state through the already used
   SDF → MolSys → RDKit → MolSys conversion route, with explicit stereo handling
   and input/state/atom/coordinate preservation controls. No local parser,
   conformer generation, protonation or standardization. Retain failures.
3. All three training inputs must prepare. Call native `from_rigid_ligands`
   with `association_cliques`, pivot index 0, the three declared feature families,
   `min_matches=3`, `min_support=2`, `min_sites=3`, no refinement and the exact
   tolerances/budgets in the declaration. Resource exhaustion is failure, not
   empty completed discovery. Keep every alternative and full report.
4. Select exactly one model by descending site count, descending hypothesis
   `joint_support_count`, then ascending `layout_id` and `hypothesis_id`.
   Selection uses training evidence only. The selected query must yield a native
   `seeded_hit` on at least one training input. If this readiness check fails,
   do not try the next model or relax parameters.
5. Commit full training results and the selected query's exact hash before
   acquiring evaluation structures or computing their pharmacophore scores.
   If training preparation, discovery or readiness fails, preserve the result
   and keep evaluation unopened. A later protocol is a distinct declared run.

## Evaluation and claims

Both frozen queries use `RigidPoseSearch(search_method='seeded_hit')` and
`seeded_hit@1`, 10,000 raw trials, point tolerance 0.10 nm, direction tolerance
30 degrees and minimum fit 0. Valid completed negatives score zero; a missing
pose is not fabricated; failed/unresolved inputs remain unscored. Do not optimize
query, model, features, thresholds, preparation, method or budgets on evaluation.

Report all 64 reserved inputs, per-arm and common-evaluable subsets, failures,
AUC, tie-aware EF at 10%, BEDROC(alpha=20) and hypothetical missing-score AUC
sensitivity. Metrics requiring both classes are undefined if a class is absent.
These are descriptive results on one small, selected assay cohort, not confidence
intervals, affinity, full-benchmark enrichment or predictive acceptance.

The planned public-provider route reuses MolSysMT 0.23.0 and the existing
[325-record environment](evidence/seeded_ranking_environment_20261024_explicit.txt),
with the exact current PHMT source installed editable. Its base PHMT 0.4.0 record
does not identify executed source. Record actual versions/origins, source and
native-extension hashes, dirty overlays and actual Ackredit captures for new runs.
No scientific environment is created or qualified by declaring this protocol.

## Reproduce the declaration

Restore original source responses with the existing case reader into a **new**
directory, then generate a distinct declaration output:

```bash
python phmt_test_support/esr1_activity_pilot.py \
  --data-dir /tmp/esr1-comparison-sources --restore-archive
python phmt_test_support/esr1_consensus_declaration.py \
  --source-dir /tmp/esr1-comparison-sources \
  --output /tmp/esr1-comparison-declaration.json
cmp tests/data/esr1_consensus_comparison/declaration.json /tmp/esr1-comparison-declaration.json
```

The driver verifies the original manifest and all three source-response hashes;
it refuses to overwrite its output. The offline guard reconstructs the frozen
split from the checksum-qualified archive, tests conflicting/inconclusive IDs,
row-order independence, lowest-SID selection, changed sources and no-clobber CLI
behavior. No molecular workload or new citation registration runs in these checks.

## Execute only training

The opt-in `phmt_test_support/esr1_consensus_training.py` verifies the exact
committed declaration and restricts acquisition to its three training entries.
Use a new input directory. Preserve the acquisition receipt and every response,
including HTTP errors; it never retries with another CID. Run the scientific
stage by path against an owned environment with the declared public providers
and exact editable PHMT source:

```bash
python phmt_test_support/esr1_consensus_training.py \
  --data-dir /tmp/esr1-training-inputs --acquire
/tmp/esr1-training-env/bin/python phmt_test_support/esr1_consensus_training.py \
  --data-dir /tmp/esr1-training-inputs --output /tmp/esr1-training-run.json
```

The second command revalidates all input bytes, reuses the original pilot's
MolSysMT preservation orchestration, retains preparation/consensus/readiness
failures and verifies producer/runtime stability. `status='stopped'` is a
retained scientific/readiness outcome, not a successful query. Only `ready`
supports a later evaluation stage after committing the evidence. The native
query, when available, is saved beside the run. Existing outputs are refused.
This driver has no evaluation acquisition/scoring mode.

Deeper docs, addon and release work remain deferred. Original #62/#63 outputs
stay immutable; new measurements require separate run identities.

## Measured original attempt — 2026-10-24

The [training summary](evidence/esr1_consensus_training_20261024_summary.json)
retains an executed stop at preparation. CID 24633 returns PubChem 3D HTTP 404;
31477 and 6293 prepare and pass all preservation controls with public MolSysMT
0.23.0. No consensus, new query, readiness screening or evaluation is executed.
The [case](../docs/content/validation/esr1_consensus_comparison.md) and owning
report qualify original inputs, all outcomes, versions and actual attribution.

This is the predeclared stop, not permission to replace an input or relax the
all-three rule. The 64 evaluation inputs remain unopened. A new attempt requires
a separately frozen training-readiness policy before additional acquisition;
retain this declaration, original 404 and original full output unchanged.

## Attempt 2: bounded training readiness — declared 2026-10-24

The separate [readiness declaration](../tests/data/esr1_consensus_comparison/readiness_declaration.json)
preserves the original attempt and its terminal stop. Its SHA-256 is
`b8ff6305ed7527289dad6ee13f7992b74928d93738c6f290fbdeff4099b1757e`.
It reuses the exact original 64 evaluation records, baseline query, preparation
route, consensus parameters/model ordering, screening and comparison criteria.
No evaluation structures or scores have been examined.

The fixed candidate pool contains 12 training-only actives in the existing hash
order: original first three, followed by active positions 19:28 (zero-based),
skipping all 16 reserved evaluation actives. CIDs are 31477, 24633, 6293,
9818306, 123504, 5857, 443831, 13765, 6422843, 17701, 6327657 and 70400.
The original three acquisition responses are reused without refresh, including
the known 404. Only the other nine are requested, once each. The known original
training observations are exposed development evidence, not fresh validation.

Prepare and retain every candidate using the same public MolSysMT route and
preservation checks. Eligibility requires completed acquisition and successful
preparation/feature-inventory operation; it has no minimum feature-count,
geometry, pharmacophore-support, similarity or screening-score threshold.
Select the first three eligible candidates in the declared order **before**
consensus. Their first member is the fixed pivot. Do not test another trio,
pivot, model, budget or threshold if consensus or selected-query readiness fails.
Fewer than three eligible inputs also stops the attempt. The pool cannot expand.

This conditions training on public-input availability/provider readiness, rather
than treating the original missing CID as replaceable within attempt 1. It does
not filter or replace evaluation inputs; their failures will remain unscored.
All candidates, failures, selected identities and full consensus alternatives
must be retained. A valid query and complete training evidence must still be
committed before evaluation opens.

Reproduce the new declaration from the same original source directory with
`phmt_test_support/esr1_consensus_readiness_declaration.py --source-dir <sources>
--output <new-json>`. It verifies attempt 1's original declaration, source bytes
and retained acquisition identity and refuses output overwrite. The existing
training runner supports the second frozen declaration explicitly:

```bash
python phmt_test_support/esr1_consensus_training.py \
  --declaration tests/data/esr1_consensus_comparison/readiness_declaration.json \
  --data-dir /tmp/esr1-readiness-inputs --acquire
/tmp/esr1-training-env/bin/python phmt_test_support/esr1_consensus_training.py \
  --declaration tests/data/esr1_consensus_comparison/readiness_declaration.json \
  --data-dir /tmp/esr1-readiness-inputs --output /tmp/esr1-readiness-run.json
```

## Execute the frozen paired evaluation

After the valid query/training archive is committed, use the opt-in
`phmt_test_support/esr1_consensus_evaluation.py`. It restores both exact queries
through the existing checksum reader and verifies the ready training receipt
before acquiring any evaluation input. Use a new directory and retain every
one-request response/error. No source refresh, replacement, training or model
selection occurs in this stage.

```bash
python phmt_test_support/esr1_consensus_evaluation.py \
  --data-dir /tmp/esr1-paired-inputs --acquire
/tmp/esr1-training-env/bin/python phmt_test_support/esr1_consensus_evaluation.py \
  --data-dir /tmp/esr1-paired-inputs --output /tmp/esr1-paired-run.json
```

Public MolSysMT prepares the supplied systems once using the declared route.
Each query's native `RigidPoseSearch` and `RetrospectiveValidator` receive the
same successfully prepared systems. The original 64-input ledger separately
retains unavailable acquisitions and preparation failures as unscored, with
their original causes; they are not converted into placeholder molecular inputs
or fabricated native search failures. Native-report input indices/counts refer
to the prepared subset; the driver keeps an explicit mapping to original cohort
indices. Search failures stay in the native report and original ledger.

The driver uses public native metrics for each arm and the common-evaluable
subset, without rerunning search to calculate paired metrics. Report the
consensus-minus-baseline AUC difference on that common subset. Binary missing-
score sensitivity assigns only hypothetical 0/1 extremes by true label; it is
not observation imputation or a confidence interval. Empty/single-class metric
limitations remain explicit.

Before evaluation, actual product/provider file hashes must match the qualified
training runtime exactly. Read-only MolSysMT observations check that coordinates,
chemical states, atom IDs and elements stay identical across both arms. These
are case integrity checks, not chemical-equivalence/scaffold analysis. Original
full results, a preparation journal, all native outcomes, input mapping and actual
attribution are retained. Existing output/journal paths are refused. The retained
editable version metadata identifies the unchanged training library; the new
evaluation driver and its actual Git producer are recorded independently.

## Completed result and reusable follow-up

The [paired summary](evidence/esr1_paired_evaluation_20261024_summary.json)
and [case](../docs/content/validation/esr1_consensus_comparison.md) retain the
completed 64-input comparison: 45 common evaluable compounds, 19 unavailable
3D records, AUC 0.4848/0.5530 and descriptive difference +0.0682. All original
failure causes and independent metric/index/integrity checks are preserved.
This closes the bounded #64 workflow, not biological predictive acceptance.
The environment retained during training is retired after this phase; the
original source snapshots remain historical and unchanged.

The case demonstrates a reusable PHMT validation need: original-cohort/saved-
evaluation/unscored-input aggregation and paired common-subset reporting.
That product proposal is [#65](https://github.com/uibcdf/pharmacophoremt/issues/65).
The current case-only ledger remains an explicitly bounded interim consumer
under LMMV/dprada, review 2026-11-07; future consumers migrate to a qualified
native operation, while historical driver commits remain available for replay.
No molecular operation or generic environment-management workaround is added.
This observed cohort cannot become unseen validation after future tuning.
