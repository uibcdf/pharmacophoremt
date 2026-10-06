# Prepare an observed EST ligand with an explicit template

Run from the source checkout in the compatible development environment. This
recipe consumes MolSysMT's development template tools; published availability
is a separate gate. The observed input is the retained RCSB 1QKU asymmetric unit,
label chain D, author chain A, residue 600. Its 20 deposited heavy-atom coordinates
remain unchanged throughout chemical preparation.

The fixture client checks both the acquired source and a frozen MolSysMT-curated
template. The template has no coordinates. It declares chemical assignments,
an exhaustive atom map and 24 stored hydrogen counts. No H positions are generated.
Its manifest explicitly chooses canonical-descriptor stereochemistry and retains
the discrepant CCD atom flag at C8.

```python
import ackredit
import pharmacophoremt as phmt
from devtools.prepare_eralpha_ligand import prepare_case, credit_inputs

with ackredit.session('observed EST preparation'), phmt.attribution():
    case = prepare_case()
    credit_inputs()
    preparation_references = ackredit.get_attribution().to_dict()

audit = case['report']
assert audit['assessment']['status'] == 'compatible'
assert audit['application']['status'] == 'applied'
assert audit['pose_preserved'] and audit['source_unchanged']
assert audit['feature_counts'] == {
    'hydrophobicity': 9, 'hb acceptor': 2, 'aromatic ring': 1,
}
assert audit['readiness']['hydrogen_placement'] == 'not_performed'
```

Stored hydrogen counts describe the chosen chemical state; they do not provide
donor-H geometry. Recognition returns no explicit donor-H pairs. Therefore this
example deliberately selects only acceptors and the aromatic ring. This subset
is a geometric hypothesis, not a complete donor-inclusive pharmacophore or a
receptor-interaction model.

```python
from pharmacophoremt.modeler import from_ligand
from pharmacophoremt.screening import PoseEvaluator

with ackredit.session('observed EST placed evaluation'), phmt.attribution():
    case = prepare_case()
    credit_inputs()
    query = from_ligand(
        case['molecular_system'], features=['hb acceptor', 'aromatic ring'],
        radius='.02 nm',
    )
    evaluator = PoseEvaluator(query, direction_tolerance='10 degrees', min_fit_value=1)
    positive = evaluator.evaluate(case['molecular_system'])
    references = ackredit.get_attribution().to_dict()

assert query.n_interaction_sites == 3
assert positive['status'] == 'matched' and positive['fit_value'] == 1
```

Use MolSysMT for the displaced molecular copy. A 2 nm shift rejects essential
sites in this fixed-frame evaluation. Rigid search could align that copy back;
this control tests placement, not free screening.

```python
import molsysmt as msm
from pharmacophoremt import pyunitwizard as puw

displaced = msm.structure.translate(
    case['molecular_system'],
    translation=puw.quantity([[[2., 0., 0.]]], 'nm'), in_place=False,
)
negative = evaluator.evaluate(displaced)
assert negative['status'] == 'not_matched' and negative['fit_value'] == 0
bibliography = ackredit.Attribution.from_dict(references).report(format='bibtex')
assert '1QKU' in bibliography
assert any(item['type'] == 'dataset' for item in references['items'])
```

Reproduce all controls with
`python -m devtools.validate_eralpha_template --output /tmp/observed-est.json`.
The driver also checks aromatic normal-sign symmetry, rejection of an orthogonal
query normal, native molecular/query persistence and identical science with host
tracking disabled/enabled. It retains actual whole-workflow citations and both
chemical-state payloads across H5MSM's two component-text dtype normalizations.
Preparation provenance is stored separately from molecular H5MSM values.

The [input-audit notebook](eralpha_input_audit.ipynb) retains the original
unprepared-input evidence. This recipe advances the separately sourced observed
ligand; it does not establish the old OpenMM snapshot's derivation. The
[fixed-state H continuation](observed_est_hydrogens.md) now supplies donor geometry
through MolSysMT. This heavy-only recipe still generates no H coordinates.
Receptor readiness, environment refinement and biological validation remain pending.
Site radii/angles are declared test parameters, not validated
binding cutoffs. No timing or memory benchmark is claimed.
