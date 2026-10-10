---
summary: Qualify distinct prepared EST/DES consensus support, empty outcomes and persisted source maps.
issue: uibcdf/pharmacophoremt#51
status: resolved
opened: 2026-10-10
closed: 2026-10-10
verification: measured
area: [modeling, validation, io]
guard: tests/test_prepared_consensus_workflow.py
normative: devguide/prepared_consensus_workflow.md
blocked_by: []
supersedes: []
---

# Prepared distinct-ligand consensus

## What

Continue #49/#50 using existing rigid consensus and the explicit native facade
on two chemically distinct public CCD prepared inputs, EST and DES.

## How

Request acceptor spheres and aromatic axes only. Reuse public MolSysMT
preparation and frame transforms, native PHMT consensus, saved model codecs and
the existing workflow recorder. Check original occurrence/atom maps and joint
support independently of returned model counts.

## Why

Multiple proposals, layouts or frames cannot substitute for distinct ligand
support. Empty hypotheses are valid completed outcomes; resource exhaustion
must remain failure, with no stale successful facade result.

## What is measured and what is assumed

The normal editable Python 3.14.7 selection passes 36 controls, including eight
new independent consensus guards. Native/facade retain one three-site model, two
fits and one layout. The impossible four-site minimum is completed empty; one-fit
budget failure clears facade state. Original source geometry/chemistry and maps
survive three codecs, alternate units and fresh readers. Frozen CCD ideal geometry and provider CTAB interpretation
remain preparation controls rather than binding poses, activity or independently
qualified chemical-state inference.

## Alternatives and refuted paths

No duplicate EST frames are declared independent ligands. No molecular solver,
hydrogen preparation or donor/acceptor direction engine is added here.

## Scope and exclusions

Only native finite-family prepared workflow controls. Provider #375/#323/#219,
biological validation, timing comparisons and required hosted/public delivery
(#23) remain separate. LMMV/dprada own review and publication.

## Acceptance criteria

Independent support/injectivity/maps, impossible-site-count empty control,
fit-budget failure, immutable sources, codec/unit/fresh-reader retention,
actual attribution and a new full immutable run identity. Preserve all previous
archives, execute focused guards and report the exact scope of qualification.

## Measured completion — 2026-10-10

The [new original summary](../evidence/prepared_consensus_workflow_py314_summary.json)
links full native reports, failure/empty outcomes, original source/extension/input
identities, executed uncommitted developer-tool/test overlay, actual attribution
and complete focused guard output. All 30 prior gzip archives are byte-identical.
Both public recipe blocks and reviewed installed-development preflight pass;
strict isolated rendering covers the two new pages. Host-off/on science is stable,
host-on captures both datasets (21 items/81 uses), provider-only host-off capture
retains four items/six uses, and fresh reading registers no new uses.

This closes only the bounded prepared distinct-ligand acceptance case. Scientific
runtime and sibling repositories are unchanged; hosted/public gates and provider
geometry/preparation/biological requirements remain independent. Later governance
and source rechecks are retained in the completion receipt.
