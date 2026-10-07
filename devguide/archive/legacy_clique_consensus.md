---
summary: Legacy distance partitioning and clique support disagree with the matching criterion.
issue: uibcdf/pharmacophoremt#18
status: resolved
opened: 2026-10-02
closed: 2026-10-07
severity: high
verification: measured
area: [modeling, consensus]
guard: tests/test_ligand_based_facade.py
normative: devguide/ligand_based_workflow.md
blocked_by: []
supersedes: []
---

# Audit legacy recursive partitioning and clique consensus

## What

The legacy modeler drops accepted candidate pairs at bin boundaries, duplicates
candidates after overlapping partitioning, permits same-ligand edges and emits
maximal cliques without checking distinct-ligand support. It sorts feature names
without canonicalizing geometry and builds a seed model rather than aligned
consensus centers. Direct molecular operations remain outside the provider.

## How

Run `python devtools/audit_legacy_cliques.py` in the controlled development
environment. The bounded helper audit reports pair RMSD 0.10 nm but no surviving
boxes, four entries for two candidate identities, one unsupported maximal
clique, unequal distance vectors after reordering an identical pattern and
equal vectors for a reflection.

## Why

A fast filtering strategy must not silently change the accepted scientific
patterns. Candidate count is not distinct-ligand support, and distance agreement
does not establish a proper geometric superposition or a usable consensus model.

## What is measured and what is assumed

The actual legacy helpers and reconstructed graph predicate were executed on
synthetic arrays; no full molecular benchmark, timing claim or repaired legacy
implementation is implied. Source inspection establishes the missing support
gate, correspondence canonicalization, budget and aligned-center construction.
The literature comparison and proposed native contracts are in
`../clique_consensus_review.md`.

## Alternatives and refuted paths

Increasing the arbitrary 10% overlap or switching the generic clique solver
does not address ligand support, identities, proper alignment or shape semantics.
The local hybrid cannot inherit the published RDP completeness guarantee.

## Scope and exclusions

This issue owns correction or replacement of the legacy consensus contract.
The review and audit are delivered locally; the native consensus method is
subsequent product work. Molecular preparation and geometry stay with MolSysMT;
generic graph solvers stay with their graph provider.

## Acceptance criteria

Deliver a native, provider-supported consensus consumer with documented
support, correspondence, geometric verification and completion contracts.
Add independent bounded-oracle controls for boundaries, permutations, repeated
types, duplicate conformers, distinct-ligand support and reflections before
claiming consensus correctness. Retain this audit as defect evidence until the
legacy route is replaced or explicitly retired. Issue remains open for review.

## 2026-10-07 resolution: explicit native transition

The original report above records the retired implementation and is preserved.
The public class now requires `consensus_method='aligned_cliques'` or `'rigid'`
and calls the existing independently tested public native tool. The high-level
dispatcher routes the ligand collection before single-system conversion. No
legacy partitioning, direct molecular preparation or distance-RMSD ranking is
executed. The class/list syntax remains; the selected method's scientific
contract is explicit: `n_points` is a minimum site count, `min_actives` is joint
distinct-ligand support, and ligands arrive prepared.

The full native `result`/`report`, proper-fit placement evidence, source/frame
and unit context, finite search criteria and optional detached bibliography are
retained. Evaluated empty returns `[]`; limits and provider failures raise and
clear stale success evidence. Raw repeated objects and duplicate ligand IDs
are refused. Chemical duplicates across declared IDs remain the caller's
responsibility. Historical generation defaults are inert; nondefault generation
requests are refused rather than silently ignored.

The selected guard asserts explicit retirement and real prepared aligned/rigid
controls, source preservation, reflected-input rejection, support denominators,
no hidden aligned fitting, frame/atom selection, non-default unit persistence,
executed-method bibliography and failed rebuild semantics. Existing independent
native assignment/clique/package/mapping oracles cover boundaries, permutations,
repeated types and distinct support; they certify their declared native families,
not published RDP equivalence or unrestricted consensus completeness.

The old two numerical helpers are frozen in `devtools/legacy_clique_helpers.py`
from the recorded source revision/hash, without a molecular/build API. Their
syntax trees and all original counterexample outcomes are preserved. This
historical fixture is consumed only by the audit, never by product modeling.

Focused Python 3.14 verification: 117 tests passed. Both new cookbook blocks
executed on frozen prepared EST/DES ideal inputs, returning one three-site
hypothesis with two fits under the declared ranked/greedy policy. This is a
workflow control, not biological, energy or affinity validation. The receipt is
`devguide/evidence/ligand_based_facade_review_py314.json`; the maintained contract
and recipe document migration and remaining scope. Existing original evidence
archives are unchanged. Legacy screening/LOO qualification, broader conformer
discovery and ERα environmental-H refinement (MolSysMT #323/local #22) remain
separate; no MolSysMT code is modified.
