---
summary: Qualify saved prepared queries through rigid recovery, selected negatives and frame-budget accounting.
issue: uibcdf/pharmacophoremt#50
status: resolved
opened: 2026-10-10
closed: 2026-10-10
verification: measured
area: [screening, validation, io]
guard: tests/test_prepared_search_workflow.py
normative: devguide/prepared_search_workflow.md
blocked_by: []
supersedes: []
---

# Prepared rigid-search continuation

## What

Continue #49's public prepared EST chain with explicit rigid-method anchors,
saved query recovery and prepared-frame failure/score accounting.

## How

Reuse the public CCD fixture, existing cached curation, codecs and workflow
evidence driver. Declare three essential sites: the aromatic center and source
atoms zero/eight. Public MolSysMT tools produce two placements of the same
conformation and fit proposed pharmacophoric correspondences. Run native
`RigidPoseSearch`, `ConformerScreening`, `VirtualScreening` and alignment replay.
Do not add a local molecular operation or another provenance recorder.

## Why

The prior single-essential-site hypothesis is valid for placed evaluation but
cannot seed this rigid method. A displaced pose is also not a valid negative
for a method allowed to align it. Independent cases must distinguish a complete
selected-participant negative, failed limited search, maximum-fit termination
with incomplete enumeration, source frame identity and incomplete ensembles.

## What is measured and what is assumed

The frozen selected atom set contains only the original aromatic ring. Its
maximum pair distance is less than the ring-to-required-atom-eight distance
minus the declared summed matching tolerance; it cannot satisfy that anchor
triplet. A one-product budget visits a reused candidate first and produces no
fit proposal. The moved frame therefore fails unscored; the original frame
still proves valid coverage one by identity placement. Two prepared placements
are not independent conformers or distinct chemical supporters.

## Alternatives and refuted paths

No displaced-pose label is reused as a rigid-search inactive. No molecule is
distorted or prepared with a consumer molecular kernel. Frozen source geometry
and source-index selection provide independent controls; repeated input/frame
orders test ties rather than biological discrimination.

## Scope and exclusions

Analytical ideal-coordinate controls, not activity validation, docking, generated
conformers, environmental H refinement or a performance benchmark. MolSysMT
#375/#219/#323 remain their independent scopes. Arbitrary degenerate explicit
fits remain provider #367; replay here uses already qualified automatic anchors.
Hosted/installed/public delivery remains #23. Maintainers LMMV/dprada own review.

## Acceptance criteria

Execute the public-step recipe and focused numerical/source-mapping/failure
guards; retain full dated output, executed source overlay, actual attribution
and fresh-reader evidence. Verify provider/input stability and original archive
immutability. Publish a new evidence identity without replacing #49 outputs.

## Measured completion — 2026-10-10

The combined focused selection passes 28 controls (15 search/frame, 13 prior
placed-chain) on normal editable Python 3.14.7 in 66.55 s. The opt-in driver passes
all three saved-codec control groups with stable scientific fields across host
tracking settings and unchanged provider Python/input hashes. The independent
triangle/range bounds, source preservation and full-atom provider fit replay pass.
Both recipe blocks execute; strict isolated rendering passes.

The [new original summary](../evidence/prepared_search_workflow_py314_summary.json)
retains the full original result, executed developer-source overlay, producer/
extension/input identities, exploratory observations, full guard output, actual
attribution and fresh readers. All 29 previous gzip archives remain unchanged.
Host-on captures 15 items/36 uses with actual EST input; host-off retains independent
provider attribution (four items/six uses). Readers register zero new uses.
Later final governance/rendering checks are in the completion receipt.

This closes the bounded prepared rigid/frame continuation. Runtime scientific
source and sibling repositories are unchanged. Biological/continuous-search,
arbitrary explicit provider fit, generated conformer and hosted/public delivery
qualification remain separate and are not inferred from these controls.
