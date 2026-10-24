# Build explicit complementary receptor hypotheses

Use `from_receptor_projections()` for query construction from cached native
features. The `StructureBasedModeler` class and `model(method='structure-based')`
compose this tool with optional cached exclusions. Prepare/select the receptor
through MolSysMT first. Actual pocket detection belongs to TopoMT.

This small propane input is an analytical recognition/placement control, not a
protein pocket or a biological binding model. All molecular construction and
movement below use the provider. The direction and distance are deliberately
chosen hypothesis parameters, without a molecular direction inference routine.

```python
import molsysmt as msm
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import (
    StructureBasedModeler, from_receptor_projections, get_features,
)
from pharmacophoremt.screening import PoseEvaluator

source = msm.convert(msm.convert('smiles:CCC', to_form='rdkit.Mol'),
                     to_form='molsysmt.MolSys')
source.structures.append(coordinates=puw.quantity(
    [[[0,0,0], [.15,0,0], [.30,0,0]]], 'nm'))
inventory = get_features(source, features=['hydrophobicity'])
heavy = get_features(source, features=['included volume'])
assert len(inventory['features']) == 1
specs = [dict(
    feature_index=0, projection_direction=[0,1,0], distance='3.5 angstrom',
    label='analytical positive-y hypothesis',
    evidence={'producer': 'caller-declared analytical control'},
)]
query = from_receptor_projections(inventory, projection_specs=specs,
                                 radius='20 pm')
assert query.n_interaction_sites == 1
assert query.interaction_sites[0].metadata['atom_indices'] == [1]
candidate = msm.structure.translate(source,
    translation=puw.quantity([[[0,.35,0]]], 'nm'), in_place=False)
assert PoseEvaluator(query).evaluate(candidate)['status'] == 'matched'
assert PoseEvaluator(query).evaluate(source)['status'] == 'not_matched'
```

`feature_index` refers to the inventory's feature-list position, not an atom
index. Unlisted features emit no sites. Source indices remain in site metadata;
projection labels/evidence are caller declarations. Cached inventories must
retain native quantities. Their origin and common coordinates remain your
responsibility; model construction does not authenticate them against a system.

Each source feature has at most one projection in a hypothesis. Alternative
faces/directions require separate calls. Every emitted site starts essential,
with weight one. An explicitly empty list yields an empty hypothesis, which
cannot be evaluated as a positive query.

```python
modeler = StructureBasedModeler(source, feature_inventory=inventory,
    projection_specs=specs, radius='20 pm',
    excluded_volume_inventory=heavy, excluded_volume_radius='10 pm')
combined = modeler.build(structure_indices=[0])
assert modeler.result is combined
assert combined.n_interaction_sites == 4
assert combined.metadata['excluded_volumes']['global_site_indices'] == [1,2,3]
assert sum(site.weight for site in combined.interaction_sites) == 1
assert PoseEvaluator(combined).evaluate(candidate)['status'] == 'matched'
named = phmt.model(source, method='structure-based',
    feature_inventory=inventory, projection_specs=specs, radius='20 pm')
assert named.n_interaction_sites == 1
empty = from_receptor_projections(inventory, projection_specs=[])
assert empty.n_interaction_sites == 0
```

Exclusions require both a heavy-atom inventory and an explicit radius. The
facade checks equal declared atom sets, frame and chemical-state selector, then
delegates to `get_excluded_volume_sites()`. Uniform radii are query choices,
not physical atomic radii. Exclusions have weight zero and veto candidate
heavy-atom centers strictly inside their spheres. No surface sampling, pocket
pruning or coordinate movement is performed during query composition.

A receptor donor produces a spherical ligand acceptor. A receptor acceptor
produces a ligand donor and requires an independent `target_direction`.
Aromatic projections require an independent `target_normal` and emit a Disk.
Charges are complemented; hydrophobic/aromatic kinds remain the same.
Projection direction and target orientation are different hypothesis decisions;
neither a negative-direction shortcut nor a first-neighbor fallback is assumed.

```python
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from pharmacophoremt.io import load_json, to_json

with TemporaryDirectory(prefix='phmt-receptor-recipe-') as directory:
    path = Path(directory) / 'hypothesis.json'
    to_json(combined, file_name=str(path))
    saved = load_json(str(path))
    assert saved.metadata == combined.metadata
    assert saved.n_interaction_sites == 4
    assert PoseEvaluator(saved).evaluate(candidate)['status'] == 'matched'
json.dumps(combined.metadata, allow_nan=False)
```

The old pocket-selection/sphere arguments, automatic exclusions and fixed
projection rules are retired. Request exactly the cached frame; multiple
frames need separate inventories/modelers. The prepared molecular reference is
retained without reading or converting it. Cached molecular evidence and optional
attribution survive persistence without registering another recognition run.

Missing provider donor-pair/local acceptor direction geometry is requested in
[MolSysMT #375](https://github.com/uibcdf/molsysmt/issues/375); existing donor-vector
arithmetic in `get_features()` remains tracked under PharmacophoreMT #41.
Environmental hydrogen refinement is separately MolSysMT #323. This method
declares query geometry explicitly and does not claim automatic chemically
informed pocket modeling, legacy equivalence, affinity or activity validation.
