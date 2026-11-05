"""Independent algebraic public-profile controls; no molecular recognition fixture."""

import copy
import importlib
import json
import warnings

import numpy as np
import pytest
from argdigest import UnknownArgumentError, describe_contract

from pharmacophoremt import _ackredit, attribution
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io import load_json, load_yaml, to_json, to_yaml
from pharmacophoremt.modeler import from_receptor_features
from phmt_test_support.prepared_workflow import models_equivalent
from phmt_test_support.saved_model_reader import native_record

OWNER = importlib.import_module("pharmacophoremt.modeler.receptor_generation")
OPTIONS = dict(
    receptor_profile="donor_aromatic_carbonyl_experimental",
    donor_distances=[".28 nm"],
    aromatic_distances=[".35 nm"],
    acceptor_distances=[".35 nm"],
    acceptor_structure_position=0,
    acceptor_target_orientation="towards_receptor",
    radius=".02 nm",
    max_hypotheses=8,
)


def caches(
    *, count=1, model=2, status=1, families=("hb donor", "hb acceptor", "aromatic ring")
):
    """Typed protocol data, not invented molecular chemistry or a model oracle."""
    anchors = [2] + [8 + 3 * i for i in range(count - 1)]
    size = max(7, max(anchors) + 3)
    pairs = np.array([[0, 1]], dtype=np.int64)
    acceptors = np.array(anchors, dtype=np.int64)
    recognition = dict(
        method="smarts_donor_acceptor",
        chemical_state_index=0,
        assume_complete_connectivity=False,
        software={"molsysmt": "synthetic-provider", "rdkit": "synthetic-recognition"},
        donor_hydrogen_pairs=pairs,
        acceptor_atom_indices=acceptors,
        atom_source_indices=np.arange(size, dtype=np.int64),
        selected_atom_indices=np.arange(size, dtype=np.int64),
    )
    features = []
    if "hb donor" in families:
        features.append(
            dict(
                kind="hb donor",
                atom_indices=[0, 1],
                center=puw.quantity([0, 0, 0], "nm"),
                direction=puw.quantity([1, 0, 0], "dimensionless"),
                normal=None,
            )
        )
    if "hb acceptor" in families:
        for anchor in anchors:
            features.append(
                dict(
                    kind="hb acceptor",
                    atom_indices=[anchor],
                    center=puw.quantity([anchor, 0, 0], "nm"),
                    direction=None,
                    normal=None,
                )
            )
    if "aromatic ring" in families:
        features.append(
            dict(
                kind="aromatic ring",
                atom_indices=[4, 5, 6],
                center=puw.quantity([4, 0, 0], "nm"),
                normal=puw.quantity([0, 0, 1], "dimensionless"),
                direction=None,
            )
        )
    inventory = dict(
        definition="classical_atomic_formal@1",
        features=features,
        selected_atom_indices=list(range(size)),
        structure_index=4,
        chemical_state="reference",
        recognition={"hydrogen_bond": detached(recognition)},
    )
    members = [[0, 1]] + [
        [a] if model == 0 else [a, a + 1] if model == 4 else [a, a + 1, a + 2]
        for a in anchors
    ]
    offsets = np.cumsum([0] + [len(row) for row in members]).astype(np.int64)
    roles = np.array([0] + [1] * count, dtype=np.uint8)
    models = np.array([1] + [model] * count, dtype=np.uint8)
    states = np.array([[1] + [status] * count] * 3, dtype=np.uint8)
    dirs = []
    origins = []
    positions = []
    sites = []
    locals_ = []
    images = []
    image_offsets = [0]
    h = np.sqrt(3) / 2
    for p in range(3):
        for s in range(count + 1):
            if states[p, s] != 1:
                continue
            vectors = (
                [[1, 0, 0]] if s == 0 or model != 2 else [[0.5, h, 0], [0.5, -h, 0]]
            )
            for k, vector in enumerate(vectors):
                dirs.append(vector)
                origins.append([0, 0, 0] if s == 0 else [anchors[s - 1], 0, 0])
                positions.append(p)
                sites.append(s)
                locals_.append(k)
                images.extend([[0, 0, 0]] * len(members[s]))
                image_offsets.append(len(images))
    cache = dict(
        schema="molsysmt.hbond_site_directions@1",
        assume_complete_connectivity=False,
        method="ideal_local_geometry",
        site_method="smarts_donor_acceptor",
        chemical_state_index=0,
        sites=copy.deepcopy(recognition),
        software=copy.deepcopy(recognition["software"]),
        parameters={"pbc": False},
        units={"directions": "dimensionless", "origins": "nm"},
        codes={
            "site_roles": {0: "donor", 1: "acceptor"},
            "site_models": {
                0: "unsupported",
                1: "observed_donor_hydrogen",
                2: "carbonyl_trigonal",
                3: "aromatic_nitrogen_bisector",
                4: "nitrile_linear",
            },
            "status": {0: "unsupported", 1: "defined", 2: "undefined"},
        },
        site_atom_indices=np.array([0] + anchors, dtype=np.int64),
        site_roles=roles,
        site_models=models,
        status=states,
        support_atom_indices=np.array(sum(members, []), dtype=np.int64),
        support_atom_offsets=offsets,
        evaluated_structure_indices=np.array([4, 7, 4], dtype=np.int64),
        directions=np.array(dirs, dtype=float),
        origins=puw.quantity(origins, "nm"),
        direction_structure_positions=np.array(positions, dtype=np.int64),
        direction_site_indices=np.array(sites, dtype=np.int64),
        direction_indices=np.array(locals_, dtype=np.uint8),
        direction_structure_indices=np.array(
            [[4, 7, 4][p] for p in positions], dtype=np.int64
        ),
        image_offsets=np.array(image_offsets, dtype=np.int64),
        image_vectors=np.array(images, dtype=np.int32),
        attribution={
            "status": "cached",
            "items": [
                {"id": "synthetic-geometric-evidence", "note": "not newly calculated"}
            ],
        },
        **{
            k: copy.deepcopy(recognition[k])
            for k in [
                "donor_hydrogen_pairs",
                "acceptor_atom_indices",
                "atom_source_indices",
                "selected_atom_indices",
            ]
        },
    )
    return inventory, cache


def build(inventory=None, cache=None, **options):
    if inventory is None:
        inventory, default = caches()
        cache = default if cache is None else cache
    return from_receptor_features(
        inventory, **(OPTIONS | dict(acceptor_directions=cache) | options)
    )


def test_definition_owned_argdigest_and_new_signature_are_live():
    plan = from_receptor_features.digestion_plan
    assert plan.contract_caller == OWNER.__name__ + ".from_receptor_features"
    assert (
        describe_contract(plan.contracts.resolve(plan.contract_caller), plan.domains)[
            "admits"
        ]
        == "signature"
    )
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert build()["complete"]
    with pytest.raises(UnknownArgumentError):
        build(acceptor_direcitons={})


@pytest.mark.parametrize("policy", [["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
def test_independent_joint_product_geometry_order_and_provenance(policy):
    source, cache = caches()
    before = json.dumps(detached((source, cache)), sort_keys=True)
    with puw.context(standard_units=policy):
        result = build(
            source,
            cache,
            donor_distances=[".28 nm", "350 pm"],
            aromatic_distances=[".35 nm", ".45 nm"],
            acceptor_distances=[".30 nm", "350 pm"],
            max_hypotheses=100,
        )
    assert len(result["models"]) == 32 and result["complete"]
    assert result["method"] == OWNER.CARBONYL_METHOD
    expected = []
    for donor in [0.28, 0.35]:
        for acceptor in [0.30, 0.35]:
            for local in [0, 1]:
                for ring in [0.35, 0.45]:
                    for sign in [1, -1]:
                        expected.append((donor, acceptor, local, ring, sign))
    for model, (d, a, local, r, sign) in zip(result["models"], expected, strict=True):
        assert model.n_interaction_sites == 3
        sites = model.interaction_sites
        np.testing.assert_allclose(
            puw.get_value(sites[0].center, to_unit="nm"), [d, 0, 0], atol=1e-12
        )
        axis = np.array([0.5, (1 if local == 0 else -1) * np.sqrt(3) / 2, 0])
        np.testing.assert_allclose(
            puw.get_value(sites[1].center, to_unit="nm"),
            [2, 0, 0] + a * axis,
            atol=1e-12,
        )
        np.testing.assert_allclose(
            puw.get_value(sites[1].shape.direction, to_unit="dimensionless"),
            -axis,
            atol=1e-12,
        )
        np.testing.assert_allclose(
            puw.get_value(sites[2].center, to_unit="nm"), [4, 0, sign * r], atol=1e-12
        )
        assert [s.features for s in sites] == [
            ["hb acceptor"],
            ["hb donor"],
            ["aromatic ring"],
        ]
        assert all(s.essential and s.weight == 1 for s in sites)
        evidence = sites[1].metadata["projection"]["evidence"]["provider_geometry"]
        assert evidence["context"]["support_atom_indices"] == [2, 3, 4]
        assert evidence["provider"]["software"]["molsysmt"] == "synthetic-provider"
        assert (
            evidence["provider"]["attribution"]["items"][0]["id"]
            == "synthetic-geometric-evidence"
        )
    assert json.dumps(detached((source, cache)), sort_keys=True) == before


@pytest.mark.parametrize("budget", [0, 1, 3, 8, 20])
def test_budget_empty_prefix_and_exact_exhaustion(budget):
    result = build(max_hypotheses=budget)
    report = result["report"]["enumeration"]
    total = 4
    assert report["total_possible"] == total and report["returned"] == min(
        total, budget
    )
    assert report["remaining"] == max(total - budget, 0) and result["complete"] == (
        budget >= total
    )
    for model in result["models"]:
        assert model.n_interaction_sites == 3


def test_multiple_acceptors_have_one_site_each_and_lazy_large_product():
    inv, cache = caches(count=2, families=("hb acceptor",))
    result = build(inv, cache, max_hypotheses=10)
    assert len(result["models"]) == 4 and all(
        m.n_interaction_sites == 2 for m in result["models"]
    )
    inv, cache = caches(count=70, families=("hb acceptor",))
    result = build(inv, cache, max_hypotheses=2)
    assert result["report"]["enumeration"]["total_possible"] == 2**70
    assert len(result["models"]) == 2 and not result["complete"]


@pytest.mark.parametrize(
    "model,status,reason",
    [
        (0, 0, "unsupported_acceptor_geometry"),
        (2, 2, "undefined_acceptor_geometry"),
        (3, 1, "outside_carbonyl_profile"),
        (4, 1, "outside_carbonyl_profile"),
    ],
)
def test_no_usable_query_or_score_for_unadmitted_acceptor(model, status, reason):
    inv, cache = caches(model=model, status=status, families=("hb acceptor",))
    result = build(inv, cache)
    assert (
        result["models"] == []
        and result["complete"]
        and result["report"]["status"] == "no_supported_features"
    )
    assert result["report"]["omitted"][0]["reason"] == reason
    assert result["report"]["omitted"][0]["provider_context"]["status"] == status
    assert "fit_value" not in result["report"]


@pytest.mark.parametrize("position,frame", [(0, 4), (1, 7), (2, 4)])
def test_explicit_repeated_structure_position_preserved(position, frame):
    inv, cache = caches(families=("hb acceptor",))
    inv["structure_index"] = frame
    result = build(inv, cache, acceptor_structure_position=position)
    for model in result["models"]:
        context = model.interaction_sites[0].metadata["projection"]["evidence"][
            "provider_geometry"
        ]["context"]
        assert (
            context["source_structure_position"] == position
            and context["source_structure_index"] == frame
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "field,value",
    [
        ("acceptor_directions", None),
        ("acceptor_structure_position", None),
        ("acceptor_structure_position", True),
        ("acceptor_structure_position", -1),
        ("acceptor_structure_position", 1.0),
        ("acceptor_distances", None),
        ("acceptor_distances", []),
        ("acceptor_distances", ["1 ps"]),
        ("acceptor_distances", [0.35]),
        ("acceptor_target_orientation", None),
        ("acceptor_target_orientation", "automatic"),
    ],
)
def test_argument_admission_is_mandatory_with_bypass(skip, field, value):
    with pytest.raises(ArgumentError):
        build(skip_digestion=skip, **{field: value})


@pytest.mark.parametrize(
    "field,value",
    [
        ("acceptor_directions", {}),
        ("acceptor_structure_position", 0),
        ("acceptor_distances", [".35 nm"]),
        ("acceptor_target_orientation", "towards_receptor"),
    ],
)
def test_original_profile_refuses_non_none_acceptor_options(field, value):
    inv, _ = caches()
    opts = dict(
        receptor_profile="donor_aromatic_faces",
        donor_distances=[".28 nm"],
        aromatic_distances=[".35 nm"],
        radius=".02 nm",
        max_hypotheses=1,
    )
    with pytest.raises(ArgumentError):
        from_receptor_features(inv, **opts, **{field: value})


@pytest.mark.parametrize("budget", [0, 1])
@pytest.mark.parametrize(
    "case",
    [
        "schema",
        "method",
        "pbc",
        "state",
        "source",
        "selection",
        "recognition",
        "producer",
        "code",
        "unknown_model",
        "unknown_status",
        "bad_csr",
        "support_outside",
        "bad_positions",
        "bad_locals",
        "zero_vector",
        "nonfinite",
        "origin_dimension",
        "origin_label",
        "origin_center",
        "alternative_origin",
        "image",
        "duplicate_anchor",
        "missing_anchor",
        "saved_quantity",
    ],
)
def test_invalid_cache_fails_before_any_model(monkeypatch, budget, case):
    inv, cache = caches()
    if case == "schema":
        cache["schema"] = "unsupported@2"
    elif case == "method":
        cache["method"] = "first-neighbor"
    elif case == "pbc":
        cache["parameters"]["pbc"] = True
    elif case == "state":
        cache["chemical_state_index"] = 1
    elif case == "source":
        cache["atom_source_indices"][0] = 99
    elif case == "selection":
        cache["selected_atom_indices"] = np.array([0, 1])
    elif case == "recognition":
        del inv["recognition"]["hydrogen_bond"]
    elif case == "producer":
        cache["software"]["molsysmt"] = "another-version"
    elif case == "code":
        cache["codes"]["status"][2] = "unsupported"
    elif case == "unknown_model":
        cache["site_models"][1] = 9
    elif case == "unknown_status":
        cache["status"][0, 1] = 9
    elif case == "bad_csr":
        cache["support_atom_offsets"][1] = 0
    elif case == "support_outside":
        cache["support_atom_indices"][-1] = 999
    elif case == "bad_positions":
        cache["direction_structure_positions"][-1] = 0
    elif case == "bad_locals":
        cache["direction_indices"][2] = 0
    elif case == "zero_vector":
        cache["directions"][2] = 0
    elif case == "nonfinite":
        cache["directions"][2, 0] = np.nan
    elif case == "origin_dimension":
        cache["origins"] = puw.quantity(np.zeros((9, 3)), "ps")
    elif case == "origin_label":
        cache["units"]["origins"] = "pm"
    elif case == "origin_center":
        inv["features"][1]["center"] = puw.quantity([99, 0, 0], "nm")
    elif case == "alternative_origin":
        values = np.asarray(
            puw.get_value(cache["origins"], to_unit="nm"), dtype=float
        ).copy()
        values[2, 0] += 0.1
        cache["origins"] = puw.quantity(values, "nm")
        assert values[2, 0] == pytest.approx(2.1)
    elif case == "image":
        cache["image_vectors"][0, 0] = 1
    elif case == "duplicate_anchor":
        inv["features"].append(copy.deepcopy(inv["features"][1]))
    elif case == "missing_anchor":
        inv["features"][1]["atom_indices"] = [3]
    elif case == "saved_quantity":
        cache["origins"] = detached(cache["origins"])

    def forbidden(*args, **kwargs):
        raise AssertionError("must fail before model construction")

    monkeypatch.setattr(OWNER, "from_receptor_projections", forbidden)
    with pytest.raises(ArgumentError) as caught:
        build(inv, cache, max_hypotheses=budget, skip_digestion=True)
    assert caught.value.code == "PHMT-E102"
    if case == "producer":
        cache["software"]["molsysmt"] = ""
        cache["sites"]["software"]["molsysmt"] = ""
        inv["recognition"]["hydrogen_bond"]["software"]["molsysmt"] = ""
        with pytest.raises(ArgumentError):
            build(inv, cache, max_hypotheses=budget, skip_digestion=True)


def test_metadata_independence_curated_subset_and_no_molecular_access(monkeypatch):
    import molsysmt as msm

    inv, cache = caches(count=2)
    inv["features"] = [r for r in inv["features"] if r["atom_indices"] != [8]]
    before = json.dumps(detached((inv, cache)), sort_keys=True)

    def forbidden(*args, **kwargs):
        raise AssertionError("cached generation accessed a molecular system")

    for name in ["get", "select", "convert"]:
        monkeypatch.setattr(msm, name, forbidden)
    result = build(inv, cache, max_hypotheses=2)
    assert json.dumps(detached((inv, cache)), sort_keys=True) == before
    first, second = result["models"]
    first.interaction_sites[1].metadata["projection"]["evidence"]["provider_geometry"][
        "provider"
    ]["software"]["molsysmt"] = "changed"
    assert (
        second.interaction_sites[1].metadata["projection"]["evidence"][
            "provider_geometry"
        ]["provider"]["software"]["molsysmt"]
        == "synthetic-provider"
    )
    result["report"]["acceptor_directions"]["software"]["molsysmt"] = "changed"
    assert cache["software"]["molsysmt"] == "synthetic-provider"


def test_exclusions_native_persistence_and_real_optional_credit(tmp_path):
    inv, cache = caches(families=("hb acceptor",))
    heavy = copy.deepcopy(inv)
    heavy["features"] = [
        dict(
            kind="included volume",
            atom_indices=[0],
            center=puw.quantity([0, 0, 0], "nm"),
        )
    ]
    with attribution():
        result = build(
            inv, cache, excluded_volume_inventory=heavy, excluded_volume_radius=".01 nm"
        )
    assert result["attribution"]["status"] == "captured"
    assert all(m.n_interaction_sites == 2 for m in result["models"])
    assert result["report"]["excluded_volumes"]["attached_model_count"] == 2
    for index, model in enumerate(result["models"]):
        original = native_record(model, tmp_path, f"original{index}")
        for suffix, write, read in [
            ("json", to_json, load_json),
            ("yaml", to_yaml, load_yaml),
        ]:
            path = tmp_path / f"model{index}.{suffix}"
            write(model, path)
            assert models_equivalent(
                original, native_record(read(path), tmp_path, f"read{index}{suffix}")
            )


@pytest.mark.parametrize("fail", [False, True])
def test_optional_provider_absence_failure_does_not_erase_models(monkeypatch, fail):
    def backend():
        if fail:
            raise RuntimeError("controlled tracking failure")
        return None

    monkeypatch.setattr(_ackredit, "backend", backend)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("error")
        with attribution():
            result = build()
    assert len(result["models"]) == 4 and result["complete"]
    assert result["attribution"]["status"] != "captured"


def test_empty_detached_donor_metadata_retains_native_sparse_shape():
    inv, cache = caches(families=("hb acceptor",))
    records = cache["direction_site_indices"] == 1
    for name in [
        "directions",
        "direction_structure_positions",
        "direction_structure_indices",
        "direction_indices",
    ]:
        cache[name] = cache[name][records]
    cache["direction_site_indices"] = np.zeros(6, dtype=np.int64)
    cache["origins"] = cache["origins"][records]
    cache["site_atom_indices"] = np.array([2], dtype=np.int64)
    cache["site_roles"] = np.array([1], dtype=np.uint8)
    cache["site_models"] = np.array([2], dtype=np.uint8)
    cache["status"] = np.ones((3, 1), dtype=np.uint8)
    cache["support_atom_indices"] = np.array([2, 3, 4], dtype=np.int64)
    cache["support_atom_offsets"] = np.array([0, 3], dtype=np.int64)
    cache["image_offsets"] = np.arange(0, 19, 3, dtype=np.int64)
    cache["image_vectors"] = np.zeros((18, 3), dtype=np.int32)
    cache["donor_hydrogen_pairs"] = np.empty((0, 2), dtype=np.int64)
    cache["sites"]["donor_hydrogen_pairs"] = np.empty((0, 2), dtype=np.int64)
    inv["recognition"]["hydrogen_bond"]["donor_hydrogen_pairs"] = []
    result = build(inv, cache)
    assert len(result["models"]) == 2 and result["complete"]


def test_shared_donor_acceptor_anchor_keeps_roles_and_omission_distinct():
    inv, cache = caches(model=0, status=0, families=("hb donor", "hb acceptor"))
    inv["features"][1]["atom_indices"] = [0]
    inv["features"][1]["center"] = puw.quantity([0, 0, 0], "nm")
    inv["recognition"]["hydrogen_bond"]["acceptor_atom_indices"] = [0]
    cache["acceptor_atom_indices"] = np.array([0], dtype=np.int64)
    cache["sites"]["acceptor_atom_indices"] = np.array([0], dtype=np.int64)
    cache["site_atom_indices"] = np.array([0, 0], dtype=np.int64)
    cache["support_atom_indices"] = np.array([0, 1, 0], dtype=np.int64)
    result = build(inv, cache)
    assert len(result["models"]) == 1 and result["models"][0].n_interaction_sites == 1
    assert result["models"][0].interaction_sites[0].features == ["hb acceptor"]
    assert result["report"]["omitted"][0]["reason"] == "unsupported_acceptor_geometry"
