"""Bounded rigid search built from reusable native pharmacophoric tools."""

from copy import deepcopy

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.pose_batch import run_evaluations
from pharmacophoremt._private.smonitor.exceptions import (
    PoseEvaluationError,
    SearchLimitError,
)
from pharmacophoremt.modeler.features import get_features
from pharmacophoremt.pharmacophore import Pharmacophore
from pharmacophoremt.screening.alignment import align_to_pharmacophore
from pharmacophoremt.screening.correspondence import (
    _essential_anchors,
    get_correspondences,
)
from pharmacophoremt.screening.pose_evaluation import PoseEvaluator


class RigidPoseSearch:
    """Find a placed rigid ligand pose from essential-center triplet seeds.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        Query with at least three essential non-collinear centers.
    max_trials : int, default=10000
        Maximum raw candidate triplet products visited before truncation.
    point_tolerance : length quantity, default='0.10 nm'
        Point-site tolerance, shared with correspondence and pose evaluation.
    direction_tolerance : angle quantity, default='30 degrees'
        Donor-H and aromatic-axis tolerance used after alignment.
    min_fit_value : float, default=0.0
        Minimum weighted coverage for a hit.

    Notes
    -----
    The method is rigid_triplet_fit@1: proposed center fits are checked by
    PoseEvaluator, including all essential sites and exclusions. It does not
    guarantee exhaustive continuous tolerance solutions or generate conformers.
    A budget-exhausted search raises unless a valid unit-fit hit establishes the
    maximum possible coverage. A complete valid negative is reported explicitly.
    Molecular inputs are never modified. Returned results are portable; the best
    alignment retains fitted coordinates and can be reproduced with the public
    alignment tool. Recognition and provider failures retain their cause.

    Examples
    --------
    >>> search = RigidPoseSearch(query, max_trials=10000)
    >>> result = search.evaluate(prepared_ligand)
    """

    @signal(tags=["screening", "rigid_search", "init"])
    @arg_digest()
    def __init__(
        self,
        pharmacophore,
        *,
        max_trials=10000,
        point_tolerance="0.10 nm",
        direction_tolerance="30 degrees",
        min_fit_value=0.0,
    ):
        self.evaluator = PoseEvaluator(
            pharmacophore,
            point_tolerance=point_tolerance,
            direction_tolerance=direction_tolerance,
            min_fit_value=min_fit_value,
        )
        self.pharmacophore = Pharmacophore()
        self.pharmacophore.interaction_sites = deepcopy(self.evaluator.sites)
        self.pharmacophore.n_interaction_sites = len(self.evaluator.sites)
        self.pharmacophore.metadata = deepcopy(self.evaluator.model_metadata)
        self.max_trials = max_trials
        self.point_tolerance = point_tolerance
        _essential_anchors(self.evaluator)

    @signal(tags=["screening", "rigid_search", "evaluate"])
    @arg_digest()
    @attributed()
    def evaluate(
        self,
        molecular_system,
        *,
        selection="all",
        structure_index=0,
        chemical_state="reference",
        pose_id=None,
    ):
        """Return the best checked coverage, alignment and search evidence.

        A valid unit-fit hit stops the search because coverage cannot exceed one.
        Equal results retain the earliest seed deterministically. A matched pose
        ranks ahead of any non-hit, then coverage ranks poses within that status.
        Incomplete search and
        provider failures raise PoseEvaluationError retaining the original cause.
        """
        stage = "recognition"
        try:
            options = dict(
                selection=selection,
                structure_index=structure_index,
                chemical_state=chemical_state,
            )
            requested = sorted(
                {kind for _, site in self.evaluator.query for kind in site.features}
            )
            inventory = get_features(molecular_system, features=requested, **options)
            stage = "correspondence"
            proposals = get_correspondences(
                self.pharmacophore,
                inventory,
                point_tolerance=self.point_tolerance,
                max_trials=self.max_trials,
            )
            # Identity placement is also a candidate; zero fitted seeds should
            # still retain provider recognition and a fully evaluated result.
            stage = "matching"
            best = self.evaluator.evaluate(molecular_system, pose_id=pose_id, **options)
            best_alignment, n_fitted = None, 0
            optimal = best["status"] == "matched" and best["fit_value"] == 1
            for correspondence in proposals["correspondences"]:
                if optimal:
                    break
                stage = "alignment"
                aligned = align_to_pharmacophore(
                    molecular_system,
                    self.pharmacophore,
                    correspondence,
                    feature_inventory=inventory,
                    **options,
                )
                n_fitted += 1
                stage = "matching"
                result = self.evaluator.evaluate(
                    aligned["molecular_system"], pose_id=pose_id, **options
                )
                # Preserve the existence of a valid hit even if an inadmissible
                # pose covers more optional sites but violates an exclusion.
                if (result["status"] == "matched", result["fit_value"]) > (
                    best["status"] == "matched",
                    best["fit_value"],
                ):
                    best, best_alignment = result, aligned["alignment"]
                optimal = best["status"] == "matched" and best["fit_value"] == 1
            if not proposals["complete"] and not optimal:
                stage = "search_budget"
                raise SearchLimitError(
                    max_trials=self.max_trials, n_trials=proposals["n_trials"]
                )
        except PoseEvaluationError:
            raise
        except Exception as error:
            raise PoseEvaluationError(
                pose_id=pose_id, stage=stage, reason=str(error)
            ) from error
        return dict(
            best,
            alignment=best_alignment,
            search=dict(
                method="rigid_triplet_fit@1",
                max_trials=self.max_trials,
                n_trials=proposals["n_trials"],
                n_pruned=proposals["n_pruned"],
                n_proposals=len(proposals["correspondences"]),
                n_fitted=n_fitted,
                enumeration_complete=proposals["complete"],
                termination="optimal_fit_found" if optimal else "enumeration_complete",
                identity_pose_tested=True,
            ),
        )

    @signal(tags=["screening", "rigid_search", "batch"])
    @arg_digest()
    def run(self, molecular_database, *, on_error="raise", **evaluation_options):
        """Search each prepared input with stable identity and explicit failures.

        With on_error='record', failures have fit_value=None and keep their cause.
        Otherwise the first failed search raises. One source frame is searched
        per input; repeated objects and generators retain independent indices.
        """
        return run_evaluations(self, molecular_database, on_error, evaluation_options)
