"""
Molecular standardization and library filtering utilities.

These functions implement the preparation steps that should precede any
pharmacophore modeling or virtual screening run (Phase 0 of the classical
workflow).
"""

import numpy as np
from smonitor import signal
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, SaltRemover, MolStandardize


# ---------------------------------------------------------------------------
# Single-molecule standardization
# ---------------------------------------------------------------------------

@signal(tags=["utils", "preparation", "standardize"])
def standardize_mol(mol, remove_salts=True, neutralize=True,
                    remove_stereo_from_unknowns=False):
    """Standardize a single RDKit molecule for pharmacophore work.

    Steps applied in order:
    1. Desalt — keep the largest organic fragment.
    2. Neutralize — remove counterion charges (protonation-state normalisation).
    3. Sanitize — re-evaluate aromaticity, ring perception, valence.

    Parameters
    ----------
    mol : rdkit.Chem.Mol
        Input molecule (may be 2D or 3D; conformers are preserved).
    remove_salts : bool, optional
        Strip salt fragments (default True).
    neutralize : bool, optional
        Neutralize formal charges via MolStandardize (default True).
    remove_stereo_from_unknowns : bool, optional
        Remove stereo annotations that are marked unknown/unspecified
        (default False).

    Returns
    -------
    rdkit.Chem.Mol or None
        Standardized molecule, or None if standardization fails.
    """
    if mol is None:
        return None

    try:
        # 1. Desalt
        if remove_salts:
            remover = SaltRemover.SaltRemover()
            mol = remover.StripMol(mol, dontRemoveEverything=True)

        # 2. Neutralize via MolStandardize
        if neutralize:
            normalizer = MolStandardize.rdMolStandardize.Normalizer()
            mol = normalizer.normalize(mol)
            uncharger = MolStandardize.rdMolStandardize.Uncharger()
            mol = uncharger.uncharge(mol)

        # 3. Sanitize
        Chem.SanitizeMol(mol)

        if remove_stereo_from_unknowns:
            Chem.RemoveStereoChemistry(mol)

        return mol

    except Exception:
        return None


# ---------------------------------------------------------------------------
# Database filtering
# ---------------------------------------------------------------------------

def _compute_properties(mol):
    """Return a dict of molecular properties used for filtering."""
    return {
        'mw': Descriptors.ExactMolWt(mol),
        'logp': Descriptors.MolLogP(mol),
        'hbd': rdMolDescriptors.CalcNumHBD(mol),
        'hba': rdMolDescriptors.CalcNumHBA(mol),
        'rotbonds': rdMolDescriptors.CalcNumRotatableBonds(mol),
        'tpsa': rdMolDescriptors.CalcTPSA(mol),
        'rings': rdMolDescriptors.CalcNumRings(mol),
    }


@signal(tags=["utils", "preparation", "filter"])
def filter_database(molecules, min_mw=200.0, max_mw=600.0,
                    min_logp=-2.0, max_logp=5.0,
                    max_hbd=5, max_hba=10,
                    max_rotbonds=10, max_tpsa=140.0,
                    standardize=True):
    """Filter a molecular library by drug-likeness criteria.

    Applies Lipinski/Veber-style property filters. Molecules that fail
    any criterion are discarded. Optionally standardizes each molecule
    before filtering.

    Parameters
    ----------
    molecules : iterable of rdkit.Chem.Mol
        Input library.
    min_mw, max_mw : float
        Molecular weight range in Da (default 200–600).
    min_logp, max_logp : float
        LogP range (default −2 to 5).
    max_hbd : int
        Maximum H-bond donors (default 5 — Lipinski rule).
    max_hba : int
        Maximum H-bond acceptors (default 10 — Lipinski rule).
    max_rotbonds : int
        Maximum rotatable bonds (default 10 — Veber rule).
    max_tpsa : float
        Maximum topological polar surface area in Å² (default 140).
    standardize : bool
        Standardize each molecule before filtering (default True).

    Returns
    -------
    list of rdkit.Chem.Mol
        Molecules that pass all filters, in input order.
    """
    passed = []
    for mol in molecules:
        if mol is None:
            continue
        if standardize:
            mol = standardize_mol(mol)
            if mol is None:
                continue
        try:
            props = _compute_properties(mol)
        except Exception:
            continue

        if not (min_mw <= props['mw'] <= max_mw):
            continue
        if not (min_logp <= props['logp'] <= max_logp):
            continue
        if props['hbd'] > max_hbd:
            continue
        if props['hba'] > max_hba:
            continue
        if props['rotbonds'] > max_rotbonds:
            continue
        if props['tpsa'] > max_tpsa:
            continue

        passed.append(mol)

    return passed


@signal(tags=["utils", "preparation", "smiles"])
def smiles_to_mols(smiles_list, standardize=True):
    """Convert a list of SMILES strings to RDKit Mol objects.

    Invalid SMILES are silently skipped.

    Parameters
    ----------
    smiles_list : list of str
    standardize : bool
        Apply standardize_mol() to each parsed molecule (default True).

    Returns
    -------
    list of rdkit.Chem.Mol
    """
    mols = []
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue
        if standardize:
            mol = standardize_mol(mol)
            if mol is None:
                continue
        mols.append(mol)
    return mols
