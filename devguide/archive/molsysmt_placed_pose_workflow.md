---
summary: Deliver a bounded MolSysMT-backed interaction-to-pharmacophore and pose-evaluation workflow.
issue: uibcdf/pharmacophoremt#13
status: resolved
opened: 2026-10-02
closed: 2026-11-03
verification: measured
area: [modeling, screening, integration]
guard: tests/test_pose_evaluation.py
normative: devguide/placed_pose_workflow.md
blocked_by: []
supersedes: []
---

# MolSysMT-backed placed-pose workflow

## Resolution — 2026-11-03

Accepted the native observation-to-query and already-placed pose source/API slice.
The [new receipt](../evidence/placed_pose_acceptance_20261103_summary.json) records
clean receiving **1eea04d6f92b2e58d8603aa95e204f3e9fa0caf2**: 99 fresh controls
pass in 16.66 s, zero failures/errors/skips/warnings (14 pose, eight retrospective,
44 metric, 18 contract and 15 observed donor-geometry controls). The guard protects
real native observations, one-to-one/zero-weight essential semantics, exclusions,
direction, indices, units, persistence and failure identity; companion modules
protect accounting, independent RDKit metric oracles and public-vector receiving.
No new full suite is claimed.

Fresh host-off/on capsules calculate actual hydrophobic and SMARTS hydrogen-bond
observations with public MolSysMT. Two contacts involving one ligand atom become
one hydrophobic site with both observations; direct and dispatcher queries agree.
Two donor observations become one directed donor site with both original records,
or two atomic acceptor spheres when the opposite side is selected. The public
donor-vector route retains local pair [1,0], declared source pair [21,20], local
frame 1 and declared structure sources [4,7]. Labels are explicit controlled
native mappings, not authenticated molecular origin. Cached conversion does not
redetect observed chemistry. The same unchanged source/index space remains a
caller obligation; axis/label agreement cannot authenticate it.

Reference/displaced poses give coverage 1/0; public MolSysMT shared rigid motion
and regenerated observations preserve a match. Wrong-frame and reversed donor-H
poses fail; source acceptors match without invented orientations. One feature
cannot satisfy two essential sites, even when one has weight zero: coverage one
still gives not_matched. An essential site wins over an optional weight-100
competitor for the same candidate (coverage 1/101). A missing optional weight-three
site permits coverage .25 with all essential sites fulfilled; an explicit .3
minimum rejects it. Heavy-atom exclusion veto preserves coverage one and the
clash record. Covered-empty native observations produce an empty model; evaluating
that model is refused. Uncovered frames, split donor/H selection, controlled
unsupported kinds/nonzero periodic images and implicit legacy screening fail
visibly. The periodic/unsupported cases are declared native-record perturbations,
not new detector or periodic-image calculations.

Batch indices [0,1,2,3] retain matched/failed/matched/not_matched. The failed source
has fit_value=None, PHMT-E103 and its source-stage/cause evidence. The explicitly
placed VirtualScreening facade retains every native evaluation and returns only
hits [0,2], preserving original repeated inputs. Retrospective generators retain
original classes 3/2, failures [0,4], evaluated indices [1,2,3], scores [1,1,0] and
analytical AUC/BEDROC one. Six JSON/YAML round trips per profile retain hydro/donor/
acceptor metadata, constraints, physical geometry to 1e-12 and matched outcomes
across pm/fs/degrees and angstrom/ps/radians. Original observations and molecular
atom/state/coordinate domains remain unchanged, including exact default-policy
fingerprints. Off/on science agrees, with actual credit 3 items/12 uses host-off
and 12/43 host-on.

The chemical-definition review is accepted explicitly: conversion preserves supplied
observation roles/profile; evaluation independently applies the declared classical
SMARTS definition. A separate real-provider explicit_sites control declares a bonded
C-H donor, converts its geometric observation into one donor site, then obtains a
valid zero-coverage negative under smarts_donor_acceptor. This is a deliberately
declared profile mismatch, not a claim of conventional C-H hydrogen bonding.
No observed role guarantees a candidate match, and no repair/reinterpretation is
performed. Both tracking modes agree (credit 4 items/5 uses off; 12/22 on).

The unchanged normative Python block passes (11 items/23 uses), as does strict
isolated rendering of the original page with six neighbor link-target stubs.
Full loaded-source/native/helper/test/input and metadata identities are stable
in focused/capsule/profile/example phases. The main capsule, tests, example and
render need no correction. The supplementary profile script initially looked up
recognition.hbond instead of recognition.hydrogen_bond; its failed original/log
are retained and only that one-off key is corrected. No library/test/fixture/
scientific-definition/provider/prefix/sibling change is needed.

Public MolSysMT owns all molecular construction, inspection, recognition,
observations, source mapping, donor vectors and rigid motion. PHMT owns cached
pharmacophoric interpretation, constraints, matching, persistence and result/metric
accounting. The historical molecular modelers/utilities have since transitioned
under #18/#42/#44/#45/#46; the screening facade requires an explicit native method,
and retrospective evaluation has no implicit legacy fallback. No preparation,
conformer generation, implicit search, ideal acceptor geometry, affinity, biology
or performance is established here. #41 remains partial for public/floor/installed
receiving and final historical donor-absence retirement, review 2026-11-11.

This resolves #13 scientific/API review. Installed/public/platform/hosted #23/#10/#9
and inherited workspace #82 remain separate. Next review #19 activation/payload/
saved-report/reached-credit contracts, keeping its delivered-package/all-minor
public receiving explicitly pending unless independently qualified. #60/#66 retain
their gates; addon/new release defer. Owned /tmp/phmt13-acceptance-20261103-k2desp6c/,
LMMV/dprada, review 2026-11-17; borrowed #69 venv remains normal editable PHMT
0.4.0+62.g6a7537b with unchanged providers/native. No local process remains after
closeout. Original October/local-implementation/future-work statements below keep
their historical scope and are superseded where noted.

## What

Provide independently usable interaction extraction and evaluation of existing
poses while keeping all molecular-system operations in MolSysMT. The first
slice supports hydrophobic contacts and hydrogen bonds, explicit frame/state
selection, source-index provenance and inspectable matching results.

## How and evidence

`modeler.from_interactions()` and `model(method='interaction-based')` consume
native observations. `screening.PoseEvaluator` obtains chemical features through
public MolSysMT tools and assigns each candidate to at most one site. Essential
sites, directed donor-H geometry, heavy-atom exclusions and weighted coverage
have explicit semantics. Native metadata and detached provider bibliography
survive round trips; physical result fields use QuantityRecords.

`tests/test_pose_evaluation.py` exercises real MolSysMT interaction calculations
and independent analytical geometry controls. `tests/test_contracts.py` protects
invalid quantities/vectors, non-default unit policy and optional-viewer absence.
No biological pilot success or private evidence is claimed.

## Scope and exclusions

Unsupported kinds and periodic image reconstruction raise. No alignment,
hydrogen addition, protonation repair or conformer generation is performed.
The legacy modelers/screener are not fully migrated. The controlled dependency
route uses a published review snapshot, not a verified stable release closure.

## Acceptance and next review

The guard and `../placed_pose_workflow.md` define the delivered local slice.
Keep this proposal active during review and discussion of the scientific/API
contracts. Further families and adapters require their own controls. No commit
or hosted CI pass is claimed for this local implementation.
