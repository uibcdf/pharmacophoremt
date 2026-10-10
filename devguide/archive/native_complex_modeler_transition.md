---
summary: Transition the complex modeler and default dispatcher to prepared native observations.
issue: uibcdf/pharmacophoremt#42
status: resolved
opened: 2026-10-10
closed: 2026-10-10
verification: measured
area: [architecture, complex-modeling, integration]
guard: tests/test_complex_based_facade.py
normative: devguide/complex_based_workflow.md
blocked_by: []
supersedes: []
---

# Native complex modeler transition

## What

Retire the general molecular preparation, inference, recognition and detection
behind exported `ComplexBasedModeler` and the default `phmt.model()` route.
Require an explicit ligand selection and a nonempty named collection of native
MolSysMT observations computed on the same unchanged prepared source. Preserve
the class, method name and one-model versus multiple-model return shape.

## How

Use the existing public `from_interaction_collection()` as the frame-level
consumer. Keep original native state/maps/profile/coverage/evidence and optional
attribution. Reject implicit ligand/receptor preparation and retired detector
thresholds. Remove the old engine rather than moving molecular operations into
a local helper or runnable fallback. This is a breaking scientific transition;
the old heuristic definitions are not asserted equivalent to native profiles.

## Why

The [#41 ownership audit](../pending_proposals/retire_legacy_molecular_operations.md)
found the complex modeler reachable through the default dispatcher despite the
prepared-input native tools. The old engine called local feature SMARTS, RDKit
bond-order inference, hydrogen addition and geometry helpers. Native provider
operations are reusable and have explicit preparation and detection contracts.

## What is measured and what is assumed

The audit records the reachable old caller at commit `1198af1`. Historical #5
source/test assertions remain readable in that immutable revision; original
archived claims and measured evidence are retained. Current scientific tests
will check actual native observations on analytical controls and the separately
declared ERα fragment, including evaluated-empty families. Caller responsibility
for unchanged source identity remains explicit; biological equivalence and full
receptor acceptance are not inferred from model counts.

## Alternatives and refuted paths

Do not retain silent RDKit recovery or silently map old thresholds to different
native methods. Do not manufacture H-bonds/aromatic constraints from an empty
observed family. Do not implement missing MolSysMT preparation or fit routines
locally. Missing provider capabilities retain their owning issues.

## Scope and exclusions

This issue closes only the complex modeler/default dispatch transition. Broader
#41 remains partial: structure-based, legacy screening and molecular utilities
have separate callers. MolSysMT #323/#350/#367 and all original evidence archives
remain unchanged. No provider or DockingMT implementation is part of this change.

## Acceptance criteria

- Class, explicit method and default dispatcher consume prepared observations.
- Missing/obsolete configuration fails before molecular operations; no local
  inference, preparation or detector engine remains in the complex route.
- Single/multiple-frame return shape, evaluated-empty evidence, native failures,
  source preservation, saved evidence and actual optional attribution are guarded.
- The prepared ERα fragment continuation preserves six hydrophobic sites and
  evaluated-empty H-bond/pi-pi evidence without claims of affinity validation.
- Historical #5 claims are preserved with a dated retirement correction; the
  recipe/maintained migration contract/report indexes are executable and valid.
- Relevant scientific, reporting and documentation checks pass on the change.

## Resolution — 2026-10-10

The class and both complex dispatcher entry points now require explicit prepared
native observations and delegate to `from_interaction_collection()`. The old
general molecular engine is removed rather than moved to another local helper.
The 31 new facade controls and prepared-fragment continuation are included in
the **712 passing full local tests** on normal editable Python 3.14.7
(1336.82 s, 12 warnings). The warnings are ten declared structural B-factor
drops, one deliberate optional-attribution failure, and one remaining legacy
virtual-screening unit strip; they are not new facade warnings. Three cookbook
blocks produce 9/9/9/0 sites through class/named/default/empty routes. Ruff,
strict isolated new-recipe/navigation rendering, archive integrity and reporting
checks pass. This is local qualification; published matrix state is recorded
separately on the owning issue.

The original measured output, JUnit, exact source overlay/new test source,
Python/provider/native-binary identities, declared-input hashes and saved
analytical models are retained in
[the final archive summary](../evidence/complex_based_facade_review_py314_summary.json).
All scientific source/binary identities and recorded input hashes are unchanged.
The raw driver's conservative combined flag is false solely because repository
dirty-overlay metadata gained the separately retained initial failed evidence
files during the corrected run; the summary preserves and explains that fact,
and independently verifies every scientific source/binary and input hash.

The [initial failed execution](../evidence/complex_based_facade_initial_full_py314_summary.json)
is retained, excluded from acceptance and qualified for its capture/source-change
limitations. Its new ERα test supplied the deposited original source rather than
the prepared source used for the native analyses; native validation correctly
rejected differing source axes. The fixture reference was corrected without
weakening provider or adapter checks. The corrected continuation yields six
hydrophobic sites, retains empty H-bond/pi-pi families and preserves prepared
coordinates, histories, maps and cached observations. No scientific equivalence
with legacy heuristic output or full biological acceptance is asserted.

All twenty pre-existing gzip evidence files and the original #5 archive body
are preserved. #5 gains only new guard/normative frontmatter and a dated
retirement qualification. #41 remains partial/open for other reachable legacy
routes, with structure-based provider consumption next. No sibling source was
modified and MolSysMT #323/#350/#367 remain independent limitations.
