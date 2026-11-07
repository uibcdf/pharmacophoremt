"""Public iterator admission, compatibility and actual lazy native attribution."""

import json
import subprocess
import sys

import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import from_ligand
from pharmacophoremt.screening import PoseEvaluator, PreparedInput, screen_prepared
from phmt_test_support.absence_inputs import system


class ObservedInputs:
    def __init__(self, entries=()):
        self.entries = iter(entries)
        self.events = []

    def __iter__(self):
        self.events.append("iter")
        return self

    def __next__(self):
        self.events.append("next")
        return next(self.entries)

    def close(self):
        self.events.append("close")


@pytest.fixture
def prepared():
    source = system()
    query = from_ligand(source, features=["hydrophobicity"], radius="0.02 nm")
    return source, PoseEvaluator(query)


def entry(source, key="work:0"):
    return PreparedInput(key, "source:shared", "occurrence:" + key, source)


def test_public_exports_and_compatibility_helper_are_the_same_objects():
    from pharmacophoremt.screening.prepared_screening import (
        PreparedInput as declared_input,
    )
    from pharmacophoremt.screening.prepared_screening import (
        screen_prepared as declared_screen,
    )
    from phmt_test_support.prepared_library_reference import (
        PreparedInput as compatible_input,
    )
    from phmt_test_support.prepared_library_reference import (
        screen_prepared as compatible_screen,
    )

    assert PreparedInput is declared_input is compatible_input
    assert screen_prepared is declared_screen is compatible_screen
    assert PreparedInput.__module__ == screen_prepared.__module__
    assert screen_prepared.__module__ == "pharmacophoremt.screening.prepared_screening"


def test_definition_contract_is_closed_and_preserves_source_identity(prepared):
    _, evaluator = prepared
    plan = screen_prepared.digestion_plan
    owner = "pharmacophoremt.screening.prepared_screening.screen_prepared"
    assert plan.contract_caller == owner
    description = describe_contract(plan.contracts.resolve(owner), plan.domains)
    assert description["caller"] == owner
    assert description["admits"] == "signature"
    assert plan.enable_argument_digestion
    assert plan.standardizer is None
    source = ObservedInputs()
    outputs = screen_prepared(source, evaluator, score_method="checked_pose_coverage")
    assert source.events == []
    outputs.close()
    assert source.events == []


@pytest.mark.parametrize(
    "options",
    [
        {"typo": True},
        {"skip_digestion": False},
        {"skip_digestion": True},
        {"kwargs": {"inputs": "literal payload"}},
    ],
)
def test_unknown_public_options_fail_before_borrowing_source(prepared, options):
    _, evaluator = prepared
    source = ObservedInputs()
    with pytest.raises(TypeError):
        screen_prepared(
            source, evaluator, score_method="checked_pose_coverage", **options
        )
    assert source.events == []


@pytest.mark.parametrize(
    "overrides",
    [
        {"evaluator": None},
        {"on_error": []},
        {"score_method": True},
        {"evaluation_options": object()},
    ],
)
def test_nontrivial_public_values_are_refused_before_borrowing_source(
    prepared, overrides
):
    _, evaluator = prepared
    source = ObservedInputs()
    options = {"evaluator": evaluator, "score_method": "checked_pose_coverage"}
    options.update(overrides)
    with pytest.raises(ArgumentError):
        screen_prepared(source, **options)
    assert source.events == []


def test_fresh_runtime_import_and_unconsumed_close_need_no_support_or_ackredit(
    tmp_path,
):
    code = """
import sys
blocked = {'ackredit', 'phmt_test_support', 'devtools', 'tests'}
class Guard:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked:
            raise AssertionError('unexpected runtime dependency: '+fullname)
sys.meta_path.insert(0, Guard())
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt.pharmacophore import Pharmacophore
from pharmacophoremt.screening import PoseEvaluator, screen_prepared
query = Pharmacophore()
query.add_interaction_site(InteractionSite(
    Sphere(puw.quantity([0.0, 0.0, 0.0], 'nm'), '0.1 nm'), 'hydrophobicity'))
class Untouched:
    def __iter__(self):
        raise AssertionError('factory or close iterated the source')
    def close(self):
        raise AssertionError('factory closed the borrowed source')
with phmt.attribution():
    outputs = screen_prepared(Untouched(), PoseEvaluator(query),
                              score_method='checked_pose_coverage')
    outputs.close()
assert not any(name.split('.')[0] in blocked for name in sys.modules)
"""
    completed = subprocess.run(
        [sys.executable, "-P", "-B", "-c", code],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_factory_and_unconsumed_close_create_no_application_credit(prepared):
    ackredit = pytest.importorskip("ackredit")
    source, evaluator = prepared
    inputs = ObservedInputs([entry(source)])
    with (
        ackredit.session("unconsumed-public-screen") as application,
        phmt.attribution(),
    ):
        before = ackredit.get_attribution().to_dict()
        outputs = screen_prepared(
            inputs, evaluator, score_method="checked_pose_coverage"
        )
        assert ackredit.get_attribution().to_dict() == before
        outputs.close()
        assert ackredit.get_attribution().to_dict() == before
        assert ackredit.current_session() is application
    assert inputs.events == []


def test_partial_consumption_retains_actual_native_credit_and_source_identity(prepared):
    ackredit = pytest.importorskip("ackredit")
    source, evaluator = prepared
    inputs = ObservedInputs([entry(source), entry(source, "work:1")])
    with ackredit.session("partial-public-screen") as application, phmt.attribution():
        outputs = screen_prepared(
            inputs, evaluator, score_method="checked_pose_coverage"
        )
        first = next(outputs)
        captured = ackredit.get_attribution().to_dict()
        frozen = json.dumps(first, sort_keys=True)
        assert first["native_result"]["attribution"]["status"] == "captured"
        assert first["native_result"]["attribution"]["references"]["items"]
        assert first["native_result"]["attribution"]["references"]["uses"]
        assert first["native_result"]["pose_id"] == first["work_key"] == "work:0"
        assert first["source_key"] == "source:shared"
        assert first["occurrence_key"] == "occurrence:work:0"
        assert first["ranking_score"] == 1
        assert "attribution" not in first
        assert set(first) == {
            "work_key",
            "source_key",
            "occurrence_key",
            "native_result",
            "ranking_score",
            "score_method",
        }
        outputs.close()
        assert ackredit.current_session() is application
        assert ackredit.get_attribution().to_dict() == captured
        assert json.dumps(first, sort_keys=True) == frozen
    assert inputs.events == ["iter", "next"]


def test_source_interruption_preserves_yielded_native_evidence_and_session(prepared):
    ackredit = pytest.importorskip("ackredit")
    source, evaluator = prepared

    def interrupted():
        yield entry(source)
        raise OSError("source ended unexpectedly")

    with (
        ackredit.session("interrupted-public-screen") as application,
        phmt.attribution(),
    ):
        outputs = screen_prepared(
            interrupted(),
            evaluator,
            score_method="checked_pose_coverage",
            on_error="record",
        )
        first = next(outputs)
        frozen = json.dumps(first, sort_keys=True)
        captured = ackredit.get_attribution().to_dict()
        with pytest.raises(OSError, match="source ended unexpectedly"):
            next(outputs)
        assert ackredit.current_session() is application
        assert ackredit.get_attribution().to_dict() == captured
        assert json.dumps(first, sort_keys=True) == frozen
        assert first["native_result"]["attribution"]["status"] == "captured"
