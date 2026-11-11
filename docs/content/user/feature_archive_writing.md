# Retain and publish saved feature evidence

This development API adds a writer-owned local archive to the existing
[feature reader](feature_archives.md). Its first profile preserves **whole existing
generations**, including original positions, payload bytes, metadata and references.
Creating new payloads from live native inventories remains a later operation.
Use a build containing `FeatureAssetStore`; the 0.5.0 source tag has no writer.

## Save an existing generation in your own archive

Extract the [analytical example](../../_static/examples/feature_archive_example.zip)
into your working directory. It is a small feature-evidence example, not a compound
collection or biological benchmark.

```python
from pharmacophoremt_features import FeatureAssetStore, FeatureAssetView

with FeatureAssetView.open("feature-archive-example") as source:
    with FeatureAssetStore.create(
        "my-feature-archive", payload_profile="snapshot-study-v1"
    ) as store:
        candidate = store.stage(source, expected_generation=source.generation)
        print(store.current())  # None: the candidate is not published yet
        with store.view(generation=candidate) as preview:
            print(preview.summary()["record_count"])  # 11
            print(preview.payload_info(1)["work_ordinal"])  # 1
        store.publish(candidate, expected_current=None)
        print(store.current() == candidate)  # True
```

Creation refuses an existing destination. `open()` requires an existing writer-
owned archive; it never adopts or repairs an ordinary reader-only directory.
Staging validates all ready original quantities/maps but does not publish. An
incomplete candidate remains inspectable and cannot replace published evidence.
Publication validates again under the current unit policy and requires the exact
expected current generation. Explicit None means first publication.

Source views remain caller-owned. Whole manifests preserve their original global
ordinals; no selection is silently filtered or renumbered. Each candidate admits
at most 64 records and 8 MiB of repeated original bytes, within the reader's unique-
payload/document bounds. Each writer archive retains at most 64 operation attempts.
Keep full history; create an explicitly linked new archive when its quota is full.

## Inspect visibility before deciding on recovery

```python
with FeatureAssetStore.open("my-feature-archive") as store:
    last = store.attempts()[-1]
    recovery = store.inspect_recovery(last["attempt"])
    print(recovery["decision"]["action"])  # already_current
    print(recovery["candidate_native_validation_performed"])  # False
    if recovery["decision"]["action"] == "retry_available":
        store.retry_publication(last["attempt"])
```

A raised call or missing terminal receipt does not imply that publication was
rolled back. Inspection reports receipt state and actual current visibility
independently, and performs no scientific validation, write or retry. An explicit
eligible retry links the retained original attempt and uses the same publication
validator; earlier unknown/raised history stays original. Already current,
completed or displaced attempts refuse retry.

Inspect a completed published archive with ordinary `FeatureAssetView.open(...)`.
Readers need no writer lease, stay pinned to their opened generation and survive
writer closure. Metadata and recovery inspection import no scientific stack;
staging/publishing ready payloads explicitly activates quantity/native validation.
These operations preserve attribution without crediting another extraction and
do not authenticate the current molecular source or admit a query.

The first profile is for trusted local POSIX directories and cooperating writers.
It does not promise power-loss durability or distributed filesystem behavior.
Full supported/public/platform qualification remains separately tracked under
[#23](https://github.com/uibcdf/pharmacophoremt/issues/23).
