---
summary: Build reusable exclusion spheres from native heavy-atom inventories without molecular inference.
issue: uibcdf/pharmacophoremt#32
status: resolved
opened: 2026-10-03
closed: 2026-11-03
verification: measured
area: [modeling, geometry]
guard: tests/test_excluded_volume_sites.py
normative: devguide/excluded_volume_workflow.md
blocked_by: []
supersedes: []
---

# Public heavy-atom exclusion sites

## Resolution — 2026-11-03

Reviewed and incorporated as a source/API workflow. Clean producer
25d41077a238cd3f5b54e235011df3e5b276531f passes all **26 owning controls**, zero
failures/errors/skips, in 26.06 s: 22 constructor and four observed controls.
The original driver passes both host tracking profiles with identical scientific
projections, unchanged source/input hashes, 153 spheres over 19 residues and all
seven pose/persistence outcomes. All three cookbook blocks execute; strict
isolated rendering passes with two neighboring recipe link-target stubs.

The .1 nm reference passes; a controlled O3/candidate index 3 to GLU353 OE2/
complete-source index 394 collision gives one veto with five positive matches and
fit 1. The .35 nm sensitivity control retains 12 clashes and fit 1. Native query
persistence preserves reference/collision results and metadata. Original source,
prepared ligand and heavy pose remain unchanged. Enabled workflow attribution
has 15 items/39 uses, including three input datasets; disabled host tracking still
retains actually reached provider credit (4 items/13 uses). Constructor-only
credits do not invent another extraction, G3PS or receptor interaction detection.

The [new receipt](../evidence/exclusion_acceptance_20261103_summary.json) retains
complete new outputs, source/native/helper/test/input identities, commands/logs/XML
and full before/after metadata differences. Actual module versions and physical
identities remain stable in every phase. Distribution-record lookups instead
switch to older canonical PHMT/MolSysMT/Viewer/DepDigest records: **strict full
identity equality and metadata equality are false in all three phases**. These
original differences are retained, consistent with the inherited #82 workspace
limitation; no clean installed closure is inferred or host repaired.

No runtime, test, fixture, expectation, provider, shared-prefix or sibling changes
are needed. Ordinary editable PHMT 0.4.0+56.g9387852 uses controlled MolSysMT
0faf1584 and unchanged native bytes. The Oct03 claims below remain historical.
Their legacy-migration statement is superseded by #44: the current structure
facade delegates explicit cached exclusions to this public builder; that is source
inspection here, not a new qualification of the complete facade.

This closes the bounded construction/source acceptance, not physical radii,
receptor chemistry, biological prediction, performance, clean installed/public/
Conda/platform or exact-head hosted gates. Those remain #22/#66, provider work,
#23/#10 and #9 as applicable. The old 1,020-item full run stays a dated baseline.
Owned root /tmp/phmt32-acceptance-20261103-1_kyuklf/, LMMV/dprada, review 2026-11-17.
A transient pre-science sandbox quota startup failure is retained; the default
sandbox recovered without deleting resources or changing environments.

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
