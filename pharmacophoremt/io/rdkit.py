"""Explicit field projections to and from RDKit pharmacophore containers."""

import math
from numbers import Real

import numpy as np
from argdigest import arg_digest
from depdigest import dep_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.arg_digestion.curation import model
from pharmacophoremt._private.arg_digestion.rdkit_io import CONFIG
from pharmacophoremt._private.smonitor.emitter import warn
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ProjectionLossError,
)
from pharmacophoremt._private.smonitor.warnings import ProjectionLossWarning

PHMT_TO_RDKIT = {
    "hb donor": "Donor",
    "hb acceptor": "Acceptor",
    "aromatic ring": "Aromatic",
    "hydrophobicity": "Hydrophobic",
    "positive charge": "PosIonizable",
    "negative charge": "NegIonizable",
    "excluded volume": "ExcludedVolume",
}
RDKIT_TO_PHMT = {value: key for key, value in PHMT_TO_RDKIT.items()}


def _options(return_report, on_loss):
    if type(return_report) is not bool:
        raise ArgumentError(argument="return_report", reason="expected a boolean")
    if not isinstance(on_loss, str) or on_loss not in {"warn", "raise", "ignore"}:
        raise ArgumentError(argument="on_loss", reason="choose warn, raise or ignore")


def _report(direction, representation):
    return {
        "schema": "pharmacophoremt.rdkit-projection@1",
        "direction": direction,
        "representation": representation,
        "length_unit": "angstrom",
        "sites": [],
        "losses": [],
        "assumptions": [],
    }


def _loss_policy(report, on_loss):
    fields = report["losses"]
    if not fields:
        return
    if on_loss == "raise":
        raise ProjectionLossError(operation=report["direction"], fields=list(fields))
    if on_loss == "warn":
        warn(ProjectionLossWarning(operation=report["direction"], fields=list(fields)))


def _radius(value):
    """Reader zero means Point; native Sphere retains positive-radius admission."""
    quantity = _contracts.digest_nonnegative_radius(value)
    return _wire_values(quantity, "radius")


def _wire_values(quantity, argument, *, vector=False):
    values = np.asarray(puw.get_value(quantity, to_unit="angstrom"), dtype=float)
    if values.shape != ((3,) if vector else ()) or not np.all(np.isfinite(values)):
        raise ArgumentError(argument=argument, reason="expected finite angstrom values")
    return values.tolist() if vector else float(values)


def _native_rows(pharmacophore, representation, report):
    from pharmacophoremt.interaction_site.shape import (
        Disk,
        GaussianKernel,
        Point,
        Sphere,
        SphereAndVector,
    )

    model(pharmacophore)
    for field in (
        "name",
        "description",
        "score",
        "ref_mol",
        "ref_struct",
        "molecular_system",
    ):
        if getattr(pharmacophore, field) is not None:
            report["losses"].append("model." + field)
    if pharmacophore.metadata:
        report["losses"].append("model.metadata")
    for index, site in enumerate(pharmacophore.interaction_sites):
        features = _contracts.digest_features(site.features)
        if len(features) != 1 or site.n_features != len(site.features):
            raise ArgumentError(
                argument="features",
                reason="RDKit projection requires exactly one role per site; OR alternatives are unsupported",
            )
        feature = features[0]
        if feature not in PHMT_TO_RDKIT:
            raise ArgumentError(
                argument="features",
                reason="no RDKit family mapping for this native role",
            )
        essential = _contracts.digest_essential(site.essential)
        weight = _contracts.digest_weight(site.weight)
        if not isinstance(site.metadata, dict):
            raise ArgumentError(argument="metadata", reason="expected a site mapping")
        shape = _contracts.digest_shape(site.shape)
        radius = None
        lost = []
        if isinstance(shape, Point):
            shape_name = "point"
            center = _contracts.digest_position(shape.position)
            radius = 0.0
        elif isinstance(shape, (Sphere, SphereAndVector, Disk, GaussianKernel)):
            center = _contracts.digest_center(shape.center)
            if isinstance(shape, GaussianKernel):
                shape_name = "gaussian kernel"
                _contracts.digest_sigma(shape.sigma)
                lost.append("sigma")
            else:
                shape_name = "sphere"
                radius = _wire_values(_contracts.digest_radius(shape.radius), "radius")
            if isinstance(shape, SphereAndVector):
                shape_name = "sphere and vector"
                _contracts.digest_direction(shape.direction)
                lost.append("direction")
            if isinstance(shape, Disk):
                shape_name = "disk"
                _contracts.digest_normal(shape.normal)
                lost.append("normal")
        else:
            raise ArgumentError(
                argument="shape",
                reason="RDKit projection requires an explicit center; no center is inferred",
            )
        if representation == "spheres" and radius is None:
            raise ArgumentError(
                argument="shape",
                reason="explicit spheres require a radius; sigma is not a radius",
            )
        if representation == "points" and radius not in (None, 0.0):
            lost.append("radius")
        if not essential:
            lost.append("essential")
        if weight != 1.0:
            lost.append("weight")
        if site.metadata:
            lost.append("metadata")
        if feature == "excluded volume":
            lost.append("exclusion_constraint")
        row = {
            "source_index": index,
            "target_index": index,
            "feature": feature,
            "family": PHMT_TO_RDKIT[feature],
            "source_shape": shape_name,
            "center": _wire_values(center, "center", vector=True),
            "encoded_fields": ["family", "center"],
        }
        if representation == "spheres":
            row["radius"] = radius
            row["encoded_fields"].append("radius")
        report["sites"].append(row)
        report["losses"].extend(f"sites[{index}].{field}" for field in lost)
    report["assumptions"].append(
        {"field": "RDKit.feature_type", "value": "any", "origin": "adapter default"}
    )
    report["assumptions"].extend(
        [
            {"field": "RDKit.feature_id", "value": -1, "origin": "provider default"},
            {
                "field": "unencoded_native_defaults",
                "value": {"essential": True, "weight": 1.0},
            },
        ]
    )
    if representation == "points":
        report["assumptions"].append(
            {
                "field": "RDKit.pair_bounds",
                "value": "provider initialization from centers; no native radius translation",
            }
        )


@signal(tags=["io", "rdkit", "projection"])
@arg_digest(config=CONFIG)
@dep_digest("rdkit")
def to_rdkit(
    pharmacophore, *, representation="points", return_report=False, on_loss="warn"
):
    """Project native fields with an explicit warn/raise/ignore loss policy.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        Prepared native sites. A point supplies its position; supported extended
        shapes supply their center. Multi-role alternatives are refused.
    representation : {'points', 'spheres'}, keyword-only
        ``points`` preserves the historical RDKit Pharmacophore type and its
        ordinary initialized bounds. ``spheres`` uses ExplicitPharmacophore
        with angstrom radii; a native Point has radius zero.
    return_report : bool, keyword-only
        Return the converted object together with a detached finite JSON report
        of ordered field mappings, omitted fields and separate assumptions.
    on_loss : {'warn', 'raise', 'ignore'}, keyword-only
        Emit PHMT-W103, refuse with PHMT-E110 before construction, or explicitly
        accept omitted fields. Invalid inputs are refused in every mode.

    Returns
    -------
    rdkit.Chem.Pharm3D.Pharmacophore.Pharmacophore or ExplicitPharmacophore
        Provider object, or ``(object, report)`` when requested.

    Notes
    -----
    Field retention does not establish scientific matching or embedding
    equivalence. No radii are translated into pair-bound tolerances. Molecular
    preparation remains in MolSysMT; this operation exchanges prepared fields.

    Examples
    --------
    >>> import pharmacophoremt as phmt
    >>> converted, report = phmt.io.to_rdkit(
    ...     phmt.Pharmacophore(), representation='spheres',
    ...     return_report=True, on_loss='raise')
    >>> report['losses']
    []
    """
    from rdkit import Geometry
    from rdkit.Chem import ChemicalFeatures
    from rdkit.Chem.Pharm3D import Pharmacophore as rd

    _options(return_report, on_loss)
    if not isinstance(representation, str) or representation not in {
        "points",
        "spheres",
    }:
        raise ArgumentError(
            argument="representation", reason="choose points or spheres"
        )
    report = _report("to_rdkit", representation)
    _native_rows(pharmacophore, representation, report)
    positions = [Geometry.Point3D(*row["center"]) for row in report["sites"]]
    if representation == "points":
        for i, left in enumerate(positions):
            for right in positions[i + 1 :]:
                if not math.isfinite(left.Distance(right)):
                    raise ArgumentError(
                        argument="center",
                        reason="RDKit initialized pair distances overflow",
                    )
    _loss_policy(report, on_loss)
    features = [
        ChemicalFeatures.FreeChemicalFeature(row["family"], "any", position)
        for row, position in zip(report["sites"], positions)
    ]
    if representation == "points":
        target = rd.Pharmacophore(features)
    elif features:
        target = rd.ExplicitPharmacophore(
            features, [row["radius"] for row in report["sites"]]
        )
    else:
        target = rd.ExplicitPharmacophore()
        target.initFromLines([])
    return (target, report) if return_report else target


@signal(tags=["io", "rdkit", "projection"])
@arg_digest(config=CONFIG)
@dep_digest("rdkit")
def load_rdkit(
    rd_pharmacophore, *, radius="1 angstrom", return_report=False, on_loss="warn"
):
    """Read RDKit fields; radius=None retains explicit stored angstrom radii.

    Parameters
    ----------
    rd_pharmacophore : RDKit Pharmacophore or ExplicitPharmacophore
        Object with recognized mapped feature families and finite geometry.
    radius : length quantity or str or None, keyword-only
        The default ``'1 angstrom'`` keeps the historical fixed-radius reader.
        An explicit nonnegative length applies to every site; zero creates
        Points. ``None`` reads individual ExplicitPharmacophore radii and is
        refused for pair-bound Pharmacophore objects.
    return_report : bool, keyword-only
        Also return ordered mappings, field losses and construction assumptions.
    on_loss : {'warn', 'raise', 'ignore'}, keyword-only
        Report loss through PHMT-W103, refuse through PHMT-E110 before native
        construction, or explicitly accept it. Provider failures propagate.

    Returns
    -------
    Pharmacophore or tuple
        Native model, or ``(model, report)`` when requested. Standard positive
        radii keep the existing specialized Sphere classes.

    Notes
    -----
    Pair intervals never imply site radii. Native essential=True and weight=1
    are declared reader defaults, not recovered RDKit fields. See to_rdkit for
    the field-preservation and scientific-equivalence boundary.

    Examples
    --------
    >>> import pharmacophoremt as phmt
    >>> rd_query = phmt.io.to_rdkit(
    ...     phmt.Pharmacophore(), representation='spheres', on_loss='raise')
    >>> phmt.io.load_rdkit(rd_query, radius=None).n_interaction_sites
    0
    """
    from rdkit.Chem.Pharm3D import Pharmacophore as rd

    from pharmacophoremt import interaction_site as sites
    from pharmacophoremt.interaction_site.shape import Point, Sphere
    from pharmacophoremt.pharmacophore import Pharmacophore

    _options(return_report, on_loss)
    if not isinstance(rd_pharmacophore, (rd.Pharmacophore, rd.ExplicitPharmacophore)):
        raise ArgumentError(
            argument="rd_pharmacophore",
            reason="expected an RDKit Pharmacophore or ExplicitPharmacophore",
        )
    explicit = isinstance(rd_pharmacophore, rd.ExplicitPharmacophore)
    if radius is None and not explicit:
        raise ArgumentError(
            argument="radius",
            reason="radius=None requires explicit stored radii; pair bounds are not radii",
        )
    fixed_radius = _radius(radius) if radius is not None else None
    report = _report("load_rdkit", "spheres" if explicit else "points")
    features = list(rd_pharmacophore.getFeatures())
    if explicit and len(rd_pharmacophore.getRadii()) != len(features):
        raise ArgumentError(
            argument="rd_pharmacophore", reason="feature and radius counts disagree"
        )
    for index, feature in enumerate(features):
        family = feature.GetFamily()
        if family not in RDKIT_TO_PHMT:
            raise ArgumentError(
                argument="family", reason="no native role mapping for the RDKit family"
            )
        pos = feature.GetPos()
        center = _contracts.digest_center(
            puw.quantity([pos.x, pos.y, pos.z], "angstrom")
        )
        row = {
            "source_index": index,
            "target_index": index,
            "family": family,
            "feature": RDKIT_TO_PHMT[family],
            "center": _wire_values(center, "center", vector=True),
            "encoded_fields": ["family", "center"],
        }
        if explicit:
            raw_radius = rd_pharmacophore.getRadius(index)
            if isinstance(raw_radius, (bool, np.bool_)) or not isinstance(
                raw_radius, Real
            ):
                raise ArgumentError(
                    argument="radius", reason="stored radii must be nonnegative numbers"
                )
            stored_radius = _radius(puw.quantity(raw_radius, "angstrom"))
            if radius is None:
                row["encoded_fields"].append("radius")
            else:
                report["losses"].append(f"sites[{index}].stored_radius")
        row["radius"] = stored_radius if radius is None else fixed_radius
        for field, value, default in [
            ("type", feature.GetType(), "any"),
            ("id", feature.GetId(), -1),
        ]:
            if value not in (default, ""):
                report["losses"].append(f"sites[{index}].{field}")
        report["sites"].append(row)
        if family == "ExcludedVolume":
            report["assumptions"].append(
                {
                    "field": f"sites[{index}].exclusion_semantics",
                    "value": "custom family label decoded as native exclusion; upstream execution not established",
                }
            )
    if not explicit and len(features) > 1:
        for i in range(len(features)):
            for j in range(i + 1, len(features)):
                for lower, upper in [
                    (
                        rd_pharmacophore.getLowerBound(i, j),
                        rd_pharmacophore.getUpperBound(i, j),
                    ),
                    (
                        rd_pharmacophore.getLowerBound2D(i, j),
                        rd_pharmacophore.getUpperBound2D(i, j),
                    ),
                ]:
                    if (
                        not math.isfinite(lower)
                        or not math.isfinite(upper)
                        or lower < 0
                        or upper < lower
                    ):
                        raise ArgumentError(
                            argument="pair_bounds",
                            reason="expected finite nonnegative ordered intervals",
                        )
        report["losses"].extend(["pair_bounds", "pair_bounds_2d"])
    report["assumptions"].extend(
        [
            {"field": "sites.essential", "value": True},
            {"field": "sites.weight", "value": 1.0},
            {"field": "default_RDKit_type_and_id", "value": {"type": "any", "id": -1}},
        ]
    )
    if radius is not None:
        report["assumptions"].append(
            {
                "field": "sites.radius",
                "value": fixed_radius,
                "origin": "reader option; no pair-bound inference",
            }
        )
    _loss_policy(report, on_loss)
    target = Pharmacophore()
    specialized = dict(
        zip(
            [
                "hb donor",
                "hb acceptor",
                "aromatic ring",
                "hydrophobicity",
                "positive charge",
                "negative charge",
            ],
            [
                sites.HBDonorSphere,
                sites.HBAcceptorSphere,
                sites.AromaticRingSphere,
                sites.HydrophobicSphere,
                sites.PositiveChargeSphere,
                sites.NegativeChargeSphere,
            ],
        )
    )
    for row in report["sites"]:
        center = puw.quantity(row["center"], "angstrom")
        native_radius = puw.quantity(row["radius"], "angstrom")
        if row["radius"] == 0:
            site = sites.InteractionSite(Point(center), row["feature"])
        elif row["feature"] in specialized:
            site = specialized[row["feature"]](center, native_radius)
        else:
            site = sites.InteractionSite(Sphere(center, native_radius), row["feature"])
        target.add_interaction_site(site)
    return (target, report) if return_report else target
