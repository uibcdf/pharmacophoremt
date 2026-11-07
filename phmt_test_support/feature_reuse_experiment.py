"""Compare fresh/reused source inventories through existing public native tools.

This case harness is not a matcher, persistent cache, index or public runtime API.
It compares the same explicit proposal/placement subworkflow, not the complete
RigidPoseSearch stopping, score or witness contract. An unchanged prepared
source/selection/frame/state/chemistry is a caller precondition, not authenticated
by the coordinate/inventory immutability checks below.
"""

from copy import deepcopy

from pharmacophoremt._ackredit import attributed


def _declarations(references, features, max_placements):
    if not isinstance(references, (list, tuple)) or not references:
        raise ValueError("references must be a nonempty fixed list of query records")
    keys = []
    for reference in references:
        if not isinstance(reference, dict) or set(reference) != {"key", "inventory"}:
            raise ValueError("references require exactly key and inventory")
        key = reference["key"]
        if type(key) is not str or not key.strip() or key in keys:
            raise ValueError("reference keys must be nonempty and unique")
        keys.append(key)
    if (
        not isinstance(features, (list, tuple))
        or not features
        or any(type(value) is not str or not value.strip() for value in features)
        or len(set(features)) != len(features)
    ):
        raise ValueError("declare a nonempty sequence of unique feature families")
    if type(max_placements) is not int or max_placements < 1:
        raise ValueError("max_placements must be a positive integer")


@attributed()
def compare_feature_reuse(
    molecular_system,
    references,
    *,
    features,
    selection="all",
    structure_index=0,
    chemical_state=0,
    distance_tolerance="0.15 nm",
    direction_tolerance="30 degrees",
    correspondence_strategy="association_cliques",
    min_matches=3,
    max_graph_nodes=64,
    max_cliques=1000,
    max_trials=10000,
    max_matrix_entries=1000000,
    max_placements=1,
):
    """Compare native proposal, selected-placement and checked-pose evidence.

    Each reference is ``{'key': opaque_unique_key, 'inventory': get_features(...)}``.
    Both arms use the same explicitly declared feature families and settings.
    The reused arm requests source extraction once; the fresh arm requests it
    once per reference. Native fitting still reextracts and validates features.
    ``outer_extraction_requests`` therefore counts only harness-level requests,
    not total recognition/provider calls or any measured performance benefit.

    Each arm fits the first ``max_placements`` canonical native proposals. Native
    proposal-family completion and selected-prefix coverage remain separate.
    Full native reports and checked-pose evaluations must compare exactly after
    the existing quantity-preserving detachment. Failures propagate. Returned
    evidence contains no live molecule; query count and one molecule's workload
    are intentionally bounded by the declaring caller.
    """
    _declarations(references, features, max_placements)

    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt._private.molsysmt import detached
    from pharmacophoremt.modeler import from_feature_inventory, get_features
    from pharmacophoremt.screening import (
        PoseEvaluator,
        get_rigid_feature_correspondences,
        get_rigid_feature_placements,
        get_screening_score,
    )

    families = tuple(features)
    references = deepcopy(references)
    reference_before = detached(references)
    source_options = deepcopy(
        dict(
            selection=selection,
            structure_index=structure_index,
            chemical_state=chemical_state,
        )
    )
    proposal_options = dict(
        correspondence_strategy=correspondence_strategy,
        distance_tolerance=distance_tolerance,
        min_matches=min_matches,
        max_graph_nodes=max_graph_nodes,
        max_cliques=max_cliques,
        max_trials=max_trials,
        max_matrix_entries=max_matrix_entries,
    )
    placement_options = dict(
        **source_options,
        features=families,
        min_matches=min_matches,
        distance_tolerance=distance_tolerance,
        direction_tolerance=direction_tolerance,
        max_fits=max_placements,
        max_matrix_entries=max_matrix_entries,
    )

    def coordinates():
        values = np.asarray(
            puw.get_value(msm.get(molecular_system, coordinates=True), to_unit="nm")
        )
        if values.ndim != 3 or values.shape[-1] != 3 or not np.isfinite(values).all():
            raise ValueError("source requires finite coordinate frames")
        return values.copy()

    original_coordinates = coordinates()
    reused_inventory = get_features(
        molecular_system, features=families, **source_options
    )
    inventory_before = detached(reused_inventory)

    def run_arm(reference, inventory):
        proposals = get_rigid_feature_correspondences(
            reference["inventory"], inventory, **proposal_options
        )
        selected = proposals["correspondences"][:max_placements]
        placed = get_rigid_feature_placements(
            molecular_system,
            reference["inventory"],
            selected,
            feature_inventory=inventory,
            **placement_options,
        )
        query = from_feature_inventory(
            reference["inventory"], radius=distance_tolerance, name=reference["key"]
        )
        evaluator = PoseEvaluator(
            query,
            point_tolerance=distance_tolerance,
            direction_tolerance=direction_tolerance,
        )
        evaluations = []
        for index, placement in enumerate(placed["placements"]):
            native = evaluator.evaluate(
                placement["molecular_system"],
                pose_id=f"{reference['key']}:accepted:{index}",
                **source_options,
            )
            evaluations.append(
                dict(
                    native_result=native,
                    score_method="checked_pose_coverage@1",
                    ranking_score=get_screening_score(
                        native, score_method="checked_pose_coverage"
                    ),
                )
            )
        return detached(
            dict(
                proposals=proposals,
                placement_report=placed["report"],
                native_evaluations=evaluations,
            )
        )

    comparisons = []
    for reference in references:
        fresh_inventory = get_features(
            molecular_system, features=families, **source_options
        )
        if detached(fresh_inventory) != inventory_before:
            raise ValueError(
                "fresh source inventory differs from the reused observation"
            )
        fresh = run_arm(reference, fresh_inventory)
        reused = run_arm(reference, reused_inventory)
        if fresh != reused:
            raise ValueError("fresh and reused native subworkflow evidence differs")
        if detached(reused_inventory) != inventory_before:
            raise ValueError("native subworkflow changed the reused inventory")
        if detached(references) != reference_before:
            raise ValueError("native subworkflow changed a reference inventory")
        if not np.array_equal(coordinates(), original_coordinates):
            raise ValueError("native subworkflow changed source coordinates")
        proposed = len(fresh["proposals"]["correspondences"])
        selected_count = min(proposed, max_placements)
        comparisons.append(
            dict(
                key=reference["key"],
                native_evidence_equal=True,
                proposed_mappings=proposed,
                selected_mappings=selected_count,
                omitted_mappings=proposed - selected_count,
                placement_coverage="all_proposed_mappings"
                if proposed == selected_count
                else "selected_prefix_only",
                fresh=fresh,
                reused=reused,
            )
        )
    return detached(
        dict(
            schema="pharmacophoremt.feature-reuse-comparison@1",
            features=families,
            source_options=source_options,
            proposal_options=proposal_options,
            placement_options=placement_options,
            comparisons=comparisons,
            outer_extraction_requests=dict(
                reused=1,
                fresh=len(references),
                scope="harness source requests only; native post-fit extraction excluded",
            ),
            source_coordinates_unchanged=True,
            reused_inventory_unchanged=True,
            reference_inventories_unchanged=True,
            reused_inventory=inventory_before,
            source_identity_scope="unchanged prepared source is a caller precondition",
            completion_scope="native proposal family and selected mappings only",
            performance_claim=False,
            full_rigid_search_equivalence=False,
        )
    )
