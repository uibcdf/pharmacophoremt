# Reuse saved native features

This API is available in development source toward 0.6.0. Use a build containing
`screening.reuse_feature_inventories` with PyUnitWizard >=0.28.1. The 0.5.0 source
tag contains metadata/original-byte inspection only.

The operation reconstructs saved features without another molecular extraction.
It checks units, geometry, maps and the agreement between original payloads and
archive metadata. Historical producer versions and references remain original.

## Inspect, reconstruct and build a query

Download the [analytical example](../../_static/examples/feature_archive_example.zip)
and extract it as described in [feature-archive inspection](feature_archives.md).
This example is analytical data, not a public compound collection or biological
validation. Its original study payloads need explicit compatibility admission:

```python
from pharmacophoremt_features import FeatureAssetView
from pharmacophoremt import modeler
from pharmacophoremt.screening import reuse_feature_inventories

with FeatureAssetView.open("feature-archive-example") as features:
    preview = features.inspect(["hb donor"], work_keys=["nm"])
    restored = reuse_feature_inventories(
        features,
        ["hb donor"],
        expected_generation=features.generation,
        payload_profile="snapshot-study-v1",
        work_keys=["nm"],
    )

original = restored["inventories"][0]
print(original["work_ordinal"])  # 1: original global manifest position
query = modeler.from_feature_inventory(original["inventory"], radius="0.1 nm")
print(query.n_interaction_sites)  # 4: all captured features, including other families
```

Requiring donor coverage checks that donors were evaluated; it does not filter
the inventory to donors. Creating the query is a separate explicit operation.
Reconstruction alone does not admit a query, authenticate the molecular source
or evaluate a match. The returned data remains usable after closing the view.

## Compose the same operations for a selected batch

```python
with FeatureAssetView.open("feature-archive-example") as features:
    restored = reuse_feature_inventories(
        features,
        ["hb donor", "positive charge"],
        expected_generation=features.generation,
        payload_profile="snapshot-study-v1",
        work_keys=["repeat=α", "1 nm", "nm"],
    )
    print(restored["report"]["selection_ordinals"])  # [1, 6, 10]
```

Keys retain case, spaces and Unicode. Manifest order determines returned order.
Each call admits at most 64 occurrences and 8 MiB of original bytes, counting
repeated occurrences separately. Use metadata pages to select smaller batches.
Each call validates quantities afresh under the current application policy.

Missing family evaluation and incomplete extraction raise `FeatureAssetError`;
inspect the original cause before explicitly requesting replacement work. An
evaluated-empty inventory is valid but cannot supply a nonempty model. An empty
key list returns no inventories and claims no quantity validation. Errors do not
return a partially reconstructed batch or close the caller's view.

The compatibility profile supports only its declared historical single-frame
schema. [Public archive writing/recovery](feature_archive_writing.md) and
[native record assembly](native_feature_archives.md) are separate explicit
operations. General molecular collections and source authentication retain their
provider-owned acceptance gates. Public-channel/platform qualification stays tracked in
[#23](https://github.com/uibcdf/pharmacophoremt/issues/23).
