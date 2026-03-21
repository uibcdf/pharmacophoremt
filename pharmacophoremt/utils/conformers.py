import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from argdigest import arg_digest
from smonitor import signal

class ConformerGenerator:
    """
    Generator for molecular conformers using RDKit with energy minimization.
    
    Procedure:
    1. Generate an initial pool of conformers.
    2. Minimize using UFF or MMFF force fields.
    3. Filter by RMSD threshold to ensure diversity.
    """

    def __init__(self, n_conformers=50, rmsd_threshold=0.5, forcefield='uff', seed=-1):
        self.n_conformers = n_conformers
        self.rmsd_threshold = rmsd_threshold
        self.forcefield = forcefield.lower()
        self.seed = seed

    @signal(tags=["utils", "conformers", "generate"])
    @arg_digest(type_check=True)
    def generate(self, mol, skip_digestion=False):
        """Generate a set of minimized conformers for an RDKit Mol."""
        # Ensure hydrogens are present for forcefield calculation
        if not any(atom.GetSymbol() == 'H' for atom in mol.GetAtoms()):
            mol = Chem.AddHs(mol)
        
        # 1. Embed
        AllChem.EmbedMultipleConfs(
            mol, numConfs=self.n_conformers, 
            randomSeed=self.seed, pruneRmsThresh=-1.0
        )
        
        if mol.GetNumConformers() == 0:
            return mol # Fallback
            
        # 2. Minimize
        if self.forcefield == 'uff':
            AllChem.UFFOptimizeMoleculeConfs(mol)
        else:
            AllChem.MMFFOptimizeMoleculeConfs(mol)
            
        # 3. Filter by RMSD
        return self._filter_by_rmsd(mol)

    def _filter_by_rmsd(self, mol):
        """Internal helper to keep unique conformers."""
        if mol.GetNumConformers() <= 1:
            return mol
            
        conf_ids = [c.GetId() for c in mol.GetConformers()]
        keep = [conf_ids[0]]
        
        for i in range(1, len(conf_ids)):
            is_unique = True
            for accepted_id in keep:
                rmsd = AllChem.GetBestRMS(mol, mol, accepted_id, conf_ids[i])
                if rmsd < self.rmsd_threshold:
                    is_unique = False
                    break
            if is_unique:
                keep.append(conf_ids[i])
        
        # Create new mol with filtered conformers
        new_mol = Chem.Mol(mol)
        new_mol.RemoveAllConformers()
        for cid in keep:
            new_mol.AddConformer(mol.GetConformer(cid), assignId=True)
            
        return new_mol
