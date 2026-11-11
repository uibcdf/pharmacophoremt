# Capture features with their evaluation provenance

Development source toward 0.6.0 adds `modeler.capture_features`. It extracts once
and retains the families actually evaluated, their counts, the resolved local
atom/frame/state maps and the observed original extraction software. Use it when
you want to save a new inventory without declaring the evaluated families again.
An evaluated family with no features remains distinct from an unrequested family.

## Extract and save

This complete analytical example uses two prepared ions with explicit coordinates.
For your own work, supply an unchanged prepared MolSysMT-compatible source.
MolSysMT owns molecular preparation and access. No protonation, repair or conformer
generation occurs in feature capture.

```python
from pathlib import Path
import molsysmt as msm
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt_features import FeatureInventoryPayload

prepared = msm.convert(
    msm.convert("smiles:[Na+].[Cl-]", to_form="rdkit.Mol"),
    to_form="molsysmt.MolSys",
)
prepared.structures.append(
    coordinates=puw.quantity([[[0, 0, 0], [.5, 0, 0]]], "nm"),
)
capture = phmt.modeler.capture_features(
    prepared, features=["positive charge", "negative charge", "hb donor"],
)
parent = {
    "source_key": "two-ions", "occurrence_key": "two-ions:0",
    "artifact_sha256": None, "artifact_bytes": None, "n_atoms": 2,
    "preparation": "caller-prepared analytical coordinates; no repair",
    "mapping_policy": "caller-declared-local-atom-axis@1",
}
payload = FeatureInventoryPayload.from_capture(
    capture, parent=parent, payload_profile="native-classical-v1",
)
Path("captured-features.json").write_bytes(payload.to_bytes())
print(len(capture["inventory"]["features"]))
print(capture["evaluation"]["coverage"]["hb donor"]["status"])
```

The output is `2` and `evaluated_empty`. The ordinary native inventory is
`capture["inventory"]`, usable by existing modeling tools. `get_features()` keeps
its existing result contract. Historical inventories use the explicit
[`from_inventory` route](native_feature_payloads.md); their effective request
cannot be inferred from feature presence.

Parent identity and preparation remain caller declarations. Unknown file identity
is explicit above; a capture does not authenticate a molecule or reserve its state
against concurrent changes. Keep the prepared source unchanged throughout capture.

## Inspect and reconstruct

```python
saved = FeatureInventoryPayload.from_bytes(
    Path("captured-features.json").read_bytes(),
    payload_profile="native-classical-v1",
)
info = saved.describe()
print(info["extraction_producer"]["evaluation"] == capture["evaluation"])
native = saved.to_inventory(required_families=["positive charge", "hb donor"])
print(native["selected_atom_indices"] == capture["inventory"]["selected_atom_indices"])
print(saved.to_bytes() == payload.to_bytes())
```

All three outputs are `True`. Metadata inspection is scientifically cold; native
reconstruction checks every quantity and map afresh. Capture and serialization
observe their own software separately. Neither reading nor serialization performs
another extraction or registers another extraction credit. To retain optional
original scientific references, call capture inside `with phmt.attribution():`;
the application's Ackredit session remains authoritative.

## Compose a public archive

The same payload can become a native archive record. This block creates a new
local directory and uses the existing guarded publication route.

```python
from pharmacophoremt_features import FeatureAssetRecord, FeatureAssetStore, FeatureAssetView

record = FeatureAssetRecord.from_payload("ions:0", payload)
with FeatureAssetStore.create("captured-feature-store", payload_profile="native-classical-v1") as store:
    generation = store.stage_records([record])
    store.publish(generation, expected_current=None)
with FeatureAssetView.open("captured-feature-store") as view:
    reused = phmt.screening.reuse_feature_inventories(
        view, ["positive charge"], expected_generation=view.generation,
        payload_profile="native-classical-v1",
    )["inventories"][0]
    print(reused["work_ordinal"])
    print(view.snapshot_bytes(0) == payload.to_bytes())
```

The output is `0` and `True`. See [native archives](native_feature_archives.md) for
subset assembly and original ordinal lineage, and [archive writing](feature_archive_writing.md)
for publication attempts and linked recovery.

## Expert argument controls

Ordinary calls validate and normalize arguments. Development source also exposes
keyword-only `skip_digestion=False` on `get_features` and
`FeatureInventoryPayload.from_inventory`, matching the explicit control on the
capture operations. Use True only when your application already supplies canonical
arguments. The following block continues with `prepared` and `parent` from above:

```python
families = ["hb donor", "positive charge", "negative charge"]
inventory = phmt.modeler.get_features(
    prepared, features=families, skip_digestion=True,
)
expert_payload = FeatureInventoryPayload.from_inventory(
    inventory, families, parent=parent, extraction_producer=None,
    payload_profile="native-classical-v1", skip_digestion=True,
)
restored = expert_payload.to_inventory(required_families=families)
print(len(restored["features"]))
print(expert_payload.describe()["coverage"]["hb donor"]["count"])
```

The outputs are `2` and `0`. Unknown original extraction software remains None;
use `capture_features` when you need its observed evaluation/producer evidence.
True skips argument digestion for that call only. It keeps native profile, unit,
geometry, mapping, coverage and resource checks active, and nested public tools
keep their own validation. For example, supply a list of canonical family names
in bypass mode; the ordinary scalar-name normalization is skipped. There is no
measured performance claim for this control.

The complete [public API](../../api/users/api_users.rst) exposes all operations.
`capture_features` accepts the existing `selection`, `structure_index`,
`chemical_state` and `features` choices. Effective families use canonical order;
duplicates mean one evaluation. Included-volume captures are complete native
inventories, but the classical payload refuses every included-volume evaluation,
including an empty one. Choose only supported families when saving this profile.

This first capture admits 1–256 total source atoms, at most 64 features and 2 MiB
of sealed observation, with bounded finite metadata. Oversized input is refused
before extraction; failed extraction returns no successful capture. The digest
binds the original content and detects later edits, with fresh validation at
encoding. It is neither a signature nor a scientific validation passport. The
runtime envelope contains native quantities: persist through the payload writer,
rather than JSON-encoding the envelope or using pickle. These development
capabilities do not establish biological accuracy, scale or full public delivery.
