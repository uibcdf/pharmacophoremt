---
summary: Build reusable exclusion spheres from native heavy-atom inventories without molecular inference.
issue: uibcdf/pharmacophoremt#32
status: active
opened: 2026-10-03
closed:
verification: measured
area: [modeling, geometry]
guard: tests/test_excluded_volume_sites.py
normative: devguide/excluded_volume_workflow.md
blocked_by: []
supersedes: []
---

# Public heavy-atom exclusion sites

## What

Expose a cached-inventory exclusion-sphere builder that can be composed with
different pharmacophoric hypotheses independently of molecular preparation.

## How

`get_features(..., features=['included volume'])` obtains source-indexed heavy
geometry through MolSysMT. `get_excluded_volume_sites(feature_inventory, radius=...)`
constructs independently owned spheres and a detached report without molecular
access. Consumers compose the sites with existing public Pharmacophore methods.

## Why

Exclusions belong to pharmacophoric Feature + Shape modeling. The observed #22
receptor lacks interaction-ready chemistry but has explicit heavy-atom geometry.
A reusable builder supports this bounded step without reconstructing chemistry
or hiding selection/radius decisions inside a monolithic complex modeler.

## What is measured and what is assumed

Selection, physical interpretation, source identity and common coordinate frame
remain caller declarations. Uniform positive scalar radii are chosen explicitly.
Existing PoseEvaluator exclusion semantics are the compatibility boundary.
Executed controls and observed-case outcomes are recorded below. These are
geometric controls, not receptor chemical or biological validation.

## Executed constructor and observed controls — 2026-10-03

Twenty-two public constructor controls pass, including cached no-molecular-
access, independent ownership, malformed radii/inventories, empty construction,
inside/equality/outside veto, native query persistence, units, actual repeated/
empty attribution, genuine fresh-process absence and detached fresh readers.
The report retains actual construction software versions even when attribution
is disabled. Controlled optional-provider failure preserves the scientific data.

Four observed controls compose the H-prepared EST and raw 19-residue receptor
shell, producing 153 exclusion sites. At 0.1 nm the reference passes. A controlled
translation superposes candidate O3 (index 3) on receptor GLU353 OE2 (complete-
source index 394); one exclusion vetoes it while all five positive matches remain.
The deliberately broad 0.4 nm positive radius isolates that veto. At 0.35 nm
exclusion radius the unchanged reference has 12 clashes and is vetoed. Neither
choice is a validated physical radius; both explicit alternatives remain.

All 26 focused controls pass and three cookbook blocks execute on Python 3.14.7;
strict isolated cookbook rendering passes with existing 3.13 tooling. The two
driver profiles retain identical science and unchanged source/input identities.
The enabled workflow capture has 15 items/39 uses, including three input datasets,
actually reached ligand preparation/recognition and assignment references, without
G3PS or receptor-interaction credits. Constructor-only attribution excludes a
new MolSysMT extraction and retains the original inventory report unchanged.

Retained original evidence: `devguide/evidence/eralpha_exclusions_py314.json.gz`,
uncompressed SHA-256
`b927e5ef0f4c667602fc9cb941a76cfdc86fc786a81757313db2e981873b5902`.
`python -m devtools.validate_eralpha_exclusions --output FILE` reproduces the
bounded case; no timing/memory or biological acceptance is measured. Source/input
identities and complete actual provider/constructor/query/pose/attribution reports
remain in the archive. Review/incorporation and published dependency qualification
remain open.

Complete local verification: **378 tests pass in 473.81 s** on Python 3.14.7,
with eight warnings (the six previous warnings and two expected B-factor drops).
All final 26 focused controls pass after adding producer versions independent
of optional tracking. Ruff, offline reporting/index and whitespace checks pass.
All nine original evidence archives verify; the library's editable installation
is confirmed in `molsyssuite@uibcdf_3.14`. This is not hosted-matrix, immutable
provider, wheel or biological qualification.

The [owning implementation result](https://github.com/uibcdf/pharmacophoremt/issues/32#issuecomment-5973661182)
retains the public contract, scientific outcomes, guards and remaining review.

## Alternatives and refuted paths

Direct RDKit receptor access and local molecular preparation remain legacy
migration work. Physical atomic-radius tables belong to MolSysMT; the initial
builder does not claim their use. Grouped chemical features are not singleton
heavy-atom inventories. No automatic ligand-based exclusion pruning is selected.

## Scope and exclusions

One fixed-radius public builder and its independently composable controls. No
new molecular clash engine, physical pair-radius overlap, force field, implicit
chemical preparation, ligand pruning or receptor biological acceptance.
Optional backend integration is not applicable: this tool uses the existing
host geometry/units and cached inventory, with no new external engine. Ackredit
records executed construction software and retains original cached provenance;
no paper-specific exclusion algorithm is claimed or newly credited.

## Acceptance criteria

Native cached construction requires no molecular access, preserves source maps
and independent geometry/metadata, and rejects malformed/grouped/duplicate
inventories. Units, exact-boundary/inside/outside steric veto with full positive
fit, native persistence and real Ackredit absence/failure/reuse are protected.
An explicit observed receptor-geometry continuation and cookbook execute without
asserting receptor chemistry or biological readiness. Review/incorporation and
public dependency delivery remain separate gates.
