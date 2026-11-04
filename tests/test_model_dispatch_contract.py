"""Scoped public admission; endpoint spies test routing, not molecular science."""

import importlib

import pytest
from argdigest import ArgumentConsistencyError, UnknownArgumentError, describe_contract

import pharmacophoremt as phmt
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from phmt_test_support.interaction_collection_cases import build_case, observe

ROUTES = {
    "reference-ligand": ("reference_ligand", "from_ligand", {}),
    "interaction-based": (
        "interaction_based",
        "from_interactions",
        {"ligand_selection": "all", "interactions": object()},
    ),
    "interaction-collection": (
        "interaction_collection",
        "from_interaction_collection",
        {"ligand_selection": "all", "interaction_collection": {}},
    ),
    "ligand-based": (
        "ligand_based",
        "LigandBasedModeler",
        {"consensus_method": "rigid"},
    ),
    "complex-based": ("complex_based", "ComplexBasedModeler", {}),
    "structure-based": ("structure_based", "StructureBasedModeler", {}),
}


@pytest.fixture(scope="module")
def observations():
    source, ligand, partner = build_case()
    return observe(source, ligand, partner)


@pytest.fixture(params=ROUTES)
def route(request, monkeypatch, observations):
    method = request.param
    module, name, options = ROUTES[method]
    options = dict(options)
    if method == "interaction-based":
        options["interactions"] = next(iter(observations.values()))
    elif method == "interaction-collection":
        options["interaction_collection"] = observations
    owner = importlib.import_module("pharmacophoremt.modeler." + module)
    result, calls = object(), []

    def endpoint(*args, **kwargs):
        calls.append((args, kwargs))
        return result

    class Builder:
        def __init__(self, *args, **kwargs):
            calls.append((args, kwargs))

        def build(self, **kwargs):
            calls.append(((), kwargs))
            return result

    monkeypatch.setattr(owner, name, Builder if name.endswith("Modeler") else endpoint)
    return method, options, result, calls


@pytest.mark.parametrize(
    "input_name", ["positional", "molecular_system", "system", "mol_sys"]
)
def test_source_names_preserve_route_and_identity(route, input_name):
    method, options, result, calls = route
    source = object()
    args = (source,) if input_name == "positional" else ()
    kwargs = {} if args else {input_name: source}
    assert phmt.model(*args, method=method, **kwargs, **options) is result
    assert calls[0][0] == (source,)
    if method == "reference-ligand":
        assert calls[0][1] == {"selection": "all"}
    elif method in {"complex-based", "structure-based"}:
        assert calls[-1] == ((), {"structure_indices": None})
    else:
        assert calls[0][1] == options


def test_unknown_option_is_refused_before_entering_endpoint(route):
    method, options, _, calls = route
    with pytest.raises(UnknownArgumentError, match="raduis"):
        phmt.model(object(), method=method, raduis="0.2 nm", **options)
    assert calls == []


def test_method_domain_rejects_option_from_another_route(route):
    method, options, _, calls = route
    foreign = "n_points" if method != "ligand-based" else "interaction_collection"
    with pytest.raises(UnknownArgumentError, match=foreign):
        phmt.model(object(), method=method, **options, **{foreign: 3})
    assert calls == []


def test_dispatch_contract_is_readable_and_covers_all_routes():
    plan = phmt.model.digestion_plan
    owner = "pharmacophoremt.modeler.dispatcher.model"
    contract = plan.contracts.resolve(owner)
    assert contract is not None
    description = describe_contract(contract, plan.domains)
    domain = description["admitted_domains"][0]
    assert domain["depends_on"] == ("method",)
    assert set(domain["by_value"]) == set(ROUTES)
    assert "structure_indices" in domain["by_value"]["complex-based"]
    assert "structure_index" not in domain["by_value"]["complex-based"]
    assert "selection" not in domain["by_value"]["reference-ligand"]
    assert "ligands" not in domain["by_value"]["ligand-based"]
    assert "min_sites" not in domain["by_value"]["ligand-based"]
    assert "min_support" not in domain["by_value"]["ligand-based"]
    assert "n_points" in domain["by_value"]["ligand-based"]


@pytest.mark.parametrize(
    "first,second",
    [
        ("system", "molecular_system"),
        ("mol_sys", "system"),
        ("mol_sys", "molecular_system"),
    ],
)
def test_conflicting_source_aliases_cannot_silently_replace_input(
    first, second, monkeypatch
):
    owner = importlib.import_module("pharmacophoremt.modeler.reference_ligand")
    monkeypatch.setattr(owner, "from_ligand", lambda *args, **kwargs: object())
    with pytest.raises(ArgumentConsistencyError):
        phmt.model(method="reference-ligand", **{first: object(), second: object()})


@pytest.mark.parametrize("method", ["unimplemented", None])
def test_unknown_method_keeps_its_own_diagnostic(method):
    with pytest.raises(ArgumentError) as error:
        phmt.model(object(), method=method, typo=True)
    assert error.value.extra["argument"] == "method"


def test_default_method_and_build_frame_forwarding(monkeypatch):
    owner = importlib.import_module("pharmacophoremt.modeler.complex_based")
    calls, result = [], object()

    class Builder:
        def __init__(self, source, **kwargs):
            calls.append(kwargs)

        def build(self, **kwargs):
            calls.append(kwargs)
            return result

    monkeypatch.setattr(owner, "ComplexBasedModeler", Builder)
    assert phmt.model(object(), structure_indices=[2, 0]) is result
    assert calls == [
        {"ligand_selection": None, "receptor_selection": None},
        {"structure_indices": [2, 0]},
    ]


@pytest.mark.parametrize("skip", [False, True])
def test_explicit_skip_keeps_existing_bypass(route, skip):
    method, options, result, calls = route
    assert phmt.model(object(), method=method, skip_digestion=skip, **options) is result
    assert calls


def test_skip_keeps_unsupported_method_failure():
    with pytest.raises(NotImplementedError, match="not yet implemented"):
        phmt.model(object(), method="unsupported", skip_digestion=True)
