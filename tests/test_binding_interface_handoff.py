"""Independent analytical acceptance for the native BindingMT H0/H1 inputs."""

import json
import shutil
import sys
from copy import deepcopy
from pathlib import Path

import ackredit as ack
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import (
    compose_pharmacophores,
    from_interaction_collection,
    from_interactions,
)
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.binding_interface_handoff import (
    construct,
    load_package,
    observation_rows,
    receive_package,
    scope,
)

INPUTS = Path(__file__).parent / "data" / "binding_interface_handoff"


@pytest.fixture(scope="module")
def package():
    return load_package(INPUTS)


def _without_checked_query_producer(metadata, expected_version):
    """Separate one explicitly checked new/historical PHMT producer declaration."""
    result = deepcopy(metadata)
    assert result.pop("producer") == {"pharmacophoremt": expected_version}
    return result


def test_native_full_context_and_strict_group_scope_preserve_original_ids(package):
    manifest, source, _ = package
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"),
        [[[0, 0, 0], [0.2, 0, 0], [0, 0.25, 0], [0, 0.45, 0]]],
    )
    scoped = scope(source.interactions)
    links = []
    for label in ("ionic_031", "ionic_035"):
        original = observation_rows(source.interactions[label])
        assert sorted(row["pair"] for row in original) == [[0, 1], [0, 2], [2, 3]]
        retained = observation_rows(scoped[label])
        assert len(retained) == 1 and retained[0]["pair"] == [0, 2]
        assert retained[0] in original
        links.append(
            dict(
                source="source.h5msm",
                analysis=label,
                relation=retained[0]["relation"],
                occurrence=retained[0]["occurrence"],
                hypothesis="primary.json",
                site=0,
            )
        )
    assert links == manifest["analysis_site_links"]
    empty = scoped["ionic_empty"]
    assert observation_rows(empty) == []
    assert list(empty.evaluated_structure_indices) == [0]


def test_rebuilt_primary_preserves_labeled_evidence_and_saved_native_semantics(package):
    manifest, source, models = package
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    query = construct(source)
    assert query.n_interaction_sites == 1
    site = query.interaction_sites[0]
    assert site.feature_name == "positive charge"
    assert site.essential and site.weight == 1
    np.testing.assert_allclose(
        puw.get_value(site.center, to_unit="nm"), [0, 0.25, 0], atol=1e-12
    )
    assert puw.get_value(site.radius, to_unit="nm") == pytest.approx(0.02)
    stored = models["primary"]
    historical_version = manifest["producer"]["pharmacophoremt"]
    fresh_metadata = _without_checked_query_producer(query.metadata, phmt.__version__)
    stored_metadata = _without_checked_query_producer(
        stored.metadata, historical_version
    )
    for fresh_component, stored_component in zip(
        fresh_metadata["components"], stored_metadata["components"], strict=True
    ):
        fresh_component["metadata"] = _without_checked_query_producer(
            fresh_component["metadata"], phmt.__version__
        )
        stored_component["metadata"] = _without_checked_query_producer(
            stored_component["metadata"], historical_version
        )
        if fresh_component["label"] in ("ionic_031", "ionic_035"):
            # Construction performs fresh charge recognition. Its declaration
            # belongs to the current provider, independently of saved native
            # interaction software and the historical recognition producer.
            for component, version in (
                (fresh_component, msm.__version__),
                (stored_component, manifest["producer"]["molsysmt"]),
            ):
                charge = component["metadata"]["ionic_feature_inventory"][
                    "recognition"
                ]["formal_charge"]
                assert charge.pop("software") == {"molsysmt": version}
    assert fresh_metadata == stored_metadata
    # Site/contribution evidence has no newly generated model producer field.
    # Compare it exactly, including all original native software/attribution.
    assert site.metadata == stored.interaction_sites[0].metadata
    assert stored.metadata["producer"] == {"pharmacophoremt": historical_version}
    assert {
        (row["component"], row["relation_index"], row["occurrence_index"])
        for row in site.metadata["observations"]
    } == {
        (row["analysis"], row["relation"], row["occurrence"])
        for row in manifest["analysis_site_links"]
    }
    assert len(site.metadata["composition_contributions"]) == 2
    thresholds = [
        puw.get_value(
            puw.quantity(**row["metadata"]["parameters"]["distance_threshold"]),
            to_unit="nm",
        )
        for row in query.metadata["components"]
    ]
    assert thresholds == pytest.approx([0.31, 0.35, 0.01])
    assert query.metadata["components"][-1]["n_sites"] == 0
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )


@pytest.mark.parametrize("change", ["producer_version", "producer_extra", "charge"])
def test_reconstruction_oracle_rejects_changed_recognition_evidence(
    package, monkeypatch, change
):
    original = construct

    def changed(source):
        query = original(source)
        charge = query.metadata["components"][0]["metadata"]["ionic_feature_inventory"][
            "recognition"
        ]["formal_charge"]
        if change == "producer_version":
            charge["software"]["molsysmt"] = "unexpected-producer"
        elif change == "producer_extra":
            charge["software"]["unexpected-provider"] = "1.0"
        else:
            charge["charges"]["values"][0] = 2.0
        return query

    monkeypatch.setattr(sys.modules[__name__], "construct", changed)
    with pytest.raises(AssertionError):
        test_rebuilt_primary_preserves_labeled_evidence_and_saved_native_semantics(
            package
        )


def test_alternatives_and_hard_constraints_have_independent_expected_decisions():
    measured = receive_package(INPUTS)
    json.dumps(measured, allow_nan=False)
    expected = {
        "primary_self": ("matched", 1),
        "primary_alternative": ("not_matched", 0),
        "alternative_self": ("matched", 1),
        "alternative_primary": ("not_matched", 0),
        "zero_essential": ("not_matched", 1),
        "excluded": ("not_matched", 1),
        "keep": ("not_matched", 0.5),
    }
    for name, (status, fit) in expected.items():
        assert measured["evaluations"][name]["status"] == status
        assert measured["evaluations"][name]["fit_value"] == pytest.approx(fit)
    assert measured["evaluations"]["zero_essential"]["missing_essential_sites"] == [1]
    assert measured["evaluations"]["excluded"]["excluded_volume_clashes"] == [
        dict(site_index=1, atom_index=2)
    ]
    assert len(measured["evaluations"]["keep"]["missing_essential_sites"]) == 1


def test_conflicting_alternative_must_not_be_merged_by_same_participant(package):
    _, source, _ = package
    other = msm.h5msm.read(str(INPUTS / "alternative.h5msm"))
    primary = from_interactions(source, scope(source.interactions)["ionic_031"], [2])
    alternative = from_interactions(other, scope(other.interactions)["ionic_031"], [2])
    with pytest.raises(ArgumentError, match="conflicting constraints"):
        compose_pharmacophores(
            {"primary": primary, "alternative": alternative},
            duplicate_policy="same_participant",
        )


@pytest.mark.parametrize("failure", ["state", "maps", "uncovered"])
def test_incompatible_native_evidence_fails_instead_of_returning_partial_hypothesis(
    package, failure
):
    _, source, _ = package
    analyses = dict(source.interactions)
    changed = analyses["ionic_035"]
    if failure == "uncovered":
        changed = changed.invalidate_structures([0])
    else:
        # Deliberately contradictory evidence via the public owner codec, not
        # original detector output and not a custom serialized interaction format.
        payload = msm.convert(changed, to_form="molsysmt.InteractionsDict")
        if failure == "state":
            payload.data["parameters"]["chemical_state_index"] = 1
        else:
            payload.data["atom_source_indices"] = np.array([3, 2, 1, 0])
        changed = msm.convert(payload, to_form="molsysmt.Interactions")
    analyses["ionic_035"] = changed
    with pytest.raises(ArgumentError):
        from_interaction_collection(source, scope(analyses), [2])


def test_evaluated_empty_is_recorded_but_is_not_a_positive_query(package):
    _, source, _ = package
    query = from_interaction_collection(
        source, {"empty": source.interactions["ionic_empty"]}, [2]
    )
    assert query.n_interaction_sites == 0
    assert query.metadata["components"][0]["metadata"][
        "evaluated_structure_indices"
    ] == [0]
    with pytest.raises(ArgumentError, match="positive total weight"):
        PoseEvaluator(query)


def test_partial_compound_charge_participant_is_refused():
    source = msm.convert(
        msm.convert("smiles:CC(=O)[O-].[Na+]", to_form="rdkit.Mol"),
        to_form="molsysmt.MolSys",
    )
    source.structures.append(
        coordinates=puw.quantity(
            [
                [
                    [0, -0.15, 0],
                    [0, 0, 0],
                    [-0.1, 0.1, 0],
                    [0.1, 0.1, 0],
                    [0.1, 0.4, 0],
                ]
            ],
            "nm",
        )
    )
    observed = msm.interactions.ionic.get_ionic_interactions(
        source,
        ".31 nm",
        selection=[0, 1, 2, 3],
        selection_2=[4],
        selection_mode="between",
        structure_indices=[0],
        pbc=False,
    )
    assert len(observation_rows(observed)) == 1
    complete = from_interactions(source, observed, [0, 1, 2, 3])
    assert complete.n_interaction_sites == 1
    assert complete.interaction_sites[0].feature_name == "negative charge"
    with pytest.raises(ArgumentError, match="charge center crosses"):
        from_interactions(source, observed, [2, 3])


def test_native_saved_read_needs_no_detection_recognition_or_new_credit(
    package, monkeypatch
):
    _, _, original = package

    def forbidden(*args, **kwargs):
        raise AssertionError("saved hypothesis reading must not calculate science")

    import pharmacophoremt.modeler.features as features

    for name in ("get", "select", "convert"):
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(msm.interactions.ionic, "get_ionic_interactions", forbidden)
    monkeypatch.setattr(msm.physchem, "get_charge_centers", forbidden)
    monkeypatch.setattr(features, "get_features", forbidden)
    monkeypatch.setattr(features, "capability", forbidden)
    with ack.capture("saved-native-read") as capture:
        restored_source = msm.h5msm.read(str(INPUTS / "source.h5msm"))
        assert sorted(restored_source.interactions) == [
            "ionic_031",
            "ionic_035",
            "ionic_empty",
        ]
        assert sorted(
            row["pair"]
            for row in observation_rows(restored_source.interactions["ionic_031"])
        ) == [[0, 1], [0, 2], [2, 3]]
        for name, model in original.items():
            recovered = phmt.io.load_json(str(INPUTS / (name + ".json")))
            assert recovered.metadata == model.metadata
            assert recovered.n_interaction_sites == model.n_interaction_sites
            for left, right in zip(
                recovered.interaction_sites, model.interaction_sites
            ):
                assert (left.weight, left.essential, left.metadata) == (
                    right.weight,
                    right.essential,
                    right.metadata,
                )
    assert capture.attribution.to_dict()["uses"] == []


@pytest.mark.parametrize("failure", ["missing", "corrupt"])
def test_unavailable_artifact_does_not_become_evaluated_empty(tmp_path, failure):
    destination = tmp_path / "inputs"
    shutil.copytree(INPUTS, destination)
    selected = destination / "primary.json"
    if failure == "missing":
        selected.unlink()
        expected = FileNotFoundError
    else:
        selected.write_text("{}")
        expected = ValueError
    with pytest.raises(expected):
        load_package(destination)
