"""Public argument bypass retains the real extraction/native science boundaries."""

import importlib
import inspect
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import get_features
from pharmacophoremt_features import FeatureAssetError, FeatureInventoryPayload
from phmt_test_support.feature_snapshot_case import load_parent, projection

OWNER = importlib.import_module("pharmacophoremt.modeler.features")
FAMILIES = ["hb donor", "positive charge", "negative charge"]
PROFILE = "native-classical-v1"


def prepared():
    source, original = load_parent("ions")
    parent = {
        key: original[key]
        for key in (
            "source_key",
            "occurrence_key",
            "artifact_sha256",
            "artifact_bytes",
            "n_atoms",
            "preparation",
        )
    }
    parent["mapping_policy"] = "caller-declared-local-atom-axis@1"
    return source, parent


def encode(inventory, parent, **options):
    return FeatureInventoryPayload.from_inventory(
        inventory,
        FAMILIES,
        parent=parent,
        extraction_producer={"original": "retained", "unknown": None},
        payload_profile=options.pop("payload_profile", PROFILE),
        **options,
    )


@pytest.mark.parametrize(
    "operation", [get_features, FeatureInventoryPayload.from_inventory]
)
def test_additive_keyword_only_control(operation):
    control = inspect.signature(operation).parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY
    assert control.default is False


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_actual_default_false_true_preserve_native_evidence_and_source(unit):
    source, parent = prepared()
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = puw.configure.report()
        inventories = [
            get_features(source, features=FAMILIES, **options)
            for options in ({}, {"skip_digestion": False}, {"skip_digestion": True})
        ]
        assert all(detached(value) == detached(inventories[0]) for value in inventories)
        assert {row["kind"] for row in inventories[0]["features"]} == {
            "positive charge",
            "negative charge",
        }
        payloads = [
            encode(value, parent, **options)
            for value, options in zip(
                inventories, ({}, {"skip_digestion": False}, {"skip_digestion": True})
            )
        ]
        assert len({payload.to_bytes() for payload in payloads}) == 1
        for payload in payloads:
            assert projection(
                payload.to_inventory(required_families=FAMILIES)
            ) == projection(inventories[0])
            description = payload.describe()
            assert description["coverage"]["hb donor"]["count"] == 0
            assert description["extraction_producer"]["original"] == "retained"
            assert description["parent"] == parent
        assert puw.configure.report() == policy
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), coordinates
    )


def test_bypass_actually_requires_canonical_family_sequence():
    source, _ = prepared()
    ordinary = get_features(source, features="positive charge")
    explicit = get_features(source, features="positive charge", skip_digestion=False)
    assert projection(ordinary) == projection(explicit)
    with pytest.raises(ArgumentError):
        get_features(source, features="positive charge", skip_digestion=True)


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_family_never_accesses_source(monkeypatch, skip):
    def forbidden(*args, **kwargs):
        pytest.fail("unsupported family reached molecular access")

    monkeypatch.setattr(OWNER, "source_frame", forbidden)
    with pytest.raises(ArgumentError):
        get_features(object(), features=["unknown"], skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_invalid_frame_never_calls_provider(monkeypatch, skip):
    def forbidden(*args, **kwargs):
        pytest.fail("invalid frame reached molecular access")

    monkeypatch.setattr(msm, "get", forbidden)
    with pytest.raises(ArgumentError):
        get_features(
            object(), structure_index=-1, features=FAMILIES, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
def test_provider_failure_retains_original_exception(monkeypatch, skip):
    source, _ = prepared()
    failure = RuntimeError("original analytical provider failure")

    def failed(*args, **kwargs):
        raise failure

    monkeypatch.setattr(OWNER, "capability", lambda path: failed)
    with pytest.raises(RuntimeError) as caught:
        get_features(source, features=["positive charge"], skip_digestion=skip)
    assert caught.value is failure


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("profile", [None, "snapshot-study-v1", "unknown", 1])
def test_profile_refused_before_native_encoding(monkeypatch, skip, profile):
    source, parent = prepared()
    inventory = get_features(source, features=FAMILIES)
    codec = importlib.import_module("pharmacophoremt._private.native_feature_payload")

    def forbidden(*args, **kwargs):
        pytest.fail("unsupported profile reached native encoding")

    monkeypatch.setattr(codec, "encode", forbidden)
    with pytest.raises(FeatureAssetError) as caught:
        encode(inventory, parent, payload_profile=profile, skip_digestion=skip)
    assert caught.value.code == "PHMT-E301"


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "change,code", [("unit", "332"), ("map", "330"), ("volume", "331")]
)
def test_native_quantity_mapping_and_volume_checks_survive_bypass(skip, change, code):
    source, parent = prepared()
    inventory = deepcopy(get_features(source, features=FAMILIES))
    if change == "unit":
        inventory["features"][0]["center"] = puw.quantity([0, 0, 0], "ps")
    elif change == "map":
        inventory["features"][0]["atom_indices"] = [parent["n_atoms"]]
    else:
        inventory["features"][0]["kind"] = "included volume"
    with pytest.raises(FeatureAssetError) as caught:
        encode(inventory, parent, skip_digestion=skip)
    assert caught.value.code == "PHMT-E" + code


@pytest.mark.parametrize("flag", [0, 1, "true", None])
def test_nonboolean_controls_do_not_bypass(flag):
    source, parent = prepared()
    with pytest.raises(ArgumentError):
        get_features(source, features=FAMILIES, skip_digestion=flag)
    inventory = get_features(source, features=FAMILIES)
    with pytest.raises(FeatureAssetError) as caught:
        encode(inventory, parent, skip_digestion=flag)
    assert caught.value.code == "PHMT-E301"


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keywords_and_missing_inputs_keep_typeerror_compatibility(skip):
    with pytest.raises(TypeError):
        get_features(object(), unknown_option=True, skip_digestion=skip)
    with pytest.raises(TypeError):
        get_features(skip_digestion=skip)
    with pytest.raises(TypeError):
        FeatureInventoryPayload.from_inventory(
            {}, FAMILIES, unknown_option=True, skip_digestion=skip
        )
