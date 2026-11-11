# Store and assemble native feature evidence

Development source toward 0.6.0 can retain [native feature payloads](native_feature_payloads.md)
in writer-owned archives. Explicit `native-classical-v1` selects native archive
v2. Historical `snapshot-study-v1` archives keep their original format; copying
between profiles or mixing them is refused.

The same public writer stages immutable candidates, publishes against an exact
expected current generation, and retains interrupted operation history. Record
factories preserve original bytes and declared producer/source metadata. They
perform no new extraction or molecular preparation.

## Save captured inventories

First run the [standalone payload example](native_feature_payloads.md), which
creates `native-feature.json` from the small analytical archive. This example
deliberately assigns two work keys to the same captured inventory: repeated
evidence is not another molecule or independent support.

```python
from pathlib import Path
from pharmacophoremt_features import (
    FeatureAssetRecord, FeatureAssetStore, FeatureAssetView, FeatureInventoryPayload,
)

payload = FeatureInventoryPayload.from_bytes(
    Path("native-feature.json").read_bytes(), payload_profile="native-classical-v1",
)
first = FeatureAssetRecord.from_payload("first", payload)
repeat = FeatureAssetRecord.from_payload("repeat=α", payload)
with FeatureAssetStore.create(
    "native-archive", payload_profile="native-classical-v1",
) as store:
    candidate = store.stage_records([first, repeat])
    store.publish(candidate, expected_current=None)

with FeatureAssetView.open("native-archive") as view:
    print(view.summary()["record_count"])  # 2
    print(view.summary()["unique_payload_count"])  # 1
```

`stage_records` accepts an explicit bounded list or tuple. Work keys must be
unique; source/occurrence keys remain literal. Ready payloads are validated
afresh at staging and publication. Creation refuses an existing destination.
The caller owns all views and writer lifetimes.

## Select a subset while preserving its old position

A record borrowed from a view retains its source generation, global ordinal,
literal identities and original record digest. Default staging preserves its
most recent source position. Moving it requires explicit consent and keeps the
old position in its lineage.

```python
with FeatureAssetView.open("native-archive") as view:
    previous = view.generation
    selected = FeatureAssetRecord.from_view(
        view, 1, expected_generation=previous,
    )

with FeatureAssetStore.open("native-archive") as store:
    subset = store.stage_records(
        [selected], ordinal_policy="explicit-rebase@1",
    )
    store.publish(subset, expected_current=previous)

with FeatureAssetView.open("native-archive") as view:
    row = view.work_items()["records"][0]
    print(row["work_ordinal"])  # 0: destination position
    print(row["lineage"][-1]["work_ordinal"])  # 1: retained original position
    print(view.snapshot_bytes(0) == payload.to_bytes())  # True
```

Omitting `explicit-rebase@1` here refuses the move. Whole-generation
`store.stage(view, expected_generation=...)` retains every row, lineage, position
and original payload within the same profile. A borrowed record survives source
view closure. No operation silently renames a borrowed work/source/occurrence key
or trims earlier lineage. At most 16 source anchors per record are retained.

## Reconstruct explicitly and inspect publication

Native-v2 views structurally check native metadata while keeping quantity
decoding separate. This works without activating the scientific stack. Explicit
reuse validates every original native field and preserves retained lineage.

```python
from pharmacophoremt.screening import reuse_feature_inventories

with FeatureAssetView.open("native-archive") as view:
    print(view.summary()["quantity_semantics_checked"])  # False
    restored = reuse_feature_inventories(
        view, ["hb donor"], expected_generation=view.generation,
        payload_profile="native-classical-v1",
    )["inventories"][0]
    print(restored["lineage"][-1]["work_ordinal"])  # 1
    print(restored["inventory"].get("attribution") == native.get("attribution"))

with FeatureAssetStore.open("native-archive") as store:
    last = store.attempts()[-1]
    print(store.inspect_recovery(last["attempt"])["decision"]["action"])
```

The final two values are `True` and `already_current`. Here `native` is the
original inventory from the prerequisite standalone example. Reconstruction and
archive operations preserve original references without registering another
extraction. Recovery inspection is metadata only; an eligible linked retry is
explicit and revalidates before publication, as in the [writer guide](feature_archive_writing.md).

Use `FeatureAssetRecord.incomplete(..., status=..., cause=...)` to retain explicit
failed, partial, unsupported or unattempted evidence. Such records have no payload;
they remain inspectable in staged candidates and refuse publication. An evaluated
empty family in a complete native payload remains distinct from missing work.

The first local POSIX profile admits 64 records, 8 MiB repeated original input,
4 MiB unique payloads, 8 MiB generation bytes and 64 attempts per store. Larger
collections, mixed-format migration, source authentication and biological/human/
scale qualification remain separate. See the [public API](../../api/users/api_users.rst)
for record factories, explicit assembly, reading and writer recovery operations.
