"""Independent assignment controls and real-provider aligned consensus workflows."""

import itertools
import json

import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ConsensusLimitError,
)
from pharmacophoremt.io.phmt import load_json, to_json
from pharmacophoremt.modeler import (
    from_aligned_ligands,
    get_aligned_feature_matches,
    get_consensus_sites,
)
from pharmacophoremt.modeler.features import DEFINITION
from tests.test_pose_evaluation import system
from tests.test_reference_ligand import benzene
from tests.test_rigid_search import COORDINATES, FAMILIES, reference


def inventory(centers, kinds=None, directions=None, normals=None):
    """Synthetic feature geometry for mathematical controls; no molecular claim."""
    n = len(centers)
    kinds = kinds or ["hb acceptor"] * n
    directions = directions or [None] * n
    normals = normals or [None] * n
    return dict(
        definition=DEFINITION,
        structure_index=0,
        chemical_state="reference",
        selected_atom_indices=list(range(max(1, n))),
        recognition={},
        features=[
            dict(
                kind=kind,
                center=puw.quantity(center, "nm"),
                atom_indices=[i],
                geometry_atom_indices=[i],
                charge=None,
                direction=None
                if direction is None
                else puw.quantity(direction, "dimensionless"),
                normal=None
                if normal is None
                else puw.quantity(normal, "dimensionless"),
            )
            for i, (center, kind, direction, normal) in enumerate(
                zip(centers, kinds, directions, normals)
            )
        ],
    )


def test_assignment_matches_bounded_exhaustive_oracle_with_repeated_types():
    rng = np.random.default_rng(93)
    for _ in range(20):
        first, second = rng.uniform(0, 0.4, (3, 3)), rng.uniform(0, 0.4, (3, 3))
        # Enumerate every injection, including unmatched rows, independently of SciPy.
        best = None
        for mapping in itertools.product(range(-1, 3), repeat=3):
            used = [column for column in mapping if column >= 0]
            if len(set(used)) != len(used):
                continue
            distances = [
                float(np.linalg.norm(first[row] - second[column]))
                for row, column in enumerate(mapping)
                if column >= 0
            ]
            if any(distance > 0.25 for distance in distances):
                continue
            objective = (-len(used), sum(distances))
            if best is None or objective < best:
                best = objective
        result = get_aligned_feature_matches(
            inventory(first), inventory(second), distance_tolerance="0.25 nm"
        )
        measured = (
            -len(result["matches"]),
            sum(np.linalg.norm(first[a] - second[b]) for a, b in result["matches"]),
        )
        assert measured[0] == best[0]
        assert measured[1] == pytest.approx(best[1])
        assert result["complete"]


def test_assignment_maximizes_cardinality_before_distance_and_handles_type_order():
    first = inventory([[0, 0, 0], [0.1, 0, 0]])
    second = inventory([[0.04, 0, 0], [-0.08, 0, 0]])
    result = get_aligned_feature_matches(first, second, distance_tolerance="0.10 nm")
    assert result["matches"] == [[0, 1], [1, 0]]  # Nearest-first greedy loses a match.
    reordered = inventory([[0.1, 0, 0], [0, 0, 0]], ["positive charge", "hb acceptor"])
    typed = inventory([[0, 0, 0], [0.1, 0, 0]], ["hb acceptor", "positive charge"])
    assert get_aligned_feature_matches(typed, reordered)["matches"] == [[0, 1], [1, 0]]


def test_centroid_support_dispersion_and_detached_members_are_analytical():
    first, second = inventory([[0, 0, 0]]), inventory([[0.06, 0, 0]])
    missing = inventory([])
    result = get_consensus_sites(
        [first, second, missing], [[[0, 0], [1, 0]]], ligand_ids=["a", "b", "empty"]
    )
    site = result["sites"][0]
    np.testing.assert_allclose(
        puw.get_value(site["center"], to_unit="nm"), [0.03, 0, 0]
    )
    assert site["support_count"] == 2 and site["support_fraction"] == pytest.approx(
        2 / 3
    )
    assert float(puw.get_value(site["position_rmsd"], to_unit="nm")) == pytest.approx(
        0.03
    )
    assert float(
        puw.get_value(site["maximum_center_deviation"], to_unit="nm")
    ) == pytest.approx(0.03)
    first["features"][0]["atom_indices"][0] = 99
    assert site["members"][0]["atom_indices"] == [0]


def test_orientations_distinguish_donor_vectors_and_equivalent_aromatic_axes():
    donor = inventory([[0, 0, 0]], ["hb donor"], directions=[[1, 0, 0]])
    reverse = inventory([[0, 0, 0]], ["hb donor"], directions=[[-1, 0, 0]])
    assert get_aligned_feature_matches(donor, reverse)["matches"] == []
    rejected = get_consensus_sites(
        [donor, reverse], [[[0, 0], [1, 0]]], ligand_ids=["a", "b"]
    )
    assert not rejected["sites"] and rejected["rejected_groups"][0]["reasons"] == [
        "orientation_dispersion"
    ]
    ring = inventory([[0, 0, 0]], ["aromatic ring"], normals=[[0, 0, 1]])
    inverse = inventory([[0, 0, 0]], ["aromatic ring"], normals=[[0, 0, -1]])
    assert get_aligned_feature_matches(ring, inverse, direction_tolerance="0 degrees")[
        "matches"
    ] == [[0, 0]]
    result = get_consensus_sites(
        [ring, inverse],
        [[[0, 0], [1, 0]]],
        ligand_ids=["a", "b"],
        direction_tolerance="0 degrees",
    )
    np.testing.assert_array_equal(
        puw.get_value(result["sites"][0]["normal"]), [0, 0, 1]
    )
    assert result["criteria"]["orientation_aggregation"] == "first_member_reference"


def test_empty_success_and_rejections_preserve_complete_evidence():
    empty, one = inventory([]), inventory([[0, 0, 0]])
    assert get_aligned_feature_matches(empty, one)["unmatched_candidate"] == [0]
    assert get_aligned_feature_matches(one, empty)["n_matrix_entries"] == 0
    report = get_consensus_sites([empty, one], [], ligand_ids=["a", "b"])
    assert report["complete"] and report["sites"] == []
    report = get_consensus_sites([one, empty], [[[0, 0]]], ligand_ids=["a", "b"])
    assert report["rejected_groups"][0]["reasons"] == ["insufficient_ligand_support"]
    far = inventory([[2, 0, 0]])
    report = get_consensus_sites([one, far], [[[0, 0], [1, 0]]], ligand_ids=["a", "b"])
    assert report["rejected_groups"][0]["reasons"] == ["position_dispersion"]


@pytest.mark.parametrize(
    "groups",
    [
        [[[0, 0], [0, 1]]],
        [[[0, 0]], [[0, 0]]],
        [[[0, 9]]],
        [[[2, 0]]],
        [[[0, -1]]],
        [[[0.0, 0.0]]],
        [[]],
    ],
)
def test_duplicate_source_reused_or_invalid_correspondences_raise(groups):
    with pytest.raises(ArgumentError):
        get_consensus_sites(
            [inventory([[0, 0, 0], [1, 0, 0]]), inventory([])],
            groups,
            ligand_ids=["a", "b"],
        )


def test_duplicate_identity_mixed_types_and_invalid_geometry_raise():
    first = inventory([[0, 0, 0]])
    with pytest.raises(ArgumentError):
        get_consensus_sites([first, first], [[[0, 0], [1, 0]]], ligand_ids=["a", "a"])
    second = inventory([[0, 0, 0]], ["positive charge"])
    with pytest.raises(ArgumentError):
        get_consensus_sites([first, second], [[[0, 0], [1, 0]]], ligand_ids=["a", "b"])
    bad = inventory([[0, 0, 0]], ["hb donor"])
    with pytest.raises(ArgumentError):
        get_aligned_feature_matches(first, bad)
    for kwargs in (
        {"distance_tolerance": 0.15},
        {"direction_tolerance": "2 nm"},
        {"min_support": True},
    ):
        with pytest.raises(ArgumentError):
            get_consensus_sites(
                [first, first], [[[0, 0], [1, 0]]], ligand_ids=["a", "b"], **kwargs
            )


def test_matrix_budget_raises_before_assignment_instead_of_returning_empty(monkeypatch):
    import pharmacophoremt.modeler.aligned_consensus as module

    def never(*args, **kwargs):
        raise AssertionError("assignment must not be called")

    monkeypatch.setattr(module, "linear_sum_assignment", never)
    with pytest.raises(ConsensusLimitError) as caught:
        get_aligned_feature_matches(
            inventory([[0, 0, 0]] * 2), inventory([[0, 0, 0]] * 2), max_matrix_entries=7
        )
    assert caught.value.code == "PHMT-E106"
    assert caught.value.extra["matrix_entries"] == 8


def test_real_workflow_uses_provider_preserves_sources_and_portable_attribution(
    tmp_path, monkeypatch
):
    source, _ = reference()
    translated = msm.structure.translate(
        source, translation=puw.quantity([[[0.04, 0, 0]]], "nm"), in_place=False
    )
    negative = system("[Na+]", [[4, 0, 0]])
    before = [
        puw.get_value(msm.get(item, coordinates=True), to_unit="nm").copy()
        for item in (source, translated, negative)
    ]
    calls, provider = [], msm.physchem.get_hbond_sites

    def observed(*args, **kwargs):
        calls.append(kwargs["structure_indices"])
        return provider(*args, **kwargs)

    monkeypatch.setattr(msm.physchem, "get_hbond_sites", observed)
    ligands = [
        dict(ligand_id=identity, molecular_system=item)
        for identity, item in zip(
            ("a", "b", "negative"), (source, translated, negative)
        )
    ]
    with phmt.attribution():
        model = from_aligned_ligands(ligands, features=FAMILIES, radius="0.06 nm")
    assert len(calls) == 3
    assert model.n_interaction_sites == 5
    assert [record["ligand_id"] for record in model.metadata["sources"]] == [
        "a",
        "b",
        "negative",
    ]
    assert model.metadata["attribution"]["status"] == "captured"
    assert "10.1109/TAES.2016.140952" in json.dumps(model.metadata["attribution"])
    assert "10.1021/ci8002478" not in json.dumps(model.metadata["attribution"])
    assert all(site.metadata["support_count"] == 2 for site in model.interaction_sites)
    assert all(
        site.metadata["support_fraction"] == pytest.approx(2 / 3)
        for site in model.interaction_sites
    )
    evaluator = phmt.screening.PoseEvaluator(model)
    assert (
        evaluator.evaluate(source)["status"]
        == evaluator.evaluate(translated)["status"]
        == "matched"
    )
    assert evaluator.evaluate(negative)["status"] == "not_matched"
    for item, coordinates in zip((source, translated, negative), before):
        np.testing.assert_array_equal(
            puw.get_value(msm.get(item, coordinates=True), to_unit="nm"), coordinates
        )
    json.dumps(model.metadata, allow_nan=False)
    target = tmp_path / "consensus.json"
    to_json(model, target)
    assert load_json(target).metadata == model.metadata


def test_real_aromatic_planes_and_nondefault_units_produce_disk():
    first, second = benzene(), benzene(translation=[0.02, 0, 0], unit="nm")
    with puw.context(standard_units=["angstrom", "ps", "degrees"]):
        model = from_aligned_ligands(
            [
                dict(ligand_id="a", molecular_system=first),
                dict(ligand_id="b", molecular_system=second),
            ],
            features=["aromatic ring"],
            radius="0.05 nm",
        )
    site = model.interaction_sites[0]
    assert site.shape_name == "disk"
    np.testing.assert_allclose(
        puw.get_value(site.center, to_unit="nm"), [0.01, 0, 0], atol=1e-15
    )
    assert phmt.screening.PoseEvaluator(model).evaluate(second)["status"] == "matched"


def test_per_ligand_frame_selection_and_reference_scope_are_explicit():
    source, _ = reference()
    source.structures.append(
        coordinates=puw.quantity([COORDINATES + [0.06, 0, 0]], "nm")
    )
    ligand = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.3, 0, 0]])
    model = from_aligned_ligands(
        [
            dict(
                ligand_id="full",
                molecular_system=source,
                selection=[0, 1, 2],
                structure_index=1,
            ),
            dict(ligand_id="small", molecular_system=ligand),
        ],
        reference_index=1,
        features=["hydrophobicity"],
    )
    assert model.ref_mol == 1 and model.n_interaction_sites == 1
    assert model.metadata["sources"][0]["structure_index"] == 1
    assert model.interaction_sites[0].metadata["members"][0]["ligand_id"] == "small"
    with pytest.raises(ArgumentError):
        from_aligned_ligands([dict(ligand_id="a", molecular_system=ligand)] * 2)
    with pytest.raises(ArgumentError):
        from_aligned_ligands(
            [
                dict(ligand_id="a", molecular_system=ligand),
                dict(ligand_id="b", molecular_system=system("[Na+]", [[0, 0, 0]])),
            ],
            features=["hb donor"],
        )
