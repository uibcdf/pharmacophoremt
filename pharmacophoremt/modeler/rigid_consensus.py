"""Alternative consensus models from prepared, rigid, unaligned ligand frames."""

from copy import deepcopy
from itertools import product
from math import prod

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.pharmacophore import Pharmacophore

from .aligned_cliques import _limit, get_aligned_consensus_hypotheses
from .aligned_consensus import (
    _records,
    _site_from_consensus,
)
from .features import CLASSICAL_FEATURES, get_features

METHOD = "pivot_rigid_clique_consensus@1"


def _inventory(ligand, features, molecular_system=None):
    return get_features(
        ligand["molecular_system"] if molecular_system is None else molecular_system,
        selection=ligand.get("selection", "all"),
        structure_index=ligand.get("structure_index", 0),
        chemical_state=ligand.get("chemical_state", "reference"),
        features=features,
    )


@signal(tags=["modeling", "consensus", "rigid"])
@arg_digest()
@attributed("numpy", "molsysmt", "pyunitwizard", model_results=True)
def from_rigid_ligands(
    ligands,
    *,
    reference_index=0,
    correspondence_strategy="association_cliques",
    n_seeds=None,
    refinement_strategy=None,
    orientation_policy="final",
    features=CLASSICAL_FEATURES,
    min_matches=3,
    min_support=2,
    min_sites=1,
    distance_tolerance="0.15 nm",
    direction_tolerance="30 degrees",
    radius="0.15 nm",
    max_graph_nodes=64,
    max_cliques=1000,
    max_trials=10000,
    max_fits=1000,
    max_layouts=1000,
    max_combinations=10000,
    max_matrix_entries=1000000,
    name=None,
):
    """Align prepared ligand frames to a pivot and retain consensus alternatives.

    Parameters
    ----------
    ligands : sequence of dict
        At least two unique ligand_id/molecular_system records, optionally with
        selection, structure_index and chemical_state. One prepared frame each.
    reference_index : int, default=0
        Explicit pivot; it must have three non-collinear classical centers.
    correspondence_strategy : str, default='association_cliques'
        Proposal family: 'association_cliques', 'triplet_seeds' or
        'ranked_triplet_seeds' (G3PS seed stage only).
    n_seeds : int or None
        Scientific guess limit for ranked_triplet_seeds. None retains all;
        finite values may miss valid placements. Other families reject it.
    refinement_strategy : {None, 'greedy'}, default=None
        None fits supplied proposals once. greedy grows each proposal through the
        public refinement tool and retains its best fully evaluated placement.
    orientation_policy : {'final', 'each_step'}, default='final'
        Angular growth policy when refinement is greedy. Both validate final
        matching completely. each_step without refinement raises.
    features : sequence of str
        Classical chemical families obtained with MolSysMT-supported extraction.
    min_matches : int, default=3
        Minimum final injective pivot-feature matches, at least three. A smaller
        seed may grow before meeting this requirement when refinement is selected.
    min_support, min_sites : int
        Common-ligand support and minimum sites in emitted consensus hypotheses.
    distance_tolerance, direction_tolerance : quantities
        Post-fit pivot displacement/orientation and aligned clique criteria.
    radius : length quantity
        Shape radius for emitted models, independent of discovery tolerance.
    max_graph_nodes, max_cliques : int
        Bounds per association graph and per aligned layout graph/enumeration.
    max_trials : int
        Triplet candidate-product bound per source ligand.
    max_fits, max_layouts : int
        Total attempted fits and Cartesian product of accepted placements.
    max_combinations : int
        Consensus candidate-extension bound per layout.
    max_matrix_entries : int
        Bound on the post-fit pivot assignment matrix, including dummy columns.
    name : str, optional
        Model name prefix.

    Returns
    -------
    dict
        Native models, detached sources/placements/layouts report, complete=True.
        Unplaced ligands retain their place in support denominators. Failed
        providers or exhausted resources raise; they are not scientific negatives.

    Notes
    -----
    All fitting and molecular transformation use MolSysMT through the existing
    align_to_pharmacophore tool. Every seed pair must satisfy absolute center and
    orientation criteria after fitting, and an injective full-inventory matching
    must meet min_matches. All accepted proposal placements are retained, even
    when different proposals give identical geometry. No optimum-coverage early
    stop is applied. Completion concerns the chosen pivot/proposal family and
    maximal aligned hypotheses, not all continuous or flexible alignments. A
    ligand lacking a direct pivot placement contributes no sites in any layout.
    Chemical preparation, conformer generation and global multiple alignment are
    separate operations. Original molecular systems are never changed.
    With greedy refinement, its declared growth policy replaces ordinary seed
    acceptance: final checks orientation in final matching, each_step also checks
    every fitted anchor during growth. Both retain their best fully evaluated
    accepted state. All initial/trial fits count against the global allowance.

    Examples
    --------
    >>> result = from_rigid_ligands([{'ligand_id':'a', 'molecular_system':a}, {'ligand_id':'b', 'molecular_system':b}])
    >>> alternatives = result['models']
    """
    from pharmacophoremt.screening.rigid_correspondence import (
        get_rigid_feature_correspondences,
    )
    from pharmacophoremt.screening.rigid_placements import get_rigid_feature_placements
    from pharmacophoremt.screening.rigid_refinement import (
        refine_rigid_feature_correspondences,
    )

    if (
        reference_index >= len(ligands)
        or min_support > len(ligands)
        or not set(features) <= set(CLASSICAL_FEATURES)
    ):
        raise ArgumentError(
            argument="reference_index/min_support/features",
            reason="require an existing pivot, attainable support and classical families",
        )
    if n_seeds is not None and correspondence_strategy != "ranked_triplet_seeds":
        raise ArgumentError(argument="n_seeds", reason="requires ranked_triplet_seeds")
    if refinement_strategy is None and orientation_policy != "final":
        raise ArgumentError(
            argument="orientation_policy", reason="each_step requires greedy refinement"
        )
    inventories = [_inventory(ligand, features) for ligand in ligands]
    pivot = inventories[reference_index]
    # Validate the pivot even if other sources have empty inventories.
    from pharmacophoremt.screening.correspondence import _noncollinear

    reference_records = _records(pivot)
    if len(reference_records) < 3 or not _noncollinear(
        np.array([r["center"] for r in reference_records])
    ):
        raise ArgumentError(
            argument="reference_index",
            reason="pivot requires three non-collinear feature centers",
        )
    placements, source_reports, n_fits = [], [], 0
    for index, (ligand, inventory) in enumerate(zip(ligands, inventories)):
        options, rejected = [], []
        proposals = None
        refinement = None
        if index == reference_index:
            options.append(
                dict(inventory=inventory, alignment=dict(method="pivot_identity@1"))
            )
        else:
            proposals = get_rigid_feature_correspondences(
                pivot,
                inventory,
                correspondence_strategy=correspondence_strategy,
                distance_tolerance=distance_tolerance,
                min_matches=min_matches,
                max_graph_nodes=max_graph_nodes,
                max_cliques=max_cliques,
                max_trials=max_trials,
                n_seeds=n_seeds,
                max_matrix_entries=max_matrix_entries,
            )
            mappings = proposals["correspondences"]
            _limit(
                "rigid_alignment", "scheduled fits", n_fits + len(mappings), max_fits
            )
            placement_tool = (
                get_rigid_feature_placements
                if refinement_strategy is None
                else refine_rigid_feature_correspondences
            )
            refinement_options = (
                {}
                if refinement_strategy is None
                else dict(orientation_policy=orientation_policy)
            )
            fitted = placement_tool(
                ligand["molecular_system"],
                pivot,
                mappings,
                selection=ligand.get("selection", "all"),
                structure_index=ligand.get("structure_index", 0),
                chemical_state=ligand.get("chemical_state", "reference"),
                features=features,
                feature_inventory=inventory,
                min_matches=min_matches,
                distance_tolerance=distance_tolerance,
                direction_tolerance=direction_tolerance,
                max_fits=max(1, max_fits - n_fits),
                max_matrix_entries=max_matrix_entries,
                **refinement_options,
            )
            n_fits += fitted["report"]["n_fits"]
            options = [
                {
                    key: value
                    for key, value in option.items()
                    if key != "molecular_system"
                }
                for option in fitted["placements"]
            ]
            rejected = fitted["report"]["rejected_placements"]
            if refinement_strategy is not None:
                refinement = {
                    key: value
                    for key, value in fitted["report"].items()
                    if key
                    not in {
                        "reference_inventory",
                        "source_inventory",
                        "accepted_placements",
                        "rejected_placements",
                    }
                }
        source_reports.append(
            dict(
                ligand_id=ligand["ligand_id"],
                status="pivot"
                if index == reference_index
                else ("placed" if options else "unplaced"),
                proposals=proposals,
                accepted_placements=options,
                rejected_placements=rejected,
            )
        )
        if refinement is not None:
            source_reports[-1]["refinement"] = refinement
        if not options:
            empty = deepcopy(inventory)
            empty["features"] = []
            options = [dict(inventory=empty, alignment=None)]
        placements.append(options)
    n_layouts = prod(len(options) for options in placements)
    _limit("alignment_layouts", "placement combinations", n_layouts, max_layouts)
    models, layouts = [], []
    ligand_ids = [ligand["ligand_id"] for ligand in ligands]
    sources = [
        dict(ligand_id=identity, **inventory)
        for identity, inventory in zip(ligand_ids, inventories)
    ]
    criteria = detached(
        dict(
            reference_index=reference_index,
            reference_ligand_id=ligand_ids[reference_index],
            correspondence_strategy=correspondence_strategy,
            n_seeds=n_seeds,
            refinement_strategy=refinement_strategy,
            orientation_policy=orientation_policy
            if refinement_strategy is not None
            else None,
            features=features,
            min_matches=min_matches,
            min_support=min_support,
            min_sites=min_sites,
            distance_tolerance=distance_tolerance,
            direction_tolerance=direction_tolerance,
            max_graph_nodes=max_graph_nodes,
            max_cliques=max_cliques,
            max_trials=max_trials,
            max_fits=max_fits,
            max_layouts=max_layouts,
            max_combinations=max_combinations,
            max_matrix_entries=max_matrix_entries,
            emitted_radius=radius,
            completion_scope="declared_pivot_proposals_and_maximal_aligned_hypotheses",
            duplicate_policy="retain_every_accepted_proposal_placement",
        )
    )
    for layout_index, option_indices in enumerate(
        product(*(range(len(options)) for options in placements))
    ):
        chosen = [options[index] for options, index in zip(placements, option_indices)]
        report = get_aligned_consensus_hypotheses(
            [option["inventory"] for option in chosen],
            ligand_ids=ligand_ids,
            min_support=min_support,
            min_sites=min_sites,
            distance_tolerance=distance_tolerance,
            direction_tolerance=direction_tolerance,
            max_graph_nodes=max_graph_nodes,
            max_cliques=max_cliques,
            max_combinations=max_combinations,
        )
        layout_id = f"layout_{layout_index:05d}"
        layout = dict(
            layout_id=layout_id,
            placement_indices=list(option_indices),
            unplaced_ligand_ids=[
                ligand_ids[i]
                for i, option in enumerate(chosen)
                if option["alignment"] is None
            ],
        )
        layouts.append(dict(layout, consensus=report))
        for hypothesis in report["hypotheses"]:
            model = Pharmacophore(
                name=f"{name or 'Rigid consensus'} {layout_id} {hypothesis['hypothesis_id']}"
            )
            sites = [report["candidate_sites"][i] for i in hypothesis["site_indices"]]
            model.metadata = detached(
                dict(
                    method=METHOD,
                    criteria=criteria,
                    layout=layout,
                    hypothesis=hypothesis,
                    sources=sources,
                    placements=[
                        dict(ligand_id=identity, **option)
                        for identity, option in zip(ligand_ids, chosen)
                    ],
                    consensus=dict(
                        method=report["method"],
                        sites=sites,
                        ligand_ids=ligand_ids,
                        n_ligands=len(ligands),
                        criteria=report["criteria"],
                        complete=True,
                    ),
                    emitted_radius=radius,
                )
            )
            for site in sites:
                model.add_interaction_site(_site_from_consensus(site, radius))
            models.append(model)
    return dict(
        method=METHOD,
        models=models,
        complete=True,
        report=detached(
            dict(
                method=METHOD,
                sources=sources,
                source_alignments=source_reports,
                layouts=layouts,
                n_fits=n_fits,
                n_layouts=n_layouts,
                criteria=criteria,
                complete=True,
            )
        ),
    )
