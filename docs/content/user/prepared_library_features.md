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
Open readers keep their original generation. The following continuation connects
the retained query to a recoverable prepared-input screening run.
This finite example supplies no general PubChem connector, provider-owned
molecular collection, search index, speed measurement or biological validation.

## Screen prepared placements with a retained query

Choose one reconstructed model deliberately. Here the last model describes the
repeated caffeine occurrence; the repeat supplies no additional independent
evidence. The query retains all five captured caffeine features under the
constructor's essential, equal-weight convention. Curate a different hypothesis
through the [public curation tools](../cookbook/pharmacophore_curation.md) when
those assumptions do not express your question.

This continuation evaluates the supplied coordinates in their fixed frame. It
does not align molecules, generate conformers or search alternative placements.
The matching caffeine pose is a consistency control, not independent validation.
For another question, select the appropriate [prepared screening method](chemical_libraries.md)
and record its settings in a separate run.

Saved features construct the query without another extraction. Candidate
evaluation still reads the unchanged prepared molecules and performs native
recognition and matching. This is not candidate screening entirely from cache.

```python
from contextlib import closing
from pharmacophoremt.screening import (
    PreparedInput, PreparedScreeningRun, build_prepared_run_plan,
)
from pharmacophoremt_results import ScreeningRunView

screening_records = inputs + [dict(inputs[-1], work_key="repeat:last")]
query_path = Path("retained-query.json")
phmt.io.to_json(models[-1], str(query_path))
plan = build_prepared_run_plan(
    str(query_path), screening_method="placed", score_method="checked_pose_coverage",
    compatibility={
        "prepared_snapshot": parents,
        "preparation": [row["preparation"] for row in inputs],
        "features": {"archive_generation": original_generation, "payload_profile": profile},
        "index": None,
        "grouping": "original work/source/occurrence keys; repeat is not independent",
        "numerical": "unchanged supplied coordinates; native matching defaults",
    },
    evaluation_options={"structure_index": 0, "chemical_state": 0},
    on_error="record",
)
print(plan.describe())


def screening_entries(records):
    for row in records:
        path = Path(row["path"])
        raw = path.read_bytes()
        if len(raw) != row["bytes"] or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise ValueError("Prepared input differs from its receiving record")
        yield PreparedInput(
            **{key: row[key] for key in ("work_key", "source_key", "occurrence_key")},
            molecular_system=msm.h5msm.read(str(path)),
        )
```

The plan admits query/settings before manifest creation or candidate loading.
Compatibility fields are producer declarations, not molecular authentication.
Use fresh destinations; writers refuse existing files.

## Stop and resume the saved run

```python
manifest_path = Path("screening-work.jsonl")
run_path = Path("screening.sqlite3")
with manifest_path.open("x", encoding="utf-8") as manifest:
    for row in screening_records:
        mapping = {key: row[key] for key in ("work_key", "source_key", "occurrence_key")}
        manifest.write(json.dumps(mapping, sort_keys=True, separators=(",", ":")) + "\n")

with PreparedScreeningRun.create(
    str(run_path), plan=plan, manifest_path=str(manifest_path),
    run_id="retained-query:placed:1",
) as run:
    entries = screening_entries(screening_records)
    with closing(entries), closing(run.resume(entries)) as outcomes:
        first = next(outcomes)

with ScreeningRunView.open(str(run_path)) as view:
    print(view.progress())
```

The first result is committed before delivery. Closing the iterator stops further
work. In the original four-work example, one outcome is confirmed and three remain
pending. Reopen the same compatible plan and replay the declared sequence:

```python
with PreparedScreeningRun.open(
    str(run_path), plan=plan, manifest_path=str(manifest_path),
) as run:
    entries = screening_entries(screening_records)
    with closing(entries), closing(run.resume(entries)) as outcomes:
        newly_confirmed = list(outcomes)

with ScreeningRunView.open(str(run_path)) as view:
    print(view.progress())
    print(view.summary(score_method="checked_pose_coverage@1"))
    jsonl_receipt = view.to_jsonl("screening-outcomes.jsonl")
    csv_receipt = view.to_csv("screening-outcomes.csv")
```

The continuation confirms three new outcomes; saved results contain all four.
Replaying completed work may reopen its input but does not evaluate it again.
Each result preserves native status and coverage: positive coverage alone need
not satisfy every essential site. Scores are geometric coverage, not affinity.

Input integrity or reader failures propagate and preserve prior confirmations;
they do not become negative scores. Restore the admitted unchanged inputs before
resuming. Recorded native evaluation failures remain terminal and unscored in
that run; a deliberate retry uses a new linked run. Changed query, settings or
compatibility also require a new run. See the [recovery contract](../cookbook/recoverable_prepared_screening.md)
for attempt history and publication-failure behavior.

## Inspect and export without the original inputs

After closing the writer, `ScreeningRunView` and the standalone results CLI can
inspect/export the saved database without PHMT/MolSysMT scientific imports,
the original molecules or the feature archive. Reading performs no recognition
or matching and grants no new calculation credit:

```bash
python -m pharmacophoremt_results screening.sqlite3 --summary
python -m pharmacophoremt_results screening.sqlite3 --to-csv another-export.csv
```

Export the complete saved view rather than only `newly_confirmed`. Repeated work
retains its original source/occurrence keys; four work items are still three
original molecules. Each export requires a fresh destination and retains its own
publication receipt. Actual independent human usability, biological accuracy,
large-library performance and public-package qualification remain separate.
