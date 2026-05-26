"""
Leave-One-Out (LOO) cross-validation for ligand-based pharmacophore models.
"""

import numpy as np
from argdigest import arg_digest
from smonitor import signal


class LeaveOneOutValidator:
    """Leave-One-Out cross-validation for LigandBasedModeler.

    For each active ligand i, the pharmacophore is built from all other actives
    and the held-out ligand is tested against it with VirtualScreening. The
    fraction of actives successfully retrieved (LOO recall) measures the model's
    self-consistency.

    Parameters
    ----------
    modeler_class : type
        The modeler class to instantiate (must accept a list of molecular systems
        as first argument, e.g. LigandBasedModeler).
    modeler_kwargs : dict, optional
        Extra keyword arguments forwarded to the modeler constructor.
    min_match_ratio : float, optional
        Minimum match ratio for a hit (default 1.0).

    Examples
    --------
    >>> from pharmacophoremt.modeler.ligand_based import LigandBasedModeler
    >>> loo = LeaveOneOutValidator(LigandBasedModeler, {'n_points': 4})
    >>> report = loo.run(active_molecules)
    >>> print(f"LOO recall: {report['loo_recall']:.2f}")
    """

    def __init__(self, modeler_class, modeler_kwargs=None, min_match_ratio=1.0):
        self.modeler_class = modeler_class
        self.modeler_kwargs = modeler_kwargs or {}
        self.min_match_ratio = min_match_ratio

    @signal(tags=["validation", "loo", "run"])
    @arg_digest(type_check=True)
    def run(self, molecules, skip_digestion=False):
        """Run LOO cross-validation.

        Parameters
        ----------
        molecules : list
            Active molecules (any format accepted by molsysmt / the modeler).

        Returns
        -------
        dict
            'loo_recall' : fraction of actives retrieved across all LOO rounds,
            'n_molecules' : total number of molecules,
            'n_retrieved' : number of molecules that were retrieved,
            'rounds' : list of per-round results (pharmacophore, hit bool,
                       fit_value or None).
        """
        from pharmacophoremt.screening.virtual_screening import VirtualScreening

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

            # Take the top-ranked hypothesis
            if not hypotheses:
                rounds.append({'held_out_idx': i, 'hit': False, 'fit_value': None,
                                'pharmacophore': None})
                continue

            best_ph = hypotheses[0] if isinstance(hypotheses, list) else hypotheses

            # Screen the held-out molecule
            screener = VirtualScreening(best_ph, min_match_ratio=self.min_match_ratio)
            hits = screener.run([test_mol])

            hit = len(hits) > 0
            fit = hits[0]['fit_value'] if hit else None

            if hit:
                n_retrieved += 1

            rounds.append({
                'held_out_idx': i,
                'hit': hit,
                'fit_value': fit,
                'pharmacophore': best_ph,
            })

        return {
            'loo_recall': n_retrieved / n,
            'n_molecules': n,
            'n_retrieved': n_retrieved,
            'rounds': rounds,
        }
