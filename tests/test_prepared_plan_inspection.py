"""Inspect native-admitted plans without molecular inputs or fitting."""

import hashlib
import json
from copy import deepcopy
from dataclasses import FrozenInstanceError, fields, replace

import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt.io import to_json
from pharmacophoremt.screening import (
    PreparedRunPlan,
    PreparedScreeningRun,
    build_prepared_run_plan,
)
from pharmacophoremt.screening import prepared_runs as runtime
from pharmacophoremt_results import canonical_json

MARKER = "SYNTHETIC_UNPRINTED_QUERY_MARKER"


def native_plan(tmp_path, method="placed"):
    query = phmt.Pharmacophore()
    query.metadata["inspection_fixture"] = MARKER
    for center in ("[0,0,0] nm", "[0.3,0,0] nm", "[0,0.5,0] nm"):
        query.add_interaction_site(
            InteractionSite(Sphere(center, "0.02 nm"), "positive charge")
        )
    path = tmp_path / "query.json"
    to_json(query, str(path))
    compatibility = {
        "prepared_snapshot": {"fixture": "no molecular input"},
        "preparation": "caller-declared-synthetic@1",
        "features": ["positive charge"],
        "index": None,
        "grouping": {"policy": "explicit work"},
        "numerical": {"threads": 1, "declared_precision": "float64"},
    }
    constructor = {} if method == "placed" else {"search_method": "seeded_hit"}
    evaluation = {
        "chemical_state": 0,
        "structure_indices" if method == "conformers" else "structure_index": (
            [0, 2] if method == "conformers" else 0
        ),
    }
    plan = build_prepared_run_plan(
        path,
        screening_method=method,
        score_method=None,
        compatibility=compatibility,
        constructor_options=constructor,
        evaluation_options=evaluation,
        on_error="record",
    )
    return plan, path


@pytest.mark.parametrize("method", ["placed", "rigid", "conformers"])
def test_public_factory_description_preserves_exact_query_and_native_settings(
    tmp_path, method
):
    plan, path = native_plan(tmp_path, method)
    raw = path.read_bytes()
    result = plan.describe()
    assert result == {
        "query": {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()},
        "context": plan.context,
    }
    assert json.loads(json.dumps(result, allow_nan=False)) == result
    execution = result["context"]["execution"]
    assert execution["screening_method"] == method
    assert execution["score_method"] == (
        "checked_pose_coverage" if method == "placed" else "seeded_hit"
    )
    assert execution["constructor_options"]["point_tolerance"] == "0.10 nm"
    assert execution["constructor_options"]["direction_tolerance"] == "30 degrees"
    assert execution["evaluation_options"]["chemical_state"] == 0
    assert result["context"]["schema"] == "pharmacophoremt.prepared-run-plan@1"
    assert MARKER not in repr(plan) and plan.context_json not in repr(plan)


@pytest.mark.parametrize("method", ["placed", "rigid", "conformers"])
def test_inspection_retains_captured_bytes_after_query_file_changes(tmp_path, method):
    plan, path = native_plan(tmp_path, method)
    before = plan.describe()
    path.write_bytes(b"changed source is not reread")
    assert plan.describe() == before
    path.unlink()
    assert plan.describe() == before


@pytest.mark.parametrize("size", [0, 30, 2 * 1024 * 1024])
def test_repr_is_bounded_for_admitted_field_sizes_without_printing_payload(
    tmp_path, size
):
    plan, _ = native_plan(tmp_path)
    # The direct dataclass fields permit opaque bytes; only the native factory
    # admits query science. This tests representation, not native validity.
    raw = b"X" * size
    candidate = replace(plan, query_bytes=raw)
    shown = repr(candidate)
    assert len(shown) < 240
    assert "PreparedRunPlan" in shown
    assert "placed" in shown and "checked_pose_coverage" in shown
    assert str(size) in shown and hashlib.sha256(raw).hexdigest() in shown
    assert "XXXXXXXX" not in shown
    assert "context_json" not in shown and "caller-declared-synthetic@1" not in shown
    assert candidate.describe()["query"] == {
        "bytes": size,
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def test_description_is_detached_and_preserves_frozen_fields_and_equality(tmp_path):
    plan, _ = native_plan(tmp_path)
    before = plan.describe()
    altered = plan.describe()
    altered["query"]["bytes"] = -1
    altered["query"]["sha256"] = "changed"
    altered["context"]["execution"]["constructor_options"]["point_tolerance"] = "9 nm"
    altered["context"]["compatibility"]["features"].append("changed")
    altered["context"]["runtime"].clear()
    assert plan.describe() == before
    assert [field.name for field in fields(plan)] == ["query_bytes", "context_json"]
    assert plan == replace(plan) and hash(plan) == hash(replace(plan))
    with pytest.raises(FrozenInstanceError):
        plan.query_bytes = b"changed"


def test_description_and_repr_do_not_reconstruct_or_check_current_runtime(
    tmp_path, monkeypatch
):
    plan, _ = native_plan(tmp_path)
    before = plan.context

    def forbidden(*args, **kwargs):
        raise AssertionError("inspection must not reconstruct or access runtime")

    monkeypatch.setattr(runtime, "_runtime_identity", forbidden)
    monkeypatch.setattr(runtime, "_source_digest", forbidden)
    monkeypatch.setattr(runtime, "_load_query", forbidden)
    monkeypatch.setattr(PreparedRunPlan, "new_evaluator", forbidden)
    assert plan.describe()["context"] == before
    assert len(repr(plan)) < 240


def test_original_runtime_declarations_can_be_inspected_without_admitting_execution(
    tmp_path,
):
    plan, _ = native_plan(tmp_path)
    context = plan.context
    context["runtime"] = {"original_declared_producer": "different"}
    historical = replace(plan, context_json=canonical_json(context))
    assert historical.describe()["context"] == context
    assert "different" not in repr(historical)
    destination = tmp_path / "not-created.sqlite3"
    with pytest.raises(ArgumentError, match="software binding changed"):
        PreparedScreeningRun.create(
            destination,
            plan=historical,
            manifest_path=tmp_path / "not-read.jsonl",
            run_id="not-admitted",
        )
    assert not destination.exists()


@pytest.mark.parametrize(
    "options",
    [
        {"typo": True},
        {"skip_digestion": False},
        {"skip_digestion": True},
        {"kwargs": {}},
    ],
)
def test_description_rejects_undeclared_options(tmp_path, options):
    plan, _ = native_plan(tmp_path)
    with pytest.raises(TypeError):
        plan.describe(**options)


def test_inspection_contract_is_definition_owned_and_has_no_standardizer():
    declared = PreparedRunPlan.describe.digestion_plan
    owner = "pharmacophoremt.screening.prepared_runs.describe"
    assert declared.contract_caller == owner
    info = describe_contract(declared.contracts.resolve(owner), declared.domains)
    assert info["caller"] == owner and info["admits"] == "signature"
    assert declared.enable_argument_digestion and declared.standardizer is None


def test_inspection_preserves_a_nondefault_application_unit_policy(tmp_path):
    with puw.context(standard_units=["angstrom", "fs", "degrees"]):
        plan, _ = native_plan(tmp_path)
        before = deepcopy(puw.configure.get_standard_units())
        description = plan.describe()
        assert puw.configure.get_standard_units() == before
        assert description["context"] == plan.context
        assert (
            description["context"]["execution"]["constructor_options"][
                "point_tolerance"
            ]
            == "0.10 nm"
        )


def test_exact_query_spelling_changes_hash_without_rewriting_context(tmp_path):
    plan, path = native_plan(tmp_path)
    original = path.read_bytes()
    path.write_bytes(original + b"\n")
    changed = build_prepared_run_plan(
        path,
        screening_method="placed",
        score_method=None,
        compatibility=plan.context["compatibility"],
        evaluation_options={"chemical_state": 0, "structure_index": 0},
    )
    assert changed.describe()["context"] == plan.describe()["context"]
    assert changed.describe()["query"]["sha256"] != plan.describe()["query"]["sha256"]
    assert plan.query_bytes == original and changed.query_bytes == original + b"\n"


def test_explicit_inspection_preserves_application_attribution_without_new_credit(
    tmp_path,
):
    import ackredit as ack

    plan, _ = native_plan(tmp_path)
    with ack.session("plan-inspection-application") as application:
        before = ack.get_attribution().to_dict()
        with phmt.attribution():
            plan.describe()
            repr(plan)
        assert ack.current_session() is application
        assert ack.get_attribution().to_dict() == before
