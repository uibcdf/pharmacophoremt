"""Real provider contracts, no proposed public namespace or storage promotion."""

import copy
import os
import pickle
from pathlib import Path

import pytest

from phmt_test_support.feature_asset_admission import (
    AssetAdmissionErrorStudy,
    admit_inspection,
    admit_open,
    admit_page,
    admit_publication,
    admit_reuse,
)
from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
from phmt_test_support.feature_store import FeatureStoreReaderStudy, FeatureStoreStudy
from phmt_test_support.feature_store_workflow import (
    FeatureStoreWorkflowStudy,
    prepare_reuse,
)
from phmt_test_support.typed_retrieval import load_entries

HASH = "a" * 64


def test_literal_paths_keys_and_family_order_are_not_confused_with_units():
    assert admit_open("literal nm/1 nm") == {
        "path": Path("literal nm/1 nm"),
        "generation": None,
    }
    keys = ["nm", "1 nm", "repeat=α", " --literal key "]
    value = admit_inspection(
        ["positive charge", "hb donor", "hb donor"], work_keys=keys
    )
    assert value == {
        "required_families": ("hb donor", "positive charge"),
        "work_keys": tuple(keys),
    }
    keys.clear()
    assert len(value["work_keys"]) == 4
    assert admit_inspection(["hb donor"], work_keys=[])["work_keys"] == ()
    assert admit_inspection(["hb donor"])["work_keys"] is None


def test_caller_owned_none_semantics_and_explicit_publication_expectation():
    assert admit_open("source", generation=None)["generation"] is None
    assert admit_open("source", generation=HASH)["generation"] == HASH
    with pytest.raises(AssetAdmissionErrorStudy) as caught:
        admit_publication(None, expected_current=None)
    assert caught.value.code == "PHMT-ASSET-STUDY-E002"
    assert admit_publication(HASH, expected_current=None) == {
        "generation": HASH,
        "expected_current": None,
        "retry_of": None,
    }
    assert (
        admit_publication(HASH, expected_current=HASH, retry_of="b" * 32)["retry_of"]
        == "b" * 32
    )


@pytest.mark.parametrize(
    "operation",
    [
        lambda: admit_reuse(["hb donor"]),
        lambda: admit_publication(HASH),
        lambda: admit_open("a", unknown=True),
        lambda: admit_page(1),
    ],
)
def test_native_argdigest_call_shape_type_errors_are_not_replaced(operation):
    from argdigest import DigestError

    with pytest.raises(TypeError) as caught:
        operation()
    assert type(caught.value) is TypeError or isinstance(caught.value, DigestError)
    assert not isinstance(caught.value, AssetAdmissionErrorStudy)


@pytest.mark.parametrize("value", [b"file", "", "a\x00b", 0, None])
def test_bad_paths_are_catalogued_without_opening(value):
    with pytest.raises(AssetAdmissionErrorStudy) as caught:
        admit_open(value)
    assert caught.value.code == "PHMT-ASSET-STUDY-E001"
    assert "nonempty text path" in str(caught.value)


@pytest.mark.parametrize("value", [None, "current", "A" * 64, "0" * 63, 12, True])
def test_reuse_requires_exact_generation_identity(value):
    with pytest.raises(AssetAdmissionErrorStudy) as caught:
        admit_reuse(["hb donor"], expected_generation=value)
    assert caught.value.code == "PHMT-ASSET-STUDY-E002"
    assert caught.value.extra["argument"] == "expected_generation"


@pytest.mark.parametrize("families", [[], "hb donor", ["unknown"], [1]])
def test_family_admission_is_conservative_and_no_query_is_inferred(families):
    with pytest.raises(AssetAdmissionErrorStudy) as caught:
        admit_inspection(families)
    assert caught.value.code == "PHMT-ASSET-STUDY-E003"
    assert isinstance(caught.value.__cause__, ValueError)


@pytest.mark.parametrize(
    "keys", ["nm", ["nm", "nm"], [""], [False], [str(i) for i in range(13)]]
)
def test_selection_refuses_ambiguous_or_unbounded_study_inputs(keys):
    with pytest.raises(AssetAdmissionErrorStudy) as caught:
        admit_inspection(["hb donor"], work_keys=keys)
    assert caught.value.code == "PHMT-ASSET-STUDY-E004"


@pytest.mark.parametrize(
    "options",
    [{"offset": True}, {"limit": False}, {"offset": -1}, {"limit": -1}, {"limit": "1"}],
)
def test_page_integers_do_not_accept_booleans_or_coercions(options):
    with pytest.raises(AssetAdmissionErrorStudy) as caught:
        admit_page(**options)
    assert caught.value.code == "PHMT-ASSET-STUDY-E005"


def test_zero_page_is_a_request_without_a_false_empty_corpus_claim():
    assert admit_page(offset=9, limit=0) == {"offset": 9, "limit": 0}
    assert admit_page() == {"offset": 0, "limit": 100}
    assert "selected_count" not in admit_page(limit=0)


@pytest.mark.parametrize("retry", ["", "a" * 31, "A" * 32, 1])
def test_retry_identifiers_are_literal_and_not_new_attempts(retry):
    with pytest.raises(AssetAdmissionErrorStudy) as caught:
        admit_publication(HASH, expected_current=None, retry_of=retry)
    assert caught.value.code == "PHMT-ASSET-STUDY-E006"


def test_poison_input_is_not_iterated_formatted_or_used_as_a_reader():
    import smonitor

    class Poison:
        def __iter__(self):
            raise AssertionError("Admission consumed an opaque source")

        def __repr__(self):
            raise AssertionError("Admission formatted a rejected value")

    with smonitor.diagnostic_scope(safe_extra={"operation": "feature_asset_admission"}):
        for operation in (
            lambda: admit_inspection(["hb donor"], work_keys=Poison()),
            lambda: admit_open(Poison()),
        ):
            with pytest.raises(AssetAdmissionErrorStudy):
                operation()


def test_catalog_exception_retains_identity_through_python_roundtrips():
    try:
        admit_page(limit=-1)
    except AssetAdmissionErrorStudy as error:
        original = error
    for restored in (copy.deepcopy(original), pickle.loads(pickle.dumps(original))):
        assert restored.code == original.code
        assert restored.extra == original.extra
        assert str(restored) == str(original)


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_admitted_requests_compose_with_unchanged_workflow_and_original_quantity_validation(
    tmp_path, unit
):
    from pharmacophoremt import pyunitwizard as puw
    from phmt_test_support.feature_snapshot_case import projection

    rows = []
    entries = load_entries(os.environ.get("PHMT_RECEIVING_CONTEXT", "source"))
    for entry in entries:
        parent = FeatureSnapshotStudy(entry["snapshot"]).describe()["parent"]
        rows.append(
            {
                "work_key": entry["work_key"],
                "source_key": parent["source_key"],
                "occurrence_key": parent["occurrence_key"],
                "status": "ready",
                "snapshot": entry["snapshot"],
            }
        )
    root = tmp_path / "store"
    with FeatureStoreStudy(root, create=True) as writer:
        generation = writer.seal(rows)
        writer.publish(generation, expected_current=None)
    request = admit_reuse(
        ["positive charge", "hb donor"],
        expected_generation=generation,
        work_keys=["repeat=α", "1 nm", "nm"],
    )
    with (
        puw.context(standard_units=[unit, "ps", "radians"]),
        FeatureStoreWorkflowStudy(root) as guided,
        FeatureStoreReaderStudy(root) as expert,
    ):
        a = guided.reuse(**request)
        b = prepare_reuse(
            expert,
            ["hb donor", "positive charge"],
            expected_generation=generation,
            work_keys=["nm", "1 nm", "repeat=α"],
        )
        assert a["report"] == b["report"]
        assert [r["work_ordinal"] for r in a["inventories"]] == [1, 6, 10]
        assert [projection(r["inventory"]) for r in a["inventories"]] == [
            projection(r["inventory"]) for r in b["inventories"]
        ]
        assert a["report"]["query_admitted"] is None
        assert a["report"]["quantity_semantics_checked"]


@pytest.mark.parametrize("flag", [True, False, 1])
def test_public_admission_does_not_expose_internal_skip(flag):
    # ArgDigest forwards a literal True bypass to the underlying callable.
    # This proposed public signature deliberately has no such internal option.
    with pytest.raises(TypeError):
        admit_reuse(["hb donor"], expected_generation=HASH, skip_digestion=flag)


def test_plain_request_dict_does_not_replace_owner_validation():
    class Unreadable:
        def describe(self):
            raise AssertionError("Bad generation reached a reader")

    request = {"required_families": ["hb donor"], "expected_generation": "bad"}
    with pytest.raises(ValueError):
        prepare_reuse(Unreadable(), **request)
