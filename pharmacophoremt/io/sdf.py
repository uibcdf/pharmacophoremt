"""Versioned persistence of PHMT virtual sites, not molecular SDF libraries."""

import json
import math

import numpy as np
from rdkit import Chem

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.argument._contracts import digest_features
from pharmacophoremt.io.phmt import _from_dict, _to_dict

_SCHEMA = "pharmacophoremt.sdf@1"
_SCHEMA_TAG = "PHARMACOPHOREMT_SCHEMA"
_MODEL_TAG = "PHARMACOPHOREMT_MODEL"
_MODEL_FIELDS = {
    "software",
    "version",
    "name",
    "description",
    "score",
    "ref_mol",
    "ref_struct",
    "metadata",
    "units",
    "interaction_sites",
}
_SITE_FIELDS = {"features", "essential", "weight", "shape", "metadata"}
# A virtual atom displays one anchor; the native payload holds the full shape.
_SHAPE_FIELDS = {
    "point": ("position",),
    "sphere": ("center", "radius"),
    "sphere and vector": ("center", "radius", "direction"),
    "gaussian kernel": ("center", "sigma"),
    "disk": ("center", "radius", "normal"),
    "cylinder": ("start", "end", "radius"),
}


def _fields(record, fields, label):
    if not isinstance(record, dict) or set(record) != set(fields):
        raise ValueError(f"Invalid {_SCHEMA} {label}: missing or unknown fields")


def _number(value):
    return type(value) in (int, float) and math.isfinite(value)


def _validate_model(data):
    """Check this format's complete record before native reconstruction."""
    _fields(data, _MODEL_FIELDS, "model")
    if data["software"] != "pharmacophoremt" or data["units"] != {
        "length": "nm",
        "direction": "dimensionless",
    }:
        raise ValueError(f"Invalid {_SCHEMA} software or units")
    if not isinstance(data["metadata"], dict) or not isinstance(
        data["interaction_sites"], list
    ):
        raise ValueError(f"Invalid {_SCHEMA} metadata or interaction_sites")
    # Also refuse non-finite numbers in metadata or model-level fields.
    json.dumps(data, allow_nan=False)
    for site in data["interaction_sites"]:
        _fields(site, _SITE_FIELDS, "site")
        if (
            not isinstance(site["features"], list)
            or not all(isinstance(feature, str) for feature in site["features"])
            or type(site["essential"]) is not bool
            or not _number(site["weight"])
            or site["weight"] < 0
            or not isinstance(site["metadata"], dict)
        ):
            raise ValueError(f"Invalid {_SCHEMA} site constraints")
        if digest_features(site["features"]) != site["features"]:
            raise ValueError(f"Invalid {_SCHEMA} duplicate features")
        shape = site["shape"]
        if (
            not isinstance(shape, dict)
            or not isinstance(shape.get("type"), str)
            or shape["type"] not in _SHAPE_FIELDS
        ):
            raise ValueError(f"Unsupported {_SCHEMA} shape")
        fields = _SHAPE_FIELDS[shape["type"]]
        _fields(shape, ("type", *fields), "shape")
        for field in fields:
            value = shape[field]
            if field in {"radius", "sigma"}:
                if not _number(value) or value <= 0:
                    raise ValueError(f"Invalid {_SCHEMA} {field}")
            elif (
                not isinstance(value, list)
                or len(value) != 3
                or not all(_number(component) for component in value)
            ):
                raise ValueError(f"Invalid {_SCHEMA} {field}")
            elif field in {"direction", "normal"} and not np.isclose(
                np.linalg.norm(value), 1.0, rtol=0, atol=1e-12
            ):
                raise ValueError(f"Invalid {_SCHEMA} unit {field}")


def _anchor(shape):
    """Display position in angstroms; never used to reconstruct geometry."""
    field = _SHAPE_FIELDS[shape["type"]][0]
    return puw.get_value(puw.quantity(shape[field], "nm"), to_unit="angstroms")


def to_sdf(pharmacophore, file_name):
    """Write one pharmacophore using the ``pharmacophoremt.sdf@1`` schema.

    A native JSON payload preserves supported shapes, site constraints and
    model/site metadata. Helium atoms display anchors in angstroms. Point,
    sphere, sphere-and-vector, disk, Gaussian kernel and cylinder are supported;
    shapelets are rejected before opening the destination. As in native JSON/
    YAML, the live molecular system is not serialized. See the persistence guide.
    """
    data = _to_dict(pharmacophore)
    _validate_model(data)
    payload = json.dumps(data, ensure_ascii=True, allow_nan=False)
    mol = Chem.RWMol()
    conf = Chem.Conformer(len(data["interaction_sites"]))
    conf.Set3D(True)
    for site in data["interaction_sites"]:
        index = mol.AddAtom(Chem.Atom(2))
        conf.SetAtomPosition(
            index, tuple(float(value) for value in _anchor(site["shape"]))
        )
    mol.AddConformer(conf)
    mol.SetProp(_SCHEMA_TAG, _SCHEMA)
    mol.SetProp(_MODEL_TAG, payload)
    with Chem.SDWriter(str(file_name)) as writer:
        # The model payload, not the rounded mol block, is authoritative.
        writer.SetProps([_SCHEMA_TAG, _MODEL_TAG])
        writer.write(mol)


def load_sdf(file_name):
    """Read exactly one versioned PHMT pharmacophore, with its native semantics.

    Unversioned historical/foreign SDFs, unknown schemas, incomplete payloads
    and inconsistent virtual atoms are rejected. Historical files omitted
    scientific constraints, so an automatic lossless migration is impossible.
    Regenerate from the original model or use native JSON/YAML instead.
    """
    supplier = Chem.SDMolSupplier(str(file_name), removeHs=False)
    if len(supplier) != 1:
        raise ValueError("Expected exactly one annotated PHMT pharmacophore SDF record")
    mol = supplier[0]
    if mol is None:
        raise ValueError("Invalid annotated PHMT pharmacophore SDF record")
    if not mol.HasProp(_SCHEMA_TAG):
        raise ValueError(
            "Unversioned or foreign SDF cannot restore PHMT scientific constraints; "
            "regenerate from the original model or use native JSON/YAML"
        )
    if mol.GetProp(_SCHEMA_TAG) != _SCHEMA:
        raise ValueError("Unsupported PHMT pharmacophore SDF schema")
    if not mol.HasProp(_MODEL_TAG):
        raise ValueError("Missing PHMT pharmacophore SDF model payload")
    data = json.loads(mol.GetProp(_MODEL_TAG))
    _validate_model(data)
    sites = data["interaction_sites"]
    if (
        mol.GetNumAtoms() != len(sites)
        or mol.GetNumBonds() != 0
        or mol.GetNumConformers() != 1
        or any(atom.GetAtomicNum() != 2 for atom in mol.GetAtoms())
    ):
        raise ValueError("Inconsistent PHMT SDF virtual sites")
    conf = mol.GetConformer()
    for index, site in enumerate(sites):
        position = conf.GetAtomPosition(index)
        # V2000 rounds coordinates to four decimal places in angstroms.
        if not np.allclose(
            [position.x, position.y, position.z],
            _anchor(site["shape"]),
            rtol=0,
            atol=5.1e-5,
        ):
            raise ValueError("Inconsistent PHMT SDF virtual-site anchor")
    return _from_dict(data)
