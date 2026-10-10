"""
Leave-One-Out (LOO) cross-validation for ligand-based pharmacophore models.
"""

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._private.arg_digestion.argument._contracts import digest_evaluator
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)


class LeaveOneOutValidator:
    """Leave-One-Out cross-validation for LigandBasedModeler.

    For each active ligand i, the pharmacophore is built from all other actives
    and an explicit evaluator factory constructs its prepared-native screener. The
    fraction of actives successfully retrieved (LOO recall) measures the model's
    self-consistency.

    LigandBasedModeler requires prepared inputs and an explicit consensus_method.
    This validator selects the first native hypothesis; it does not rank
    hypotheses by affinity. At least three inputs are needed when
    the chosen modeler requires two training ligands.

    Parameters
    ----------
    modeler_class : type
        The modeler class to instantiate (must accept a list of molecular systems
        as first argument, e.g. LigandBasedModeler).
    modeler_kwargs : dict, optional
        Extra keyword arguments forwarded to the modeler constructor.
    min_match_ratio : float, optional
        Inert historical default 1.0; other values are refused.
    evaluator_factory : callable
        Required factory called with each selected query. Return a native
        evaluator/search whose run() returns all per-input records, not a hit list.

    Examples
    --------
    >>> from pharmacophoremt.modeler.ligand_based import LigandBasedModeler
    >>> from pharmacophoremt.screening import RigidPoseSearch
    >>> loo = LeaveOneOutValidator(
    ...     LigandBasedModeler, {'n_points': 4, 'consensus_method': 'rigid'},
    ...     evaluator_factory=RigidPoseSearch)
    >>> report = loo.run(active_molecules)
    >>> print(f"LOO recall: {report['loo_recall']:.2f}")
    """

    def __init__(
        self,
        modeler_class,
        modeler_kwargs=None,
        min_match_ratio=1.0,
        *,
        evaluator_factory=None,
    ):
        if type(min_match_ratio) not in (int, float) or min_match_ratio != 1:
            raise ArgumentError(
                argument="min_match_ratio",
                reason="only the inert default is supported; the native evaluator owns hit criteria",
            )
        if not callable(evaluator_factory):
            raise ArgumentError(
                argument="evaluator_factory",
                reason="supply an explicit factory for a prepared-native evaluator/search",
            )
        self.modeler_class = modeler_class
        self.modeler_kwargs = modeler_kwargs or {}
        self.evaluator_factory = evaluator_factory

    @signal(tags=["validation", "loo", "run"])
    @arg_digest(type_check=True)
    def run(self, molecules, skip_digestion=False, **evaluation_options):
        """Run LOO cross-validation.

        Parameters
        ----------
        molecules : list
            Prepared active molecules supported by the chosen modeler/evaluator.

        Returns
        -------
        dict
            'loo_recall' : fraction of actives retrieved across all LOO rounds,
            'n_molecules' : total number of molecules,
            'n_retrieved' : number of molecules that were retrieved,
            'rounds' : list of per-round results (pharmacophore, hit bool,
                       fit_value or None).
        """
        n = len(molecules)
        if n < 2:
            raise ValueError("LOO requires at least 2 molecules.")

        rounds = []
        n_retrieved = 0

        for i in range(n):
            train = [molecules[j] for j in range(n) if j != i]
            test_mol = molecules[i]

            # Build pharmacophore from training set
            modeler = self.modeler_class(train, **self.modeler_kwargs)
            hypotheses = modeler.build()

            # Select the first returned hypothesis (native order is not affinity).
            if not hypotheses:
                rounds.append(
                    {
                        "held_out_idx": i,
                        "hit": False,
                        "fit_value": None,
                        "pharmacophore": None,
                    }
                )
                continue

            best_ph = hypotheses[0] if isinstance(hypotheses, list) else hypotheses

            # Screen the held-out molecule
            screener = digest_evaluator(self.evaluator_factory(best_ph))
            if screener is None:
                raise ArgumentError(
                    argument="evaluator_factory", reason="factory result requires run()"
                )
            evaluation = screener.run([test_mol], **evaluation_options)[0]
            # Native run() includes negatives; length is never a hit criterion.
            hit = evaluation["status"] == "matched"
            fit = evaluation["fit_value"]
            if evaluation["status"] == "failed":
                raise PoseEvaluationError(
                    pose_id=i,
                    stage=evaluation["error"].get("stage", "screening"),
                    reason=evaluation["error"]["message"],
                )

            if hit:
                n_retrieved += 1

            rounds.append(
                {
                    "held_out_idx": i,
                    "hit": hit,
                    "fit_value": fit,
                    "pharmacophore": best_ph,
                    "evaluation": evaluation,
                }
            )

        return {
            "loo_recall": n_retrieved / n,
            "n_molecules": n,
            "n_retrieved": n_retrieved,
            "rounds": rounds,
        }
