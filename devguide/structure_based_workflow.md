# Explicit receptor projection workflow

Owner: [PharmacophoreMT #44](https://github.com/uibcdf/pharmacophoremt/issues/44),
under the molecular-ownership migration in #41. Development contract, 2026-10-10.

`from_receptor_projections()` builds a complementary ligand hypothesis from a
cached native `get_features()` receptor inventory. MolSysMT owns receptor
selection, preparation, chemical recognition, coordinates, centers, molecular
directions and planes. TopoMT owns actual pocket detection. PharmacophoreMT
owns choosing contributing features, query placement, matching tolerance and
complementary feature types. The constructor performs no molecular access.

`projection_specs` is an explicit list, including an explicitly empty list when
no projection is requested. Each mapping requires `feature_index` (inventory-list
position), `projection_direction` (dimensionless query vector), `distance`
(positive finite scalar length with units) and a nonempty `label`. Optional
`evidence` is a caller-supplied mapping; its producer/model is not authenticated.
Vectors are normalized as query parameters. Placement is
`source_feature_center + normalized_projection_direction * distance`.
Radius is a separate matching tolerance, default `0.15 nm`.

| Receptor kind | Complementary ligand target | Target geometry |
| --- | --- | --- |
| HB donor | HB acceptor | Sphere; native acceptors have no orientation |
| HB acceptor | HB donor | SphereAndVector; require `target_direction` |
| Aromatic ring | Aromatic ring | Disk; require `target_normal` |
| Positive charge | Negative charge | Sphere |
| Negative charge | Positive charge | Sphere |
| Hydrophobicity | Hydrophobicity | Sphere |

Target orientation is independently declared, with dimensionless units, and is
not inferred as the negative projection direction or as a molecular lone pair.
Other kinds cannot specify non-null target orientation. Receptor `normal` and
`direction` fields are retained as source evidence, not automatically used as
projection policy. All source records must be classical chemical features;
heavy-atom exclusion records belong in a separate inventory.

Unlisted source features emit no sites and are recorded as omitted. Each feature
may appear once in one hypothesis. To explore two ring faces or multiple local
directions, construct separate hypotheses and evaluate them independently;
combining alternatives as simultaneous essential sites changes the question.
Sites are essential with weight one. Explicit empty inventories/projection lists
produce empty models; an empty or exclusion-only model is not a valid positive
`PoseEvaluator` query. No observed interaction or affinity claim is inferred.

The historical `StructureBasedModeler` and `model(method='structure-based')`
delegate to this public constructor. Pass the same unchanged prepared source as
`molecular_system`, plus `feature_inventory` and `projection_specs`. The source
is retained as a reference and is not converted, unwrapped, inspected or moved.
`build()` returns one model for the inventory's frame; an explicit integer or
one-element sequence must match that frame. Multiple frames require separate
inventories/modelers. A successful result is stored in `result`; entered build
attempts clear it before validation and do not publish partial results.

Exclusions are optional. Supply both `excluded_volume_inventory` from
`get_features(..., features=['included volume'])` and an explicit
`excluded_volume_radius`, or neither. The facade requires the same declared atom
set, frame and chemical-state selector for both inventories, then calls the
existing public `get_excluded_volume_sites()`. Exclusions have weight zero and
retain local site correspondence plus their global appended indices. No surface
selection, van der Waals assignment or ligand-based pruning is performed.

Cached inventories carry caller-declared origin and common coordinates. Equal
atom indices/frame/state selectors do not prove two inventories came from the
same source or unchanged coordinates. Native quantities are required; detached
metadata JSON is preserved for inspection, not decoded as a native inventory.
Site geometry/metadata and model provenance are detached from caller inputs;
optional construction attribution credits reached query operations, while
cached recognition attribution is preserved without a new recognition claim.

The old `selection`, `pocket_selection`, `pocket_center`, `pocket_radius`,
`PROJECTION_RULES`, automatic heavy-atom exclusions and `add_excluded_volumes`
build option are retired. Dispatcher ligand/receptor selection arguments also
raise instead of being ignored. Resolve molecular selections in MolSysMT before
obtaining the inventory. Legacy first-neighbor/+z, RDKit SMARTS and ring geometry
have no hidden fallback. This is a new explicit scientific contract; matching
old model counts is not an acceptance criterion.

Missing reusable donor-pair vectors and named local acceptor geometry are
requested in [MolSysMT #375](https://github.com/uibcdf/molsysmt/issues/375).
Existing local donor-vector arithmetic in `get_features()` remains outstanding
under #41, reviewed by 2026-10-17 or before extension; this facade adds none.
MolSysMT #323 environmental refinement remains independent. Until a provider
contract is delivered, declare hypotheses explicitly rather than deriving
molecular directions in this package. Automatic chemically informed pocket
hypotheses and biological qualification remain future work.

See [the executable recipe](../docs/content/cookbook/structure_based_modeler.md)
and `tests/test_receptor_projections.py` for independent controls.
