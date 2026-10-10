# Build a complex model from prepared native observations

`ComplexBasedModeler` consumes explicit MolSysMT observations on an unchanged
prepared source. Choose the molecular preparation and detection methods in
MolSysMT first, then pass a named collection and an explicit ligand selection.
The class and the default `phmt.model()` route perform no implicit preparation
or detection. Native profiles have a different scientific contract from the
retired complex heuristics; old threshold or receptor-selection arguments fail.

Run these blocks from the source checkout in the compatible development
environment. This disconnected analytical control exercises five interaction
families with independently declared geometry; it is not a biological complex.
The fixture creates its declared topology through public MolSysMT conversion;
`observe()` calls the public provider detectors with explicit profiles, selections,
frame zero, cutoffs and no periodic boundaries. See
[interaction composition](interaction_composition.md) for those detection choices.

```python
import molsysmt as msm
import numpy as np
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import ComplexBasedModeler
from devtools.interaction_collection_cases import build_case, observe

source, ligand, partner = build_case()
analyses = observe(source, ligand, partner)
before = puw.get_value(msm.get(source, coordinates=True), to_unit='nm').copy()
options = dict(ligand_selection=ligand, interaction_collection=analyses,
               radius='.02 nm')
modeler = ComplexBasedModeler(source, **options)
query = modeler.build()
assert query is modeler.result and query.n_interaction_sites == 9
assert sum(site.weight for site in query.interaction_sites) == 9
assert {site.feature_name for site in query.interaction_sites} == {
    'hydrophobicity', 'hb donor', 'positive charge', 'aromatic ring'}
assert sum(row['action'] == 'reused' for row in query.metadata['site_map']) == 2
```

The named method and the default dispatcher require the same explicit options.
They delegate to `from_interaction_collection()` rather than calculating new
observations. The query radius is independent of the detector cutoffs.

```python
named = phmt.model(source, method='complex-based', **options)
default = phmt.model(source, **options)
assert named.n_interaction_sites == default.n_interaction_sites == 9
np.testing.assert_array_equal(
    puw.get_value(msm.get(source, coordinates=True), to_unit='nm'), before)
```

An evaluated empty family remains explicit and produces no invented sites.
Missing observations or an unevaluated frame raises; neither becomes an empty
negative result. Do not screen a zero-site query as if it had positive weight.

```python
empty = ComplexBasedModeler(
    source, ligand_selection=ligand,
    interaction_collection={'empty': analyses['ionic_empty']}).build()
assert empty.n_interaction_sites == 0
assert empty.metadata['components'][0]['metadata']['evaluated_structure_indices'] == [0]
```

For ensembles call `modeler.build(structure_indices=[1, 0])`, or pass those indices
to `phmt.model()`, after every analysis has evaluated both frames on the same
source. A single index returns one model; multiple indices return an ordered list.
Failed rebuilds clear `modeler.result` and do not return partial models.

The [prepared ERα interface](prepared_eralpha_interface.md) supplies a traceable
real fragment: six hydrophobic sites with evaluated-empty H-bond/pi-pi families.
Those empties retain the current hydrogen/geometry limitations and are not repaired
inside PharmacophoreMT. Saved model evidence and optional
[scientific attribution](attribution.md) retain the native contracts. The
[migration contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/complex_based_workflow.md)
documents the breaking transition and guards.
