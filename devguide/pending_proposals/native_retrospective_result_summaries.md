---
summary: Reuse saved native evaluations with original-cohort and unscored-input accounting.
issue: uibcdf/pharmacophoremt#65
status: open
opened: 2026-10-24
closed:
verification: asserted
area: [validation, screening]
guard: devtools/tests/test_esr1_consensus_evaluation.py::TestEsr1ConsensusEvaluation::test_prepared_native_indices_keep_failed_originals_and_class_order_distinct
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
evidence. The selected guard protects the existing original/native-index
separation; it is not proof of an implemented future public summary API.
Original declarations/outputs are immutable.

The case-only ledger remains an interim consumer until a native contract is
reviewed/qualified. Owners LMMV/dprada; review 2026-11-07. No public runtime
workaround is introduced. Future consumers migrate to the qualified native tool;
retain historical driver commits for exact replay.

## Acceptance

Public documented contracts, reusable owner implementation using existing
scientific tools, analytical tie/failure/index oracles, saved-result/no-molecular-
work controls and a consumer using the existing #64 evidence. Do not rewrite
historical measurements as adoption of the new API. Contract/implementation
work has not started; no extra environment or public delivery is claimed.
