"""Prepared-native facade controls; no biological or legacy equivalence claim."""

import ast
import inspect
import json
import sys
from importlib.abc import MetaPathFinder

import molsysmt as msm
import numpy as np
import pandas as pd
import pytest

from pharmacophoremt import Pharmacophore
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere, SphereAndVector
from pharmacophoremt.screening import PoseEvaluator, VirtualScreening
from pharmacophoremt.validation.loo import LeaveOneOutValidator
from tests.test_conformer_screening import ensemble, moved_coordinates
from tests.test_pose_evaluation import model_from_source, system
from tests.test_rigid_search import COORDINATES, moved, reference


@pytest.mark.parametrize("method", [None, "legacy", "", [], True])
def test_requires_explicit_native_method(method):
    with pytest.raises(ArgumentError, match="explicitly choose"):
        VirtualScreening(Pharmacophore(), screening_method=method)


@pytest.mark.parametrize(
    "options",
    [
        {"n_conformers": 7},
        {"n_conformers": True},
        {"min_match_ratio": 0.5},
        {"min_match_ratio": True},
    ],
)
def test_retired_preparation_and_partial_essential_threshold_are_refused(options):
    with pytest.raises(ArgumentError):
        VirtualScreening(Pharmacophore(), screening_method="placed", **options)


@pytest.mark.parametrize(
    "options",
    [
        {"point_tolerance": 0.1},
        {"direction_tolerance": 30.0},
    ],
)
def test_explicit_units_are_required(options):
    with pytest.raises(ArgumentError):
        VirtualScreening(Pharmacophore(), screening_method="placed", **options)


def test_placed_records_preserve_indices_negatives_and_original_repeated_sources():
    source = system()
    query, _ = model_from_source(source)
    negative = system(
        coordinates=puw.get_value(msm.get(source, coordinates=True), to_unit="nm")[0]
        + 2
    )
    screen = VirtualScreening(query, screening_method="placed")
    hits = screen.run(iter([source, negative, source]), selection=[0, 1, 2])
    assert [hit["input_index"] for hit in hits] == [0, 2]
    assert all(hit["mol"] is source and hit["conf_id"] == 0 for hit in hits)
    assert all("rd_mol" not in hit for hit in hits)
    assert [entry["status"] for entry in screen.evaluations] == [
        "matched",
        "not_matched",
        "matched",
    ]
    assert screen.evaluations[1]["fit_value"] == 0
    json.dumps(screen.evaluations, allow_nan=False)
    hits[0]["assignments"].clear()
    assert screen.evaluations[0]["assignments"]  # detached hit evidence


def test_native_assignment_and_zero_weight_essential_rules_replace_legacy_reuse():
    source = system()
    query, _ = model_from_source(source)
    site = query.interaction_sites[0]
    query.add_interaction_site(
        InteractionSite(Sphere(site.center, site.radius), "hydrophobicity", weight=0)
    )
    screen = VirtualScreening(query, screening_method="placed")
    assert screen.run([source], selection=[0, 1, 2]) == []
    result = screen.evaluations[0]
    assert result["fit_value"] == 1 and result["status"] == "not_matched"
    assert len(result["assignments"]) == len(result["missing_essential_sites"]) == 1


def test_hits_rank_by_native_weighted_coverage_with_stable_input_ties():
    query = Pharmacophore()
    query.add_interaction_site(
        InteractionSite(Sphere("[.15,0,0] nm", ".02 nm"), "hydrophobicity")
    )
    query.add_interaction_site(
        InteractionSite(
            Sphere("[0,1,0] nm", ".02 nm"), "positive charge", weight=3, essential=False
        )
    )
    partial = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.3, 0, 0]])
    full = system("CCC.[Na+]", [[0, 0, 0], [0.15, 0, 0], [0.3, 0, 0], [0, 1, 0]])
    screen = VirtualScreening(query, screening_method="placed")
    hits = screen.run([partial, full, partial])
    assert [entry["input_index"] for entry in hits] == [1, 0, 2]
    assert [entry["fit_value"] for entry in hits] == [1.0, 0.25, 0.25]
    assert [entry["input_index"] for entry in screen.evaluations] == [0, 1, 2]
    threshold = VirtualScreening(query, screening_method="placed", min_fit_value=0.5)
    assert [entry["input_index"] for entry in threshold.run([partial, full])] == [1]


def test_unit_context_and_optional_attribution_survive_the_facade():
    import pharmacophoremt as phmt

    source = system()
    query, _ = model_from_source(source)
    with puw.context(standard_units=["angstrom", "ps", "degrees"]):
        with phmt.attribution():
            screen = VirtualScreening(
                query,
                screening_method="placed",
                point_tolerance="1 angstrom",
                direction_tolerance="0.5 radian",
            )
            hit = screen.run([source], selection=[0, 1, 2])[0]
    assert hit["fit_value"] == 1
    assert hit["attribution"] == screen.evaluations[0]["attribution"]
    assert hit["attribution"]["status"] == "captured"


def test_coincident_donor_geometry_and_steric_veto_remain_native():
    source = system("[2H]O", [[0.1, 0, 0], [0, 0, 0]])
    query = Pharmacophore()
    query.add_interaction_site(
        InteractionSite(SphereAndVector("[0,0,0] nm", ".15 nm", [-1, 0, 0]), "hb donor")
    )
    screen = VirtualScreening(query, screening_method="placed")
    assert screen.run([source]) == []
    query.interaction_sites[0].shape.direction = np.array([1.0, 0, 0])
    assert VirtualScreening(query, screening_method="placed").run([source])
    query.add_interaction_site(
        InteractionSite(Sphere("[0,0,0] nm", ".05 nm"), "excluded volume")
    )
    vetoed = VirtualScreening(query, screening_method="placed")
    assert vetoed.run([source]) == []
    assert vetoed.evaluations[0]["excluded_volume_clashes"]


def test_rigid_method_recovers_transformed_prepared_frame_without_mutation():
    source, query = reference()
    displaced = moved(source)
    before = puw.get_value(msm.get(displaced, coordinates=True), to_unit="nm").copy()
    screen = VirtualScreening(query, screening_method="rigid")
    hit = screen.run([displaced])[0]
    assert (
        hit["fit_value"] == 1
        and hit["alignment"]["provider"] == "molsysmt.structure.least_rmsd_fit"
    )
    assert hit["conf_id"] == hit["structure_index"] == 0
    np.testing.assert_array_equal(
        puw.get_value(msm.get(displaced, coordinates=True), to_unit="nm"), before
    )


def test_prepared_conformer_order_and_partial_failure_evidence_are_retained():
    _, query = reference()
    source = ensemble(moved_coordinates(), COORDINATES)
    screen = VirtualScreening(query, screening_method="conformers", max_trials=1)
    with pytest.raises(PoseEvaluationError):
        screen.run([source])
    hit = screen.run([source], on_error="record")[0]
    assert hit["conf_id"] == hit["best_conformer_index"] == 1
    assert hit["fit_value"] == 1 and not hit["ensemble"]["complete"]
    assert hit["ensemble"]["proven_maximum"] and hit["ensemble"]["score_resolved"]
    assert hit["conformers"][0]["status"] == "failed"
    assert hit["conformers"][0]["fit_value"] is None


def test_conformer_ties_follow_requested_source_frame_order():
    _, query = reference()
    source = ensemble(COORDINATES, COORDINATES)
    hit = VirtualScreening(query, screening_method="conformers").run(
        [source], structure_indices=[1, 0]
    )[0]
    assert hit["conf_id"] == 1 and hit["ensemble"]["structure_indices"] == [1, 0]


def test_recorded_failures_are_unscored_and_not_hits():
    source = system()
    query, _ = model_from_source(source)
    screen = VirtualScreening(query, screening_method="placed")
    hits = screen.run(
        [source, "invalid source", source], on_error="record", selection=[0, 1, 2]
    )
    assert [hit["input_index"] for hit in hits] == [0, 2]
    failed = screen.evaluations[1]
    assert failed["status"] == "failed" and failed["fit_value"] is None
    assert failed["error"]["code"] == "PHMT-E103"


def test_no_coordinates_never_trigger_local_preparation(monkeypatch):
    class RetiredBackendFinder(MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if fullname.startswith("pharmacophoremt.utils"):
                pytest.fail(
                    "Screening attempted to load a retired local molecular backend"
                )

    monkeypatch.setattr(sys, "meta_path", [RetiredBackendFinder(), *sys.meta_path])
    source, query = reference()
    unprepared = msm.convert(
        msm.convert("smiles:CCC", to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
    )
    screen = VirtualScreening(query, screening_method="conformers")
    assert screen.run([unprepared], on_error="record") == []
    assert screen.evaluations[0]["status"] == "failed"
    assert screen.evaluations[0]["fit_value"] is None


@pytest.mark.parametrize("failure", ["provider", "options", "iterator"])
def test_failed_rebuild_clears_caches_and_does_not_publish_partial_results(failure):
    source = system()
    query, _ = model_from_source(source)
    screen = VirtualScreening(query, screening_method="placed")
    assert screen.run([source], selection=[0, 1, 2])

    def broken():
        yield source
        raise RuntimeError("iterator failure")

    with pytest.raises((ArgumentError, PoseEvaluationError, RuntimeError)):
        if failure == "provider":
            screen.run([source, "invalid"])
        elif failure == "options":
            screen.run([source], on_error="ignore")
        else:
            screen.run(broken())
    assert screen.matches == screen.evaluations == []


def test_scalar_exports_need_no_molecular_conversion_and_sdf_is_explicitly_retired(
    tmp_path, monkeypatch
):
    source = system()
    query, _ = model_from_source(source)
    screen = VirtualScreening(query, screening_method="placed")
    empty = screen.to_dataframe()
    assert list(empty.columns) == [
        "rank",
        "input_index",
        "fit_value",
        "conf_id",
        "status",
    ]
    assert empty.empty
    screen.run([source], selection=[0, 1, 2])

    def forbidden(*args, **kwargs):
        pytest.fail("Scalar formatting cannot perform molecular conversion")

    monkeypatch.setattr(msm, "convert", forbidden)
    frame = screen.to_dataframe()
    assert frame.iloc[0].to_dict() == dict(
        rank=1, input_index=0, fit_value=1.0, conf_id=0, status="matched"
    )
    path = tmp_path / "hits.csv"
    screen.to_csv(path)
    pd.testing.assert_frame_equal(pd.read_csv(path), frame)
    sdf = tmp_path / "hits.sdf"
    with pytest.raises(ArgumentError, match="issues/215"):
        screen.to_sdf(sdf)
    assert not sdf.exists()


def test_loo_requires_explicit_factory_and_uses_native_status_for_negatives():
    source = system()
    query, _ = model_from_source(source)
    negative = system(
        coordinates=puw.get_value(msm.get(source, coordinates=True), to_unit="nm")[0]
        + 2
    )

    class FixedModeler:
        # Adapter control: model selection is held fixed, not consensus validation.
        def __init__(self, training):
            assert len(training) == 2

        def build(self):
            return [query]

    with pytest.raises(ArgumentError, match="explicit"):
        LeaveOneOutValidator(FixedModeler)
    validator = LeaveOneOutValidator(FixedModeler, evaluator_factory=PoseEvaluator)
    report = validator.run([source, negative, source], selection=[0, 1, 2])
    assert report["n_retrieved"] == 2 and report["loo_recall"] == pytest.approx(2 / 3)
    assert report["rounds"][1]["hit"] is False
    assert report["rounds"][1]["evaluation"]["status"] == "not_matched"
    with pytest.raises(PoseEvaluationError):
        validator.run([source, "invalid", source], selection=[0, 1, 2])


def test_facade_and_validation_callers_have_no_direct_molecular_backend_imports():
    import pharmacophoremt.screening.virtual_screening as screening
    import pharmacophoremt.validation.loo as loo
    import pharmacophoremt.validation.retrospective as retrospective

    for module in (screening, loo, retrospective):
        tree = ast.parse(inspect.getsource(module))
        imports = [
            node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
        ]
        imports += [
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        ]
        assert not any(
            name
            and (
                name.startswith("rdkit")
                or name.startswith("molsysmt")
                or name.startswith("pharmacophoremt.utils")
            )
            for name in imports
        )
