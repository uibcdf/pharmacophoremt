"""Bounded complementary hypotheses from cached provider-derived geometry."""

from itertools import islice, product
from math import prod

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument._contracts import (
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

from .receptor_projections import from_receptor_projections

METHOD = "cached_receptor_donor_aromatic_faces@1"


def _choices(inventory, donor_distances, aromatic_distances):
    options, omitted = [], []
    for index, record in enumerate(inventory["features"]):
        kind = record["kind"]
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
                        method=METHOD,
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
    name=None,
    skip_digestion=False,
):
    """Generate separate complementary hypotheses from a cached receptor region.

    Parameters
    ----------
    feature_inventory : dict
        Native get_features result for one explicitly prepared region, structure
        and chemical state. Cached origin/frame claims remain caller declarations.
    receptor_profile : {'donor_aromatic_faces'}
        Required scientific choice. Every indexed donor emits a spherical ligand
        acceptor along its cached D→H direction. Every aromatic ring emits a Disk
        on either face, with the cached ring axis explicitly used as target axis.
    donor_distances, aromatic_distances : list or tuple of length quantities
        Nonempty positive finite scalar choices with explicit units, in caller
        order. Both lists are required even if a family is absent. Repeated
        physically equivalent choices remain distinct declared alternatives.
    radius : length quantity
        Required positive positional matching tolerance, independent of offsets.
    max_hypotheses : int
        Required finite nonnegative bound. Zero can return incomplete empty output.
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
    donor-H pairs remain distinct even when they share a donor atom. Every site
    starts essential and weight one; these are construction assumptions.

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
    options, omitted = _choices(feature_inventory, donor_distances, aromatic_distances)
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
        order="inventory feature; distance; aromatic +1/-1 face; rightmost feature fastest",
    )
    parameters = dict(
        receptor_profile=receptor_profile,
        donor_distances=donor_distances,
        aromatic_distances=aromatic_distances,
        radius=radius,
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
        generation = detached(
            dict(
                method=METHOD,
                hypothesis_id=identity,
                parameters=parameters,
                choices=choices,
                enumeration=enumeration,
                omitted=omitted,
                assumptions="essential and weight-one construction; no binding importance inferred",
            )
        )
        model.metadata["projection_method"] = model.metadata["method"]
        model.metadata["method"] = METHOD
        model.metadata["generation"] = generation
        rows.append(detached(dict(hypothesis_id=identity, choices=choices)))
        models.append(model)
    report = detached(
        dict(
            method=METHOD,
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
    return dict(method=METHOD, models=models, report=report, complete=complete)
