"""Reference-anchored consensus on native feature inventories in a common frame."""

import numpy as np
from argdigest import arg_digest
from scipy.optimize import linear_sum_assignment
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed, credit_criterion, credit_software
from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_direction,
    digest_feature_inventory,
)
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ConsensusLimitError,
)
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Disk, Sphere, SphereAndVector
from pharmacophoremt.pharmacophore import Pharmacophore

from .features import CLASSICAL_FEATURES, DEFINITION, get_features

METHOD = "aligned_reference_consensus@1"
_COS_SLACK = 8 * np.finfo(float).eps


def _records(inventory):
    if inventory is None:
        raise ArgumentError(
            argument="feature_inventory", reason="provide a native inventory"
        )
    digest_feature_inventory(inventory)
    records = []
    for original in inventory["features"]:
        kind = original["kind"]
        if kind not in CLASSICAL_FEATURES:
            raise ArgumentError(
                argument="features",
                reason="consensus requires classical chemical features",
            )
        record = dict(
            original, center=np.asarray(puw.get_value(original["center"], to_unit="nm"))
        )
        for key, required in (
            ("direction", kind == "hb donor"),
            ("normal", kind == "aromatic ring"),
        ):
            value = original.get(key)
            if required != (value is not None):
                raise ArgumentError(
                    argument="feature_inventory",
                    reason=f"{kind} has invalid {key} geometry",
                )
            record[key] = None if value is None else digest_direction(value)
        records.append(record)
    return records


def _orientation_cosine(first, second):
    key = "direction" if first["kind"] == "hb donor" else "normal"
    if first[key] is None:
        return 1.0
    cosine = float(np.clip(np.dot(first[key], second[key]), -1, 1))
    return abs(cosine) if key == "normal" else cosine


@signal(tags=["modeling", "consensus", "correspondence"])
@arg_digest()
@attributed("numpy", "pyunitwizard")
def get_aligned_feature_matches(
    reference_inventory,
    feature_inventory,
    *,
    distance_tolerance="0.15 nm",
    direction_tolerance="30 degrees",
    max_matrix_entries=1000000,
):
    """Match two native inventories already expressed in a common frame.

    Parameters
    ----------
    reference_inventory, feature_inventory : dict
        Outputs of get_features; feature indices retain their original ordering.
    distance_tolerance : length quantity
        Maximum distance between matched feature centers, inclusive.
    direction_tolerance : angle quantity
        Maximum directed donor-vector or unoriented aromatic-axis angle.
    max_matrix_entries : int
        Bound on assignment matrix entries, including unmatched dummy columns.

    Returns
    -------
    dict
        Injective matches [reference feature index, candidate feature index],
        unmatched indices, matrix size and complete=True. Maximize cardinality,
        then minimize total center distance. Matrix-budget exhaustion raises
        PHMT-E106 before allocation; it is not an empty scientific match.

    Notes
    -----
    Equal optima retain the solver's deterministic input-order choice. This tool
    performs no alignment, preparation, molecular access or exhaustive search.

    Examples
    --------
    >>> matches = get_aligned_feature_matches(get_features(reference), get_features(ligand))
    """
    first, second = _records(reference_inventory), _records(feature_inventory)
    n_first, n_second = len(first), len(second)
    entries = n_first * (n_second + n_first) if n_first and n_second else 0
    if entries > max_matrix_entries:
        raise ConsensusLimitError(
            matrix_entries=entries, max_matrix_entries=max_matrix_entries
        )
    matches = []
    if entries:
        tolerance = float(puw.get_value(distance_tolerance, to_unit="nm"))
        threshold = np.cos(float(puw.get_value(direction_tolerance, to_unit="radians")))
        cost = np.ones((n_first, n_second + n_first))
        cost[:, n_second:] = 0
        for row, reference in enumerate(first):
            for column, candidate in enumerate(second):
                if reference["kind"] != candidate["kind"]:
                    continue
                distance = np.linalg.norm(reference["center"] - candidate["center"])
                if (
                    distance <= tolerance
                    and _orientation_cosine(reference, candidate) + _COS_SLACK
                    >= threshold
                ):
                    cost[row, column] = -(n_first + 1) + distance / tolerance
        rows, columns = linear_sum_assignment(cost)
        target = __name__ + ".get_aligned_feature_matches.assignment"
        credit_software("scipy", target)
        credit_criterion("assignment", target)
        matches = [
            [int(row), int(column)]
            for row, column in zip(rows, columns)
            if column < n_second and cost[row, column] < 0
        ]
    return dict(
        method="typed_maximum_cardinality_minimum_distance@1",
        definition=DEFINITION,
        matches=matches,
        complete=True,
        n_matrix_entries=entries,
        unmatched_reference=[
            i for i in range(n_first) if i not in {pair[0] for pair in matches}
        ],
        unmatched_candidate=[
            i for i in range(n_second) if i not in {pair[1] for pair in matches}
        ],
        criteria=detached(
            dict(
                distance_tolerance=distance_tolerance,
                direction_tolerance=direction_tolerance,
            )
        ),
    )


@signal(tags=["modeling", "consensus", "aggregation"])
@arg_digest()
@attributed("numpy", "pyunitwizard")
def get_consensus_sites(
    feature_inventories,
    correspondence_groups,
    *,
    ligand_ids,
    min_support=2,
    distance_tolerance="0.15 nm",
    direction_tolerance="30 degrees",
):
    """Aggregate explicit pharmacophoric correspondences into supported sites.

    Parameters
    ----------
    feature_inventories : sequence of dict
        One native inventory per distinct ligand in a common coordinate frame.
    correspondence_groups : sequence
        Each site group lists [inventory index, feature index] pairs. Each group
        contains at most one feature per ligand, with one common chemical kind;
        an occurrence cannot belong to multiple groups within this hypothesis.
    ligand_ids : sequence of str
        Unique declared source identities, including ligands with no features.
    min_support : int
        Minimum distinct-ligand count per site, between 1 and the input count.
    distance_tolerance : length quantity
        Maximum member distance from the unweighted feature-center mean.
    direction_tolerance : angle quantity
        Maximum orientation deviation from the first member's donor vector or
        aromatic axis. Reference orientation is retained; no angular mean occurs.

    Returns
    -------
    dict
        Unit-bearing site records, explicit members/support/dispersion, rejected
        groups with reasons, and complete=True, including evaluated-empty results.

    Notes
    -----
    This aggregates pharmacophoric geometry, not molecular coordinates. It never
    reads/modifies a molecular system. Ligand identities are caller declarations;
    this method does not infer chemical equivalence or collapse dataset duplicates.

    Examples
    --------
    >>> sites = get_consensus_sites([get_features(a), get_features(b)], [[[0, 0], [1, 0]]], ligand_ids=['a', 'b'])
    """
    if len(feature_inventories) != len(ligand_ids) or min_support > len(ligand_ids):
        raise ArgumentError(
            argument="ligand_ids/min_support",
            reason="one identity per inventory and attainable support are required",
        )
    inventories = [_records(inventory) for inventory in feature_inventories]
    tolerance = float(puw.get_value(distance_tolerance, to_unit="nm"))
    threshold = np.cos(float(puw.get_value(direction_tolerance, to_unit="radians")))
    seen, sites, rejected = set(), [], []
    for group_index, group in enumerate(correspondence_groups):
        if len({pair[0] for pair in group}) != len(group):
            raise ArgumentError(
                argument="correspondence_groups",
                reason="a ligand may contribute once per group",
            )
        members, records = [], []
        for source_index, feature_index in group:
            pair = (source_index, feature_index)
            if (
                pair in seen
                or source_index >= len(inventories)
                or feature_index >= len(inventories[source_index])
            ):
                raise ArgumentError(
                    argument="correspondence_groups",
                    reason="out-of-range or reused feature occurrence",
                )
            seen.add(pair)
            record = inventories[source_index][feature_index]
            records.append(record)
            members.append(
                dict(
                    ligand_id=ligand_ids[source_index],
                    inventory_index=source_index,
                    feature_index=feature_index,
                    atom_indices=list(record["atom_indices"]),
                    structure_index=feature_inventories[source_index][
                        "structure_index"
                    ],
                    chemical_state=feature_inventories[source_index]["chemical_state"],
                    geometry=detached(
                        {
                            key: feature_inventories[source_index]["features"][
                                feature_index
                            ].get(key)
                            for key in (
                                "center",
                                "direction",
                                "normal",
                                "geometry_atom_indices",
                                "charge",
                            )
                        }
                    ),
                )
            )
        if len({record["kind"] for record in records}) != 1:
            raise ArgumentError(
                argument="correspondence_groups",
                reason="site members must have one common feature kind",
            )
        center = np.mean([record["center"] for record in records], axis=0)
        residuals = np.linalg.norm(
            np.asarray([record["center"] for record in records]) - center, axis=1
        )
        cosines = np.asarray(
            [_orientation_cosine(records[0], record) for record in records]
        )
        reasons = []
        if len(records) < min_support:
            reasons.append("insufficient_ligand_support")
        if np.max(residuals) > tolerance:
            reasons.append("position_dispersion")
        if np.any(cosines + _COS_SLACK < threshold):
            reasons.append("orientation_dispersion")
        evidence = dict(
            group_index=group_index,
            members=members,
            support_count=len(records),
            support_fraction=len(records) / len(ligand_ids),
            position_rmsd=puw.quantity(float(np.sqrt(np.mean(residuals**2))), "nm"),
            maximum_center_deviation=puw.quantity(float(np.max(residuals)), "nm"),
            maximum_orientation_deviation=puw.quantity(
                float(np.degrees(np.arccos(np.clip(np.min(cosines), -1, 1)))), "degrees"
            ),
        )
        if reasons:
            rejected.append(dict(evidence, reasons=reasons))
            continue
        sites.append(
            dict(
                evidence,
                kind=records[0]["kind"],
                center=puw.quantity(center, "nm"),
                direction=None
                if records[0]["direction"] is None
                else puw.quantity(records[0]["direction"], "dimensionless"),
                normal=None
                if records[0]["normal"] is None
                else puw.quantity(records[0]["normal"], "dimensionless"),
                orientation_reference=members[0]
                if records[0]["kind"] in {"hb donor", "aromatic ring"}
                else None,
            )
        )
    return dict(
        method=METHOD,
        definition=DEFINITION,
        sites=sites,
        rejected_groups=rejected,
        ligand_ids=list(ligand_ids),
        n_ligands=len(ligand_ids),
        complete=True,
        criteria=detached(
            dict(
                min_support=min_support,
                distance_tolerance=distance_tolerance,
                direction_tolerance=direction_tolerance,
                center_aggregation="unweighted_feature_mean",
                orientation_aggregation="first_member_reference",
            )
        ),
    )


@signal(tags=["modeling", "consensus", "aligned_ligands"])
@arg_digest()
@attributed("molsysmt", "pyunitwizard")
def from_aligned_ligands(
    ligands,
    *,
    reference_index=0,
    features=CLASSICAL_FEATURES,
    min_support=2,
    distance_tolerance="0.15 nm",
    direction_tolerance="30 degrees",
    radius="0.15 nm",
    max_matrix_entries=1000000,
    name=None,
):
    """Build reference-anchored consensus from prepared ligands in one frame.

    Parameters
    ----------
    ligands : sequence of dict
        At least two sources with unique 'ligand_id' and 'molecular_system'. Each
        may declare selection, structure_index and chemical_state; defaults are
        'all', 0 and 'reference'. Each identity contributes one prepared frame.
    reference_index : int
        Source whose features anchor the hypothesis. Features absent from that
        source are outside this method's discovery scope.
    features : sequence of str
        Classical families obtained through get_features/MolSysMT.
    min_support : int
        Minimum distinct input ligand count, including empty inventories.
    distance_tolerance, direction_tolerance : quantities
        Matching and final center/reference-orientation acceptance tolerances.
    radius : length quantity
        Emitted site radius, independent of correspondence/dispersion tolerance.
    max_matrix_entries : int
        Assignment matrix bound per reference/candidate comparison.
    name : str, optional
        Output model name.

    Returns
    -------
    Pharmacophore
        Essential, equally weighted editable sites with native portable source,
        correspondence, support and dispersion metadata. Empty consensus raises.

    Notes
    -----
    No preparation, alignment, conformer generation or all-pattern enumeration.
    Support records feature correspondence, not affinity or guaranteed acceptance
    under independently curated emitted radii. Geometry rejection is retained;
    maximum-cardinality pairwise matches are not globally optimized afterward.

    Examples
    --------
    >>> query = from_aligned_ligands([{'ligand_id':'a', 'molecular_system':a}, {'ligand_id':'b', 'molecular_system':b}])
    """
    if reference_index >= len(ligands) or min_support > len(ligands):
        raise ArgumentError(
            argument="reference_index/min_support",
            reason="reference and support must lie within the source set",
        )
    if not set(features) <= set(CLASSICAL_FEATURES):
        raise ArgumentError(
            argument="features", reason="consensus supports classical chemical features"
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
    groups = [
        [[reference_index, feature]]
        for feature in range(len(inventories[reference_index]["features"]))
    ]
    comparisons = []
    for index, inventory in enumerate(inventories):
        if index == reference_index:
            continue
        matches = get_aligned_feature_matches(
            inventories[reference_index],
            inventory,
            distance_tolerance=distance_tolerance,
            direction_tolerance=direction_tolerance,
            max_matrix_entries=max_matrix_entries,
        )
        comparisons.append(dict(inventory_index=index, **matches))
        for reference_feature, candidate_feature in matches["matches"]:
            groups[reference_feature].append([index, candidate_feature])
    consensus = get_consensus_sites(
        inventories,
        groups,
        ligand_ids=[ligand["ligand_id"] for ligand in ligands],
        min_support=min_support,
        distance_tolerance=distance_tolerance,
        direction_tolerance=direction_tolerance,
    )
    if not consensus["sites"]:
        raise ArgumentError(
            argument="ligands",
            reason="no supported geometrically consistent consensus sites",
        )
    model = Pharmacophore(
        name=name,
        ref_mol=reference_index,
        ref_struct=inventories[reference_index]["structure_index"],
    )
    model.metadata = detached(
        dict(
            consensus=consensus,
            comparisons=comparisons,
            method=METHOD,
            sources=[
                dict(ligand_id=ligand["ligand_id"], **inventory)
                for ligand, inventory in zip(ligands, inventories)
            ],
            emitted_radius=radius,
            reference_index=reference_index,
        )
    )
    for record in consensus["sites"]:
        model.add_interaction_site(_site_from_consensus(record, radius))
    return model


def _site_from_consensus(record, radius):
    """Construct a classical Feature + Shape site from validated aggregation."""
    if record["direction"] is not None:
        shape = SphereAndVector(
            record["center"], radius, puw.get_value(record["direction"])
        )
    elif record["normal"] is not None:
        shape = Disk(record["center"], puw.get_value(record["normal"]), radius)
    else:
        shape = Sphere(record["center"], radius)
    return InteractionSite(
        shape,
        record["kind"],
        metadata=detached(
            {
                key: value
                for key, value in record.items()
                if key not in {"center", "direction", "normal"}
            }
        ),
    )
