"""Explicit one-shot study export; not a supported writer/publication API."""

import base64
import hashlib
from pathlib import Path

from pharmacophoremt_features import FeatureAssetView
from pharmacophoremt_features._schema import (
    GENERATION_SCHEMA,
    MARKER,
    PROFILE,
    STORE_SCHEMA,
)
from pharmacophoremt_results import canonical_json
from phmt_test_support.feature_snapshot import SCHEMA as SNAPSHOT_SCHEMA
from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
from phmt_test_support.feature_store import SCHEMA as STUDY_SCHEMA
from phmt_test_support.feature_store import FeatureStoreReaderStudy


def export_study_feature_archive(source, destination, *, generation=None):
    """Create a distinct metadata archive while retaining original payload bytes.

    Original snapshot validation is owned by the study reader. The public view
    subsequently validates only its declared metadata and opaque byte integrity.
    This builder refuses any existing destination; interrupted output is retained
    for inspection. It promises no transactional/public writer or recovery route.
    """
    rows, payloads = [], {}
    with FeatureStoreReaderStudy(source, generation) as original:
        source_generation = original.describe()["generation"]
        for entry in original.entries():
            row = {
                k: entry[k]
                for k in ("work_key", "source_key", "occurrence_key", "status")
            }
            if row["status"] == "ready":
                raw = entry["snapshot"]
                description = FeatureSnapshotStudy(raw).describe()
                digest = hashlib.sha256(raw).hexdigest()
                row.update(
                    payload_sha256=digest,
                    extraction={
                        "definition": description["request"]["definition"],
                        "requested_families": description["request"]["features"],
                        "coverage": description["coverage"],
                        "parent": description["parent"],
                        "producer": description["producer"],
                    },
                )
                payloads[digest] = {
                    "format": SNAPSHOT_SCHEMA,
                    "data": base64.b64encode(raw).decode("ascii"),
                }
            else:
                row["cause"] = entry["cause"]
            rows.append(row)
    bundle = {
        "schema": GENERATION_SCHEMA,
        "profile": PROFILE,
        "origin": {
            "format": STUDY_SCHEMA,
            "generation": source_generation,
            "policy": "explicit-study-evidence-export@1",
        },
        "records": rows,
        "payloads": payloads,
    }
    raw = canonical_json(bundle).encode()
    identity = hashlib.sha256(raw).hexdigest()
    destination = Path(destination)
    destination.mkdir()
    (destination / "generations").mkdir()
    for path, value in (
        (destination / "STORE.json", canonical_json(MARKER).encode()),
        (destination / "generations" / (identity + ".json"), raw),
        (
            destination / "CURRENT",
            canonical_json(
                {"schema": STORE_SCHEMA, "generation": identity, "bytes": len(raw)}
            ).encode(),
        ),
    ):
        with path.open("xb") as stream:
            stream.write(value)
    with FeatureAssetView.open(destination) as view:
        assert view.generation == identity
        return view.summary()
