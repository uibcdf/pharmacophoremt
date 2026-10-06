"""Screen prepared conformations without implementing molecular preparation."""

from copy import deepcopy

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.molsysmt import capability, detached
from pharmacophoremt._private.pose_batch import failure_record, run_evaluations
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.screening.rigid_search import RigidPoseSearch


class ConformerScreening:
    """Search every requested prepared frame and retain the best checked pose.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        Query with three or more essential non-collinear centers.
    max_trials : int, default=10000
        Candidate triplet budget per frame, passed to RigidPoseSearch.
    point_tolerance : length quantity, default='0.10 nm'
        Point-site tolerance for the rigid search.
    direction_tolerance : angle quantity, default='30 degrees'
        Donor-H and aromatic-axis tolerance.
    min_fit_value : float, default=0.0
        Minimum weighted coverage for a hit.

    Notes
    -----
    MolSysMT supplies frame identities, coordinates and declared chemical states.
    No conformations, protonation states or torsions are generated. All selected
    frames are attempted; hits rank before negatives, then by coverage. Equal
    results retain the first requested frame. RigidPoseSearch's discrete-method
    restrictions apply independently to each frame.

    Examples
    --------
    >>> screen = ConformerScreening(query)
    >>> result = screen.evaluate(prepared_ligand, chemical_state='structure')
    >>> best_frame = result['best_conformer_index']
    """

    @signal(tags=["screening", "conformers", "init"])
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
        self.search = RigidPoseSearch(
            pharmacophore,
            max_trials=max_trials,
            point_tolerance=point_tolerance,
            direction_tolerance=direction_tolerance,
            min_fit_value=min_fit_value,
        )

    @signal(tags=["screening", "conformers", "evaluate"])
    @arg_digest()
    @attributed()
    def evaluate(
        self,
        molecular_system,
        *,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        pose_id=None,
        on_error="raise",
    ):
        """Return portable per-frame evidence and a definitive molecule score.

        Parameters
        ----------
        molecular_system : molecular system
            Prepared input supported by MolSysMT, left unmodified.
        selection : str or sequence of int, default='all'
            Source atoms selected through MolSysMT.
        structure_indices : 'all' or sequence of int, default='all'
            Unique nonnegative source frames, in deterministic tie order.
        chemical_state : str or int, default='reference'
            MolSysMT state policy. 'structure' resolves each frame separately.
        pose_id : str or int, optional
            Molecule identity; conformer_index is its source frame index.
        on_error : {'raise', 'record'}, default='raise'
            Raise on failure, or retain failed frames and continue.

        Returns
        -------
        dict
            Best pose fields, conformers and ensemble accounting. Unresolved
            coverage has status='failed', fit_value=None and best_observed for
            inspection. A valid unit-fit hit proves maximal coverage even when
            other frames failed; ensemble.complete still reports those failures.
            pose_coordinates seals selected best-pose coordinates with units.

        Examples
        --------
        >>> result = screen.evaluate(prepared_ligand, structure_indices=[2, 0])
        >>> evidence = result['conformers']
        """
        try:
            get = capability("get")
            frames = [
                int(index)
                for index in get(
                    molecular_system,
                    structure_indices=structure_indices,
                    structure_index=True,
                )
            ]
            if not frames:
                raise ArgumentError(
                    argument="molecular_system", reason="no prepared coordinate frames"
                )
        except Exception as error:
            raise PoseEvaluationError(
                pose_id=pose_id, stage="frames", reason=str(error)
            ) from error

        records, best = [], None
        for frame in frames:
            stage = "chemical_state"
            resolved_state = None
            try:
                if chemical_state == "structure":
                    state = get(
                        molecular_system,
                        structure_indices=[frame],
                        structure_chemical_state_index=True,
                    )[0]
                elif chemical_state is None or chemical_state == "reference":
                    state = get(molecular_system, reference_chemical_state_index=True)
                else:
                    # Public state scoping validates the explicit index before
                    # it is reported as resolved, including in failed searches.
                    get(
                        molecular_system,
                        structure_indices=[frame],
                        chemical_state=chemical_state,
                        chemical_state_index=True,
                    )
                    state = chemical_state
                try:
                    resolved_state = int(state)
                except (TypeError, ValueError) as error:
                    # Let the molecular owner explain missing or ambiguous state
                    # associations through a state-dependent public attribute.
                    get(
                        molecular_system,
                        element="atom",
                        structure_indices=[frame],
                        chemical_state=chemical_state,
                        formal_charge=True,
                    )
                    raise ArgumentError(
                        argument="chemical_state",
                        reason="MolSysMT did not resolve a declared state index",
                    ) from error
                stage = "search"
                result = self.search.evaluate(
                    molecular_system,
                    selection=selection,
                    structure_index=frame,
                    chemical_state=chemical_state,
                    pose_id=pose_id,
                )
                stage = "pose_record"
                alignment = result["alignment"]
                coordinates = (
                    alignment["aligned_atom_coordinates"]
                    if alignment is not None
                    else detached(
                        get(
                            molecular_system,
                            element="atom",
                            selection=result["selected_atom_indices"],
                            structure_indices=[frame],
                            coordinates=True,
                        )
                    )
                )
                result = dict(result, pose_coordinates=coordinates)
            except Exception as error:
                if not isinstance(error, PoseEvaluationError):
                    cause = error
                    error = PoseEvaluationError(
                        pose_id=pose_id, stage=stage, reason=str(cause)
                    )
                    error.__cause__ = cause
                if on_error == "raise":
                    raise error
                result = failure_record(error, pose_id)
            record = dict(
                result,
                conformer_index=frame,
                structure_index=frame,
                chemical_state=chemical_state,
                resolved_chemical_state_index=resolved_state,
            )
            records.append(record)
            if record["status"] != "failed" and (
                best is None
                or (record["status"] == "matched", record["fit_value"])
                > (best["status"] == "matched", best["fit_value"])
            ):
                best = record

        failures = [record for record in records if record["status"] == "failed"]
        proven_maximum = (
            best is not None and best["status"] == "matched" and best["fit_value"] == 1
        )
        resolved = best is not None and (not failures or proven_maximum)
        if resolved:
            result = deepcopy(best)
        else:
            # The first failure remains the diagnostic cause; the best partial
            # pose remains evidence, never a score used by retrospective metrics.
            result = deepcopy(failures[0])
            result.pop("conformer_index")
            result.pop("structure_index")
            result.pop("resolved_chemical_state_index")
            result["best_observed"] = deepcopy(best)
        return dict(
            result,
            best_conformer_index=best["conformer_index"] if resolved else None,
            conformers=records,
            ensemble=dict(
                method="prepared_conformer_rigid_search@1",
                structure_indices=frames,
                n_requested=len(frames),
                n_evaluated=len(records) - len(failures),
                n_failed=len(failures),
                complete=not failures,
                score_resolved=resolved,
                proven_maximum=proven_maximum,
                ranking="hit_then_coverage_first_requested_tie",
            ),
        )

    @signal(tags=["screening", "conformers", "batch"])
    @arg_digest()
    def run(self, molecular_database, *, on_error="raise", **evaluation_options):
        """Screen inputs once, preserving molecule IDs and per-frame failures.

        Examples
        --------
        >>> results = screen.run(prepared_library, on_error='record')
        """
        return run_evaluations(
            self,
            molecular_database,
            on_error,
            dict(evaluation_options, on_error=on_error),
        )
