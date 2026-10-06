# Reusable exclusion-site construction

The owning issue is [#32](https://github.com/uibcdf/pharmacophoremt/issues/32).
`modeler.get_excluded_volume_sites(feature_inventory, radius=...)` constructs
excluded-volume Sphere sites from a native heavy-atom inventory. It is a separate
pharmacophoric operation; workflows choose its inputs and compose its output.

## Ownership and contracts

MolSysMT owns molecular conversion, elements, coordinates, frames, selections,
preparation and any atomic-radius definitions. `get_features(...,
features=['included volume'])` obtains source-indexed heavy-atom geometry through
those public boundaries. This branch does not run chemical SMARTS or require a
completed receptor chemical assignment. It still requires the native inventory's
declared source selection and a finite coordinate frame; it does not authenticate
source identity or complete missing molecular data.

The new builder owns the Feature + Shape decision to place one sphere per
singleton volume record. It accepts only a native supported inventory, requires
an explicit positive finite scalar length, rejects chemical/grouped/oriented/
duplicate records, and copies geometry/metadata. An empty declared feature list
constructs no sites; it does not prove that a molecular source has no heavy atoms.
Input inventories and generated sites/reports have independent ownership.

The result contains `interaction_sites` and a detached
`pharmacophoremt.excluded_volume_sites@1` report. Reports retain original source
indices, frame/state declarations, the source inventory, selected radius and
local list indices. Add sites to a query with `Pharmacophore.add_interaction_site`.
Local exclusion indices become different global query indices after composition;
candidate atom indices in clash results belong to the evaluated candidate.

Callers guarantee the common coordinate frame. No alignment, periodic imaging,
ligand-based pruning, atomic-radius inference or receptor chemistry preparation
occurs. The constant radius is a modeling choice. The tool does not implement a
pairwise van der Waals sum, solvent surface, clash energy or a named third-party
exclusion-generation algorithm. Physical radii can be obtained from MolSysMT;
using those in another strategy needs its own declared construction semantics.

## Evaluation and compatibility

Sites have `features=['excluded volume']`, Sphere geometry, zero positive-fit
weight and explicit source metadata. Existing `PoseEvaluator` behavior stays:
candidate **heavy-atom centers strictly inside** a sphere veto the pose. Equality
is permitted. Exclusions do not contribute to matched/total positive weight;
essential/optional flags do not soften their veto. An exclusion-only query is
invalid. A pose can have positive geometric fit 1 and `status='not_matched'`.

This version constructs uniform radii, retaining that option even if later
strategies use atom-dependent physical radii, surfaces or reference-volume
pruning. Those future methods need independent definitions and comparisons.
Legacy structure-based direct RDKit exclusion construction remains separately
owned migration work; this tool does not silently redirect that modeler.

## Attribution and persistence

The existing deferred host adapter records construction software actually used:
PharmacophoreMT, NumPy and PyUnitWizard. No MolSysMT molecular operation runs
inside cached construction. Original inventory attribution remains in the
detached source inventory without being tracked as another extraction. Actual
provider chemistry/reference credits arise from earlier workflow stages.

Applications own sessions/captures and can save the constructor's portable
attribution beside its JSON report or native query. Repeated and empty
constructions retain full bibliography even when Ackredit deduplicates identical
uses. Genuine absence, controlled tracking failure and a fresh reader preserve
scientific output/original versions. Optional external-engine policy is not
applicable to this builder: no new engine, dependency or fallback is introduced.
There is no paper-specific algorithm to credit in the fixed-radius constructor.

## Independent controls and observed continuation

`tests/test_excluded_volume_sites.py` supplies analytical construction, validation,
detachment, units, exact-boundary/inside/outside veto, persistence and real
Ackredit/lazy-import/absence/reader controls. Three analytical candidate
placements all retain full positive fit; only the inside placement is vetoed.
`tests/test_eralpha_exclusions.py` composes the independently prepared observed
EST with raw receptor geometry and protects both source index spaces.

The observed recipe/driver selects the same 19-residue 0.5 nm nonperiodic shell
under #22 and obtains its 153 heavy-atom records. A 0.1 nm exclusion radius admits
the unchanged reference pose. A controlled translation puts ligand O3 (candidate
index 3) onto receptor GLU353 OE2 (complete-source index 394); one clash vetoes
the pose while all five positive feature matches remain. A deliberately broad
0.4 nm positive radius isolates the exclusion effect; it is not the earlier
0.02 nm pose-recovery hypothesis or a biologically validated cutoff.

Increasing exclusions to 0.35 nm rejects the unchanged reference with 12
atom/site clashes and still positive fit 1. This demonstrates radius sensitivity,
not validation or a universal preference for 0.1 nm. Both declared alternatives
remain reproducible. Native query JSON preserves geometry, metadata and original
reference/collision outcomes. Source/receptor chemistry and heavy poses remain
unchanged. Generated ligand H remain local geometry, not receptor-refined H.

The receptor still lacks chemical fields needed for interaction recognition.
No receptor interaction detector runs in this continuation; no binding affinity,
enrichment, full clash-physics model or complete receptor readiness is inferred.
Receptor preparation stays with MolSysMT #298. Independent construction can
advance while that provider work remains open.

Run `python -m devtools.validate_eralpha_exclusions --output FILE`. It retains
complete preparation/construction/readiness/pose reports, source/input identities,
both actual host-tracking profiles and enclosing method/resource attribution.
It measures no timing or memory. The
[cookbook](../docs/content/cookbook/excluded_volumes.md) exposes the separate steps.

The first focused run passes **26 controls** on Python 3.14.7 (22 constructor
controls and four observed controls). The final focused run also passes after
adding software versions to the report independent of optional tracking. Three
recipe blocks execute on 3.14, and strict isolated cookbook rendering passes with
existing 3.13 documentation tools. The complete off/on evidence driver preserves
identical science and unchanged producers/inputs; its enabled capture retains
15 bibliographic items and 39 uses, with three actually used datasets, actual
ligand preparation/recognition and assignment references. No G3PS or receptor
interaction calculation runs. Original evidence is retained in
[the evidence collection](evidence/README.md).

The complete local suite passes **378 tests in 473.81 s** on Python 3.14.7, with
eight warnings: the six previous warnings and two additional expected B-factor
drops from the H-prepared observed controls. The final 26 focused controls pass
after adding actual producer versions to the construction report independent of
optional attribution. Ruff, offline reporting/index and whitespace checks pass;
all nine original evidence archives verify. Editable installation in the requested
3.14 environment is confirmed. No hosted matrix or public provider delivery is
inferred from these local results.

The [owning result](https://github.com/uibcdf/pharmacophoremt/issues/32#issuecomment-5973661182)
retains the implementation and review handoff. The receptor case remains under
#22; no provider chemical-preparation completion is inferred.
