# Build explicit complementary receptor hypotheses

Use `from_receptor_projections()` for query construction from cached native
features. The `StructureBasedModeler` class and `model(method='structure-based')`
compose this tool with optional cached exclusions. Prepare/select the receptor
through MolSysMT first. Actual pocket detection belongs to TopoMT.

Development-source addition: `from_receptor_features()` enumerates separate
cached donor/aromatic alternatives under an explicit profile and finite budget;
see the final section below. It is not yet a new published package version.

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

## Enumerate cached donor/aromatic alternatives

The development-source public tool `from_receptor_features` generalizes the
[qualified receptor pilot](../validation/receptor_hypothesis_pilot.md). Choose
`receptor_profile='donor_aromatic_faces'`, both distance lists, a query radius
and a finite `max_hypotheses`. Each admitted source record contributes once to
all joint models. Aromatic +/− faces are separate alternatives; every donor-H
pair remains a separate occurrence. Unsupported chemical families are recorded
as omitted; excluded volumes require a separate inventory.

This second input is a declared planar benzene control. MolSysMT constructs,
recognizes and characterizes it. It is an analytical feature example, without a
protein pocket, steric-accessibility claim or biological binding interpretation.

```python
from pharmacophoremt.modeler import from_receptor_features

ring_source = msm.convert(
    msm.convert('smiles:c1ccccc1', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
ring_source.structures.append(coordinates=puw.quantity([[
    [.14, 0, 0], [.07, .1212435565298214, 0],
    [-.07, .1212435565298214, 0], [-.14, 0, 0],
    [-.07, -.1212435565298214, 0], [.07, -.1212435565298214, 0],
]], 'nm'))
ring_cache = get_features(ring_source, features=['aromatic ring'])
generated = from_receptor_features(
    ring_cache, receptor_profile='donor_aromatic_faces',
    donor_distances=['.28 nm'], aromatic_distances=['.35 nm', '.45 nm'],
    radius='20 pm', max_hypotheses=2,
)
assert len(generated['models']) == 2
assert generated['report']['enumeration']['total_possible'] == 4
assert generated['report']['enumeration']['remaining'] == 2
assert generated['complete'] is False
assert all(m.n_interaction_sites == 1 for m in generated['models'])
```

The prefix follows feature/distance/face order; it is not energetic ranking.
Zero budget is incomplete when eligible alternatives exist. A valid chemical
cache without admitted records returns no models and status
`no_supported_features`; a malformed admitted direction raises even with zero
budget. Donor-complement distances and aromatic distances are pharmacophoric
choices. Radius is a matching tolerance. Essentiality and weight one do not
measure binding importance.

Model metadata retain generation/underlying-projection methods, source maps,
structure/state, unit-bearing choices, omissions and enumeration scope. The
[public contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/public_receptor_generation.md)
explains native-cache versus saved-QuantityRecord semantics and the
[source receiving receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/public_receptor_generation_20261105_summary.json)
retains independent controls and the actual development environment. All
molecular operations remain MolSysMT-owned; further acceptor profiles remain
separately qualified provider/consumer work.

## Attach cached exclusions to every generated hypothesis

Obtain a separate heavy-atom inventory for the same prepared source, selection,
frame and chemical-state selector. Pass it together with an explicit exclusion
radius. The generator reuses the facade's exclusion construction and appends
independent zero-weight constraints after each hypothesis's positive sites.

```python
ring_heavy = get_features(ring_source, features=['included volume'])
with_exclusions = from_receptor_features(
    ring_cache, receptor_profile='donor_aromatic_faces',
    donor_distances=['.28 nm'], aromatic_distances=['.35 nm', '.45 nm'],
    radius='20 pm', max_hypotheses=2,
    excluded_volume_inventory=ring_heavy, excluded_volume_radius='.10 nm',
)
assert with_exclusions['report']['enumeration'] == generated['report']['enumeration']
assert with_exclusions['report']['excluded_volumes']['attached_model_count'] == 2
assert 'global_site_indices' not in with_exclusions['report']['excluded_volumes']
for hypothesis in with_exclusions['models']:
    assert hypothesis.n_interaction_sites == 7
    assert hypothesis.metadata['excluded_volumes']['global_site_indices'] == [1,2,3,4,5,6]
    assert [site.weight for site in hypothesis.interaction_sites] == [1,0,0,0,0,0,0]
```

This leaves positive enumeration and its incomplete budget unchanged. No pruning
or steric test occurs during generation. During later pose evaluation, a selected
candidate heavy-atom center strictly inside a sphere vetoes a model while its
positive fit value stays unchanged; equality is permitted. The uniform radius is
a query assumption, without physical-radius or whole-pocket accessibility claims.

Cache checks compare declared atom sets, frame and state; they do not authenticate
a common molecular source or complete heavy-atom coverage. Both optional inputs
must be supplied together, and are validated even with zero budget or no admitted
positive features. No exclusion-only positive model is returned. The
[contract and original evidence](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/receptor_generation_exclusions.md)
retain strict-boundary controls and the prepared PHE404 example under two unit
policies. Molecular loading, selection, geometry and movement remain in MolSysMT.

## Experimental cached carbonyl alternatives

The explicitly selected `donor_aromatic_carbonyl_experimental` profile also uses
provider model2/status1 acceptor geometry. This example requires a MolSysMT source
with the experimental `get_hbond_site_directions` API; the qualified producer is
`0faf1584d05ac47ddcebfc20d9c9978b7f4f230e`. Computing the cache and consuming it
are separate operations. Installed/public provider qualification remains distinct.

The following three blocks form a standalone analytical example. MolSysMT creates
and inspects the molecular source. No hydrogen optimization or pocket finding is
performed. The literal neutral-aldehyde coordinates are the unchanged #92/#93
fixture, in nm.

```python
import molsysmt as msm
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import get_features, from_receptor_features

carbonyl = msm.convert(
    msm.convert('smiles:CC=O', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
carbonyl.structures.append(
    coordinates=puw.quantity([[[0,.15,0], [0,0,0], [.12,0,0]]], 'nm')
)
carbonyl_features = get_features(carbonyl, selection=[2], features=['hb acceptor'])
carbonyl_directions = msm.interactions.hbonds.get_hbond_site_directions(
    carbonyl, selection=[2], structure_indices=[0], chemical_state='reference',
    method='ideal_local_geometry', site_method='smarts_donor_acceptor', pbc=False,
)
```

Choose a separate hypothesis per lobe, with explicit distance/radius and donor
orientation. `towards_receptor` means target D→H=-u; it is a pharmacophoric choice,
not a predicted electronic orbital or an energetic optimum. Structure position0
refers to the first entry in the provider's requested axis, even when indices repeat.

```python
with phmt.attribution():
    carbonyl_generated = from_receptor_features(
        carbonyl_features,
        receptor_profile='donor_aromatic_carbonyl_experimental',
        donor_distances=['.35 nm'], aromatic_distances=['.35 nm'],
        acceptor_directions=carbonyl_directions,
        acceptor_structure_position=0, acceptor_distances=['.35 nm'],
        acceptor_target_orientation='towards_receptor',
        radius='20 pm', max_hypotheses=2,
    )
assert carbonyl_generated['complete']
assert carbonyl_generated['report']['enumeration']['total_possible'] == 2
assert len(carbonyl_generated['models']) == 2
assert all(model.n_interaction_sites == 1 for model in carbonyl_generated['models'])
```

Native pharmacophore persistence preserves the selected provider evidence and
scientific choices. It does not recompute molecular geometry.

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from pharmacophoremt.io import to_json, load_json

with TemporaryDirectory(prefix='phmt-carbonyl-recipe-') as temporary:
    saved = Path(temporary) / 'carbonyl.json'
    to_json(carbonyl_generated['models'][0], saved)
    recovered_carbonyl = load_json(saved)
assert recovered_carbonyl.n_interaction_sites == 1
assert recovered_carbonyl.interaction_sites[0].features == ['hb donor']
```

Both donor/aromatic distance lists remain required even when their families are
absent. Unsupported, undefined and known outside-profile acceptors are omitted
with reasons; missing or incoherent caches fail before generation, including at
zero budget. Cached source-context consistency does not authenticate an unchanged
molecular system. Default position-only features and `donor_aromatic_faces` remain
available. See the [contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/public_cached_carbonyl_generation.md)
and [original carbonyl receiving case](../validation/carbonyl_acceptor_receiving.md)
for scientific limits; this example is not biological validation.
