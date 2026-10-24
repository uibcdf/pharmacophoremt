---
summary: Compare training-only rigid consensus against a frozen reference on new assay CIDs.
issue: uibcdf/pharmacophoremt#64
status: partial
opened: 2026-10-24
closed:
verification: measured
area: [validation, modeling, mvp]
guard: devtools/tests/test_esr1_consensus_declaration.py::TestEsr1ConsensusDeclaration::test_frozen_declaration_reconstructs_original_sources_and_excludes_exposed_cids
normative: devguide/esr1_consensus_comparison.md
blocked_by: []
supersedes: []
---

# Training-only consensus versus frozen reference

## What and why

Continue the scientific MVP after the bounded #62 pilot and #63 scoring contract.
The observed pilot cannot become a fresh holdout after criterion development.
Declare a separate comparison using three new training actives and 64 previously
unscreened evaluation CIDs from the original primary assay source.

## Delivered pre-score slice — 2026-10-24

The [protocol](../esr1_consensus_comparison.md),
[declaration](../../tests/data/esr1_consensus_comparison/declaration.json) and
[standalone declaration driver](../../phmt_test_support/esr1_consensus_declaration.py)
freeze all IDs and methods before any new structure acquisition or molecular
calculation. They use unchanged archived PubChem AID 743075 v2 responses and
exclude the entire Bath source CID population plus all conflicting assay CIDs.
Three active CIDs train; 16 other actives and 48 inactives evaluate. Lowest-SID
representatives and hash ordering are independent of source row order.

Baseline is the exact original #62 query with explicit seed-only binary ranking.
Native rigid consensus uses only the three training inputs, a fixed pivot,
association cliques, at least two jointly supporting ligands and three sites,
and declared finite budgets. One model is selected using training-only site and
support counts with deterministic ties. Every training prerequisite and a native
training-hit readiness check must pass before evaluation opens. No fallback,
replacement, relaxed bounds or tuning on evaluation outcomes is permitted.

Two offline guards pass: original-source reconstruction of all 67 frozen IDs,
counts, source/query identities and no-clobber CLI; and synthetic conflicting/
inconclusive labels, row-order/lowest-SID selection and insufficient-input failure.
This is executed declaration verification, not measured molecular science.
The complete administrative/documentation selection passes 40 tests and 24
subtests, including strict Sphinx; three reporting tests, whole-tree Ruff and
generated indexes pass. Declaration SHA-256:
`a1a476e7e94fd3480ee3845fbc5cca138221c4052eb7165a254499fd526ff647`.

## Ownership and limitations

MolSysMT owns all molecular I/O, preparation, states, identity/coordinate controls
and fits. PHMT owns pharmacophore hypotheses, method/model choice and study
interpretation. No runtime molecular routine or optional engine is introduced.
The new source script is unshipped case orchestration; existing archive reading,
source retention and scientific APIs are reused, not replaced.

Source/issue inspection found no identified reusable molecular identity/scaffold
overlap tool. The concrete proposal is
[MolSysMT #447](https://github.com/uibcdf/molsysmt/issues/447), linked to this
consumer. The study does not block on that proposal, but only claims external-CID
separation, not chemical-series or independent-assay validation. Existing
conformer/stereo/environmental-H work stays with its provider issues.

## Remaining acceptance and next action

The executable training driver is `phmt_test_support/esr1_consensus_training.py`.
It reuses the original case's HTTP/identity/serialization and existing MolSysMT
preservation checks; the latter are moved without changing their operations
(verified by AST comparison after explicit feature injection). Two additional
offline guards restrict requests to the three training CIDs, preserve HTTP
failures/refuse substitutions and protect the fixed training-only model order.
It contains no evaluation acquisition/scoring mode. This establishes executable
orchestration, not a scientific result before its opt-in run.

Acquire and retain only the three training structures, qualify MolSysMT
preparation and execute native consensus in an owned public-provider environment.
Retain all failures and alternatives; commit the selected valid query and full
training evidence before any evaluation structure/score acquisition. If training
cannot produce a usable query, record that outcome and keep evaluation unopened.

After valid frozen queries, execute paired screening with all failures, per-arm
and common-subset denominators, independent metric/accounting guards, exact
runtime/source provenance, actual attribution and portable original outputs.
No new result is claimed by the declaration. Keep this issue partial for those
scientific execution stages; addon and release infrastructure remain deferred.
