# Exchange pharmacophore fields with RDKit

Use explicit spheres when you want RDKit to retain each site's center and radius.
Request a field report to see what the conversion encodes and what it omits.

```python
import pharmacophoremt as phmt
from math import isclose
from pharmacophoremt.interaction_site import HBAcceptorSphere, HBDonorPoint

query = phmt.Pharmacophore()
query.add_interaction_site(HBDonorPoint("[1, 2, 3] angstrom"))
query.add_interaction_site(
    HBAcceptorSphere("[0.3, 0.4, 0] nm", "0.2 nm")
)
rd_query, report = phmt.io.to_rdkit(
    query, representation="spheres", return_report=True, on_loss="raise"
)
assert report["losses"] == []
assert rd_query.getRadius(0) == 0
assert isclose(rd_query.getRadius(1), 2.0)

restored, reading = phmt.io.load_rdkit(
    rd_query, radius=None, return_report=True, on_loss="raise"
)
assert reading["losses"] == []
assert restored.interaction_sites[0].shape_name == "point"
assert restored.interaction_sites[1].features == ["hb acceptor"]
```

Coordinates and explicit RDKit radii use angstroms. `radius=None` reads stored
explicit radii; zero produces a native Point. The reader's ordinary default
remains a fixed one-angstrom Sphere for every site. Passing another nonnegative
length sets every site's radius and records that assumption. Bounds between
pairs of features cannot determine individual radii.

| Choice | Result |
| --- | --- |
| `to_rdkit(query)` | The existing RDKit `Pharmacophore`: centers, families and ordinary initialized pair bounds; native radii are omitted and reported |
| `to_rdkit(query, representation="spheres")` | RDKit `ExplicitPharmacophore` with centers and per-site radii |
| `load_rdkit(rd_query)` | Native sites with the historical fixed one-angstrom radius assumption |
| `load_rdkit(rd_query, radius=None)` | Read each explicit radius; requires `ExplicitPharmacophore` |

The default `on_loss="warn"` emits one `PHMT-W103` warning if fields are omitted.
`on_loss="raise"` raises `PHMT-E110` before constructing a partial result.
`on_loss="ignore"` explicitly accepts the losses. With `return_report=True`, either
operation returns `(converted_object, report)`; otherwise it returns the object.
Reports are independent JSON-compatible mappings that you can inspect or save.

The six standard families map to donor, acceptor, aromatic, hydrophobic, positive
and negative native features. Multi-feature OR sites, unknown families and shapes
without a defined center are refused. Model names/provenance, metadata, nondefault
weights/essential flags and directional constraints have no complete RDKit field
mapping here. Gaussian sigma is not a sphere radius. A custom ExcludedVolume label
does not establish an executable exclusion in RDKit. A reader reports omitted
pair-bound constraints and nondefault feature types/identifiers. Keep the native
format when you need those complete original fields.

Strict field preservation does not establish equivalent screening or embedding.
The [analytical comparison](../validation/rdkit_bounds_comparison.md) explains
the demonstrated distance-filter and reflection/boundary differences. These
operations exchange already prepared pharmacophore fields; they do not perceive
features, prepare molecules or create new scientific attribution.
