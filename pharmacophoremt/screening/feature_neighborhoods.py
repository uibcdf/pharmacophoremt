"""Typed pharmacophoric environments and explicit ranking of rigid triplets."""

import numpy as np
from argdigest import arg_digest
from scipy.optimize import linear_sum_assignment
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed, credit_criterion, credit_software
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler.aligned_cliques import _limit
from pharmacophoremt.modeler.aligned_consensus import _records

METHOD = "typed_neighborhood_assignment@1"


@signal(tags=["screening", "correspondence", "neighborhood"])
@arg_digest()
@attributed("numpy", "pyunitwizard")
def get_feature_pair_dissimilarities(
    reference_inventory,
    feature_inventory,
    *,
    distance_tolerance="0.15 nm",
    max_matrix_entries=1000000,
):
    """Compare typed distance neighborhoods without molecular access or fitting.

    Parameters
    ----------
    reference_inventory, feature_inventory : dict
        Native classical inventories; output axes retain their original order.
    distance_tolerance : length quantity
        Uniform positional tolerance on both inventories. Neighbor distance
        differences are divided by twice this tolerance and capped at one.
    max_matrix_entries : int
        Bound on each allocated distance, pair or padded neighbor-cost matrix.
        This does not bound cumulative assignment work or elapsed time.

    Returns
    -------
    dict
        Finite costs, compatible mask, axis sizes, assignment/work counts,
        detached criteria and complete=True. Costs are dimensionless in [0, 1].
        Different focal types are incompatible even when their numeric cost is 1.

    Notes
    -----
    Adapts G3PS section 2.2.1 (Permann et al., 2021): exclude each focal feature,
    assign typed neighbor distances, then divide the optimal cost by the larger
    whole-inventory feature count. Unmatched neighbors have unit cost through
    explicit square padding. Uniform tolerances and this padding are declared
    adaptations. Dissimilarity ranks guesses; it is not a safe rejection test or
    a completed G3PS alignment. Orientations are checked after molecular fitting.
    Empty axes succeed without an assignment. Resource exhaustion raises.

    Examples
    --------
    >>> costs = get_feature_pair_dissimilarities(reference, candidate)
    >>> compatible = costs['compatible']
    """
    first, second = _records(reference_inventory), _records(feature_inventory)
    n_first, n_second = len(first), len(second)
    nonempty = bool(n_first and n_second)
    neighbor_size = max(n_first, n_second) - 1 if nonempty else 0
    largest = (
        max(n_first**2, n_second**2, n_first * n_second, neighbor_size**2)
        if nonempty
        else 0
    )
    _limit("feature_neighborhoods", "matrix entries", largest, max_matrix_entries)
    costs = np.ones((n_first, n_second))
    compatible = np.zeros((n_first, n_second), dtype=bool)
    assignments = 0
    if nonempty:
        positions = [
            np.array([r["center"] for r in records]) for records in (first, second)
        ]
        distances = [
            np.linalg.norm(points[:, None, :] - points[None, :, :], axis=2)
            for points in positions
        ]
        denominator = 2 * float(puw.get_value(distance_tolerance, to_unit="nm"))
        for row, reference in enumerate(first):
            for column, candidate in enumerate(second):
                if reference["kind"] != candidate["kind"]:
                    continue
                compatible[row, column] = True
                if not neighbor_size:
                    costs[row, column] = 0
                    continue
                neighbors = np.ones((neighbor_size, neighbor_size))
                left = [i for i in range(n_first) if i != row]
                right = [j for j in range(n_second) if j != column]
                for i, reference_index in enumerate(left):
                    for j, candidate_index in enumerate(right):
                        if (
                            first[reference_index]["kind"]
                            == second[candidate_index]["kind"]
                        ):
                            neighbors[i, j] = min(
                                abs(
                                    distances[0][row, reference_index]
                                    - distances[1][column, candidate_index]
                                )
                                / denominator,
                                1.0,
                            )
                rows, columns = linear_sum_assignment(neighbors)
                costs[row, column] = float(neighbors[rows, columns].sum()) / max(
                    n_first, n_second
                )
                assignments += 1
        if compatible.any():
            credit_criterion(
                "g3ps_seed_ranking", __name__ + ".get_feature_pair_dissimilarities"
            )
        if assignments:
            target = __name__ + ".get_feature_pair_dissimilarities.assignment"
            credit_software("scipy", target)
            credit_criterion("assignment", target)
    return dict(
        method=METHOD,
        n_reference=n_first,
        n_candidate=n_second,
        costs=costs.tolist(),
        compatible=compatible.tolist(),
        complete=True,
        n_pair_assignments=assignments,
        n_assignment_matrix_entries=assignments * neighbor_size**2,
        largest_matrix_entries=largest,
        criteria=detached(
            dict(
                distance_tolerance=distance_tolerance,
                distance_difference_denominator="twice_uniform_position_tolerance",
                unmatched_neighbor_cost=1,
                normalization="larger_whole_inventory_feature_count",
                orientation_policy="post_fit_only",
                max_matrix_entries=max_matrix_entries,
                completion_scope="typed_neighborhood_comparison_only",
            )
        ),
    )


@signal(tags=["screening", "correspondence", "ranking"])
@arg_digest()
@attributed("numpy")
def rank_rigid_feature_correspondences(
    correspondences, feature_pair_dissimilarities, *, n_seeds=None
):
    """Rank supplied three-pair guesses by summed neighborhood dissimilarity.

    Parameters
    ----------
    correspondences : sequence of mappings
        Exactly three injective pairs each. Native inventory indices must agree
        with the comparison axes. Geometric feasibility is the producer's job.
    feature_pair_dissimilarities : dict
        Completed get_feature_pair_dissimilarities output, also after JSON saving.
        The caller owns its identity/origin; this tool cannot authenticate it.
    n_seeds : int or None
        Retain at most this many guesses; None retains every supplied guess.
        This is a scientific selection, not a failed computation budget.

    Returns
    -------
    dict
        Canonical correspondences, summed scores, supplied proposal indices,
        selected/omitted counts, selection_exhaustive and complete=True. Ties
        use lexicographic pairs then supplied index; duplicates remain separate.

    Notes
    -----
    Implements the multiple-guess ranking part of G3PS section 2.2.1, not its
    greedy refinement or translation/exclusion correction. A finite seed count
    may omit valid alignments; complete concerns ranking/declared selection only.
    No molecular access, fitting or geometry rejection occurs. Source attribution
    is retained separately from newly reached ranking operations.

    Examples
    --------
    >>> ranked = rank_rigid_feature_correspondences(seeds, costs, n_seeds=20)
    >>> mappings = ranked['correspondences']
    """
    report = feature_pair_dissimilarities
    shape = (report["n_reference"], report["n_candidate"])
    costs = np.asarray(report["costs"], dtype=float).reshape(shape)
    compatible = np.asarray(report["compatible"], dtype=bool).reshape(shape)
    ranked = []
    for supplied_index, pairs in enumerate(correspondences):
        if (
            len(pairs) != 3
            or np.any(pairs[:, 0] >= shape[0])
            or np.any(pairs[:, 1] >= shape[1])
        ):
            raise ArgumentError(
                argument="correspondences",
                reason="require triplets inside the comparison axes",
            )
        canonical = tuple(sorted(tuple(pair) for pair in pairs))
        if not all(compatible[pair] for pair in canonical):
            raise ArgumentError(
                argument="correspondences",
                reason="triplet contains incompatible feature types",
            )
        score = float(sum(costs[pair] for pair in canonical))
        ranked.append((score, canonical, supplied_index))
    ranked.sort()
    selected = ranked if n_seeds is None else ranked[:n_seeds]
    if ranked:
        credit_criterion(
            "g3ps_seed_ranking", __name__ + ".rank_rigid_feature_correspondences"
        )
    return dict(
        method="summed_neighborhood_triplet_ranking@1",
        correspondences=[
            [[int(i), int(j)] for i, j in pairs] for _, pairs, _ in selected
        ],
        scores=[score for score, _, _ in selected],
        supplied_proposal_indices=[index for _, _, index in selected],
        n_supplied=len(ranked),
        n_selected=len(selected),
        n_omitted=len(ranked) - len(selected),
        selection_exhaustive=len(ranked) == len(selected),
        complete=True,
        source_attribution=detached(report.get("attribution")),
        criteria=detached(
            dict(
                n_seeds=n_seeds,
                dissimilarity_method=report["method"],
                dissimilarity_criteria=report["criteria"],
                tie_break="canonical_pairs_then_supplied_index",
                completion_scope="supplied_guesses_and_declared_seed_selection",
            )
        ),
    )
