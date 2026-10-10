# Review cached prepared receptor hypotheses and contacts

Consume the existing [prepared ERα fragment](prepared_eralpha_interface.md)
without repeating hydrogen preparation or contact detection. This example uses
a translated PHE404 as a synthetic geometric candidate. It does not predict a
binding pose or establish biological acceptance.

## Build separately declared projections

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import molsysmt as msm
from devtools.prepared_receptor_workflow import load_input, projections
from pharmacophoremt.modeler import get_features
from pharmacophoremt.screening import PoseEvaluator

with TemporaryDirectory(prefix='phmt-cached-receptor-') as directory:
    source, identity = load_input(Path(directory))
selection = msm.select(source, selection='group_id == "404"')
inventory = get_features(source, selection=selection, features=['aromatic ring'])
heavy = get_features(source, selection=selection, features=['included volume'])
models, modeler = projections(source, inventory, heavy)
moved = msm.structure.translate(source, translation='[0,0,.35] nm', in_place=False)
positive = PoseEvaluator(models['projected']).evaluate(moved, selection=selection)
veto = PoseEvaluator(models['collision']).evaluate(moved, selection=selection)
assert positive['status'] == 'matched' and positive['fit_value'] == 1
assert veto['status'] == 'not_matched' and veto['fit_value'] == 1
assert PoseEvaluator(models['opposite']).evaluate(moved, selection=selection)['status'] == 'not_matched'
assert PoseEvaluator(models['projected']).evaluate(source, selection=selection)['status'] == 'not_matched'
```

The fixed client declares ±z projection alternatives at 0.35 nm with matching
radius 0.02 nm, explicitly retaining the cached MolSysMT ring axis as target
orientation. Eleven heavy-atom exclusions use radius 0.01 nm; the veto model
broadens them to 0.40 nm. A molecular translation of 0.35 nm clears the narrow
exclusions but enters its own broadened original-atom spheres. Coverage one
therefore cannot by itself establish acceptance. These are explicit query
choices; no direction, pocket or physical-radius inference is performed.

## Reconstruct original observed evidence

```python
from pharmacophoremt.modeler import ComplexBasedModeler
from pharmacophoremt._private.smonitor.exceptions import ArgumentError

ligand = msm.select(source, selection='group_name == "EST"')
observed = ComplexBasedModeler(source, ligand_selection=ligand,
    interaction_collection=source.interactions)
query = observed.build([0])
assert query.n_interaction_sites == 6
assert PoseEvaluator(query).evaluate(source, selection=ligand)['status'] == 'matched'
assert {row['label']:row['n_observations']
        for row in query.metadata['interaction_collection']['analyses']} == {
    'hydrophobic':12, 'hbonds':0, 'pi_pi':0}
for facade in (modeler, observed):
    try:
        facade.build([1])
    except (ArgumentError, msm.ArgumentError):
        pass
    else:
        raise AssertionError('Uncached/unevaluated frame must fail')
    assert facade.result is None
# An existing frame also fails when its observations were explicitly invalidated.
observed.interaction_collection = {
    label: value.invalidate_structures([0]) for label, value in source.interactions.items()}
try:
    observed.build([0])
except ArgumentError:
    pass
else:
    raise AssertionError('Invalidated observations cannot cover frame zero')
assert observed.result is None
```

The H-bond/pi-pi families are evaluated-empty historical observations. They are
retained with their original criteria and maps; reading does not redetect them.
The source stays unchanged. Molecular decoding, selection, recognition, planes
and movement all use MolSysMT. Missing molecular geometry remains provider-owned.

```bash
python -m devtools.prepared_workflow --case receptor --output /tmp/prepared-receptor.json
python -m pytest tests/test_prepared_receptor_workflow.py --receptor=llm
```

The [validation case](../validation/prepared_receptor_workflow.md) retains original
atom/plane/contact-distance oracles, empty/failure controls, twelve saved models
across JSON/YAML/PHMT SDF, alternate units, actual attribution and fresh readers.
