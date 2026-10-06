"""Greedy growth of supplied rigid feature mappings through MolSysMT fitting."""

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed, credit_criterion
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler.aligned_cliques import _limit
from pharmacophoremt.modeler.aligned_consensus import (
    _records,
    get_aligned_feature_matches,
)
from pharmacophoremt.modeler.features import CLASSICAL_FEATURES
from pharmacophoremt.modeler.reference_ligand import from_feature_inventory

from .feature_geometry import evaluate_feature_correspondence
from .rigid_placements import _fit_feature_mapping, _source_inventory


@signal(tags=["screening", "refinement", "rigid"])
@arg_digest()
@attributed("numpy", "molsysmt", "pyunitwizard")
def refine_rigid_feature_correspondences(
    molecular_system,
    reference_inventory,
    correspondences,
    *,
    selection="all",
    structure_index=0,
    chemical_state="reference",
    features=CLASSICAL_FEATURES,
    feature_inventory=None,
    orientation_policy="final",
    min_matches=3,
    distance_tolerance="0.15 nm",
    direction_tolerance="30 degrees",
    max_fits=1000,
    max_matrix_entries=1000000,
):
    """Grow each supplied mapping and retain its best fully evaluated placement.

    Parameters
    ----------
    molecular_system : molecular system
        Unchanged prepared source supported by MolSysMT.
    reference_inventory : dict
        Native classical target features with original occurrence indices.
    correspondences : sequence of mappings
        Injective equal-kind non-collinear seeds containing at least three pairs.
        Seeds may come from any proposal method; empty input is completed empty.
    selection, structure_index, chemical_state
        Declared source selection/frame/state, as in get_features.
    features : sequence of str
        Classical families used for source recognition and re-extraction.
    feature_inventory : dict, optional
        From this unchanged source/selection/frame/state and feature request.
    orientation_policy : {'final', 'each_step'}, default='final'
        final accepts growth by positions; each_step also requires all fitted
        anchors to pass orientation. Both evaluate complete final matching at
        every accepted state and return only placements meeting min_matches.
    min_matches : int, default=3
        Required final injective position/orientation matches, not seed size.
    distance_tolerance, direction_tolerance : quantities
        Inclusive pair displacement and directed donor/aromatic-axis limits.
    max_fits : int, default=1000
        Total initial/trial fits, checked before each provider call. Exhaustion
        raises instead of returning a partial or evaluated-empty result.
    max_matrix_entries : int, default=1000000
        Bound per full-inventory assignment matrix, including dummy columns.

    Returns
    -------
    dict
        At most one best placement per supplied seed, plus detached report of
        every initial/trial fit, accepted/rejected growth, termination and counts.
        Live systems appear only in placements. Duplicate seeds remain independent.

    Notes
    -----
    Adapts G3PS section 2.2.2: choose the closest unblocked same-type pair, refit
    from the unchanged original source, and accept only if every collected pair
    meets the growth policy. Rejection permanently blocks that pair for this
    seed and preserves the previous accepted state. Accepted rows/columns cannot
    be reused. Ties use original pair indices. No sufficient-match early stop,
    seed skipping, translation rescue or orientation-aware fit is implemented.
    Best accepted state maximizes final full-inventory match count, then minimizes
    RMSD of those matched centers, then keeps the earliest fit. Fitting anchors
    and final matches are distinct; final-policy anchors may fail orientation.
    complete=True covers supplied seeds and this greedy policy, not global search.

    Examples
    --------
    >>> result = refine_rigid_feature_correspondences(source, target, seeds, orientation_policy='each_step')
    >>> alternatives = result['placements']
    """
    first = _records(reference_inventory)
    source_options = dict(
        selection=selection,
        structure_index=structure_index,
        chemical_state=chemical_state,
    )
    feature_inventory = _source_inventory(
        molecular_system, feature_inventory, features, source_options
    )
    _limit("rigid_refinement", "minimum scheduled fits", len(correspondences), max_fits)
    # Validate every seed before provider work. Geometry here is not a rejection
    # test because the original inventories need not share a fitted frame.
    for pairs in correspondences:
        checked = evaluate_feature_correspondence(
            reference_inventory, feature_inventory, pairs
        )
        if not checked["all_kinds_compatible"]:
            raise ArgumentError(
                argument="correspondences", reason="incompatible seed feature types"
            )
    query = from_feature_inventory(reference_inventory, radius=distance_tolerance)
    accepted, rejected, seeds, n_fits = [], [], [], 0

    for proposal_index, seed in enumerate(correspondences):
        blocked = set()
        pairs = seed.copy()
        steps, best, best_key, current, current_step = [], None, None, None, None
        termination = "no_remaining_pairs"

        while True:
            _limit("rigid_refinement", "attempted fits", n_fits + 1, max_fits)
            fitted = _fit_feature_mapping(
                molecular_system,
                query,
                pairs,
                feature_inventory,
                features,
                source_options,
            )
            n_fits += 1
            credit_criterion(
                "g3ps_refinement_" + orientation_policy,
                __name__ + ".refine_rigid_feature_correspondences",
            )
            check = evaluate_feature_correspondence(
                reference_inventory,
                fitted["inventory"],
                pairs,
                distance_tolerance=distance_tolerance,
                direction_tolerance=direction_tolerance,
            )
            matches = get_aligned_feature_matches(
                reference_inventory,
                fitted["inventory"],
                distance_tolerance=distance_tolerance,
                direction_tolerance=direction_tolerance,
                max_matrix_entries=max_matrix_entries,
            )
            growth_accepted = check["all_positions_valid"] and (
                orientation_policy == "final" or check["all_orientations_valid"]
            )
            matched_check = evaluate_feature_correspondence(
                reference_inventory,
                fitted["inventory"],
                matches["matches"],
                distance_tolerance=distance_tolerance,
                direction_tolerance=direction_tolerance,
            )
            step_index = len(steps)
            step = dict(
                step_index=step_index,
                fit_index=n_fits - 1,
                correspondence=pairs.tolist(),
                attempted_pair=None if current is None else pairs[-1].tolist(),
                growth_accepted=growth_accepted,
                pair_evaluation=check,
                matches=matches,
                matched_pair_evaluation=matched_check,
                previous_accepted_step=current_step,
                alignment=fitted["alignment"],
            )
            steps.append(step)
            if growth_accepted:
                current, current_step = fitted, step_index
                match_count = len(matches["matches"])
                rmsd = (
                    float(
                        puw.get_value(
                            puw.QuantityRecord.from_dict(
                                matched_check["position_rmsd"]
                            ).to_quantity(),
                            to_unit="nm",
                        )
                    )
                    if match_count
                    else 0.0
                )
                key = (-match_count, rmsd, step_index)
                if match_count >= min_matches and (best_key is None or key < best_key):
                    best_key = key
                    best = dict(
                        proposal_index=proposal_index,
                        selected_step_index=step_index,
                        correspondence=pairs.tolist(),
                        **fitted,
                        matches=matches,
                        pair_evaluation=check,
                        invalid_anchor_pairs=check["invalid_pairs"],
                    )
                accepted_pairs = pairs.copy()
            elif current is None:
                termination = "initial_seed_failed_growth_constraints"
                break
            else:
                blocked.add(tuple(pairs[-1]))
            # Distances/order always refer to the last accepted placement,
            # including after a rejected trial; no rejected coordinates leak.
            current_records = _records(current["inventory"])
            used_rows, used_columns = (
                set(accepted_pairs[:, 0]),
                set(accepted_pairs[:, 1]),
            )
            candidates = [
                (float(np.linalg.norm(reference["center"] - candidate["center"])), i, j)
                for i, reference in enumerate(first)
                for j, candidate in enumerate(current_records)
                if i not in used_rows
                and j not in used_columns
                and (i, j) not in blocked
                and reference["kind"] == candidate["kind"]
            ]
            if not candidates:
                break
            _, row, column = min(candidates)
            pairs = np.vstack((accepted_pairs, [row, column]))
        seeds.append(
            dict(
                proposal_index=proposal_index,
                initial_correspondence=seed.tolist(),
                steps=steps,
                n_fits=len(steps),
                n_accepted_steps=sum(s["growth_accepted"] for s in steps),
                n_rejected_steps=sum(not s["growth_accepted"] for s in steps),
                termination=termination,
                final_accepted_step_index=current_step,
                selected_step_index=None
                if best is None
                else best["selected_step_index"],
                permanently_rejected_pairs=[list(pair) for pair in sorted(blocked)],
                complete=True,
            )
        )
        if best is not None:
            accepted.append(best)
        else:
            observed = max(steps, key=lambda s: len(s["matches"]["matches"]))
            rejected.append(
                dict(
                    proposal_index=proposal_index,
                    matches=observed["matches"],
                    alignment=observed["alignment"],
                    reason="no_accepted_state_meets_final_match_count",
                )
            )
    report = detached(
        dict(
            method="greedy_rigid_feature_refinement@1",
            reference_inventory=reference_inventory,
            source_inventory=feature_inventory,
            n_fits=n_fits,
            n_seeds=len(correspondences),
            accepted_placements=[
                {k: v for k, v in option.items() if k != "molecular_system"}
                for option in accepted
            ],
            rejected_placements=rejected,
            refinement_seeds=seeds,
            complete=True,
            criteria=dict(
                orientation_policy=orientation_policy,
                min_matches=min_matches,
                features=features,
                distance_tolerance=distance_tolerance,
                direction_tolerance=direction_tolerance,
                max_fits=max_fits,
                max_matrix_entries=max_matrix_entries,
                candidate_order="nearest_center_pair_then_original_indices",
                rejected_pair_policy="permanently_blocked_within_seed",
                selection="best_accepted_state_by_final_match_count_then_matched_center_rmsd_then_first_fit",
                fitting_provider="molsysmt",
                translation_rescue=False,
                completion_scope="supplied_seeds_and_declared_greedy_growth_only",
            ),
        )
    )
    return dict(
        method=report["method"], placements=accepted, report=report, complete=True
    )
