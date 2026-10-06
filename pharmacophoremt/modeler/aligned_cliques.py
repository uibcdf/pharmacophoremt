"""Exact local feature cliques and joint-support hypotheses in a common frame."""

from itertools import combinations

import networkx as nx
import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed, credit_criterion, credit_software
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError, CliqueLimitError
from pharmacophoremt.pharmacophore import Pharmacophore

from .aligned_consensus import (
    _COS_SLACK,
    _orientation_cosine,
    _records,
    _site_from_consensus,
    get_consensus_sites,
)
from .features import CLASSICAL_FEATURES, DEFINITION, get_features

METHOD = "aligned_maximal_clique_consensus@1"


def _limit(stage, resource, observed, limit):
    if observed > limit:
        raise CliqueLimitError(
            stage=stage,
            resource=resource,
            observed=observed,
            limit=limit,
            complete=False,
        )


def _support_inputs(feature_inventories, ligand_ids, min_support):
    if len(feature_inventories) != len(ligand_ids) or min_support > len(ligand_ids):
        raise ArgumentError(
            argument="ligand_ids/min_support",
            reason="one unique identity per inventory and attainable support are required",
        )


@signal(tags=["modeling", "consensus", "cliques"])
@arg_digest()
@attributed("numpy", "pyunitwizard")
def get_aligned_feature_cliques(
    feature_inventories,
    *,
    ligand_ids,
    min_support=2,
    distance_tolerance="0.15 nm",
    direction_tolerance="30 degrees",
    max_graph_nodes=64,
    max_cliques=1000,
):
    """Discover all supported maximal feature cliques in a declared common frame.

    Parameters
    ----------
    feature_inventories : sequence of dict
        Native get_features results; each ligand contributes one prepared frame.
    ligand_ids : sequence of str
        Unique declared identities, including sources with empty inventories.
    min_support : int, default=2
        Minimum distinct-ligand count per clique.
    distance_tolerance : length quantity, default='0.15 nm'
        Inclusive maximum pairwise feature-center distance.
    direction_tolerance : angle quantity, default='30 degrees'
        Inclusive directed donor angle or unoriented aromatic-axis angle.
    max_graph_nodes : int, default=64
        Total feature occurrence bound, checked before graph construction.
    max_cliques : int, default=1000
        Bound on all enumerated maximal cliques, including unsupported ones.

    Returns
    -------
    dict
        Canonical groups of [inventory index, feature index] pairs, unsupported
        groups, graph counts, criteria and complete=True. Exhausting any limit
        raises PHMT-E107; no truncated result is returned.

    Notes
    -----
    Edges require equal kinds, distinct ligands and compatible absolute geometry.
    NetworkX find_cliques implements Bron--Kerbosch with the Tomita adaptation.
    Maximal is inclusion-maximal, not only the largest clique. This discovers
    site correspondences, not DISCO superpositions or RDP patterns. Graph size
    bounds pair construction and storage; the output bound is not a wall-time
    limit or an internal NetworkX search-step bound.

    Examples
    --------
    >>> result = get_aligned_feature_cliques([get_features(a), get_features(b)], ligand_ids=['a', 'b'])
    >>> groups = result['groups']
    """
    _support_inputs(feature_inventories, ligand_ids, min_support)
    inventories = [_records(inventory) for inventory in feature_inventories]
    occurrences = sorted(
        ((i, j) for i, records in enumerate(inventories) for j in range(len(records))),
        key=lambda pair: (ligand_ids[pair[0]], pair[1]),
    )
    _limit("feature_graph", "nodes", len(occurrences), max_graph_nodes)
    distance = float(puw.get_value(distance_tolerance, to_unit="nm"))
    threshold = np.cos(float(puw.get_value(direction_tolerance, to_unit="radians")))
    graph = nx.Graph()
    graph.add_nodes_from(occurrences)
    credit_software("networkx", __name__ + ".get_aligned_feature_cliques.graph")
    for first, second in combinations(occurrences, 2):
        if first[0] == second[0]:
            continue
        one, two = inventories[first[0]][first[1]], inventories[second[0]][second[1]]
        if (
            one["kind"] == two["kind"]
            and np.linalg.norm(one["center"] - two["center"]) <= distance
            and _orientation_cosine(one, two) + _COS_SLACK >= threshold
        ):
            graph.add_edge(first, second)
    cliques = []
    if occurrences:
        target = __name__ + ".get_aligned_feature_cliques.find_cliques"
        credit_criterion("bron_kerbosch", target)
        credit_criterion("tomita_cliques", target)
        for count, clique in enumerate(nx.find_cliques(graph), start=1):
            _limit("feature_cliques", "maximal cliques", count, max_cliques)
            cliques.append(
                sorted(clique, key=lambda pair: (ligand_ids[pair[0]], pair[1]))
            )
    cliques.sort(key=lambda group: [(ligand_ids[i], j) for i, j in group])
    groups, rejected = [], []
    for group in cliques:
        pairs = [list(pair) for pair in group]
        if len(group) < min_support:
            rejected.append(dict(members=pairs, reason="insufficient_ligand_support"))
        else:
            groups.append(pairs)
    return dict(
        method=METHOD,
        definition=DEFINITION,
        groups=groups,
        rejected_groups=rejected,
        ligand_ids=list(ligand_ids),
        n_ligands=len(ligand_ids),
        n_graph_nodes=len(occurrences),
        n_graph_edges=graph.number_of_edges(),
        n_maximal_cliques=len(cliques),
        complete=True,
        criteria=detached(
            dict(
                min_support=min_support,
                distance_tolerance=distance_tolerance,
                direction_tolerance=direction_tolerance,
                max_graph_nodes=max_graph_nodes,
                max_cliques=max_cliques,
                discovery="all_inclusion_maximal_pairwise_compatible_site_groups",
            )
        ),
    )


def _packages(groups, ligand_ids, min_support, min_sites, max_combinations):
    """Enumerate pharmacophoric packages with disjoint occurrences and joint support."""
    occurrences = [frozenset(map(tuple, group)) for group in groups]
    supporters = [frozenset(i for i, _ in group) for group in groups]
    packages, n_trials = [], 0

    def feasible(index, used, common):
        return (
            not used & occurrences[index]
            and len(common & supporters[index]) >= min_support
        )

    def visit(start, chosen, used, common):
        nonlocal n_trials
        if len(chosen) >= min_sites and not any(
            feasible(index, used, common)
            for index in range(len(groups))
            if index not in chosen
        ):
            packages.append(
                dict(
                    site_indices=list(chosen),
                    joint_ligand_ids=sorted(ligand_ids[i] for i in common),
                    joint_support_count=len(common),
                    joint_support_fraction=len(common) / len(ligand_ids),
                )
            )
        for index in range(start, len(groups)):
            n_trials += 1
            _limit(
                "hypothesis_combinations",
                "candidate extensions",
                n_trials,
                max_combinations,
            )
            if feasible(index, used, common):
                visit(
                    index + 1,
                    chosen + (index,),
                    used | occurrences[index],
                    common & supporters[index],
                )

    visit(0, (), frozenset(), frozenset(range(len(ligand_ids))))
    packages.sort(key=lambda package: package["site_indices"])
    for index, package in enumerate(packages):
        package["hypothesis_id"] = f"hypothesis_{index:05d}"
    return packages, n_trials


@signal(tags=["modeling", "consensus", "hypotheses"])
@arg_digest()
@attributed("numpy", "pyunitwizard")
def get_aligned_consensus_hypotheses(
    feature_inventories,
    *,
    ligand_ids,
    min_support=2,
    min_sites=1,
    distance_tolerance="0.15 nm",
    direction_tolerance="30 degrees",
    max_graph_nodes=64,
    max_cliques=1000,
    max_combinations=10000,
):
    """Aggregate aligned cliques and enumerate maximal jointly supported hypotheses.

    Parameters
    ----------
    feature_inventories : sequence of dict
        Native inventories in one declared coordinate frame.
    ligand_ids : sequence of str
        Unique source identities; empty inventories count in support fractions.
    min_support : int, default=2
        Minimum count for each site and for the common supporters of all sites.
    min_sites : int, default=1
        Minimum number of sites in an emitted hypothesis.
    distance_tolerance, direction_tolerance : quantities
        Pairwise clique and final aggregation tolerances.
    max_graph_nodes, max_cliques : int
        Bounds forwarded to get_aligned_feature_cliques.
    max_combinations : int, default=10000
        Bound on attempted candidate-site extensions, including rejected ones.

    Returns
    -------
    dict
        Candidate sites, their correspondence groups, rejected aggregation,
        alternative hypotheses with shared ligand evidence, discovery report,
        combination count and complete=True. Evaluated-empty discovery succeeds.

    Notes
    -----
    A feature occurrence cannot be reused within a hypothesis; different
    hypotheses may share it. Joint support is an intersection, not pairwise
    support. Sites are unweighted feature means with the lexicographically first
    ligand member's orientation, as in get_consensus_sites. Emitted hypotheses
    are inclusion-maximal feasible packages of maximal site cliques, not all
    subcliques or globally optimized pharmacophores. No affinity score is assigned.

    Examples
    --------
    >>> result = get_aligned_consensus_hypotheses([get_features(a), get_features(b)], ligand_ids=['a', 'b'])
    >>> alternatives = result['hypotheses']
    """
    discovery = get_aligned_feature_cliques(
        feature_inventories,
        ligand_ids=ligand_ids,
        min_support=min_support,
        distance_tolerance=distance_tolerance,
        direction_tolerance=direction_tolerance,
        max_graph_nodes=max_graph_nodes,
        max_cliques=max_cliques,
    )
    sites, groups, rejected = [], [], []
    # Alternative cliques may overlap. Aggregate each independently rather than
    # relaxing the existing one-hypothesis occurrence validation.
    for group in discovery["groups"]:
        aggregation = get_consensus_sites(
            feature_inventories,
            [group],
            ligand_ids=ligand_ids,
            min_support=min_support,
            distance_tolerance=distance_tolerance,
            direction_tolerance=direction_tolerance,
        )
        if aggregation["sites"]:
            index = len(sites)
            record = dict(
                aggregation["sites"][0], group_index=index, site_id=f"site_{index:05d}"
            )
            sites.append(record)
            groups.append(group)
        else:
            rejected.append(dict(group=group, evidence=aggregation["rejected_groups"]))
    hypotheses, trials = _packages(
        groups, ligand_ids, min_support, min_sites, max_combinations
    )
    return dict(
        method=METHOD,
        definition=DEFINITION,
        candidate_sites=sites,
        correspondence_groups=groups,
        hypotheses=hypotheses,
        rejected_groups=rejected,
        discovery=discovery,
        ligand_ids=list(ligand_ids),
        n_ligands=len(ligand_ids),
        n_combinations=trials,
        complete=True,
        criteria=detached(
            dict(
                min_support=min_support,
                min_sites=min_sites,
                distance_tolerance=distance_tolerance,
                direction_tolerance=direction_tolerance,
                max_graph_nodes=max_graph_nodes,
                max_cliques=max_cliques,
                max_combinations=max_combinations,
                center_aggregation="unweighted_feature_mean",
                orientation_aggregation="lexicographic_first_ligand_reference",
                hypothesis_support="intersection_of_site_supporters",
            )
        ),
    )


@signal(tags=["modeling", "consensus", "aligned_ligands"])
@arg_digest()
@attributed("molsysmt", "pyunitwizard", model_results=True)
def from_aligned_ligand_cliques(
    ligands,
    *,
    features=CLASSICAL_FEATURES,
    min_support=2,
    min_sites=1,
    distance_tolerance="0.15 nm",
    direction_tolerance="30 degrees",
    radius="0.15 nm",
    max_graph_nodes=64,
    max_cliques=1000,
    max_combinations=10000,
    name=None,
):
    """Build alternative Feature + Shape consensus models from prepared aligned ligands.

    Parameters
    ----------
    ligands : sequence of dict
        Unique ligand_id/molecular_system records; optional selection,
        structure_index and chemical_state default to 'all', 0 and 'reference'.
    features : sequence of str
        Classical families extracted through MolSysMT-supported get_features.
    min_support, min_sites : int
        Shared ligand and site-count requirements for each hypothesis.
    distance_tolerance, direction_tolerance : quantities
        Geometric discovery/aggregation criteria in the declared common frame.
    radius : length quantity, default='0.15 nm'
        Emitted shape radius, independent of discovery tolerance.
    max_graph_nodes, max_cliques, max_combinations : int
        Explicit discovery bounds; exceeding a bound raises PHMT-E107.
    name : str, optional
        Model name prefix; each name includes its deterministic hypothesis ID.

    Returns
    -------
    dict
        Models in hypothesis order, a detached scientific report and complete=True.
        No supported hypothesis yields models=[], not an empty usable model.
        Each model retains source, correspondence and joint-support evidence.

    Notes
    -----
    Inputs are prepared and aligned by the caller through MolSysMT. No chemical
    preparation, hydrogen addition or molecular alignment occurs here. Sites
    begin essential with weight 1; support is not affinity. Optional attribution
    records the whole hypothesis-generation calculation in the report and each
    derived model, retaining original bibliography and producer versions.

    Examples
    --------
    >>> result = from_aligned_ligand_cliques([{'ligand_id':'a', 'molecular_system':a}, {'ligand_id':'b', 'molecular_system':b}])
    >>> models = result['models']
    """
    if min_support > len(ligands) or not set(features) <= set(CLASSICAL_FEATURES):
        raise ArgumentError(
            argument="min_support/features",
            reason="require attainable support and classical chemical families",
        )
    inventories = [
        get_features(
            ligand["molecular_system"],
            selection=ligand.get("selection", "all"),
            structure_index=ligand.get("structure_index", 0),
            chemical_state=ligand.get("chemical_state", "reference"),
            features=features,
        )
        for ligand in ligands
    ]
    report = get_aligned_consensus_hypotheses(
        inventories,
        ligand_ids=[ligand["ligand_id"] for ligand in ligands],
        min_support=min_support,
        min_sites=min_sites,
        distance_tolerance=distance_tolerance,
        direction_tolerance=direction_tolerance,
        max_graph_nodes=max_graph_nodes,
        max_cliques=max_cliques,
        max_combinations=max_combinations,
    )
    sources = detached(
        [
            dict(ligand_id=ligand["ligand_id"], **inventory)
            for ligand, inventory in zip(ligands, inventories)
        ]
    )
    models = []
    for hypothesis in report["hypotheses"]:
        model = Pharmacophore(
            name=f"{name or 'Clique consensus'} {hypothesis['hypothesis_id']}"
        )
        model.metadata = detached(
            dict(
                method=METHOD,
                hypothesis=hypothesis,
                sources=sources,
                consensus=dict(
                    method=METHOD,
                    sites=[
                        report["candidate_sites"][index]
                        for index in hypothesis["site_indices"]
                    ],
                    ligand_ids=report["ligand_ids"],
                    n_ligands=report["n_ligands"],
                    criteria=report["criteria"],
                    complete=report["complete"],
                ),
                emitted_radius=radius,
            )
        )
        for index in hypothesis["site_indices"]:
            model.add_interaction_site(
                _site_from_consensus(report["candidate_sites"][index], radius)
            )
        models.append(model)
    return dict(method=METHOD, models=models, report=detached(report), complete=True)
