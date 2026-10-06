# Rank rigid seeds by typed feature environments

Use `get_feature_pair_dissimilarities()` and `rank_rigid_feature_correspondences()`
to prioritize supplied guesses before fitting them. The convenience strategy
`ranked_triplet_seeds` composes both with the existing typed triplet generator.
It adapts the seed-selection stage in section 2.2.1 of the
[G3PS paper](https://doi.org/10.3390/molecules26237201); greedy refinement and
translation/exclusion correction are separate future stages.

## Prepare an analytical control

Run the blocks in order. Two positive and two negative charge features form a
tetrahedron. The source's last vertex is reflected. Alternative same-type
correspondences allow a proper rigid alignment; a distance-only ranking cannot
identify that orientation constraint reliably from a single seed.

```python
import json
import molsysmt as msm
import numpy as np
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw

points = [
    [0, 0, 0], [.4, 0, 0], [.2, np.sqrt(3)*.2, 0],
    [.2, np.sqrt(3)*.4/6, np.sqrt(2/3)*.4],
]
reference = msm.convert(
    msm.convert('smiles:[Na+].[K+].[Cl-].[Br-]', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
reference.structures.append(coordinates=puw.quantity([points], 'nm'))
source_points = [list(point) for point in points]
source_points[-1][-1] *= -1
source = msm.copy(reference)
msm.set(source, coordinates=puw.quantity([source_points], 'nm'))
families = ['positive charge', 'negative charge']
target_inventory = phmt.modeler.get_features(reference, features=families)
source_inventory = phmt.modeler.get_features(source, features=families)
```

These are declared fragment coordinates, not a biological or conformer-energy
benchmark. MolSysMT supplies all molecular construction and geometry operations.

## Compare environments, then rank supplied triplets

```python
with phmt.attribution():
    dissimilarities = phmt.screening.get_feature_pair_dissimilarities(
        target_inventory, source_inventory, distance_tolerance='0.01 nm',
    )
    proposals = phmt.screening.get_rigid_feature_correspondences(
        target_inventory, source_inventory,
        correspondence_strategy='triplet_seeds', distance_tolerance='0.01 nm',
    )
    ranked = phmt.screening.rank_rigid_feature_correspondences(
        proposals['correspondences'], dissimilarities, n_seeds=1,
    )

assert dissimilarities['complete'] and proposals['complete'] and ranked['complete']
assert ranked['n_supplied'] == 16 and ranked['n_selected'] == 1
assert ranked['n_omitted'] == 15 and not ranked['selection_exhaustive']
json.dumps(dissimilarities, allow_nan=False)
```

The comparison assigns typed neighbor distances and reports a dimensionless
dissimilarity matrix with an independent compatibility mask. Uniform tolerances
and unit-cost padding for unmatched neighbors are explicit PHMT adaptations.
Ranking sums the three selected pair costs. Canonical mappings and supplied
indices break ties deterministically; duplicates remain alternatives. No molecular
read or fit occurs in either tool. Existing inventories and saved comparisons
can be reused with their original feature-index domains.

## Compare one selected seed with all seeds

```python
ligands = [
    {'ligand_id': 'a', 'molecular_system': reference},
    {'ligand_id': 'b', 'molecular_system': source},
]
settings = dict(
    features=families, correspondence_strategy='ranked_triplet_seeds',
    distance_tolerance='0.01 nm', min_matches=4, min_sites=4,
)
with phmt.attribution():
    selected = phmt.modeler.from_rigid_ligands(ligands, n_seeds=1, **settings)
    all_seeds = phmt.modeler.from_rigid_ligands(ligands, **settings)

assert selected['complete'] and selected['models'] == []
assert all_seeds['complete'] and len(all_seeds['models']) == 8
short = phmt.validation.summarize_rigid_consensus(selected['report'])
full = phmt.validation.summarize_rigid_consensus(all_seeds['report'])
assert short['n_fits'] == 1 and full['n_fits'] == 16
assert short['sources'][1]['proposal_selection_exhaustive'] is False
assert full['max_joint_sites'] == 4
```

`n_seeds=None` retains the whole feasible triplet family; a positive integer
selects at most that many ranked guesses. This scientific selection can miss
valid placements, as the control demonstrates. `complete=True` means the declared
selection was evaluated. It does not prove that no other mapping or continuous
alignment could work. Work budgets such as `max_trials` and `max_fits` still raise
on exhaustion, rather than silently dropping guesses.

With all seeds retained, ranked and unranked triplets contain identical mappings;
ordering and layout IDs can differ. MolSysMT fits them and PHMT applies the same
absolute center, donor-vector/aromatic-axis and injective matching checks. The
default association-clique strategy remains unchanged.

## Keep the reached-stage citation

```python
if all_seeds['attribution']['status'] == 'captured':
    bibliography = phmt.attribution_report(all_seeds['attribution'], format='bibtex')
    assert '10.3390/molecules26237201' in bibliography
    assert '10.1109/TAES.2016.140952' in bibliography
    assert all_seeds['models'][0].metadata['attribution'] == all_seeds['attribution']
```

Ackredit retains the method's paper, adapted stage and actual SciPy assignment
reference, together with reached placement/consensus methods. It does not credit
the omitted G3PS refinement or rescue stages as executed. Native saving/loading
preserves this bibliography as in the [attribution recipe](attribution.md).

For an optional source-checkout comparison with one warmup and three measured
calls per sequential isolated worker:

```bash
python -m devtools.benchmark_rigid_consensus --cases tests/data/ranked_seed_cases.json --strategies triplet_seeds ranked_triplet_seeds --repetitions 3 --warmups 1 --output /tmp/ranked-comparison.json
```

The fixtures declare strategy-specific settings. Compare coverage, omitted seeds
and alternative counts as well as time; fewer fits with fewer solutions is a
different scientific tradeoff. The contract lives in `devguide/ranked_seed_workflow.md`
and [issue #28](https://github.com/uibcdf/pharmacophoremt/issues/28).
