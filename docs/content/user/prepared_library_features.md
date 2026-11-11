# Reuse features from prepared library records

Capture features once, save them together, inspect their coverage and reconstruct
them for later model construction. This worked example uses the existing public
capture, payload and archive tools in development source toward 0.6.0.

The received case uses the three original prepared PubChem3D records: CIDs 1983,
2244 and 2519, one supplied conformer each. Their original files remain local
under the [pilot's publication limits](../validation/pubchem3d_library_pilot.md).
Use your authorized prepared files and their own receipt values when adapting the
example. Changed inputs form a new case with their own observations.

## Supply the prepared records

Create `prepared-records.json` as your application's input table. Each row carries
`work_key`, `source_key`, `occurrence_key`, `path`, `sha256`, `bytes`, `n_atoms`
and `preparation`. These are application metadata, not a new molecular format or
PHMT collection API. The path refers to an already prepared H5MSM file; obtain
hashes and preparation facts from your receiving process.

| Original case row | Source key | Occurrence key | Prepared atoms |
| --- | --- | --- | ---: |
| Acetaminophen, CID 1983 | `PubChemCID:1983` | `selected:0` | 20 |
| Aspirin, CID 2244 | `PubChemCID:2244` | `selected:1` | 21 |
| Caffeine, CID 2519 | `PubChemCID:2519` | `selected:2` | 24 |

This example uses a small finite table within the [native payload and archive
bounds](native_feature_archives.md). MolSysMT owns preparation and molecular
reading. Supplied state/H/aromaticity/coordinates are retained; no download,
chemical repair or conformer generation occurs here. Source labels are caller
declarations; file hashes bind bytes and do not authenticate chemical identity.

## Capture the requested families

```python
import hashlib
import json
from pathlib import Path
import molsysmt as msm
import pharmacophoremt as phmt
from pharmacophoremt_features import (
    FeatureAssetRecord, FeatureAssetStore, FeatureAssetView, FeatureInventoryPayload,
)

inputs = json.loads(Path("prepared-records.json").read_text())
families = [
    "hydrophobicity", "hb donor", "hb acceptor", "aromatic ring",
    "positive charge", "negative charge",
]
captures, parents = [], []
for row in inputs:
    path = Path(row["path"])
    original = path.read_bytes()
    if len(original) != row["bytes"] or hashlib.sha256(original).hexdigest() != row["sha256"]:
        raise ValueError("Prepared input differs from its receiving record")
    prepared = msm.h5msm.read(str(path))
    capture = phmt.modeler.capture_features(
        prepared, features=families, structure_index=0, chemical_state=0,
    )
    captures.append(capture)
    parents.append({
        "source_key": row["source_key"], "occurrence_key": row["occurrence_key"],
        "artifact_sha256": row["sha256"], "artifact_bytes": row["bytes"],
        "n_atoms": row["n_atoms"], "preparation": row["preparation"],
        "mapping_policy": "caller-declared-local-atom-axis@1",
    })
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
```

All requested families retain their evaluated counts, including zero. In the
original three-record case, acceptor counts are 2, 4 and 3; caffeine's donor
evaluation is empty. Those observations do not imply inactivity or affinity.

## Encode and publish one archive

```python
profile = "native-classical-v1"
payloads = [
    FeatureInventoryPayload.from_capture(capture, parent=parent, payload_profile=profile)
    for capture, parent in zip(captures, parents)
]
records = [
    FeatureAssetRecord.from_payload(row["work_key"], payload)
    for row, payload in zip(inputs, payloads)
]
records.append(FeatureAssetRecord.from_payload("repeat:last", payloads[-1]))
with FeatureAssetStore.create("prepared-library-features", payload_profile=profile) as store:
    original_generation = store.stage_records(records)
    store.publish(original_generation, expected_current=None)
```

The last row deliberately references the same caffeine occurrence and exact
payload. Four work records retain three unique payloads and three original source
occurrences. No new extraction occurs during encoding or publication.
Use a fresh destination; a failed publication keeps its recorded recovery state.

## Inspect coverage and reconstruct explicitly

```python
with FeatureAssetView.open("prepared-library-features") as view:
    print(view.summary()["record_count"], view.summary()["unique_payload_count"])
    donor = view.inspect(["hb donor"], work_keys=["repeat:last"])
    print(donor["records"][0]["declared_counts"]["hb donor"])
    restored = phmt.screening.reuse_feature_inventories(
        view, ["hb donor"], expected_generation=view.generation,
        payload_profile=profile,
    )["inventories"]
```

The original case prints `4 3` and `0`. The metadata inspection keeps quantities
unchecked and molecular origin unauthenticated. Explicit native reconstruction
validates every quantity, geometry and map afresh. Required families are a coverage
check: donor-only admission still returns the complete original inventories,
including caffeine's acceptors and aromatic features. No molecule is re-extracted.

## Build hypotheses from retained inventories

```python
models = [
    phmt.modeler.from_feature_inventory(
        row["inventory"], radius="0.15 nm", name=row["work_key"],
    )
    for row in restored
]
print([model.n_interaction_sites for model in models])
```

Every retained feature becomes a site under the constructor's essential,
equal-weight defaults. These are reference hypotheses for curation; this step
does not evaluate a compound against another query or establish activity.
Original source maps, geometry and references survive reconstruction. Model
construction has its own scientific attribution; saved reuse earns no new
extraction credit. Applications may enable [optional attribution](../cookbook/attribution.md).

For subsets and replacement, follow [explicit native rebasing](native_feature_archives.md#select-a-subset-while-preserving-its-old-position).
Open readers keep their original generation. Prepared-input screening and saved
run recovery remain separate [public workflows](chemical_libraries.md).
This finite example supplies no general PubChem connector, provider-owned
molecular collection, search index, speed measurement or biological validation.
