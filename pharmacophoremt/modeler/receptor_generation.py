"""Bounded complementary hypotheses from cached provider-derived geometry."""

from itertools import islice, product
from math import prod

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_acceptor_directions,
    digest_acceptor_distances,
    digest_acceptor_structure_position,
    digest_acceptor_target_orientation,
    digest_aromatic_distances,
    digest_direction,
    digest_donor_distances,
    digest_feature_inventory,
    digest_max_hypotheses,
    digest_radius,
    digest_receptor_profile,
)
from pharmacophoremt._private.arg_digestion.argument.skip_digestion import (
    digest_skip_digestion,
)
from pharmacophoremt._private.arg_digestion.receptor_generation import CONFIG
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError

from ._receptor_directions import cached_acceptor_choices
from .excluded_volumes import _attach_receptor_exclusions, _receptor_exclusions
from .receptor_projections import from_receptor_projections

METHOD = "cached_receptor_donor_aromatic_faces@1"
CARBONYL_METHOD = "cached_receptor_donor_aromatic_carbonyl@1"
CARBONYL_PROFILE = "donor_aromatic_carbonyl_experimental"
AROMATIC_N_METHOD = "cached_receptor_donor_aromatic_carbonyl_aromatic_n@1"
AROMATIC_N_PROFILE = "donor_aromatic_carbonyl_aromatic_n_experimental"


def _choices(
    inventory,
    donor_distances,
    aromatic_distances,
    *,
    acceptors=None,
    acceptor_distances=None,
    acceptor_label="carbonyl",
    method=METHOD,
):
    options, omitted = [], []
    for index, record in enumerate(inventory["features"]):
        kind = record["kind"]
        if kind == "hb acceptor" and acceptors is not None:
            if index in acceptors["omitted"]:
                omitted.append(acceptors["omitted"][index])
                continue
            choices = []
            for distance_index, distance in enumerate(acceptor_distances):
                for row in acceptors["admitted"][index]:
                    axis = puw.quantity(row["axis"], "dimensionless")
                    choice = dict(
                        feature_index=index,
                        distance_index=distance_index,
                        distance=puw.convert(distance, to_unit="nm"),
                        face_sign=None,
                        provider_record_index=row["provider_record_index"],
                        local_direction_index=row["local_direction_index"],
                    )
                    spec = dict(
                        feature_index=index,
                        projection_direction=axis,
                        target_direction=-axis,
                        distance=choice["distance"],
                        label=f"feature {index}, distance {distance_index}, {acceptor_label} direction {row['local_direction_index']}",
                        evidence=dict(
                            method=method,
                            choice=choice,
                            geometry_origin="cached provider-derived geometry",
                            placement_origin="explicit pharmacophoric hypothesis",
                            target_orientation="towards_receptor",
                            provider_geometry=row["evidence"],
                        ),
                    )
                    choices.append((choice, spec))
            options.append(choices)
            continue
        if kind not in {"hb donor", "aromatic ring"}:
            omitted.append(
                dict(
                    feature_index=index,
                    kind=kind,
                    atom_indices=record["atom_indices"],
                    reason="ideal_acceptor_profile_not_adopted"
                    if kind == "hb acceptor"
                    else "outside_receptor_profile",
                )
            )
            continue
        field = "direction" if kind == "hb donor" else "normal"
        try:
            axis = digest_direction(record.get(field))
        except ArgumentError as error:
            raise ArgumentError(
                argument="feature_inventory",
                reason=f"feature {index} has invalid cached {field} geometry",
            ) from error
        distances = donor_distances if kind == "hb donor" else aromatic_distances
        choices = []
        for distance_index, distance in enumerate(distances):
            for sign in [1] if kind == "hb donor" else [1, -1]:
                choice = dict(
                    feature_index=index,
                    distance_index=distance_index,
                    distance=puw.convert(distance, to_unit="nm"),
                    face_sign=sign if kind == "aromatic ring" else None,
                )
                spec = dict(
                    feature_index=index,
                    projection_direction=puw.quantity(sign * axis, "dimensionless"),
                    distance=choice["distance"],
                    label=f"feature {index}, distance {distance_index}, face {sign}",
                    evidence=dict(
                        method=method,
                        choice=choice,
                        geometry_origin="cached provider-derived geometry",
                        placement_origin="explicit pharmacophoric hypothesis",
                    ),
                )
                if kind == "aromatic ring":
                    spec["target_normal"] = puw.quantity(axis, "dimensionless")
                choices.append((choice, spec))
        options.append(choices)
    return options, omitted


@signal(tags=["modeling", "receptor_generation"])
@arg_digest(config=CONFIG)
@attributed("numpy", "pyunitwizard", model_results=True)
def from_receptor_features(
    feature_inventory,
    *,
    receptor_profile,
    donor_distances,
    aromatic_distances,
    radius,
    max_hypotheses,
    excluded_volume_inventory=None,
    excluded_volume_radius=None,
    acceptor_directions=None,
    acceptor_structure_position=None,
    acceptor_distances=None,
    acceptor_target_orientation=None,
    name=None,
    skip_digestion=False,
):
    """Generate separate complementary hypotheses from a cached receptor region.

    Parameters
    ----------
    feature_inventory : dict
        Native get_features result for one explicitly prepared region, structure
        and chemical state. Cached origin/frame claims remain caller declarations.
    receptor_profile : str
        Required scientific choice. Every indexed donor emits a spherical ligand
        acceptor along its cached D→H direction. Every aromatic ring emits a Disk
        on either face, with the cached ring axis explicitly used as target axis.
        'donor_aromatic_faces' admits these two families only.
        'donor_aromatic_carbonyl_experimental' adds native model2 carbonyls.
        'donor_aromatic_carbonyl_aromatic_n_experimental' explicitly adds model3
        aromatic-nitrogen acceptors alongside model2. Neither admits model4.
    donor_distances, aromatic_distances : list or tuple of length quantities
        Nonempty positive finite scalar choices with explicit units, in caller
        order. Both lists are required even if a family is absent. Repeated
        physically equivalent choices remain distinct declared alternatives.
    radius : length quantity
        Required positive positional matching tolerance, independent of offsets.
    max_hypotheses : int
        Required finite nonnegative bound. Zero can return incomplete empty output.
    excluded_volume_inventory : dict, optional
        Native included-volume inventory with the same declared atom set,
        structure and chemical-state selector as the chemical cache.
    excluded_volume_radius : length quantity, optional
        Explicit uniform query radius, required with the heavy-atom cache.
        Exclusions append after positive sites at weight zero; they are not
        physical radii, hypothesis pruning or a steric calculation here.
    acceptor_directions : dict, optional
        Required native MolSysMT hbond_site_directions@1 cache for the experimental
        acceptor profiles; ideal_local_geometry/smarts_donor_acceptor, pbc=False.
        Original recognition/source/state and native origins must match the
        feature cache. This does not authenticate molecular source coordinates.
    acceptor_structure_position : int, optional
        Required explicit position in the provider's ordered structure axis,
        including repetitions, referring to the cached feature frame.
    acceptor_distances : list or tuple of length quantities, optional
        Required nonempty positive choices for the experimental profile.
    acceptor_target_orientation : {'towards_receptor'}, optional
        Required explicit hypothesis rule: donor target axis -u for provider
        direction u. The two carbonyl lobes produce separate hypotheses.
        An admitted aromatic nitrogen contributes one native direction.
        These four options must be None with the original profile.
    name : str, optional
        Model-name prefix; deterministic enumeration indices are appended.
    skip_digestion : bool, default=False
        Internal generic-digestion control. Mandatory scientific checks still apply.

    Returns
    -------
    dict
        Models, a detached report and complete. The report retains exact total,
        visited/returned/remaining counts, source inventory, parameters, choices,
        omissions and deterministic order. No eligible records yields models=[]
        and status='no_supported_features', complete=True, not an empty usable query.

    Notes
    -----
    The Cartesian product contains one choice for EVERY admitted source feature,
    in inventory order; distance order precedes aromatic +/− face. The rightmost
    feature changes fastest. Opposite faces are separate hypotheses. Multiple
    donor-H pairs remain distinct even when they share a donor atom. Every positive
    site starts essential and weight one; these are construction assumptions.

    Unsupported records are explicitly omitted. Position-only acceptors get no
    invented directions. Missing/invalid admitted direction geometry raises before
    any model, including with budget zero. General molecular recognition, geometry,
    formats and preparation belong to MolSysMT. This tool performs no molecular
    access, pocket detection, steric test, fitting, ranking or biological inference.
    A finite prefix is incomplete enumeration, not a negative or optimized search.

    Uses existing from_receptor_projections; its explicit-projection facade and
    defaults are unchanged. Units/source/choice evidence and original cached
    attribution remain in independent model metadata and the report. Saved
    QuantityRecord metadata alone is not a hydrated native feature inventory.

    Examples
    --------
    >>> result = from_receptor_features(inventory,
    ...     receptor_profile='donor_aromatic_faces', donor_distances=['.28 nm'],
    ...     aromatic_distances=['.35 nm'], radius='20 pm', max_hypotheses=8)
    >>> models, complete = result['models'], result['complete']
    """
    # Scientific admission also applies when generic digestion is explicitly bypassed.
    digest_skip_digestion(skip_digestion)
    digest_receptor_profile(receptor_profile)
    donor_distances = digest_donor_distances(donor_distances)
    aromatic_distances = digest_aromatic_distances(aromatic_distances)
    radius = digest_radius(radius)
    budget = digest_max_hypotheses(max_hypotheses)
    if feature_inventory is None:
        raise ArgumentError(
            argument="feature_inventory", reason="provide a native cache"
        )
    digest_feature_inventory(feature_inventory)
    if any(r["kind"] == "included volume" for r in feature_inventory["features"]):
        raise ArgumentError(
            argument="feature_inventory",
            reason="provide chemical features; exclusions require a separate inventory",
        )
    acceptor_directions = digest_acceptor_directions(acceptor_directions)
    acceptor_structure_position = digest_acceptor_structure_position(
        acceptor_structure_position
    )
    acceptor_distances = digest_acceptor_distances(acceptor_distances)
    acceptor_target_orientation = digest_acceptor_target_orientation(
        acceptor_target_orientation
    )
    aromatic_n = receptor_profile == AROMATIC_N_PROFILE
    experimental = receptor_profile in {CARBONYL_PROFILE, AROMATIC_N_PROFILE}
    family = "carbonyl/aromatic-N" if aromatic_n else "carbonyl"
    optional = [
        acceptor_directions,
        acceptor_structure_position,
        acceptor_distances,
        acceptor_target_orientation,
    ]
    if experimental and any(value is None for value in optional):
        raise ArgumentError(
            argument="receptor_profile",
            reason=f"experimental {family} generation requires a native direction cache, explicit structure position, acceptor distances and target orientation",
        )
    if not experimental and any(value is not None for value in optional):
        raise ArgumentError(
            argument="receptor_profile",
            reason="acceptor options require the explicitly selected experimental carbonyl profile",
        )
    acceptors = (
        cached_acceptor_choices(
            feature_inventory,
            acceptor_directions,
            acceptor_structure_position,
            aromatic_n=aromatic_n,
        )
        if experimental
        else None
    )
    method = (
        AROMATIC_N_METHOD if aromatic_n else CARBONYL_METHOD if experimental else METHOD
    )
    options, omitted = _choices(
        feature_inventory,
        donor_distances,
        aromatic_distances,
        acceptors=acceptors,
        acceptor_distances=acceptor_distances,
        acceptor_label="acceptor" if aromatic_n else "carbonyl",
        method=method,
    )
    excluded = _receptor_exclusions(
        feature_inventory, excluded_volume_inventory, excluded_volume_radius
    )
    total = prod(len(choices) for choices in options) if options else 0
    count = min(total, budget)
    complete = count == total
    enumeration = dict(
        total_possible=total,
        visited=count,
        returned=count,
        remaining=total - count,
        max_hypotheses=budget,
        complete=complete,
        order="inventory feature; distance; aromatic +1/-1 face; provider acceptor local direction; rightmost feature fastest"
        if aromatic_n
        else "inventory feature; distance; aromatic +1/-1 face; provider carbonyl local direction; rightmost feature fastest"
        if experimental
        else "inventory feature; distance; aromatic +1/-1 face; rightmost feature fastest",
    )
    parameters = dict(
        receptor_profile=receptor_profile,
        donor_distances=donor_distances,
        aromatic_distances=aromatic_distances,
        radius=radius,
    )
    if excluded is not None:
        parameters["excluded_volume_radius"] = excluded["report"]["radius"]
    if experimental:
        parameters.update(
            acceptor_distances=acceptor_distances,
            acceptor_structure_position=acceptor_structure_position,
            acceptor_target_orientation=acceptor_target_orientation,
        )
    rows, models = [], []
    for index, combination in enumerate(islice(product(*options), count)):
        choices, specs = zip(*combination, strict=True)
        identity = f"receptor:{index}"
        model = from_receptor_projections(
            feature_inventory,
            projection_specs=list(specs),
            radius=radius,
            name=f"{name or 'Receptor hypothesis'} {index}",
            skip_digestion=True,
        )
        if excluded is not None:
            _attach_receptor_exclusions(model, excluded)
        generation = detached(
            dict(
                method=method,
                hypothesis_id=identity,
                parameters=parameters,
                choices=choices,
                enumeration=enumeration,
                omitted=omitted,
                assumptions="essential and weight-one construction; no binding importance inferred",
            )
        )
        model.metadata["projection_method"] = model.metadata["method"]
        model.metadata["method"] = method
        model.metadata["generation"] = generation
        rows.append(detached(dict(hypothesis_id=identity, choices=choices)))
        models.append(model)
    report = detached(
        dict(
            method=method,
            status="enumerated" if options else "no_supported_features",
            source_inventory=feature_inventory,
            parameters=parameters,
            enumeration=enumeration,
            omitted=omitted,
            hypotheses=rows,
            criteria=dict(
                ranking="none",
                geometry="cached only",
                molecular_operations=False,
                hypothesis="one choice per admitted source occurrence",
                aromatic_target="parallel cached unoriented axis",
            ),
        )
    )
    if excluded is not None:
        report["excluded_volumes"] = detached(excluded["report"])
        report["excluded_volumes"]["attached_model_count"] = len(models)
    if experimental:
        report["acceptor_directions"] = detached(acceptor_directions)
        report["criteria"].update(
            experimental=True,
            acceptor_model="provider carbonyl_trigonal model2 or aromatic_nitrogen_bisector model3/status1 only"
            if aromatic_n
            else "provider carbonyl_trigonal model2/status1 only",
            acceptor_target_orientation="explicit towards_receptor hypothesis (-u)",
            cache_consistency="declared source context; not molecular-source authentication",
        )
    return dict(method=method, models=models, report=report, complete=complete)
