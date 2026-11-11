"""Scientific activation of explicitly selected, original captured inventories."""

from argdigest import arg_digest
from depdigest import dep_digest
from smonitor import signal

from pharmacophoremt._private.arg_digestion.feature_reuse import CONFIG
from pharmacophoremt_features import _schema
from pharmacophoremt_features._diagnostics import fail

MAX_REUSE_RECORDS = 64
MAX_REUSE_BYTES = 8 * 1024 * 1024


@signal(tags=["screening", "feature-reuse"])
@arg_digest(config=CONFIG, type_check=False)
@dep_digest("pyunitwizard")
def reuse_feature_inventories(
    view,
    required_families,
    *,
    expected_generation,
    payload_profile,
    work_keys=None,
):
    """Return complete captured inventories from an explicitly admitted profile.

    ``payload_profile='snapshot-study-v1'`` explicitly admits only the documented
    historical single-frame profile; native-classical-v1 selects native-v2 archives.
    No implicit cross-profile decoding, extraction, source
    authentication, query admission or writer is provided. Quantities, geometry
    and metadata bindings are revalidated on each call. The caller owns ``view``;
    this bounded eager operation never closes it and returns no partial batch.

    Keys are literal; None selects all, [] none. Returned order/global ordinals
    follow the original manifest, and all captured features remain in each native
    inventory. Recognition and attribution are detached original provenance, not
    recomputed scientific quantities or new extraction credit. The generation
    identifies the pinned archive, not the current molecular source.
    """
    if view.generation != expected_generation:
        fail(308)
    native_profile = payload_profile == _schema.NATIVE_PAYLOAD_PROFILE
    expected_schema = (
        _schema.NATIVE_GENERATION_SCHEMA
        if native_profile
        else _schema.GENERATION_SCHEMA
    )
    if view.summary()["schema"] != expected_schema:
        fail(336)
    preview = view.inspect(required_families, work_keys=work_keys)
    action = preview["decision"]["action"]
    if action == "resolve_incomplete_extraction":
        fail(306)
    if action == "evaluate_missing_families":
        fail(309)
    if preview["selected_count"] > MAX_REUSE_RECORDS:
        fail(313)
    originals, total = [], 0
    for row in preview["records"]:
        raw = view.snapshot_bytes(row["work_ordinal"])
        total += len(raw)
        if total > MAX_REUSE_BYTES:
            fail(313)
        originals.append(raw)
    rows = []
    for row, raw in zip(preview["records"], originals):
        if native_profile:
            from pharmacophoremt_features import FeatureInventoryPayload

            payload = FeatureInventoryPayload.from_bytes(
                raw, payload_profile=payload_profile
            )
            if _schema.encoded(payload.describe()) != _schema.encoded(
                row["extraction"]
            ):
                fail(310)
            native = payload.to_inventory(required_families=required_families)
        else:
            from pharmacophoremt._private.feature_snapshot_v1 import decode_snapshot

            native = decode_snapshot(raw, row["extraction"])
        rows.append(
            {
                "work_ordinal": row["work_ordinal"],
                "work_key": row["work_key"],
                "source_key": row["source_key"],
                "occurrence_key": row["occurrence_key"],
                "extraction": row["extraction"],
                "inventory": native,
                **({"lineage": row["lineage"]} if native_profile else {}),
            }
        )
    return {
        "report": {
            "generation": expected_generation,
            "payload_profile": payload_profile,
            "scope": "captured-inventory-only",
            "required_families": list(required_families),
            "manifest_complete": preview["manifest_complete"],
            "selected_count": len(rows),
            "selection_ordinals": preview["selection_ordinals"],
            "original_payloads_interpreted": bool(rows),
            "quantity_semantics_checked": bool(rows),
            "molecular_origin_authenticated": False,
            "query_admitted": None,
            "match_outcome": None,
            "decision": {
                "action": "captured_features_ready" if rows else "empty_selection"
            },
        },
        "inventories": rows,
    }
