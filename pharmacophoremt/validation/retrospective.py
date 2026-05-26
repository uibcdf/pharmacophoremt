"""
Retrospective validation of pharmacophore models using labeled datasets.
"""

import numpy as np
from argdigest import arg_digest
from smonitor import signal
from pharmacophoremt.screening.virtual_screening import VirtualScreening
from pharmacophoremt.validation.metrics import enrichment_factor, roc_auc, bedroc


class RetrospectiveValidator:
    """Validate a pharmacophore model on a labeled dataset.

    The dataset is a list of (molecule, label) pairs where label is 1 (active)
    or 0 (decoy). VirtualScreening is run and the resulting Fit Values are used
    to compute enrichment metrics.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        The pharmacophore to validate.
    min_match_ratio : float, optional
        Passed to VirtualScreening (default 1.0).

    Examples
    --------
    >>> val = RetrospectiveValidator(pharmacophore)
    >>> report = val.run(actives, decoys)
    >>> print(report['EF@1%'], report['BEDROC'])
    """

    def __init__(self, pharmacophore, min_match_ratio=1.0):
        self.pharmacophore = pharmacophore
        self.min_match_ratio = min_match_ratio
        self._screener = VirtualScreening(pharmacophore, min_match_ratio=min_match_ratio)

    @signal(tags=["validation", "retrospective", "run"])
    @arg_digest(type_check=True)
    def run(self, actives, decoys, ef_fractions=(0.01, 0.05, 0.10),
            bedroc_alpha=20.0, skip_digestion=False):
        """Run retrospective screening and compute validation metrics.

        Parameters
        ----------
        actives : list
            Active molecules (any format accepted by molsysmt).
        decoys : list
            Decoy molecules.
        ef_fractions : tuple of float, optional
            Database fractions for EF computation (default (0.01, 0.05, 0.10)).
        bedroc_alpha : float, optional
            Alpha parameter for BEDROC (default 20.0).

        Returns
        -------
        dict
            Keys: 'AUC', 'BEDROC', 'EF@1%', 'EF@5%', 'EF@10%' (and any other
            fractions requested), plus 'n_actives', 'n_decoys',
            'n_actives_found', 'scores', 'labels'.
        """
        all_mols = list(actives) + list(decoys)
        true_labels = [1] * len(actives) + [0] * len(decoys)

        # Screen all molecules with min_match_ratio=0 to get Fit Values for all,
        # including those that don't pass the threshold (they get 0.0)
        loose_screener = VirtualScreening(self.pharmacophore, min_match_ratio=0.0)
        raw_matches = loose_screener.run(all_mols)

        # Build a score lookup: mol index → fit_value
        # VirtualScreening returns original mol objects; we use index tracking
        mol_to_score = {}
        for entry in raw_matches:
            mol_obj = entry['mol']
            for i, mol in enumerate(all_mols):
                if mol is mol_obj and i not in mol_to_score:
                    mol_to_score[i] = entry['fit_value']
                    break

        scores = np.array([mol_to_score.get(i, 0.0) for i in range(len(all_mols))])
        labels = np.array(true_labels, dtype=int)

        n_actives_found = int(np.sum(
            scores[:len(actives)] >= (1.0 / len(self.pharmacophore.interaction_sites))
            if len(self.pharmacophore.interaction_sites) > 0 else scores[:len(actives)] > 0
        ))

        report = {
            'n_actives': len(actives),
            'n_decoys': len(decoys),
            'n_actives_found': n_actives_found,
            'AUC': roc_auc(labels, scores),
            'BEDROC': bedroc(labels, scores, alpha=bedroc_alpha),
            'scores': scores,
            'labels': labels,
        }

        for frac in ef_fractions:
            pct = int(round(frac * 100))
            key = f'EF@{pct}%'
            report[key] = enrichment_factor(labels, scores, fraction=frac)

        return report
