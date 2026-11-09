"""PHMT-owned scientific field planning for the existing saved JSON reader."""

from collections.abc import Mapping

from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ArgumentTypeError,
)

FEATURES = {
    "Aromatic",
    "Hydrophobic",
    "HydrogenAcceptor",
    "HydrogenDonor",
    "PositiveIon",
    "NegativeIon",
    "ExclusionSphere",
    "InclusionSphere",
}
DIRECTED = {"Aromatic", "HydrogenAcceptor", "HydrogenDonor"}
POINT_FIELDS = {
    "name",
    "x",
    "y",
    "z",
    "radius",
    "enabled",
    "requirement",
    "minsize",
    "maxsize",
    "size",
    "vector_on",
    "svector",
    "vector",
}
POINT_UI = {"selected", "hasvec"}
QUERY_UI = {
    "view",
    "backgroundcolor",
    "surfaceopacity",
    "LigandMolStyleSelect",
    "LigandMolStyleSelectcolor",
    "ResultsMolStyleSelect",
    "ResultsMolStyleSelectcolor",
    "ReceptorMolStyleSelect",
    "ReceptorMolStyleSelectcolor",
    "receptorbackbone",
    "recname",
    "receptorid",
    "ligandFormat",
}
ENGINE_FIELDS = {
    "subset",
    "max-orient",
    "reduceConfs",
    "max-hits",
    "maxRMSD",
    "minMolWeight",
    "maxMolWeight",
    "minrotbonds",
    "maxrotbonds",
    "minlogp",
    "maxlogp",
    "minpsa",
    "maxpsa",
    "minaromatics",
    "maxaromatics",
    "minhba",
    "maxhba",
    "minhbd",
    "maxhbd",
    "ShapeModeSelect",
    "inselect",
    "intolerance",
    "inshapestyle",
    "exselect",
    "extolerance",
    "exshapestyle",
}


def _type_error(field, expected, value):
    raise ArgumentTypeError(
        argument=field, expected_type=expected, actual_type=type(value).__name__
    )


def _mapping(value, field):
    if not isinstance(value, Mapping):
        _type_error(field, "a JSON mapping", value)
    if any(not isinstance(key, str) for key in value):
        raise ArgumentError(argument=field, reason="JSON member names must be strings")


def _count(value, field):
    if value is None or isinstance(value, str) and value == "":
        return
    if type(value) is int:
        if value < 0:
            raise ArgumentError(
                argument=field, reason="expected a nonnegative feature count"
            )
        return
    if isinstance(value, str) and value.isascii() and value.isdecimal():
        return
    _type_error(
        field, "a nonnegative integer, decimal string, empty string or null", value
    )


def _direction(point, prefix, report):
    flag = point.get("vector_on")
    if "vector_on" in point:
        if not (type(flag) is bool or type(flag) is int and flag in (0, 1)):
            _type_error(prefix + ".vector_on", "a boolean or integer 0/1", flag)
        if not flag:
            report["ignored_fields"].extend(
                prefix + "." + key for key in ("svector", "vector") if key in point
            )
            return None
    value = point.get("svector")
    field = prefix + ".svector"
    if value is None:
        vectors = point.get("vector", [])
        field = prefix + ".vector"
        if not isinstance(vectors, (list, tuple)):
            _type_error(field, "a JSON vector array", vectors)
        if len(vectors) > 1:
            raise ArgumentError(
                argument=field,
                reason="multiple active vector alternatives have no supported native mapping",
            )
        value = vectors[0] if vectors else None
    elif "vector" in point:
        report["ignored_fields"].append(prefix + ".vector")
    if value is None:
        if flag:
            raise ArgumentError(
                argument=prefix + ".vector_on",
                reason="active direction requires a vector",
            )
        return None
    _mapping(value, field)
    if set(value) != {"x", "y", "z"}:
        raise ArgumentError(
            argument=field, reason="a single vector requires exactly x, y and z"
        )
    if point["name"] not in DIRECTED:
        _loss(
            report,
            field,
            "this feature's native spherical representation has no direction",
        )
        return None
    return [value[key] for key in ("x", "y", "z")]


def _loss(report, field, reason):
    report["losses"].append(field)
    report["loss_details"][field] = reason


def _plan(data):
    """Classify all admitted metadata before model/site/molecule construction."""
    _mapping(data, "query")
    points = data.get("points")
    if not isinstance(points, (list, tuple)):
        _type_error("points", "a JSON array", points)
    report = {
        "schema": "pharmacophoremt.pharmer-import@1",
        "direction": "Pharmer JSON -> native",
        "length_unit": "angstrom",
        "sites": [],
        "losses": [],
        "loss_details": {},
        "ignored_fields": [],
        "unapplied_settings": [],
        "disabled_point_indices": [],
        "assumptions": [
            {"field": "native.weight", "value": 1.0},
            {
                "field": "native.angular_policy",
                "value": "chosen independently by the evaluator; no engine equivalence",
            },
        ],
    }
    rows = []
    for index, point in enumerate(points):
        prefix = f"points[{index}]"
        _mapping(point, prefix)
        enabled = point.get("enabled", True)
        if not isinstance(enabled, bool):
            _type_error(prefix + ".enabled", "a JSON boolean", enabled)
        if not enabled:
            report["disabled_point_indices"].append(index)
            continue
        name = point.get("name")
        if not isinstance(name, str) or name not in FEATURES:
            raise ArgumentError(
                argument=prefix + ".name", reason="unsupported Pharmer feature name"
            )
        requirement = point.get("requirement", "required")
        if not isinstance(requirement, str):
            _type_error(prefix + ".requirement", "a requirement string", requirement)
        if requirement.lower() not in {"", "required", "optional", "notpresent"}:
            raise ArgumentError(
                argument=prefix + ".requirement",
                reason="choose required, optional or notpresent; unqualified meanings are reported",
            )
        if requirement.lower() in {"optional", "notpresent"}:
            _loss(
                report,
                prefix + ".requirement",
                "optional/negated semantics are not mapped; compatibility projection remains required",
            )
        for key in ("minsize", "maxsize", "size"):
            if key not in point:
                continue
            value = point[key]
            _count(value, prefix + "." + key)
            neutral = (
                value is None or value == "" or key == "minsize" and value in (0, "0")
            )
            if not neutral:
                _loss(
                    report,
                    prefix + "." + key,
                    "feature size/count information has no native field mapping",
                )
        for key in sorted(point):
            if key in POINT_UI:
                report["ignored_fields"].append(prefix + "." + key)
            elif key not in POINT_FIELDS:
                _loss(
                    report,
                    prefix + "." + key,
                    "unclassified point field is not preserved",
                )
        direction = _direction(point, prefix, report)
        report["sites"].append(
            {
                "source_index": index,
                "target_index": len(rows),
                "feature": name,
                "shape": "sphere and vector" if direction is not None else "sphere",
                "direction_active": direction is not None,
                "encoded_fields": ["name", "center", "radius", "enabled"]
                + (["direction"] if direction is not None else []),
            }
        )
        rows.append((index, point, direction))
    for key in sorted(data):
        path = "query." + key
        if key in {"points", "ligand"}:
            continue
        if key in QUERY_UI:
            report["ignored_fields"].append(path)
        elif key in ENGINE_FIELDS:
            report["unapplied_settings"].append(path)
            if data[key] is not None and data[key] != "":
                _loss(
                    report,
                    path,
                    "engine/library/search setting is not executed by model import",
                )
        else:
            _loss(
                report,
                path,
                "unclassified query field or unsupported attachment is not preserved",
            )
    return rows, report
