"""Evaluation of placed poses, with chemistry supplied by MolSysMT."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import scipy
from argdigest import arg_digest
from scipy.optimize import linear_sum_assignment
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed, credit_criterion, credit_software
from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_center,
    digest_direction,
    digest_essential,
    digest_features,
    digest_normal,
    digest_radius,
    digest_weight,
)
from pharmacophoremt._private.molsysmt import detached, source_frame
from pharmacophoremt._private.pose_batch import run_evaluations
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.modeler.features import DEFINITION, get_features

_ANGLE_COSINE_SLACK = float(8 * np.finfo(np.float64).eps)


class PoseEvaluator:
    """Assign chemical participants to a pharmacophore in a fixed frame.

    MolSysMT supplies atomic hydrophobic, donor-H/acceptor, aromatic-ring and
    formal-charge-center definitions. Heavy-atom volumes are also supported.
    Point/Sphere sites bound center distance. Donor SphereAndVector sites also
    bound directed donor-H angles. Aromatic Disk sites bound center distance by
    radius and the unoriented plane-axis angle; they do not test point-in-disk
    intersection or infer a physical disk thickness. Other definitions raise.
    Each candidate fills at most one site. All essential sites must be assigned,
    even with zero weight. No alignment or molecular preparation is performed.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        Query model; sites are copied on construction.
    point_tolerance : length quantity, default='0.10 nm'
        Matching radius for Point sites.
    direction_tolerance : angle quantity, default='30 degrees'
        Maximum donor-H angle or unoriented aromatic-plane angle, including coincident centers.
    min_fit_value : float, default=0.0
        Minimum weighted fraction of matched non-exclusion sites, in [0, 1].

    Notes
    -----
    Recognition uses MolSysMT's ``smarts_hydrophobic_atoms`` and
    ``smarts_donor_acceptor`` rules reproducing ProLIF 2.2.2 definitions.
    Aromatic recognition uses stored aromatic bonds and a minimum cycle basis;
    charge centers use declared formal charges and provider-defined membership.
    These definitions are shared with modeler.get_features/from_ligand.
    Fit values express geometric coverage, not affinity.

    Examples
    --------
    Given a query built from MolSysMT observations and an already placed pose:

    >>> evaluator = PoseEvaluator(query, direction_tolerance='30 degrees')
    >>> result = evaluator.evaluate(source, selection='molecule_type == "small molecule"', pose_id='pose-0')
    """

    @signal(tags=["screening", "pose", "init"])
    @arg_digest()
    def __init__(
        self,
        pharmacophore,
        *,
        point_tolerance="0.10 nm",
        direction_tolerance="30 degrees",
        min_fit_value=0.0,
    ):
        from pharmacophoremt.pharmacophore import Pharmacophore

        if not isinstance(pharmacophore, Pharmacophore):
            raise ArgumentError(
                argument="pharmacophore", reason="expected a Pharmacophore"
            )
        self.sites = deepcopy(pharmacophore.interaction_sites)
        self.model_metadata = detached(pharmacophore.metadata)
        self.point_tolerance = float(
            puw.get_value(digest_radius(point_tolerance), to_unit="nm")
        )
        try:
            angle = puw.ensure_quantity(direction_tolerance, dimensionality={})
            self.direction_tolerance = float(puw.get_value(angle, to_unit="degrees"))
        except Exception as error:
            raise ArgumentError(
                argument="direction_tolerance",
                reason="expected an explicit angle quantity",
            ) from error
        if (
            not np.isfinite(self.direction_tolerance)
            or not 0 <= self.direction_tolerance <= 180
        ):
            raise ArgumentError(
                argument="direction_tolerance",
                reason="expected an angle in [0, 180] degrees",
            )
        try:
            self.min_fit_value = float(min_fit_value)
        except (TypeError, ValueError) as error:
            raise ArgumentError(
                argument="min_fit_value", reason="expected a finite fraction in [0, 1]"
            ) from error
        if (
            isinstance(min_fit_value, (bool, np.bool_))
            or not np.isfinite(self.min_fit_value)
            or not 0 <= self.min_fit_value <= 1
        ):
            raise ArgumentError(
                argument="min_fit_value", reason="expected a finite fraction in [0, 1]"
            )
        supported = {
            "hydrophobicity",
            "hb donor",
            "hb acceptor",
            "aromatic ring",
            "positive charge",
            "negative charge",
            "included volume",
            "excluded volume",
        }
        self.query, self.exclusions = [], []
        for index, site in enumerate(self.sites):
            site.features = digest_features(site.features)
            site.weight = digest_weight(site.weight)
            site.essential = digest_essential(site.essential)
            if not site.features or not set(site.features) <= supported:
                raise ArgumentError(
                    argument="pharmacophore",
                    reason=f"unsupported feature at site {index}",
                )
            if site.shape_name not in {"point", "sphere", "sphere and vector", "disk"}:
                raise ArgumentError(
                    argument="pharmacophore",
                    reason=f"unsupported shape at site {index}",
                )
            if site.shape_name == "point":
                site.shape.position = digest_center(site.shape.position)
            else:
                site.shape.center = digest_center(site.center)
                site.shape.radius = digest_radius(site.radius)
            if site.shape_name == "sphere and vector":
                site.shape.direction = puw.quantity(
                    digest_direction(site.direction), "dimensionless"
                )
            if site.shape_name == "sphere and vector" and site.features != ["hb donor"]:
                raise ArgumentError(
                    argument="pharmacophore",
                    reason="directed sites require a donor-H feature",
                )
            if site.shape_name == "disk":
                if site.features != ["aromatic ring"]:
                    raise ArgumentError(
                        argument="pharmacophore",
                        reason="disks require an aromatic-ring feature",
                    )
                site.shape.normal = puw.quantity(
                    digest_normal(site.shape.normal), "dimensionless"
                )
            if "excluded volume" in site.features:
                if site.features != ["excluded volume"] or site.shape_name != "sphere":
                    raise ArgumentError(
                        argument="pharmacophore",
                        reason="excluded volumes require a standalone sphere",
                    )
                self.exclusions.append((index, site))
            else:
                self.query.append((index, site))
        self.total_weight = sum(site.weight for _, site in self.query)
        if (
            not self.query
            or not np.isfinite(self.total_weight)
            or self.total_weight <= 0
        ):
            raise ArgumentError(
                argument="pharmacophore",
                reason="expected matching sites with positive total weight",
            )

    def _inventory(self, system, coordinates, indices, structure_index, chemical_state):
        requested = {feature for _, site in self.query for feature in site.features}
        if self.exclusions:
            requested.add("included volume")
        inventory = get_features(
            system,
            selection=indices,
            structure_index=structure_index,
            chemical_state=chemical_state,
            features=sorted(requested),
        )
        records = inventory["features"]
        heavy = np.asarray(
            [
                record["atom_indices"][0]
                for record in records
                if record["kind"] == "included volume"
            ],
            dtype=np.int64,
        )
        features = []
        for record in records:
            if record["kind"] == "included volume" and not any(
                "included volume" in site.features for _, site in self.query
            ):
                continue
            feature = dict(record)
            feature["center"] = puw.get_value(record["center"], to_unit="nm")
            for key in ("direction", "normal"):
                if record[key] is not None:
                    feature[key] = puw.get_value(record[key], to_unit="dimensionless")
            features.append(feature)
        return features, inventory["recognition"], heavy

    def _match(self, features, coordinates, heavy):
        clashes = []
        for index, site in self.exclusions:
            center = puw.get_value(site.center, to_unit="nm")
            radius = float(puw.get_value(site.radius, to_unit="nm"))
            for atom in heavy[
                np.linalg.norm(coordinates[heavy] - center, axis=1) < radius
            ]:
                clashes.append(dict(site_index=index, atom_index=int(atom)))
        # Dummy columns keep every row feasible. Normalize weights to bound the
        # objective; essential bonuses dominate all optional weights together.
        benefit = np.full((len(self.query), len(features) + len(self.query)), -1.0)
        benefit[:, len(features) :] = 0
        distances = {}
        for row, (_, site) in enumerate(self.query):
            center = site.center if site.center is not None else site.shape.position
            center = np.asarray(puw.get_value(center, to_unit="nm"))
            radius = (
                float(puw.get_value(site.radius, to_unit="nm"))
                if site.radius is not None
                else self.point_tolerance
            )
            for column, feature in enumerate(features):
                if feature["kind"] not in site.features:
                    continue
                distance = float(np.linalg.norm(feature["center"] - center))
                if distance > radius:
                    continue
                if site.shape_name == "sphere and vector":
                    direction = np.asarray(
                        puw.get_value(site.direction, to_unit="dimensionless")
                    )
                    cosine = np.clip(np.dot(direction, feature["direction"]), -1, 1)
                    if cosine + _ANGLE_COSINE_SLACK < np.cos(
                        np.deg2rad(self.direction_tolerance)
                    ):
                        continue
                if site.shape_name == "disk":
                    normal = puw.get_value(site.shape.normal, to_unit="dimensionless")
                    cosine = np.clip(abs(np.dot(normal, feature["normal"])), 0, 1)
                    if cosine + _ANGLE_COSINE_SLACK < np.cos(
                        np.deg2rad(self.direction_tolerance)
                    ):
                        continue
                benefit[row, column] = site.weight / self.total_weight + (
                    2 if site.essential else 0
                )
                distances[row, column] = distance
        rows, columns = linear_sum_assignment(benefit, maximize=True)
        credit_software("scipy", "pharmacophoremt.screening.PoseEvaluator.assignment")
        credit_criterion(
            "assignment", "pharmacophoremt.screening.PoseEvaluator.assignment"
        )
        assignments, matched, weight = [], set(), 0.0
        for row, column in zip(rows, columns):
            if (row, column) not in distances:
                continue
            index, site = self.query[row]
            feature = features[column]
            matched.add(index)
            weight += site.weight
            assignments.append(
                dict(
                    site_index=index,
                    feature=feature["kind"],
                    atom_indices=list(feature["atom_indices"]),
                    distance=puw.QuantityRecord.from_quantity(
                        puw.quantity(distances[row, column], "nm"),
                        field="distance",
                        unit="nm",
                    ).to_dict(),
                )
            )
        missing = [
            index
            for index, site in self.query
            if site.essential and index not in matched
        ]
        fit = weight / self.total_weight
        hit = (
            bool(assignments)
            and not missing
            and not clashes
            and fit >= self.min_fit_value
        )
        return dict(
            status="matched" if hit else "not_matched",
            fit_value=fit,
            assignments=assignments,
            missing_essential_sites=missing,
            excluded_volume_clashes=clashes,
        )

    @signal(tags=["screening", "pose", "evaluate"])
    @arg_digest()
    @attributed("numpy", "pyunitwizard")
    def evaluate(
        self,
        molecular_system,
        *,
        selection="all",
        structure_index=0,
        chemical_state="reference",
        pose_id=None,
    ):
        """Return geometric assignments and detached provenance for one pose.

        Selection and frame indices are resolved by MolSysMT. Failed source,
        recognition or matching calculations raise PoseEvaluationError retaining
        their cause. A valid negative returns ``status='not_matched'``. Distances
        carry explicit units as QuantityRecords. Recognition metadata retains
        the provider's executed versions and detached bibliography.
        """
        stage = "source"
        try:
            coordinates, indices = source_frame(
                molecular_system,
                selection,
                structure_index,
                chemical_state=chemical_state,
            )
            stage = "recognition"
            features, recognition, heavy = self._inventory(
                molecular_system, coordinates, indices, structure_index, chemical_state
            )
            stage = "matching"
            result = self._match(features, coordinates, heavy)
        except Exception as error:
            raise PoseEvaluationError(
                pose_id=pose_id, stage=stage, reason=str(error)
            ) from error
        from pharmacophoremt._version import __version__

        return dict(
            result,
            pose_id=pose_id,
            structure_index=int(structure_index),
            selected_atom_indices=indices.tolist(),
            chemical_state=detached(chemical_state),
            recognition=recognition,
            model_metadata=deepcopy(self.model_metadata),
            software={"pharmacophoremt": __version__, "molsysmt": msm.__version__},
            execution=dict(
                matching_method="essential_then_weighted_one_to_one@1",
                backend="numpy_scipy_cpu",
                numpy=np.__version__,
                scipy=scipy.__version__,
                precision="float64",
            ),
            criteria=dict(
                feature_definition=DEFINITION,
                point_tolerance=puw.QuantityRecord.from_quantity(
                    puw.quantity(self.point_tolerance, "nm"),
                    field="point_tolerance",
                    unit="nm",
                ).to_dict(),
                direction_tolerance=puw.QuantityRecord.from_quantity(
                    puw.quantity(self.direction_tolerance, "degrees"),
                    field="direction_tolerance",
                    unit="degrees",
                ).to_dict(),
                angle_comparison_cosine_slack=_ANGLE_COSINE_SLACK,
                min_fit_value=self.min_fit_value,
                assignment="one_to_one",
                aromatic_normal="unoriented_axis",
                aromatic_disk_position="center_distance_within_radius",
                essential="all",
                excluded_volume_boundary="strictly_inside",
            ),
        )

    @signal(tags=["screening", "pose", "batch"])
    @arg_digest()
    def run(self, molecular_database, *, on_error="raise", **evaluation_options):
        """Evaluate each input once, retaining its zero-based ``input_index``.

        With ``on_error='record'``, failures retain their cause and have no fit
        value. Pose IDs are input indices. One frame per input is evaluated.
        """
        return run_evaluations(self, molecular_database, on_error, evaluation_options)
