"""Explicit aromatic-N cache receiving; algebraic controls are not chemistry."""

import copy
import hashlib
import importlib
import json
import warnings

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import _ackredit, attribution
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io import load_json, load_yaml, to_json, to_yaml
from pharmacophoremt.modeler import from_receptor_features, get_features
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.prepared_receptor_workflow import credit_input, load_input
from phmt_test_support.prepared_workflow import models_equivalent
from phmt_test_support.receptor_contribution import candidate_custody, source_custody
from phmt_test_support.saved_model_reader import native_record
from tests.test_cached_carbonyl_generation import OPTIONS, caches

OWNER = importlib.import_module("pharmacophoremt.modeler.receptor_generation")
PROFILE = "donor_aromatic_carbonyl_aromatic_n_experimental"
METHOD = "cached_receptor_donor_aromatic_carbonyl_aromatic_n@1"


def build(inventory=None, cache=None, **options):
    if inventory is None:
        inventory, cache = caches(model=3, families=("hb acceptor",))
    return from_receptor_features(
        inventory,
        **(
            OPTIONS
            | dict(receptor_profile=PROFILE, acceptor_directions=cache)
            | options
        ),
    )


@pytest.mark.parametrize("policy", [["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
def test_algebraic_placement_target_axis_and_opposite_cloud(policy):
    inv, cache = caches(model=3, families=("hb acceptor",))
    before = json.dumps(detached((inv, cache)), sort_keys=True)
    with puw.context(standard_units=policy):
        result = build(inv, cache, acceptor_distances=[".30 nm", "350 pm"])
        assert result["method"] == METHOD and result["complete"]
        assert len(result["models"]) == 2
        for model, distance in zip(result["models"], [0.30, 0.35], strict=True):
            site = model.interaction_sites[0]
            np.testing.assert_allclose(
                puw.get_value(site.center, to_unit="nm"),
                [2 + distance, 0, 0],
                atol=1e-12,
                rtol=0,
            )
            np.testing.assert_allclose(
                puw.get_value(site.direction, to_unit="dimensionless"),
                [-1, 0, 0],
                atol=1e-12,
                rtol=0,
            )
            assert site.features == ["hb donor"] and site.essential and site.weight == 1
            evidence = site.metadata["projection"]["evidence"]["provider_geometry"]
            assert evidence["context"]["site_model"] == 3
            assert evidence["context"]["support_atom_indices"] == [2, 3, 4]
            evaluator = PoseEvaluator(
                model, direction_tolerance="1 degree", min_fit_value=1
            )
            # Independent analytical feature clouds; no molecular candidate or
            # new public molecular geometry path is implied by this private match.
            for center, axis, score in [
                ([2 + distance, 0, 0], [-1, 0, 0], 1),
                ([2 + distance, 0, 0], [1, 0, 0], 0),
                ([3 + distance, 0, 0], [-1, 0, 0], 0),
            ]:
                cloud = [
                    dict(
                        kind="hb donor",
                        atom_indices=[0, 1],
                        center=np.array(center),
                        direction=np.array(axis),
                    )
                ]
                outcome = evaluator._match(
                    cloud, np.empty((0, 3)), np.empty(0, dtype=int)
                )
                assert outcome["fit_value"] == score
                assert outcome["status"] == ("matched" if score else "not_matched")
    assert json.dumps(detached((inv, cache)), sort_keys=True) == before


@pytest.mark.parametrize("budget", [0, 1, 2, 9])
def test_donor_ring_product_retains_single_n_choice_and_exact_budget(budget):
    inv, cache = caches(model=3)
    result = build(inv, cache, max_hypotheses=budget)
    e = result["report"]["enumeration"]
    assert e["total_possible"] == 2 and e["returned"] == min(2, budget)
    assert e["remaining"] == max(2 - budget, 0)
    assert result["complete"] is (budget >= 2)
    assert all(m.n_interaction_sites == 3 for m in result["models"])
    for m, sign in zip(result["models"], [1, -1]):
        assert [r["feature_index"] for r in m.metadata["generation"]["choices"]] == [
            0,
            1,
            2,
        ]
        assert m.metadata["generation"]["choices"][2]["face_sign"] == sign


def test_mixed_carbonyl_and_aromatic_n_product_keeps_alternatives_separate():
    inv, cache = caches(count=2, model=2, families=("hb acceptor",))
    cache["site_models"][2] = 3
    keep = ~((cache["direction_site_indices"] == 2) & (cache["direction_indices"] == 1))
    old_offsets, old_images = cache["image_offsets"], cache["image_vectors"]
    image_rows = [
        old_images[old_offsets[i] : old_offsets[i + 1]] for i in np.flatnonzero(keep)
    ]
    cache["image_offsets"] = np.cumsum([0] + [len(r) for r in image_rows]).astype(
        np.int64
    )
    cache["image_vectors"] = np.concatenate(image_rows)
    for field in [
        "directions",
        "origins",
        "direction_site_indices",
        "direction_structure_positions",
        "direction_structure_indices",
        "direction_indices",
    ]:
        cache[field] = cache[field][keep]
    result = build(inv, cache)
    assert len(result["models"]) == 2 and result["complete"]
    h = np.sqrt(3) / 2
    for model, sign in zip(result["models"], [1, -1], strict=True):
        for site, point in zip(
            model.interaction_sites,
            [[2.175, sign * 0.35 * h, 0], [8.175, 0.35 * h, 0]],
            strict=True,
        ):
            np.testing.assert_allclose(
                puw.get_value(site.center, to_unit="nm"), point, atol=1e-12, rtol=0
            )


@pytest.mark.parametrize(
    "model,status,reason",
    [
        (0, 0, "unsupported_acceptor_geometry"),
        (3, 2, "undefined_acceptor_geometry"),
        (4, 1, "outside_carbonyl_aromatic_n_profile"),
    ],
)
def test_omitted_geometry_is_not_a_usable_empty_query(model, status, reason):
    inv, cache = caches(model=model, status=status, families=("hb acceptor",))
    result = build(inv, cache)
    assert result["models"] == [] and result["complete"]
    assert result["report"]["status"] == "no_supported_features"
    assert result["report"]["omitted"][0]["reason"] == reason
    assert "fit_value" not in result["report"]


@pytest.mark.parametrize("position,frame", [(0, 4), (1, 7), (2, 4)])
def test_explicit_repeated_frame_and_resolved_state(position, frame):
    inv, cache = caches(model=3, families=("hb acceptor",))
    inv["structure_index"] = frame
    result = build(inv, cache, acceptor_structure_position=position)
    context = (
        result["models"][0]
        .interaction_sites[0]
        .metadata["projection"]["evidence"]["provider_geometry"]["context"]
    )
    assert context["source_structure_position"] == position
    assert context["source_structure_index"] == frame


@pytest.mark.parametrize("budget", [0, 1])
@pytest.mark.parametrize(
    "case",
    [
        "support",
        "cardinality",
        "state",
        "frame",
        "source",
        "selection",
        "unit",
        "zero",
        "missing",
        "unknown_model",
    ],
)
def test_malformed_n_cache_refused_before_models_with_bypass(monkeypatch, budget, case):
    inv, cache = caches(model=3, families=("hb acceptor",))
    if case == "support":
        cache["support_atom_offsets"][-1] -= 1
        cache["support_atom_indices"] = cache["support_atom_indices"][:-1]
    elif case == "cardinality":
        cache["direction_indices"][1] = 1
    elif case == "state":
        cache["chemical_state_index"] = 1
    elif case == "frame":
        inv["structure_index"] = 99
    elif case == "source":
        cache["atom_source_indices"][0] = 99
    elif case == "selection":
        cache["selected_atom_indices"] = np.array([2], dtype=np.int64)
    elif case == "unit":
        cache["units"]["origins"] = "pm"
    elif case == "zero":
        cache["directions"][1] = 0
    elif case == "missing":
        cache = None
    elif case == "unknown_model":
        cache["site_models"][1] = 8

    def forbidden(*args, **kwargs):
        raise AssertionError("must fail before constructing a hypothesis")

    monkeypatch.setattr(OWNER, "from_receptor_projections", forbidden)
    with pytest.raises(ArgumentError) as caught:
        build(inv, cache, max_hypotheses=budget, skip_digestion=True)
    assert caught.value.code == "PHMT-E102"


def test_cached_only_execution_detaches_credit_and_models(monkeypatch, tmp_path):
    inv, cache = caches(model=3, families=("hb acceptor",))
    before = json.dumps(detached((inv, cache)), sort_keys=True)
    heavy = copy.deepcopy(inv)
    heavy["features"] = [
        dict(
            kind="included volume",
            atom_indices=[0],
            center=puw.quantity([0, 0, 0], "nm"),
        )
    ]

    def forbidden(*args, **kwargs):
        raise AssertionError("cached generation must not access a molecular system")

    for name in ["get", "convert", "select"]:
        monkeypatch.setattr(msm, name, forbidden)
    with attribution():
        result = build(
            inv,
            cache,
            acceptor_distances=[".3 nm", ".35 nm"],
            excluded_volume_inventory=heavy,
            excluded_volume_radius=".01 nm",
        )
    assert result["attribution"]["status"] == "captured"
    assert result["report"]["excluded_volumes"]["attached_model_count"] == 2
    assert all(m.n_interaction_sites == 2 for m in result["models"])
    assert json.dumps(detached((inv, cache)), sort_keys=True) == before
    for i, model in enumerate(result["models"]):
        original = native_record(model, tmp_path, f"original{i}")
        for suffix, write, read in [
            ("json", to_json, load_json),
            ("yaml", to_yaml, load_yaml),
        ]:
            path = tmp_path / f"model{i}.{suffix}"
            write(model, path)
            assert models_equivalent(
                original, native_record(read(path), tmp_path, f"read{i}{suffix}")
            )
    a, b = result["models"]
    a.interaction_sites[0].metadata["projection"]["evidence"]["provider_geometry"][
        "provider"
    ]["software"]["molsysmt"] = "changed"
    assert (
        b.interaction_sites[0].metadata["projection"]["evidence"]["provider_geometry"][
            "provider"
        ]["software"]["molsysmt"]
        == "synthetic-provider"
    )
    assert cache["software"]["molsysmt"] == "synthetic-provider"


@pytest.mark.parametrize("fail", [False, True])
def test_optional_credit_absence_or_failure_keeps_native_n_hypothesis(
    monkeypatch, fail
):
    def backend():
        if fail:
            raise RuntimeError("controlled tracking failure")
        return None

    monkeypatch.setattr(_ackredit, "backend", backend)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("error")
        with attribution():
            result = build()
    assert len(result["models"]) == 1 and result["complete"]
    assert result["attribution"]["status"] != "captured"


def test_real_native_his524_receiving_preserves_source_and_old_profile(tmp_path):
    source, identity = load_input(tmp_path)
    assert (
        identity["native_evidence"]["uncompressed_sha256"]
        == "a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a"
    )
    before = source_custody(source)
    with attribution():
        credit_input()
        inv = get_features(source, selection=[1754], features=["hb acceptor"])
        cache = msm.interactions.hbonds.get_hbond_site_directions(
            source,
            selection=[1754],
            structure_indices=[0],
            chemical_state="reference",
            pbc=False,
        )
        assert cache["site_models"].tolist() == [3] and cache["status"].tolist() == [
            [1]
        ]
        assert cache["support_atom_indices"].tolist() == [1754, 1753, 1756]
        # Frozen receiving vector from the preceding read-only audit. It is
        # exposed provider evidence, not a separately validated electronic model.
        axis = np.array([-0.07537837089851458, 0.10218907917041739, 0.9919049819912129])
        np.testing.assert_allclose(cache["directions"], [axis], atol=1e-12, rtol=0)
        result = build(inv, cache, acceptor_distances=[".3 nm", ".35 nm"])
        old = from_receptor_features(inv, **(OPTIONS | dict(acceptor_directions=cache)))
        # Four literal indexed-D/O poses declared from the preceding exposed
        # direction audit, before executing this receiving. MolSysMT constructs
        # and reads molecules; this test implements no molecular transformation.
        candidate = msm.convert(
            msm.convert("smiles:[2H]O", to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
        )
        candidate.structures.append(
            coordinates=puw.quantity(
                [
                    [
                        [11.105924325820297, 1.1043378158340835, 2.282580996398243],
                        [11.098386488730446, 1.1145567237511254, 2.381771494597364],
                    ],
                    [
                        [11.090848651640595, 1.1247756316681672, 2.480961992796485],
                        [11.098386488730446, 1.1145567237511254, 2.381771494597364],
                    ],
                    [
                        [11.10215540727537, 1.1094472697926043, 2.3321762454978034],
                        [11.09461757018552, 1.1196661777096462, 2.4313667436969246],
                    ],
                    [
                        [11.087079733095669, 1.129885085626688, 2.530557241896046],
                        [11.09461757018552, 1.1196661777096462, 2.4313667436969246],
                    ],
                ],
                "nm",
            )
        )
        candidate_before = candidate_custody(candidate)
        native, outcomes, recovery = [], [], []
        for i, model in enumerate(result["models"]):
            native.append(native_record(model, tmp_path, f"native-his524-{i}"))
            evaluator = PoseEvaluator(
                model, min_fit_value=1, direction_tolerance="1 degree"
            )
            outcomes.append(
                [evaluator.evaluate(candidate, structure_index=j) for j in range(4)]
            )
            assert [r["fit_value"] for r in outcomes[-1]] == (
                [1, 0, 0, 0] if i == 0 else [0, 0, 1, 0]
            )
            assert [r["status"] for r in outcomes[-1]] == (
                ["matched", "not_matched", "not_matched", "not_matched"]
                if i == 0
                else ["not_matched", "not_matched", "matched", "not_matched"]
            )
            path = tmp_path / f"native-his524-{i}.yaml"
            to_yaml(model, path)
            restored = load_yaml(path)
            assert models_equivalent(
                native[-1], native_record(restored, tmp_path, f"native-read-{i}")
            )
            recovered = PoseEvaluator(
                restored, min_fit_value=1, direction_tolerance="1 degree"
            ).evaluate(candidate, structure_index=2 * i)
            assert recovered["fit_value"] == 1 and recovered["status"] == "matched"
            recovery.append(recovered)
        assert candidate_custody(candidate) == candidate_before
    assert (
        old["models"] == []
        and old["report"]["omitted"][0]["reason"] == "outside_carbonyl_profile"
    )
    assert len(result["models"]) == 2 and result["complete"]
    for model, distance in zip(result["models"], [0.3, 0.35], strict=True):
        site = model.interaction_sites[0]
        np.testing.assert_allclose(
            puw.get_value(site.center, to_unit="nm"),
            np.array([11.121, 1.0839, 2.0842]) + distance * axis,
            atol=1e-12,
            rtol=0,
        )
        np.testing.assert_allclose(
            puw.get_value(site.direction, to_unit="dimensionless"),
            -axis,
            atol=1e-12,
            rtol=0,
        )
        assert site.metadata["atom_indices"] == [1754]
    assert source_custody(source) == before
    payload = dict(
        scope="Exposed prepared-input/provider receiving and literal analytical donor witnesses; no activity cohort, biological prediction or performance claim.",
        input_identity=identity,
        feature_inventory=detached(inv),
        native_cache=detached(cache),
        generated={k: v for k, v in result.items() if k != "models"},
        old_profile={k: v for k, v in old.items() if k != "models"},
        native_models=native,
        outcomes=outcomes,
        recovery=recovery,
        candidate_before=candidate_before,
        candidate_after=candidate_custody(candidate),
        source_custody_unchanged=True,
        source_custody_sha256=hashlib.sha256(
            json.dumps(before, sort_keys=True).encode()
        ).hexdigest(),
    )
    (tmp_path / "native_his524_receiving.json").write_text(
        json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n"
    )
