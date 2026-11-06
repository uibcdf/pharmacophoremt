"""Source aliases preserve one declared source and refuse competing names."""

from importlib import import_module

import pytest
from argdigest import (
    ArgumentConsistencyError,
    UnknownArgumentError,
    describe_normalization,
)

from pharmacophoremt import Pharmacophore, model
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt.modeler import from_ligand, get_features
from pharmacophoremt.screening import ConformerScreening, PoseEvaluator, RigidPoseSearch
from tests.test_nested_facade_contracts import query
from tests.test_pose_evaluation import system

# Explicit API scopes, including the dispatcher whose aliases are already safe.
CASES = [
    ("pharmacophore", "pharmacophoremt.pharmacophore", "Pharmacophore", "__init__", {}),
    (
        "features",
        "pharmacophoremt.modeler.features",
        "get_features",
        "get_features",
        {},
    ),
    (
        "reference",
        "pharmacophoremt.modeler.reference_ligand",
        "from_ligand",
        "from_ligand",
        {},
    ),
    (
        "interactions",
        "pharmacophoremt.modeler.interaction_based",
        "from_interactions",
        "from_interactions",
        {"interactions": None, "ligand_selection": None},
    ),
    (
        "collection",
        "pharmacophoremt.modeler.interaction_collection",
        "from_interaction_collection",
        "from_interaction_collection",
        {"interaction_collection": None, "ligand_selection": None},
    ),
    (
        "complex",
        "pharmacophoremt.modeler.complex_based",
        "ComplexBasedModeler",
        "__init__",
        {},
    ),
    (
        "structure",
        "pharmacophoremt.modeler.structure_based",
        "StructureBasedModeler",
        "__init__",
        {},
    ),
    (
        "placements",
        "pharmacophoremt.screening.rigid_placements",
        "get_rigid_feature_placements",
        "get_rigid_feature_placements",
        {"reference_inventory": None, "correspondences": None},
    ),
    (
        "alignment",
        "pharmacophoremt.screening.alignment",
        "align_to_pharmacophore",
        "align_to_pharmacophore",
        {"pharmacophore": None, "correspondence": None},
    ),
    (
        "refinement",
        "pharmacophoremt.screening.rigid_refinement",
        "refine_rigid_feature_correspondences",
        "refine_rigid_feature_correspondences",
        {"reference_inventory": None, "correspondences": None},
    ),
    (
        "placed",
        "pharmacophoremt.screening.pose_evaluation",
        "PoseEvaluator",
        "evaluate",
        {},
    ),
    (
        "rigid",
        "pharmacophoremt.screening.rigid_search",
        "RigidPoseSearch",
        "evaluate",
        {},
    ),
    (
        "conformers",
        "pharmacophoremt.screening.conformer_screening",
        "ConformerScreening",
        "evaluate",
        {},
    ),
    (
        "dispatcher",
        "pharmacophoremt.modeler.dispatcher",
        "model",
        "model",
        {"method": "reference-ligand"},
    ),
]


def endpoint(case, inherited=False):
    label, module, name, method, _ = case
    tool = getattr(import_module(module), name)
    if method in {"__init__", "evaluate"} and inherited:
        mixin = type("Presentation", (), {"__module__": "consumer.sources"})
        tool = type(
            "ApplicationTool", (mixin, tool), {"__module__": "consumer.sources"}
        )
    if method == "evaluate":
        return tool(query()).evaluate
    return tool


@pytest.mark.parametrize("case", CASES[:-1], ids=lambda x: x[0])
@pytest.mark.parametrize("alias", ["system", "mol_sys"])
@pytest.mark.parametrize("canonical_supplied", [False, True])
def test_closed_entry_refuses_undeclared_source_names_before_molecular_access(
    case, alias, canonical_supplied, monkeypatch
):
    import molsysmt as msm

    tool = endpoint(case)

    def forbidden(*args, **kwargs):
        pytest.fail("unknown source names must fail before molecular access")

    for name in ["get", "select", "convert", "copy", "extract"]:
        monkeypatch.setattr(msm, name, forbidden)
    options = dict(case[4], **{alias: object()})
    if canonical_supplied:
        options["molecular_system"] = object()
    with pytest.raises(UnknownArgumentError, match=alias):
        tool(**options)


@pytest.mark.parametrize("case", CASES[:-1], ids=lambda x: x[0])
def test_same_object_does_not_admit_an_undeclared_alias(case):
    source = object()
    with pytest.raises(UnknownArgumentError, match="system"):
        endpoint(case)(**dict(case[4], molecular_system=source, system=source))


@pytest.mark.parametrize(
    "names",
    [
        ("molecular_system", "system"),
        ("molecular_system", "mol_sys"),
        ("system", "mol_sys"),
    ],
)
@pytest.mark.parametrize("same_object", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
def test_dispatcher_refuses_competing_declared_names(names, same_object, reverse):
    source = object()
    other = source if same_object else object()
    names = tuple(reversed(names)) if reverse else names
    with pytest.raises(ArgumentConsistencyError):
        model(method="reference-ligand", **{names[0]: source, names[1]: other})


def test_dispatcher_alias_declaration_does_not_apply_to_unrelated_callers():
    plan = model.digestion_plan
    owner = "pharmacophoremt.modeler.dispatcher.model"
    tables = describe_normalization(plan.normalization, owner)
    assert len(tables) == 1
    assert tables[0]["aliases"] == {
        "system": "molecular_system",
        "mol_sys": "molecular_system",
    }
    assert tables[0]["applies_to"] == owner
    assert (
        describe_normalization(plan.normalization, "application.unrelated.function")
        == []
    )


@pytest.mark.parametrize("cls", [PoseEvaluator, RigidPoseSearch, ConformerScreening])
def test_inherited_native_evaluate_preserves_closed_source_admission(cls):
    child = type("ApplicationEvaluator", (cls,), {"__module__": "consumer.sources"})
    with pytest.raises(UnknownArgumentError, match="system"):
        child(query()).evaluate(object(), system=object())


@pytest.mark.parametrize("inherited", [False, True])
def test_canonical_optional_source_keeps_live_reference_and_default(inherited):
    cls = (
        type("ApplicationQuery", (Pharmacophore,), {"__module__": "consumer.sources"})
        if inherited
        else Pharmacophore
    )
    source = object()
    assert cls(molecular_system=source).molecular_system is source
    assert cls().molecular_system is None


@pytest.mark.parametrize("builder", [get_features, from_ligand])
def test_canonical_source_reaches_the_molecular_boundary_unchanged(
    builder, monkeypatch
):
    module = import_module("pharmacophoremt.modeler.features")
    source = object()
    seen = []

    class ReachedSource(Exception):
        pass

    def frame(actual, *args, **kwargs):
        seen.append(actual)
        raise ReachedSource

    monkeypatch.setattr(module, "source_frame", frame)
    with pytest.raises(ReachedSource):
        builder(molecular_system=source, features=["hydrophobicity"])
    assert len(seen) == 1 and seen[0] is source


@pytest.mark.parametrize("source_name", ["molecular_system", "system", "mol_sys"])
def test_real_dispatcher_names_keep_features_model_reference_and_pose_results(
    source_name,
):
    source = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.3, 0, 0]])
    expected = detached(get_features(source))
    actual = model(**{source_name: source}, method="reference-ligand")
    assert actual.molecular_system is source
    assert detached(actual.metadata["source_inventory"]) == expected
    evaluator = PoseEvaluator(actual)
    assert detached(evaluator.evaluate(molecular_system=source)) == detached(
        evaluator.evaluate(source)
    )


def test_internal_bypass_keeps_its_existing_canonical_call_contract():
    source = object()
    assert (
        Pharmacophore(molecular_system=source, skip_digestion=True).molecular_system
        is source
    )
    with pytest.raises(TypeError):
        Pharmacophore(system=source, skip_digestion=True)
