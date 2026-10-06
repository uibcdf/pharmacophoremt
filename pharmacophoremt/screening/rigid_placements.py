"""Fit and verify explicitly selected pharmacophoric correspondence alternatives."""

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler.aligned_cliques import _limit
from pharmacophoremt.modeler.aligned_consensus import (
    _records,
    get_aligned_feature_matches,
)
from pharmacophoremt.modeler.features import CLASSICAL_FEATURES, get_features
from pharmacophoremt.modeler.reference_ligand import from_feature_inventory

from .alignment import align_to_pharmacophore
from .feature_geometry import evaluate_feature_correspondence


def _source_inventory(molecular_system, feature_inventory, features, source_options):
    """Shared prepared-source boundary for placement and iterative refinement."""
    if not set(features) <= set(CLASSICAL_FEATURES):
        raise ArgumentError(
            argument="features", reason="require classical chemical families"
        )
    if feature_inventory is None:
        feature_inventory = get_features(
            molecular_system, features=features, **source_options
        )
    _records(feature_inventory)
    if not {r["kind"] for r in feature_inventory["features"]} <= set(features):
        raise ArgumentError(
            argument="feature_inventory",
            reason="inventory contains unrequested feature families",
        )
    return feature_inventory


def _fit_feature_mapping(
    molecular_system, query, pairs, inventory, features, source_options
):
    """Fit through the public provider boundary and verify occurrence identity."""
    fitted = align_to_pharmacophore(
        molecular_system, query, pairs, feature_inventory=inventory, **source_options
    )
    placed_inventory = get_features(
        fitted["molecular_system"], features=features, **source_options
    )
    _records(placed_inventory)
    if [(r["kind"], r["atom_indices"]) for r in placed_inventory["features"]] != [
        (r["kind"], r["atom_indices"]) for r in inventory["features"]
    ]:
        raise ArgumentError(
            argument="feature_inventory",
            reason="provider extraction changed feature identities after a rigid fit",
        )
    return dict(**fitted, inventory=placed_inventory)


@signal(tags=["screening", "placement", "rigid"])
@arg_digest()
@attributed("numpy", "molsysmt", "pyunitwizard")
def get_rigid_feature_placements(
    molecular_system,
    reference_inventory,
    correspondences,
    *,
    selection="all",
    structure_index=0,
    chemical_state="reference",
    features=CLASSICAL_FEATURES,
    feature_inventory=None,
    min_matches=3,
    distance_tolerance="0.15 nm",
    direction_tolerance="30 degrees",
    max_fits=1000,
    max_matrix_entries=1000000,
):
    """Fit each supplied mapping through MolSysMT and verify absolute geometry.

    Parameters
    ----------
    molecular_system : molecular system
        Prepared source accepted by MolSysMT, never changed in place.
    reference_inventory : dict
        Native classical target features; query sites follow its original order.
    correspondences : sequence of mappings
        Each mapping contains at least three injective (reference, source) pairs.
        Choose proposals independently with get_rigid_feature_correspondences or
        another method. An empty sequence is a completed empty placement request.
    selection, structure_index, chemical_state
        Source selection, one frame and declared chemistry, as in get_features.
    features : sequence of str
        Classical families for source extraction/re-extraction. When reusing an
        inventory, declare the same requested families; missing types cannot be
        inferred from empty recognition results.
    feature_inventory : dict, optional
        Inventory from this unchanged source/frame/selection/state. Alignment
        checks axes but cannot authenticate origin or coordinates.
    min_matches : int, default=3
        Required injective full-inventory target matches after fitting.
    distance_tolerance, direction_tolerance : quantities
        Inclusive pair displacement and donor-vector/aromatic-axis criteria.
    max_fits : int, default=1000
        Mapping-count bound checked before any fit.
    max_matrix_entries : int, default=1000000
        Assignment matrix bound per post-fit full-inventory matching.

    Returns
    -------
    dict
        placements retains accepted molecular_system copies and native feature
        inventories. report retains detached accepted/rejected evidence, criteria
        and n_fits. It contains no live molecular systems; complete=True covers
        only the supplied mappings, not the method that generated them.

    Notes
    -----
    Every seed pair must pass absolute position/orientation after a proper fit.
    Full-inventory matching must also meet min_matches. No early stop, pose
    deduplication, preparation or conformer generation occurs. Invalid mappings,
    provider failures, changed feature membership and budgets raise. Consumers
    must propagate proposal-generation incompleteness independently.

    Examples
    --------
    >>> seeds = get_rigid_feature_correspondences(target, source_inventory)
    >>> placed = get_rigid_feature_placements(source, target, seeds['correspondences'], feature_inventory=source_inventory)
    """
    _records(reference_inventory)
    source_options = dict(
        selection=selection,
        structure_index=structure_index,
        chemical_state=chemical_state,
    )
    feature_inventory = _source_inventory(
        molecular_system, feature_inventory, features, source_options
    )
    _limit("rigid_alignment", "scheduled fits", len(correspondences), max_fits)
    query = from_feature_inventory(reference_inventory, radius=distance_tolerance)
    accepted, rejected = [], []
    for proposal_index, pairs in enumerate(correspondences):
        fitted = _fit_feature_mapping(
            molecular_system, query, pairs, feature_inventory, features, source_options
        )
        inventory = fitted["inventory"]
        pair_evaluation = evaluate_feature_correspondence(
            reference_inventory,
            inventory,
            pairs,
            distance_tolerance=distance_tolerance,
            direction_tolerance=direction_tolerance,
        )
        invalid = pair_evaluation["invalid_pairs"]
        matches = get_aligned_feature_matches(
            reference_inventory,
            inventory,
            distance_tolerance=distance_tolerance,
            direction_tolerance=direction_tolerance,
            max_matrix_entries=max_matrix_entries,
        )
        evidence = dict(
            proposal_index=proposal_index,
            alignment=fitted["alignment"],
            matches=matches,
            invalid_seed_pairs=invalid,
            pair_evaluation=pair_evaluation,
        )
        if invalid or len(matches["matches"]) < min_matches:
            rejected.append(dict(evidence, reason="post_fit_geometry_or_match_count"))
        else:
            accepted.append(
                dict(
                    evidence,
                    inventory=inventory,
                    molecular_system=fitted["molecular_system"],
                )
            )
    report = detached(
        dict(
            method="explicit_rigid_feature_placements@1",
            reference_inventory=reference_inventory,
            source_inventory=feature_inventory,
            n_fits=len(correspondences),
            accepted_placements=[
                {
                    key: value
                    for key, value in option.items()
                    if key != "molecular_system"
                }
                for option in accepted
            ],
            rejected_placements=rejected,
            complete=True,
            criteria=dict(
                features=features,
                min_matches=min_matches,
                distance_tolerance=distance_tolerance,
                direction_tolerance=direction_tolerance,
                max_fits=max_fits,
                max_matrix_entries=max_matrix_entries,
                completion_scope="explicit_supplied_mappings_only",
            ),
        )
    )
    return dict(
        method=report["method"], placements=accepted, report=report, complete=True
    )
