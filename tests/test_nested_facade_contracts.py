"""Real ArgDigest admission for owned method-specific constructor options."""

from functools import wraps
from importlib import import_module

import pytest
from argdigest import UnknownArgumentError, describe_contract

from pharmacophoremt import Pharmacophore
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt.modeler import LigandBasedModeler
from pharmacophoremt.screening import VirtualScreening


def query():
    result = Pharmacophore()
    for center in ["[0,0,0] nm", "[1,0,0] nm", "[0,1,0] nm"]:
        result.add_interaction_site(
            InteractionSite(Sphere(center, ".1 nm"), "hydrophobicity")
        )
    return result


@pytest.mark.parametrize(
    "facade,owner,methods,dependency",
    [
        (
            LigandBasedModeler,
            "pharmacophoremt.modeler.ligand_based.__init__",
            {"rigid", "aligned_cliques"},
            "consensus_method",
        ),
        (
            VirtualScreening,
            "pharmacophoremt.screening.virtual_screening.__init__",
            {"placed", "rigid", "conformers"},
            "screening_method",
        ),
    ],
)
def test_nested_contract_is_declared_and_keeps_definition_owner(
    facade, owner, methods, dependency
):
    inherited = type("ApplicationFacade", (facade,), {"__module__": "consumer.facades"})
    plan = inherited.__init__.digestion_plan
    assert plan.contract_caller == owner
    contract = plan.contracts.resolve(owner)
    assert contract is not None
    description = describe_contract(contract, plan.domains)
    domain = description["admitted_domains"][0]
    assert domain["depends_on"] == (dependency,)
    assert set(domain["by_value"]) == methods
    if facade is LigandBasedModeler:
        assert "max_fits" in domain["by_value"]["rigid"]
        assert "max_fits" not in domain["by_value"]["aligned_cliques"]
        assert all(
            "min_support" not in opts and "min_sites" not in opts
            for opts in domain["by_value"].values()
        )
    else:
        assert "max_trials" in domain["by_value"]["rigid"]
        assert "max_trials" not in domain["by_value"]["placed"]


@pytest.mark.parametrize(
    "method,option",
    [
        ("rigid", "typo_option"),
        ("aligned_cliques", "typo_option"),
        ("aligned_cliques", "max_fits"),
        ("rigid", "min_support"),
        ("aligned_cliques", "min_sites"),
    ],
)
def test_ligand_unknown_option_is_refused_before_consuming_prepared_inputs(
    method, option
):
    class Inputs:
        consumed = 0

        def __iter__(self):
            self.consumed += 1
            return iter([object(), object()])

    inputs = Inputs()
    with pytest.raises(UnknownArgumentError, match=option):
        LigandBasedModeler(inputs, consensus_method=method, **{option: 1})
    assert inputs.consumed == 0


@pytest.mark.parametrize("option", ["typo_option", "structure_indices"])
@pytest.mark.parametrize("method", ["placed", "rigid", "conformers"])
def test_screening_unknown_option_is_refused_before_entering_native_constructor(
    method, option, monkeypatch
):
    owner = import_module("pharmacophoremt.screening.virtual_screening")

    def forbidden(*args, **kwargs):
        pytest.fail("An unknown option must be refused before native constructor entry")

    name = {
        "placed": "PoseEvaluator",
        "rigid": "RigidPoseSearch",
        "conformers": "ConformerScreening",
    }[method]
    monkeypatch.setattr(owner, name, forbidden)
    with pytest.raises(UnknownArgumentError, match=option):
        VirtualScreening(query(), screening_method=method, **{option: [0]})


@pytest.mark.parametrize("method", ["placed", "rigid", "conformers"])
@pytest.mark.parametrize("skip", [False, True])
def test_virtual_skip_is_consumed_at_facade(method, skip):
    options = {} if method == "placed" else {"search_method": "seeded_hit"}
    screened = VirtualScreening(
        query(), screening_method=method, skip_digestion=skip, **options
    )
    assert screened.screening_method == method
    assert screened.matches == screened.evaluations == []
    assert screened.score_method == (
        "checked_pose_coverage" if method == "placed" else "seeded_hit"
    )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("method", ["rigid", "aligned_cliques"])
def test_ligand_valid_options_forward_once_without_copying_sources(
    skip, method, monkeypatch
):
    module = "rigid_consensus" if method == "rigid" else "aligned_cliques"
    name = "from_rigid_ligands" if method == "rigid" else "from_aligned_ligand_cliques"
    owner = import_module("pharmacophoremt.modeler." + module)
    received = []
    models = [object()]
    report = {"status": "control"}

    @wraps(getattr(owner, name))
    def native(ligands, **kwargs):
        received.append((ligands, kwargs))
        return {"models": models, "report": report}

    monkeypatch.setattr(owner, name, native)
    sources = [object(), object()]
    option = {"max_fits": 7} if method == "rigid" else {"max_combinations": 9}
    modeler = LigandBasedModeler(
        iter(sources),
        consensus_method=method,
        n_points=2,
        min_actives=2,
        skip_digestion=skip,
        **option,
    )
    assert modeler.build() is models and modeler.report is report
    assert len(received) == 1
    assert all(
        record["molecular_system"] is source
        for record, source in zip(received[0][0], sources)
    )
    assert received[0][1] == dict(min_sites=2, min_support=2, **option)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("facade", ["ligand", "screening"])
def test_bypass_keeps_method_and_inert_preparation_refusals(skip, facade):
    if facade == "ligand":
        with pytest.raises(ArgumentError):
            LigandBasedModeler(
                [object(), object()], consensus_method=None, skip_digestion=skip
            )
        with pytest.raises(ArgumentError):
            LigandBasedModeler(
                [object(), object()],
                consensus_method="rigid",
                n_conformers=7,
                skip_digestion=skip,
            )
    else:
        with pytest.raises(ArgumentError):
            VirtualScreening(query(), screening_method=None, skip_digestion=skip)
        with pytest.raises(ArgumentError):
            VirtualScreening(
                query(), screening_method="placed", n_conformers=7, skip_digestion=skip
            )


@pytest.mark.parametrize("value", [0, 1, None, "true"])
def test_virtual_nonboolean_skip_is_not_a_bypass(value):
    with pytest.raises(ArgumentError):
        VirtualScreening(query(), screening_method="placed", skip_digestion=value)


@pytest.mark.parametrize("method", ["placed", "rigid", "conformers"])
def test_run_option_rejection_still_clears_both_facade_caches(method, monkeypatch):
    import molsysmt as msm

    options = {} if method == "placed" else {"search_method": "seeded_hit"}
    screen = VirtualScreening(query(), screening_method=method, **options)
    screen.matches = [object()]
    screen.evaluations = [object()]

    def forbidden(*args, **kwargs):
        pytest.fail("An unknown run option must fail before molecular access")

    for name in ["get", "select", "convert", "copy"]:
        monkeypatch.setattr(msm, name, forbidden)
    with pytest.raises((ArgumentError, UnknownArgumentError), match="typo_option"):
        screen.run([object()], typo_option=True)
    assert screen.matches == screen.evaluations == []


@pytest.mark.parametrize("method", ["rigid", "aligned_cliques"])
def test_application_ligand_subclass_executes_definition_contract(method):
    subclass = type(
        "ApplicationLigands", (LigandBasedModeler,), {"__module__": "consumer.facades"}
    )
    sources = [object(), object()]
    builder = subclass(sources, consensus_method=method)
    assert builder.consensus_method == method and builder.systems == sources


@pytest.mark.parametrize("method", ["placed", "rigid", "conformers"])
def test_application_screening_subclass_executes_definition_contract(method):
    subclass = type(
        "ApplicationScreen", (VirtualScreening,), {"__module__": "consumer.facades"}
    )
    options = {} if method == "placed" else {"search_method": "seeded_hit"}
    screen = subclass(query(), screening_method=method, **options)
    assert screen.screening_method == method and screen.matches == []
