# Reusing feature inventories across queries

Case `feature-inventory-reuse-20261107`, owners LMMV/dprada;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108).
Evidence class: bounded native-subworkflow equivalence, with analytical controls
and three previously prepared real inputs. No biological or performance validation.

The [declared case and receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/feature_inventory_reuse.md)
compare fresh extraction against one in-memory inventory reused for two distinct
references. Both use the same public correspondence and explicit-placement
tools, with native post-fit recognition and checked-pose evaluation retained.
Full native evidence agrees in all six source/reference comparisons.

The original PubChem3D snapshots supply acetaminophen, aspirin and caffeine,
with2/4/3 acceptor features. References are caffeine and aspirin. Original supplied
states, hydrogens, coordinates and byte identities remain unchanged; no new source
request or conformer generation occurs. Input rights/provenance and local-only
geometry custody retain the [original pilot](pubchem3d_library_pilot.md)'s scope.

| Source CID | Caffeine proposals / selected / accepted | Aspirin proposals / selected / accepted |
| --- | --- | --- |
| 1983 | 0 / 0 / 0 | 0 / 0 / 0 |
| 2244 | 24 / 1 / 0 | 24 / 1 / 1 |
| 2519 | 6 / 1 / 1 | 24 / 1 / 0 |

Both self-placements score1 under the declared checked-pose criterion. Only the
first mapping is fitted per query/arm. An empty accepted prefix with omitted
mappings is unevaluated work, not a compound negative; placement acceptance and
all-essential query matching are also distinct. This is not an equivalent run
of `RigidPoseSearch`, an affinity prediction or an activity-labeled cohort.

The controlled outer extraction requests are fresh6 versus reused3. Native
post-fit extraction and final evaluation still run. Fewer outer requests establish
neither speedup nor an indexing strategy. Preserved software/method attribution
records actual native branches; manual source provenance remains separate.

The [public recipe](../cookbook/modular_rigid_tools.md#reuse-one-prepared-source-across-queries)
demonstrates the same composition principle without the experimental helper.
All four Python blocks were executed. It fits all six mappings for its original
analytical charge triangle and none for its changed-distance reference, within
its explicit budget. Reading detached JSON does not reconstruct a native
quantity-bearing inventory; reuse requires the unchanged source, explicit
requested families, selection, frame and chemical state.

The receipt preserves exact source overlays, environment/native identity, actual
resource limits, original logs and full local outputs. Reexecute under a new
identity after relevant code/provider/input changes; preserve historical results
and authorization/hash requirements. Source controls and a recipe execution
do not qualify a new installed/public artifact or supported-platform matrix.
