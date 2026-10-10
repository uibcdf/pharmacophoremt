"""Shared validators for the public geometry and pose-evaluation boundaries."""

from copy import deepcopy

import numpy as np
import pyunitwizard as puw

from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def _length(obj, argument, vector=False):
    try:
        quantity = puw.ensure_quantity(obj, dimensionality={"[L]": 1})
        values = np.asarray(puw.get_value(quantity, to_unit="nm"), dtype=float)
    except Exception as error:
        raise ArgumentError(
            argument=argument, reason="expected a length quantity with an explicit unit"
        ) from error
    shape = (3,) if vector else ()
    if values.shape != shape or not np.all(np.isfinite(values)):
        raise ArgumentError(
            argument=argument, reason=f"expected finite values with shape {shape}"
        )
    if not vector and values <= 0:
        raise ArgumentError(argument=argument, reason="expected a positive length")
    return quantity


def digest_center(obj):
    return _length(obj, "center", vector=True)


def digest_position(obj):
    return _length(obj, "position", vector=True)


def digest_start(obj):
    return _length(obj, "start", vector=True)


def digest_end(obj):
    return _length(obj, "end", vector=True)


def digest_radius(obj):
    return _length(obj, "radius")


def digest_excluded_volume_radius(obj):
    return None if obj is None else digest_radius(obj)


def digest_excluded_volume_inventory(obj):
    return digest_feature_inventory(obj)


def digest_projection_specs(obj):
    if not isinstance(obj, (list, tuple)) or any(
        not isinstance(row, dict) for row in obj
    ):
        raise ArgumentError(
            argument="projection_specs",
            reason="provide an explicit list of projection mappings",
        )
    return obj


def digest_sigma(obj):
    return _length(obj, "sigma")


def digest_direction(obj):
    try:
        values = np.asarray(
            puw.get_value(puw.convert(obj, to_unit="dimensionless"))
            if puw.is_quantity(obj)
            else obj,
            dtype=float,
        )
    except Exception as error:
        raise ArgumentError(
            argument="direction", reason="expected a dimensionless vector"
        ) from error
    if values.shape != (3,) or not np.all(np.isfinite(values)) or not np.any(values):
        raise ArgumentError(
            argument="direction",
            reason="expected a finite, nonzero vector of shape (3,)",
        )
    scaled = values / np.max(np.abs(values))
    return scaled / np.linalg.norm(scaled)


def digest_normal(obj):
    return digest_direction(obj)


def digest_features(obj):
    from pharmacophoremt.data.smarts import FEAT_TO_CHAR

    try:
        values = [obj] if isinstance(obj, str) else list(obj)
    except TypeError as error:
        raise ArgumentError(
            argument="features", reason="expected known pharmacophore feature names"
        ) from error
    if not values or any(
        not isinstance(value, str) or value not in FEAT_TO_CHAR for value in values
    ):
        raise ArgumentError(
            argument="features", reason="expected known pharmacophore feature names"
        )
    return list(dict.fromkeys(values))


def digest_shape(obj):
    from pharmacophoremt.interaction_site.shape import (
        Cylinder,
        Disk,
        GaussianKernel,
        Point,
        Sphere,
        SphereAndVector,
    )

    if not isinstance(
        obj, (Cylinder, Disk, GaussianKernel, Point, Sphere, SphereAndVector)
    ):
        raise ArgumentError(
            argument="shape", reason="expected a supported pharmacophore geometry"
        )
    return obj


def digest_essential(obj):
    if not isinstance(obj, (bool, np.bool_)):
        raise ArgumentError(argument="essential", reason="expected a boolean")
    return bool(obj)


def digest_weight(obj):
    if isinstance(obj, (bool, np.bool_)):
        raise ArgumentError(
            argument="weight", reason="expected a nonnegative real number"
        )
    try:
        value = float(obj)
    except (TypeError, ValueError) as error:
        raise ArgumentError(
            argument="weight", reason="expected a nonnegative real number"
        ) from error
    if not np.isfinite(value) or value < 0:
        raise ArgumentError(
            argument="weight", reason="expected a finite, nonnegative real number"
        )
    return value


def digest_metadata(obj):
    if obj is None:
        return {}
    if not isinstance(obj, dict):
        raise ArgumentError(argument="metadata", reason="expected a dictionary")
    return deepcopy(obj)


def digest_score(obj):
    if obj is None:
        return None
    try:
        value = float(obj)
    except (TypeError, ValueError) as error:
        raise ArgumentError(
            argument="score", reason="expected a finite scalar or None"
        ) from error
    if not np.isfinite(value):
        raise ArgumentError(argument="score", reason="expected a finite scalar or None")
    return value


def digest_ref_mol(obj):
    if obj is not None and (
        isinstance(obj, (bool, np.bool_))
        or not isinstance(obj, (int, np.integer))
        or obj < 0
    ):
        raise ArgumentError(
            argument="reference", reason="expected a nonnegative integer or None"
        )
    return obj


def digest_ref_struct(obj):
    return digest_ref_mol(obj)


def digest_skip_digestion(obj):
    return digest_essential(obj)


def digest_labels(obj):
    values = np.asarray(obj)
    if values.ndim != 1 or not values.size or not np.all(np.isin(values, [0, 1])):
        raise ArgumentError(
            argument="labels", reason="expected a nonempty vector of binary labels"
        )
    return values.astype(int)


def digest_scores(obj):
    try:
        if puw.is_quantity(obj):
            obj = puw.get_value(puw.convert(obj, to_unit="dimensionless"))
        values = np.asarray(obj, dtype=float)
    except Exception as error:
        raise ArgumentError(
            argument="scores", reason="expected dimensionless scores"
        ) from error
    if values.ndim != 1 or not values.size or not np.all(np.isfinite(values)):
        raise ArgumentError(
            argument="scores", reason="expected a nonempty vector of finite scores"
        )
    return values


def digest_fraction(obj):
    from pharmacophoremt.validation.metrics import _positive

    return _positive(obj, "fraction", maximum=1)


def digest_alpha(obj):
    from pharmacophoremt.validation.metrics import _positive

    return _positive(obj, "alpha")


def digest_get_direction(obj):
    return digest_essential(obj)


def digest_method(obj):
    if obj not in {
        "complex-based",
        "ligand-based",
        "structure-based",
        "interaction-based",
        "interaction-collection",
        "reference-ligand",
    }:
        raise ArgumentError(
            argument="method", reason="expected a supported modeling route"
        )
    return obj


def digest_consensus_method(obj):
    if not isinstance(obj, str) or obj not in {"aligned_cliques", "rigid"}:
        raise ArgumentError(
            argument="consensus_method",
            reason="legacy consensus is retired; explicitly choose aligned_cliques or rigid on prepared ligands",
        )
    return obj


def digest_molecular_systems(obj):
    if isinstance(obj, (str, bytes, dict)):
        raise ArgumentError(
            argument="molecular_systems",
            reason="provide an iterable of prepared ligands",
        )
    try:
        iter(obj)
    except TypeError as error:
        raise ArgumentError(
            argument="molecular_systems",
            reason="provide an iterable of prepared ligands",
        ) from error
    return obj


def digest_n_points(obj):
    return _positive_integer(obj, "n_points")


def digest_min_actives(obj):
    return None if obj is None else _positive_integer(obj, "min_actives")


def digest_n_conformers(obj):
    return _positive_integer(obj, "n_conformers")


def digest_conformer_rmsd_threshold(obj):
    if (
        isinstance(obj, (bool, np.bool_))
        or not isinstance(obj, (int, float, np.integer, np.floating))
        or not np.isfinite(obj)
        or obj <= 0
    ):
        raise ArgumentError(
            argument="conformer_rmsd_threshold",
            reason="expected a positive finite scalar",
        )
    return float(obj)


def digest_ligand_selection(obj):
    if obj is None or isinstance(obj, str):
        return obj  # The selection expression is resolved by MolSysMT.
    values = np.asarray(obj)
    if (
        values.ndim != 1
        or not values.size
        or values.dtype.kind not in "iu"
        or np.any(values < 0)
    ):
        raise ArgumentError(
            argument="ligand_selection",
            reason="expected a MolSysMT selection or nonnegative atom indices",
        )
    return values.astype(np.int64)


def digest_receptor_selection(obj):
    return digest_ligand_selection(obj)


def digest_color_palette(obj):
    if not isinstance(obj, (str, dict)) or not obj:
        raise ArgumentError(
            argument="color_palette",
            reason="expected a nonempty palette name or mapping",
        )
    return deepcopy(obj)


def digest_structure_index(obj):
    if (
        isinstance(obj, (bool, np.bool_))
        or not isinstance(obj, (int, np.integer))
        or obj < 0
    ):
        raise ArgumentError(
            argument="structure_index", reason="expected a nonnegative integer"
        )
    return int(obj)


def digest_point_tolerance(obj):
    return _length(obj, "point_tolerance")


def digest_direction_tolerance(obj):
    try:
        quantity = puw.ensure_quantity(obj, dimensionality={})
        value = np.asarray(puw.get_value(quantity, to_unit="degrees"), dtype=float)
    except Exception as error:
        raise ArgumentError(
            argument="direction_tolerance", reason="expected an explicit angle quantity"
        ) from error
    if value.shape != () or not np.isfinite(value) or not 0 <= value <= 180:
        raise ArgumentError(
            argument="direction_tolerance",
            reason="expected an angle in [0, 180] degrees",
        )
    return quantity


def _fraction(obj, name):
    if isinstance(obj, (bool, np.bool_)) or not np.isscalar(obj):
        raise ArgumentError(argument=name, reason="expected a fraction in [0, 1]")
    try:
        value = float(obj)
    except (TypeError, ValueError) as error:
        raise ArgumentError(
            argument=name, reason="expected a fraction in [0, 1]"
        ) from error
    if not np.isfinite(value) or not 0 <= value <= 1:
        raise ArgumentError(argument=name, reason="expected a fraction in [0, 1]")
    return value


def digest_min_fit_value(obj):
    return _fraction(obj, "min_fit_value")


def digest_min_match_ratio(obj):
    return _fraction(obj, "min_match_ratio")


def digest_chemical_state(obj):
    if obj is None or (isinstance(obj, str) and obj in {"reference", "structure"}):
        return obj
    return digest_structure_index(obj)


def digest_on_error(obj):
    if not isinstance(obj, str) or obj not in {"raise", "record"}:
        raise ArgumentError(argument="on_error", reason="expected 'raise' or 'record'")
    return obj


def digest_pose_id(obj):
    if obj is None or isinstance(obj, str):
        return obj
    if isinstance(obj, (int, np.integer)) and not isinstance(obj, (bool, np.bool_)):
        return int(obj)
    raise ArgumentError(argument="pose_id", reason="expected a string, integer or None")


def digest_molecular_database(obj):
    if isinstance(obj, (str, bytes)):
        raise ArgumentError(
            argument="molecular_database",
            reason="expected an iterable of molecular systems",
        )
    try:
        iter(obj)
    except TypeError as error:
        raise ArgumentError(
            argument="molecular_database",
            reason="expected an iterable of molecular systems",
        ) from error
    return obj  # Preserve the iterable; materialization belongs to the batch.


def digest_actives(obj):
    return digest_molecular_database(obj)


def digest_decoys(obj):
    return digest_molecular_database(obj)


def digest_bedroc_alpha(obj):
    return digest_alpha(obj)


def digest_ef_fractions(obj):
    return tuple(digest_fraction(value) for value in obj)


def digest_evaluator(obj):
    from pharmacophoremt.screening.conformer_screening import ConformerScreening
    from pharmacophoremt.screening.pose_evaluation import PoseEvaluator
    from pharmacophoremt.screening.rigid_search import RigidPoseSearch

    if obj is not None and not isinstance(
        obj, (PoseEvaluator, RigidPoseSearch, ConformerScreening)
    ):
        raise ArgumentError(
            argument="evaluator",
            reason="expected a native pose evaluator/search or None",
        )
    return obj


def digest_enabled(obj):
    if not isinstance(obj, (bool, np.bool_)):
        raise ArgumentError(argument="enabled", reason="expected a boolean")
    return bool(obj)


def digest_distance_tolerance(obj):
    return _length(obj, "distance_tolerance")


def digest_reference_index(obj):
    return digest_structure_index(obj)


def digest_min_support(obj):
    if (
        isinstance(obj, (bool, np.bool_))
        or not isinstance(obj, (int, np.integer))
        or obj < 1
    ):
        raise ArgumentError(
            argument="min_support", reason="expected a positive integer"
        )
    return int(obj)


def _positive_integer(obj, argument):
    if (
        isinstance(obj, (bool, np.bool_))
        or not isinstance(obj, (int, np.integer))
        or obj < 1
    ):
        raise ArgumentError(argument=argument, reason="expected a positive integer")
    return int(obj)


def digest_min_sites(obj):
    return _positive_integer(obj, "min_sites")


def digest_max_graph_nodes(obj):
    return _positive_integer(obj, "max_graph_nodes")


def digest_max_cliques(obj):
    return _positive_integer(obj, "max_cliques")


def digest_max_combinations(obj):
    return _positive_integer(obj, "max_combinations")


def digest_correspondence_strategy(obj):
    if not isinstance(obj, str) or obj not in {
        "association_cliques",
        "triplet_seeds",
        "ranked_triplet_seeds",
    }:
        raise ArgumentError(
            argument="correspondence_strategy",
            reason="expected association_cliques, triplet_seeds or ranked_triplet_seeds",
        )
    return obj


def digest_n_seeds(obj):
    return None if obj is None else _positive_integer(obj, "n_seeds")


def digest_orientation_policy(obj):
    if not isinstance(obj, str) or obj not in {"final", "each_step"}:
        raise ArgumentError(
            argument="orientation_policy", reason="expected final or each_step"
        )
    return obj


def digest_refinement_strategy(obj):
    if obj is not None and (not isinstance(obj, str) or obj != "greedy"):
        raise ArgumentError(
            argument="refinement_strategy", reason="expected None or greedy"
        )
    return obj


def digest_feature_pairs(obj):
    values = np.asarray(obj)
    if values.size == 0 and values.shape == (0,):
        return np.empty((0, 2), dtype=np.int64)
    if (
        values.ndim != 2
        or values.shape[1] != 2
        or values.dtype.kind not in "iu"
        or np.any(values < 0)
        or len(set(values[:, 0])) != len(values)
        or len(set(values[:, 1])) != len(values)
    ):
        raise ArgumentError(
            argument="feature_pairs",
            reason="expected injective nonnegative integer [reference, source] pairs",
        )
    return values.astype(np.int64)


def digest_feature_pair_dissimilarities(obj):
    required = {
        "method",
        "complete",
        "n_reference",
        "n_candidate",
        "costs",
        "compatible",
        "criteria",
    }
    if (
        not isinstance(obj, dict)
        or not required <= obj.keys()
        or obj["method"] != "typed_neighborhood_assignment@1"
        or obj["complete"] is not True
    ):
        raise ArgumentError(
            argument="feature_pair_dissimilarities",
            reason="expected a complete native neighborhood comparison",
        )
    for key in ("n_reference", "n_candidate"):
        if (
            isinstance(obj[key], (bool, np.bool_))
            or not isinstance(obj[key], (int, np.integer))
            or obj[key] < 0
        ):
            raise ArgumentError(
                argument="feature_pair_dissimilarities",
                reason="expected nonnegative axis sizes",
            )
    shape = (obj["n_reference"], obj["n_candidate"])
    try:
        costs = np.asarray(obj["costs"], dtype=float)
        mask = np.asarray(obj["compatible"])
        if shape[0] == 0 and costs.shape == mask.shape == (0,):
            costs = costs.reshape(shape)
            mask = mask.reshape(shape)
        valid = (
            costs.shape == mask.shape == shape
            and np.all(np.isfinite(costs))
            and np.all((costs >= 0) & (costs <= 1))
            and all(isinstance(value, (bool, np.bool_)) for value in mask.flat)
            and isinstance(obj["criteria"], dict)
        )
    except (TypeError, ValueError):
        valid = False
    if not valid:
        raise ArgumentError(
            argument="feature_pair_dissimilarities",
            reason="expected finite unit-interval costs and boolean mask on the declared axes",
        )
    return obj


def digest_min_matches(obj):
    value = _positive_integer(obj, "min_matches")
    if value < 3:
        raise ArgumentError(
            argument="min_matches", reason="require at least three matched centers"
        )
    return value


def digest_max_fits(obj):
    return _positive_integer(obj, "max_fits")


def digest_max_layouts(obj):
    return _positive_integer(obj, "max_layouts")


def digest_max_matrix_entries(obj):
    if (
        isinstance(obj, (bool, np.bool_))
        or not isinstance(obj, (int, np.integer))
        or obj < 1
    ):
        raise ArgumentError(
            argument="max_matrix_entries", reason="expected a positive integer"
        )
    return int(obj)


def digest_ligand_ids(obj):
    if (
        not isinstance(obj, (list, tuple))
        or not obj
        or any(not isinstance(value, str) or not value for value in obj)
        or len(set(obj)) != len(obj)
    ):
        raise ArgumentError(
            argument="ligand_ids",
            reason="expected unique nonempty ligand identity strings",
        )
    return list(obj)


def digest_ligands(obj):
    required = {"ligand_id", "molecular_system"}
    allowed = required | {"selection", "structure_index", "chemical_state"}
    if (
        not isinstance(obj, (list, tuple))
        or len(obj) < 2
        or any(
            not isinstance(entry, dict)
            or not required <= entry.keys()
            or not entry.keys() <= allowed
            for entry in obj
        )
    ):
        raise ArgumentError(
            argument="ligands",
            reason="provide at least two ligand_id/molecular_system records with optional selection, structure_index and chemical_state",
        )
    digest_ligand_ids([entry["ligand_id"] for entry in obj])
    return list(obj)


def digest_reference_inventory(obj):
    return digest_feature_inventory(obj)


def digest_feature_inventories(obj):
    if not isinstance(obj, (list, tuple)) or not obj:
        raise ArgumentError(
            argument="feature_inventories",
            reason="expected a nonempty sequence of native inventories",
        )
    return list(obj)


def digest_correspondence_groups(obj):
    if not isinstance(obj, (list, tuple)):
        raise ArgumentError(
            argument="correspondence_groups",
            reason="expected a sequence of feature correspondence groups",
        )
    groups = []
    for group in obj:
        values = np.asarray(group)
        if (
            values.ndim != 2
            or values.shape[1] != 2
            or not len(values)
            or values.dtype.kind not in "iu"
            or np.any(values < 0)
        ):
            raise ArgumentError(
                argument="correspondence_groups",
                reason="each group requires nonnegative integer [inventory, feature] pairs",
            )
        groups.append(values.tolist())
    return groups


def digest_attribution_data(obj):
    if obj is not None and not isinstance(obj, dict):
        raise ArgumentError(
            argument="attribution_data", reason="expected a dictionary or None"
        )
    return obj


def digest_format(obj):
    if not isinstance(obj, str) or not obj:
        raise ArgumentError(argument="format", reason="expected a report format name")
    return obj  # Ackredit owns the format registry, including third-party formats.


def digest_structure_indices(obj):
    if isinstance(obj, str) and obj == "all":
        return obj
    try:
        values = np.asarray(obj)
    except (TypeError, ValueError) as error:
        raise ArgumentError(
            argument="structure_indices", reason="expected a flat integer sequence"
        ) from error
    if (
        values.ndim != 1
        or not values.size
        or values.dtype.kind not in "iu"
        or np.any(values < 0)
        or len(np.unique(values)) != len(values)
    ):
        raise ArgumentError(
            argument="structure_indices",
            reason="expected 'all' or a nonempty sequence of unique nonnegative integers",
        )
    return values.tolist()


def digest_interactions(obj):
    from pharmacophoremt._private.molsysmt import capability

    if not isinstance(obj, capability("Interactions")):
        raise ArgumentError(
            argument="interactions", reason="expected native MolSysMT interactions"
        )
    return obj


def digest_max_trials(obj):
    if (
        isinstance(obj, (bool, np.bool_))
        or not isinstance(obj, (int, np.integer))
        or obj <= 0
    ):
        raise ArgumentError(argument="max_trials", reason="expected a positive integer")
    return int(obj)


def digest_correspondence(obj):
    values = np.asarray(obj)
    if (
        values.ndim != 2
        or values.shape[1] != 2
        or len(values) < 3
        or values.dtype.kind not in "iu"
        or np.any(values < 0)
    ):
        raise ArgumentError(
            argument="correspondence",
            reason="expected at least three nonnegative integer (site, feature) pairs",
        )
    return values.astype(np.int64)


def digest_correspondences(obj):
    if not isinstance(obj, (list, tuple)):
        raise ArgumentError(
            argument="correspondences", reason="expected a sequence of mappings"
        )
    mappings = [digest_correspondence(mapping) for mapping in obj]
    for mapping in mappings:
        if len(set(mapping[:, 0])) != len(mapping) or len(set(mapping[:, 1])) != len(
            mapping
        ):
            raise ArgumentError(
                argument="correspondences",
                reason="each mapping requires unique reference and source indices",
            )
    return mappings


def digest_consensus_report(obj):
    required = {
        "method",
        "complete",
        "criteria",
        "sources",
        "source_alignments",
        "layouts",
        "n_fits",
        "n_layouts",
    }
    if (
        not isinstance(obj, dict)
        or not required <= obj.keys()
        or obj["method"] != "pivot_rigid_clique_consensus@1"
        or obj["complete"] is not True
    ):
        raise ArgumentError(
            argument="consensus_report",
            reason="expected a complete native rigid consensus report",
        )
    if (
        not isinstance(obj["criteria"], dict)
        or "reference_index" not in obj["criteria"]
        or any(
            not isinstance(obj[key], list)
            for key in ("sources", "source_alignments", "layouts")
        )
    ):
        raise ArgumentError(
            argument="consensus_report", reason="invalid report axes or criteria"
        )
    if not obj["sources"] or len(obj["sources"]) != len(obj["source_alignments"]):
        raise ArgumentError(
            argument="consensus_report",
            reason="expected one placement report per input source",
        )
    digest_reference_index(obj["criteria"]["reference_index"])
    for key in ("n_fits", "n_layouts"):
        if (
            isinstance(obj[key], (bool, np.bool_))
            or not isinstance(obj[key], (int, np.integer))
            or obj[key] < 0
        ):
            raise ArgumentError(
                argument="consensus_report",
                reason="expected nonnegative integer fit/layout counts",
            )
    return obj


def digest_feature_inventory(obj):
    from pharmacophoremt.modeler.features import CLASSICAL_FEATURES, DEFINITION

    if obj is None:
        return None  # Alignment may request extraction itself.
    required = {
        "definition",
        "features",
        "selected_atom_indices",
        "structure_index",
        "chemical_state",
        "recognition",
    }
    if (
        not isinstance(obj, dict)
        or not required <= obj.keys()
        or obj["definition"] != DEFINITION
    ):
        raise ArgumentError(
            argument="feature_inventory",
            reason="expected the supported modeler.get_features result",
        )
    if not isinstance(obj["features"], list) or not isinstance(
        obj["recognition"], dict
    ):
        raise ArgumentError(
            argument="feature_inventory",
            reason="expected feature records and recognition metadata",
        )
    digest_structure_index(obj["structure_index"])
    digest_chemical_state(obj["chemical_state"])
    indices = np.asarray(obj["selected_atom_indices"])
    if (
        indices.ndim != 1
        or not indices.size
        or indices.dtype.kind not in "iu"
        or np.any(indices < 0)
    ):
        raise ArgumentError(
            argument="feature_inventory",
            reason="expected nonnegative selected atom indices",
        )
    for record in obj["features"]:
        if (
            not isinstance(record, dict)
            or not {"kind", "center", "atom_indices"} <= record.keys()
            or record["kind"] not in set(CLASSICAL_FEATURES) | {"included volume"}
        ):
            raise ArgumentError(
                argument="feature_inventory",
                reason="expected recognized chemical records",
            )
        digest_center(record["center"])
        atoms = np.asarray(record["atom_indices"])
        if (
            atoms.ndim != 1
            or not atoms.size
            or atoms.dtype.kind not in "iu"
            or not np.isin(atoms, indices).all()
        ):
            raise ArgumentError(
                argument="feature_inventory",
                reason="feature participants must lie in the source selection",
            )
    return obj
