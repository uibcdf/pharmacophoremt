"""Prepared native observations replace the implicit complex chemistry engine."""

import ackredit as ack
import molsysmt as msm
import numpy as np
import pytest
from argdigest.core.errors import DigestNotDigestedWarning, UnknownArgumentError

import pharmacophoremt as phmt
from devtools.interaction_collection_cases import build_case, observe
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import ComplexBasedModeler
from tests.test_ionic_interactions import replace_records


@pytest.fixture(scope="module")
def case():
    source, ligand, partner = build_case()
    return source, ligand, observe(source, ligand, partner)


@pytest.mark.parametrize("route", ["class", "default", "named"])
def test_native_collection_controls_and_no_implicit_preparation(
    case, monkeypatch, route
):
    source, ligand, analyses = case
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()

    def forbidden(*args, **kwargs):
        pytest.fail("The complex facade must not prepare or detect interactions")

    monkeypatch.setattr(msm.build, "add_missing_hydrogens", forbidden)
    for owner, name in (
        (msm.interactions.hydrophobic, "get_hydrophobic_interactions"),
        (msm.interactions.hbonds, "get_hbonds"),
        (msm.interactions.ionic, "get_ionic_interactions"),
        (msm.interactions.pi_pi, "get_pi_pi_interactions"),
        (msm.interactions.cation_pi, "get_cation_pi_interactions"),
    ):
        monkeypatch.setattr(owner, name, forbidden)
    options = dict(
        ligand_selection=ligand, interaction_collection=analyses, radius="20 pm"
    )
    if route == "class":
        modeler = ComplexBasedModeler(source, **options)
        assert modeler.system is source and modeler.result is None
        model = modeler.build()
        assert modeler.result is model
    else:
        method = {} if route == "default" else {"method": "complex-based"}
        model = phmt.model(source, **method, **options)
    assert model.n_interaction_sites == 9
    assert sum(site.weight for site in model.interaction_sites) == 9
    assert {site.feature_name for site in model.interaction_sites} == {
        "hydrophobicity",
        "hb donor",
        "positive charge",
        "aromatic ring",
    }
    assert [row["label"] for row in model.metadata["components"]] == list(analyses)
    assert sum(row["action"] == "reused" for row in model.metadata["site_map"]) == 2
    for site in model.interaction_sites:
        assert puw.get_value(site.shape.radius, to_unit="nm") == pytest.approx(0.02)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "missing", ["ligand", "observations", "receptor", "empty", "invalid"]
)
def test_legacy_calls_fail_before_any_molecular_operation(monkeypatch, skip, missing):
    def forbidden(*args, **kwargs):
        pytest.fail("Incomplete configuration must fail before molecular operations")

    for name in ("convert", "select", "get"):
        monkeypatch.setattr(msm, name, forbidden)
    options = dict(ligand_selection=[0], skip_digestion=skip)
    if missing == "ligand":
        options.pop("ligand_selection")
    elif missing == "receptor":
        options["receptor_selection"] = "all"
    elif missing == "empty":
        options["interaction_collection"] = {}
    elif missing == "invalid":
        options["interaction_collection"] = {"not_native": object()}
    with pytest.raises(ArgumentError):
        ComplexBasedModeler(object(), **options)
    with pytest.raises(ArgumentError):
        phmt.model(object(), **options)


@pytest.mark.parametrize(
    "option",
    [
        "hb_dist_max",
        "hyd_dist_max",
        "charge_dist_max",
        "halogen_dist_max",
        "metal_dist_max",
    ],
)
def test_retired_thresholds_are_not_silently_ignored(case, option):
    source, ligand, analyses = case
    with pytest.warns(DigestNotDigestedWarning), pytest.raises(UnknownArgumentError):
        phmt.model(
            source,
            ligand_selection=ligand,
            interaction_collection=analyses,
            **{option: ".3 nm"},
        )


@pytest.mark.parametrize("frames", [[], "all", -1, True, [0, 0], [0.0], [False]])
def test_invalid_or_implicit_frames_clear_previous_result(case, frames):
    source, ligand, analyses = case
    modeler = ComplexBasedModeler(
        source, ligand_selection=ligand, interaction_collection=analyses
    )
    assert modeler.build().n_interaction_sites == 9
    with pytest.raises(ArgumentError):
        modeler.build(structure_indices=frames)
    assert modeler.result is None


def test_evaluated_empty_and_uncovered_are_distinct_and_singleton_shape_is_retained(
    case,
):
    source, ligand, analyses = case
    modeler = ComplexBasedModeler(
        source,
        ligand_selection=ligand,
        interaction_collection={"empty": analyses["ionic_empty"]},
    )
    for frames in (None, 0, np.int64(0), [0]):
        model = modeler.build(frames)
        assert model.n_interaction_sites == 0
        assert model.metadata["components"][0]["metadata"][
            "evaluated_structure_indices"
        ] == [0]
        assert modeler.result is model
    modeler.interaction_collection = {
        "not_evaluated": analyses["ionic_empty"].invalidate_structures([0])
    }
    with pytest.raises(ArgumentError):
        modeler.build()
    assert modeler.result is None


@pytest.mark.parametrize("failure", ["state", "maps", "profile"])
def test_native_collection_failures_propagate_without_a_partial_model(case, failure):
    source, ligand, analyses = case
    original = analyses["pi_prolif"]
    parameters = dict(original.parameters)
    options = {}
    if failure == "state":
        parameters["chemical_state_index"] = 1
    elif failure == "maps":
        options["atom_source_indices"] = list(range(20, 40))
    else:
        parameters["profile"] = "unknown"
    collection = dict(analyses)
    collection["pi_prolif"] = replace_records(
        original, parameters=parameters, **options
    )
    modeler = ComplexBasedModeler(
        source, ligand_selection=ligand, interaction_collection=collection
    )
    with pytest.raises(ArgumentError):
        modeler.build()
    assert modeler.result is None


def test_multiple_frames_return_in_caller_order_and_any_failure_clears_result():
    source, ligand, partner = build_case()
    coordinates = msm.get(source, coordinates=True)
    source.structures.append(coordinates=coordinates)
    observed = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source,
        distance_threshold=".4 nm",
        selection=ligand,
        selection_2=partner,
        selection_mode="between",
        structure_indices=[0, 1],
        pbc=False,
    )
    options = dict(
        ligand_selection=ligand, interaction_collection={"hydrophobic": observed}
    )
    modeler = ComplexBasedModeler(source, **options)
    for models in (
        modeler.build([1, 0]),
        phmt.model(source, structure_indices=[1, 0], **options),
    ):
        assert isinstance(models, list)
        assert [model.ref_struct for model in models] == [1, 0]
        assert [
            model.metadata["components"][0]["metadata"]["structure_index"]
            for model in models
        ] == [1, 0]
        assert [model.n_interaction_sites for model in models] == [6, 6]
    modeler.interaction_collection = {"partial": observed.invalidate_structures([1])}
    with pytest.raises(ArgumentError):
        modeler.build([0, 1])
    assert modeler.result is None


def test_facade_preserves_native_capture_and_saved_evidence(case, tmp_path):
    source, ligand, analyses = case
    with ack.session("native complex facade"):
        with ack.capture("cached observations") as run:
            with phmt.attribution():
                model = phmt.model(
                    source, ligand_selection=ligand, interaction_collection=analyses
                )
        uses = run.attribution.to_dict()["uses"]
        assert any("from_interaction_collection" in use["used_by"] for use in uses)
        assert not any(
            "get_pi_pi_interactions" in use["used_by"]
            or "get_ionic_interactions" in use["used_by"]
            for use in uses
        )
        assert model.metadata["attribution"]["references"]["items"]
        before = ack.get_attribution().to_dict()
        target = tmp_path / "native_complex.json"
        to_json(model, target)
        loaded = load_json(target)
        assert loaded.metadata == model.metadata
        assert [site.metadata for site in loaded.interaction_sites] == [
            site.metadata for site in model.interaction_sites
        ]
        assert ack.get_attribution().to_dict() == before
