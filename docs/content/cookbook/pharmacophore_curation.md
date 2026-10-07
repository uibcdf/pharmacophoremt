# Create and evaluate independent hypothesis variants

Select, copy, extract and edit cached models as separate workflow steps. These
operations belong to PharmacophoreMT; molecular preparation and transformations
use MolSysMT. A copied model retains its molecular-system reference. Copy that
molecular system through MolSysMT when an independent molecular graph is needed.

## Select sites and declare a geometric alternative

This source-checkout example reuses the prepared analytical interaction fixture
from `devtools`. Its disconnected fragments are adapter controls, not a biological
ligand–receptor complex. In an application, supply your existing native model.

```python
import molsysmt as msm
import numpy as np
import pharmacophoremt as phmt
from devtools.interaction_collection_cases import build_case, observe
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import (
    copy_pharmacophore, edit_pharmacophore, extract_pharmacophore,
    from_interaction_collection, get_interaction_site_indices,
)
from pharmacophoremt.screening import PoseEvaluator

source, ligand, partner = build_case()
with phmt.attribution():
    original = from_interaction_collection(
        source, observe(source, ligand, partner), ligand, radius='.02 nm')
original.name, original.score = 'original observations', .9
assert original.n_interaction_sites == 9

copied = copy_pharmacophore(original, name='independent alternative')
assert copied.score == original.score
assert copied.molecular_system is original.molecular_system
assert copied.interaction_sites[0] is not original.interaction_sites[0]

donors = get_interaction_site_indices(
    original, feature_names='hb donor', shape_names='sphere and vector')
query = extract_pharmacophore(original, site_indices=donors, name='donor subset')
assert len(donors) == query.n_interaction_sites == 1
assert query.score is None
assert query.metadata['site_map'] == [dict(source_site_index=donors[0], site_index=0)]

candidate = msm.structure.translate(
    source, selection=ligand, translation='[0,0,.05] nm', in_place=False)
narrow = PoseEvaluator(query).evaluate(candidate, selection=ligand)
relaxed = edit_pharmacophore(
    query, radius='.1 nm', reason='declared geometric tolerance control')
wide = PoseEvaluator(relaxed).evaluate(candidate, selection=ligand)
assert narrow['status'] == 'not_matched'
assert wide['status'] == 'matched' and wide['fit_value'] == 1
np.testing.assert_array_equal(
    puw.get_value(query.interaction_sites[0].center, to_unit='nm'),
    puw.get_value(relaxed.interaction_sites[0].center, to_unit='nm'))
np.testing.assert_array_equal(
    puw.get_value(query.interaction_sites[0].direction, to_unit='dimensionless'),
    puw.get_value(relaxed.interaction_sites[0].direction, to_unit='dimensionless'))
```

The radius alternative accepts a known displacement without moving the model or
changing donor orientation. This demonstrates the parameter's meaning; it does
not establish that the wider hypothesis predicts activity better. Retain both
variants for a declared validation experiment.

Indices refer to local model sites, with caller order preserved. Exact feature
and shape filters combine with AND; unknown names raise. Empty selection and
extraction are valid, but an empty model is not a usable pose query. Radius edits
apply to spheres, spheres with vectors, disks and cylinders. Use `sigma` for
Gaussian width; `set_radius()` now rejects a Gaussian rather than silently
changing another magnitude. Geometry editing does not extend evaluator shape
support.

## Compare weights, essential sites and exclusions

Declare an additional unfulfilled positive constraint. Keep its obligatory and
weighted meanings separate, then demonstrate an independent steric veto.

```python
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere

extra = copy_pharmacophore(original)
missing = extra.n_interaction_sites
extra.add_interaction_site(InteractionSite(
    Sphere('[9,0,0] nm', '.02 nm'), 'hydrophobicity'))
required = PoseEvaluator(extra).evaluate(source, selection=ligand)
optional = edit_pharmacophore(extra, site_indices=missing, essential=False)
optional_result = PoseEvaluator(optional).evaluate(source, selection=ligand)
weighted = edit_pharmacophore(optional, site_indices=missing, weight=3)
weighted_result = PoseEvaluator(weighted).evaluate(source, selection=ligand)
zero = edit_pharmacophore(extra, site_indices=missing, weight=0)
zero_result = PoseEvaluator(zero).evaluate(source, selection=ligand)
assert required['status'] == 'not_matched' and np.isclose(required['fit_value'], .9)
assert optional_result['status'] == 'matched' and np.isclose(optional_result['fit_value'], .9)
assert np.isclose(weighted_result['fit_value'], .75)
assert zero_result['status'] == 'not_matched' and zero_result['fit_value'] == 1

collision = copy_pharmacophore(original)
collision.add_interaction_site(InteractionSite(
    Sphere('[3,0,0] nm', '.05 nm'), 'excluded volume', weight=0, essential=False))
edited_collision = edit_pharmacophore(
    collision, site_indices=collision.n_interaction_sites - 1,
    essential=False, weight=0)
veto = PoseEvaluator(edited_collision).evaluate(source, selection=ligand)
assert veto['status'] == 'not_matched' and veto['fit_value'] == 1
assert veto['excluded_volume_clashes']
positive = extract_pharmacophore(
    edited_collision, site_indices=range(original.n_interaction_sites),
    reason='explicit alternative without this exclusion')
assert PoseEvaluator(positive).evaluate(source, selection=ligand)['status'] == 'matched'
```

Zero weight does not remove an essential constraint or an exclusion. Extraction
explicitly removes unwanted constraints. Matching also uses one-to-one candidate
allocation: a very wide radius cannot create extra chemical participants.
The coverage value is geometric fit, not affinity.

Edits require at least one target and one changed field. Weights must be finite
nonnegative real scalars, flags booleans, and lengths positive scalar quantities
with units. Incompatible targets raise before modifying the original, including
with `in_place=True`. Class setters `set_radius`, `set_sigma`, `set_weight` and
`set_essential` delegate to the same editor, update in place and return None.

## Preserve original evidence and capture actual work

Copying preserves score and bibliography. Extraction and editing invalidate score
and retain the complete original native model in `metadata['source_model']`, with
local source/output mapping and before/after values. Repeated edits nest this
history. Original observation indices remain scoped to their own analyses.

```python
import ackredit as ack
from pathlib import Path
from tempfile import TemporaryDirectory
from pharmacophoremt.io import load_json, load_yaml, to_json, to_yaml

with ack.session('explicit hypothesis variants'):
    with ack.capture('cached operations') as cached:
        with phmt.attribution():
            copied = copy_pharmacophore(original)
            rings = get_interaction_site_indices(copied, feature_names='aromatic ring')
            ring_query = extract_pharmacophore(copied, site_indices=rings)
    assert cached.attribution.to_dict()['uses'] == []
    with ack.capture('declared radius edit') as edited:
        with phmt.attribution():
            variant = edit_pharmacophore(
                copied, site_indices=rings, radius='200 pm', weight=2,
                reason='caller-declared ring tolerance and weight')
    uses = edited.attribution.to_dict()['uses']
    assert any('edit_pharmacophore' in row['used_by'] for row in uses)
    assert not any('get_pi_pi_interactions' in row['used_by'] for row in uses)

assert variant.metadata['source_model']['metadata']['attribution'] == original.metadata['attribution']
assert variant.metadata['source_model']['score'] == .9 and variant.score is None
with TemporaryDirectory() as directory:
    with puw.context(standard_units=['pm', 'fs', 'degrees']):
        for suffix, write, read in [('json', to_json, load_json), ('yaml', to_yaml, load_yaml)]:
            path = Path(directory) / ('variant.' + suffix)
            write(variant, path)
            restored = read(path)
            assert restored.metadata == variant.metadata
            for index in rings:
                assert np.isclose(float(puw.get_value(
                    restored.interaction_sites[index].shape.radius, to_unit='nm')), .2)
```

Optional attribution records actual host edits and unit work without re-crediting
detectors. Pure cached operations add no calculation credits; earlier references
remain in source history. No publication is assigned to these caller choices.
Tracking failure/absence preserves completed scientific edits under the existing
[attribution contract](attribution.md).

Names, identifiers and notes remain literal text, including NumPy text such as
`'2 m'` or `'1 ps'`; they are not inferred to be quantities. Actual metadata
quantities retain their own portable value/unit records. Decode a declared
quantity field through `puw.QuantityRecord.from_dict(record).to_quantity()`
and extract with an explicit target unit. Native model geometry uses declared
nm lengths and dimensionless directions across application unit policies.
See the maintained
[persistence contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/native_provenance_persistence.md).

Compose native observed evidence with bounded `same_participant` reuse before
curation. A curated metadata root has a different contract; use generic `keep`
composition for explicit curated hypotheses. The complete source snapshot
requires native-serializable models. This recipe qualifies local constraint and
provenance behavior, with no biological, activity-learning or speed claim.
