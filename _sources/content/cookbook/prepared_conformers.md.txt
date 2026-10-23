# Search rigid poses and prepared conformations

Use `RigidPoseSearch` to align and evaluate one prepared frame. Use
`ConformerScreening` to apply that search to requested prepared frames of each
molecule and retain its best checked pose. Both compose chemical recognition,
pharmacophoric correspondence proposals, MolSysMT fitting and pose evaluation.

The current `rigid_triplet_fit@1` method requires at least three essential sites
with non-collinear centers. It enumerates chemically compatible triplet fits
within a finite budget; it does not exhaust continuous pose space. Prepared
conformations and declared chemical states are inputs. Their generation and
molecular preparation belong to MolSysMT-supported workflows.

## Executable example

Three charged fragments provide distinct, non-collinear anchors. The second
frame is displaced through MolSysMT so that the search must recover a placement.
This fixture is an API control, not an optimized ligand or biological benchmark.

Run the blocks on this page in order.

```python
import json
import molsysmt as msm
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_ligand
from pharmacophoremt.screening import ConformerScreening, RigidPoseSearch

source = msm.convert(
    msm.convert('smiles:[Na+].[K+].[Li+]', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity(
    [[[0, 0, 0], [1, 0, 0], [0, 1, 0]]], 'nm'))
query = from_ligand(source, features=['positive charge'], radius='0.02 nm')
source.structures.append(coordinates=msm.get(source, coordinates=True))
prepared = msm.structure.translate(
    source, structure_indices=[1],
    translation=puw.quantity([[[2, 1, 3]]], 'nm'), in_place=False,
)

rigid = RigidPoseSearch(query, max_trials=10000)
pose = rigid.evaluate(prepared, structure_index=1, chemical_state='structure')
assert pose['status'] == 'matched' and pose['fit_value'] == 1
assert pose['alignment'] is not None

screen = ConformerScreening(query, max_trials=10000)
result = screen.evaluate(
    prepared, structure_indices=[1, 0], chemical_state='structure', pose_id='ligand',
)
assert result['status'] == 'matched' and result['fit_value'] == 1
assert result['best_conformer_index'] == 1
assert result['ensemble']['n_evaluated'] == 2
assert result['ensemble']['complete']
assert result['resolved_chemical_state_index'] == 0
assert [entry['conformer_index'] for entry in result['conformers']] == [1, 0]
json.dumps(result, allow_nan=False)
```

Hits rank before negatives, then weighted coverage ranks within each status.
Exact ties retain the first requested frame: both frames achieve unit coverage
above, so `[1, 0]` chooses frame 1. RMSD does not break coverage ties.

## Request a ranked hit list explicitly

`VirtualScreening` wraps these same prepared-native tools. Choose the method
explicitly: `placed`, `rigid` or `conformers`. There is no hidden preparation.
The prepared inputs and query from the preceding block can be reused:

```python
from pharmacophoremt.screening import VirtualScreening

library = [prepared, prepared]
facade = VirtualScreening(query, screening_method='conformers', max_trials=10000)
hits = facade.run(library, structure_indices=[1, 0], chemical_state='structure')
assert [hit['input_index'] for hit in hits] == [0, 1]
assert [hit['conf_id'] for hit in hits] == [1, 1]
assert all(hit['fit_value'] == 1 for hit in hits)
assert hits[0]['mol'] is prepared
assert len(facade.evaluations) == 2
assert list(facade.to_dataframe().columns) == [
    'rank', 'input_index', 'fit_value', 'conf_id', 'status',
]
json.dumps(facade.evaluations, allow_nan=False)
```

Native assignment uses each participant at most once and requires every
essential site. Historical `min_match_ratio=1.0` and `n_conformers=50` defaults
are inert; other values are refused. Use native `min_fit_value` for weighted
coverage thresholds. Point/angle tolerances have explicit units. Exact hit ties
retain input order. Coverage is not affinity or equivalence to the retired fit
engine.

Failures raise by default; `on_error='record'` retains unscored failures in
`evaluations`. A resolved maximal conformer hit may also contain failed frames;
inspect its complete native evidence. CSV/DataFrame exports scalar hit records
without molecular conversion. `to_sdf()` is retired pending MolSysMT's molecular
collection/property contract (#215/#223), and conformer generation belongs to
MolSysMT #219. See [the full transition contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/virtual_screening_workflow.md).

## Inspect the best pose and every frame

The best pose fields appear at the top level. `assignments` records matched
sites and atom participants; `alignment` records the fit correspondence, RMSD,
provider and fitted coordinates. When the original placement wins,
`alignment=None`, and `pose_coordinates` still retains that pose.

Coordinates are sealed PyUnitWizard QuantityRecords in the order given by
`selected_atom_indices`, with shape `(1, n_selected_atoms, 3)`:

```python
coordinates = puw.QuantityRecord.from_dict(result['pose_coordinates']).to_quantity(
    unit='nm', dimensionality={'[L]': 1},
)
assert puw.get_value(coordinates).shape == (1, 3, 3)
assert result['alignment']['correspondence']
assert all(entry['pose_id'] == 'ligand' for entry in result['conformers'])
```

`conformers` retains per-frame results, recognition, assignments, search evidence
and failures in requested order. Each `conformer_index` is the source
`structure_index`, not a new index after filtering. `ensemble` reports requested,
evaluated and failed counts, completeness and whether the molecule score is
resolved. Molecular source systems remain unchanged.

## Choose frames and chemical states

`structure_indices='all'` searches every prepared frame. An explicit sequence
must contain unique nonnegative source indices; MolSysMT validates bounds.
`selection` chooses source atoms independently in each requested frame.
Different atom inventories should be separate molecular systems.

| `chemical_state` | Meaning |
| --- | --- |
| `'reference'` (default) | Use MolSysMT's declared reference state in every frame |
| Integer | Use that explicitly declared state in every frame |
| `'structure'` | Resolve each frame's associated state independently |

State-dependent selections use the same state as recognition. Missing
associations and invalid state indices are calculation failures. No alternative
chemical states are inferred or enumerated.

## Screen a database and retain failures

Each input is one molecule with its prepared frames. Input position identifies
the molecule; frame indices are local to it. Generators and repeated objects
retain separate identities.

```python
records = screen.run((item for item in [prepared, prepared]), on_error='record')
assert [entry['input_index'] for entry in records] == [0, 1]
assert [entry['pose_id'] for entry in records] == [0, 1]
assert all(entry['status'] == 'matched' for entry in records)
```

Default errors raise immediately. With `on_error='record'`, remaining frames are
attempted and each failed frame retains its diagnostic code, cause and stage.
`max_trials` is a triplet-product budget **per frame**, including pruned products.
A truncated search fails unless a valid unit-fit hit proves maximal coverage.

If any frame fails without that proven maximum, the molecule has
`status='failed'`, `fit_value=None` and `best_conformer_index=None`. Its
`best_observed` retains the best successful partial pose, or `None` if all frames
failed. It must not be ranked as a definitive score or counted as a negative.

A valid unit-fit hit resolves the score even if another frame fails. Those
failures remain visible and `ensemble.complete=False`. Unit coverage on a pose
rejected by exclusions or essential criteria does not prove this maximum.
All requested frames succeeding without a hit give a complete negative for
this discrete method. [Retrospective validation](retrospective_validation.md)
uses resolved molecule scores and retains the frame-level evidence.
