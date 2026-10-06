# Build consensus from prepared rigid unaligned ligands

Use `modeler.from_rigid_ligands()` when your prepared ligand frames are not yet
superposed. Choose a pivot and a feature-correspondence proposal strategy. PHMT
proposes correspondences, MolSysMT fits and transforms molecular coordinates,
and PHMT verifies positions/orientations before discovering aligned consensus.

The current method takes one prepared frame per ligand. It does not prepare
chemistry or generate conformers, and its explicit finite search family does not
prove a globally optimal continuous or flexible alignment.

## Execute both strategies

This small disconnected-fragment fixture has noncoplanar feature centers and an
explicit donor hydrogen. Its coordinates are analytical controls, not an optimized
ligand or biological benchmark. All molecular construction and motion below go
through MolSysMT. Replace these systems with your prepared inputs in actual work.

Run the blocks on this page in order.

```python
import json
import molsysmt as msm
import numpy as np
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_rigid_ligands, get_features
from pharmacophoremt.screening import get_rigid_feature_correspondences

coordinates = np.array([
    [0, 0, 0], [.15, 0, 0], [.3, 0, 0],
    [.1, .5, 0], [0, .5, 0], [.3, .6, 0], [.3, .5, 0], [.05, .2, .7],
])
source = msm.convert(
    msm.convert('smiles:CCC.[2H]O.C=O.[NH4+]', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity([coordinates], 'nm'))
rotated = msm.structure.rotate(
    source, rotation=np.array([[0., -1, 0], [1, 0, 0], [0, 0, 1]]),
    rotation_center=puw.quantity([0, 0, 0], 'nm'), in_place=False,
)
displaced = msm.structure.translate(
    rotated, translation=puw.quantity([[[2., 1, 3]]], 'nm'), in_place=False,
)
ligands = [
    {'ligand_id': 'a', 'molecular_system': source},
    {'ligand_id': 'b', 'molecular_system': displaced},
]
families = ['hydrophobicity', 'hb donor', 'hb acceptor', 'positive charge']
results = {}
with phmt.attribution():
    for strategy in ('association_cliques', 'triplet_seeds'):
        result = from_rigid_ligands(
            ligands, correspondence_strategy=strategy, features=families,
            min_matches=5, min_support=2, min_sites=5,
            distance_tolerance='0.02 nm', direction_tolerance='5 degrees',
            radius='0.02 nm', max_fits=1000, max_layouts=1000,
        )
        assert result['complete'] and result['models']
        assert all(model.n_interaction_sites == 5 for model in result['models'])
        assert all(model.metadata['hypothesis']['joint_ligand_ids'] == ['a', 'b']
                   for model in result['models'])
        json.dumps(result['report'], allow_nan=False)
        results[strategy] = result
```

`association_cliques` fits inclusion-maximal injective feature mappings whose
internal distances are compatible. `triplet_seeds` fits every eligible typed
non-collinear triplet, then tests full-inventory matching. Different anchor sets
can give different placements. A maximal clique that fails after fitting does
not cause the method to enumerate all its smaller submappings.

The pair-distance filter permits differences up to twice the positional tolerance.
It is a necessary condition; it cannot certify absolute geometry or rule out
reflections. Each proposal's original pairs must satisfy positions and orientations
after fitting, and at least min_matches injective pivot pairs must match. RMSD alone
does not decide acceptance.

## Reuse proposals and inspect evidence

```python
first, second = [get_features(item['molecular_system'], features=families)
                 for item in ligands]
proposals = get_rigid_feature_correspondences(
    first, second, distance_tolerance='0.02 nm', min_matches=5,
)
assert proposals['complete'] and proposals['correspondences']

result = results['association_cliques']
report = result['report']
assert report['criteria']['reference_ligand_id'] == 'a'
assert report['n_fits'] > 0 and report['n_layouts'] > 0
placed = report['source_alignments'][1]['accepted_placements'][0]
assert placed['alignment']['provider'] == 'molsysmt.structure.least_rmsd_fit'
fitted = puw.QuantityRecord.from_dict(
    placed['alignment']['aligned_atom_coordinates'],
).to_quantity(unit='nm', dimensionality={'[L]': 1})
np.testing.assert_allclose(puw.get_value(fitted, to_unit='nm')[0], coordinates, atol=1e-12)

if result['attribution']['status'] == 'captured':
    bibliography = phmt.attribution_report(result['attribution'], format='bibtex')
    assert '10.1107/S0567739476001873' in bibliography
    assert '10.1145/362342.362367' in bibliography
```

Proposal indices refer to the original inventories. The source report retains
every accepted and rejected fit with mapping, RMSD and absolute matching evidence.
Models retain their selected layout/placement, original source records, shared
ligand support, emitted shape radius and optional detached bibliography. Native
JSON saving/loading preserves this evidence, using the same functions as the
[aligned-clique recipe](aligned_cliques.md).

All accepted placements remain alternatives, including equivalent geometry from
different seeds. No unit-coverage early stop or hidden geometric deduplication is
applied. Compare proposal/fit/layout counts before drawing performance conclusions.

## Inputs, accounting and limits

The [modular recipe](modular_rigid_tools.md) exposes cached query construction,
supplied-mapping placement and saved-report summaries as independent public steps.

`reference_index` chooses the pivot record, default 0. It must have at least three
non-collinear feature centers. Each record can declare `selection`, `structure_index`
and `chemical_state`; defaults are `'all'`, 0 and `'reference'`. Original molecular
systems remain unchanged.

A ligand with no accepted direct pivot placement is `unplaced`. Its original
inventory remains in source evidence and it still counts in support fractions,
but contributes no sites to aligned layouts. This does not prove chemical absence
or incompatibility with every possible pivot. If no jointly supported hypothesis
meets your criteria, completed discovery returns `models=[]`.

The graph/clique/triplet, total-fit, layout-product, assignment-matrix and per-layout
consensus-extension limits are explicit. Exceeding a limit raises a diagnostic;
partial results are not presented as an empty scientific consensus. Provider
failures propagate too. The source repository's `devguide/rigid_consensus_workflow.md`
defines the exact budget semantics; [issue #26](https://github.com/uibcdf/pharmacophoremt/issues/26)
tracks this development workflow.

The primary-source comparison in `devguide/pharmacophore_search_strategies.md`
records RDP, frequent cliques, triangle indexing and Gaussian-overlap alternatives.
The [ranked-seed recipe](ranked_seeds.md) implements the first G3PS stage;
[public greedy refinement](rigid_refinement.md) offers both angular policies.
Translation rescue and exclusion corrections remain future stages.
Only implemented methods actually reached by a
calculation are included in its Ackredit bibliography.
