# Refine rigid correspondences with alternative orientation policies

This recipe consumes a manually supplied seed through a public refinador.
Seeds could instead come from [ranked search](ranked_seeds.md), cliques or another
proposal method. Both policies remain available; their relative results depend
on the input geometry, tolerances and seed choices.

The analytical donor fragments below contain explicit isotope hydrogens and
declared coordinates. They exercise geometry, not biological activity or
optimized conformations. MolSysMT supplies all molecular construction,
recognition, fitting and transformation.

```python
import numpy as np
import molsysmt as msm
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import get_features
from pharmacophoremt.screening import (
    evaluate_feature_correspondence,
    refine_rigid_feature_correspondences,
)

def donors(centers):
    coordinates = []
    for center in centers:
        # Each fragment has explicit H followed by O, with direction +x.
        coordinates.extend([center + [.1, 0, 0], center])
    system = msm.convert(
        msm.convert('smiles:' + '.'.join(['[2H]O'] * len(centers)),
                    to_form='rdkit.Mol'),
        to_form='molsysmt.MolSys',
    )
    system.structures.append(coordinates=puw.quantity([coordinates], 'nm'))
    return system

centers = np.array([[0., 0, 0], [.2, 0, 0], [0, .2, 0], [3, 0, 0]])
angle = np.pi / 4
rotation = np.array([[np.cos(angle), -np.sin(angle), 0],
                     [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
source_centers = centers.copy()
source_centers[:3] = source_centers[:3] @ rotation.T
reference, source = donors(centers), donors(source_centers)
target = get_features(reference, features=['hb donor'])
source_inventory = get_features(source, features=['hb donor'])
seeds = [[[0, 0], [1, 1], [2, 2]]]
```

Here the first three centers suggest a rotation that violates the donor-angle
criterion. Adding the fourth pair changes the fit enough to recover the angles.
final permits that intermediate state; each_step rejects it. Both require
position and orientation compatibility in the final returned matching.

```python
results = {}
for policy in ('final', 'each_step'):
    with phmt.attribution():
        results[policy] = refine_rigid_feature_correspondences(
            source, target, seeds,
            features=['hb donor'], feature_inventory=source_inventory,
            orientation_policy=policy, min_matches=4,
            distance_tolerance='.3 nm', direction_tolerance='30 degrees',
        )

assert len(results['final']['placements']) == 1
assert results['each_step']['placements'] == []
assert results['final']['report']['n_fits'] == 2
assert results['each_step']['report']['n_fits'] == 1
```

Evaluate the actual final matching independently. The evaluator works on any
number of explicitly supplied pairs in a shared frame; it neither chooses a
matching nor performs molecular operations. Measurements retain explicit units
as portable PyUnitWizard quantity records.

```python
placement = results['final']['placements'][0]
check = evaluate_feature_correspondence(
    target, placement['inventory'], placement['matches']['matches'],
    distance_tolerance='.3 nm', direction_tolerance='30 degrees',
)
assert check['all_pairs_valid']
assert len(check['pair_tests']) == 4

trace = results['final']['report']['refinement_seeds'][0]
assert trace['selected_step_index'] == 1
assert trace['steps'][0]['matches']['matches'] == []
assert len(trace['steps'][1]['matches']['matches']) == 4
```

Actual optional Ackredit capture records the adapted G3PS refinement, its angular
policy and reached provider/assignment methods. Installed Ackredit exports the
bibliography; it remains an optional scientific reporting dependency.

```python
bibliography = phmt.attribution_report(results['final']['attribution'], format='bibtex')
assert '10.3390/molecules26237201' in bibliography
```

In a prepared rigid consensus workflow, select refinement explicitly:

```python
from pharmacophoremt.modeler import from_rigid_ligands
from pharmacophoremt.validation import summarize_rigid_consensus

consensus = from_rigid_ligands(
    [{'ligand_id': 'reference', 'molecular_system': reference},
     {'ligand_id': 'source', 'molecular_system': source}],
    features=['hb donor'], correspondence_strategy='triplet_seeds',
    refinement_strategy='greedy', orientation_policy='final',
    min_matches=4, min_sites=4,
    distance_tolerance='.3 nm', direction_tolerance='30 degrees',
)
summary = summarize_rigid_consensus(consensus['report'])
assert summary['max_joint_sites'] == 4
assert summary['sources'][1]['orientation_policy'] == 'final'
```

Ordinary placement remains the default when refinement_strategy is None.
Refinement preserves the best fully evaluated accepted state per seed, so growth
that later worsens angular matching does not erase an earlier valid placement.
Fit anchors and final matches are separate evidence. The required min_matches
does not prevent smaller seeds from growing.

The source contract `devguide/rigid_refinement_workflow.md` also records a case
where each_step succeeds and final fails, plus a retained-checkpoint control.
Neither policy dominates these tests. Budgets count all initial/trial fits and
raise on exhaustion. Provider failures propagate. Completion concerns supplied
seeds and the chosen greedy policy; no global optimum, translation rescue,
orientation-aware fit or complete G3PS is claimed.

When comparing policies, vary the seeds as well as the tolerances: a seed rejected
by each_step can have a successful alternative, while starting from a larger
seed can skip a useful earlier checkpoint. Three distinct feature indices can
also share collinear centers, especially when donor and acceptor sites overlap;
the provider requires a noncollinear fitting geometry.

The source checkout includes eleven analytical workloads covering these choices,
mixed classical feature families, reflection, and 6/12-site donor arrangements.
Their opt-in benchmark can be run from the checkout with
`python -m devtools.benchmark_rigid_refinement --output /tmp/refinement-benchmark.json`.
It records solutions and fit counts beside three measured repeats per policy,
whole-worker peak memory, full scientific traces and a separate Ackredit call.
Preparation and citation capture are excluded from the measured refinement time.
See `devguide/evidence/README.md` for retained evidence and its limits.
