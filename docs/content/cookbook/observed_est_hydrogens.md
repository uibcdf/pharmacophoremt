# Include directional donors in the observed EST workflow

This source-checkout recipe continues the [chemical-template stage](observed_est_template.md).
Use compatible MolSysMT development APIs in the scientific environment. The
selected EST state is already declared; hydrogen placement does not choose pH,
a protomer or a tautomer. All molecular operations use public MolSysMT tools.

Request `mode='fixed_chemical_state'`, `pH=None` and `engine='RDKit'` explicitly.
The provider uses [RDKit AddHs with generated coordinates](https://www.rdkit.org/docs/source/rdkit.Chem.rdmolops.html#rdkit.Chem.rdmolops.AddHs).
The source has 20 observed heavy atoms; its 24 stored H counts become actual H
atoms on a new native copy. The observed pose remains unchanged. Generated H
positions are local geometry, without energy or receptor refinement.

```python
import ackredit
import molsysmt as msm
import numpy as np
import pharmacophoremt as phmt
from devtools.prepare_eralpha_ligand import prepare_case, credit_inputs
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import get_features, from_ligand
from pharmacophoremt.screening import PoseEvaluator

features = ['hb donor', 'hb acceptor', 'aromatic ring']
with ackredit.session('observed EST preparation and self-placement'), phmt.attribution():
    heavy_case = prepare_case()
    hydrogenation = msm.build.add_missing_hydrogens(
        heavy_case['molecular_system'], mode='fixed_chemical_state',
        pH=None, engine='RDKit', chemical_state='reference', structure_indices=[0],
        return_report=True, attribute_policy='intersection',
    )
    prepared = hydrogenation['molecular_system']
    inventory = get_features(prepared, features=features)
    credit_inputs()
    query = from_ligand(prepared, features=features, radius='.02 nm')
    evaluator = PoseEvaluator(query, direction_tolerance='10 degrees', min_fit_value=1)
    positive = evaluator.evaluate(prepared)
    preparation_references = ackredit.get_attribution().to_dict()

assert hydrogenation['report']['n_added_hydrogens'] == 24
assert hydrogenation['report']['dropped_attributes'] == ['b_factor']
assert len(inventory['features']) == query.n_interaction_sites == 5
assert positive['status'] == 'matched' and positive['fit_value'] == 1
np.testing.assert_array_equal(
    puw.get_value(msm.get(prepared, coordinates=True), to_unit='nm')[:, :20],
    puw.get_value(msm.get(heavy_case['molecular_system'], coordinates=True), to_unit='nm'),
)
```

The full classical inventory contains 9 atomic hydrophobic participants, 2 donors,
2 acceptors and 1 aromatic ring. The selected five essential sites omit atomic
hydrophobicity deliberately. Donor pairs are O3/H22 and O17/H40 in the local
expanded atom domain; the H indices refer to generated atoms, not deposited
source indices. The original 20 atoms retain their identity and map to the complex.

The explicit intersection policy drops the expanded copy's B-factor domain,
because generated H have no experimental B factors. MolSysMT emits a diagnostic
and names this in its report. The original ligand and retained deposition keep
their annotations; `attribute_policy='strict'` rejects this input instead.
No values for the new atoms are fabricated. The builder also checks the selected
chemical state, coordinate stereo and hydrogen inventory before adding atoms.

Check direction and pose independently. These are geometric negatives for a
fully essential query, not biological activity labels. Evaluating the heavy-only
input with this query exposes absent directional geometry.

```python
from copy import deepcopy

with ackredit.session('observed EST placed negatives'), phmt.attribution():
    heavy_only = evaluator.evaluate(heavy_case['molecular_system'])
    opposite = deepcopy(query)
    donor = next(site for site in opposite.interaction_sites if site.features == ['hb donor'])
    donor.shape.direction = -donor.shape.direction
    wrong_direction = PoseEvaluator(
        opposite, direction_tolerance='10 degrees', min_fit_value=1,
    ).evaluate(prepared)
    displaced = msm.structure.translate(
        prepared, translation=puw.quantity([[[2., 0., 0.]]], 'nm'), in_place=False,
    )
    wrong_position = evaluator.evaluate(displaced)

assert heavy_only['status'] == 'not_matched' and heavy_only['fit_value'] == .6
assert wrong_direction['status'] == 'not_matched' and wrong_direction['fit_value'] == .8
assert wrong_position['status'] == 'not_matched' and wrong_position['fit_value'] == 0
```

Save the native molecular values and query through their public codecs. Retain
template/H preparation reports and their original citations separately. H5MSM
does not automatically embed a preparation-history report.

```python
import json
import tempfile
from pathlib import Path
from pharmacophoremt.io import to_json, load_json
from devtools.validate_eralpha_template import portable

with tempfile.TemporaryDirectory() as directory:
    directory = Path(directory)
    msm.convert(prepared, to_form='file:h5msm', output_filename=str(directory / 'est.h5msm'))
    to_json(query, str(directory / 'query.json'))
    history = portable({
        'template_preparation': heavy_case['report'],
        'hydrogen_addition': hydrogenation['report'],
        'attribution': preparation_references,
    })
    (directory / 'preparation.json').write_text(json.dumps(history))
    loaded = msm.convert(directory / 'est.h5msm', to_form='molsysmt.MolSys')
    loaded_query = load_json(str(directory / 'query.json'))
    assert PoseEvaluator(loaded_query).evaluate(loaded)['status'] == 'matched'
    assert json.loads((directory / 'preparation.json').read_text()) == history
```

Reuse the independent seed and refinement tools for a rigidly moved copy of the
same conformation. Both angular policies remain available. This is rigid-motion
recovery, not conformer generation or a comparison of environmental OH orientations.

```python
from devtools.prepared_ccd_ligands import motion_frames
from pharmacophoremt.screening import (
    get_rigid_feature_correspondences, refine_rigid_feature_correspondences,
)

with ackredit.session('observed EST rigid recovery'), phmt.attribution():
    frames = motion_frames(prepared)
    reference = get_features(frames, structure_index=0, features=features)
    moving = get_features(frames, structure_index=1, features=features)
    credit_inputs()
    seeds = get_rigid_feature_correspondences(
        reference, moving, correspondence_strategy='ranked_triplet_seeds',
        n_seeds=1, distance_tolerance='.02 nm',
    )
    assert seeds['correspondences'] == [[[0, 0], [1, 1], [4, 4]]]
    for policy in ('final', 'each_step'):
        refined = refine_rigid_feature_correspondences(
            frames, reference, seeds['correspondences'], features=features,
            feature_inventory=moving, structure_index=1, orientation_policy=policy,
            min_matches=5, distance_tolerance='.02 nm', direction_tolerance='20 degrees',
        )
        assert len(refined['placements']) == 1 and refined['report']['n_fits'] == 3
        assert len(refined['placements'][0]['matches']['matches']) == 5
    search_references = ackredit.get_attribution().to_dict()
```

Each bounded session records only its executed stages. Preparation's bibliography
includes the actual RDKit/CIP work; the search bibliography includes adapted G3PS
ranking/refinement. In an application, one enclosing session can capture both;
the retained validation driver does so.

```python
preparation_bib = ackredit.Attribution.from_dict(preparation_references).report(format='bibtex')
search_bib = ackredit.Attribution.from_dict(search_references).report(format='bibtex')
assert 'RDKit' in preparation_bib
assert '10.3390/molecules26237201' in search_bib
```

Reproduce complete preparation, donor/normal/position controls, persistence and
both rigid policies with
`python -m devtools.validate_eralpha_hydrogens --output /tmp/observed-est-h.json`.
The report retains full science, explicit units, atom maps, source/producer hashes
and real citations, with identical science across host tracking profiles. It takes
no timing or memory measurements. Five assigned CIP centers and the observed
heavy-atom pose are preserved; receptor preparation, environment refinement,
conformer-energy and biological acceptance remain separate steps. The historical
OpenMM fixture is not repaired or newly attributed by this route.

Continue with the [receptor coverage recipe](observed_receptor_coverage.md) to
inspect the separate molecular gate before attempting a complex-based hypothesis.
