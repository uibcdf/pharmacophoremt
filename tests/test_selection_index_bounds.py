"""Public selections retain integer identity before molecular-provider access."""

import importlib

import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import (
    ComplexBasedModeler,
    from_interaction_collection,
    from_interactions,
)
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.absence_inputs import system
from tests.test_ionic_interactions import observations

INTERACTIONS = importlib.import_module("pharmacophoremt.modeler.interaction_based")
FEATURES = importlib.import_module("pharmacophoremt.modeler.features")
APIS = [
    "adapter",
    "collection",
    "complex",
    "reference_dispatch",
    "adapter_dispatch",
    "collection_dispatch",
    "complex_dispatch",
]


@pytest.fixture(scope="module")
def case():
    source = system("[Na+].[Cl-].[K+]", [[0, 0, 0], [0.3, 0, 0], [0.6, 0, 0]])
    return source, observations(source, [0, 2], [1])


def call(api, case, selection, **options):
    source, observed = case
    if api == "adapter":
        return from_interactions(source, observed, selection, **options)
    if api == "collection":
        return from_interaction_collection(
            source, {"ionic": observed}, selection, **options
        )
    if api == "complex":
        return ComplexBasedModeler(
            source, selection, interaction_collection={"ionic": observed}, **options
        ).build()
    methods = {
        "reference_dispatch": "reference-ligand",
        "adapter_dispatch": "interaction-based",
        "collection_dispatch": "interaction-collection",
        "complex_dispatch": "complex-based",
    }
    if api == "adapter_dispatch":
        options["interactions"] = observed
    elif api in {"collection_dispatch", "complex_dispatch"}:
        options["interaction_collection"] = {"ionic": observed}
    return phmt.model(
        source, method=methods[api], ligand_selection=selection, **options
    )


@pytest.mark.parametrize("api", APIS)
@pytest.mark.parametrize("large", [2**63, 2**64 - 1])
def test_large_unsigned_ligand_selection_refuses_before_molecular_work(
    api, large, case, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("A large unsigned selection cannot reach molecular-provider work")

    for name in ("get", "select", "convert", "copy"):
        monkeypatch.setattr(msm, name, forbidden)
    with pytest.raises(ArgumentError, match="ligand_selection"):
        call(api, case, np.array([large], dtype=np.uint64))


@pytest.mark.parametrize("large", [2**63, 2**64 - 1])
def test_native_complex_constructor_guard_refuses_overflow_during_bypass(large, case):
    source, observed = case
    with pytest.raises(ArgumentError, match="ligand_selection"):
        ComplexBasedModeler(
            source,
            np.array([large], dtype=np.uint64),
            interaction_collection={"ionic": observed},
            skip_digestion=True,
        )


@pytest.mark.parametrize(
    "method, module, endpoint",
    [
        ("reference-ligand", "reference_ligand", "from_ligand"),
        ("interaction-based", "interaction_based", "from_interactions"),
        (
            "interaction-collection",
            "interaction_collection",
            "from_interaction_collection",
        ),
        ("complex-based", "complex_based", "ComplexBasedModeler"),
    ],
)
def test_dispatcher_refuses_overflow_before_entering_endpoint(
    method, module, endpoint, case, monkeypatch
):
    source, observed = case

    def forbidden(*args, **kwargs):
        pytest.fail(
            "The public dispatcher must validate its own selection before delegation"
        )

    monkeypatch.setattr(
        importlib.import_module("pharmacophoremt.modeler." + module),
        endpoint,
        forbidden,
    )
    options = {}
    if method == "interaction-based":
        options["interactions"] = observed
    elif method != "reference-ligand":
        options["interaction_collection"] = {"ionic": observed}
    with pytest.raises(ArgumentError, match="ligand_selection"):
        phmt.model(
            source,
            method=method,
            ligand_selection=np.array([2**64 - 1], dtype=np.uint64),
            **options,
        )


@pytest.mark.parametrize("argument", ["ligand_selection", "receptor_selection"])
@pytest.mark.parametrize("value", [[-1], [True], [0.5], [[0]], []])
def test_invalid_selection_diagnostic_names_its_actual_argument(argument, value):
    options = {"ligand_selection": "all", argument: value}
    with pytest.raises(ArgumentError) as caught:
        phmt.model(object(), method="reference-ligand", **options)
    assert caught.value.extra["argument"] == argument


@pytest.mark.parametrize("large", [2**63, 2**64 - 1])
def test_receptor_overflow_refuses_before_the_native_route_option_policy(large):
    with pytest.raises(ArgumentError) as caught:
        phmt.model(
            object(),
            method="reference-ligand",
            receptor_selection=np.array([large], dtype=np.uint64),
        )
    assert caught.value.extra["argument"] == "receptor_selection"
    assert "representable" in caught.value.extra["reason"]


@pytest.mark.parametrize("api", APIS)
@pytest.mark.parametrize("dtype", [np.int32, np.int64, np.uint32, np.uint64])
def test_ordered_representable_selections_reach_provider_boundary_without_wrap(
    api, dtype, case, monkeypatch
):
    supplied = np.array([2, 0], dtype=dtype)
    seen = []

    class ReachedFrame(Exception):
        pass

    def frame(source, selection, *args, **kwargs):
        seen.append(selection)
        raise ReachedFrame

    monkeypatch.setattr(INTERACTIONS, "source_frame", frame)
    monkeypatch.setattr(FEATURES, "source_frame", frame)
    with pytest.raises(ReachedFrame):
        call(api, case, supplied)
    assert len(seen) == 1 and seen[0].dtype == np.int64
    np.testing.assert_array_equal(seen[0], [2, 0])
    assert supplied.dtype == dtype and supplied.tolist() == [2, 0]


@pytest.mark.parametrize(
    "selection, expected",
    [(None, "all"), ("all", "all"), ("atom_index in [2, 0]", "atom_index in [2, 0]")],
)
def test_optional_reference_selection_and_literal_expressions_keep_owner_semantics(
    selection, expected, monkeypatch
):
    owner = importlib.import_module("pharmacophoremt.modeler.reference_ligand")
    source, result = object(), object()
    seen = []

    def endpoint(actual, *, selection):
        assert actual is source
        seen.append(selection)
        return result

    monkeypatch.setattr(owner, "from_ligand", endpoint)
    assert (
        phmt.model(source, method="reference-ligand", ligand_selection=selection)
        is result
    )
    assert seen == [expected]


@pytest.mark.parametrize("api", APIS)
def test_exact_int64_maximum_is_not_wrapped_or_refused_as_unrepresentable(
    api, case, monkeypatch
):
    seen = []

    class ReachedFrame(Exception):
        pass

    def frame(source, selection, *args, **kwargs):
        seen.append(selection)
        raise ReachedFrame

    monkeypatch.setattr(INTERACTIONS, "source_frame", frame)
    monkeypatch.setattr(FEATURES, "source_frame", frame)
    with pytest.raises(ReachedFrame):
        call(api, case, np.array([2**63 - 1], dtype=np.uint64))
    assert seen[0].dtype == np.int64 and seen[0].tolist() == [2**63 - 1]
    # Molecular bounds remain the provider's responsibility; no atom access ran.


@pytest.mark.parametrize("skip", [False, True])
def test_valid_explicit_receptor_selection_retains_native_unsupported_option_error(
    skip, case
):
    source, observed = case
    with pytest.raises(ArgumentError, match="partner boundary") as caught:
        ComplexBasedModeler(
            source,
            [2, 0],
            receptor_selection=[1],
            interaction_collection={"ionic": observed},
            skip_digestion=skip,
        )
    assert caught.value.extra["argument"] == "receptor_selection"


@pytest.mark.parametrize("api", ["adapter", "collection", "complex"])
@pytest.mark.parametrize("dtype", [np.int32, np.uint64])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_actual_observed_models_preserve_order_quantities_attribution_and_source(
    api, dtype, unit, case
):
    source, _ = case
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    selection = np.array([2, 0], dtype=dtype)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        with phmt.attribution():
            query = call(api, case, selection, radius=".02 nm")
        assert query.n_interaction_sites == 2
        assert query.metadata["attribution"]["status"] == "captured"
        metadata = (
            query.metadata
            if api == "adapter"
            else query.metadata["components"][0]["metadata"]
        )
        assert metadata["ligand_atom_indices"] == [2, 0]
        result = PoseEvaluator(query).evaluate(source, selection=[2, 0])
        assert result["status"] == "matched" and result["fit_value"] == 1
        for site in query.interaction_sites:
            assert float(puw.get_value(site.radius, to_unit="nm")) == pytest.approx(
                0.02
            )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
    assert selection.dtype == dtype and selection.tolist() == [2, 0]
