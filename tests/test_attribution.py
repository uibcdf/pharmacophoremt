"""Real-provider attribution, optional failures and detached scientific reports."""

import json
import subprocess
import sys
import warnings

import ackredit as ack
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import _ackredit
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.io.phmt import load_json, to_json
from pharmacophoremt.modeler import from_ligand, get_features
from pharmacophoremt.screening import PoseEvaluator
from pharmacophoremt.validation import metrics
from pharmacophoremt.validation.retrospective import RetrospectiveValidator
from tests.test_conformer_screening import ensemble
from tests.test_pose_evaluation import system
from tests.test_rigid_search import COORDINATES, reference


@pytest.fixture(scope="module")
def prepared():
    return reference()


def run_reader(code, *arguments):
    result = subprocess.run(
        [sys.executable, "-c", code, *map(str, arguments)],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def test_import_and_empty_activation_are_lazy():
    run_reader("""
import sys
import pharmacophoremt as phmt
assert 'ackredit' not in sys.modules
with phmt.attribution():
    pass
assert 'ackredit' not in sys.modules
""")


def test_two_results_reuse_references_and_preserve_application_session(prepared):
    source, query = prepared
    evaluator = PoseEvaluator(query)
    plain = evaluator.evaluate(source)
    assert "attribution" not in plain
    with ack.session("application") as application:
        with ack.capture("workflow") as workflow:
            with phmt.attribution():
                first = evaluator.evaluate(source)
                with phmt.attribution(False):
                    paused = evaluator.evaluate(source)
                second = evaluator.evaluate(source)
        assert ack.current_session() is application
        assert "attribution" not in paused
        one, two = (result["attribution"] for result in (first, second))
        assert one["status"] == two["status"] == "captured"
        assert first["status"] == second["status"] == plain["status"]
        assert first["fit_value"] == second["fit_value"] == plain["fit_value"]
        assert one["references"]["items"] == two["references"]["items"]
        assert {item["id"] for item in one["references"]["items"]} <= {
            item["id"] for item in workflow.attribution.to_dict()["items"]
        }
        assert one["references"]["uses"] and two["references"]["uses"]
        frozen = json.dumps(two, sort_keys=True)
        one["references"]["items"].clear()
        assert json.dumps(two, sort_keys=True) == frozen


def test_actual_branches_roles_versions_and_empty_success(prepared):
    source, query = prepared
    with ack.session("roles"):
        with phmt.attribution():
            result = PoseEvaluator(query).evaluate(source)
            empty = get_features(system("[Na+]", [[0, 0, 0]]), features=["hb donor"])
            metrics.bedroc([1, 0], [1.0, 0.0])
        payload = result["attribution"]
        declarations = payload["host_references"]
        by_title = {entry["record"]["title"]: entry for entry in declarations}
        assert by_title["SciPy"]["roles"] == ["executed_software"]
        assert (
            by_title["SciPy"]["record"]["version"] == sys.modules["scipy"].__version__
        )
        assert by_title["On implementing 2D rectangular assignment algorithms"][
            "roles"
        ] == ["reference_implementation"]
        assert by_title["Array programming with NumPy"]["roles"] == [
            "software_description"
        ]
        assert "10.1021/ci600426e" not in json.dumps(payload)
        workflow = ack.get_attribution().to_dict()
        assert "10.1021/ci600426e" in json.dumps(workflow)
        assert any(
            "scientific_criterion" in use.get("roles", []) for use in workflow["uses"]
        )
        assert empty["features"] == [] and empty["attribution"]["status"] == "captured"
        assert "10.1021/ci8002478" not in json.dumps(workflow)
        assert "10.1021/ci7000583" not in json.dumps(workflow)


def test_native_model_and_fresh_reader_preserve_original_records(tmp_path, prepared):
    source, _ = prepared
    with ack.session("producer"):
        with phmt.attribution():
            model = from_ligand(source)
        original = model.metadata["attribution"]
        model_path = tmp_path / "model.json"
        to_json(model, model_path)
        assert load_json(model_path).metadata["attribution"] == original
        bibliography = tmp_path / "references.json"
        bibliography.write_text(json.dumps(original["references"]))
        before = ack.get_attribution().to_dict()
        for format in ("markdown", "bibtex", "csl-json", "json", "provenance"):
            assert phmt.attribution_report(original, format=format)
        assert ack.get_attribution().to_dict() == before
    run_reader(
        """
import sys,json,importlib.abc
class NoScience(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'rdkit','scipy','molsysmt','pharmacophoremt'}:
            raise ModuleNotFoundError('reader has no scientific engines: ' + fullname, name=fullname)
sys.meta_path.insert(0, NoScience())
import ackredit as ack
data = json.load(open(sys.argv[1]))
with ack.session('reader'):
    saved = ack.Attribution.from_dict(data)
    assert saved.to_dict() == data
    assert saved.report(format='bibtex')
    assert ack.get_used_items() == {}
    assert not {'rdkit','scipy','molsysmt','pharmacophoremt'} & set(sys.modules)
""",
        bibliography,
    )


@pytest.mark.parametrize(
    "operation", ["load", "capture", "register", "track", "export", "finish"]
)
def test_provider_failures_and_warning_as_error_preserve_science(
    monkeypatch, prepared, operation
):
    source, query = prepared
    plain = PoseEvaluator(query).evaluate(source)

    def fail(*args, **kwargs):
        raise RuntimeError("controlled provider failure")

    if operation == "load":
        monkeypatch.setattr(_ackredit, "backend", fail)
    elif operation == "capture":
        monkeypatch.setattr(ack, "capture", fail)
    elif operation in {"register", "track"}:
        original = getattr(ack, operation + "_item")

        def fail_host(*args, **kwargs):
            item_id = args[0] if args else kwargs.get("id", "")
            if item_id.startswith("pharmacophoremt:"):
                fail()
            return original(*args, **kwargs)

        monkeypatch.setattr(ack, operation + "_item", fail_host)
    elif operation == "export":
        monkeypatch.setattr(ack.Attribution, "to_dict", fail)
    else:
        original = ack.scope

        class FailingExit:
            def __init__(self, *args, **kwargs):
                self.context = original(*args, **kwargs)
                self.host = args[0].startswith("pharmacophoremt.")

            def __enter__(self):
                return self.context.__enter__()

            def __exit__(self, *args):
                self.context.__exit__(*args)
                if self.host:
                    fail()

        monkeypatch.setattr(ack, "scope", FailingExit)
    with ack.session("failed tracking"):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with phmt.attribution():
                result = PoseEvaluator(query).evaluate(source)
    assert result["status"] == plain["status"]
    assert result["fit_value"] == plain["fit_value"]
    assert result["attribution"]["status"] == "failed"
    assert result["attribution"]["references"] is None
    assert result["attribution"]["errors"]
    assert result["attribution"]["host_references"]


def test_tracking_failure_does_not_replace_scientific_exception(monkeypatch, prepared):
    _, query = prepared

    def fail():
        raise RuntimeError("provider failed")

    monkeypatch.setattr(_ackredit, "backend", fail)
    with phmt.attribution():
        with pytest.raises(PoseEvaluationError) as caught:
            PoseEvaluator(query).evaluate(object())
    assert caught.value.code == "PHMT-E103"


def test_missing_provider_retains_offline_provenance():
    run_reader("""
import sys,importlib.abc
class NoAckredit(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] == 'ackredit':
            raise ModuleNotFoundError('absent provider', name='ackredit')
sys.meta_path.insert(0, NoAckredit())
import pharmacophoremt as phmt
from tests.test_rigid_search import reference
source, query = reference()
with phmt.attribution():
    result = phmt.screening.PoseEvaluator(query).evaluate(source)
assert result['status'] == 'matched'
payload = result['attribution']
assert payload['status'] == 'unavailable' and payload['references'] is None
assert payload['host_references'] and not payload['errors']
assert 'ackredit' not in sys.modules
""")


def test_activation_and_saved_report_validation():
    with pytest.raises(ArgumentError):
        with phmt.attribution("yes"):
            pass
    with pytest.raises(ArgumentError):
        phmt.attribution_report({"status": "failed"})


def test_composed_ensemble_and_retrospective_results_keep_bounded_credit(prepared):
    source, query = prepared
    with ack.session("composed"):
        with phmt.attribution():
            single = phmt.screening.ConformerScreening(query).evaluate(source)
            multiple = phmt.screening.ConformerScreening(query).evaluate(
                ensemble(COORDINATES, COORDINATES)
            )
            report = RetrospectiveValidator(
                query, evaluator=phmt.screening.PoseEvaluator(query)
            ).run([source], [system("[Na+]", [[0, 0, 0]])])
    assert (
        single["attribution"]["host_references"]
        == multiple["attribution"]["host_references"]
    )
    assert multiple["attribution"]["scientific_outcome"] == "matched"
    assert "10.1021/ci600426e" in json.dumps(report["attribution"])
    assert report["attribution"]["status"] == "captured"
