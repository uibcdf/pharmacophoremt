"""Complementary pharmacophoric hypotheses from cached receptor features."""

from copy import deepcopy

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_center,
    digest_direction,
    digest_feature_inventory,
    digest_projection_specs,
    digest_radius,
    digest_structure_index,
)
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt._version import __version__
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Disk, Sphere, SphereAndVector
from pharmacophoremt.pharmacophore import Pharmacophore

METHOD = "explicit_receptor_projection@1"
COMPLEMENTS = {
    "hb donor": "hb acceptor",
    "hb acceptor": "hb donor",
    "aromatic ring": "aromatic ring",
    "positive charge": "negative charge",
    "negative charge": "positive charge",
    "hydrophobicity": "hydrophobicity",
}


def _specifications(inventory, specs):
    """Validate declared query decisions, without inferring molecular geometry."""
    digest_projection_specs(specs)
    allowed = {
        "feature_index",
        "projection_direction",
        "distance",
        "label",
        "target_direction",
        "target_normal",
        "evidence",
    }
    required = {"feature_index", "projection_direction", "distance", "label"}
    normalized, seen = [], set()
    for spec in specs:
        if not required <= spec.keys() or spec.keys() - allowed:
            raise ArgumentError(
                argument="projection_specs",
                reason="missing or unknown projection fields",
            )
        index = digest_structure_index(spec["feature_index"])
        if index >= len(inventory["features"]) or index in seen:
            raise ArgumentError(
                argument="projection_specs",
                reason="require unique existing feature indices; build alternative directions as separate hypotheses",
            )
        seen.add(index)
        if not isinstance(spec["label"], str) or not spec["label"].strip():
            raise ArgumentError(
                argument="projection_specs",
                reason="declare a nonempty hypothesis label",
            )
        if "evidence" in spec and not isinstance(spec["evidence"], dict):
            raise ArgumentError(
                argument="projection_specs",
                reason="projection evidence must be a mapping",
            )
        kind = COMPLEMENTS[inventory["features"][index]["kind"]]
        if (kind == "hb donor") != (spec.get("target_direction") is not None) or (
            kind == "aromatic ring"
        ) != (spec.get("target_normal") is not None):
            raise ArgumentError(
                argument="projection_specs",
                reason="declare target_direction only for donor targets and target_normal only for aromatic targets",
            )
        normalized.append(
            dict(
                feature_index=index,
                label=spec["label"],
                projection_direction=digest_direction(spec["projection_direction"]),
                distance=digest_radius(spec["distance"]),
                target_direction=None
                if kind != "hb donor"
                else digest_direction(spec["target_direction"]),
                target_normal=None
                if kind != "aromatic ring"
                else digest_direction(spec["target_normal"]),
                evidence=detached(spec.get("evidence", {})),
            )
        )
    return normalized


@signal(tags=["modeling", "receptor_projections"])
@arg_digest()
@attributed("numpy", "pyunitwizard")
def from_receptor_projections(
    feature_inventory, *, projection_specs, radius="0.15 nm", name=None
):
    """Build one complementary ligand hypothesis from declared receptor features.

    ``feature_inventory`` is a cached native ``get_features`` inventory containing
    only classical chemical features. ``projection_specs`` is an explicit list
    (possibly empty) of mappings with ``feature_index``, ``projection_direction``,
    positive explicit-unit ``distance`` and nonempty ``label``. The direction is
    normalized as a query parameter; the target center is the source feature
    center plus distance times that direction. Unlisted features emit no sites.

    Each source feature may appear once in a hypothesis. Alternative faces or
    directions require separate calls. A receptor acceptor yields a ligand donor
    and requires an independent ``target_direction``. Aromatic targets require an
    independent ``target_normal``. These target orientations are dimensionless
    query parameters; they are not inferred from the projection direction.
    Other targets are spheres and cannot declare target orientation. Receptor
    donors yield spherical acceptors, compatible with the native undirected
    acceptor inventory. Charges are complemented; hydrophobic/aromatic kinds
    retain their kind. Optional ``evidence`` mappings retain caller declarations.

    This operation places pharmacophoric query geometry, without accessing or
    moving molecular atoms, computing bond directions, finding pockets, assigning
    chemistry, or detecting observed interactions. Inventory origin, common frame
    and physical justification of each projection remain caller declarations.
    Molecular geometry must come from public MolSysMT tools; missing donor/local
    acceptor direction capabilities are tracked in MolSysMT #375. There are no
    default projection distances, directions or chemical-repair fallbacks.

    The returned Pharmacophore contains essential sites of weight one and
    detached source/specification provenance. An explicit empty projection list
    returns an empty hypothesis, which is not a valid positive PoseEvaluator query.
    Native quantity inventories are required; detached JSON is not decoded here.
    Cached attribution is preserved without crediting new molecular recognition.
    This method does not assert equivalence to retired structure-based heuristics
    or biological validity. Radius is a matching tolerance, independent of distance.
    """
    if feature_inventory is None:
        raise ArgumentError(
            argument="feature_inventory", reason="provide a cached receptor inventory"
        )
    digest_feature_inventory(feature_inventory)
    if any(
        record["kind"] not in COMPLEMENTS for record in feature_inventory["features"]
    ):
        raise ArgumentError(
            argument="feature_inventory",
            reason="use a chemical receptor inventory; exclusions are separate",
        )
    specs = _specifications(feature_inventory, projection_specs)
    radius = digest_radius(radius)
    model = Pharmacophore(name=name, ref_struct=feature_inventory["structure_index"])
    rows = []
    for site_index, spec in enumerate(specs):
        record = feature_inventory["features"][spec["feature_index"]]
        kind = COMPLEMENTS[record["kind"]]
        source_center = digest_center(record["center"])
        center = digest_center(
            puw.convert(source_center, to_unit="nm")
            + spec["projection_direction"] * puw.convert(spec["distance"], to_unit="nm")
        )
        if kind == "hb donor":
            shape = SphereAndVector(center, deepcopy(radius), spec["target_direction"])
        elif kind == "aromatic ring":
            shape = Disk(center, spec["target_normal"], deepcopy(radius))
        else:
            shape = Sphere(center, deepcopy(radius))
        metadata = detached(
            dict(
                method=METHOD,
                source_feature_index=spec["feature_index"],
                receptor_kind=record["kind"],
                atom_indices=record["atom_indices"],
                geometry_atom_indices=record.get(
                    "geometry_atom_indices", record["atom_indices"]
                ),
                structure_index=feature_inventory["structure_index"],
                chemical_state=feature_inventory["chemical_state"],
                projection=spec,
            )
        )
        site = InteractionSite(shape, kind, metadata=metadata)
        model.add_interaction_site(site)
        rows.append(
            detached(
                dict(
                    site_index=site_index,
                    feature_index=spec["feature_index"],
                    receptor_kind=record["kind"],
                    target_kind=kind,
                    center=site.center,
                    shape=site.shape_name,
                )
            )
        )
    used = {spec["feature_index"] for spec in specs}
    model.metadata = detached(
        dict(
            method=METHOD,
            software={
                "pharmacophoremt": __version__,
                "numpy": np.__version__,
                "pyunitwizard": puw.__version__,
            },
            source_inventory=feature_inventory,
            projection_specs=specs,
            supplied_projection_specs=projection_specs,
            emitted_radius=radius,
            sites=rows,
            omitted_feature_indices=[
                i for i in range(len(feature_inventory["features"])) if i not in used
            ],
            policy={
                "common_frame": "caller_declared",
                "placement": "explicit_hypothesis",
                "molecular_geometry_inference": False,
            },
        )
    )
    if "attribution" in feature_inventory:
        model.metadata["source_attribution"] = detached(
            feature_inventory["attribution"]
        )
    return model
