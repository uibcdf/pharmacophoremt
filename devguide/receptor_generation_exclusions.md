# Cached exclusions in receptor hypothesis generation

Owner LMMV/dprada, [#88](https://github.com/uibcdf/pharmacophoremt/issues/88),
2026-11-05. This extends [#87](public_receptor_generation.md) with the existing
#32/#44 excluded-volume contract, without a new molecular routine.

## Scientific contract

`from_receptor_features` accepts optional `excluded_volume_inventory` and
`excluded_volume_radius`. Supply both or neither. The chemical and heavy-atom
caches must declare equal selected atom sets, structure index and chemical-state
selector. Selection ordering may differ. These checks do not authenticate one
unchanged molecular source, coordinate correspondence or complete heavy-atom
coverage; callers obtain consistent native inventories through MolSysMT.

Shared private PHMT helpers now hold StructureBasedModeler's existing context
validation and attachment. Public `get_excluded_volume_sites` constructs the
single heavy-atom recipe, preserving its singleton/duplicate/orientation/radius
checks. Each hypothesis receives independent copies after its positive sites,
with zero weight and actual global indices. The root report retains a local
recipe and `attached_model_count`; it does not invent global indices when no
model exists. The default absent-exclusion path retains its previous output.

Invalid optional inputs raise before any model even with zero hypothesis budget
or no admitted positive features. A valid zero/empty generation can still
validate/construct its recipe, but returns no exclusion-only positive model.
Positive enumeration, omission, order and completion remain unchanged. Exclusions
do not prune generated hypotheses, change fit weights, or perform a steric test
during generation. PoseEvaluator later vetoes selected candidate heavy-atom
centers strictly inside spheres; equality is permitted.

Radii are explicit uniform pharmacophoric query choices. They are neither
van der Waals radii nor a force-field overlap calculation. Molecular preparation,
coordinates, selections, transformations and physical radii remain MolSysMT-owned.
Cached matching/composition remains PHMT-owned. ArgDigest admits both optional
arguments through the existing definition-owned signature; mandatory scientific
checks survive bypass. Existing SMonitor/PyUnitWizard/Ackredit contracts apply;
there is no new optional backend or dependency floor.

## Prespecified independent controls

Freeze these methodological settings before the placed-pose checks. Reuse the
original prepared #52 PHE404 artifact, SHA-256
`a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`.
Request aromatic and heavy-atom inventories for group 404, structure zero,
reference chemistry. Ring atoms are 796–801; heavy atoms 791–801. Build both
faces at .35 nm, positional radius .02 nm and budget two, once with exclusion
radius .01 nm and once with .40 nm. Translate the candidate copy .35 nm along
the cached native axis using public MolSysMT. Never optimize H geometry or
redetect cached observations.

Test-only original-coordinate mean/SVD verifies the ring center and unoriented
axis. An independent `math.dist` enumeration over original heavy coordinates and
the declared translation defines EVERY strict-inside pair and source/global site
index. Compare all reported clashes, not a fitted count. The forward face has
positive fit one under both radii; the .40 nm veto has at least eleven pairs
because each source atom moves .35 nm. The opposite face is a valid negative.
Run nm/ps/radians and pm/fs/degrees, preserving full coordinates, chemical
history, cached observations, inventories, units and original data credit.

An additional indexed-water analytical control uses source `[2H]O`, O at origin,
H at +.1 nm, and a donor complement at +.5 nm with positional radius .4 nm and
exclusion radius .5 nm. A one-O candidate at x=.25/.5/.75 nm has positive fit one;
the first is vetoed, exact equality and outside are permitted. All molecular
construction/translations/recognition use public MolSysMT. These are selected
heavy-center controls, not binding or solvent claims. Floating comparisons use
the existing evaluator semantics; geometric oracles use 1e-12 nm tolerance.

Synthetic native-cache controls cover source maps, independence, ordering,
optional pairing, malformed and mismatched data, zero/empty budgets, native
JSON/YAML and actual optional attribution. Inputs and expected transitions stay
fixed; unexpected answers require investigation. Existing receptor, exclusion,
generation and placed-pose controls remain separate compatibility evidence.

## Scope

This qualifies query construction and explicit selected-center veto semantics.
It does not prove physical accessibility, binding relevance, optimal radii,
chemical realism, affinity or biological validity. Settings are not independent
ligands; no holdout is consulted. Existing source/floor/provider pins and #87
positive-method IDs stay unchanged. Further directions, environmental refinement,
optional pockets and installed/public/platform/hosted qualification remain separate.

## Executed qualification — 2026-11-05

The scientific settings above were frozen before execution; their original bytes,
timestamp and SHA-256 remain in the [evidence](evidence/receptor_generation_exclusions_20261105_summary.json).
All 217 selected cases pass (258.89 s), including 61 new guards, without
failures/errors/skips. The initial 53-case run also passes. A quota-interrupted
broader attempt has no complete result and remains retained, not counted as
qualification; only owned task storage relocates to ignored repository build/.

Both unit policies yield prepared 0/42 strict-inside pairs at .01/.40 nm, with
forward-face positive fit one and opposite-face zero. The indexed-water inside/
equal/outside cases retain fit one and statuses not_matched/matched/matched.
Empty requested heavy recipes, no-supported-positive validation, bypass, optional
tracking absence/failure, ownership and JSON/YAML are covered. Five cookbook
blocks and a captured prepared replay execute on final runtime bytes; bounded
strict linked-page rendering and administrative checks pass. The original input,
chemical history, observations and units remain unchanged; actual input/operation
credit is retained. Source/native/helper/test/input/metadata identities remain
stable. This is controlled Linux/Python 3.14.7 source qualification with public
ArgDigest 0.17.0 extraction, not a full-suite/installed/public/platform result.

Reexecute [the guard](../tests/test_receptor_generation_exclusions.py) after cache,
composition, geometry, veto, persistence, fixture or provider changes. Append new
evidence rather than revising this measurement. Broader comparison parameters and
regions must be declared before evaluation. Provider/biological/delivery limits
above remain; no dependency floors, pins, releases or provider sources change.
