"""Explicit controls retain native interaction and hypothesis semantics."""

import inspect

import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import (
    compose_pharmacophores,
    copy_pharmacophore,
    from_interaction_collection,
    from_interactions,
)
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.interaction_collection_cases import build_case, observe

OPERATIONS = [from_interactions, from_interaction_collection, compose_pharmacophores]


@pytest.fixture(scope="module")
def case():
    source, ligand, partner = build_case()
    return source, ligand, observe(source, ligand, partner)


def components(case, radius=".02 nm"):
    source, ligand, analyses = case
    return {
        name: from_interactions(source, observed, ligand, radius=radius)
        for name, observed in analyses.items()
    }


def call(case, operation, options):
    source, ligand, analyses = case
    if operation == "adapter":
        return from_interactions(source, analyses["ionic"], ligand, **options)
    if operation == "collection":
        return from_interaction_collection(source, analyses, ligand, **options)
    return compose_pharmacophores(components(case), **options)


@pytest.mark.parametrize("operation", OPERATIONS)
def test_explicit_keyword_only_control_and_defining_closed_contract(operation):
    parameter = inspect.signature(operation).parameters["skip_digestion"]
    assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
    assert parameter.default is False
    owner = operation.__module__ + "." + operation.__name__
    plan = operation.digestion_plan
    assert plan.contract_caller == owner
    contract = plan.contracts.resolve(owner)
    assert contract is not None
    assert describe_contract(contract, plan.domains)["admits"] == "signature"


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize(
    "operation,expected", [("adapter", 1), ("collection", 9), ("composer", 9)]
)
def test_actual_scientific_evidence_and_saved_semantics_agree_across_controls(
    case, unit, operation, expected, tmp_path
):
    source, ligand, _ = case
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = puw.configure.report()
        snapshots = []
        for index, control in enumerate(
            ({}, {"skip_digestion": False}, {"skip_digestion": True})
        ):
            options = dict(control)
            if operation != "composer":
                options["radius"] = puw.standardize(puw.quantity(0.02, "nm"))
            else:
                options["duplicate_policy"] = "same_participant"
            query = call(case, operation, options)
            assert query.n_interaction_sites == expected
            assert sum(site.weight for site in query.interaction_sites) == expected
            assert all(site.essential for site in query.interaction_sites)
            evaluation = PoseEvaluator(query).evaluate(source, selection=ligand)
            assert evaluation["status"] == "matched" and evaluation["fit_value"] == 1
            snapshots.append(detached(query.metadata))
            path = tmp_path / (str(index) + ".json")
            phmt.io.to_json(query, str(path))
            restored = phmt.io.load_json(str(path))
            assert restored.metadata == query.metadata
            assert [s.metadata for s in restored.interaction_sites] == [
                s.metadata for s in query.interaction_sites
            ]
            assert (
                PoseEvaluator(restored).evaluate(source, selection=ligand)["fit_value"]
                == 1
            )
        assert snapshots == [snapshots[0]] * 3
        assert puw.configure.report() == policy
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )


@pytest.mark.parametrize("skip", [False, True])
def test_keep_stays_two_independent_constraints_and_does_not_inflate_a_hit(case, skip):
    source, ligand, analyses = case
    query = from_interaction_collection(
        source, analyses, ligand, duplicate_policy="keep", skip_digestion=skip
    )
    assert query.n_interaction_sites == 11
    result = PoseEvaluator(query).evaluate(source, selection=ligand)
    assert result["status"] == "not_matched"
    assert result["fit_value"] == pytest.approx(9 / 11)
    assert len(result["missing_essential_sites"]) == 2


@pytest.mark.parametrize("skip", [False, True])
def test_existing_model_dispatcher_reaches_the_controlled_native_collection(case, skip):
    source, ligand, analyses = case
    query = phmt.model(
        source,
        method="interaction-collection",
        interaction_collection=analyses,
        ligand_selection=ligand,
        skip_digestion=skip,
    )
    assert query.n_interaction_sites == 9


@pytest.mark.parametrize("operation", ["adapter", "collection", "composer"])
@pytest.mark.parametrize("control", [None, 0, 1, "true"])
def test_nonboolean_controls_are_refused(case, operation, control):
    with pytest.raises(ArgumentError):
        call(case, operation, {"skip_digestion": control})


@pytest.mark.parametrize("operation", ["adapter", "collection", "composer"])
@pytest.mark.parametrize("skip", [False, True])
def test_closed_calls_refuse_unknown_keywords(case, operation, skip):
    with pytest.raises(TypeError):
        call(case, operation, {"skip_digestion": skip, "unrecognized_option": 1})


@pytest.mark.parametrize("failure", ["state", "maps", "uncovered"])
@pytest.mark.parametrize("skip", [False, True])
def test_collection_incompatibilities_remain_scientific_errors(case, failure, skip):
    source, ligand, analyses = case
    changed = dict(analyses)
    original = analyses["ionic"]
    if failure == "uncovered":
        replacement = original.invalidate_structures([0])
    else:
        # Explicit negative evidence through the owner codec, not detector output.
        payload = msm.convert(original, to_form="molsysmt.InteractionsDict")
        if failure == "state":
            payload.data["parameters"]["chemical_state_index"] = 1
        else:
            payload.data["atom_source_indices"] = np.arange(original.n_atoms)[::-1]
        replacement = msm.convert(payload, to_form="molsysmt.Interactions")
    changed["ionic"] = replacement
    with pytest.raises(ArgumentError):
        from_interaction_collection(source, changed, ligand, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("failure", ["geometry", "frame"])
def test_composition_conflicts_do_not_average_or_mutate_inputs(case, skip, failure):
    original = components(case)["ionic"]
    changed = copy_pharmacophore(original)
    if failure == "geometry":
        changed.interaction_sites[0].shape.radius = puw.quantity(0.04, "nm")
    else:
        changed.ref_struct = 1
    before = detached(original.metadata)
    with pytest.raises(ArgumentError):
        compose_pharmacophores(
            {"original": original, "changed": changed},
            duplicate_policy="same_participant",
            skip_digestion=skip,
        )
    assert detached(original.metadata) == before
    assert puw.get_value(
        original.interaction_sites[0].radius, to_unit="nm"
    ) == pytest.approx(0.02)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("options", [{"radius": "2 ps"}, {"cation_mapping": "unknown"}])
def test_adapter_profile_and_quantity_errors_precede_source_access(
    case, monkeypatch, skip, options
):
    import pharmacophoremt.modeler.interaction_based as owner

    source, ligand, analyses = case

    def forbidden(*args, **kwargs):
        pytest.fail("invalid native settings reached molecular access")

    monkeypatch.setattr(owner, "source_frame", forbidden)
    with pytest.raises(ArgumentError):
        from_interactions(
            source, analyses["ionic"], ligand, skip_digestion=skip, **options
        )


@pytest.mark.parametrize("skip", [False, True])
def test_parent_uses_explicit_bypass_only_for_its_canonical_internal_calls(
    case, monkeypatch, skip
):
    import pharmacophoremt.modeler.interaction_collection as owner

    source, ligand, analyses = case
    adapter, composer = owner.from_interactions, owner.compose_pharmacophores
    calls = []

    def convert(*args, **kwargs):
        calls.append(("adapter", kwargs.get("skip_digestion")))
        return adapter(*args, **kwargs)

    def compose(*args, **kwargs):
        calls.append(("composer", kwargs.get("skip_digestion")))
        return composer(*args, **kwargs)

    monkeypatch.setattr(owner, "from_interactions", convert)
    monkeypatch.setattr(owner, "compose_pharmacophores", compose)
    query = owner.from_interaction_collection(
        source,
        analyses,
        ligand,
        radius=puw.standardize(puw.quantity(0.02, "nm")),
        skip_digestion=skip,
    )
    assert query.n_interaction_sites == 9
    assert calls == [("adapter", True)] * len(analyses) + [("composer", True)]


@pytest.mark.parametrize("skip", [False, True])
def test_cached_composition_needs_no_molecular_access(case, monkeypatch, skip):
    pieces = components(case)

    def forbidden(*args, **kwargs):
        pytest.fail("cached composition performed molecular science")

    for name in ("get", "select", "convert"):
        monkeypatch.setattr(msm, name, forbidden)
    query = compose_pharmacophores(
        pieces, duplicate_policy="same_participant", skip_digestion=skip
    )
    assert query.n_interaction_sites == 9


@pytest.mark.parametrize("skip", [False, True])
def test_evaluated_empty_analysis_is_preserved_but_not_a_positive_query(case, skip):
    source, ligand, analyses = case
    query = from_interaction_collection(
        source, {"empty": analyses["ionic_empty"]}, ligand, skip_digestion=skip
    )
    assert query.n_interaction_sites == 0
    assert query.metadata["components"][0]["metadata"][
        "evaluated_structure_indices"
    ] == [0]
    with pytest.raises(ArgumentError, match="positive total weight"):
        PoseEvaluator(query)
