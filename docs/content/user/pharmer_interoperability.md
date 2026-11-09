# Reading Pharmer queries

Read a saved query with `pharmacophoremt.io.load("query.json")`, or pass its decoded
mapping to `io.from_pharmer(data)`. The constructor
`Pharmacophore("query.json", form="pharmer")` uses the same default reader.

## Review what the import preserves

The reader warns when it cannot preserve a scientific constraint. Ask for a
report to see the affected fields and the decisions for each imported point:

```python
import pharmacophoremt as phmt

model, report = phmt.io.load("query.json", return_report=True)
print(report["losses"])
print(report["ignored_fields"])
print(report["unapplied_settings"])
```

| Policy | Behavior |
| --- | --- |
| `on_loss="warn"` (default) | Warn once and return the supported compatibility projection |
| `on_loss="raise"` | Refuse a lossy import before constructing the model or converting an attached molecule |
| `on_loss="ignore"` | Explicitly accept the compatibility projection without the loss warning; retain its audit |

For a query whose constraints must all be preserved, use
`phmt.io.load("query.json", on_loss="raise")`. Fix or review the reported fields
before screening. Accepting losses does not admit malformed geometry, unknown
feature names or invalid field values. The constructor uses `warn`; use the
reader/facade for explicit expert options.

The report has schema `pharmacophoremt.pharmer-import@1`. It records site mappings,
field paths and loss reasons, with the source length unit and native assumptions.
It does not retain the original molecule or session payload. Imports with losses
or engine settings also store an independent copy in
`model.metadata["pharmer"]["import_report"]`; native PHMT JSON persistence keeps
that audit, even after explicit `ignore`.

## Enabled points and directions

| Original point field | Result |
| --- | --- |
| `"enabled": true`, or no `enabled` field | Import the supported point |
| `"enabled": false` | Omit before reading feature, geometry or other point constraints |
| Another enabled value, such as `"false"`,0 or null | Structured type error identifying the point |
| `"vector_on": false` or 0 | Undirected sphere; inactive vector payload is ignored |
| True/1, or absent activation with one vector | Preserve direction for aromatic, donor and acceptor points |
| No vector and no explicit activation | Undirected sphere |
| Explicit activation without a vector; multiple active alternatives | Refuse rather than invent or select a direction |

`hasvec` and `selected` are display annotations. A disabled point does not become
an optional weighted site. Surviving points keep their input order and receive
compact site indices. If every point is disabled, the model is empty; individual
evaluation tools retain their own minimum-query requirements.

When omission or an import audit adds a `pharmer` metadata namespace, it contains:

- `source_point_indices`: original zero-based JSON positions in result-site order;
- `disabled_point_indices`: original zero-based positions omitted.

For three points with the first disabled, those lists are `[1, 2]` and `[0]`.
They identify supplied query points, not molecular atoms or authenticated source
provenance. The mapping survives native persistence. Ordinary lossless imports
without omissions or engine settings keep empty metadata; request a report to
inspect their point mappings and ignored annotations.

## Scientific and compatibility limits

Required points are preserved. Optional and negated (`notpresent`) requirements
are reported as losses: the compatibility model still treats those imported
sites as essential. Nonneutral feature-size/count restrictions, directions on
unsupported feature roles and unknown fields also produce loss reports. Known
engine/library/search settings are listed as unapplied; nonempty/non-null values
produce losses. Importing a model does not execute those settings or select a
chemical library. Known display/session annotations are listed separately.

Coordinates and radii are angstroms; their physical meaning follows the active
PyUnitWizard policy. Inspect quantities with an explicit target unit. Attached
ligand conversion belongs to MolSysMT. Angular tolerances belong to the chosen
evaluator, and rigid triplet search still requires at least three non-collinear
essential centers.

The bundled query has19 points but only10 enabled constraints. Reimporting now also
honors inactive stored vectors. Previously saved native models and screening
results keep their original contents; reimport the original query to apply these
corrections. Original input mappings and files are not changed.

This reader does not run Pharmer or certify equivalent feature perception,
directional/search policy or lossless export. The
[P1 analytical comparison](../validation/pharmer_p1.md) retains its separately
unexecuted external arm. Current evidence and the exact admission profile are
linked from the [developer contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/pharmer_interoperability.md).
