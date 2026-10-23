---
summary: Frozen ligand-reference ERα assay pilot with held-out experimental outcomes.
issue: uibcdf/pharmacophoremt#62
status: active
opened: 2026-10-23
closed:
verification: inspected
area: [validation, mvp]
guard: devtools/tests/test_esr1_activity_pilot.py::TestEsr1ActivityPilot::test_frozen_split_excludes_ambiguous_compounds_and_reference_leakage
normative: devguide/validation_collection.md
blocked_by: []
supersedes: []
---

# Frozen ligand-reference ERα activity pilot

## What and why

Resume the MVP after public 0.4.0 and documentation foundations. Existing
geometry/prepared controls do not measure discrimination of assay activity.
This bounded retrospective case uses prepared published 3D inputs and existing
native PharmacophoreMT tools. It does not wait for receptor H refinement.

## Declared experiment

The acquisition/split manifest is
`tests/data/esr1_activity_pilot/manifest.json`; the opt-in driver is
`phmt_test_support/esr1_activity_pilot.py`. Bath's CC BY-SA 4.0 ESR1ago table
supplies selected IDs and labels, independently checked against PubChem assay
743075. No docking score or imputed potency enters the experiment. The Bath
archive is not interchangeable with the original full LIT-PCBA population.

Before any scores, exclude every CID with contradictory substance outcomes:
2662, 5361202, 6128 and 17113. Preserve the eight original conflicting rows.
Order remaining unique CIDs by SHA-256 of `phmt-esr1ago-pilot-v1:<CID>`.
The first active, CID 9821849, is the sole reference; seven other actives and
24 inactives are held out. No replacement after acquisition/preparation/search
failure. CID disjointness does not establish chemical-series independence.

Each source is a single computed PubChem 3D conformer, with supplied chemical
state and explicit hydrogens; it is not an experimental bound conformation.
Public MolSysMT reads SDF and performs the sanitizing RDKit conversion roundtrip;
the consumer observes counts, declared state and coordinate/identity preservation.
No local molecular parser, conformer generation, protonation or scaffold routine
is added. Raw SDF/archive bytes remain outside the repository; URLs, hashes,
attributed labels and the acquisition recipe are retained.

The single-reference native model requests donor, acceptor and aromatic families;
all emitted sites are essential, with radius 0.15 nm. Native `RigidPoseSearch`
uses 10000 trials, point tolerance 0.10 nm, direction tolerance 30 degrees and
minimum fit 0. Native `RetrospectiveValidator` records failures, evaluated-subset
ROC AUC, BEDROC(alpha=20) and tie-aware EF at 10%. This small selected cohort
does not support full-benchmark early enrichment, affinity or prospective claims.

## Execution and acceptance

Use an owned isolated public-provider environment with PharmacophoreMT 0.4.0
and MolSysMT 0.23.0. Execute the driver by file path so the installed runtime,
not the checkout package, supplies the API. Retain actual runtime origins,
versions, driver/manifest/query hashes and producer identity. Molecular work
stays upstream; newer-provider qualification remains a separate #41 task.

Completion requires original full outputs, saved query, per-input preparation
and evaluation outcomes, clear denominators, independent accounting/metric
checks, a maintained validation case and an updated checkpoint. An uninformative
or negative scientific result is retained without tuning held-out parameters.
Any later consensus or conformer continuation has a distinct declared run.

## Current evidence

Acquisition and pre-score data qualification are implemented: 32 inputs are
frozen; 27 have a PubChem 3D record and five return HTTP 404 (one held-out active,
four inactives). Those inputs remain in the experiment without replacement.
The offline split/ambiguity guard passes. Scientific execution and acceptance
are pending; this report does not claim discrimination.
Addon, release infrastructure and deeper documentation remain deferred.
