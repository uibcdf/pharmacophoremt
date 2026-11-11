# Inspect saved feature evidence

`pharmacophoremt_features.FeatureAssetView` reads saved feature evidence without
importing the scientific stack. It belongs to the PharmacophoreMT distribution.
Use a build containing this new reader; public-channel/platform qualification is
still tracked in [#23](https://github.com/uibcdf/pharmacophoremt/issues/23).
It is not a separate package installation.

The reader verifies metadata and original-byte integrity. Coverage and counts are
producer declarations. Original payloads remain opaque: opening an archive does
not validate quantities, authenticate its molecular source or perform screening.

## Open one generation and inspect a page

Download the [small analytical example](../../_static/examples/feature_archive_example.zip)
and extract it into your working directory. It contains eleven declared work
occurrences and original analytical captures, with no activity labels or biological
validation. The archive data is an example, not a public compound collection.

```python
from pharmacophoremt_features import FeatureAssetView

with FeatureAssetView.open("feature-archive-example") as features:
    summary = features.summary()
    print(summary["record_count"])  # 11
    print(features.generation)

    page = features.work_items(
        work_keys=["repeat=α", "1 nm", "nm"], offset=1, limit=1
    )
    print(page["selected_count"])  # 3, not just this page's row count
    print(page["records"][0]["work_ordinal"])  # 6, the original global position
```

Opening resolves the current generation once. The view keeps it even if a producer
later publishes another generation. Reopen explicitly to choose the new one, or
pass `generation=<saved SHA-256>` to open the older generation. An unreadable or
missing archive raises an error; opening never creates or repairs one.

Keys are literal. `"nm"`, `"1 nm"` and `"repeat=α"` remain distinct keys, and leading
spaces are not removed. Selection follows the original manifest order. None
selects all work; an empty key list selects none. Unknown/duplicate keys refuse.
A zero page limit returns no rows with the full selected count; it does not mean
there are no selected occurrences.

## Distinguish empty evaluation from missing evaluation

```python
with FeatureAssetView.open("feature-archive-example") as features:
    aromatic = features.inspect(["aromatic ring"], work_keys=["empty:nm"])
    print(aromatic["records"][0]["declared_counts"])  # {"aromatic ring": 0}

    donor = features.inspect(["hb donor"], work_keys=["empty:nm"])
    print(donor["records"][0]["unobserved_families"])  # ["hb donor"]
    print(donor["decision"]["message"])
```

An aromatic-only empty request did not evaluate donors. Request missing evaluation
explicitly through a qualified capture route. Completed declared coverage still
needs original payload/quantity/geometry validation before scientific reuse; this
reader supplies no native decoder or query admission.

Failed, partial, unsupported and unattempted occurrences retain their original
cause. They are not replaced by empty features. Inspect their metadata before
requesting new work. The view also distinguishes a complete selected subset from
an incomplete manifest.

## Retain original bytes and close

```python
with FeatureAssetView.open("feature-archive-example") as features:
    original_bytes = features.snapshot_bytes(1)  # global manifest ordinal
```

These are exact original opaque bytes. Preserve their format/provenance and use
an explicitly qualified decoder to interpret them. They may contain geometry or
private producer data; requesting them does not register new scientific credit.
Returned bytes/pages remain usable after close. Further view operations refuse,
and closing one view never closes another caller's resources.

The first profile is bounded: at most4096records,8 MiB generation JSON,4 MiB unique
original bytes and2 MiB per original. Limits apply together. This is saved-evidence
inspection, with no public writer, index, large-library performance or biological
prediction claim. Full metadata/format scope is in the
[format contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/feature_archive_format.md).
