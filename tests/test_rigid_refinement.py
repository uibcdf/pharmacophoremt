"""Pair geometry, real-provider policy counterexamples and refinement accounting."""

import json
import math
from copy import deepcopy

import ackredit
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from devtools.rigid_consensus_cases import build_case, load_cases
from devtools.rigid_refinement_cases import build_refinement_case, load_refinement_cases
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError, CliqueLimitError
from pharmacophoremt.modeler import from_rigid_ligands, get_features
from pharmacophoremt.screening import (
    evaluate_feature_correspondence,
    refine_rigid_feature_correspondences,
)
from pharmacophoremt.validation import summarize_rigid_consensus
from tests.test_aligned_consensus import inventory


def value(record, unit):
    return puw.get_value(
        puw.QuantityRecord.from_dict(record).to_quantity(), to_unit=unit
    )


@pytest.fixture(
    scope="module", params=load_refinement_cases(), ids=lambda case: case["case_id"]
)
def prepared(request):
    reference, source = build_refinement_case(request.param)
    return (
        request.param,
        source,
        get_features(reference, features=["hb donor"]),
        get_features(source, features=["hb donor"]),
    )


def refine(prepared, policy, **options):
    case, source, target, source_inventory = prepared
    kwargs = dict(case["parameters"], **options)
    return refine_rigid_feature_correspondences(
        source,
        target,
        case["correspondences"],
        features=["hb donor"],
        feature_inventory=source_inventory,
        orientation_policy=policy,
        **kwargs,
    )


def test_pair_evaluation_agrees_with_scalar_geometry_and_preserves_ownership(
    monkeypatch,
):
    first = inventory(
        [[0, 0, 0], [0, 1, 0], [0, 0, 1]],
        ["hb donor", "aromatic ring", "positive charge"],
        directions=[[1, 0, 0], None, None],
        normals=[None, [0, 0, 1], None],
    )
    second = inventory(
        [[0.2, 0, 0], [0, 1, 0], [0, 0, 1]],
        ["hb donor", "aromatic ring", "negative charge"],
        directions=[[math.sqrt(3) / 2, 0.5, 0], None, None],
        normals=[None, [0, 0, -1], None],
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("geometry evaluation must not access a molecular system")

    monkeypatch.setattr(msm, "get", forbidden)
    report = evaluate_feature_correspondence(
        first,
        second,
        [[0, 0], [1, 1], [2, 2]],
        distance_tolerance="2.01 angstrom",
        direction_tolerance="30 degrees",
    )
    assert report["invalid_kind_pairs"] == [[2, 2]]
    assert report["invalid_position_pairs"] == []
    assert report["invalid_orientation_pairs"] == [[2, 2]]
    assert value(report["position_rmsd"], "nm") == pytest.approx(math.sqrt(0.04 / 3))
    assert value(
        report["pair_tests"][0]["orientation_deviation"], "degrees"
    ) == pytest.approx(30)
    assert value(
        report["pair_tests"][1]["orientation_deviation"], "degrees"
    ) == pytest.approx(0)
    assert not report["all_pairs_valid"] and report["complete"]
    first["features"][0]["center"] = puw.quantity([99, 0, 0], "nm")
    assert value(report["pair_tests"][0]["center_deviation"], "nm") == pytest.approx(
        0.2
    )
    json.dumps(report, allow_nan=False)
    empty = evaluate_feature_correspondence(inventory([]), inventory([]), [])
    assert empty["all_pairs_valid"] and empty["position_rmsd"] is None


def test_inclusive_positional_boundary_and_directed_vector_reversal():
    first = inventory([[0, 0, 0]], ["hb donor"], directions=[[1, 0, 0]])
    second = inventory([[0.2, 0, 0]], ["hb donor"], directions=[[-1, 0, 0]])
    at_boundary = evaluate_feature_correspondence(
        first, second, [[0, 0]], distance_tolerance=".2 nm"
    )
    assert (
        at_boundary["all_positions_valid"] and not at_boundary["all_orientations_valid"]
    )
    beyond = evaluate_feature_correspondence(
        first, second, [[0, 0]], distance_tolerance=".199 nm"
    )
    assert not beyond["all_positions_valid"]
    assert value(
        at_boundary["pair_tests"][0]["orientation_deviation"], "degrees"
    ) == pytest.approx(180)


def test_pair_evaluation_matches_independent_scalar_oracle():
    rng = np.random.default_rng(29)
    centers = rng.uniform(-1, 1, (2, 8, 3))
    directions = rng.normal(size=(2, 8, 3))
    inventories = [
        inventory(centers[i], ["hb donor"] * 8, directions=directions[i].tolist())
        for i in (0, 1)
    ]
    report = evaluate_feature_correspondence(
        *inventories,
        [[i, i] for i in range(8)],
        distance_tolerance="1.1 nm",
        direction_tolerance="50 degrees",
    )
    for i, test in enumerate(report["pair_tests"]):
        distance = math.dist(centers[0, i], centers[1, i])
        left, right = directions[:, i]
        cosine = sum(float(x * y) for x, y in zip(left, right)) / (
            math.sqrt(sum(float(x * x) for x in left))
            * math.sqrt(sum(float(y * y) for y in right))
        )
        angle = math.degrees(math.acos(max(-1, min(1, cosine))))
        assert value(test["center_deviation"], "nm") == pytest.approx(distance)
        assert value(test["orientation_deviation"], "degrees") == pytest.approx(angle)
        assert test["position_valid"] == (distance <= 1.1)
        assert test["orientation_valid"] == (angle <= 50)


def test_nontriplet_seed_is_supported_and_inputs_are_validated_before_fitting(
    monkeypatch,
):
    import pharmacophoremt.screening.rigid_refinement as module

    case = load_cases()[0]
    reference, source = [ligand["molecular_system"] for ligand in build_case(case)]
    target = get_features(reference, features=case["parameters"]["features"])
    inv = get_features(source, features=case["parameters"]["features"])
    pairs = [[i, i] for i in range(5)]
    parameters = {
        key: val for key, val in case["parameters"].items() if key != "min_sites"
    }
    result = refine_rigid_feature_correspondences(
        source, target, [pairs], feature_inventory=inv, **parameters
    )
    assert result["report"]["n_fits"] == 1 and len(result["placements"]) == 1

    def forbidden(*args, **kwargs):
        raise AssertionError("invalid supplied axes must fail before fitting")

    monkeypatch.setattr(module, "_fit_feature_mapping", forbidden)
    with pytest.raises(ArgumentError):
        refine_rigid_feature_correspondences(
            source,
            target,
            [pairs, [[0, 0], [1, 1], [2, 99]]],
            feature_inventory=inv,
            **parameters,
        )


@pytest.mark.parametrize(
    "pairs",
    [
        [[0, 0], [0, 1]],
        [[0, 0], [1, 0]],
        [[0, 9]],
        [[True, False]],
        [[0.0, 0.0]],
        [[-1, 0]],
    ],
)
def test_pair_evaluation_rejects_invalid_index_contract(pairs):
    with pytest.raises(ArgumentError):
        evaluate_feature_correspondence(
            inventory([[0, 0, 0], [1, 0, 0]]), inventory([[0, 0, 0], [1, 0, 0]]), pairs
        )


@pytest.mark.parametrize("policy", ["final", "each_step"])
def test_real_provider_policy_counterexamples_and_immutable_sources(prepared, policy):
    case, source, target, _ = prepared
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    result = refine(prepared, policy)
    report = result["report"]
    expected = case["expected"][policy]
    assert len(result["placements"]) == expected["n_placements"]
    assert report["n_fits"] == expected["n_fits"]
    assert (
        max((len(p["matches"]["matches"]) for p in result["placements"]), default=0)
        == expected["max_matches"]
    )
    seed = report["refinement_seeds"][0]
    assert seed["n_fits"] == len(seed["steps"])
    assert seed["n_accepted_steps"] + seed["n_rejected_steps"] == seed["n_fits"]
    for placement in result["placements"]:
        assert evaluate_feature_correspondence(
            target,
            placement["inventory"],
            placement["matches"]["matches"],
            **{k: v for k, v in case["parameters"].items() if k != "min_matches"},
        )["all_pairs_valid"]
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
    assert "molecular_system" not in json.dumps(report)
    json.dumps(report, allow_nan=False)
    if case["case_id"] == "orientation_recovery":
        assert value(
            seed["steps"][0]["pair_evaluation"]["pair_tests"][0][
                "orientation_deviation"
            ],
            "degrees",
        ) == pytest.approx(45)
        if policy == "final":
            assert not seed["steps"][0]["matches"]["matches"]
            assert result["placements"][0]["selected_step_index"] == 1
    if case["case_id"] == "orientation_blocking" and policy == "each_step":
        assert seed["permanently_rejected_pairs"] == [[3, 3], [4, 4]]
        assert seed["steps"][2]["previous_accepted_step"] == 0
        assert seed["steps"][3]["correspondence"] == [[0, 0], [1, 1], [2, 2], [3, 4]]
    if case["case_id"] == "orientation_checkpoint":
        assert result["placements"][0]["selected_step_index"] == 0
        assert len(result["placements"][0]["matches"]["matches"]) == 3


def test_fit_budget_and_provider_failure_never_return_partial_science(
    prepared, monkeypatch
):
    import pharmacophoremt.screening.rigid_refinement as module

    real = module._fit_feature_mapping
    calls = []

    def observed(*args, **kwargs):
        calls.append(1)
        return real(*args, **kwargs)

    monkeypatch.setattr(module, "_fit_feature_mapping", observed)
    with pytest.raises(CliqueLimitError) as exhausted:
        refine(prepared, "final", max_fits=1)
    assert exhausted.value.code == "PHMT-E107" and len(calls) == 1

    def failed(*args, **kwargs):
        raise RuntimeError("controlled provider failure")

    monkeypatch.setattr(module, "_fit_feature_mapping", failed)
    with pytest.raises(RuntimeError, match="controlled provider failure"):
        refine(prepared, "final")


def test_duplicate_seeds_and_empty_requests_and_invalid_policies(prepared):
    case, source, target, inv = prepared
    empty = refine_rigid_feature_correspondences(
        source, target, [], feature_inventory=inv, features=["hb donor"]
    )
    assert empty["report"]["n_fits"] == 0 and empty["placements"] == []
    result = refine_rigid_feature_correspondences(
        source,
        target,
        case["correspondences"] * 2,
        feature_inventory=inv,
        features=["hb donor"],
        **case["parameters"],
    )
    assert result["report"]["n_fits"] == 2 * case["expected"]["final"]["n_fits"]
    assert [s["proposal_index"] for s in result["report"]["refinement_seeds"]] == [0, 1]
    with pytest.raises(ArgumentError):
        refine(prepared, "unknown")


def test_consumer_composes_public_refinement_and_summary_counts_trials(monkeypatch):
    import pharmacophoremt.screening.rigid_refinement as module

    real = module.refine_rigid_feature_correspondences
    calls = []

    def observed(*args, **kwargs):
        calls.append(kwargs["orientation_policy"])
        return real(*args, **kwargs)

    monkeypatch.setattr(module, "refine_rigid_feature_correspondences", observed)
    case = load_cases()[0]
    result = from_rigid_ligands(
        build_case(case),
        correspondence_strategy="ranked_triplet_seeds",
        n_seeds=1,
        refinement_strategy="greedy",
        orientation_policy="each_step",
        **case["parameters"],
    )
    assert calls == ["each_step"]
    summary = summarize_rigid_consensus(json.loads(json.dumps(result["report"])))
    assert (
        summary["n_fits"] == 3
        and summary["n_models"] == 1
        and summary["max_joint_sites"] == 5
    )
    assert summary["sources"][1]["n_proposals"] == 1
    assert summary["sources"][1]["n_accepted_refinement_steps"] == 3
    for key in ("n_fits", "n_accepted_steps"):
        corrupted = deepcopy(result["report"])
        corrupted["source_alignments"][1]["refinement"]["refinement_seeds"][0][key] += 1
        with pytest.raises(ArgumentError):
            summarize_rigid_consensus(corrupted)
    corrupted = deepcopy(result["report"])
    corrupted["source_alignments"][1]["accepted_placements"][0][
        "selected_step_index"
    ] = 999
    with pytest.raises(ArgumentError):
        summarize_rigid_consensus(corrupted)
    with pytest.raises(ArgumentError):
        from_rigid_ligands(build_case(case), orientation_policy="each_step")
    ligands = build_case(case)
    ligands.append(
        dict(ligand_id="third", molecular_system=ligands[1]["molecular_system"])
    )
    with pytest.raises(CliqueLimitError):
        from_rigid_ligands(
            ligands,
            correspondence_strategy="ranked_triplet_seeds",
            n_seeds=1,
            refinement_strategy="greedy",
            max_fits=3,
            **case["parameters"],
        )


def test_actual_ackredit_records_both_executed_policies_and_no_empty_refinement(
    prepared,
):
    with ackredit.session("refinement policies"):
        for policy in ("final", "each_step"):
            with phmt.attribution():
                result = refine(prepared, policy)
            payload = result["attribution"]
            declarations = [
                d
                for d in payload["host_references"]
                if d["record"].get("doi") == "10.3390/molecules26237201"
            ]
            assert len(declarations) == 1
            context = declarations[0]["context"]
            assert (
                context["paper_section"] == "2.2.2"
                and context["orientation_policy"] == policy
            )
            assert "translation_rescue" in context["excluded_stages"]
            assert declarations[0]["roles"] == ["methodological_basis"]
            assert payload["status"] == "captured"
            assert "10.3390/molecules26237201" in phmt.attribution_report(
                payload, format="bibtex"
            )
        case, source, target, inv = prepared
        with phmt.attribution():
            empty = refine_rigid_feature_correspondences(
                source, target, [], feature_inventory=inv, features=["hb donor"]
            )
        assert not any(
            d["record"].get("doi") == "10.3390/molecules26237201"
            for d in empty["attribution"]["host_references"]
        )
