# Build from a reference ligand and evaluate a placed pose

Use `modeler.from_ligand()` to turn the chemical participants of one prepared
ligand frame into a query. Use `screening.PoseEvaluator` when the candidate is
already placed in the query's coordinate frame. For candidates that require
alignment, continue with [prepared-pose search](prepared_conformers.md).

## Inputs and chemical families

Supply a molecular system accepted by MolSysMT, with prepared coordinates and
declared chemistry. `selection` selects the ligand atoms, `structure_index`
selects one reference frame, and `chemical_state` chooses the reference state,
an explicit state index, or the frame-associated state with `'structure'`.
Selections depending on chemistry use that same state.

| Feature name | Default query geometry |
| --- | --- |
| `hydrophobicity` | Atomic sphere |
| `hb donor` | Donor-centered sphere and indexed donor-to-H vector |
| `hb acceptor` | Atomic sphere |
| `aromatic ring` | Disk at the fitted ring plane, with its normal |
| `positive charge`, `negative charge` | Sphere at the provider-defined charge-group center |

Recognition comes from MolSysMT. Donor directions require explicit indexed
hydrogens. Aromaticity, bond orders and formal charges must be declared;
the workflow does not infer protonation at a chosen pH. The delivered chemical
definition is `classical_atomic_formal@1`.

## Executable example

The propane fixture isolates a known hydrophobic participant. Replace the
fixture with your prepared ligand and its appropriate selection in real use.

```python
import molsysmt as msm
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_ligand, get_features
from pharmacophoremt.screening import PoseEvaluator

source = msm.convert(
    msm.convert('smiles:CCC', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity(
    [[[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]]], 'nm'))

inventory = get_features(source, features=['hydrophobicity'])
assert inventory['definition'] == 'classical_atomic_formal@1'
assert inventory['features']

query = from_ligand(source, features=['hydrophobicity'], radius='0.10 nm')
evaluator = PoseEvaluator(query)
positive = evaluator.evaluate(source, pose_id='reference')
assert positive['status'] == 'matched' and positive['fit_value'] == 1

displaced = msm.structure.translate(
    source, translation=puw.quantity([[[2, 0, 0]]], 'nm'), in_place=False,
)
negative = evaluator.evaluate(displaced, pose_id='displaced')
assert negative['status'] == 'not_matched' and negative['fit_value'] == 0
assert negative['missing_essential_sites']
```

`get_features()` is independently usable: its inventory retains source atom
indices, unit-bearing centers, directions/normals, charges and provider evidence.
`from_ligand()` builds editable sites from that inventory. All generated sites
initially have `essential=True` and `weight=1`; curate those choices according to
your scientific hypothesis before constructing the evaluator, which snapshots
the query. A reference feature is not automatically evidence of a binding role.

## Interpret the result

`assignments` links query site indices to recognized source atom participants.
`missing_essential_sites` and `excluded_volume_clashes` explain rejected poses.
`recognition`, `criteria`, `chemical_state` and `structure_index` retain the
definition, parameters and source context used in the calculation.

Every essential site must match, including zero-weight essential sites. Optional
sites contribute their weight. A participant fills at most one site. Donor
SphereAndVector sites check directed donor-H angles. Aromatic disks check center
distance and the unoriented normal angle: reversing a plane normal is equivalent.
This disk profile does not calculate disk thickness or point-in-disk intersection.
Spherical exclusions veto heavy atoms strictly inside the exclusion radius.

`PoseEvaluator` performs no alignment. A displaced copy is therefore a valid
negative in this example, even though a rigid-search tool could align it back
to the reference. Calculation failures raise a coded error; batch recording and
metric handling are explained in [retrospective validation](retrospective_validation.md).
