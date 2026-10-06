# Build queries from aromatic observations

`from_interactions()` accepts native MolSysMT `pi_pi` and `cation_pi`
observations. A ligand ring becomes an aromatic disk; a ligand cation becomes
a positive-charge sphere. Construction and `PoseEvaluator` use the same shared
classical feature inventory. MolSysMT supplies all molecular recognition,
geometry and interaction detection.

## Construct a ring query and check its orientation

These benzene coordinates are declared analytical controls. They do not
represent a deposited binding complex. The reference profile is an explicit
choice; no profile is asserted to be the best.

```python
import molsysmt as msm
import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_interactions
from pharmacophoremt.screening import PoseEvaluator

theta = np.arange(6) * np.pi / 3
ring_xyz = np.column_stack((.14 * np.cos(theta), .14 * np.sin(theta), np.zeros(6)))

def prepared(smiles, xyz):
    system = msm.convert(
        msm.convert('smiles:' + smiles, to_form='rdkit.Mol'),
        to_form='molsysmt.MolSys',
    )
    system.structures.append(coordinates=puw.quantity([xyz], 'nm'))
    return system

source = prepared('c1ccccc1.c1ccccc1', np.vstack((ring_xyz, ring_xyz + [0, 0, .35])))
ligand, partner = list(range(6)), list(range(6, 12))

def detect_rings():
    return msm.interactions.pi_pi.get_pi_pi_interactions(
        source, selection=ligand, selection_2=partner,
        selection_mode='between', structure_indices=[0], pbc=False,
        method='plane_angle_intersection', profile='smarts_5_6',
    )

observations = detect_rings()
query = from_interactions(source, observations, ligand, radius='.02 nm')
assert observations.n_interactions == 1 and query.n_interaction_sites == 1
site = query.interaction_sites[0]
assert site.feature_name == 'aromatic ring' and site.shape_name == 'disk'
np.testing.assert_allclose(puw.get_value(site.center, to_unit='nm'), [0, 0, 0], atol=1e-15)
assert abs(np.dot(site.shape.normal, [0, 0, 1])) > .999
evaluator = PoseEvaluator(query, direction_tolerance='10 degrees')
assert evaluator.evaluate(source, selection=ligand)['status'] == 'matched'

# An aromatic plane is unoriented: either normal sign describes the same plane.
site.shape.normal = -site.shape.normal
assert evaluator.evaluate(source, selection=ligand)['status'] == 'matched'
orthogonal = prepared('c1ccccc1', ring_xyz[:, [2, 0, 1]])
assert evaluator.evaluate(orthogonal)['status'] == 'not_matched'
displaced = msm.structure.translate(
    source, selection=ligand, translation='[1,0,0] nm', in_place=False,
)
assert evaluator.evaluate(displaced, selection=ligand)['fit_value'] == 0
```

The query disk uses the shared least-squares ring plane. Some upstream detectors
use three-atom planes instead; their original criteria remain in the observation
metadata. Detection cutoffs, query radii and evaluation direction tolerances are
independent choices. A geometric fit does not estimate interaction energy.

## Keep actual method credits and undefined measures

The application owns the Ackredit session. Detect inside the capture to credit
the actual calculation; constructing from cached observations does not execute
the detector again. This reference profile declares the ProLIF article.

```python
import tempfile
from pathlib import Path
import ackredit as ack
import pharmacophoremt as phmt
from pharmacophoremt.io import load_json, to_json

with ack.session('aromatic workflow'):
    with ack.capture('detect, construct and evaluate') as workflow:
        with phmt.attribution():
            fresh = detect_rings()
            credited = from_interactions(source, fresh, ligand, radius='.02 nm')
            assert PoseEvaluator(credited).evaluate(source, selection=ligand)['status'] == 'matched'
    references = workflow.attribution.to_dict()
    assert any(item.get('doi') == '10.1186/s13321-021-00548-6'
               for item in references['items'])
    bibliography = ack.Attribution.from_dict(references).report(format='bibtex')
    assert bibliography
    before = ack.get_attribution().to_dict()
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'aromatic_query.json'
        to_json(credited, path)
        restored = load_json(path)
        assert restored.metadata == credited.metadata
        assert restored.interaction_sites[0].metadata == credited.interaction_sites[0].metadata
    assert ack.get_attribution().to_dict() == before

# Parallel planes have no defined plane-intersection distance.
measure = restored.interaction_sites[0].metadata['observations'][0]['measurements']['intersection_distance']
value = puw.QuantityRecord.from_dict(measure).to_quantity(unit='nm')
assert np.isnan(puw.get_value(value, to_unit='nm'))
```

The undefined distance remains NaN inside a sealed PyUnitWizard quantity record
that can be stored in standard JSON. It is not replaced with zero. Molecular
coordinates, query centers and normals must still be finite. Ackredit is optional
for scientific construction/evaluation; reading a stored query adds no credits.

MolSysMT currently offers these compatible native profile choices:

| Interaction | Method | Profile | Declared reference |
| --- | --- | --- | --- |
| pi_pi | centroid_angle_offset | least_squares | MolSysMT proposal, explicit cutoffs |
| pi_pi | centroid_angle_offset | three_atom_plane | Mol* geometry |
| pi_pi | plane_angle_intersection | aromatic_cycles | MDTraj geometry |
| pi_pi | plane_angle_intersection | smarts_5_6 | ProLIF 2.2.2 |
| cation_pi | centroid_angle_offset | least_squares | MolSysMT proposal, explicit cutoffs |
| cation_pi | centroid_distance_offset | three_atom_plane | Mol* geometry |
| cation_pi | centroid_distance_angle | smarts_5_6 | ProLIF 2.2.2 |

For the proposal, specify `distance_threshold`, `angle_threshold`,
`offset_threshold` and `planarity_threshold` with units. Reference criteria and
citations come from native provider declarations. Reference methods do not imply
execution of their original packages. Primary documentation explains
[ProLIF's interaction definitions](https://prolif.readthedocs.io/en/stable/_modules/prolif/interactions/interactions.html)
and [Mol* interaction analysis](https://molstar.org/docs/extensions/interactions/).

## Choose compound-cation mapping explicitly

For this prepared guanidinium, the ProLIF reference reports three single-atom
cation observations. They cannot exactly match the shared compound positive
center. The default raises a calculation error. An explicit containing-center
policy maps each singleton to its uniquely containing shared charge center,
retaining all observations and their original atomic charges.

```python
guanidinium = prepared(
    'NC(=[NH2+])N.c1ccccc1',
    np.vstack(([
        [-.05, 0, .35], [0, 0, .35], [.05, 0, .35], [0, .03, .35],
    ], ring_xyz)),
)
cation, aromatic = list(range(4)), list(range(4, 10))
contacts = msm.interactions.cation_pi.get_cation_pi_interactions(
    guanidinium, selection=cation, selection_2=aromatic,
    selection_mode='between', structure_indices=[0], pbc=False,
    method='centroid_distance_angle', profile='smarts_5_6',
)
assert contacts.n_interactions == 3
try:
    from_interactions(guanidinium, contacts, cation)
except ValueError as error:
    assert 'does not map uniquely' in str(error)
    strict_fit = None  # Failed construction has no geometric score.
else:
    raise AssertionError('Expected strict participant mapping to reject singletons')
assert strict_fit is None

charge_query = from_interactions(
    guanidinium, contacts, cation,
    cation_mapping='containing_center', radius='.02 nm',
)
charge_site = charge_query.interaction_sites[0]
assert charge_query.n_interaction_sites == 1
assert charge_site.feature_name == 'positive charge'
assert charge_site.metadata['atom_indices'] == [0, 1, 2, 3]
assert charge_site.metadata['geometry_atom_indices'] == [0, 2, 3]
np.testing.assert_allclose(puw.get_value(charge_site.center, to_unit='nm'), [0, .01, .35], atol=1e-15)
assert len(charge_site.metadata['observations']) == 3
assert {row['measurements']['cation_charge']['values']
        for row in charge_site.metadata['observations']} == {0, 1}
assert PoseEvaluator(charge_query).evaluate(guanidinium, selection=cation)['status'] == 'matched'
```

The original singleton formal charges are checked through MolSysMT, including
neutral resonance atoms. The compound's net charge and nitrogen centroid remain
separate. The explicit policy is limited to singletons from this declared
reference profile; it does not relax exact ring membership. Fused-ring bases
with different membership can therefore require another explicit future policy.

Use the same unchanged prepared source, state, atom axes and frame as the
observations. Partial selections, uncovered frames and nonzero periodic images
are rejected. These sites can compose with the independent
[exclusion builder](excluded_volumes.md). A one-site query cannot seed a rigid
triplet search, which requires three distinct centers.

From a source checkout, run
`python -m devtools.validate_aromatic_interactions --output aromatic_validation.json`
to compare the seven profiles on parallel/edge rings and atomic/compound cations,
both ligand roles, tracking on/off, displacement and persistence. These controls
establish adapter behavior, not biological accuracy, runtime rankings or receptor
preparation for the deposited ERalpha complex.
