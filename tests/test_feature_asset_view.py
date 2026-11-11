"""Public metadata reader controls; original payload semantics stay separate."""

import base64
import copy
import hashlib
import json
import os
import pickle
import shutil

import pytest

from pharmacophoremt_features import FeatureAssetError, FeatureAssetView, _schema
from pharmacophoremt_results import canonical_json
from phmt_test_support.feature_archive_export import export_study_feature_archive
from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
from phmt_test_support.feature_store import FeatureStoreStudy
from phmt_test_support.typed_retrieval import load_entries


def records(entries):
    result = []
    for entry in entries:
        parent = FeatureSnapshotStudy(entry["snapshot"]).describe()["parent"]
        result.append(
            {
                "work_key": entry["work_key"],
                "source_key": parent["source_key"],
                "occurrence_key": parent["occurrence_key"],
                "status": "ready",
                "snapshot": entry["snapshot"],
            }
        )
    return result


def identity(root):
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*")
        if p.is_file()
    }


def install(root, value, *, publish=True):
    raw = canonical_json(value).encode()
    generation = hashlib.sha256(raw).hexdigest()
    (root / "generations" / (generation + ".json")).write_bytes(raw)
    if publish:
        (root / "CURRENT").write_bytes(
            canonical_json(
                {
                    "schema": _schema.STORE_SCHEMA,
                    "generation": generation,
                    "bytes": len(raw),
                }
            ).encode()
        )
    return generation


def bundle(root):
    generation = json.loads((root / "CURRENT").read_bytes())["generation"]
    return json.loads((root / "generations" / (generation + ".json")).read_bytes())


@pytest.fixture(scope="module")
def originals(tmp_path_factory):
    root = tmp_path_factory.mktemp("feature-view-originals")
    entries = load_entries(os.environ.get("PHMT_RECEIVING_CONTEXT", "source"))
    source = root / "study"
    with FeatureStoreStudy(source, create=True) as writer:
        generation = writer.seal(records(entries))
        writer.publish(generation, expected_current=None)
    before = identity(source)
    exported = root / "public"
    report = export_study_feature_archive(source, exported)
    assert identity(source) == before
    return source, exported, entries, report


@pytest.fixture
def archive(originals, tmp_path):
    root = tmp_path / "archive"
    shutil.copytree(originals[1], root)
    return root


def test_public_reader_preserves_originals_producers_and_does_not_claim_interpretation(
    archive, originals
):
    before = identity(archive)
    with FeatureAssetView.open(archive) as view:
        report = view.summary()
        assert report["record_count"] == 11 and report["unique_payload_count"] == 10
        assert report["status_counts"] == {
            "ready": 11,
            "failed": 0,
            "partial": 0,
            "unsupported": 0,
            "unattempted": 0,
        }
        assert (
            report["complete"]
            and report["coverage_authority"] == "producer-declared extraction metadata"
        )
        assert (
            not report["original_payloads_interpreted"]
            and not report["quantity_semantics_checked"]
        )
        assert (
            not report["molecular_origin_authenticated"]
            and report["query_admitted"] is report["match_outcome"] is None
        )
        assert not report["persisted_lookup_index"]
        for ordinal, entry in enumerate(originals[2]):
            assert view.snapshot_bytes(ordinal) == entry["snapshot"]
            old = FeatureSnapshotStudy(entry["snapshot"]).describe()
            row = view.work_items(offset=ordinal, limit=1)["records"][0]
            assert (
                row["work_ordinal"] == ordinal and row["work_key"] == entry["work_key"]
            )
            assert row["extraction"]["producer"] == old["producer"]
            assert row["extraction"]["parent"] == old["parent"]
    assert identity(archive) == before


def test_page_counts_selected_offsets_and_global_ordinals(archive):
    with FeatureAssetView.open(archive) as view:
        keys = ["repeat=α", "1 nm", "nm"]
        page = view.work_items(work_keys=keys, offset=1, limit=1)
        assert page["selected_count"] == 3 and page["returned_count"] == 1
        assert (
            page["records"][0]["work_ordinal"] == 6
            and page["records"][0]["work_key"] == "1 nm"
        )
        assert page["next_offset"] == 2 and page["has_more"]
        zero = view.work_items(work_keys=keys, limit=0)
        assert (
            zero["selected_count"] == 3
            and zero["returned_count"] == 0
            and zero["records"] == []
        )
        assert zero["next_offset"] is None and zero["has_more"]
        past = view.work_items(work_keys=keys, offset=99)
        assert (
            past["selected_count"] == 3
            and past["returned_count"] == 0
            and not past["has_more"]
        )
        assert view.work_items(work_keys=[])["selected_count"] == 0
        assert view.work_items()["selected_count"] == 11


def test_known_declared_empty_and_unobserved_family_are_separate(archive):
    with FeatureAssetView.open(archive) as view:
        aromatic = view.inspect(["aromatic ring"], work_keys=["empty:nm"])
        donor = view.inspect(["hb donor"], work_keys=["empty:nm"])
        assert aromatic["records"][0]["declared_counts"] == {"aromatic ring": 0}
        assert aromatic["decision"]["action"] == "payload_validation_required"
        assert donor["records"][0]["declared_counts"] == {}
        assert donor["records"][0]["unobserved_families"] == ["hb donor"]
        assert donor["decision"]["action"] == "evaluate_missing_families"
        assert aromatic["query_admitted"] is donor["match_outcome"] is None
        assert (
            view.inspect(["hb donor"], work_keys=[])["decision"]["action"]
            == "empty_selection"
        )


def test_opaque_payload_semantics_are_not_inferred_from_valid_metadata(archive):
    value = bundle(archive)
    original = b"This opaque original is not a native feature inventory."
    digest = hashlib.sha256(original).hexdigest()
    value["records"] = [value["records"][1]]
    value["records"][0]["payload_sha256"] = digest
    value["payloads"] = {
        digest: {
            "format": "opaque-original-test@1",
            "data": base64.b64encode(original).decode(),
        }
    }
    install(archive, value)
    with FeatureAssetView.open(archive) as view:
        assert view.snapshot_bytes(0) == original
        report = view.inspect(["hb donor"])
        assert report["records"][0]["declared_counts"] == {"hb donor": 2}
        assert (
            not report["original_payloads_interpreted"]
            and not report["quantity_semantics_checked"]
        )
        assert (
            report["decision"]["action"] == "payload_validation_required"
            and report["query_admitted"] is None
        )


@pytest.mark.parametrize("status", ["failed", "partial", "unsupported", "unattempted"])
def test_explicit_incomplete_causes_and_ready_subset(archive, status):
    value = bundle(archive)
    value["records"][0] = {
        "work_key": "gap",
        "source_key": "source-gap",
        "occurrence_key": "gap:0",
        "status": status,
        "cause": {"type": "analytical-control", "reason": "original incomplete cause"},
    }
    used = {r["payload_sha256"] for r in value["records"] if r["status"] == "ready"}
    value["payloads"] = {k: v for k, v in value["payloads"].items() if k in used}
    install(archive, value)
    with FeatureAssetView.open(archive) as view:
        assert not view.summary()["complete"]
        report = view.inspect(["hb donor"])
        assert report["decision"]["action"] == "resolve_incomplete_extraction"
        assert report["records"][0]["cause"]["reason"] == "original incomplete cause"
        assert (
            view.inspect(["hb donor"], work_keys=["nm"])["decision"]["action"]
            == "payload_validation_required"
        )
        with pytest.raises(FeatureAssetError) as caught:
            view.snapshot_bytes(0)
        assert caught.value.code == "PHMT-E306"


def test_generation_pin_relocation_detached_data_and_explicit_reopen(archive, tmp_path):
    old = FeatureAssetView.open(archive)
    first = old.generation
    original = old.snapshot_bytes(1)
    value = bundle(archive)
    value["records"][1]["work_key"] = "new literal key"
    second = install(archive, value)
    assert old.generation == first and old.snapshot_bytes(1) == original
    assert old.work_items(offset=1, limit=1)["records"][0]["work_key"] == "nm"
    moved = tmp_path / "moved"
    archive.rename(moved)
    with (
        FeatureAssetView.open(moved) as new,
        FeatureAssetView.open(moved, generation=first) as pinned,
    ):
        assert new.generation == second and pinned.generation == first
    old.close()


def test_close_is_idempotent_and_only_owned_data_is_dropped(archive):
    a, b = FeatureAssetView.open(archive), FeatureAssetView.open(archive)
    data = a.work_items(limit=1)
    original = a.snapshot_bytes(1)
    a.close()
    a.close()
    for operation in (
        lambda: a.generation,
        a.summary,
        a.work_items,
        lambda: a.snapshot_bytes(1),
        lambda: a.inspect(["hb donor"]),
        a.__enter__,
    ):
        with pytest.raises(FeatureAssetError) as caught:
            operation()
        assert caught.value.code == "PHMT-E304"
    assert data["records"] and original and b.summary()["record_count"] == 11
    b.close()


def test_returned_metadata_mutation_does_not_modify_the_view(archive):
    with FeatureAssetView.open(archive) as view:
        a = view.work_items(limit=1)
        a["records"][0]["extraction"]["producer"]["versions"].clear()
        assert view.work_items(limit=1)["records"][0]["extraction"]["producer"][
            "versions"
        ]
        report = view.inspect(["hb donor"], work_keys=["nm"])
        report["records"][0]["extraction"]["coverage"].clear()
        assert view.inspect(["hb donor"], work_keys=["nm"])["records"][0][
            "declared_counts"
        ] == {"hb donor": 2}


@pytest.mark.parametrize(
    "action",
    [
        lambda v: v.work_items(work_keys=[" nm"]),
        lambda v: v.inspect(["hb donor"], work_keys=["NM"]),
    ],
)
def test_unknown_literal_keys_refuse_instead_of_becoming_empty(archive, action):
    with FeatureAssetView.open(archive) as view:
        with pytest.raises(FeatureAssetError) as caught:
            action(view)
        assert caught.value.code == "PHMT-E305"
        assert view.work_items(work_keys=["nm"])["selected_count"] == 1


@pytest.mark.parametrize(
    "options",
    [{"generation": "../CURRENT"}, {"generation": "A" * 64}, {"generation": False}],
)
def test_bad_generation_refuses_before_storage(monkeypatch, options):
    from pharmacophoremt_features import _storage

    def forbidden(*args):
        raise AssertionError("Argument error reached storage")

    monkeypatch.setattr(_storage, "read_generation", forbidden)
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetView.open("unused", **options)
    assert caught.value.code == "PHMT-E301"


@pytest.mark.parametrize(
    "operation",
    [
        lambda v: v.work_items(limit=True),
        lambda v: v.work_items(offset=-1),
        lambda v: v.work_items(work_keys="nm"),
        lambda v: v.work_items(work_keys=["nm", "nm"]),
        lambda v: v.work_items(work_keys=["\ud800"]),
        lambda v: v.snapshot_bytes(False),
        lambda v: v.snapshot_bytes(-1),
        lambda v: v.snapshot_bytes(99),
        lambda v: v.inspect([]),
        lambda v: v.inspect(["unknown"]),
    ],
)
def test_argument_domains_are_closed(archive, operation):
    with FeatureAssetView.open(archive) as view:
        with pytest.raises(FeatureAssetError) as caught:
            operation(view)
        assert caught.value.code == "PHMT-E301"


def test_native_type_errors_and_internal_bypass_are_not_wrapped(archive):
    for operation in (
        lambda: FeatureAssetView.open(),
        lambda: FeatureAssetView.open(archive, unknown=True),
        lambda: FeatureAssetView.open(archive, skip_digestion=True),
    ):
        with pytest.raises(TypeError):
            operation()


def test_missing_open_never_creates_and_direct_study_open_never_migrates(
    originals, tmp_path
):
    missing = tmp_path / "missing"
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetView.open(missing)
    assert caught.value.code == "PHMT-E303" and not missing.exists()
    before = identity(originals[0])
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetView.open(originals[0])
    assert caught.value.code == "PHMT-E307" and identity(originals[0]) == before
    with pytest.raises(FileExistsError):
        export_study_feature_archive(originals[0], originals[1])


@pytest.mark.parametrize(
    "mutation",
    [
        "schema",
        "profile",
        "extra",
        "duplicate",
        "parent",
        "coverage",
        "count_bool",
        "producer",
        "unused",
        "missing",
        "payload",
        "noncanonical",
    ],
)
def test_self_consistent_generation_hash_does_not_bypass_metadata_checks(
    archive, mutation
):
    value = bundle(archive)
    if mutation == "schema":
        value["schema"] = "unknown"
    elif mutation == "profile":
        value["profile"] = "unknown"
    elif mutation == "extra":
        value["unexpected"] = True
    elif mutation == "duplicate":
        value["records"][1]["work_key"] = value["records"][0]["work_key"]
    elif mutation == "parent":
        value["records"][1]["extraction"]["parent"]["source_key"] = "different"
    elif mutation == "coverage":
        value["records"][1]["extraction"]["coverage"]["hb donor"]["status"] = (
            "evaluated_empty"
        )
    elif mutation == "count_bool":
        value["records"][1]["extraction"]["coverage"]["hb donor"]["count"] = True
    elif mutation == "producer":
        value["records"][1]["extraction"]["producer"]["admission_sha256"] = "bad"
    elif mutation == "unused":
        value["records"].clear()
    elif mutation == "missing":
        value["payloads"].clear()
    elif mutation == "payload":
        value["payloads"][next(iter(value["payloads"]))]["data"] = "AA=="
    if mutation == "noncanonical":
        raw = json.dumps(value, indent=2).encode()
        generation = hashlib.sha256(raw).hexdigest()
        (archive / "generations" / (generation + ".json")).write_bytes(raw)
        (archive / "CURRENT").write_bytes(
            canonical_json(
                {
                    "schema": _schema.STORE_SCHEMA,
                    "generation": generation,
                    "bytes": len(raw),
                }
            ).encode()
        )
    else:
        install(archive, value)
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetView.open(archive)
    assert caught.value.code == (
        "PHMT-E307" if mutation in ("schema", "profile") else "PHMT-E302"
    )


@pytest.mark.parametrize(
    "mutation", ["marker", "pointer", "size", "checksum", "truncate", "nan", "infinity"]
)
def test_control_corruption_refuses_and_already_open_view_stays_pinned(
    archive, mutation
):
    pinned = FeatureAssetView.open(archive)
    generation = pinned.generation
    if mutation == "marker":
        (archive / "STORE.json").write_bytes(b"{}")
    elif mutation == "pointer":
        (archive / "CURRENT").write_bytes(b"{")
    elif mutation == "size":
        value = json.loads((archive / "CURRENT").read_bytes())
        value["bytes"] += 1
        (archive / "CURRENT").write_bytes(canonical_json(value).encode())
    else:
        path = archive / "generations" / (generation + ".json")
        if mutation == "checksum":
            path.write_bytes(path.read_bytes() + b" ")
        elif mutation == "truncate":
            path.write_bytes(b"{")
        else:
            raw = b'{"bad":NaN}' if mutation == "nan" else b'{"bad":1e999}'
            gen = hashlib.sha256(raw).hexdigest()
            (archive / "generations" / (gen + ".json")).write_bytes(raw)
            (archive / "CURRENT").write_bytes(
                canonical_json(
                    {
                        "schema": _schema.STORE_SCHEMA,
                        "generation": gen,
                        "bytes": len(raw),
                    }
                ).encode()
            )
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetView.open(archive)
    assert caught.value.code == ("PHMT-E307" if mutation == "marker" else "PHMT-E302")
    assert pinned.generation == generation and pinned.snapshot_bytes(1)
    pinned.close()


@pytest.mark.parametrize("kind", ["fifo", "symlink", "directory"])
def test_nonregular_files_refuse_without_blocking(archive, kind):
    path = archive / "CURRENT"
    path.rename(archive / "original-current")
    if kind == "fifo":
        os.mkfifo(path)
    elif kind == "symlink":
        path.symlink_to(archive / "original-current")
    else:
        path.mkdir()
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetView.open(archive)
    assert caught.value.code in {"PHMT-E302", "PHMT-E303"}


def test_empty_declared_archive_is_distinct_from_missing_open(archive):
    value = bundle(archive)
    value["records"] = []
    value["payloads"] = {}
    install(archive, value)
    with FeatureAssetView.open(archive) as view:
        assert view.summary()["complete"] and view.summary()["record_count"] == 0
        assert view.work_items()["records"] == []
        assert view.inspect(["hb donor"])["decision"]["action"] == "empty_selection"


def test_document_bound_and_record_bound_refuse(archive):
    value = bundle(archive)
    value["records"] = value["records"][:1] * (_schema.MAX_RECORDS + 1)
    install(archive, value)
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetView.open(archive)
    assert caught.value.code == "PHMT-E302"
    generation = json.loads((archive / "CURRENT").read_bytes())["generation"]
    path = archive / "generations" / (generation + ".json")
    with path.open("wb") as stream:
        stream.truncate(_schema.MAX_DOCUMENT_BYTES + 1)
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetView.open(archive, generation=generation)
    assert caught.value.code == "PHMT-E302"


def test_full_payload_bound_and_unique_original_bound(archive):
    value = bundle(archive)
    template = copy.deepcopy(value["records"][1])
    value["records"] = []
    value["payloads"] = {}
    for i, raw in enumerate(
        (b"x" * _schema.MAX_PAYLOAD_BYTES, b"y" * _schema.MAX_PAYLOAD_BYTES)
    ):
        key = hashlib.sha256(raw).hexdigest()
        row = copy.deepcopy(template)
        row.update(work_key=f"opaque:{i}", payload_sha256=key)
        value["records"].append(row)
        value["payloads"][key] = {
            "format": "opaque-limit-control@1",
            "data": base64.b64encode(raw).decode(),
        }
    install(archive, value)
    with FeatureAssetView.open(archive) as view:
        assert (
            len(view.snapshot_bytes(0)) == _schema.MAX_PAYLOAD_BYTES
            and view.summary()["unique_payload_count"] == 2
        )
    raw = b"z"
    key = hashlib.sha256(raw).hexdigest()
    row = copy.deepcopy(template)
    row.update(work_key="over-aggregate", payload_sha256=key)
    value["records"].append(row)
    value["payloads"][key] = {
        "format": "opaque-limit-control@1",
        "data": base64.b64encode(raw).decode(),
    }
    install(archive, value)
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetView.open(archive)
    assert caught.value.code == "PHMT-E302"


def test_catalog_error_roundtrips_preserve_code_and_message(archive):
    try:
        FeatureAssetView.open(archive, generation="bad")
    except FeatureAssetError as error:
        original = error
    for restored in (copy.deepcopy(original), pickle.loads(pickle.dumps(original))):
        assert (
            restored.code == original.code
            and restored.extra == original.extra
            and str(restored) == str(original)
        )
