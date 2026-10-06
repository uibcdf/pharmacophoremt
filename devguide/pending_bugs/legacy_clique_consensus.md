---
summary: Legacy distance partitioning and clique support disagree with the matching criterion.
issue: uibcdf/pharmacophoremt#18
status: active
opened: 2026-10-02
closed:
severity: high
verification: measured
area: [modeling, consensus]
guard:
normative: devguide/clique_consensus_review.md
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
