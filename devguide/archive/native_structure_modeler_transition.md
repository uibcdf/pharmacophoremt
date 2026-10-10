---
summary: Replace the structure modeler's molecular heuristics with explicit cached receptor projections.
issue: uibcdf/pharmacophoremt#44
status: resolved
opened: 2026-10-10
closed: 2026-10-10
verification: measured
area: [architecture, structure-modeling, integration]
guard: tests/test_receptor_projections.py
normative: devguide/structure_based_workflow.md
blocked_by: []
supersedes: []
---

# Native structure modeler transition

## What

Retire local molecular selection, RDKit SMARTS/centroid/plane recognition and
first-neighbor or arbitrary +z direction inference behind `StructureBasedModeler`
and `model(method='structure-based')`. Consume cached native receptor features
and explicit pharmacophoric hypothesis projections instead. This is a bounded
consumer migration under #41, not delivery of an automatic pocket modeler.

## How

Expose `from_receptor_projections()` as a reusable cached query constructor.
Require feature index, declared query projection direction, physical distance
and label. Donor targets and aromatic targets also require independently declared
target direction/normal. Complement donor/acceptor and charge types; preserve
hydrophobic/aromatic types. Acceptor targets are spherical, matching the native
undirected acceptor inventory. Separate hypotheses represent alternative
directions; no first-neighbor, face-sign or fixed-distance fallback is retained.

Keep the historical class/dispatcher as thin composition facades; require cached
inventories and projections. Optional exclusions delegate to the already public
`get_excluded_volume_sites()` with a separate heavy-atom inventory and explicit
radius. Validate declared selection/frame/state compatibility and reject retired
pocket arguments. Do not claim that cached declarations authenticate source
identity or physical projection quality against the retained molecular reference.

## Why

The #41 audit and source `3ed12cd9405c8bbb577afefca58c372b5e0785f1` identify
reachable molecular operations in the old structure route. The old first-neighbor
heuristic is not the documented donor-H/lone-pair method. Cached native chemistry
and explicit hypotheses make molecular ownership and scientific assumptions
reviewable without implementing another provider geometry engine.

## What is measured and what is assumed

Source inspection identified the old callers and the absence of public pair
vectors in inspected local MolSysMT `8ae160fc9` and the remote structure-module
inventory (default head then `9ea9be32a`). Independent analytical controls and
real public-provider inventories are being qualified in the owning test module.
Source identity/common coordinates, projection labels/evidence and physical
justification remain caller declarations. There is no biological validation,
legacy/native equivalence, remote-provider qualification or performance claim.

## Alternatives and refuted paths

- Native observed-interaction construction is not receptor-only projection.
- Copying donor/acceptor local geometry into PHMT violates provider ownership.
- Retaining fixed distances or arbitrary axes silently changes user assumptions.
- A directional acceptor target cannot claim native lone-pair matching when
  the existing acceptor inventory supplies no such orientation.

## Scope and exclusions

Close this consumer migration after qualified cached construction, facade
retirement and executable guidance. MolSysMT #375 owns donor/local acceptor
geometry; existing donor-vector arithmetic in `get_features` remains a bounded
#41 debt, without a new implementation here. #323 owns environmental H refinement
and #350 owns rejected aromatic-candidate diagnostics. Actual pocket detection
belongs to TopoMT; no TopoMT API is invented in this transition. Remaining legacy
screening, molecular I/O and unused preparation utilities keep #41 open.

## Acceptance criteria

- Reusable query construction and both facade entry points use cached evidence
  and explicit hypothesis decisions, with no molecular calls.
- Independent controls cover complementary types, units, orientation, omitted
  features, alternative/empty hypotheses, malformed inputs and source custody.
- Optional exclusions preserve source correspondence, common declared selection,
  frame/state and explicit-radius semantics; failures publish no partial result.
- Public-provider analytical inventory/plane controls, placed positive/negative
  evaluation, saved JSON and actual optional-attribution limits pass.
- Migration guidance, recipe and reporting/index gates match the delivered API.

## Resolution — 2026-10-10

The public cached query constructor and both structure-based facades now use
explicit projections and optional cached exclusions. The local molecular engine
is removed. **66 new controls** are included in **247 passing focused regression
tests** on normal editable Python 3.14.7 (113.26 s). These selected modules cover
the new method, shared contracts/shapes, reference and placed-pose construction,
exclusions, complex/ligand facades, composition, attribution, persistence and
viewer consumer boundaries; this is not a new full-suite result. Two existing
warnings remain: a deliberately failed optional-attribution provider and the
legacy screening unit strip tracked under #41. No new projection warning occurs.

Three executed cookbook blocks produce 1/4/1/0 sites for the direct query,
facade with exclusions, dispatcher and empty hypothesis. Strict isolated recipe
and original-navigation rendering passes with explicit stubs for other linked
pages/notebooks, without warning suppression; it is not full-site qualification.
Ruff, report/index checks and the nine archive-integrity tests pass. Original
scientific producer sources and recorded inputs are unchanged across the accepted
run; the documentation follow-up verifies the same producers, native binaries
and 75 recorded test/input/recipe files. Native-binary inventory describes the
parent process, not subprocess import tracing. Local MolSysMT checkout remained
clean at inspected `8ae160fc9`; no sibling implementation was changed or pulled.

The [accepted scientific summary](../evidence/structure_based_facade_review_py314_summary.json)
links original output/JUnit, source overlay/additional source, driver, producer
identities, input hashes and detached analytical metadata. Its original strict
documentation failure is retained; the separately checksum-qualified
[successful documentation follow-up](../evidence/structure_based_facade_docs_py314.json)
corrects only review-harness navigation/notebook stubs and verifies source identity.
The [initial review](../evidence/structure_based_facade_initial_review_py314_summary.json)
is retained outside final acceptance. All 21 previously committed gzip JSON
archives remain byte-identical. Task-created temporary contexts were cleaned
after outputs were retained; unrelated caller resources were not removed.

Close #44 for the explicit cached consumer transition only. #41 stays partial
for MolSysMT #375's geometry contract and native donor-vector migration, and
legacy screening/preparation/I/O. Automatic provider-informed pocket modeling
and biological qualification remain future work. Hosted exact-head matrix
qualification is tracked separately; local tests do not qualify every supported
interpreter/platform or the published provider artifact.

## Distribution follow-up — 2026-10-10

The first published head `dbc82e4` failed the hosted `Reporting governance` job
in run **38035866985**, job **114166037234**: the existing complete-tree
distribution guard found that the new `modeler/receptor_projections.py` was
missing from `devtools/conda-build/resources.toml`. Report/index and archive
steps passed. The issue was reopened while this omission was corrected; the
original scientific results and archived claims above are preserved.

The required path is now registered. A clean isolated checkout of accepted SDK
`8f00e6d9de943b6e4710ea62936e2ebea00fad24` passes all **23 administrative
distribution/dependency/environment tests**, declared dependency-route preflight,
ordinary-environment check (no drift), and **7 CI/contributor-route controls**.
The distribution README now states the actual 178 committed package files plus
generated version module and distinguishes the existing publication SDK pin
from the dependency/environment SDK pin. No package scientific source or test
changed, no sibling checkout changed, and no release/build/installed artifact
qualification is claimed by these synthetic administrative controls.

The [follow-up record](../evidence/structure_based_distribution_followup_py314.json)
retains the original bounded hosted failure, local commands/output, exact SDK
identity and temporary-resource cleanup. The existing complete-tree distribution
test guards registration; the original 247 scientific controls still describe
the unchanged package code. Hosted qualification of the follow-up head is
reported separately on #44.
