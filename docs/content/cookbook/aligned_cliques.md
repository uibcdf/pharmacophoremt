# Discover aligned consensus and alternative hypotheses

Use `modeler.from_aligned_ligand_cliques()` to discover supported sites anywhere
in your prepared aligned ligand set, including sites absent from the first ligand.
The result can contain several alternative Feature + Shape models.

This development recipe uses analytical coordinates and compatible source
providers, as in the other native recipes. Molecular preparation/alignment belongs
to MolSysMT. The examples illustrate matching and evidence, not biological activity.

## Build and evaluate a consensus

The first input below has no requested hydrophobic feature. The two propane
placements still supply a supported site; no ligand anchors discovery.

```python
import molsysmt as msm
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw

def prepared(smiles, coordinates):
    source = msm.convert(
        msm.convert('smiles:' + smiles, to_form='rdkit.Mol'),
        to_form='molsysmt.MolSys',
    )
    source.structures.append(coordinates=puw.quantity([coordinates], 'nm'))
    return source

first = prepared('CCC', [[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]])
second = msm.structure.translate(
    first, translation=puw.quantity([[[0.04, 0, 0]]], 'nm'), in_place=False,
)
negative = prepared('[Na+]', [[2, 0, 0]])
ligands = [
    {'ligand_id': 'empty', 'molecular_system': negative},
    {'ligand_id': 'a', 'molecular_system': first},
    {'ligand_id': 'b', 'molecular_system': second},
]

with phmt.attribution():
    result = phmt.modeler.from_aligned_ligand_cliques(
        ligands, features=['hydrophobicity'], min_support=2,
        distance_tolerance='0.10 nm', radius='0.06 nm',
    )

assert result['complete'] and len(result['models']) == 1
query = result['models'][0]
hypothesis = result['report']['hypotheses'][0]
assert hypothesis['joint_ligand_ids'] == ['a', 'b']
assert hypothesis['joint_support_fraction'] == 2 / 3
assert query.n_interaction_sites == 1
assert abs(float(puw.get_value(query.interaction_sites[0].center,
                               to_unit='nm')[0]) - 0.17) < 1e-12

evaluator = phmt.screening.PoseEvaluator(query)
assert evaluator.evaluate(first)['status'] == 'matched'
assert evaluator.evaluate(second)['status'] == 'matched'
assert evaluator.evaluate(negative)['status'] == 'not_matched'

if result['attribution']['status'] == 'captured':
    bibliography = phmt.attribution_report(query.metadata['attribution'], format='bibtex')
    assert 'Tomita' in bibliography and 'Hagberg' in bibliography
```

Each source has a unique declared `ligand_id`, one selected prepared frame and
one chemical state. Input records can supply `selection`, `structure_index` and
`chemical_state`, defaulting to `'all'`, `0` and `'reference'`. All inputs must
already share the intended coordinate frame. Empty sources count in support
fractions. Do not declare separate conformers as independent supporting ligands.

## Inspect the reusable discovery tools

An occurrence is `[inventory_index, feature_index]`. A site clique requires
equal feature kinds, different ligand identities and pairwise compatible center
distances/orientations. Maximal means that no compatible occurrence can be added;
all maximal sizes are considered, rather than just the largest clique.

```python
inventories = [phmt.modeler.get_features(
    entry['molecular_system'], features=['hydrophobicity'],
) for entry in ligands]
identities = [entry['ligand_id'] for entry in ligands]

discovery = phmt.modeler.get_aligned_feature_cliques(
    inventories, ligand_ids=identities, distance_tolerance='0.10 nm',
)
assert discovery['groups'] == [[[1, 0], [2, 0]]]

report = phmt.modeler.get_aligned_consensus_hypotheses(
    inventories, ligand_ids=identities, distance_tolerance='0.10 nm',
)
assert report['hypotheses'][0]['site_indices'] == [0]
assert report['candidate_sites'][0]['support_count'] == 2
```

Centers are unweighted means of feature centers. Directed donor vectors and
unoriented aromatic axes have different comparison rules. The member ordered
first by ligand ID supplies the recorded orientation; no angular mean is implied.
Each candidate retains member geometry/indices, frame/state, dispersion and support.

## Keep ambiguous alternatives separate

This analytical fixture gives one ligand two nearby acceptor occurrences and
another ligand one occurrence compatible with either. The shared occurrence
cannot support two sites within one hypothesis, so two models are returned.

```python
ambiguous = prepared('COCOC', [
    [-0.10, 0, 0], [0, 0, 0], [0, 0.10, 0], [0.02, 0, 0], [0.12, 0, 0],
])
partner = prepared('COC', [[-0.10, 0, 0], [0.01, 0, 0], [0.12, 0, 0]])

with phmt.attribution():
    alternatives = phmt.modeler.from_aligned_ligand_cliques(
        [
            {'ligand_id': 'a', 'molecular_system': ambiguous},
            {'ligand_id': 'b', 'molecular_system': partner},
        ],
        features=['hb acceptor'], distance_tolerance='0.05 nm',
    )

assert len(alternatives['models']) == 2
assert all(model.n_interaction_sites == 1 for model in alternatives['models'])
assert [item['site_indices'] for item in alternatives['report']['hypotheses']] == [[0], [1]]

from tempfile import TemporaryDirectory
from pathlib import Path
from pharmacophoremt.io.phmt import to_json, load_json

with TemporaryDirectory() as directory:
    path = Path(directory) / 'alternative.json'
    original = alternatives['models'][0]
    to_json(original, path)
    restored = load_json(path)
    assert restored.metadata == original.metadata
```

For multiple-site hypotheses, the intersection of supporters for **all** sites
must reach `min_support`. Pairwise support does not suffice. `min_sites` can
require a larger hypothesis. Packages are inclusion-maximal within the discovered
maximal-site-clique family; site subcliques and all possible molecular patterns
are outside this method's completeness claim.

Sites start essential with weight 1. Curate these choices and `radius` before
screening: support is correspondence frequency, not affinity, and a smaller
radius can reject a ligand that contributed to discovery. Alternative hypotheses
are not merged or automatically ranked as binding models.

## Completion, budgets and references

`max_graph_nodes` defaults to 64 input occurrences, `max_cliques` to 1000
enumerated maximal cliques (including unsupported ones), and `max_combinations`
to 10000 attempted package extensions. Exceeding any bound raises PHMT-E107;
there is no truncated successful query. These bound graph/output/package work,
not total input memory or the internal NetworkX search time. Completed empty
discovery has `complete=True` and `models=[]`; no empty usable query is created.

With [optional attribution](attribution.md), each result and derived model retains
the executed software versions, the
[NetworkX description](https://networkx.org/documentation/stable/#citing),
[Bron–Kerbosch](https://doi.org/10.1145/362342.362367) and the
[Tomita adaptation](https://doi.org/10.1016/j.tcs.2006.06.015) when clique enumeration
runs. The implementation identity follows the
[NetworkX provider documentation](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.find_cliques.html).
An empty graph does not credit a clique algorithm. The saved bibliography describes
the whole hypothesis-generation calculation and survives native serialization;
reading it does not execute another calculation. Missing/failing Ackredit preserves
the scientific result and offline host references.
