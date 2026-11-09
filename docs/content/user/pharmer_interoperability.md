# Reading enabled Pharmer query points

Use `pharmacophoremt.io.load("query.json")` to read a Pharmer JSON query, or
call `io.from_pharmer(data)` with its decoded mapping. The constructor route
`Pharmacophore("query.json", form="pharmer")` uses the same reader.

The point-level `enabled` field controls whether a point is imported:

| Original JSON point | Result |
| --- | --- |
| `"enabled": true` | Import the supported feature and geometry |
| `"enabled": false` | Omit the point before reading feature or geometry |
| No `enabled` field | Import as enabled |
| Another value, such as `"false"`, `0` or `null` | Raise `ArgumentTypeError` / `PHMT-E109`, identifying the point and field |

This is point omission. A disabled point does not become an optional weighted
site. Surviving points retain their original order and receive compact result
site indices. If every point is disabled, the reader returns an empty model;
individual modeling/evaluation tools retain their own query requirements.

## Trace result sites to the original query

When points are omitted, `model.metadata["pharmer"]` contains two lists:

- `source_point_indices`: original zero-based JSON positions, in result-site order;
- `disabled_point_indices`: original zero-based positions that were omitted.

For a three-point query whose first point is disabled, the imported model has
two sites. Its mapping is `[1, 2]` and its disabled list is `[0]`. These positions
identify points in the supplied JSON, not molecular atoms or authenticated source
provenance. The mapping survives native PHMT JSON persistence.

```python
import pharmacophoremt as phmt

model = phmt.io.load("query.json")
print(model.n_interaction_sites)
mapping = model.metadata.get("pharmer")
if mapping is not None:
    print(mapping["source_point_indices"])
```

All-enabled and missing-flag imports keep their previous ordinary outputs;
the reader adds this metadata only when omissions occur. Original input mappings
and files are not changed. The bundled example contains 19 points with only 10
enabled, so its query now imports 10 sites instead of incorrectly requiring all 19.

Previously saved native PHMT models and screening results keep their stored
content. Reimport the original Pharmer query to apply this correction; do not
silently reinterpret an older saved model or its original screening evidence.

## Units and compatibility limits

Pharmer coordinates and radii are interpreted as angstroms. The reader preserves
their physical meaning under the application's PyUnitWizard policy; inspect
values with an explicit target unit. Attached-ligand conversion is delegated to
MolSysMT. Rigid triplet search still needs at least three non-collinear essential
centers after omission.

This reader does not run the Pharmer engine. The enabled-point correction does
not certify optional/negated, size, vector-activation, engine search-limit or
bidirectional interchange semantics. Their supported-input and loss/refusal
policy is tracked in [#163](https://github.com/uibcdf/pharmacophoremt/issues/163).
Keep the [P1 analytical case](../validation/pharmer_p1.md) and its unexecuted
external arm separate from general interoperability or performance claims.
