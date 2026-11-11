# Preserve a captured native feature inventory

Development source toward 0.6.0 provides `FeatureInventoryPayload`: encode an
already captured inventory, retain its original references, and reconstruct it
later with fresh quantity and geometry validation. The explicit profile is
`native-classical-v1`. It supports all six classical families in one frame.

For a new extraction, the [capture route](feature_capture.md) retains the effective
request and original extraction observation automatically. For an inventory you
already have, you must supply the families actually evaluated. An empty evaluated family is
valid evidence; an unrequested family remains unknown. Encoding does not perform
extraction or verify a molecule's current state. Keep the original extraction
producer, even when unknown, separate from the newly observed serializer.

## Save an inventory you already captured

This complete example starts with the [small analytical archive download](feature_archives.md),
unpacked in the current directory. It reconstructs one original inventory through
the [historical compatibility reader](native_feature_reuse.md), then serializes
that inventory in the new standalone format. A newly captured
`modeler.get_features()` result can be supplied to the same producer with its
actual evaluation/source declarations and original producer information.

```python
from pathlib import Path
from pharmacophoremt.screening import reuse_feature_inventories
from pharmacophoremt_features import FeatureAssetView, FeatureInventoryPayload

with FeatureAssetView.open("feature-archive-example") as view:
    captured = reuse_feature_inventories(
        view, ["hb donor"], expected_generation=view.generation,
        payload_profile="snapshot-study-v1", work_keys=["nm"],
    )["inventories"][0]

original = captured["extraction"]
parent = {
    key: original["parent"][key]
    for key in (
        "source_key", "occurrence_key", "artifact_sha256",
        "artifact_bytes", "n_atoms", "preparation",
    )
}
parent["mapping_policy"] = "caller-declared-local-atom-axis@1"
payload = FeatureInventoryPayload.from_inventory(
    captured["inventory"], original["requested_families"],
    parent=parent, extraction_producer=original["producer"],
    payload_profile="native-classical-v1",
)
Path("native-feature.json").write_bytes(payload.to_bytes())
print(payload.describe()["parent"]["source_key"])
```

The source key prints `nm` literally. The declaration refers to the original
local atom axis; selected subsets retain their original indices and order.
Provide `artifact_sha256=None` and `artifact_bytes=None` together when those
facts are unknown, and `extraction_producer=None` when the original producer
is unknown. These choices remain explicit unknowns. None authenticates a source.
The caller owns the output file; the example writes a newly chosen local file.

## Inspect first, then reconstruct explicitly

The next block uses the file just written. Importing `pharmacophoremt_features`,
parsing bytes and describing them work without importing the scientific stack.
Native reconstruction is a separate operation and checks every retained feature,
including families beyond the required coverage check.

```python
from pathlib import Path
from pharmacophoremt_features import FeatureInventoryPayload

saved = FeatureInventoryPayload.from_bytes(
    Path("native-feature.json").read_bytes(),
    payload_profile="native-classical-v1",
)
info = saved.describe()
print(info["quantity_semantics_checked"])
native = saved.to_inventory(required_families=["hb donor"])
print(native["selected_atom_indices"] == captured["inventory"]["selected_atom_indices"])
print(native.get("attribution") == captured["inventory"].get("attribution"))
print(saved.to_bytes() == payload.to_bytes())
```

The output is `False`, then three `True` values. Metadata never becomes a
scientific validation flag after reconstruction. Every native read verifies
sealed quantity fields/units, geometry, participant/geometry maps and charge
signs afresh. Each read returns independent objects. It preserves original
recognition/attribution without registering another extraction or adding credits.

This bounded profile admits at most 256 source atoms, 64 features and 2 MiB per
payload, with bounded finite JSON provenance. It refuses unsupported definitions,
included-volume features, incomplete records and invalid or missing scientific
fields. Use the [public API](../../api/users/api_users.rst) for all operations.
The [native-v2 archive guide](native_feature_archives.md) shows explicit native
record assembly with retained source ordinals; the historical
[archive writer](feature_archive_writing.md) keeps its original whole-generation
profile. These development increments publish no package or new tag.
