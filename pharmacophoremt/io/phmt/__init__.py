import yaml
import json
import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt import interaction_site as interaction_sites


def _to_dict(pharmacophore):
    """Internal helper to convert a Pharmacophore to a serializable dictionary."""
    from pharmacophoremt._version import __version__

    data = {
        "software": "pharmacophoremt",
        "version": __version__,
        "name": pharmacophore.name,
        "description": pharmacophore.description,
        "score": pharmacophore.score,
        "ref_mol": pharmacophore.ref_mol,
        "ref_struct": pharmacophore.ref_struct,
        "interaction_sites": []
    }

    for site in pharmacophore.interaction_sites:
        shape = site.shape
        stype = shape.shape_name

        if stype == 'point':
            shape_dict = {
                "type": "point",
                "position": puw.get_value(shape.position, to_unit='nm').tolist(),
            }
        elif stype == 'sphere':
            shape_dict = {
                "type": "sphere",
                "center": puw.get_value(shape.center, to_unit='nm').tolist(),
                "radius": float(puw.get_value(shape.radius, to_unit='nm')),
            }
        elif stype == 'sphere and vector':
            shape_dict = {
                "type": "sphere and vector",
                "center": puw.get_value(shape.center, to_unit='nm').tolist(),
                "radius": float(puw.get_value(shape.radius, to_unit='nm')),
                "direction": puw.get_value(shape.direction).tolist(),
            }
        elif stype == 'gaussian kernel':
            shape_dict = {
                "type": "gaussian kernel",
                "center": puw.get_value(shape.center, to_unit='nm').tolist(),
                "sigma": float(puw.get_value(shape.sigma, to_unit='nm')),
            }
        elif stype == 'disk':
            shape_dict = {
                "type": "disk",
                "center": puw.get_value(shape.center, to_unit='nm').tolist(),
                "radius": float(puw.get_value(shape.radius, to_unit='nm')),
                "normal": puw.get_value(shape.normal).tolist(),
            }
        elif stype == 'cylinder':
            shape_dict = {
                "type": "cylinder",
                "start": puw.get_value(shape.start, to_unit='nm').tolist(),
                "end": puw.get_value(shape.end, to_unit='nm').tolist(),
                "radius": float(puw.get_value(shape.radius, to_unit='nm')),
            }
        elif stype == 'shapelet':
            shape_dict = {"type": "shapelet"}
        else:
            raise NotImplementedError(f"Serialization not implemented for shape '{stype}'")

        site_dict = {
            "features": site.features,
            "essential": site.essential,
            "weight": site.weight,
            "shape": shape_dict,
            "metadata": site.metadata,
        }
        data["interaction_sites"].append(site_dict)

    return data


def _from_dict(data):
    """Internal helper to reconstruct a Pharmacophore from a dictionary."""
    from pharmacophoremt.pharmacophore import Pharmacophore
    from pharmacophoremt.interaction_site.shape import (
        Point, Sphere, SphereAndVector, GaussianKernel, Disk, Cylinder
    )

    if data.get("software") != "pharmacophoremt":
        raise ValueError("Not a valid PharmacophoreMT file (missing 'software: pharmacophoremt')")

    ph = Pharmacophore(
        name=data.get("name"),
        description=data.get("description"),
        score=data.get("score"),
        ref_mol=data.get("ref_mol"),
        ref_struct=data.get("ref_struct"),
    )

    for s_data in data.get("interaction_sites", []):
        features = s_data["features"]
        essential = s_data.get("essential", True)
        weight = s_data.get("weight", 1.0)
        metadata = s_data.get("metadata", {})
        shape_data = s_data["shape"]
        stype = shape_data["type"]

        if stype == 'point':
            position = puw.quantity(shape_data["position"], 'nm')
            shape = Point(position, skip_digestion=True)

        elif stype == 'sphere':
            center = puw.quantity(shape_data["center"], 'nm')
            radius = puw.quantity(shape_data["radius"], 'nm')
            shape = Sphere(center, radius, skip_digestion=True)

        elif stype == 'sphere and vector':
            center = puw.quantity(shape_data["center"], 'nm')
            radius = puw.quantity(shape_data["radius"], 'nm')
            direction = np.array(shape_data["direction"])
            shape = SphereAndVector(center, radius, direction, skip_digestion=True)

        elif stype == 'gaussian kernel':
            center = puw.quantity(shape_data["center"], 'nm')
            sigma = puw.quantity(shape_data["sigma"], 'nm')
            shape = GaussianKernel(center, sigma, skip_digestion=True)

        elif stype == 'disk':
            center = puw.quantity(shape_data["center"], 'nm')
            radius = puw.quantity(shape_data["radius"], 'nm')
            normal = np.array(shape_data["normal"])
            shape = Disk(center, normal, radius, skip_digestion=True)

        elif stype == 'cylinder':
            start = puw.quantity(shape_data["start"], 'nm')
            end = puw.quantity(shape_data["end"], 'nm')
            radius = puw.quantity(shape_data["radius"], 'nm')
            shape = Cylinder(start, end, radius, skip_digestion=True)

        elif stype == 'shapelet':
            from pharmacophoremt.interaction_site.shape import Shapelet
            shape = Shapelet(skip_digestion=True)

        else:
            raise NotImplementedError(f"Shape type '{stype}' is not supported for loading")

        site = interaction_sites.InteractionSite(
            shape, features,
            essential=essential, weight=weight, metadata=metadata,
            skip_digestion=True
        )
        ph.add_interaction_site(site, skip_digestion=True)

    return ph


def to_json(pharmacophore, file_name):
    """Export a Pharmacophore to a JSON file.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        The pharmacophore to export.
    file_name : str
        Path to the output JSON file.
    """
    data = _to_dict(pharmacophore)
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)


def load_json(file_name):
    """Load a Pharmacophore from a JSON file.

    Parameters
    ----------
    file_name : str
        Path to the JSON file.

    Returns
    -------
    Pharmacophore
    """
    with open(file_name, 'r') as f:
        data = json.load(f)
    return _from_dict(data)


def to_yaml(pharmacophore, file_name):
    """Export a Pharmacophore to a YAML file.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        The pharmacophore to export.
    file_name : str
        Path to the output YAML file.
    """
    data = _to_dict(pharmacophore)
    with open(file_name, 'w') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)


def load_yaml(file_name):
    """Load a Pharmacophore from a YAML file.

    Parameters
    ----------
    file_name : str
        Path to the YAML file.

    Returns
    -------
    Pharmacophore
    """
    with open(file_name, 'r') as f:
        data = yaml.safe_load(f)
    return _from_dict(data)
