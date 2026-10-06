# Validate a labeled set and inspect failures

Use `RetrospectiveValidator` with an explicit native evaluator to rank labeled
inputs and report coverage metrics, accepted hits and failed calculations.
Choose `PoseEvaluator` for existing placements, `RigidPoseSearch` for one prepared
frame, or `ConformerScreening` for each molecule's requested prepared frames.

## Executable example

The reference propane matches; its displaced copy is a valid negative for a
placed-pose evaluator. A molecule without coordinates illustrates a calculation
failure. This analytical fixture verifies accounting, not biological enrichment.

```python
import molsysmt as msm
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_ligand
from pharmacophoremt.screening import PoseEvaluator
from pharmacophoremt.validation import RetrospectiveValidator

source = msm.convert(
    msm.convert('smiles:CCC', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity(
    [[[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]]], 'nm'))
query = from_ligand(source, features=['hydrophobicity'], radius='0.10 nm')
displaced = msm.structure.translate(
    source, translation=puw.quantity([[[2, 0, 0]]], 'nm'), in_place=False,
)
missing_coordinates = msm.convert(
    msm.convert('smiles:CCC', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)

validator = RetrospectiveValidator(query, evaluator=PoseEvaluator(query))
report = validator.run(
    (item for item in [source]),
    (item for item in [displaced, missing_coordinates]),
    on_error='record',
)
assert report['n_actives'] == 1 and report['n_decoys'] == 2
assert report['n_evaluated'] == 2 and report['n_failed'] == 1
assert report['n_actives_found'] == 1
assert report['evaluated_indices'].tolist() == [0, 1]
assert report['scores'].tolist() == [1, 0]
assert report['AUC'] == report['BEDROC'] == 1
assert report['failures'][0]['input_index'] == 2
assert report['failures'][0]['fit_value'] is None
```

## Understand the report

| Field | Meaning |
| --- | --- |
| `n_actives`, `n_decoys` | Original input counts |
| `n_evaluated`, `n_failed` | Resolved inputs and excluded calculation failures |
| `n_actives_evaluated`, `n_decoys_evaluated` | Class counts actually entering metrics |
| `n_actives_found` | Evaluated actives accepted by the chosen native tool |
| `scores`, `labels`, `evaluated_indices` | Coverage scores, labels and original input positions used in metrics |
| `evaluations`, `failures` | Per-input evidence and failed entries |
| `AUC`, `BEDROC`, `EF@1%`, `EF@5%`, `EF@10%` | Coverage-ranking metrics with tie handling |

Coverage ranks the inputs; a high score alone does not establish an accepted hit
or predicted affinity. Ties share ranking credit instead of receiving credit
from favorable input order. Use `ef_fractions` and `bedroc_alpha` to configure
the metric parameters explicitly.

Default failures raise. Explicit recording excludes failures from metric inputs
and preserves their identity and diagnostic evidence. The resulting metrics
describe the evaluated subset, so inspect failures and class counts alongside
the scores. A batch with no successfully evaluated inputs raises. AUC and BEDROC
are NaN when only one class remains in the evaluated subset.

## Use prepared-conformer screening

Pass `evaluator=ConformerScreening(query)` for the
[prepared-conformer workflow](prepared_conformers.md), with its three-essential-
non-collinear-center query requirement. Supply `structure_indices` and
`chemical_state` to `validator.run()`; they are forwarded to the native tool.
For placed evaluation or single-frame rigid search, use `structure_index` instead.

The conformer route contributes one resolved score per molecule, rather than
one metric input per frame. An unresolved ensemble appears in `failures` with
its per-frame evidence. A proven unit-fit hit can remain evaluated despite
other failed frames; inspect `entry['ensemble']['n_failed']` and
`entry['conformers']` in `evaluations`. Failed-molecule and failed-frame counts
therefore need not coincide. Labels, curation and benchmark preparation remain
your scientific choices; these recipes do not establish biological validation.
