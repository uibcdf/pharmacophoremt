"""Saved Pharmer field import with explicit scientific projection decisions."""

import json
from copy import deepcopy

import molsysmt as msm
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import interaction_site as interaction_sites
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.pharmer_io import CONFIG

from ._pharmer_profile import _plan
from ._projection import _loss_policy, _options


@signal(tags=["io", "pharmer", "read"])
@arg_digest(config=CONFIG)
def from_pharmer(pharmacophore, *, return_report=False, on_loss="warn"):
    """Read supported fields with a warn/raise/ignore scientific loss policy.

    Disabled points are omitted before parsing; missing enabled means True.
    Source units are angstroms. A false/zero vector_on disables direction;
    otherwise one declared vector is preserved for supported directional roles.
    Optional/negated requirements, nonneutral size bounds, unknown fields and
    unapplied engine settings are reported instead of silently claimed preserved.

    Strict loss refusal and promoted warnings precede model/site/molecule
    construction. Reports retain field paths, not original molecular payloads.
    Lossy imports also retain a detached metadata['pharmer']['import_report'].
    With return_report=True return (model, report); otherwise return the model.
    No external engine or equivalent screening/angle policy is inferred.
    """
    _options(return_report, on_loss)
    if isinstance(pharmacophore, str):
        if not pharmacophore.endswith(".json"):
            raise NotImplementedError
        print(f"Reading file: {pharmacophore}")
        with open(pharmacophore) as stream:
            pharmacophore = json.load(stream)
    rows, report = _plan(pharmacophore)
    _loss_policy(report, on_loss)

    from pharmacophoremt.pharmacophore import Pharmacophore

    model = Pharmacophore()
    print(f"Number of points in JSON: {len(pharmacophore['points'])}")
    spherical = {
        "Aromatic": interaction_sites.AromaticRingSphere,
        "Hydrophobic": interaction_sites.HydrophobicSphere,
        "HydrogenAcceptor": interaction_sites.HBAcceptorSphere,
        "HydrogenDonor": interaction_sites.HBDonorSphere,
        "PositiveIon": interaction_sites.PositiveChargeSphere,
        "NegativeIon": interaction_sites.NegativeChargeSphere,
        "ExclusionSphere": interaction_sites.ExcludedVolumeSphere,
        "InclusionSphere": interaction_sites.IncludedVolumeSphere,
    }
    directional = {
        "Aromatic": interaction_sites.AromaticRingSphereAndVector,
        "HydrogenAcceptor": interaction_sites.HBAcceptorSphereAndVector,
        "HydrogenDonor": interaction_sites.HBDonorSphereAndVector,
    }
    for _, point, direction in rows:
        center = puw.quantity([point[key] for key in ("x", "y", "z")], "angstroms")
        radius = puw.quantity(point["radius"], "angstroms")
        site = (
            spherical[point["name"]](center, radius)
            if direction is None
            else directional[point["name"]](center, radius, direction)
        )
        model.add_interaction_site(site)
    if report["disabled_point_indices"]:
        model.metadata["pharmer"] = {
            "source_point_indices": [index for index, _, _ in rows],
            "disabled_point_indices": list(report["disabled_point_indices"]),
        }
    if report["losses"] or report["unapplied_settings"]:
        model.metadata.setdefault(
            "pharmer",
            {
                "source_point_indices": [index for index, _, _ in rows],
                "disabled_point_indices": [],
            },
        )["import_report"] = deepcopy(report)
    if "ligand" in pharmacophore:
        model.molecular_system = msm.convert(
            pharmacophore["ligand"], to_form="molsysmt.MolSys"
        )
    return (model, deepcopy(report)) if return_report else model


def to_pharmer(pharmacophore, file_name):

    pharmer_interaction_site_name = {  # dictionary to map pharmacophoremt feature names to pharmer feature names
        "aromatic ring": "Aromatic",
        "hydrophobicity": "Hydrophobic",
        "hb acceptor": "HydrogenAcceptor",
        "hb donor": "HydrogenDonor",
        "included volume": "InclusionSphere",
        "excluded volume": "ExclusionSphere",
        "positive charge": "PositiveIon",
        "negative charge": "NegativeIon",
    }
    points = []
    for interaction_site in pharmacophore.interaction_sites:
        point_dict = {}
        temp_center = puw.get_value(interaction_site.center, to_unit="angstroms")
        point_dict["name"] = pharmer_interaction_site_name[
            interaction_site.feature_name
        ]
        point_dict["svector"] = {}
        if hasattr(interaction_site, "direction"):
            point_dict["hasvec"] = True
            point_dict["svector"]["x"] = interaction_site.direction[0]
            point_dict["svector"]["y"] = interaction_site.direction[1]
            point_dict["svector"]["z"] = interaction_site.direction[2]
        else:
            point_dict["hasvec"] = False
            point_dict["svector"]["x"] = 1
            point_dict["svector"]["y"] = 0
            point_dict["svector"]["z"] = 0
        point_dict["x"] = temp_center[0]
        point_dict["y"] = temp_center[1]
        point_dict["z"] = temp_center[2]
        point_dict["radius"] = puw.get_value(
            interaction_site.radius, to_unit="angstroms"
        )
        point_dict["enabled"] = True
        point_dict["vector_on"] = 0
        point_dict["minsize"] = ""
        point_dict["maxsize"] = ""
        point_dict["selected"] = False

        points.append(point_dict)

    pharmer_dict = {}
    pharmer_dict["points"] = points

    # TODO: add ligand and/or receptor

    with open(file_name, "w") as outfile:
        json.dump(pharmer_dict, outfile)
