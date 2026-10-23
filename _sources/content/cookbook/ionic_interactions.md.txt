# Build queries from ionic observations

`from_interactions()` now also consumes native MolSysMT `ionic_contact`
observations. A ligand positive/negative center becomes a charge sphere using
the same recognition and geometry as `get_features()` and `PoseEvaluator`.
The molecular system must already have complete declared chemistry.

## Construct and evaluate

This prepared analytical acetate and two sodium ions demonstrate compound
membership and repeated contacts. Their coordinates are declared controls,
not an observed binding complex. All molecular operations use MolSysMT.

```python
import molsysmt as msm
import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_interactions
from pharmacophoremt.screening import PoseEvaluator

source = msm.convert(
    msm.convert('smiles:CC(=O)[O-].[Na+].[Na+]', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity([[
    [0, -.15, 0], [0, 0, 0], [-.1, .1, 0], [.1, .1, 0],
    [.1, .4, 0], [-.1, .4, 0],
]], 'nm'))
ligand, partner = [0, 1, 2, 3], [4, 5]
observations = msm.interactions.ionic.get_ionic_interactions(
    source, '0.31 nm', selection=ligand, selection_2=partner,
    selection_mode='between', structure_indices=[0], pbc=False,
)
query = from_interactions(source, observations, ligand, radius='0.02 nm')
assert observations.n_interactions == 2 and query.n_interaction_sites == 1
site = query.interaction_sites[0]
assert site.feature_name == 'negative charge'
assert site.metadata['atom_indices'] == [1, 2, 3]
assert site.metadata['geometry_atom_indices'] == [2, 3]
assert len(site.metadata['observations']) == 2
np.testing.assert_allclose(puw.get_value(site.center, to_unit='nm'), [0, .1, 0])

evaluator = PoseEvaluator(query)
reference = evaluator.evaluate(source, selection=ligand)
assert reference['status'] == 'matched' and reference['fit_value'] == 1
moved = msm.structure.translate(
    source, translation='[1,0,0] nm', selection=ligand, in_place=False,
)
negative = evaluator.evaluate(moved, selection=ligand)
assert negative['status'] == 'not_matched' and negative['fit_value'] == 0
```

The carboxylate participant comprises carbon and both oxygens, while its
position is the unweighted oxygen centroid. A guanidinium participant uses
its provider-defined nitrogen geometry. MolSysMT owns both definitions;
PharmacophoreMT does not infer which atom carries a delocalized charge.

The detector's minimum atom-contact distance and cutoff are retained in the
observations. The sphere radius above is an independent pharmacophoric matching
tolerance. Formal-charge geometric proximity is not an electrostatic energy,
affinity estimate or proof of a salt bridge.

## Capture actual work and save the query

The application owns the Ackredit session. Detect inside the capture to report
that calculation. Constructing from cached observations preserves their
original metadata without crediting another ionic detection.

```python
import tempfile
from pathlib import Path
import ackredit as ack
import pharmacophoremt as phmt
from pharmacophoremt.io import load_json, to_json

with ack.session('ionic workflow'):
    with ack.capture('detect, construct and evaluate') as workflow:
        with phmt.attribution():
            fresh = msm.interactions.ionic.get_ionic_interactions(
                source, '0.31 nm', selection=ligand, selection_2=partner,
                selection_mode='between', structure_indices=[0], pbc=False,
            )
            credited = from_interactions(source, fresh, ligand, radius='0.02 nm')
            assert PoseEvaluator(credited).evaluate(source, selection=ligand)['status'] == 'matched'
    saved_references = workflow.attribution.to_dict()
    assert any('get_ionic_interactions' in use['used_by']
               for use in saved_references['uses'])
    bibliography = ack.Attribution.from_dict(saved_references).report(format='bibtex')
    assert bibliography
    before = ack.get_attribution().to_dict()
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'ionic_query.json'
        to_json(credited, path)
        restored = load_json(path)
        assert restored.metadata == credited.metadata
        assert restored.interaction_sites[0].metadata == credited.interaction_sites[0].metadata
    assert ack.get_attribution().to_dict() == before
```

This native minimum-distance criterion supplies no named article in the current
MolSysMT declaration. The report credits executed software and the evaluator's
actual assignment method; it does not borrow a ProLIF or search-method citation.
Ackredit is optional for construction/evaluation. Attribution and persistence
retain producer versions and original observation criteria separately.

## Compose charge sites with exclusions

The independently public exclusion builder can be used with this query. The
broad positive radius below deliberately isolates the steric veto: a translated
ligand still satisfies the positive site but places an oxygen on a partner ion.
The exclusion radius is a declared control, not a physical atomic radius.

```python
from pharmacophoremt.modeler import get_features, get_excluded_volume_sites

broad = from_interactions(source, observations, ligand, radius='0.4 nm')
collision = msm.structure.translate(
    source, translation='[0,0.3,0] nm', selection=ligand, in_place=False,
)
assert PoseEvaluator(broad).evaluate(collision, selection=ligand)['status'] == 'matched'
inventory = get_features(source, selection=partner, features=['included volume'])
exclusions = get_excluded_volume_sites(inventory, radius='0.05 nm')
for exclusion in exclusions['interaction_sites']:
    broad.add_interaction_site(exclusion)
result = PoseEvaluator(broad).evaluate(collision, selection=ligand)
assert result['fit_value'] == 1 and result['status'] == 'not_matched'
assert len(result['excluded_volume_clashes']) == 2
assert PoseEvaluator(broad).evaluate(source, selection=ligand)['status'] == 'matched'
```

Pass the same unchanged source, state, atom axes and frame as the observations.
Selections cutting a compound center, incompatible recognition definitions,
uncovered frames and nonzero periodic images are rejected. An evaluated-empty
analysis yields an empty model, which `PoseEvaluator` refuses. The one-site
example does not meet the rigid triplet search's three-center requirement.

The retained analytical validation also covers atomic ions and guanidinium in
both ligand roles, with host tracking on/off, displacement negatives and JSON
round trips. From a source checkout:
`python -m devtools.validate_ionic_interactions --output ionic_validation.json`.
This does not prepare the ERalpha receptor or establish biological performance.
