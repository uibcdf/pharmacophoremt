"""Legacy merge delegates to owned common-frame composition with independent data."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import Pharmacophore, io
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.io.phmt import _to_dict
from pharmacophoremt.modeler import compose_pharmacophores
from tests.test_native_persistence_validation import SHAPES


class LiveSource:
    def __deepcopy__(self, memo):
        raise AssertionError("Molecular copies belong to MolSysMT")


def model(name="left", kind="sphere", frame=3):
    result = Pharmacophore(
        name=name,
        description=name + " description",
        score=0.75,
        ref_mol=2,
        ref_struct=frame,
        molecular_system=LiveSource(),
    )
    result.metadata = {"same_key": {"values": [name]}, "literal": "1 nm"}
    result.add_interaction_site(
        InteractionSite(
            SHAPES[kind](),
            "aromatic ring"
            if kind == "disk"
            else "hb donor"
            if kind == "sphere and vector"
            else "hydrophobicity",
            essential=False,
            weight=2.5,
            metadata={"original": [name]},
        )
    )
    return result


def test_merge_keeps_both_nested_metadata_and_original_scores():
    left, right = model(), model("right")
    expected = [deepcopy(_to_dict(item)) for item in [left, right]]
    merged = left.merge(right)
    assert merged.name == left.name and merged.description == left.description
    assert merged.score is None and merged.ref_mol is None and merged.ref_struct == 3
    assert merged.molecular_system is left.molecular_system
    assert merged.metadata["method"] == "common_frame_pharmacophore_composition@1"
    for component, label, original in zip(
        merged.metadata["components"], ["self", "other"], expected
    ):
        assert component["label"] == label
        for key in [
            "name",
            "description",
            "score",
            "ref_mol",
            "ref_struct",
            "metadata",
        ]:
            assert component[key] == original[key]
    merged.metadata["components"][0]["metadata"]["same_key"]["values"].append("changed")
    merged.metadata["components"][1]["metadata"]["same_key"]["values"].clear()
    assert [_to_dict(left), _to_dict(right)] == expected


@pytest.mark.parametrize("kind", SHAPES)
def test_all_supported_shapes_are_independent_in_both_directions(kind):
    left, right = model(kind=kind), model("right", kind=kind)
    expected = [deepcopy(_to_dict(item)) for item in [left, right]]
    merged = left.merge(right)
    assert merged.n_interaction_sites == 2
    for index, source in enumerate([left, right]):
        assert merged.interaction_sites[index] is not source.interaction_sites[0]
        assert (
            merged.interaction_sites[index].shape
            is not source.interaction_sites[0].shape
        )
    field = (
        "position" if kind == "point" else "start" if kind == "cylinder" else "center"
    )
    setattr(merged.interaction_sites[0].shape, field, puw.quantity([9, 8, 7], "nm"))
    merged.interaction_sites[0].features.append("hb acceptor")
    merged.interaction_sites[1].metadata["original"].append("changed")
    assert [_to_dict(left), _to_dict(right)] == expected
    merged_before = deepcopy(_to_dict(merged))
    setattr(left.interaction_sites[0].shape, field, puw.quantity([6, 5, 4], "nm"))
    right.interaction_sites[0].metadata["original"].clear()
    assert _to_dict(merged) == merged_before


@pytest.mark.parametrize(
    "case",
    ["both_empty", "left_empty", "right_empty", "self", "within_alias", "cross_alias"],
)
def test_occurrences_order_empty_and_self_merges_keep_independent_constraints(case):
    left, right = model(), model("right")
    if case in {"both_empty", "left_empty"}:
        left.interaction_sites.clear()
        left.n_interaction_sites = 0
    if case in {"both_empty", "right_empty"}:
        right.interaction_sites.clear()
        right.n_interaction_sites = 0
    if case == "self":
        right = left
    elif case == "within_alias":
        left.add_interaction_site(left.interaction_sites[0])
    elif case == "cross_alias":
        right.interaction_sites = [left.interaction_sites[0]]
    expected = [deepcopy(_to_dict(item)) for item in [left, right]]
    merged = left.merge(right)
    originals = left.interaction_sites + right.interaction_sites
    assert merged.n_interaction_sites == len(originals)
    assert len({id(site) for site in merged.interaction_sites}) == len(originals)
    assert merged.metadata["policy"]["duplicate_policy"] == "keep"
    assert [row["label"] for row in merged.metadata["components"]] == ["self", "other"]
    assert [row["component_site_index"] for row in merged.metadata["site_map"]] == list(
        range(left.n_interaction_sites)
    ) + list(range(right.n_interaction_sites))
    for output, original in zip(merged.interaction_sites, originals):
        assert output is not original and output.weight == original.weight
        assert (
            output.features == original.features
            and output.essential == original.essential
        )
    assert [_to_dict(left), _to_dict(right)] == expected


@pytest.mark.parametrize(
    "first,second,output", [(None, None, None), (None, 4, 4), (4, None, 4), (4, 4, 4)]
)
def test_common_reference_frame_is_retained_without_inventing_molecular_identity(
    first, second, output, monkeypatch
):
    left, right = model(frame=first), model("right", frame=second)
    assert left.molecular_system is not right.molecular_system

    def forbidden(*args, **kwargs):
        pytest.fail("Cached pharmacophore merging must not access molecular systems")

    for name in ["get", "select", "copy", "convert", "set", "merge"]:
        monkeypatch.setattr(msm, name, forbidden)
    result = left.merge(right)
    assert result.ref_struct == output
    assert result.molecular_system is left.molecular_system
    assert result.metadata["policy"]["common_frame"] == "caller_declared"


def test_conflicting_frames_raise_without_mutating_sources():
    left, right = model(frame=0), model("right", frame=1)
    before = [deepcopy(_to_dict(item)) for item in [left, right]]
    with pytest.raises(ArgumentError, match="reference frames"):
        left.merge(right)
    assert [_to_dict(left), _to_dict(right)] == before


@pytest.mark.parametrize("other", [None, object(), {}, []])
def test_invalid_other_is_refused_without_mutating_first(other):
    left = model()
    before = deepcopy(_to_dict(left))
    with pytest.raises(ArgumentError):
        left.merge(other)
    assert _to_dict(left) == before


def test_merge_calls_public_composer_once_with_keep(monkeypatch):
    import pharmacophoremt.modeler.composition as owner

    left, right = model(), model("right")
    calls = []

    def observed(*args, **kwargs):
        calls.append((args, kwargs))
        return compose_pharmacophores(*args, **kwargs)

    monkeypatch.setattr(owner, "compose_pharmacophores", observed)
    merged = left.merge(right)
    assert merged.n_interaction_sites == 2
    assert calls == [
        (
            ({"self": left, "other": right},),
            {"duplicate_policy": "keep", "name": left.name},
        )
    ]


@pytest.mark.parametrize("kind", ["json", "yaml"])
def test_merged_provenance_and_constraints_survive_nondefault_unit_persistence(
    tmp_path, kind
):
    left, right = model(kind="disk"), model("right", kind="sphere and vector")
    path = tmp_path / ("merged." + kind)
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        merged = left.merge(right)
        writer, reader = (
            (io.to_json, io.load_json) if kind == "json" else (io.to_yaml, io.load_yaml)
        )
        writer(merged, path)
    restored = reader(path)
    assert restored.metadata == merged.metadata
    assert [site.shape_name for site in restored.interaction_sites] == [
        "disk",
        "sphere and vector",
    ]
    for expected, observed in zip(merged.interaction_sites, restored.interaction_sites):
        assert (
            observed.features == expected.features
            and observed.weight == expected.weight
        )
        assert observed.essential is expected.essential
        np.testing.assert_allclose(
            puw.get_value(observed.center, to_unit="nm"),
            puw.get_value(expected.center, to_unit="nm"),
        )


@pytest.mark.parametrize("associate_left", [False, True])
def test_chained_merges_retain_nested_component_metadata(associate_left):
    left, middle, right = model(), model("middle"), model("right")
    if associate_left:
        intermediate = left.merge(middle)
        combined = intermediate.merge(right)
        nested = combined.metadata["components"][0]["metadata"]
        outer = combined.metadata["components"][1]["metadata"]
        expected_names = ["left", "middle"]
        assert outer == right.metadata
    else:
        intermediate = middle.merge(right)
        combined = left.merge(intermediate)
        nested = combined.metadata["components"][1]["metadata"]
        outer = combined.metadata["components"][0]["metadata"]
        expected_names = ["middle", "right"]
        assert outer == left.metadata
    assert combined.n_interaction_sites == 3
    assert [row["name"] for row in nested["components"]] == expected_names
    nested["components"][0]["metadata"]["same_key"]["values"].clear()
    assert all(item.metadata["same_key"]["values"] for item in [left, middle, right])
    assert intermediate.metadata["components"][0]["metadata"]["same_key"]["values"]


def test_late_copy_failure_does_not_modify_either_input():
    from pharmacophoremt.interaction_site.shape import Sphere

    failure = RuntimeError("pharmacophore extension refuses copying")

    class RefusedShape(Sphere):
        def __deepcopy__(self, memo):
            raise failure

    left, right = model(), model("right")
    right.interaction_sites[0].shape = RefusedShape("[1,2,3] nm", ".2 nm")
    before = [_to_dict(left), _to_dict(right)]
    with pytest.raises(RuntimeError) as error:
        left.merge(right)
    assert error.value is failure
    assert [_to_dict(left), _to_dict(right)] == before
