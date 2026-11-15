"""Explicit feature-pair evaluation preserves the supplied index identities."""

import numpy as np
import pytest

from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.screening import evaluate_feature_correspondence
from phmt_test_support.absence_inputs import inventory


def features():
    return inventory([[0, 0, 0], [1, 0, 0]])


@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize("large", [2**63, 2**64 - 1])
def test_unsigned_pair_indices_cannot_alias_a_different_feature(axis, large):
    pairs = np.array([[0, 0]], dtype=np.uint64)
    pairs[0, axis] = large
    with pytest.raises(ArgumentError, match="feature_pairs"):
        evaluate_feature_correspondence(features(), features(), pairs)


@pytest.mark.parametrize("dtype", [np.int32, np.int64, np.uint32, np.uint64])
def test_representable_signed_unsigned_pairs_keep_original_order_and_geometry(dtype):
    pairs = np.array([[1, 1], [0, 0]], dtype=dtype)
    result = evaluate_feature_correspondence(features(), features(), pairs)
    assert result["complete"] and result["all_pairs_valid"]
    assert [row["pair"] for row in result["pair_tests"]] == [[1, 1], [0, 0]]
    assert pairs.dtype == dtype and pairs.tolist() == [[1, 1], [0, 0]]


@pytest.mark.parametrize("pairs", [[], np.empty((0, 2), dtype=np.uint64)])
def test_empty_pair_evaluation_retains_vacuous_completion(pairs):
    result = evaluate_feature_correspondence(features(), features(), pairs)
    assert result["complete"] and result["all_pairs_valid"]
    assert result["pair_tests"] == [] and result["position_rmsd"] is None


@pytest.mark.parametrize("axis", [0, 1])
def test_exact_int64_boundary_reaches_native_inventory_range_guard(axis):
    pairs = np.array([[0, 0]], dtype=np.uint64)
    pairs[0, axis] = 2**63 - 1
    with pytest.raises(ArgumentError, match="indices outside inventories"):
        evaluate_feature_correspondence(features(), features(), pairs)
