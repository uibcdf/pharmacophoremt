# Compare positive pharmacophore centers symmetrically

The development-source tool `compare_pharmacophores()` finds maximum one-to-one
overlap between positive Point/Sphere sites. Its score is symmetric and
independent of site order. It compares prepared coordinates directly; supply a
common coordinate basis. It does not align models or inspect molecules.

## Choose the comparison explicitly

```python
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Point

def query(xs):
    result = phmt.Pharmacophore()
    for x in xs:
        result.add_interaction_site(InteractionSite(
            Point(puw.quantity([x,0,0], 'nm')), 'hydrophobicity'))
    return result

left, right = query([.1,0]), query([0,.3])
assert left.similarity(right, .21) == .5
assert right.similarity(left, .21) == 1
assert left.similarity(right, .21, method='maximum_cardinality') == 1
assert right.similarity(left, .21, method='maximum_cardinality') == 1
report = phmt.compare_pharmacophores(left, right, distance_tolerance='210 pm')
assert report['complete'] and report['similarity'] == 1
assert report['n_matches'] == 2
assert {(p['site_index'],p['other_site_index']) for p in report['matches']} == {(0,1),(1,0)}
```

The old default is explicitly `method='ordered_greedy'`; its results remain
compatible. Choose the new method when symmetric center/feature overlap is the
intended question. The public report tool supplies correspondence and expert
controls. Its quantity tolerance requires a unit; the convenience method keeps
its historical numeric `tolerance_nm` convention.

## Understand the scope and limits

Features on one site are alternatives: any shared positive name makes a pair
chemically compatible. Geometry then tests center separation. Each occurrence
can match once. Radius, weight and essential flags are recorded but do not
weight this score. Directed sites, disks, cylinders, Gaussian kernels and volume
constraints are refused. Use pose evaluation for its supported geometric and
steric constraints. This normalized overlap is not affinity or activity.

```python
from pharmacophoremt import ComparisonLimitError

assert phmt.compare_pharmacophores(query([]), query([]))['similarity'] == 0
try:
    phmt.compare_pharmacophores(left, right, max_matrix_entries=3)
except ComparisonLimitError as error:
    assert error.code == 'PHMT-E111'
else:
    raise AssertionError('The four-entry matrix exceeds the declared budget')
for control in [{}, {'skip_digestion': False}, {'skip_digestion': True}]:
    assert phmt.compare_pharmacophores(left, right, distance_tolerance='210 pm',
                                      **control)['similarity'] == 1
```

Expert controls bound sites per input and pair-matrix entries before geometry
processing/allocation. Exceeding a quota raises rather than returning an
incomplete score. The default scalar convenience route uses the report tool's
default budgets. These are dimension limits, not a timeout or complete process
memory guarantee. Tied optimal pair identities may differ after reordering;
match count and score stay invariant. Positive tolerances include a declared
relative roundoff margin; zero tolerance is exact for represented centers.

## Retain correspondence and actual calculation references

```python
import json
import ackredit as ack

with ack.session('model comparison workflow'):
    with phmt.attribution():
        first = phmt.compare_pharmacophores(left, right, distance_tolerance='.21 nm')
        second = phmt.compare_pharmacophores(left, right, distance_tolerance='.21 nm')
        empty = phmt.compare_pharmacophores(query([]), query([]))
    assert first['attribution']['status'] == second['attribution']['status'] == 'captured'
    assert first['attribution']['references']['items'] == second['attribution']['references']['items']
    assert not any(entry['record']['title'] == 'SciPy'
                   for entry in empty['attribution']['host_references'])
    saved = json.loads(json.dumps(second))
    assert saved == second
    before = ack.get_attribution().to_dict()
    references = ack.Attribution.from_dict(saved['attribution']['references'])
    assert references.report(format='bibtex')
    assert ack.get_attribution().to_dict() == before
```

Assignment reuses the supported [SciPy routine](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html).
Optional attribution records the executed branch, including references reused
inside an enclosing workflow. Missing or failed attribution preserves completed
science. Input-axis snapshots and distances carry explicit quantity records;
keep original native models for complete metadata, observations and earlier
bibliography. Reading saved JSON/references does not run another comparison.

The [analytical validation case](../validation/symmetric_model_comparison.md)
records independent small exhaustive oracles and source/owned receiving. This
first profile does not establish biological relevance or large-library speed.
