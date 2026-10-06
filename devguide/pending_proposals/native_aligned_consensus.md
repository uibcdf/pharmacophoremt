---
summary: Implement reusable reference-anchored consensus for prepared aligned ligands.
issue: uibcdf/pharmacophoremt#21
status: active
opened: 2026-10-02
closed:
verification: measured
area: [modeling, consensus]
guard: tests/test_aligned_consensus.py
normative: devguide/aligned_consensus_workflow.md
blocked_by: []
supersedes: []
---

# Native aligned-ligand consensus

## What

The first native multi-ligand method builds reference-anchored consensus over
prepared inputs in a declared common frame, separating reusable feature matching,
explicit-group aggregation and molecular workflow orchestration.

## How

`get_aligned_feature_matches` uses bounded SciPy assignment for typed compatible
features; `get_consensus_sites` counts unique declared identities and aggregates
feature centers with retained reference orientations and rejection evidence.
`from_aligned_ligands` obtains all molecular inventories through MolSysMT-supported
`get_features`, calls both tools and builds native Feature + Shape sites.

## Why

A small independently verifiable native method is needed before assessing future
clique discovery. Reference ordering must not be confused with type ordering,
conformer counts with ligand support, or seed coordinates with aggregate centers.

## What is measured and what is assumed

The focused guard passed 17 analytical/real-provider tests locally, including
independent exhaustive assignment controls and native persistence/attribution.
The final full-suite/documentation evidence is retained in the checkpoint.
Inputs being prepared/aligned and dataset ligand identities are declarations;
the method does not establish their biological correctness or chemical uniqueness.
No public distribution, biological pilot or performance result is claimed.

## Alternatives and refuted paths

Nearest-first matching loses valid correspondences in a bounded counterexample.
Do not repair the legacy hybrid by silently adjusting bins or infer its claimed
completeness. Generic angular means are not copied into PHMT; reference orientation
is an explicit first-method contract. No hidden molecular alignment/preparation.

## Scope and exclusions

Reference-anchored aligned consensus and independently reusable intermediate
tools. No patterns absent from the reference, alternative-optimum enumeration,
joint reassignment, new clique method or conformer/state generation. Legacy
correction/replacement remains with #18; evidence publication with #20.

## Acceptance criteria

Review the new public contracts/metadata, pass independent controls and an
executed cookbook recipe, preserve molecular/provider ownership and portable
attribution. Local implementation is delivered; issue remains open for scientific/
API review and broader acceptance.
