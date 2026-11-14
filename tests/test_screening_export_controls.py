"""Cached scalar exports keep their ownership and explicit public admission."""

import csv
import inspect
from io import StringIO

import molsysmt as msm
import numpy as np
import pandas as pd
import pytest
from argdigest import describe_contract

from pharmacophoremt import Pharmacophore
from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt.screening import VirtualScreening

COLUMNS = [
    "rank",
    "input_index",
    "ranking_score",
    "score_method",
    "fit_value",
    "conf_id",
    "status",
]
EXPECTED = [
    ["1", "7", "0.75", "checked_pose_coverage@1", "0.75", "3", "matched"],
    ["2", "2", "0.75", "checked_pose_coverage@1", "0.75", "1", "matched"],
]


def cached(kind=VirtualScreening, count=2):
    query = Pharmacophore()
    query.add_interaction_site(
        InteractionSite(Sphere("[0,0,0] nm", ".1 nm"), "hydrophobicity")
    )
    screen = kind(query, screening_method="placed")
    molecular_reference = object()
    screen.matches = [
        dict(
            input_index=index,
            ranking_score=0.75,
            score_method="checked_pose_coverage@1",
            fit_value=0.75,
            conf_id=frame,
            status="matched",
            mol=molecular_reference,
        )
        for index, frame in [(7, 3), (2, 1)][:count]
    ]
    screen.evaluations = [{"original": "complete cohort remains outside the hit table"}]
    return screen


@pytest.mark.parametrize("name", ["to_dataframe", "to_csv"])
def test_explicit_closed_definition_owned_contract(name):
    method = getattr(VirtualScreening, name)
    control = inspect.signature(method).parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    plan = method.digestion_plan
    assert plan.contract_caller == method.__module__ + "." + method.__name__
    assert (
        describe_contract(plan.contracts.resolve(plan.contract_caller), plan.domains)[
            "admits"
        ]
        == "signature"
    )

    class ApplicationScreen(VirtualScreening):
        pass

    screen = cached(ApplicationScreen)
    if name == "to_dataframe":
        assert screen.to_dataframe(skip_digestion=False)["input_index"].tolist() == [
            7,
            2,
        ]
    else:
        destination = StringIO()
        screen.to_csv(destination, skip_digestion=False)
        assert list(csv.reader(StringIO(destination.getvalue()))) == [
            COLUMNS,
            *EXPECTED,
        ]


@pytest.mark.parametrize("name", ["to_dataframe", "to_csv"])
@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_controls_refuse_before_output(name, flag, tmp_path):
    screen = cached()
    before = [row.copy() for row in screen.matches]
    destination = tmp_path / "existing.csv"
    destination.write_bytes(b"original bytes")
    args = [destination] if name == "to_csv" else []
    with pytest.raises(ArgumentError):
        getattr(screen, name)(*args, skip_digestion=flag)
    assert screen.matches == before
    assert destination.read_bytes() == b"original bytes"


def test_skip_control_error_names_the_supplied_argument():
    with pytest.raises(ArgumentError, match="skip_digestion"):
        _contracts.digest_skip_digestion(None)
    with pytest.raises(ArgumentError, match="essential"):
        _contracts.digest_essential(None)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        Pharmacophore().to_dataframe(skip_digestion=None)


@pytest.mark.parametrize("count", [0, 2])
@pytest.mark.parametrize(
    "options", [{}, {"skip_digestion": False}, {"skip_digestion": True}]
)
def test_cached_values_schema_custody_and_csv_parity(
    count, options, tmp_path, monkeypatch
):
    screen = cached(count=count)
    before = [row.copy() for row in screen.matches]
    evaluations = screen.evaluations

    def forbidden(*args, **kwargs):
        pytest.fail("Cached export cannot access molecular data or re-evaluate a query")

    for name in ("get", "select", "convert", "copy", "merge", "set"):
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(screen.evaluator, "run", forbidden)
    frame = screen.to_dataframe(**options)
    assert list(frame.columns) == COLUMNS
    assert frame["input_index"].tolist() == [7, 2][:count]
    assert frame["rank"].tolist() == list(range(1, count + 1))
    destination = tmp_path / "hits.csv"
    assert screen.to_csv(destination, **options) is None
    assert list(csv.reader(StringIO(destination.read_text()))) == [
        COLUMNS,
        *EXPECTED[:count],
    ]
    if count:
        frame.loc[0, "ranking_score"] = 0.0
    assert screen.matches == before and screen.evaluations is evaluations


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("kind", ["stream", "pathlike"])
def test_pandas_receives_the_original_destination(skip, kind, tmp_path, monkeypatch):
    class Destination:
        def __fspath__(self):
            return str(tmp_path / "original.csv")

    destination = StringIO() if kind == "stream" else Destination()
    seen = []
    original = pd.DataFrame.to_csv

    def observe(frame, path, *args, **kwargs):
        seen.append(path)
        return original(frame, path, *args, **kwargs)

    monkeypatch.setattr(pd.DataFrame, "to_csv", observe)
    cached().to_csv(destination, skip_digestion=skip)
    assert seen == [destination]
    if kind == "stream":
        assert not destination.closed
        text = destination.getvalue()
    else:
        text = (tmp_path / "original.csv").read_text()
    assert list(csv.reader(StringIO(text))) == [COLUMNS, *EXPECTED]


@pytest.mark.parametrize("skip", [False, True])
def test_csv_preserves_legacy_public_overrides_without_forwarding_control(skip):
    calls = []

    class ApplicationScreen(VirtualScreening):
        def to_dataframe(self):
            calls.append("legacy override has no skip parameter")
            return pd.DataFrame({"application": ["retained"]})

    destination = StringIO()
    cached(ApplicationScreen).to_csv(destination, skip_digestion=skip)
    assert calls == ["legacy override has no skip parameter"]
    assert destination.getvalue() == "application\nretained\n"


@pytest.mark.parametrize("name", ["to_dataframe", "to_csv"])
@pytest.mark.parametrize("skip", [False, True])
def test_unknown_options_refuse_before_output(name, skip, tmp_path):
    destination = tmp_path / "absent.csv"
    args = [destination] if name == "to_csv" else []
    with pytest.raises(TypeError):
        getattr(cached(), name)(*args, skip_digestion=skip, misspelled_option=True)
    assert not destination.exists()


@pytest.mark.parametrize("skip", [False, True])
def test_bad_cached_rows_and_io_failures_keep_owning_exceptions(skip, tmp_path):
    screen = cached()
    destination = tmp_path / "original.csv"
    destination.write_bytes(b"original bytes")
    screen.matches = [{"status": "matched"}]
    with pytest.raises(KeyError):
        screen.to_csv(destination, skip_digestion=skip)
    assert destination.read_bytes() == b"original bytes"
    with pytest.raises(OSError):
        cached().to_csv(tmp_path / "missing" / "out.csv", skip_digestion=skip)


@pytest.mark.parametrize("name", ["to_dataframe", "to_csv"])
@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_actual_public_bypass_is_literal_and_does_not_propagate(
    name, flag, monkeypatch
):
    screen = cached()
    observed = []
    original = _contracts._boolean

    def observe(value, argument):
        if argument == "skip_digestion":
            observed.append(value)
        return original(value, argument)

    monkeypatch.setattr(_contracts, "_boolean", observe)
    args = [StringIO()] if name == "to_csv" else []
    getattr(screen, name)(*args, skip_digestion=flag)
    assert len(observed) == (0 if flag is True else 1) + (name == "to_csv")
    if flag is not True:
        assert observed[0] is flag
    if name == "to_csv":
        assert observed[-1] is False  # Public child admission stays at its own default.
