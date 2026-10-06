"""Read-only scientific and workload summaries of rigid consensus reports."""

from copy import deepcopy

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._private.smonitor.exceptions import ArgumentError


@signal(tags=["validation", "consensus", "summary"])
@arg_digest()
def summarize_rigid_consensus(consensus_report):
    """Summarize a completed rigid consensus report without another calculation.

    Parameters
    ----------
    consensus_report : dict
        Detached result['report'] from modeler.from_rigid_ligands, including one
        pivot and all input sources, placements and layouts. Saved JSON works.

    Returns
    -------
    dict
        Per-source proposal/fit/matching counts, input ligand count, total layouts,
        hypotheses, maximum jointly supported site count and detached hypothesis
        geometry/membership. Empty discovery has zero models; incomplete reports
        are rejected, never summarized as scientific negatives.

    Notes
    -----
    This tool reads retained evidence and performs no molecular access, alignment,
    recognition or attribution tracking. Counts of proposal placements and models
    include duplicates. No geometric equivalence or affinity score is inferred.
    maximum observed matching can include rejected seed fits; accepted matching
    is reported separately. Occurrence indices refer to the declared source order.

    Examples
    --------
    >>> summary = summarize_rigid_consensus(result['report'])
    >>> n_models = summary['n_models']
    """
    try:
        return _summarize(consensus_report)
    except ArgumentError:
        raise
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise ArgumentError(
            argument="consensus_report", reason="malformed report evidence"
        ) from error


def _summarize(report):
    sources, alignments, layouts = (
        report[key] for key in ("sources", "source_alignments", "layouts")
    )
    identities = [source["ligand_id"] for source in sources]
    if (
        len(identities) != len(set(identities))
        or [entry["ligand_id"] for entry in alignments] != identities
    ):
        raise ArgumentError(
            argument="consensus_report",
            reason="source identities and placement order disagree",
        )
    pivot_index = report["criteria"]["reference_index"]
    if not 0 <= pivot_index < len(sources):
        raise ArgumentError(
            argument="consensus_report", reason="invalid declared pivot index"
        )
    n_reference = len(sources[pivot_index]["features"])
    per_source, observed_fits = [], 0
    for index, (source, alignment) in enumerate(zip(sources, alignments)):
        accepted, rejected = (
            alignment["accepted_placements"],
            alignment["rejected_placements"],
        )
        is_pivot = index == pivot_index
        proposals = alignment["proposals"]
        refinement = alignment.get("refinement")
        fits = 0 if is_pivot else len(accepted) + len(rejected)
        observed_options = accepted + rejected
        if refinement is not None:
            if (
                is_pivot
                or refinement.get("complete") is not True
                or refinement.get("method") != "greedy_rigid_feature_refinement@1"
            ):
                raise ArgumentError(
                    argument="consensus_report",
                    reason="invalid refinement completion or method",
                )
            seeds = refinement["refinement_seeds"]
            outcome_indices = [option["proposal_index"] for option in observed_options]
            if (
                len(seeds) != len(proposals["correspondences"])
                or len(seeds) != refinement["n_seeds"]
                or sorted(outcome_indices) != list(range(len(seeds)))
                or [seed["proposal_index"] for seed in seeds] != list(range(len(seeds)))
                or any(
                    seed.get("complete") is not True
                    or seed["n_fits"] != len(seed["steps"])
                    or seed["n_accepted_steps"]
                    != sum(step["growth_accepted"] for step in seed["steps"])
                    or seed["n_rejected_steps"]
                    != sum(not step["growth_accepted"] for step in seed["steps"])
                    or [step["step_index"] for step in seed["steps"]]
                    != list(range(len(seed["steps"])))
                    for seed in seeds
                )
            ):
                raise ArgumentError(
                    argument="consensus_report",
                    reason="refinement seed evidence contradicts outcomes",
                )
            fits = sum(len(seed["steps"]) for seed in seeds)
            if fits != refinement["n_fits"]:
                raise ArgumentError(
                    argument="consensus_report",
                    reason="refinement fit counts contradict steps",
                )
            observed_options = [step for seed in seeds for step in seed["steps"]]
            if [step["fit_index"] for step in observed_options] != list(range(fits)):
                raise ArgumentError(
                    argument="consensus_report",
                    reason="refinement trial identity contradicts fit count",
                )
            for option in accepted:
                seed = seeds[option["proposal_index"]]
                selected = option["selected_step_index"]
                if (
                    selected != seed["selected_step_index"]
                    or not 0 <= selected < len(seed["steps"])
                    or seed["steps"][selected]["growth_accepted"] is not True
                    or option["matches"] != seed["steps"][selected]["matches"]
                    or option["correspondence"]
                    != seed["steps"][selected]["correspondence"]
                ):
                    raise ArgumentError(
                        argument="consensus_report",
                        reason="selected placement contradicts accepted refinement state",
                    )
            if any(
                seeds[option["proposal_index"]]["selected_step_index"] is not None
                for option in rejected
            ):
                raise ArgumentError(
                    argument="consensus_report",
                    reason="rejected seed retains a selected valid state",
                )
        observed_fits += fits
        if is_pivot:
            valid = (
                alignment["status"] == "pivot"
                and proposals is None
                and len(accepted) == 1
                and not rejected
            )
        else:
            valid = (
                proposals is not None
                and proposals.get("complete") is True
                and len(proposals["correspondences"]) == len(accepted) + len(rejected)
                and alignment["status"] == ("placed" if accepted else "unplaced")
            )
        if not valid:
            raise ArgumentError(
                argument="consensus_report",
                reason="placement status/completion contradicts retained evidence",
            )
        best_accepted = (
            n_reference
            if is_pivot
            else max(
                (len(option["matches"]["matches"]) for option in accepted), default=0
            )
        )
        best_observed = (
            best_accepted
            if is_pivot
            else max(
                (len(option["matches"]["matches"]) for option in observed_options),
                default=0,
            )
        )
        per_source.append(
            dict(
                ligand_id=source["ligand_id"],
                status=alignment["status"],
                n_features=len(source["features"]),
                n_proposals=0
                if proposals is None
                else len(proposals["correspondences"]),
                proposal_counts={}
                if proposals is None
                else {
                    key: proposals[key]
                    for key in (
                        "n_trials",
                        "n_pruned",
                        "n_graph_nodes",
                        "n_graph_edges",
                        "n_maximal_cliques",
                        "n_ranked_seeds",
                        "n_omitted_seeds",
                    )
                    if key in proposals
                },
                proposal_selection_exhaustive=None
                if proposals is None
                else proposals.get("selection_exhaustive", True),
                n_fits=fits,
                **(
                    {}
                    if refinement is None
                    else dict(
                        refinement_method=refinement["method"],
                        orientation_policy=refinement["criteria"]["orientation_policy"],
                        n_accepted_refinement_steps=sum(
                            seed["n_accepted_steps"] for seed in seeds
                        ),
                        n_rejected_refinement_steps=sum(
                            seed["n_rejected_steps"] for seed in seeds
                        ),
                    )
                ),
                n_accepted_placements=len(accepted),
                n_rejected_placements=len(rejected),
                max_accepted_matches=best_accepted,
                max_observed_matches=best_observed,
                max_accepted_reference_fraction=best_accepted / n_reference
                if n_reference
                else None,
            )
        )
    if observed_fits != report["n_fits"] or len(layouts) != report["n_layouts"]:
        raise ArgumentError(
            argument="consensus_report",
            reason="declared fit/layout counts disagree with retained evidence",
        )
    hypotheses = []
    for layout in layouts:
        consensus = layout["consensus"]
        if consensus.get("complete") is not True:
            raise ArgumentError(
                argument="consensus_report",
                reason="cannot summarize incomplete layout discovery",
            )
        for hypothesis in consensus["hypotheses"]:
            sites = [
                consensus["candidate_sites"][index]
                for index in hypothesis["site_indices"]
            ]
            hypotheses.append(
                dict(
                    layout_id=layout["layout_id"],
                    hypothesis_id=hypothesis["hypothesis_id"],
                    n_sites=len(sites),
                    joint_ligand_ids=hypothesis["joint_ligand_ids"],
                    joint_support_count=hypothesis["joint_support_count"],
                    joint_support_fraction=hypothesis["joint_support_fraction"],
                    sites=[
                        {
                            key: site[key]
                            for key in (
                                "kind",
                                "center",
                                "direction",
                                "normal",
                                "members",
                            )
                        }
                        for site in sites
                    ],
                )
            )
    return deepcopy(
        dict(
            method=report["method"],
            complete=True,
            criteria=report["criteria"],
            n_ligands=len(sources),
            ligand_ids=identities,
            sources=per_source,
            n_fits=observed_fits,
            n_layouts=len(layouts),
            n_models=len(hypotheses),
            max_joint_sites=max(
                (hypothesis["n_sites"] for hypothesis in hypotheses), default=0
            ),
            hypotheses=hypotheses,
        )
    )
