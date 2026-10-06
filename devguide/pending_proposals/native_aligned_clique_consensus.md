---
summary: Discover aligned clique consensus with alternative jointly supported hypotheses.
issue: uibcdf/pharmacophoremt#24
status: active
opened: 2026-10-03
closed:
verification: measured
area: [modeling, consensus, attribution]
guard: tests/test_aligned_cliques.py
normative: devguide/aligned_clique_consensus_workflow.md
blocked_by: []
supersedes: []
---

# Aligned clique discovery and alternative consensus hypotheses

## What

Discover maximal site correspondences across prepared aligned ligands without a
reference anchor, and construct alternative Feature + Shape hypotheses with
disjoint occurrences and explicit shared ligand support.

## How

Three reusable native tools separate feature compatibility/clique enumeration,
aggregation/package discovery, and molecular workflow/model construction.
NetworkX supplies maximal-clique enumeration; MolSysMT supplies all molecular
operations. Existing `get_consensus_sites()` supplies independent clique aggregation.
Optional Ackredit records the executed NetworkX algorithm references, software
description and original versions at the reached boundary. The maintained contract
is [aligned_clique_consensus_workflow.md](../aligned_clique_consensus_workflow.md).

## Why

The delivered reference-anchored method (#21) cannot discover a site absent from
its reference. The audited legacy route (#18) has inconsistent distance filters,
duplicated occurrences, inadequate support and incomplete geometry evidence.
A small exact aligned method advances traditional modeling without duplicating
provider preparation while uibcdf/molsysmt#298/#300 remain pending.

## What is measured and what is assumed

**Measured, 2026-10-03:** The corrected full suite passes **177 tests**, including
25 clique controls and the literal-ID serialization regression (#25). All three
new cookbook code blocks execute successfully; the strict isolated cookbook
Sphinx build passes. The three offline reporting tests, generated indexes, Ruff
and whitespace checks also pass. Detailed dated scope is retained in the checkpoint.
Prepared aligned inputs and unique dataset ligand identities remain caller
declarations. No biological or performance result, published installation,
unaligned discovery or total pharmacophore search completeness is assumed.

Reproduce in the source checkout with the controlled provider revisions below
on `PYTHONPATH` and the existing scientific environment:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest --receptor=llm -p no:cacheprovider -p no:rerunfailures tests/test_aligned_cliques.py
```

Provenance: Linux, Python 3.13.14; NumPy 2.4.6, SciPy 1.18.0, NetworkX 3.6.1.
Controlled source providers: MolSysMT `4d490427e38c5836be82472348fdf61934442bda`,
PyUnitWizard `2ffe1885675f47c76af03c08e51bc889a5e99a05`, Ackredit
`584328de6efc07cee3a5ddf3ecda2d2e08cc72b4`. Runtime-reported producer versions
remain the versions captured in each result, independently of these source pins.
This does not qualify published dependencies or a hosted compatibility matrix.

## Alternatives and refuted paths

Reference-only discovery cannot recover absent-reference patterns. A largest-clique
choice drops valid smaller maximal groups. Merging overlapping site alternatives
reuses occurrences; pairwise ligand support does not establish whole-hypothesis
support. Generic graph enumeration is delegated rather than reimplemented.
This first method declares maximal site cliques as its candidate family; it does
not silently claim exhaustive subclique or RDP/DISCO pattern discovery.

## Scope and exclusions

Aligned typed geometry, local maximal cliques, maximal disjoint packages with
shared supporters, bounds, native models/evidence, Ackredit and cookbook. No
preparation, alignment, subclique family expansion, recursive distance partitioning,
angular means, receptor preparation, Rust/GPU backend or biological pilot closure.
Legacy correction/retirement remains #18; reference-based acceptance remains #21.

## Acceptance criteria

Independent bounded oracles protect clique and package correctness, including
repeated types, unequal maximal sizes, support intersections, reordering and
empty/failure separation. Limits fail without returning truncated models.
Real MolSysMT inputs preserve coordinate/frame/state evidence and produce usable
screening models with native persistence. Real Ackredit controls preserve reached
references, enclosing sessions, repeated records, detached models and saved readers;
absence/failure cannot invalidate completed science. Execute a cookbook recipe and
review the public contracts before broader scientific/distribution acceptance.

Local implementation and analytical/source-integration guards are delivered;
scientific/API review and broader acceptance remain pending. This report remains
active rather than claiming published or biological closure.
