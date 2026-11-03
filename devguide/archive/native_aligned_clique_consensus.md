---
summary: Discover aligned clique consensus with alternative jointly supported hypotheses.
issue: uibcdf/pharmacophoremt#24
status: resolved
opened: 2026-10-03
closed: 2026-11-03
verification: measured
area: [modeling, consensus, attribution]
guard: tests/test_aligned_cliques.py
normative: devguide/aligned_clique_consensus_workflow.md
blocked_by: []
supersedes: []
---

# Aligned clique discovery and alternative consensus hypotheses

## Resolution — 2026-11-03

Reviewed and incorporated as the bounded aligned-clique source/API method.
The [new receipt](../evidence/aligned_clique_acceptance_20261103_summary.json)
records clean receiving head **17fb209ed38924af1ea9dc5b5ceb359bfb4b51bc**.
All **60 freshly executed controls** pass in 16.54 s, without failures/errors/
skips: 25 aligned-clique, 17 aligned-consensus and 18 contracts/serialization.
Independent bounded subset oracles protect maximal cliques/packages, unequal
maximal sizes, repeated types, whole-package support, occurrence conflicts and
reordering. Other guards protect typed orientation, declared source frames/units,
pre-solver graph bounds, unsupported-clique counts, completion versus failure,
real optional attribution, fresh absent-provider/readers and detached bibliographies.
This is a new focused run; no new full-suite execution is claimed.

Fresh analytical capsules with host tracking off/on independently verify discovery
when the first ligand has no requested feature, center .17 nm, RMSD .02 nm and
support 2/3 including that empty inventory. Two overlapping acceptor alternatives
remain two one-site models. A separate synthetic supporter-set oracle gives
exactly three two-site packages (AC, BC, CD), never a triple with insufficient
whole-package support. Both min_sites filtering and unsupported molecular
construction return complete empty hypotheses; no usable empty model is created.
All three budgets fail PHMT-E107/complete=False without returning a partial query.

The three models retain six total JSON/YAML round trips across changed unit
policies. Each tracking profile passes 29 pose evaluations (18 matched, 11 valid
negatives), including the separately narrowed radius that rejects both contributors
without reducing support. Source atom identity, chemical state and coordinate
fingerprints remain unchanged within each of the pm and default unit policies.
Off/on scientific projections agree; actual prepared-input capture retains
3 items/6 uses off and 15/37 on, including reached clique references and no
borrowed DISCO/RDP credit. All three unchanged cookbook blocks execute with
application-owned capture (12 items/30 uses). Strict isolated Sphinx rendering
passes with one attribution link-target stub, not a full-site claim. Actual
loaded source/native/helper/test/input and metadata identities remain stable
in focused, capsule and cookbook phases.

The initial capsule and its diagnostic repeat fail a script-only cross-policy
coordinate byte comparison. A no-model diagnostic reproduces unit-conversion
rounding up to 5.551115123125783e-17 nm. The final runner compares fingerprints
within identical policies and additionally verifies the default policy exactly
before/after the entire workflow. Original scripts/logs/diagnostics are preserved;
failed attempts are not qualified. No library/test/fixture/tolerance/scientific-
definition/provider/prefix/sibling change is needed.

Ownership review: MolSysMT supplies every molecular preparation, conversion,
translation, selection, inspection, recognition and state/geometry operation.
PHMT discovers, aggregates and packages cached pharmacophoric occurrences;
NetworkX owns generic clique enumeration. No molecular preparation/alignment or
generic molecular kernel is introduced. IDs and prepared common frames remain
caller declarations. Completeness covers maximal feasible packages within the
maximal-site-clique family, not all subcliques, chemical patterns or continuous
alignment; support does not establish affinity or chemical uniqueness.

This resolves #24 source/API acceptance. Clean installed/public/platform/hosted
qualification stays #23/#10/#9; inherited workspace conflicts remain #82. No
biological/performance qualification follows. #41 remains partial for public/
floor/installed receiving and final historical fallback retirement, review
2026-11-11. Next #26 prepared rigid unaligned consensus requires its own provider-
owned fitting/transformation and correspondence/support/budget acceptance.
#66 still awaits four original binding methods; addon/new release remain deferred.
Owned root /tmp/phmt24-acceptance-20261103-vw26hupl/, LMMV/dprada, review
2026-11-17. No local process remains after closeout. Original October text below
is preserved; its pending review/provider statements are historical.

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
