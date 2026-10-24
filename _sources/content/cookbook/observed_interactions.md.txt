# Build from observed ligand–receptor interactions

Use `modeler.from_interactions()` to build a query from native MolSysMT
interaction observations in an evaluated source frame. This route selects
observed participants rather than every feature present in a reference ligand.
The current extraction supports hydrophobic contacts, hydrogen bonds and
[ionic contacts](ionic_interactions.md) and
[pi-pi/cation-pi contacts](aromatic_interactions.md).

## Executable example

Two propane fragments provide an analytical ligand–partner contact. Replace
the fixture and selections with your prepared complex in a real workflow.

```python
import molsysmt as msm
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_interactions
from pharmacophoremt.screening import PoseEvaluator

source = msm.convert(
    msm.convert('smiles:CCC.CCC', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity([
    [[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0],
     [0, 0.3, 0], [0.15, 0.3, 0], [0.30, 0.3, 0]],
], 'nm'))

observations = msm.interactions.hydrophobic.get_hydrophobic_interactions(
    source, selection=[0, 1, 2], selection_2=[3, 4, 5],
    selection_mode='between', structure_indices=[0], pbc=False,
)
query = from_interactions(
    source, observations, ligand_selection=[0, 1, 2], structure_index=0,
)
result = PoseEvaluator(query).evaluate(
    source, selection=[0, 1, 2], structure_index=0, pose_id='ligand',
)
assert query.n_interaction_sites == 1
assert result['status'] == 'matched' and result['fit_value'] == 1
assert result['assignments'][0]['atom_indices'] == [1]
```

## Source and observation requirements

Pass the same unchanged source and local atom index space used to calculate the
observations. Matching axis lengths cannot establish that two inputs came from
the same molecular source. The requested frame must have been evaluated in the
interaction result; an unevaluated frame is not an empty negative.

Repeated observations of a participant contribute to one site. Sites retain
their source participants, observations, measurements and evidence. Ligand
donors retain the indexed donor-H direction; acceptors receive no invented
lone-pair direction. Unsupported interaction kinds, split donor-H selections
and nonzero periodic image vectors raise. An evaluated frame with no contacts
produces an empty query, which is not a valid evaluation model.

The observation provider's chemical definitions and the evaluator's recognition
profile can differ. Evaluation uses MolSysMT's SMARTS donor/acceptor and
hydrophobic definitions; an upstream elemental hydrogen-bond definition can
recognize other participants. Observing a contact does not guarantee a later
match under a different declared definition.

The example checks an existing placement. For pose search, use the
[prepared-conformer tools](prepared_conformers.md) with a suitable query; the
rigid triplet method requires at least three essential non-collinear centers.
The one-site fixture here belongs with `PoseEvaluator`.
