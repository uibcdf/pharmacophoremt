"""Fit a ligand to pharmacophoric correspondences using MolSysMT geometry."""

import molsysmt as msm
import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed, credit_criterion
from pharmacophoremt._private.molsysmt import capability, detached, source_frame
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler.features import get_features
from pharmacophoremt.screening.correspondence import _centers_of_sites
from pharmacophoremt.screening.pose_evaluation import PoseEvaluator


@signal(tags=["screening", "alignment"])
@arg_digest()
@attributed("numpy", "molsysmt", "pyunitwizard")
def align_to_pharmacophore(
    molecular_system,
    pharmacophore,
    correspondence,
    *,
    selection="all",
    structure_index=0,
    chemical_state="reference",
    feature_inventory=None,
):
    """Rigidly fit selected atoms to matched pharmacophoric feature centers.

    Parameters
    ----------
    molecular_system : molecular system
        Unchanged prepared source accepted by MolSysMT.
    pharmacophore : Pharmacophore
        Query supplying target centers.
    correspondence : sequence of pairs of int
        (Site index, feature index) pairs, at least three, without repeats.
    selection : MolSysMT selection, default='all'
        Atoms to move; other atoms and other frames are left intact in a copy.
    structure_index : int, default=0
        Local source frame to fit.
    chemical_state : str or int, default='reference'
        State used for feature recognition.
    feature_inventory : dict, optional
        Reuse modeler.get_features output from this same source, selection, state
        and unchanged frame. Axis checks cannot authenticate origin or geometry.

    Returns
    -------
    dict
        Fitted molecular_system and detached alignment evidence, including source
        atom indices, paired centers, RMSD and fitted coordinates with units.

    Notes
    -----
    MolSysMT performs the least-RMSD fit on a native Structures point cloud of
    selected atom positions plus feature-center anchors. Its copy/get/set tools
    apply the fitted coordinates to a copy of the original system. No artificial
    topology or local molecular Kabsch implementation is constructed. Molecular
    chemistry, box and other frame data are not altered. Non-periodic prepared
    coordinates and non-collinear anchors are required. The selected CPU/double
    provider route is recorded; no particular internal MolSysMT kernel is claimed.

    Examples
    --------
    >>> aligned = align_to_pharmacophore(source, query, proposals['correspondences'][0], feature_inventory=inventory)
    >>> placed = aligned['molecular_system']
    """
    from molsysmt.native import Structures

    evaluator = PoseEvaluator(pharmacophore)
    coordinates, indices = source_frame(
        molecular_system, selection, structure_index, chemical_state=chemical_state
    )
    requested = sorted({kind for _, site in evaluator.query for kind in site.features})
    if feature_inventory is None:
        feature_inventory = get_features(
            molecular_system,
            selection=indices,
            structure_index=structure_index,
            chemical_state=chemical_state,
            features=requested,
        )
    if (
        feature_inventory["structure_index"] != structure_index
        or feature_inventory["chemical_state"] != detached(chemical_state)
        or not np.array_equal(feature_inventory["selected_atom_indices"], indices)
    ):
        raise ArgumentError(
            argument="feature_inventory",
            reason="selection, frame or chemical-state contract differs",
        )
    pairs = np.asarray(correspondence, dtype=np.int64)
    if len(set(pairs[:, 0])) != len(pairs) or len(set(pairs[:, 1])) != len(pairs):
        raise ArgumentError(
            argument="correspondence",
            reason="site and feature indices must each be unique",
        )
    records = feature_inventory["features"]
    if np.any(pairs[:, 0] >= len(evaluator.sites)) or np.any(
        pairs[:, 1] >= len(records)
    ):
        raise ArgumentError(
            argument="correspondence", reason="site or feature index is out of range"
        )
    sites = [evaluator.sites[index] for index in pairs[:, 0]]
    participants = [records[index] for index in pairs[:, 1]]
    if any(
        record["kind"] not in site.features or "excluded volume" in site.features
        for site, record in zip(sites, participants)
    ):
        raise ArgumentError(
            argument="correspondence",
            reason="chemically incompatible feature/site pair",
        )
    fit_centers = np.asarray(
        [puw.get_value(record["center"], to_unit="nm") for record in participants],
        dtype=float,
    )
    reference_centers = _centers_of_sites(sites)
    point_cloud = Structures(
        coordinates=puw.quantity(
            [np.concatenate((coordinates[indices], fit_centers))], "nm"
        )
    )
    target = Structures(coordinates=puw.quantity([reference_centers], "nm"))
    anchor_indices = np.arange(len(indices), len(indices) + len(pairs)).tolist()
    fitted_cloud = capability("structure.least_rmsd_fit")(
        point_cloud,
        selection="all",
        selection_fit=anchor_indices,
        reference_molecular_system=target,
        reference_selection_fit=list(range(len(pairs))),
        in_place=False,
        use_gpu=False,
        precision="double",
    )
    credit_criterion("kabsch", __name__ + ".align_to_pharmacophore.least_rmsd_fit")
    fitted_coordinates = capability("get")(
        fitted_cloud, selection=list(range(len(indices))), coordinates=True
    )
    output = capability("copy")(molecular_system)
    capability("set")(
        output,
        selection=indices,
        structure_indices=[structure_index],
        coordinates=fitted_coordinates,
    )
    rmsd = capability("structure.get_rmsd")(
        fitted_cloud,
        selection=anchor_indices,
        reference_molecular_system=target,
        reference_selection=list(range(len(pairs))),
    )
    return dict(
        molecular_system=output,
        alignment=detached(
            dict(
                method="feature_center_least_rmsd@1",
                provider="molsysmt.structure.least_rmsd_fit",
                provider_options=dict(
                    use_gpu=False, precision="double", engine="MolSysMT"
                ),
                software={"molsysmt": msm.__version__},
                structure_index=structure_index,
                selected_atom_indices=indices,
                correspondence=pairs,
                participants=[
                    dict(kind=record["kind"], atom_indices=record["atom_indices"])
                    for record in participants
                ],
                source_centers=puw.quantity(fit_centers, "nm"),
                target_centers=puw.quantity(reference_centers, "nm"),
                rmsd=rmsd,
                aligned_atom_coordinates=fitted_coordinates,
            )
        ),
    )
