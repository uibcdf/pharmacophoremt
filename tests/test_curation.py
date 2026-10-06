"""Explicit cached-model curation with independent evaluation and provenance."""

import json
import subprocess
import sys
from copy import deepcopy

import ackredit as ack
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from devtools.interaction_collection_cases import build_case, observe
from devtools.validate_aromatic_interactions import _fingerprint
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import (
    Cylinder,
    Disk,
    GaussianKernel,
    Point,
    Sphere,
    SphereAndVector,
)
from pharmacophoremt.io import load_json, load_yaml, to_json, to_yaml
from pharmacophoremt.io.phmt import _to_dict
from pharmacophoremt.modeler import (
    copy_pharmacophore,
    edit_pharmacophore,
    extract_pharmacophore,
    from_interaction_collection,
    get_interaction_site_indices,
)
from pharmacophoremt.pharmacophore import Pharmacophore
from pharmacophoremt.screening import PoseEvaluator


@pytest.fixture(scope="module")
def observed():
    source, ligand, partner = build_case()
    with phmt.attribution():
        model = from_interaction_collection(
            source, observe(source, ligand, partner), ligand, radius=".02 nm"
        )
    model.name, model.description, model.score = "original", "native evidence", 0.9
    return source, ligand, model


def generic_model():
    result = Pharmacophore(name="generic", score=0.8, ref_struct=0)
    result.metadata = dict(literal="2 m", nested=dict(values=[1]))
    shapes = [
        Sphere("[0,0,0] nm", ".1 nm"),
        Disk("[1,0,0] nm", [0, 0, 1], ".1 nm"),
        SphereAndVector("[2,0,0] nm", ".1 nm", [1, 0, 0]),
        GaussianKernel("[3,0,0] nm", ".1 nm"),
        Cylinder("[4,0,0] nm", "[4,0,1] nm", ".1 nm"),
        Point("[5,0,0] nm"),
    ]
    for shape in shapes:
        result.add_interaction_site(
            InteractionSite(
                shape, "hydrophobicity", metadata=dict(original=[shape.shape_name])
            )
        )
    return result


def test_selection_preserves_explicit_order_and_exact_cached_feature_shape_names(
    observed,
):
    _, _, query = observed
    assert get_interaction_site_indices(query, site_indices=[8, 1, 0]) == [8, 1, 0]
    assert get_interaction_site_indices(query, site_indices=0) == [0]
    assert get_interaction_site_indices(query, site_indices=[]) == []
    donors = get_interaction_site_indices(
        query, feature_names="hb donor", shape_names="sphere and vector"
    )
    assert len(donors) == 1
    assert (
        get_interaction_site_indices(
            query, feature_names="hb donor", shape_names="disk"
        )
        == []
    )
    assert get_interaction_site_indices(query, shape_names="gaussian kernel") == []
    with pytest.raises(ArgumentError):
        get_interaction_site_indices(query, feature_names="hb donro")


@pytest.mark.parametrize(
    "indices", [-1, True, "0", [0, 0], [999], [1.0], [[1]], np.array([[0]])]
)
def test_invalid_or_ambiguous_indices_fail_without_an_edit(indices):
    model = generic_model()
    original = deepcopy(_to_dict(model))
    with pytest.raises(ArgumentError):
        edit_pharmacophore(model, site_indices=indices, essential=False, in_place=True)
    assert _to_dict(model) == original


def test_copy_detaches_every_native_site_quantity_and_nested_evidence_without_copying_a_molecule(
    observed,
):
    _, _, original = observed

    class OpaqueMolecule:
        def __deepcopy__(self, memo):
            raise AssertionError("molecular copy must belong to MolSysMT")

    original = copy_pharmacophore(original)
    linked = OpaqueMolecule()
    original.molecular_system = linked
    copied = original.copy(name="alternative")
    assert copied.molecular_system is linked
    assert copied.name == "alternative" and copied.score == original.score
    assert (
        copied.description == original.description
        and copied.ref_struct == original.ref_struct
    )
    copied.interaction_sites[0].features.append("hb acceptor")
    copied.interaction_sites[0].metadata["observations"].clear()
    copied.interaction_sites[0].shape.center += puw.quantity([1, 0, 0], "nm")
    copied.metadata["components"].clear()
    assert len(original.interaction_sites[0].features) == 1
    assert original.interaction_sites[0].metadata["observations"]
    assert original.metadata["components"]
    assert not np.allclose(
        puw.get_value(copied.interaction_sites[0].center, to_unit="nm"),
        puw.get_value(original.interaction_sites[0].center, to_unit="nm"),
    )


def test_subset_keeps_complete_original_native_evidence_and_remaps_only_local_model_indices(
    observed,
):
    _, _, query = observed
    selected = [8, 1]
    result = extract_pharmacophore(
        query, site_indices=selected, name="subset", reason="declared feature choice"
    )
    assert result.score is None and query.score == 0.9
    assert result.metadata["source_model"] == _to_dict(query)
    assert result.metadata["site_map"] == [
        dict(source_site_index=8, site_index=0),
        dict(source_site_index=1, site_index=1),
    ]
    assert [site.metadata for site in result.interaction_sites] == [
        query.interaction_sites[index].metadata for index in selected
    ]
    assert extract_pharmacophore(query, site_indices=[]).n_interaction_sites == 0
    with pytest.raises(ArgumentError):
        PoseEvaluator(extract_pharmacophore(query, site_indices=[]))


def test_curation_uses_no_molecular_operations_or_original_pointer(
    observed, monkeypatch
):
    source, _, query = observed
    before = _fingerprint(source)

    def forbidden(*args, **kwargs):
        raise AssertionError("cached curation must not query or transform molecules")

    with monkeypatch.context() as scoped:
        for name in ("get", "convert", "extract", "copy", "merge", "select"):
            scoped.setattr(msm, name, forbidden)
        for name in ("rotate", "translate"):
            scoped.setattr(msm.structure, name, forbidden)
        changed = edit_pharmacophore(query, weight=2)
        extracted = extract_pharmacophore(changed, site_indices=[0])
        assert extracted.molecular_system is query.molecular_system
    assert _fingerprint(source) == before


@pytest.mark.parametrize(
    "field,value",
    [
        ("weight", -1),
        ("weight", np.nan),
        ("weight", np.inf),
        ("weight", True),
        ("weight", "2"),
        ("weight", [2]),
        ("weight", puw.quantity(2, "ps")),
        ("essential", 1),
        ("essential", "false"),
        ("radius", 0.2),
        ("radius", "-.1 nm"),
        ("radius", "[.1,.2] nm"),
        ("radius", "1 ps"),
    ],
)
def test_failed_multi_site_edits_are_atomic_including_when_digestion_is_bypassed(
    field, value
):
    model = generic_model()
    before = deepcopy(_to_dict(model))
    with pytest.raises(ArgumentError):
        edit_pharmacophore(
            model,
            site_indices=[0, 1],
            in_place=True,
            skip_digestion=True,
            **{field: value},
        )
    assert _to_dict(model) == before


def test_mixed_shapes_refuse_radius_sigma_confusion_without_partial_changes():
    model = generic_model()
    before = deepcopy(_to_dict(model))
    with pytest.raises(ArgumentError, match="editable radius"):
        edit_pharmacophore(model, site_indices=[0, 3], radius=".2 nm", in_place=True)
    assert _to_dict(model) == before
    with pytest.raises(ArgumentError):
        model.set_radius(3, ".2 nm")
    assert _to_dict(model) == before
    model.set_sigma(3, ".2 nm")
    assert float(puw.get_value(model.interaction_sites[3].sigma, to_unit="nm")) == 0.2
    assert model.interaction_sites[3].radius is None
    for indices, fields in [
        ("all", {}),
        ([], dict(weight=1)),
        ([3], dict(radius=".2 nm", sigma=".2 nm")),
    ]:
        with pytest.raises(ArgumentError):
            edit_pharmacophore(model, site_indices=indices, **fields)


def test_radius_updates_preserve_shape_types_and_every_other_geometry_member():
    model = generic_model()
    for index in [0, 1, 2, 4]:
        original = deepcopy(vars(model.interaction_sites[index].shape))
        variant = edit_pharmacophore(model, site_indices=index, radius="200 pm")
        shape = variant.interaction_sites[index].shape
        assert type(shape) is type(model.interaction_sites[index].shape)
        assert float(puw.get_value(shape.radius, to_unit="nm")) == pytest.approx(0.2)
        for key, value in original.items():
            if key == "radius":
                continue
            if puw.is_quantity(value):
                np.testing.assert_array_equal(
                    puw.get_value(getattr(shape, key), to_unit=puw.get_unit(value)),
                    puw.get_value(value),
                )
            else:
                assert getattr(shape, key) == value


def test_class_editors_consume_the_public_tool_and_preserve_site_identity(monkeypatch):
    import pharmacophoremt.modeler.curation as module

    actual = module.edit_pharmacophore
    calls = []

    def observed(*args, **kwargs):
        calls.append(kwargs)
        return actual(*args, **kwargs)

    monkeypatch.setattr(module, "edit_pharmacophore", observed)
    model = generic_model()
    identities = list(model.interaction_sites)
    unchanged_shape = identities[0].shape
    assert model.set_essential([0, 1], False) is None
    assert identities[0].shape is unchanged_shape
    assert model.set_weight(0, 3) is None
    assert model.set_radius([0, 1], ".2 nm") is None
    assert model.set_sigma(3, ".3 nm") is None
    assert all(
        old is new for old, new in zip(identities, model.interaction_sites, strict=True)
    )
    assert len(calls) == 4 and all(call["in_place"] for call in calls)
    assert model.score is None
    lineage = model.metadata
    for _ in range(4):
        lineage = lineage["source_model"]["metadata"]
    assert lineage == dict(literal="2 m", nested=dict(values=[1]))


def test_weight_flag_radius_and_exclusion_changes_have_independent_evaluation_semantics(
    observed,
):
    source, selection, original = observed
    query = copy_pharmacophore(original)
    missing = query.n_interaction_sites
    query.add_interaction_site(
        InteractionSite(Sphere("[9,0,0] nm", ".02 nm"), "hydrophobicity")
    )
    baseline = PoseEvaluator(query).evaluate(source, selection=selection)
    assert baseline["status"] == "not_matched" and baseline[
        "fit_value"
    ] == pytest.approx(9 / 10)
    optional = edit_pharmacophore(query, site_indices=missing, essential=False)
    result = PoseEvaluator(optional).evaluate(source, selection=selection)
    assert result["status"] == "matched" and result["fit_value"] == pytest.approx(
        9 / 10
    )
    weighted = edit_pharmacophore(optional, site_indices=missing, weight=3)
    assert PoseEvaluator(weighted).evaluate(source, selection=selection)[
        "fit_value"
    ] == pytest.approx(9 / 12)
    zero_essential = edit_pharmacophore(query, site_indices=missing, weight=0)
    result = PoseEvaluator(zero_essential).evaluate(source, selection=selection)
    assert result["status"] == "not_matched" and result["fit_value"] == 1
    wider = edit_pharmacophore(query, site_indices=missing, radius="20 nm")
    # The geometric region widens, but one-to-one essential allocation still
    # cannot create a tenth candidate for nine observed participant constraints.
    assert (
        PoseEvaluator(wider).evaluate(source, selection=selection)["status"]
        == "not_matched"
    )
    collision = copy_pharmacophore(original)
    collision.add_interaction_site(
        InteractionSite(
            Sphere("[3,0,0] nm", ".05 nm"), "excluded volume", weight=0, essential=False
        )
    )
    edited_collision = edit_pharmacophore(
        collision,
        site_indices=collision.n_interaction_sites - 1,
        weight=0,
        essential=False,
    )
    result = PoseEvaluator(edited_collision).evaluate(source, selection=selection)
    assert result["status"] == "not_matched" and result["fit_value"] == 1
    assert result["excluded_volume_clashes"]
    positive = extract_pharmacophore(
        edited_collision, site_indices=range(original.n_interaction_sites)
    )
    assert (
        PoseEvaluator(positive).evaluate(source, selection=selection)["status"]
        == "matched"
    )


@pytest.mark.parametrize(
    "format,writer,reader", [("json", to_json, load_json), ("yaml", to_yaml, load_yaml)]
)
def test_lineage_and_original_bibliography_survive_nondefault_unit_persistence(
    observed, tmp_path, format, writer, reader
):
    _, _, original = observed
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        edited = edit_pharmacophore(
            original, site_indices=[0, 1], radius="200 pm", weight=2
        )
        subset = extract_pharmacophore(edited, site_indices=[1, 0])
        path = tmp_path / ("variant." + format)
        writer(subset, path)
        restored = reader(path)
    expected, actual = _to_dict(subset), _to_dict(restored)
    assert restored.metadata == subset.metadata
    for original_site, saved_site in zip(
        expected["interaction_sites"], actual["interaction_sites"], strict=True
    ):
        assert {key: value for key, value in saved_site.items() if key != "shape"} == {
            key: value for key, value in original_site.items() if key != "shape"
        }
        assert saved_site["shape"]["type"] == original_site["shape"]["type"]
        for field in original_site["shape"]:
            if field != "type":
                np.testing.assert_allclose(
                    saved_site["shape"][field],
                    original_site["shape"][field],
                    rtol=0,
                    atol=1e-14,
                )
    assert restored.metadata["source_model"]["metadata"]["source_model"] == _to_dict(
        original
    )
    json.dumps(restored.metadata, allow_nan=False)


def test_declared_radius_change_accepts_known_displacement_without_moving_the_model(
    observed,
):
    source, selection, original = observed
    donor_indices = get_interaction_site_indices(original, feature_names="hb donor")
    query = extract_pharmacophore(original, site_indices=donor_indices)
    candidate = msm.structure.translate(
        source, selection=selection, translation="[0,0,.05] nm", in_place=False
    )
    assert (
        PoseEvaluator(query).evaluate(candidate, selection=selection)["status"]
        == "not_matched"
    )
    relaxed = edit_pharmacophore(
        query, radius=".1 nm", reason="declared tolerance control"
    )
    result = PoseEvaluator(relaxed).evaluate(candidate, selection=selection)
    assert result["status"] == "matched" and result["fit_value"] == 1
    np.testing.assert_array_equal(
        puw.get_value(query.interaction_sites[0].center, to_unit="nm"),
        puw.get_value(relaxed.interaction_sites[0].center, to_unit="nm"),
    )
    np.testing.assert_array_equal(
        puw.get_value(query.interaction_sites[0].direction, to_unit="dimensionless"),
        puw.get_value(relaxed.interaction_sites[0].direction, to_unit="dimensionless"),
    )


def test_native_yaml_normalizes_numpy_literal_text_without_quantity_inference(tmp_path):
    model = generic_model()
    model.metadata["literal"] = np.str_("2 m")
    model.interaction_sites[0].metadata["literal"] = np.str_("1 ps")
    path = tmp_path / "literal.yaml"
    to_yaml(model, path)
    assert "!!python" not in path.read_text()
    restored = load_yaml(path)
    assert (
        type(restored.metadata["literal"]) is str
        and restored.metadata["literal"] == "2 m"
    )
    assert restored.interaction_sites[0].metadata["literal"] == "1 ps"


def test_real_capture_records_curation_without_recrediting_detection_or_cached_copy(
    observed,
):
    _, _, original = observed
    with ack.session("model curation"):
        for _ in range(2):
            with ack.capture("pure cached operations") as cached:
                with phmt.attribution():
                    copied = copy_pharmacophore(original)
                    indices = get_interaction_site_indices(
                        copied, feature_names="aromatic ring"
                    )
                    extract_pharmacophore(copied, site_indices=indices)
            assert cached.attribution.to_dict()["uses"] == []
            with ack.capture("actual radius edit") as run:
                with phmt.attribution():
                    edited = edit_pharmacophore(
                        copied, site_indices=indices, radius=".2 nm"
                    )
            payload = run.attribution.to_dict()
            assert payload["uses"] and any(
                "edit_pharmacophore" in use["used_by"] for use in payload["uses"]
            )
            assert not any(
                "get_pi_pi_interactions" in use["used_by"] for use in payload["uses"]
            )
            assert (
                edited.metadata["source_model"]["metadata"]["attribution"]
                == original.metadata["attribution"]
            )


def test_tracking_failure_preserves_completed_edit(observed, monkeypatch):
    from pharmacophoremt import _ackredit
    from pharmacophoremt._private.smonitor.warnings import AckreditTrackingWarning

    def failed():
        raise RuntimeError("tracking provider failed")

    monkeypatch.setattr(_ackredit, "backend", failed)
    with pytest.warns(AckreditTrackingWarning):
        with phmt.attribution():
            result = edit_pharmacophore(observed[2], weight=2)
    assert all(site.weight == 2 for site in result.interaction_sites)
    assert result.metadata["attribution"]["status"] == "failed"


def test_fresh_process_lazy_attribution_and_genuine_absence():
    script = """
import importlib.abc
import sys
class MissingAckredit(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "ackredit" or fullname.startswith("ackredit."):
            raise ModuleNotFoundError("ackredit absent", name="ackredit")
sys.meta_path.insert(0, MissingAckredit())
import pharmacophoremt as p
from pharmacophoremt.modeler import edit_pharmacophore, copy_pharmacophore
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
assert "ackredit" not in sys.modules
q=p.Pharmacophore()
q.add_interaction_site(InteractionSite(Sphere("[0,0,0] nm", ".1 nm"), "hydrophobicity"))
assert copy_pharmacophore(q).n_interaction_sites==1
assert "ackredit" not in sys.modules
with p.attribution():
    v=edit_pharmacophore(q,radius=".2 nm")
assert v.metadata["attribution"]["status"]=="unavailable"
assert v.metadata["source_model"]["interaction_sites"][0]["shape"]["radius"]==0.1
"""
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
