# Prepared upstream report: stale mutable pmapper cache

Status: **prepared, not submitted**. Intended owner: DrrDom/pmapper.
Consumer evidence: PHMT#175, source1.1.3at
2f77e6482f6bd9bd7cc1f62b5d569ffdb8e8aafd. This is one invalidation mechanism
observed through two public mutation routes. It is not a PHMT runtime defect.
The existing upstream cache search found only#3, an unrelated documentation typo;
that bounded search does not prove no other related report exists.

## Concrete material ready for maintainer review

Suggested title: Cached signatures remain stale after bin changes or coordinate reload.

Minimal reproduction, using the unchanged public coordinate API:

```python
from pmapper.pharmacophore import Pharmacophore

points = [('P', (0, 0, 0)), ('N', (1.25, 0, 0)), ('H', (0, 3.25, 0))]

def make(rows, step=1, cached=False):
    p = Pharmacophore(bin_step=step, cached=cached)
    p.load_from_feature_coords(rows)
    return p

warm = make(points, cached=True)
original = warm.get_signature_md5()
warm.update(bin_step=0.5)
print(original, warm.get_signature_md5(), make(points, step=0.5).get_signature_md5())

warm = make(points, cached=True)
warm.get_signature_md5()
replacement = [(label, tuple(2*x for x in xyz)) for label, xyz in points]
warm.load_from_feature_coords(replacement)
print(warm.get_signature_md5(), make(replacement).get_signature_md5())
```

Expected: an updated/reloaded cached object agrees with a fresh object having the
same current coordinates/settings. Observed in both source and unchanged-owned214
PHMT contexts: the warm hash stays
`ec3cebb4aec15ae05b0bdf91e6c050ab`; the corresponding fresh hash is
`3b2a82869f3df86dcef2b41bbda76832`. Uncached update agrees with fresh, and
add_feature clears the stale subset cache. Immutable cached objects also agree
with fresh controls. The finding is scoped to cached=True with subsequent
mutation, not every pmapper calculation.

The inspected subset key contains feature IDs/tolerance; add_feature explicitly
clears cache while update/reload do not show the same invalidation. Please assess
clearing/versioning that state at all supported mutation boundaries and add
fresh-versus-warm regression controls. This proposal prescribes no backend,
patch, version floor or delivery schedule. No upstream code was modified.

Full evidence/driver: [analytical contract](pmapper_analytical_controls.md),
[case helper](../phmt_test_support/pmapper_controls.py), prospective source/input
identities and subsequent original receipts. There are no molecular inputs,
activity labels or timing/performance claims.

## Separate integration observation

get_fp changes Python's module-global RNG state through random.seed. This was
observed under a fixed state and restored by our task-owned child afterward.
It is a reproducibility/isolation concern to assess, not evidence of an incorrect
fingerprint or the same cache defect. A separate local Random instance could
avoid application-state coupling, subject to upstream compatibility review.

## Publication boundary

No external issue, comment, PR or provider patch is sent. The mandatory
[external-publication rule](../MOLSYSSUITE_GUIDE.md#human-approval-for-external-issues-and-pull-requests)
requires prior explicit permission from Diego or Liliana before publishing in
this non-UIBCDF repository. The current source study/experiment authorizes this
reviewable UIBCDF report; it grants no external publication authority. PHMT
adopts no pmapper cache/index or runtime dependency as a workaround.
