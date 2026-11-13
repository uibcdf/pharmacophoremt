# Inspect and compare cached hypotheses

These development-source tools inspect native model sites without accessing a
molecular system. Distances describe the stored coordinate frame. Supply models
in a common frame before comparing them; these operations do not align them.

## Inspect distances and a table

```python
import numpy as np
from pharmacophoremt import Pharmacophore, pyunitwizard as puw
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Point, Sphere

query = Pharmacophore(name='cached geometry')
query.add_interaction_site(InteractionSite(Point('[0,0,0] nm'), 'hydrophobicity'))
query.add_interaction_site(InteractionSite(Sphere('[.3,.4,0] nm', '.1 nm'), 'hb donor'))
matrix = query.get_distance_matrix()
np.testing.assert_allclose(puw.get_value(matrix, to_unit='angstrom'), [[0,5],[5,0]],
                           rtol=0, atol=1e-12)
table = query.to_dataframe()
assert list(table.columns) == ['index', 'features', 'shape', 'center', 'radius']
assert table.loc[0, 'radius'] is None
assert table.loc[0, 'center'] is query.interaction_sites[0].center
assert table.loc[0, 'features'] is query.interaction_sites[0].features
assert list(Pharmacophore().to_dataframe().columns) == list(table.columns)
```

The matrix is an independent length quantity; choose an explicit output unit
when extracting numbers. Empty and singleton matrices have shapes `(0,0)` and
`(1,1)`. A larger model requires a finite three-coordinate length center for
every site. Points use their canonical position. Cylinders have no inferred
center and cannot enter a larger center-distance matrix.

The table has the same five columns even when empty. It is an inspection table:
its object cells retain the original feature lists and quantities. Mutating a
contained object edits that model; replacing a cell only changes the table.
Use `query.copy()` before such exploration when you need an independent variant.
Missing centers/radii remain `None`. Use native model persistence for interchange.

## Understand the existing ordered comparison

```python
def point_query(xs):
    result = Pharmacophore()
    for x in xs:
        result.add_interaction_site(InteractionSite(
            Point(puw.quantity([x,0,0], 'nm')), 'hydrophobicity'))
    return result

left, right = point_query([.1,0]), point_query([0,.3])
assert left.similarity(right, tolerance_nm=.21) == .5
assert right.similarity(left, tolerance_nm=.21) == 1
assert left.similarity(left, tolerance_nm=0) == 1
assert Pharmacophore().similarity(Pharmacophore()) == 0
```

`similarity()` retains the existing greedy rule: visit sites in stored order,
take the closest unused counterpart sharing any feature name and count it when
its distance is within `tolerance_nm`. The score is twice that count divided by
the total number of sites. Missing centers stay unmatched and remain in the
denominator. This ordered score can change when models are swapped; it is not a
symmetric maximum-matching Dice coefficient. The separately owned
[symmetric-method proposal](https://github.com/uibcdf/pharmacophoremt/issues/205)
tracks that scientific extension and its compatibility decision.

The finite nonnegative numeric tolerance always means **nm**, including when the
application uses pm. It is not a quantity/string parameter. Radius, orientation,
weight, essential and exclusion semantics are not applied by this comparison;
use pose evaluation for those constraints. The score is not binding affinity or
biological activity.

## Explicit controls and saved readback

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from pharmacophoremt import io

for control in [{}, {'skip_digestion': False}, {'skip_digestion': True}]:
    assert left.similarity(right, .21, **control) == .5
    assert left.get_distance_matrix(**control).shape == (2,2)
    assert len(left.to_dataframe(**control)) == 2
with TemporaryDirectory() as directory:
    path = Path(directory) / 'query.json'
    io.to_json(query, path)
    restored = io.load_json(path)
    assert restored.metadata == query.metadata
    np.testing.assert_allclose(
        puw.get_value(restored.get_distance_matrix(), to_unit='nm'),
        [[0,.5],[.5,0]], rtol=0, atol=1e-14)
```

Keep the default argument validation for user inputs. Deliberate `True` requires
canonical inputs and bypasses only that call's argument preprocessing. Native
model/required-center and comparison-threshold checks stay active. The distance
tool validates its model/centers before its existing internal `get()` bypass;
it builds the fixed query arguments itself. No global bypass is propagated.

These are analytical API and geometry controls, with source and isolated-wheel
receiving. They do not qualify a symmetric method, large-scale matrix storage,
biological performance or the complete supported-platform/public installation.
