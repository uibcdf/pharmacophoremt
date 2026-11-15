"""Operation-local digestion controls never enter saved scientific recipes."""

import json
from functools import wraps

import pytest

from pharmacophoremt import Pharmacophore
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt.io import to_json
from pharmacophoremt.screening import PreparedRunPlan, build_prepared_run_plan
from pharmacophoremt.screening import prepared_runs as runtime
from pharmacophoremt_results import canonical_json

METHODS = ["placed", "rigid", "conformers"]


def plan_options(tmp_path, method):
    query = Pharmacophore()
    for center in ("[0,0,0] nm", "[1,0,0] nm", "[0,1,0] nm"):
        query.add_interaction_site(
            InteractionSite(Sphere(center, ".02 nm"), "positive charge")
        )
    path = tmp_path / "query.json"
    to_json(query, str(path))
    return dict(
        query_path=path,
        screening_method=method,
        score_method=None,
        compatibility=dict(
            prepared_snapshot="analytical-plan@1",
            preparation="explicit",
            features="classical_atomic_formal@1",
            index=None,
            grouping="declared-work",
            numerical={"threads": 1},
        ),
        constructor_options={}
        if method == "placed"
        else {"search_method": "seeded_hit"},
    )


@pytest.mark.parametrize("method", METHODS)
def test_expanded_plan_excludes_local_controls_and_reconstructs_with_default_admission(
    method, tmp_path, monkeypatch
):
    options = plan_options(tmp_path, method)
    plan = build_prepared_run_plan(**options)
    execution = plan.context["execution"]
    for name in ("constructor_options", "evaluation_options"):
        assert not {"skip_digestion", "pose_id", "on_error"} & execution[name].keys()
    assert execution["constructor_options"]["point_tolerance"] == "0.10 nm"
    assert execution["constructor_options"]["direction_tolerance"] == "30 degrees"
    assert execution["on_error"] == "record"
    assert execution["score_method"] == (
        "checked_pose_coverage" if method == "placed" else "seeded_hit"
    )
    seen = []
    native_class = runtime._TOOLS[method]
    original = native_class.__init__

    @wraps(original)
    def constructor(instance, *args, **kwargs):
        assert "skip_digestion" not in kwargs
        seen.append("native default admission")
        return original(instance, *args, **kwargs)

    monkeypatch.setattr(native_class, "__init__", constructor)
    evaluator = plan.new_evaluator()
    assert isinstance(evaluator, runtime._TOOLS[method])
    assert seen == ["native default admission"]
    assert plan.describe()["context"] == plan.context


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("where", ["constructor_options", "evaluation_options"])
@pytest.mark.parametrize("control", [False, True])
def test_explicit_reserved_controls_refuse_before_reconstruction(
    method, where, control, tmp_path, monkeypatch
):
    options = plan_options(tmp_path, method)
    options[where] = dict(options.get(where, {}), skip_digestion=control)

    def forbidden(*args, **kwargs):
        pytest.fail("A reserved plan control must refuse before query reconstruction")

    monkeypatch.setattr(runtime, "_load_query", forbidden)
    with pytest.raises(ArgumentError, match="reserved execution options"):
        build_prepared_run_plan(**options)


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("where", ["constructor_options", "evaluation_options"])
@pytest.mark.parametrize("control", [False, True])
def test_saved_context_still_refuses_injected_controls(
    method, where, control, tmp_path
):
    plan = build_prepared_run_plan(**plan_options(tmp_path, method))
    context = json.loads(plan.context_json)
    context["execution"][where]["skip_digestion"] = control
    with pytest.raises(ArgumentError, match="reserved execution options"):
        PreparedRunPlan(plan.query_bytes, canonical_json(context))
