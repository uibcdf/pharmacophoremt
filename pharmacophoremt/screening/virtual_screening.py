from argdigest import arg_digest
from smonitor import signal
from pharmacophoremt.io.rdkit import to_rdkit
from pharmacophoremt.utils.alignment import align_ligand_to_pharmacophore
import molsysmt as msm
from rdkit import Chem
from rdkit.Chem import ChemicalFeatures
import os

class VirtualScreening:
    """
    Engine to perform virtual screening of molecular libraries against pharmacophores.
    """

    def __init__(self, pharmacophore):
        self.pharmacophore = pharmacophore
        self._rd_pharmacophore = to_rdkit(pharmacophore)
        self.matches = []

    @signal(tags=["screening", "run"])
    @arg_digest(type_check=True)
    def run(self, molecular_database, skip_digestion=False):
        """
        Run the screening against a database of molecules.
        
        Parameters
        ----------
        molecular_database : iterable
            An iterable of molecular systems (e.g., from molsysmt or a list of SMILES).
        """
        for mol_system in molecular_database:
            # 1. Convert to RDKit
            try:
                rd_mol = msm.convert(mol_system, to_form='rdkit.Mol')
            except:
                continue
            
            # 2. Match Features (Rescued Logic)
            # We use RDKit's built-in feature matching for speed in Gen 1
            # Note: This requires an FDEF file. We'll use the default one.
            from rdkit import RDConfig
            fdef = os.path.join(RDConfig.RDDataDir, 'BaseFeatures.fdef')
            feat_factory = ChemicalFeatures.BuildFeatureFactory(fdef)
            
            from rdkit.Chem.Pharm3D import EmbedLib
            can_match, all_matches = EmbedLib.MatchPharmacophoreToMol(rd_mol, feat_factory, self._rd_pharmacophore)
            
            if can_match:
                # 3. Refined Alignment
                # Get atom matches from the best embedding
                # (Simplified rescue: we take the first valid match for now)
                atom_match = [list(x.GetAtomIds()) for x in all_matches]
                
                aligned_mol, rmsd = align_ligand_to_pharmacophore(rd_mol, atom_match, self._rd_pharmacophore)
                
                if aligned_mol is not None:
                    self.matches.append({
                        'mol': mol_system,
                        'rmsd': rmsd,
                        'aligned_rdkit_mol': aligned_mol
                    })

        return self.matches
