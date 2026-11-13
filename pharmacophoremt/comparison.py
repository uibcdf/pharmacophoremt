"""Bounded maximum-cardinality comparison of native positive site centers."""

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed, credit_criterion, credit_software
from pharmacophoremt._private.arg_digestion import comparison as contracts
from pharmacophoremt._private.arg_digestion import curation
from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ComparisonLimitError,
)
from pharmacophoremt._version import __version__

METHOD = "center_feature_maximum_cardinality_dice@1"
_RELATIVE_SLACK = float(8 * np.finfo(np.float64).eps)


def _size(model, max_sites):
    contracts.model_type(model)
    if not isinstance(model.interaction_sites, list):
        raise ArgumentError(
            argument="interaction_sites", reason="expected a native site list"
        )
    count = len(model.interaction_sites)
    if count > max_sites:
        raise ComparisonLimitError(
            resource="sites per model", observed=count, limit=max_sites
        )
    curation.model(model)
    return count


def _axis(model):
    from pharmacophoremt.interaction_site.shape import Point, Sphere

    records, coordinates, features = [], [], []
    for index, site in enumerate(model.interaction_sites):
        expected = (
            "point"
            if isinstance(site.shape, Point)
            else "sphere"
            if isinstance(site.shape, Sphere)
            else None
        )
        if expected is None or site.shape_name != expected:
            raise ArgumentError(
                argument="shape", reason="comparison supports only Point/Sphere centers"
            )
        names = _contracts.digest_features(site.features)
        if {"excluded volume", "included volume"}.intersection(names):
            raise ArgumentError(
                argument="features",
                reason="volume constraints are not positive comparison sites",
            )
        center = _contracts.digest_center(site.center)
        radius = _contracts.digest_radius(site.radius) if expected == "sphere" else None
        weight = _contracts.digest_weight(site.weight)
        essential = _contracts.digest_essential(site.essential)
        coordinates.append(puw.get_value(center, to_unit="nm"))
        features.append(frozenset(names))
        records.append(
            dict(
                site_index=index,
                shape=expected,
                features=list(names),
                center=detached(center),
                radius=detached(radius),
                weight=weight,
                essential=essential,
            )
        )
    return (
        np.asarray(coordinates, dtype=float).reshape((-1, 3)),
        features,
        dict(
            name=curation.text(model.name),
            ref_struct=detached(_contracts.digest_ref_struct(model.ref_struct)),
            sites=records,
        ),
    )


def _distances(origin, targets):
    # Subtraction overflow means a separation above every finite threshold.
    # hypot avoids the avoidable overflow/underflow of squaring finite offsets.
    with np.errstate(over="ignore"):
        delta = targets - origin
        return np.hypot(np.hypot(delta[:, 0], delta[:, 1]), delta[:, 2])


@signal(tags=["comparison", "maximum_cardinality"])
@arg_digest(config=contracts.CONFIG)
@attributed("numpy", "pyunitwizard")
def compare_pharmacophores(
    pharmacophore,
    other,
    *,
    distance_tolerance="0.15 nm",
    max_sites=4096,
    max_matrix_entries=1000000,
    skip_digestion=False,
):
    """Compare positive Point/Sphere centers by maximum one-to-one overlap.

    Parameters
    ----------
    pharmacophore, other : Pharmacophore
        Native models already in caller-declared common Cartesian coordinates.
        No fitting, molecular access or frame authentication is performed.
    distance_tolerance : nonnegative length quantity, default='0.15 nm'
        Shared feature names and center distance within this tolerance define
        an edge. Relative binary64 slack is eight machine epsilons; zero is exact.
    max_sites : int, default=4096
        Positive maximum number of sites in each input, including empty partners.
    max_matrix_entries : int, default=1000000
        Positive bound on the rectangular pair/solver matrix. This bounds a
        matrix size, not total elapsed time or all backend allocations.
    skip_digestion : bool, default=False
        Skip argument preprocessing for canonical inputs. Native scientific
        admission, quotas and completeness checks always remain active.

    Returns
    -------
    dict
        Complete report with similarity=2*n_matches/(n_sites+n_other_sites),
        both-empty zero, ordered input snapshots, original site correspondence,
        explicit-unit distances, unmatched sites, criteria and work counters.
        Score/count are symmetric and invariant to site order; tied optimal pair
        identities need not be. Radius, weight and essential flags do not weight
        this declared overlap. Directed/other shapes and volumes are refused.

    Notes
    -----
    Each occurrence is independent even when sites alias. Snapshots retain used
    site axes and ignored constraint declarations, not complete model metadata;
    retain the original native models for full provenance. No input is mutated.
    """
    distance_tolerance = contracts.distance_tolerance(distance_tolerance)
    max_sites, max_matrix_entries = (
        contracts.max_sites(max_sites),
        contracts.max_matrix_entries(max_matrix_entries),
    )
    n_first, n_second = _size(pharmacophore, max_sites), _size(other, max_sites)
    entries = n_first * n_second
    if entries > max_matrix_entries:
        raise ComparisonLimitError(
            resource="pair matrix entries", observed=entries, limit=max_matrix_entries
        )
    first, first_features, first_record = _axis(pharmacophore)
    second, second_features, second_record = _axis(other)
    tolerance_nm = float(puw.get_value(distance_tolerance, to_unit="nm"))
    benefit = np.zeros((n_first, n_second), dtype=float)
    for i, names in enumerate(first_features):
        distances = _distances(first[i], second)
        near = (distances <= tolerance_nm) | (
            (distances - tolerance_nm) <= _RELATIVE_SLACK * tolerance_nm
        )
        benefit[i] = near & np.asarray(
            [bool(names & other_names) for other_names in second_features], dtype=bool
        )
    edges = int(np.count_nonzero(benefit))
    matches, used_first, used_second = [], set(), set()
    if edges:
        from scipy.optimize import linear_sum_assignment

        rows, columns = linear_sum_assignment(benefit, maximize=True)
        credit_software("scipy", __name__ + ".compare_pharmacophores.assignment")
        credit_criterion("assignment", __name__ + ".compare_pharmacophores.assignment")
        for row, column in zip(rows, columns):
            if not benefit[row, column]:
                continue
            i, j = int(row), int(column)
            distance = float(_distances(first[i], second[j : j + 1])[0])
            matches.append(
                dict(
                    site_index=i,
                    other_site_index=j,
                    distance=detached(puw.quantity(distance, "nm")),
                )
            )
            used_first.add(i)
            used_second.add(j)
    count = len(matches)
    return dict(
        method=METHOD,
        producer=dict(pharmacophoremt=__version__),
        complete=True,
        similarity=2.0 * count / (n_first + n_second) if n_first + n_second else 0.0,
        n_sites=n_first,
        n_other_sites=n_second,
        n_matches=count,
        n_compatible_pairs=edges,
        matches=matches,
        unmatched_site_indices=[i for i in range(n_first) if i not in used_first],
        unmatched_other_site_indices=[
            j for j in range(n_second) if j not in used_second
        ],
        inputs=dict(pharmacophore=first_record, other=second_record),
        criteria=dict(
            distance_tolerance=detached(distance_tolerance),
            relative_distance_slack=_RELATIVE_SLACK,
            zero_tolerance="exact",
            score="2*n_matches/(n_sites+n_other_sites); both_empty=0",
            features="any_shared_positive_feature",
            shapes=["point", "sphere"],
            ignored_constraints=["radius", "weight", "essential"],
            common_coordinates="caller_declared_no_alignment_or_authentication",
            tie_policy="one_optimal_matching; tied_pair_identity_not_invariant",
            snapshot_scope="site_axes_not_full_native_model_provenance",
        ),
        parameters=dict(max_sites=max_sites, max_matrix_entries=max_matrix_entries),
        work=dict(matrix_entries=entries, assignment_calls=int(bool(edges))),
    )
