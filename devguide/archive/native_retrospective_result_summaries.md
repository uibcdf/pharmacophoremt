---
summary: Reuse saved native evaluations with original-cohort and unscored-input accounting.
issue: uibcdf/pharmacophoremt#65
status: resolved
opened: 2026-10-24
closed: 2026-10-24
verification: measured
area: [validation, screening]
guard: tests/test_saved_results.py::test_original_sparse_indices_distinct_samples_and_native_failure_are_preserved
normative: devguide/api_design_standards.md
blocked_by: []
supersedes: []
---

# Native retrospective summaries from saved results

## What and why

The completed #64 comparison has 64 original inputs but only 45 prepared
systems. Its unshipped case driver composes native search, RetrospectiveValidator,
get_screening_score and public metrics, then maintains original indices/causes
and common-evaluable subsets locally. This demonstrates a reusable PHMT validation
need. Existing #12 repairs metric math and native batch accounting; this is an
extension for saved results and upstream unavailable/preparation-failure records.

## Proposed owner and contract review

Inspect existing public operations first. Define an independently useful native
summary consuming an explicit original cohort/labels, detached native results
and their index mapping, plus explicit unscored causes. Compose existing score
and metric contracts; retain original/evaluated/unscored class counts, criteria,
producer and actual attribution. A common-evaluable paired comparison may be a
separately useful operation. Do not rerun molecular search to read saved results.

Review sparse/duplicate/unknown mappings, repeated source objects with distinct
sample indices, label conflicts, empty/single-class subsets, ties, compatible
score criteria, complete negatives without fitted poses and missing/search
failures. Recomputed metrics have their own reached attribution; reading source
evidence does not credit its calculation again. No molecular I/O, scaffold,
normalization, preparation or new engine is introduced. This belongs in PHMT
validation and does not require a MolSysMT implementation change.

## Evidence and bounded interim disposition

The #64 [paired summary](../evidence/esr1_paired_evaluation_20261024_summary.json)
and `phmt_test_support/esr1_consensus_evaluation.py` are concrete consumer
evidence. The original consumer guard protects original/native-index separation;
the selected public-tool guard now protects the implemented native contract.
Original declarations/outputs are immutable.

At issue opening the case-only ledger was an interim consumer owned by
LMMV/dprada, review 2026-11-07. The new saved-evidence consumer now calls the
qualified native tool. Future statistical consumers use this public operation;
the original #64 driver/ledger is retained only for exact historical experiment
replay. Its producer and original scientific measurements are never relabeled as
new API adoption. No public runtime workaround is introduced.

## Acceptance

Public documented contracts, reusable owner implementation using existing
scientific tools, analytical tie/failure/index oracles, saved-result/no-molecular-
work controls and a consumer using the existing #64 evidence. Do not rewrite
historical measurements as adoption of the new API. These local API/consumer
criteria are met below. Hosted/installed/public delivery remain separate;
no extra environment or new public release is claimed.

## Implementation and initial verification — 2026-10-24

`validation.summarize_screening_results` composes get_screening_score and the
existing metrics using explicit original records, native/original mapping,
upstream causes and separate source metadata. It retains complete class and
failure denominators. `validation.compare_screening_results` requires the same
criterion and recomputes common-scored-subset statistics. Sparse indices and
repeated source IDs remain distinct observations; incomplete/unknown/duplicate
or overlapping mappings and label conflicts raise. Undefined metrics are None.
Native errors and upstream causes remain separate. New calculations receive
their own reached attribution without recrediting source calculations.

84 saved-result/metric tests pass in canonical Python 3.14.7, including analytical
tie/failure controls and real Ackredit sessions plus optional absent/broken
provider behavior. A preliminary new consumer replay of the immutable #64 archive
reproduces all original counts, indices, labels/scores, arm metrics, common AUC
delta and binary missing-score sensitivity; native/source records stay unchanged.
Permanent clean-producer evidence and administrative/documentation qualification
remain pending. The driver is `phmt_test_support/replay_esr1_saved_results.py`;
it calls the public tool and does not rerun molecular work. The original #64
driver, declarations and outputs are unchanged.

## Completed clean-source verification — 2026-10-24

Implementation/consumer commit `e32c80e0cbc9837e8badcda2b7c93f22d30f1ddc`
is pushed to main. The separate clean-source replay has empty Git status and
records current module origins, actual package metadata, runtime file hashes and
newly reached attribution. Its original scientific producer remains
`012544472e8eca27d1646a6e8065ee22872d4368`, with all original provider records and
source attribution intact. Current workspace metadata still has its old editable
PHMT version; source identity is the recorded commit/file hashes, not a new
release. No molecules are prepared, transformed or searched by the replay.

The [new summary](../evidence/esr1_saved_summary_replay_20261024_summary.json)
qualifies the new compressed output (raw SHA-256
`d8104d4019c908dfd01345158e7440880d2a26c3e356662248b5322196005da4`).
Both native arms retain 64 original inputs (16 active / 48 inactive), 45 scored
(12 / 33), 19 upstream unscored (4 / 15), zero native failures and the unchanged
original mapping, labels, scores and causes. Arm/common AUC, BEDROC, EF10%, AUC
delta and missing-score sensitivity match #64. Actual newly captured attribution
contains summary/scoring/metric operations, without source recognition/fitting.
The new offline guard
`devtools/tests/test_saved_results_replay.py::TestSavedResultsReplay::test_clean_native_replay_preserves_original_counts_metrics_and_provenance`
checks original archive identity, independent retained values, complete counts,
source producer and reached credit. Existing #64 independent numerical-oracle
controls remain in place.

84 selected scientific tests pass in canonical Python 3.14.7; the final complete
administrative run passes 50 tests plus 26 subtests, including strict Sphinx and
the new offline replay guard. Its collection imports the checksum reader by file
without populating the installed-test support namespace, preserving that gate's
isolation. Reporting/index/Ruff/whitespace checks pass. The deliberately broken
optional-provider test retains its catalog warning and scientific result.
Implementation CI 40147016165 is queued at observation; policy 40147016265 and
Conda governance 40147016227 succeed. These local results do not stand in for a
new full hosted/installed matrix; follow #9 for exact-head receiving. Public
0.4.0 remains unchanged, so no new release-specific MolSysSuite notice is due.

Recheck the local gates with the canonical interpreter:

```bash
python -m pytest -q tests/test_saved_results.py tests/test_validation_metrics.py
PHARMACOPHOREMT_SUITE_ROOT=/tmp/phmt-installed-qualification-1wwqno5j/sdk-installed python -m pytest -q devtools/tests
python devtools/devguide_index.py --check
python -m unittest discover -s tests -p test_reporting_protocol.py
python -m ruff check .
git diff --check
```

The shared SDK root remains an existing external resource, not a new task-owned
environment. No environment cleanup or shared-prefix modification occurs.
