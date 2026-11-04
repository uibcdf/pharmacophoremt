"""Prepared consumer branches use public MolSysMT copies and intentional references."""

from copy import deepcopy

import ackredit as ack
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt.io.phmt import _to_dict
from pharmacophoremt.modeler import ComplexBasedModeler, copy_pharmacophore
from phmt_test_support.interaction_collection_cases import build_case, observe


@pytest.fixture(params=["nm", "pm"])
def prepared(request):
    with puw.context(standard_units=[request.param, "fs", "degrees"]):
        source, ligand, partner = build_case()
        with phmt.attribution():
            source.interactions = observe(source, ligand, partner)
            builder = ComplexBasedModeler(
                source,
                ligand_selection=ligand,
                interaction_collection=dict(source.interactions.items()),
            )
            query = builder.build()
        query.score = 0.9
        yield source, ligand, builder, query


def coordinates(source):
    return puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()


def analyses(source):
    # Provider NaNs mean unavailable measurements; compare with equal NaNs, never zero.
    return {
        name: detached(value.to_dict()) for name, value in source.interactions.items()
    }


@pytest.mark.parametrize(
    "copier",
    [msm.copy, lambda source: source.copy(deep=True)],
    ids=["public", "resident"],
)
def test_explicit_molecular_variants_preserve_maps_then_edit_independently(
    prepared, copier
):
    source, ligand, builder, query = prepared
    original_coordinates = coordinates(source)
    original_analyses = analyses(source)
    original_query = deepcopy(_to_dict(query))
    variant = copier(source)
    assert variant is not source
    np.testing.assert_equal(analyses(variant), original_analyses)
    np.testing.assert_array_equal(coordinates(variant), original_coordinates)
    assert msm.get(variant, n_atoms=True) == msm.get(source, n_atoms=True)
    np.testing.assert_array_equal(
        msm.select(variant, selection=ligand), msm.select(source, selection=ligand)
    )
    variant_builder = ComplexBasedModeler(
        variant,
        ligand_selection=ligand,
        interaction_collection=dict(variant.interactions.items()),
    )
    variant_query = variant_builder.build()
    assert variant_query.molecular_system is variant
    assert (
        _to_dict(variant_query)["interaction_sites"]
        == original_query["interaction_sites"]
    )
    variant_snapshot = deepcopy(_to_dict(variant_query))
    retained = dict(variant.interactions.items())
    assert (
        msm.structure.translate(variant, translation="[1,0,0] nm", in_place=True)
        is None
    )
    np.testing.assert_allclose(coordinates(variant), original_coordinates + [1, 0, 0])
    np.testing.assert_array_equal(coordinates(source), original_coordinates)
    np.testing.assert_equal(analyses(source), original_analyses)
    for name in variant.interactions:
        assert not variant.interactions[name].evaluated_structure_indices.size
        np.testing.assert_equal(
            detached(retained[name].to_dict()), original_analyses[name]
        )
    # Cached hypotheses are retained historical results; their sites do not follow a live source.
    assert _to_dict(variant_query) == variant_snapshot
    assert builder.result is query and variant_builder.result is variant_query
    assert (
        msm.structure.translate(source, translation="[0,1,0] nm", in_place=True) is None
    )
    np.testing.assert_allclose(coordinates(source), original_coordinates + [0, 1, 0])
    np.testing.assert_allclose(coordinates(variant), original_coordinates + [1, 0, 0])
    assert _to_dict(query) == original_query


def test_pharmacophore_copy_keeps_live_source_without_a_new_calculation(
    prepared, monkeypatch
):
    source, _, _, query = prepared
    before = deepcopy(_to_dict(query))
    original_coordinates = coordinates(source)

    def forbidden(*args, **kwargs):
        pytest.fail(
            "Pure pharmacophore copy must not inspect, copy or modify its molecular source"
        )

    with ack.session("copy consumer ownership"):
        with ack.capture("pure pharmacophore copy") as run:
            with monkeypatch.context() as patch:
                for name in ["get", "select", "convert", "copy", "set"]:
                    patch.setattr(msm, name, forbidden)
                patch.setattr(type(source), "__deepcopy__", forbidden)
                with phmt.attribution():
                    duplicate = copy_pharmacophore(query)
        assert run.attribution.to_dict()["uses"] == []
    assert duplicate.molecular_system is query.molecular_system is source
    assert duplicate.ref_struct == query.ref_struct
    assert duplicate.ref_mol == query.ref_mol
    assert _to_dict(duplicate) == before
    duplicate.interaction_sites[0].shape.center += puw.quantity([0.1, 0, 0], "nm")
    duplicate.metadata["components"].clear()
    assert _to_dict(query) == before
    np.testing.assert_array_equal(coordinates(source), original_coordinates)
    copied_snapshot = deepcopy(_to_dict(duplicate))
    msm.structure.translate(source, translation="[1,0,0] nm", in_place=True)
    assert duplicate.molecular_system is query.molecular_system is source
    np.testing.assert_allclose(
        coordinates(duplicate.molecular_system), original_coordinates + [1, 0, 0]
    )
    assert _to_dict(query) == before and _to_dict(duplicate) == copied_snapshot


def test_refused_molecular_resource_copy_preserves_the_original_workflow(prepared):
    source, _, builder, query = prepared
    original_coordinates, original_analyses = coordinates(source), analyses(source)
    original_query = deepcopy(_to_dict(query))
    failure = RuntimeError("extension resource cannot be copied")

    class Resource:
        def __deepcopy__(self, memo):
            raise failure

    source.consumer_resource = Resource()
    duplicate = query.copy()
    assert duplicate.molecular_system is source
    with pytest.raises(RuntimeError) as error:
        msm.copy(source)
    assert error.value is failure
    assert builder.result is query and _to_dict(query) == original_query
    np.testing.assert_array_equal(coordinates(source), original_coordinates)
    np.testing.assert_equal(analyses(source), original_analyses)
    assert builder.build().n_interaction_sites == query.n_interaction_sites


def test_refused_coordinate_edit_preserves_native_analysis_and_cached_result(prepared):
    source, _, builder, query = prepared
    variant = msm.copy(source)
    original_coordinates, original_analyses = coordinates(variant), analyses(variant)
    original_query = deepcopy(_to_dict(query))
    with pytest.raises(Exception, match="translation"):
        msm.structure.translate(variant, translation="[1,2] nm", in_place=True)
    np.testing.assert_array_equal(coordinates(variant), original_coordinates)
    np.testing.assert_equal(analyses(variant), original_analyses)
    assert builder.result is query and _to_dict(query) == original_query
