"""Bounded invariant feature correspondences before molecular superposition."""

from itertools import combinations

import networkx as nx
import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed, credit_criterion, credit_software
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError, CliqueLimitError
from pharmacophoremt.modeler.aligned_cliques import _limit
from pharmacophoremt.modeler.aligned_consensus import _records
from pharmacophoremt.modeler.reference_ligand import from_feature_inventory

from .correspondence import _noncollinear, get_correspondences
from .feature_neighborhoods import (
    get_feature_pair_dissimilarities,
    rank_rigid_feature_correspondences,
)


@signal(tags=["screening", "correspondence", "rigid"])
@arg_digest()
@attributed("numpy", "pyunitwizard")
def get_rigid_feature_correspondences(
    reference_inventory,
    feature_inventory,
    *,
    correspondence_strategy="association_cliques",
    distance_tolerance="0.15 nm",
    min_matches=3,
    max_graph_nodes=64,
    max_cliques=1000,
    max_trials=10000,
    n_seeds=None,
    max_matrix_entries=1000000,
):
    """Propose injective feature mappings from invariant internal distances.

    Parameters
    ----------
    reference_inventory, feature_inventory : dict
        Native classical get_features results in their original frames.
    correspondence_strategy : str, default='association_cliques'
        'association_cliques' enumerates maximal association-graph mappings;
        'triplet_seeds' reuses the typed non-collinear triplet proposal tool.
        'ranked_triplet_seeds' orders that same family by typed neighborhood
        dissimilarity and optionally retains n_seeds. This is G3PS stage one,
        not its greedy refinement or translation/exclusion correction.
    distance_tolerance : length quantity, default='0.15 nm'
        Intended maximum fitted pair displacement. The necessary internal
        distance condition permits differences up to twice this tolerance.
    min_matches : int, default=3
        Minimum maximal-clique size. Triplet proposals always contain three
        pairs; the consumer must test min_matches after fitting.
    max_graph_nodes, max_cliques : int
        Association-pair node and enumerated maximal-clique bounds.
    max_trials : int, default=10000
        Raw candidate-product bound for triplet enumeration.
    n_seeds : int or None
        Scientific guess limit for ranked_triplet_seeds; None retains all.
        Other families reject a supplied limit. Selection may miss alignments.
    max_matrix_entries : int
        Per-matrix bound for ranked neighborhood comparison.

    Returns
    -------
    dict
        Canonical correspondences, proposal-family counts, criteria and
        complete=True. PHMT-E107 marks exhausted resources; no partial output.

    Notes
    -----
    No molecular access, fitting or orientation test occurs here. Both frames
    must provide non-collinear centers for a proposal. Distances cannot rule out
    reflections. Completion covers the declared finite proposal family only:
    neither method proves continuous global optimality. Maximal cliques exclude
    submappings even if fitting a maximal mapping later fails. Graph/output
    bounds do not bound internal NetworkX search steps or elapsed time.

    Examples
    --------
    >>> proposals = get_rigid_feature_correspondences(reference, candidate)
    >>> mappings = proposals['correspondences']
    """
    first, second = _records(reference_inventory), _records(feature_inventory)
    if n_seeds is not None and correspondence_strategy != "ranked_triplet_seeds":
        raise ArgumentError(argument="n_seeds", reason="requires ranked_triplet_seeds")
    tolerance = float(puw.get_value(distance_tolerance, to_unit="nm"))
    if len(first) < 3 or not _noncollinear(np.array([r["center"] for r in first])):
        raise ArgumentError(
            argument="reference_inventory",
            reason="require at least three non-collinear feature centers",
        )
    counts = {}
    if correspondence_strategy in {"triplet_seeds", "ranked_triplet_seeds"}:
        proposals = get_correspondences(
            from_feature_inventory(reference_inventory, radius=distance_tolerance),
            feature_inventory,
            max_trials=max_trials,
        )
        if not proposals["complete"]:
            raise CliqueLimitError(
                stage="triplet_proposals",
                resource="candidate products",
                observed=max_trials + 1,
                limit=max_trials,
                complete=False,
            )
        correspondences = proposals["correspondences"]
        counts = {key: proposals[key] for key in ("n_trials", "n_pruned")}
        if correspondence_strategy == "ranked_triplet_seeds":
            comparison = get_feature_pair_dissimilarities(
                reference_inventory,
                feature_inventory,
                distance_tolerance=distance_tolerance,
                max_matrix_entries=max_matrix_entries,
            )
            ranking = rank_rigid_feature_correspondences(
                correspondences,
                comparison,
                n_seeds=n_seeds,
            )
            correspondences = ranking["correspondences"]
            counts.update(
                neighborhood_comparison=comparison,
                seed_ranking=ranking,
                n_ranked_seeds=ranking["n_selected"],
                n_omitted_seeds=ranking["n_omitted"],
                selection_exhaustive=ranking["selection_exhaustive"],
            )
    else:
        # Check before constructing the potentially quadratic pair graph.
        n_nodes = sum(a["kind"] == b["kind"] for a in first for b in second)
        _limit("association_graph", "nodes", n_nodes, max_graph_nodes)
        nodes = [
            (i, j)
            for i, a in enumerate(first)
            for j, b in enumerate(second)
            if a["kind"] == b["kind"]
        ]
        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        credit_software(
            "networkx", __name__ + ".get_rigid_feature_correspondences.graph"
        )
        for (i, j), (k, column) in combinations(nodes, 2):
            if (
                i != k
                and j != column
                and abs(
                    np.linalg.norm(first[i]["center"] - first[k]["center"])
                    - np.linalg.norm(second[j]["center"] - second[column]["center"])
                )
                <= 2 * tolerance
            ):
                graph.add_edge((i, j), (k, column))
        correspondences, count, rejected = [], 0, 0
        if nodes:
            target = __name__ + ".get_rigid_feature_correspondences.find_cliques"
            credit_criterion("bron_kerbosch", target)
            credit_criterion("tomita_cliques", target)
            for count, clique in enumerate(nx.find_cliques(graph), 1):
                _limit("association_cliques", "maximal cliques", count, max_cliques)
                pairs = sorted(clique)
                if len(pairs) < min_matches or not all(
                    _noncollinear(np.array([records[p[axis]]["center"] for p in pairs]))
                    for axis, records in enumerate((first, second))
                ):
                    rejected += 1
                    continue
                correspondences.append([list(pair) for pair in pairs])
        counts = dict(
            n_graph_nodes=n_nodes,
            n_graph_edges=graph.number_of_edges(),
            n_maximal_cliques=count,
            n_pruned=rejected,
        )
    if correspondence_strategy != "ranked_triplet_seeds":
        correspondences.sort()
    return dict(
        method=f"rigid_{correspondence_strategy}@1",
        correspondences=correspondences,
        complete=True,
        **counts,
        criteria=detached(
            dict(
                correspondence_strategy=correspondence_strategy,
                distance_tolerance=distance_tolerance,
                pair_distance_multiplier=2,
                min_matches=min_matches,
                max_graph_nodes=max_graph_nodes,
                max_cliques=max_cliques,
                max_trials=max_trials,
                n_seeds=n_seeds,
                max_matrix_entries=max_matrix_entries,
                completion_scope="declared_finite_correspondence_proposal_family",
            )
        ),
    )
