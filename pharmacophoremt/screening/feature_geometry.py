"""Evaluate supplied pharmacophoric pairs in an already shared frame."""

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler.aligned_consensus import (
    _COS_SLACK,
    _orientation_cosine,
    _records,
)


@signal(tags=["screening", "correspondence", "geometry"])
@arg_digest()
@attributed("numpy", "pyunitwizard")
def evaluate_feature_correspondence(
    reference_inventory,
    feature_inventory,
    feature_pairs,
    *,
    distance_tolerance="0.15 nm",
    direction_tolerance="30 degrees",
):
    """Evaluate explicit injective pairs without fitting or choosing a matching.

    Parameters
    ----------
    reference_inventory, feature_inventory : dict
        Native classical inventories expressed in the same coordinate frame.
    feature_pairs : sequence of pairs of int
        Original [reference, source] feature indices, including an empty sequence.
        Out-of-range/repeated indices raise; different kinds are evaluated invalid.
    distance_tolerance, direction_tolerance : quantities
        Inclusive displacement and directed donor/unoriented aromatic-axis limits.

    Returns
    -------
    dict
        Per-pair kind, position and orientation tests; invalid-pair lists;
        positional RMSD and maximum deviation with units; complete=True.
        Empty input has no measurements and vacuously satisfied pair tests.

    Notes
    -----
    No molecular access, correspondence search or minimum match count occurs.
    Missing required donor/normal geometry is invalid inventory input, not a
    scientifically unmatched pair. Angular checks preserve the shared numerical
    cosine slack and aromatic sign equivalence. Completion covers supplied pairs.

    Examples
    --------
    >>> check = evaluate_feature_correspondence(target, source, [[0, 0]])
    >>> valid = check['all_pairs_valid']
    """
    first, second = _records(reference_inventory), _records(feature_inventory)
    if len(feature_pairs) and (
        np.any(feature_pairs[:, 0] >= len(first))
        or np.any(feature_pairs[:, 1] >= len(second))
    ):
        raise ArgumentError(
            argument="feature_pairs", reason="indices outside inventories"
        )
    tolerance = float(puw.get_value(distance_tolerance, to_unit="nm"))
    threshold = np.cos(float(puw.get_value(direction_tolerance, to_unit="radians")))
    tests, distances = [], []
    for row, column in feature_pairs:
        reference, candidate = first[row], second[column]
        distance = float(np.linalg.norm(reference["center"] - candidate["center"]))
        compatible = reference["kind"] == candidate["kind"]
        cosine = _orientation_cosine(reference, candidate) if compatible else None
        distances.append(distance)
        tests.append(
            dict(
                pair=[int(row), int(column)],
                kinds_compatible=compatible,
                position_valid=distance <= tolerance,
                orientation_valid=compatible and cosine + _COS_SLACK >= threshold,
                center_deviation=puw.quantity(distance, "nm"),
                orientation_deviation=None
                if cosine is None
                else puw.quantity(float(np.arccos(cosine)), "radians"),
            )
        )
    invalid = {
        name: [test["pair"] for test in tests if not test[key]]
        for name, key in (
            ("invalid_kind_pairs", "kinds_compatible"),
            ("invalid_position_pairs", "position_valid"),
            ("invalid_orientation_pairs", "orientation_valid"),
        )
    }
    return detached(
        dict(
            method="explicit_feature_pair_geometry@1",
            complete=True,
            pair_tests=tests,
            **invalid,
            invalid_pairs=[
                test["pair"]
                for test in tests
                if not all(
                    test[key]
                    for key in (
                        "kinds_compatible",
                        "position_valid",
                        "orientation_valid",
                    )
                )
            ],
            all_kinds_compatible=not invalid["invalid_kind_pairs"],
            all_positions_valid=not invalid["invalid_position_pairs"],
            all_orientations_valid=not invalid["invalid_orientation_pairs"],
            all_pairs_valid=not any(invalid.values()),
            position_rmsd=None
            if not distances
            else puw.quantity(float(np.sqrt(np.mean(np.square(distances)))), "nm"),
            maximum_center_deviation=None
            if not distances
            else puw.quantity(max(distances), "nm"),
            criteria=dict(
                distance_tolerance=distance_tolerance,
                direction_tolerance=direction_tolerance,
                aromatic_normal="unoriented_axis",
                completion_scope="supplied_pairs_in_shared_frame_only",
            ),
        )
    )
