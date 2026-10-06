"""Bounded exhaustive clique/package oracles and real-provider workflow controls."""

import itertools
import json
import math
import warnings

import ackredit as ack
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import _ackredit
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError, CliqueLimitError
from pharmacophoremt.io.phmt import load_json, to_json
from pharmacophoremt.modeler import (
    from_aligned_ligand_cliques,
    get_aligned_consensus_hypotheses,
    get_aligned_feature_cliques,
)
from tests.test_aligned_consensus import inventory
from tests.test_attribution import run_reader
from tests.test_pose_evaluation import system
from tests.test_reference_ligand import benzene
from tests.test_rigid_search import COORDINATES, FAMILIES, reference


def keys(groups, identities):
    return {frozenset((identities[i], j) for i, j in group) for group in groups}


def exhaustive_cliques(inventories, identities, tolerance, angle):
    """Subset oracle: no graph library, production helpers or solver calls."""
    occurrences = [
        (i, j)
        for i, item in enumerate(inventories)
        for j in range(len(item["features"]))
    ]
    accepted = []
    for size in range(1, len(occurrences) + 1):
        for subset in itertools.combinations(occurrences, size):
            if len({i for i, _ in subset}) != size:
                continue
            valid = True
            for (i, j), (k, second_feature) in itertools.combinations(subset, 2):
                a, b = (
                    inventories[i]["features"][j],
                    inventories[k]["features"][second_feature],
                )
                if a["kind"] != b["kind"]:
                    valid = False
                    break
                one = puw.get_value(a["center"], to_unit="nm")
                two = puw.get_value(b["center"], to_unit="nm")
                if math.dist(one, two) > tolerance:
                    valid = False
                    break
                field = "direction" if a["kind"] == "hb donor" else "normal"
                if a[field] is not None:
                    one, two = (puw.get_value(record[field]) for record in (a, b))
                    cosine = sum(x * y for x, y in zip(one, two)) / (
                        math.sqrt(sum(x * x for x in one))
                        * math.sqrt(sum(x * x for x in two))
                    )
                    if field == "normal":
                        cosine = abs(cosine)
                    if math.degrees(math.acos(max(-1, min(1, cosine)))) > angle + 1e-12:
                        valid = False
                        break
            if valid:
                accepted.append(frozenset(subset))
    maximal = [
        subset for subset in accepted if not any(subset < other for other in accepted)
    ]
    return keys(maximal, identities)


def exhaustive_packages(groups, min_support):
    """Enumerate all subsets and test joint intersection independently."""
    accepted = []
    for size in range(1, len(groups) + 1):
        for subset in itertools.combinations(range(len(groups)), size):
            members = [tuple(pair) for index in subset for pair in groups[index]]
            if len(members) != len(set(members)):
                continue
            common = set(i for i, _ in groups[subset[0]])
            for index in subset[1:]:
                common.intersection_update(i for i, _ in groups[index])
            if len(common) >= min_support:
                accepted.append(frozenset(subset))
    return {
        subset for subset in accepted if not any(subset < other for other in accepted)
    }


def test_cliques_match_independent_subset_oracle():
    rng = np.random.default_rng(671)
    identities = ["c", "a", "b"]
    for _ in range(12):
        sources = [
            inventory(
                rng.uniform(0, 0.5, (2, 3)), kinds=["hb acceptor", "hydrophobicity"]
            )
            for _ in identities
        ]
        result = get_aligned_feature_cliques(
            sources, ligand_ids=identities, min_support=1, distance_tolerance="0.35 nm"
        )
        assert keys(result["groups"], identities) == exhaustive_cliques(
            sources, identities, 0.35, 30
        )
        assert result["complete"] is True


def test_all_maximal_sizes_are_retained_and_empty_ligands_count():
    sources = [
        inventory([[0, 0, 0], [1, 0, 0]]),
        inventory([[0.03, 0, 0], [1.02, 0, 0]]),
        inventory([[0.06, 0, 0]]),
        inventory([]),
    ]
    result = get_aligned_consensus_hypotheses(
        sources, ligand_ids=["a", "b", "c", "empty"], distance_tolerance="0.10 nm"
    )
    assert sorted(len(group) for group in result["correspondence_groups"]) == [2, 3]
    assert sorted(site["support_fraction"] for site in result["candidate_sites"]) == [
        0.5,
        0.75,
    ]
    assert len(result["hypotheses"]) == 1
    assert result["hypotheses"][0]["joint_support_count"] == 2
    assert result["hypotheses"][0]["joint_support_fraction"] == 0.5
    np.testing.assert_allclose(
        puw.get_value(result["candidate_sites"][0]["center"], to_unit="nm"),
        [0.03, 0, 0],
    )
    assert result["hypotheses"][0]["site_indices"] == [0, 1]


def test_overlapping_occurrences_form_separate_hypotheses_with_exact_budget():
    sources = [inventory([[0, 0, 0], [0, 0, 0]]), inventory([[0.05, 0, 0]])]
    result = get_aligned_consensus_hypotheses(
        sources, ligand_ids=["a", "b"], distance_tolerance="0.05 nm", max_combinations=3
    )
    assert len(result["candidate_sites"]) == len(result["hypotheses"]) == 2
    assert result["n_combinations"] == 3
    assert [item["site_indices"] for item in result["hypotheses"]] == [[0], [1]]
    assert {
        frozenset(item["site_indices"]) for item in result["hypotheses"]
    } == exhaustive_packages(result["correspondence_groups"], 2)
    with pytest.raises(CliqueLimitError) as caught:
        get_aligned_consensus_hypotheses(
            sources, ligand_ids=["a", "b"], max_combinations=2
        )
    assert caught.value.code == "PHMT-E107"
    assert caught.value.extra["complete"] is False


def test_joint_support_is_not_pairwise_support():
    kinds = ["hydrophobicity", "hb acceptor", "positive charge"]
    # Site supporters: ABC, BCD, ACD. Every pair shares two ligands,
    # while the triple shares only C. All three pair hypotheses must survive.
    memberships = [(0, 2), (0, 1), (0, 1, 2), (1, 2)]
    sources = [
        inventory([[j, 0, 0] for j in member], kinds=[kinds[j] for j in member])
        for member in memberships
    ]
    result = get_aligned_consensus_hypotheses(
        sources, ligand_ids=["a", "b", "c", "d"], min_sites=2
    )
    assert len(result["hypotheses"]) == 3
    assert all(
        len(item["site_indices"]) == item["joint_support_count"] == 2
        for item in result["hypotheses"]
    )
    actual = {frozenset(item["site_indices"]) for item in result["hypotheses"]}
    assert actual == exhaustive_packages(result["correspondence_groups"], 2)
    none = get_aligned_consensus_hypotheses(
        sources, ligand_ids=["a", "b", "c", "d"], min_sites=3
    )
    assert none["hypotheses"] == [] and none["complete"]


def test_hypothesis_packages_match_bounded_subset_oracle():
    rng = np.random.default_rng(25)
    for _ in range(10):
        sources = [inventory(rng.uniform(0, 0.3, (2, 3))) for _ in range(3)]
        result = get_aligned_consensus_hypotheses(
            sources, ligand_ids=["a", "b", "c"], distance_tolerance="0.18 nm"
        )
        assert {
            frozenset(item["site_indices"]) for item in result["hypotheses"]
        } == exhaustive_packages(result["correspondence_groups"], 2)


def test_donor_directions_and_aromatic_axes_have_distinct_semantics():
    donors = [
        inventory([[0, 0, 0]], kinds=["hb donor"], directions=[[1, 0, 0]]),
        inventory([[0, 0, 0]], kinds=["hb donor"], directions=[[-1, 0, 0]]),
    ]
    result = get_aligned_consensus_hypotheses(
        donors, ligand_ids=["a", "b"], direction_tolerance="0 degrees"
    )
    assert result["candidate_sites"] == result["hypotheses"] == []
    rings = [
        inventory([[0, 0, 0]], kinds=["aromatic ring"], normals=[[0, 0, 1]]),
        inventory([[0, 0, 0]], kinds=["aromatic ring"], normals=[[0, 0, -1]]),
    ]
    result = get_aligned_consensus_hypotheses(
        rings, ligand_ids=["b", "a"], direction_tolerance="0 degrees"
    )
    assert len(result["hypotheses"]) == 1
    assert result["candidate_sites"][0]["orientation_reference"]["ligand_id"] == "a"
    assert keys(result["discovery"]["groups"], ["b", "a"]) == exhaustive_cliques(
        rings, ["b", "a"], 0.15, 0
    )


def test_reordering_sources_and_features_preserves_corresponding_patterns():
    sources = [
        inventory([[0, 0, 0], [1, 0, 0]]),
        inventory([[0.01, 0, 0], [1.02, 0, 0]]),
        inventory([[0.03, 0, 0], [1.04, 0, 0]]),
    ]
    first = get_aligned_consensus_hypotheses(sources, ligand_ids=["z", "a", "m"])
    second = get_aligned_consensus_hypotheses(
        [sources[1], sources[2], sources[0]], ligand_ids=["a", "m", "z"]
    )
    assert keys(first["correspondence_groups"], ["z", "a", "m"]) == keys(
        second["correspondence_groups"], ["a", "m", "z"]
    )
    assert first["hypotheses"] == second["hypotheses"]
    sources[1]["features"].reverse()
    third = get_aligned_consensus_hypotheses(sources, ligand_ids=["z", "a", "m"])
    remapped = [
        [[i, 1 - j if i == 1 else j] for i, j in group]
        for group in third["correspondence_groups"]
    ]
    assert keys(first["correspondence_groups"], ["z", "a", "m"]) == keys(
        remapped, ["z", "a", "m"]
    )


def test_pattern_absent_from_first_ligand_is_discovered():
    sources = [inventory([]), inventory([[0, 0, 0]]), inventory([[0.04, 0, 0]])]
    result = get_aligned_consensus_hypotheses(sources, ligand_ids=["first", "a", "b"])
    assert len(result["hypotheses"]) == 1
    assert result["candidate_sites"][0]["support_fraction"] == pytest.approx(2 / 3)


def test_graph_limit_prevents_solver_and_counts_unsupported_cliques(monkeypatch):
    import networkx as nx

    sources = [inventory([[0, 0, 0]]), inventory([[1, 0, 0]])]
    with pytest.raises(CliqueLimitError):
        get_aligned_feature_cliques(sources, ligand_ids=["a", "b"], max_cliques=1)
    resolved = get_aligned_feature_cliques(
        sources, ligand_ids=["a", "b"], max_cliques=2
    )
    assert resolved["groups"] == [] and len(resolved["rejected_groups"]) == 2

    def forbidden(*args, **kwargs):
        raise AssertionError("solver must not run beyond the graph bound")

    monkeypatch.setattr(nx, "find_cliques", forbidden)
    with pytest.raises(CliqueLimitError) as caught:
        get_aligned_feature_cliques(sources, ligand_ids=["a", "b"], max_graph_nodes=1)
    assert (
        "nodes" in str(caught.value) and caught.value.extra["stage"] == "feature_graph"
    )


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(max_graph_nodes=True),
        dict(max_cliques=0),
        dict(max_combinations=2.5),
        dict(min_sites=0),
        dict(distance_tolerance=0.15),
        dict(direction_tolerance="181 degrees"),
        dict(ligand_ids=["same", "same"]),
        dict(min_support=3),
    ],
)
def test_invalid_contracts_raise_catalog_diagnostics(kwargs):
    sources = [inventory([[0, 0, 0]]), inventory([[0, 0, 0]])]
    with pytest.raises(ArgumentError):
        get_aligned_consensus_hypotheses(
            sources, **(dict(ligand_ids=["a", "b"]) | kwargs)
        )


def test_empty_completion_and_attribution_credit_only_reached_solver():
    with ack.session("empty graph"):
        with phmt.attribution():
            empty = get_aligned_consensus_hypotheses(
                [inventory([]), inventory([])], ligand_ids=["a", "b"]
            )
        assert empty["complete"] and empty["hypotheses"] == []
        assert empty["attribution"]["status"] == "captured"
        assert "10.1145/362342.362367" not in json.dumps(empty["attribution"])
    with ack.session("evaluated negative"):
        with phmt.attribution():
            negative = get_aligned_consensus_hypotheses(
                [inventory([[0, 0, 0]]), inventory([[1, 0, 0]])], ligand_ids=["a", "b"]
            )
        assert negative["hypotheses"] == []
        assert "10.1145/362342.362367" in json.dumps(negative["attribution"])


def test_real_workflow_preserves_sources_frames_models_and_references(tmp_path):
    source, _ = reference()
    second = msm.structure.translate(
        source, translation=puw.quantity([[[0.02, 0, 0]]], "nm"), in_place=False
    )
    before = [
        puw.get_value(msm.get(item, coordinates=True), to_unit="nm").copy()
        for item in (source, second)
    ]
    ligands = [
        dict(ligand_id="a", molecular_system=source),
        dict(ligand_id="b", molecular_system=second),
    ]
    with ack.session("application") as application:
        with ack.capture("workflow") as workflow:
            with phmt.attribution():
                first = from_aligned_ligand_cliques(
                    ligands,
                    features=FAMILIES,
                    distance_tolerance="0.06 nm",
                    radius="0.06 nm",
                    min_sites=5,
                )
                reused = from_aligned_ligand_cliques(
                    ligands,
                    features=FAMILIES,
                    distance_tolerance="0.06 nm",
                    radius="0.06 nm",
                    min_sites=5,
                )
        assert ack.current_session() is application
        assert len(first["models"]) == 1
        model = first["models"][0]
        assert model.n_interaction_sites == 5
        assert first["report"]["hypotheses"][0]["joint_ligand_ids"] == ["a", "b"]
        assert [item["ligand_id"] for item in model.metadata["sources"]] == ["a", "b"]
        assert all(
            member["ligand_id"] in {"a", "b"}
            for site in model.interaction_sites
            for member in site.metadata["members"]
        )
        assert (
            first["attribution"]["references"]["items"]
            == reused["attribution"]["references"]["items"]
        )
        assert {item["id"] for item in first["attribution"]["references"]["items"]} <= {
            item["id"] for item in workflow.attribution.to_dict()["items"]
        }
        payload = model.metadata["attribution"]
        assert payload == first["attribution"]
        assert payload is not first["attribution"]
        declarations = payload["host_references"]
        software = [
            entry for entry in declarations if entry["record"]["title"] == "NetworkX"
        ]
        assert (
            len(software) == 1
            and software[0]["record"]["version"] == __import__("networkx").__version__
        )
        assert software[0]["roles"] == ["executed_software"]
        descriptions = [
            entry
            for entry in declarations
            if entry["record"]["id"] == "pharmacophoremt:networkx:paper:2008"
        ]
        assert len(descriptions) == 1 and descriptions[0]["roles"] == [
            "software_description"
        ]
        papers = [
            entry
            for entry in declarations
            if entry["record"].get("doi")
            in {"10.1145/362342.362367", "10.1016/j.tcs.2006.06.015"}
        ]
        assert len(papers) == 2 and all(
            entry["roles"] == ["reference_implementation"] for entry in papers
        )
        assert "10.1021/ci7000583" not in json.dumps(payload)
        assert "10.1021/ci8002478" not in json.dumps(payload)
        assert "10.1109/TAES.2016.140952" not in json.dumps(payload)
        evaluator = phmt.screening.PoseEvaluator(model)
        assert (
            evaluator.evaluate(source)["status"]
            == evaluator.evaluate(second)["status"]
            == "matched"
        )
        assert (
            evaluator.evaluate(system("[Na+]", [[2, 0, 0]]))["status"] == "not_matched"
        )
        path = tmp_path / "clique.json"
        to_json(model, path)
        assert load_json(path).metadata == model.metadata
        assert load_json(path).metadata["hypothesis"]["joint_ligand_ids"] == ["a", "b"]
        before_read = ack.get_attribution().to_dict()
        assert "Tomita" in phmt.attribution_report(payload, format="bibtex")
        assert ack.get_attribution().to_dict() == before_read
    for item, coordinates in zip((source, second), before):
        np.testing.assert_array_equal(
            puw.get_value(msm.get(item, coordinates=True), to_unit="nm"), coordinates
        )
    reader = """
import sys
import ackredit as ack
from pharmacophoremt.io.phmt import load_json
with ack.session('fresh reader'):
    model = load_json(sys.argv[1])
    payload = model.metadata['attribution']['references']
    assert any(item.get('doi') == '10.1145/362342.362367' for item in payload['items'])
    assert ack.Attribution.from_dict(payload).report(format='bibtex')
    assert ack.get_used_items() == {}
"""
    run_reader(reader, path)


def test_aromatic_units_and_explicit_frame_selection():
    source, _ = reference()
    source.structures.append(
        coordinates=puw.quantity([COORDINATES + [0.03, 0, 0]], "nm")
    )
    result = from_aligned_ligand_cliques(
        [
            dict(
                ligand_id="a",
                molecular_system=source,
                structure_index=0,
                selection=[0, 1, 2],
            ),
            dict(
                ligand_id="b",
                molecular_system=source,
                structure_index=1,
                selection=[0, 1, 2],
            ),
        ],
        features=["hydrophobicity"],
    )
    model = result["models"][0]
    assert [item["structure_index"] for item in model.metadata["sources"]] == [0, 1]
    with puw.context(standard_units=["angstrom", "ps", "degrees"]):
        result = from_aligned_ligand_cliques(
            [
                dict(ligand_id="b", molecular_system=benzene()),
                dict(
                    ligand_id="a",
                    molecular_system=benzene(translation=[0.02, 0, 0], unit="nm"),
                ),
            ],
            features=["aromatic ring"],
            radius="0.05 nm",
        )
    site = result["models"][0].interaction_sites[0]
    assert site.shape_name == "disk"
    np.testing.assert_allclose(
        puw.get_value(site.center, to_unit="nm"), [0.01, 0, 0], atol=1e-15
    )


@pytest.mark.parametrize("operation", ["absence", "tracking_failure"])
def test_optional_attribution_preserves_hypotheses_with_warnings_as_errors(
    monkeypatch, operation
):
    if operation == "absence":
        monkeypatch.setattr(_ackredit, "backend", lambda: None)
    else:

        def fail(*args, **kwargs):
            raise RuntimeError("controlled attribution failure")

        monkeypatch.setattr(ack, "track_item", fail)
    with ack.session("optional provider"):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with phmt.attribution():
                result = get_aligned_consensus_hypotheses(
                    [inventory([[0, 0, 0]]), inventory([[0, 0, 0]])],
                    ligand_ids=["a", "b"],
                )
    assert len(result["hypotheses"]) == 1 and result["complete"]
    assert result["attribution"]["status"] == (
        "unavailable" if operation == "absence" else "failed"
    )
    assert result["attribution"]["references"] is None
    assert "10.1145/362342.362367" in json.dumps(
        result["attribution"]["host_references"]
    )


def test_provider_absence_and_saved_model_are_independent_in_fresh_process():
    run_reader("""
import sys, importlib.abc
class NoAckredit(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] == 'ackredit':
            raise ModuleNotFoundError('absent provider', name='ackredit')
sys.meta_path.insert(0, NoAckredit())
import pharmacophoremt as phmt
from tests.test_aligned_consensus import inventory
assert 'ackredit' not in sys.modules
with phmt.attribution():
    result = phmt.modeler.get_aligned_consensus_hypotheses([inventory([[0,0,0]]), inventory([[0,0,0]])], ligand_ids=['a','b'])
assert len(result['hypotheses']) == 1
assert result['attribution']['status'] == 'unavailable'
assert '10.1145/362342.362367' in str(result['attribution']['host_references'])
assert 'ackredit' not in sys.modules
""")


def test_empty_molecular_workflow_emits_no_usable_model():
    result = from_aligned_ligand_cliques(
        [
            dict(ligand_id="a", molecular_system=system("[Na+]", [[0, 0, 0]])),
            dict(ligand_id="b", molecular_system=system("[Na+]", [[1, 0, 0]])),
        ],
        features=["hb donor"],
    )
    assert (
        result["models"] == []
        and result["report"]["hypotheses"] == []
        and result["complete"]
    )


def test_alternative_models_have_detached_calculation_bibliographies():
    first = system(
        "COCOC", [[-0.1, 0, 0], [0, 0, 0], [0, 0.1, 0], [0.02, 0, 0], [0.12, 0, 0]]
    )
    second = system("COC", [[-0.1, 0, 0], [0.01, 0, 0], [0.12, 0, 0]])
    with ack.session("alternatives"):
        with phmt.attribution():
            result = from_aligned_ligand_cliques(
                [
                    dict(ligand_id="a", molecular_system=first),
                    dict(ligand_id="b", molecular_system=second),
                ],
                features=["hb acceptor"],
                distance_tolerance="0.05 nm",
            )
    assert len(result["models"]) == 2
    one, two = result["models"]
    assert (
        one.metadata["attribution"]
        == two.metadata["attribution"]
        == result["attribution"]
    )
    frozen = json.dumps(two.metadata["attribution"], sort_keys=True)
    one.metadata["attribution"]["references"]["items"].clear()
    assert json.dumps(two.metadata["attribution"], sort_keys=True) == frozen
    assert result["attribution"]["references"]["items"]
