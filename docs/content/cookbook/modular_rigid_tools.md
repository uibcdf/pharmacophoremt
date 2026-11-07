# Compose rigid modeling from reusable steps

Choose correspondence proposals, place each mapping and build hypotheses as
separate operations. `from_rigid_ligands()` composes these public tools and adds
pivot, support and layout accounting. Run the blocks in order.

## Extract once and build a query

This charge triangle is an analytical geometry control. Its six permutations
illustrate alternatives, not distinct binding modes. Molecular construction and
transformations go through MolSysMT.

```python
import json
import molsysmt as msm
import numpy as np
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw

reference = msm.convert(
    msm.convert('smiles:[Na+].[K+].[Li+]', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
coordinates = [[0, 0, 0], [.4, 0, 0], [.2, np.sqrt(3) * .2, 0]]
reference.structures.append(coordinates=puw.quantity([coordinates], 'nm'))
source = msm.structure.translate(
    reference, translation=puw.quantity([[[2., 1, 3]]], 'nm'), in_place=False,
)
families = ['positive charge']
reference_inventory = phmt.modeler.get_features(reference, features=families)
source_inventory = phmt.modeler.get_features(source, features=families)
query = phmt.modeler.from_feature_inventory(
    reference_inventory, radius='0.01 nm', name='Cached charge query',
)
assert query.n_interaction_sites == 3
```

`from_feature_inventory()` uses native quantity objects and performs no molecular
reads or repeated recognition. Reuse an inventory only with its unchanged source,
selection, frame, chemical state and feature-family request. Detached report JSON
is retained evidence, rather than a native inventory input to this function.

## Choose proposals, then place them

```python
with phmt.attribution():
    proposals = phmt.screening.get_rigid_feature_correspondences(
        reference_inventory, source_inventory,
        correspondence_strategy='association_cliques', distance_tolerance='0.01 nm',
        min_matches=3,
    )
    assert proposals['complete']
    placed = phmt.screening.get_rigid_feature_placements(
        source, reference_inventory, proposals['correspondences'],
        feature_inventory=source_inventory, features=families,
        distance_tolerance='0.01 nm', min_matches=3,
    )

assert placed['complete'] and len(placed['placements']) == 6
assert placed['report']['n_fits'] == 6
json.dumps(placed['report'], allow_nan=False)
option = placed['placements'][0]
assert option['molecular_system'] is not source
aligned = phmt.modeler.get_aligned_consensus_hypotheses(
    [reference_inventory, option['inventory']], ligand_ids=['a', 'b'],
    distance_tolerance='0.01 nm', min_support=2, min_sites=3,
)
assert aligned['complete'] and aligned['hypotheses']
assert aligned['hypotheses'][0]['joint_ligand_ids'] == ['a', 'b']
```

Substitute `correspondence_strategy='triplet_seeds'` or supply mappings from another proposal
method. Each mapping must be injective and have at least three non-collinear
pairs. MolSysMT performs the fit and coordinate installation; PHMT checks absolute
feature positions, orientations and full-inventory matching.

Accepted options contain independent molecular copies and reusable inventories.
The portable report retains accepted/rejected evidence and omits live molecular
systems. `complete=True` covers supplied mappings; check proposal completion
separately. Budget exhaustion raises a diagnostic. All accepted alternatives
remain available, including equivalent placements.

## Reuse one prepared source across queries

Keep the requested families and the source selection, frame and chemical state
explicit when reusing an inventory. Here a second reference has different
internal distances. Continue from the prepared `reference`, `source` and
`families` above; all operations below use the public API.

```python
alternative = msm.copy(reference)
values = puw.get_value(msm.get(alternative, coordinates=True), to_unit='nm').copy()
values[0, 2] = [0.2, 1.0, 0.0]
msm.set(alternative, coordinates=puw.quantity(values, 'nm'))
references = [
    ('original', phmt.modeler.get_features(
        reference, features=families, chemical_state=0)),
    ('changed-distances', phmt.modeler.get_features(
        alternative, features=families, chemical_state=0)),
]
source_inventory = phmt.modeler.get_features(
    source, features=families, chemical_state=0,
)
results = {}
for name, target in references:
    proposals = phmt.screening.get_rigid_feature_correspondences(
        target, source_inventory, distance_tolerance='0.01 nm',
        min_matches=3, max_graph_nodes=64, max_cliques=1000,
    )
    placed = phmt.screening.get_rigid_feature_placements(
        source, target, proposals['correspondences'], features=families,
        feature_inventory=source_inventory, chemical_state=0,
        distance_tolerance='0.01 nm', min_matches=3, max_fits=16,
    )
    results[name] = {
        'proposals': proposals,
        'placement_report': placed['report'],
    }

assert results['original']['placement_report']['n_fits'] == 6
assert results['changed-distances']['proposals']['correspondences'] == []
assert results['changed-distances']['placement_report']['n_fits'] == 0
```

The same source inventory serves both requests. Fitting still extracts features
from each placed copy and checks their identities and geometry. This reuses the
initial observation; it does not remove native post-fit validation. Changing
the source, geometry, chemistry, selection, frame or feature-family request
requires a new compatible inventory. Axis agreement alone cannot authenticate
its source. Keep the family declaration even if no records of a kind are found.

This example fits all proposed mappings within its explicit budget. Selecting
only a prefix instead requires reporting the omitted mappings; an empty accepted
prefix is not a compound negative. The [reuse control](../validation/reused_feature_inventories.md)
compares complete fresh/reused native evidence for that separate bounded case.
Neither route is a replacement for `RigidPoseSearch`'s full stopping/scoring
contract or a performance benchmark. Use compatible verified provider versions;
source composition evidence alone does not qualify an installed package.

## Summarize a saved consensus report

```python
with phmt.attribution():
    result = phmt.modeler.from_rigid_ligands(
        [
            {'ligand_id': 'a', 'molecular_system': reference},
            {'ligand_id': 'b', 'molecular_system': source},
        ],
        features=families, min_matches=3, min_support=2, min_sites=3,
        distance_tolerance='0.01 nm', radius='0.01 nm',
    )
saved_report = json.loads(json.dumps(result['report'], allow_nan=False))
summary = phmt.validation.summarize_rigid_consensus(saved_report)
assert summary['n_fits'] == 6
assert summary['n_layouts'] == summary['n_models'] == 6
assert summary['max_joint_sites'] == 3
assert summary['sources'][1]['max_accepted_matches'] == 3
assert all(item['joint_ligand_ids'] == ['a', 'b']
           for item in summary['hypotheses'])
```

Summary reading performs no molecular calculation and adds no citation. It
validates completion/count consistency and separates proposals, fits, accepted
placements, observed matches and jointly supported hypotheses. Coverage is not
affinity. Keep the original attribution alongside the summary, as in the
[attribution recipe](attribution.md).

## Compare strategies reproducibly

The [ranked-seed recipe](ranked_seeds.md) adds a reusable environment descriptor
and optional seed selection, with a control showing the risk of missed matches.

From a source checkout, run the optional driver without another known local test
or benchmark load:

```bash
python -m devtools.benchmark_rigid_consensus --repetitions 3 --warmups 1 --output /tmp/rigid-comparison.json
```

Six frozen analytical cases cover rigid motion, reflection, symmetry, differing
coverage objectives, empty recognition and exhausted fit budget. Each case and
strategy runs in its own worker, sequentially. Timings exclude imports, fixtures,
warmups, summaries and a separate attribution call. Memory is whole-worker
high-water RSS, including setup; it is not incremental per-call allocation.
Samples, scientific outcomes, environment and source hashes are retained.

The warped-square control is useful: a full-mapping least-RMSD fit matches zero
features at the requested tolerance, while triplet placements match three, with
larger RMSD over the same four feature pairs. Compare coverage as well as time.
Neither finite family proves global continuous optimality. These baseline calls
execute no G3PS method. The [ranked-seed recipe](ranked_seeds.md) demonstrates the
separate implemented seed-stage adaptation and its selection limits.

The measurement contract lives in `devguide/rigid_strategy_comparison.md` in the
source repository, tracked in [#27](https://github.com/uibcdf/pharmacophoremt/issues/27).
