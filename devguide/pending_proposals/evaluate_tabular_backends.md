---
summary: Evaluate tabular alternatives to Pandas against actual screening-analysis workloads.
issue: uibcdf/pharmacophoremt#210
status: open
opened: 2026-11-13
closed:
verification: inspected
area: [screening, results, dependencies]
guard:
normative:
blocked_by: []
supersedes: []
---

# Future tabular-engine evaluation

## What and why

At the maintainer's request, retain a deferred investigation into alternatives
or complements to Pandas. This is independent of current direct-dependency
ownership [#206](../pending_bugs/pandas_dependency_ownership.md), and does not
block the 0.6.0 candidate. No migration, engine or new dependency is selected.

Read-only inspection at PHMT source
`54ffaa78ec2b1361fbae276e71603bdbcfc48dcb` finds two direct runtime imports:
`Pharmacophore.to_dataframe()` produces site descriptions with lists and
quantity-bearing centers/radii; `VirtualScreening.to_dataframe()` produces
scalar ranked-hit evidence, also used by `to_csv()`. The saved-results reader
uses native records without importing Pandas. Changing these adapters has no
demonstrated effect on pharmacophore matching or scoring throughput.

## Evaluation outline

Start with representative [#108](qualify_public_library_workflow.md) analysis
tasks: filtering, stable ranking/top-k, grouping, source-metadata joins, batch
export and repeated saved-result queries. Compare the maintained Pandas
baseline with justified candidates: Polars for typed/lazy tabular operations,
Arrow/Parquet for interchange/storage, and DuckDB for saved-table queries.
These have different roles. Retaining Pandas or adding a small optional adapter
are valid outcomes; no generic backend abstraction is required in advance.

Measure equivalent end-to-end work, including conversion, materialization,
startup and I/O, at declared versions and bounded CPU/thread/memory limits.
Start small and serial on shared infrastructure. Record wall time and peak
memory, then expand only when measured use permits it. No comparative benchmark
or alternative-engine installation has run in this increment.

Preserve units and quantity round-trips, columns/dtypes/index semantics,
copy/alias behavior, empty tables, null/NaN/zero distinctions, stable ties and
duplicates, original molecular/state/conformer identities, failures/incomplete
outcomes and provenance/attribution. An object column does not itself establish
vectorized processing; numeric projections need explicit unit/reconstruction
contracts. Existing Pandas returns retain their documented behavior. Assess
Python/platform support, installation cost and maintenance as well as speed.

## Provider relationship and exclusions

[MolSysMT #749](https://github.com/uibcdf/molsysmt/issues/749) owns the related
native molecular-table assessment. Its source
`0dc250bb993aba0f0910c51607afb1224df76dba` has Pandas subclasses in
`native/topology.py` and `native/_chemical_state.py`, a deeper storage/editing
boundary than PHMT output adapters. Its native identity, nullable chemistry,
mutation and persistence contracts need provider-owned evaluation. PHMT does
not implement replacement molecular storage or preparation here. Changing its
own adapters alone would not remove MolSysMT's Pandas dependency.

The two published issues link to each other and carry the related-component
labels. The bounded duplicate searches found no Polars result; this is not an
exhaustive remote-inventory claim. The inspected MolSysMT checkout remains
unchanged and behind its fetched published source.

## Completion conditions

Publish reproducible representative workloads, correctness controls and bounded
measurements, then a justified retain/optional-adapter/migration decision.
Record any implementation, API transition and provider coordination separately.
A migration is not required to close the study. Revisit when #108 exposes an
actual tabular bottleneck or the maintainers schedule this investigation.

Official starting references are linked in #210: Polars lazy/streaming guides,
Arrow's Python data model and DuckDB's Parquet query documentation. They describe
capabilities, not measured performance in PHMT.
