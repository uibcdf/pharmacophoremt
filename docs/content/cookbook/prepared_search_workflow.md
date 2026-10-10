# Recover a moved prepared ligand and retain limited-search failures

Continue the [placed prepared workflow](prepared_workflow.md) with an explicitly
different hypothesis appropriate for rigid search. The public frozen EST ideal
geometry and its chemical state stay under the same preparation contract.

## Declare three independent center anchors

```python
from devtools.prepared_ccd_ligands import prepare_case, motion_frames
from devtools.prepared_workflow import build_hypotheses
from pharmacophoremt.modeler import edit_pharmacophore
from pharmacophoremt.screening import PoseEvaluator, RigidPoseSearch

prepared = prepare_case('EST', features=['hydrophobicity', 'aromatic ring'])
source = prepared['molecular_system']
_, narrow, _ = build_hypotheses(prepared)
assert [i for i, site in enumerate(narrow.interaction_sites) if site.essential] == [0]
# Frozen ring-first model: sites 1/5 correspond to source atoms 0/8.
assert [narrow.interaction_sites[i].metadata['atom_indices'] for i in (1,5)] == [[0],[8]]
query = edit_pharmacophore(narrow, site_indices=[1,5], essential=True,
    reason='declared non-collinear rigid anchors')
frames = motion_frames(source)
assert PoseEvaluator(query).evaluate(frames, structure_index=1)['status'] == 'not_matched'
recovered = RigidPoseSearch(query).evaluate(frames, structure_index=1)
assert recovered['status'] == 'matched' and recovered['fit_value'] == 1
assert recovered['alignment']['provider'] == 'molsysmt.structure.least_rmsd_fit'
assert recovered['structure_index'] == 1
```

The single-essential-site query supports placed evaluation. This rigid triplet
method requires at least three non-collinear essential centers, so the added
anchors are a declared hypothesis change. MolSysMT rotates/translates the molecular
system and fits proposed correspondences. Frame one is a second placement of
the same conformation; no conformer or chemical state is generated.

## Keep complete negatives separate from unresolved searches

```python
from pharmacophoremt.screening import ConformerScreening

negative = RigidPoseSearch(query).evaluate(source, selection=[0,1,2,4,5,10])
assert negative['status'] == 'not_matched'
assert negative['missing_essential_sites'] == [5]
assert negative['search']['enumeration_complete']
failed = RigidPoseSearch(query, max_trials=1).run(
    [frames], structure_index=1, on_error='record')[0]
assert failed['status'] == 'failed' and failed['fit_value'] is None
assert failed['error']['stage'] == 'search_budget'

limited = ConformerScreening(query, max_trials=1).evaluate(
    frames, structure_indices=[1,0], on_error='record')
assert limited['status'] == 'matched' and limited['fit_value'] == 1
assert limited['best_conformer_index'] == 0
assert limited['ensemble']['score_resolved'] and not limited['ensemble']['complete']
assert [row['status'] for row in limited['conformers']] == ['failed','matched']
assert limited['conformers'][0]['fit_value'] is None
```

The selected original ring lacks enough geometric reach to fill the required
atom-eight anchor. It is a complete negative for this discrete method, even
though some optional sites match. The one-product budget cannot resolve the moved
frame. In the ensemble, the original frame proves a valid coverage-one maximum;
that resolves the score while retaining the failed frame and incomplete ensemble.
Never infer complete execution from the top-level matched status alone.

## Review saved queries and source mappings

```bash
python -m devtools.prepared_workflow --case search --output /tmp/prepared-search.json
python -m pytest -q tests/test_prepared_search_workflow.py tests/test_prepared_workflow.py
```

The opt-in review uses JSON/YAML/versioned pharmacophore SDF, nondefault unit
policies, both frame orders, public fit replay, immutable input states/coordinates,
stable facade ties, attribution on/off and fresh readers. Its
[validation case](../validation/prepared_search_workflow.md) retains the actual
outputs and limits. These are analytical workflow controls, not activity labels,
experimental poses, generated-conformer qualification or a speed comparison.
