# Build consensus from two distinct prepared CCD ligands

Continue the [prepared workflow](prepared_workflow.md) using public CCD EST and
DES as different chemical inputs. The example consumes ideal coordinates and
explicit reference states, not experimental binding poses or activity labels.

## Declare method, sources and joint support

```python
from devtools.prepared_ccd_ligands import prepare_case, motion_frames
from devtools.prepared_consensus_workflow import OPTIONS
from pharmacophoremt.modeler import LigandBasedModeler

est = prepare_case('EST', features=['hb acceptor', 'aromatic ring'])
des = prepare_case('DES', features=['hb acceptor', 'aromatic ring'])
frames = motion_frames(des['molecular_system'])
ligands = [
    dict(ligand_id='EST', molecular_system=est['molecular_system'],
         structure_index=0, chemical_state='reference', selection='all'),
    dict(ligand_id='DES', molecular_system=frames,
         structure_index=1, chemical_state='reference', selection='all'),
]
modeler = LigandBasedModeler(ligands, consensus_method='rigid',
    n_points=3, min_actives=2, **OPTIONS)
models = modeler.build()
assert len(models) == 1 and modeler.result['complete']
hypothesis = models[0].metadata['hypothesis']
assert set(hypothesis['joint_ligand_ids']) == {'EST', 'DES'}
assert hypothesis['joint_support_count'] == 2
assert models[0].metadata['consensus']['n_ligands'] == 2
assert models[0].metadata['placements'][1]['alignment']['structure_index'] == 1
```

`OPTIONS` is a fixed case configuration: ranked triplets, four selected seeds,
greedy refinement, minimum three matches, distance 0.20 nm, angle 30 degrees and
100 fits. Molecular preparation, proper-motion placement and fitting use public
MolSysMT tools. DES frame one is another placement of the same conformation;
it does not add a ligand or conformer. Acceptors are spheres; no new donor or
acceptor direction calculation is introduced. Support is not affinity.

## Preserve empty outcomes and explicit failures

```python
from pharmacophoremt._private.smonitor.exceptions import CliqueLimitError

# EST has just three selected feature occurrences; four jointly supported,
# disjoint sites cannot be formed even though DES has four occurrences.
modeler.n_points = 4
assert modeler.build() == []
assert modeler.result['complete'] and modeler.report['n_layouts'] == 1
modeler.native_options['max_fits'] = 1
try:
    modeler.build()
except CliqueLimitError as error:
    assert error.code == 'PHMT-E107'
else:
    raise AssertionError('Budget exhaustion must remain failure')
assert modeler.result is None and modeler.report is None
```

The empty result is completed within the finite method and declared pivot/seed
family. Exhaustion provides no scientific negative and clears cached success.
The [validation case](../validation/prepared_consensus_workflow.md) checks support
sets, disjoint occurrences and member geometry independently of model counts.

```bash
python -m devtools.prepared_workflow --case consensus --output /tmp/prepared-consensus.json
python -m pytest tests/test_prepared_consensus_workflow.py --receptor=llm
```

The review preserves original atom/frame/state maps through JSON/YAML/PHMT SDF,
alternate unit policies, immutable sources, attribution repeats and fresh readers.
