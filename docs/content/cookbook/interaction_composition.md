# Compose independently observed interaction families

`from_interaction_collection()` builds a joint hypothesis from named cached
MolSysMT analyses. It calls `from_interactions()` for each and then the public
`compose_pharmacophores()` tool. Molecular recognition, geometry, selection and
detection remain in MolSysMT. No interaction detector runs during conversion.

## Detect explicitly and build the joint query

This fixture deliberately groups disconnected prepared controls into a declared
ligand selection. It is an executable adapter example, not a chemical ligand or
biological binding complex. The indexed isotope keeps an explicit donor hydrogen.

```python
import molsysmt as msm
import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_interaction_collection
from pharmacophoremt.screening import PoseEvaluator

theta = np.arange(6) * np.pi / 3
ring = np.column_stack((.14 * np.cos(theta), .14 * np.sin(theta), np.zeros(6)))
xyz = np.vstack((
    ring, [0, 0, .7], [1.1, 0, 0], [1, 0, 0], [3, 0, 0],
    ring + [0, 0, .35], [.25, 0, .7], [1.3, .1, 0], [1.3, 0, 0], [3.3, 0, 0],
))
source = msm.convert(
    msm.convert('smiles:c1ccccc1.[Na+].[2H]O.C.c1ccccc1.[Cl-].C=O.C', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity([xyz], 'nm'))
ligand, partner = list(range(10)), list(range(10, 20))
options = dict(selection=ligand, selection_2=partner,
               selection_mode='between', structure_indices=[0], pbc=False)

def detect():
    return dict(
        hydrophobic=msm.interactions.hydrophobic.get_hydrophobic_interactions(
            source, distance_threshold='.4 nm', **options),
        hbonds=msm.interactions.hbonds.get_hbonds(
            source, method='donor_acceptor_distance_angle', profile='smarts_donor_acceptor', **options),
        ionic=msm.interactions.ionic.get_ionic_interactions(source, '.3 nm', **options),
        pi_prolif=msm.interactions.pi_pi.get_pi_pi_interactions(
            source, method='plane_angle_intersection', profile='smarts_5_6', **options),
        cation_pi=msm.interactions.cation_pi.get_cation_pi_interactions(
            source, method='centroid_distance_angle', profile='smarts_5_6', **options),
        pi_molstar=msm.interactions.pi_pi.get_pi_pi_interactions(
            source, method='centroid_angle_offset', profile='three_atom_plane', **options),
        ionic_empty=msm.interactions.ionic.get_ionic_interactions(source, '.01 nm', **options),
    )

analyses = detect()
query = from_interaction_collection(source, analyses, ligand, radius='.02 nm')
assert query.n_interaction_sites == 9
assert sum(site.weight for site in query.interaction_sites) == 9
assert sum(row['action'] == 'reused' for row in query.metadata['site_map']) == 2
charge = next(site for site in query.interaction_sites if site.feature_name == 'positive charge')
assert {row['component'] for row in charge.metadata['observations']} == {'ionic', 'cation_pi'}
empty = next(row for row in query.metadata['components'] if row['label'] == 'ionic_empty')
assert empty['n_sites'] == 0 and empty['metadata']['evaluated_structure_indices'] == [0]

evaluator = PoseEvaluator(query)
assert evaluator.evaluate(source, selection=ligand)['status'] == 'matched'
moved = msm.structure.translate(source, selection=ligand, translation='[1,0,0] nm', in_place=False)
assert evaluator.evaluate(moved, selection=ligand)['fit_value'] == 0
reversed_h = msm.structure.translate(source, selection=[7], translation='[-.2,0,0] nm', in_place=False)
result = evaluator.evaluate(reversed_h, selection=ligand)
assert result['status'] == 'not_matched' and np.isclose(result['fit_value'], 8 / 9)
```

The charge center supported by ionic and cation-pi analyses contributes one unit
of fit weight. The ring supported by two pi-pi profiles also remains one site.
The independent contacts remain labeled observations; relation and occurrence
indices belong to their original analyses. Names, producer versions, criteria,
original bibliographies and empty evaluated scopes remain component metadata.

The high-level dispatcher also accepts
`phmt.model(source, method='interaction-collection', interaction_collection=analyses, ligand_selection=ligand)`.
All analyses must use the same unchanged source axes, selected frame and declared
state. Atomic H-bond/hydrophobic conversion currently requires the source reference
state. Uncovered frames or a failed child conversion raise; no partial query or
zero fit is returned. Source declarations do not authenticate molecular origin.

## Compose cached hypotheses independently

`compose_pharmacophores()` needs only models in a declared common coordinate
frame. It does not access a molecular system or perform alignment. Its default
`duplicate_policy='keep'` preserves independently chosen constraints. For native
observed queries, explicitly choosing `same_participant` requires matching source
axes, ligand, frame and state. Compatible participant constraints are reused;
different radii, geometry, weights or essential flags raise.

```python
from pharmacophoremt.modeler import compose_pharmacophores, from_interactions

pieces = {label: from_interactions(source, observed, ligand, radius='.02 nm')
          for label, observed in analyses.items()}
modular = compose_pharmacophores(pieces, duplicate_policy='same_participant')
assert modular.n_interaction_sites == 9
assert PoseEvaluator(modular).evaluate(source, selection=ligand)['fit_value'] == 1
kept = compose_pharmacophores(pieces)
assert kept.n_interaction_sites == 11
kept_result = PoseEvaluator(kept).evaluate(source, selection=ligand)
assert kept_result['status'] == 'not_matched'
assert np.isclose(kept_result['fit_value'], 9 / 11)
assert len(kept_result['missing_essential_sites']) == 2

# Different hypotheses for a participant need an explicit choice.
wide_charge = from_interactions(source, analyses['ionic'], ligand, radius='.4 nm')
try:
    compose_pharmacophores({'narrow': pieces['ionic'], 'wide': wide_charge},
                          duplicate_policy='same_participant')
except ValueError as error:
    assert 'conflicting constraints' in str(error)
else:
    raise AssertionError('Expected an explicit constraint conflict')
```

The `keep` outcome is an expected consequence of essential one-to-one matching:
one chemical participant cannot satisfy two separate required constraints of
the same feature. This is not a performance ranking between the policies. Use
`keep` for intentional independent constraints; use participant reuse for repeated
evidence about one compatible constraint. Reuse does not average centers or add
weights. Its 1e-12 nm/dimensionless tolerance handles representation equality,
not spatial clustering. Disk normal sign is irrelevant; donor direction is not.
Distinct atoms with coincident centers are kept distinct.

Every output site and provenance snapshot is independent of the inputs. Generic
composition can also combine a positive query with an independently constructed
[exclusion model](excluded_volumes.md). Input scores remain component provenance;
the tool does not invent a score for the combined hypothesis.

## Capture actual work and persist the query

Detect inside an application-owned Ackredit capture to retain the actual method
and software references. Composing cached models preserves their original
bibliography without crediting another detection, recognition or fitting run.
Composition adds no invented literature citation; the evaluator records its
assignment method when reached. Ackredit is optional for scientific work.

```python
import tempfile
from pathlib import Path
import ackredit as ack
import pharmacophoremt as phmt
from pharmacophoremt.io import load_json, to_json

with ack.session('joint workflow'):
    with ack.capture('detect, compose and evaluate') as run:
        with phmt.attribution():
            fresh = detect()
            credited = from_interaction_collection(source, fresh, ligand, radius='.02 nm')
            assert PoseEvaluator(credited).evaluate(source, selection=ligand)['status'] == 'matched'
    references = run.attribution.to_dict()
    assert any('get_pi_pi_interactions' in use['used_by'] for use in references['uses'])
    assert any(item.get('doi') == '10.1186/s13321-021-00548-6' for item in references['items'])
    assert ack.Attribution.from_dict(references).report(format='bibtex')
    before = ack.get_attribution().to_dict()
    with puw.context(standard_units=['pm', 'fs', 'degrees']):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'joint_query.json'
            to_json(credited, path)
            restored = load_json(path)
            assert restored.metadata == credited.metadata
            assert [site.metadata for site in restored.interaction_sites] == [site.metadata for site in credited.interaction_sites]
            assert PoseEvaluator(restored).evaluate(source, selection=ligand)['fit_value'] == 1
    assert ack.get_attribution().to_dict() == before
```

For standalone composition of stored components, load each with `load_json()`
and pass the named mapping to `compose_pharmacophores()`. Original component
attribution remains evidence; reading stored models adds no scientific credit.
An all-empty composition stays empty and is rejected as an evaluation query.

From a compatible source checkout, run
`python -m devtools.validate_interaction_composition --output composition_validation.json`
for actual five-family detection, both composition policies, independent
displacement/donor/exclusion controls, persistence, source fingerprints and
tracking on/off. These disconnected analytical controls do not qualify a
biological complex, receptor preparation or runtime/memory benchmark.
