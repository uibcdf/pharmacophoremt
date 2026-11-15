"""Unsigned mappings cannot silently turn into negative source/site indices."""

import importlib

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import from_feature_inventory
from pharmacophoremt.screening import align_to_pharmacophore
from phmt_test_support.absence_inputs import inventory, system

ALIGNMENT = importlib.import_module("pharmacophoremt.screening.alignment")
PLACEMENT = importlib.import_module("pharmacophoremt.screening.rigid_placements")
REFINEMENT = importlib.import_module("pharmacophoremt.screening.rigid_refinement")
CENTERS = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]


@pytest.mark.parametrize("api", ["alignment", "placement", "refinement"])
@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize("large", [2**63, 2**64 - 1])
def test_unrepresentable_unsigned_indices_refuse_before_molecular_work(
    api, axis, large, monkeypatch
):
    features = inventory(CENTERS, ["positive charge"] * 3)
    query = from_feature_inventory(features, radius=".02 nm")
    pairs = np.array([[0, 0], [1, 1], [2, 2]], dtype=np.uint64)
    pairs[2, axis] = large

    def forbidden(*args, **kwargs):
        pytest.fail("A large unsigned index must never become molecular indexing")

    monkeypatch.setattr(ALIGNMENT, "source_frame", forbidden)
    monkeypatch.setattr(PLACEMENT, "_source_inventory", forbidden)
    monkeypatch.setattr(REFINEMENT, "_source_inventory", forbidden)
    with pytest.raises(ArgumentError, match="correspondence"):
        if api == "alignment":
            align_to_pharmacophore(object(), query, pairs, feature_inventory=features)
        else:
            module = PLACEMENT if api == "placement" else REFINEMENT
            operation = (
                module.get_rigid_feature_placements
                if api == "placement"
                else module.refine_rigid_feature_correspondences
            )
            operation(object(), features, [pairs], feature_inventory=features)


@pytest.mark.parametrize("dtype", [np.int32, np.int64, np.uint32, np.uint64])
def test_representable_signed_and_unsigned_mappings_preserve_actual_fit(dtype):
    source = system("[Na+].[K+].[Li+]", CENTERS)
    features = inventory(CENTERS, ["positive charge"] * 3)
    query = from_feature_inventory(features, radius=".02 nm")
    pairs = np.array([[0, 0], [1, 1], [2, 2]], dtype=dtype)
    result = align_to_pharmacophore(source, query, pairs, feature_inventory=features)
    assert result["alignment"]["correspondence"] == [[0, 0], [1, 1], [2, 2]]
    np.testing.assert_allclose(
        puw.get_value(
            msm.get(result["molecular_system"], coordinates=True), to_unit="nm"
        )[0],
        CENTERS,
        atol=1e-12,
    )


@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize("skip", [False, True])
def test_representable_int64_maximum_reaches_native_range_guard(
    axis, skip, monkeypatch
):
    source = system("[Na+].[K+].[Li+]", CENTERS)
    features = inventory(CENTERS, ["positive charge"] * 3)
    query = from_feature_inventory(features, radius=".02 nm")
    pairs = np.array([[0, 0], [1, 1], [2, 2]], dtype=np.uint64)
    pairs[2, axis] = 2**63 - 1

    def forbidden(*args, **kwargs):
        pytest.fail("Representable but out-of-range mappings cannot enter fitting")

    monkeypatch.setattr(ALIGNMENT, "capability", forbidden)
    with pytest.raises(ArgumentError, match="out of range"):
        align_to_pharmacophore(
            source, query, pairs, feature_inventory=features, skip_digestion=skip
        )
