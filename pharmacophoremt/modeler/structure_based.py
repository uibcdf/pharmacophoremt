import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler.modeler import Modeler
from pharmacophoremt.pharmacophore import Pharmacophore
from pharmacophoremt import interaction_site as interaction_sites
from pharmacophoremt.data.smarts import PROTEIN_SMARTS
from pharmacophoremt.utils.maths import ring_normal
import molsysmt as msm
from rdkit import Chem
from argdigest import arg_digest
from smonitor import signal

class StructureBasedModeler(Modeler):
    """
    Modeler to extract interaction sites from a receptor structure (pocket).
    
    This engine projects ideal interaction points from the receptor atoms
    into the binding cavity.
    """

    # Ideal projection distances (Rescued/Standardized)
    PROJECTION_RULES = {
        'hb donor': puw.quantity(0.28, 'nm'),    # Project an Acceptor site from a Protein Donor
        'hb acceptor': puw.quantity(0.28, 'nm'), # Project a Donor site from a Protein Acceptor
        'aromatic ring': puw.quantity(0.45, 'nm'),
        'positive charge': puw.quantity(0.40, 'nm'),
        'negative charge': puw.quantity(0.40, 'nm'),
        'hydrophobicity': puw.quantity(0.35, 'nm'),
    }

    @signal(tags=["modeler", "structure", "init"])
    @arg_digest(type_check=True)
    def __init__(self, molecular_system, selection='molecule_type == "protein"',
                 pocket_selection=None, pocket_center=None, pocket_radius=None,
                 skip_digestion=False):
        
        if isinstance(molecular_system, str):
            self.system = msm.convert(molecular_system, to_form='molsysmt.MolSys')
        else:
            self.system = molecular_system
            
        while isinstance(self.system, (list, tuple)) and len(self.system) == 1:
            self.system = self.system[0]

        self.selection = selection
        self.pocket_selection = pocket_selection
        self.pocket_center = pocket_center   # puw quantity (3,) or None
        self.pocket_radius = pocket_radius   # puw quantity scalar or None
        self.params = self.PROJECTION_RULES.copy()

    def _detect_features(self, mol):
        """Detect chemical features in the receptor fragment."""
        found = {feat: [] for feat in PROTEIN_SMARTS}
        for feat_name, patterns in PROTEIN_SMARTS.items():
            for pattern in patterns:
                p = Chem.MolFromSmarts(pattern)
                if p is None: continue
                matches = mol.GetSubstructMatches(p)
                for m in matches:
                    if m not in found[feat_name]:
                        found[feat_name].append(m)
        return found

    def _get_centroid(self, mol, indices):
        conf = mol.GetConformer()
        pts = []
        for idx in indices:
            pos = conf.GetAtomPosition(idx)
            pts.append([pos.x, pos.y, pos.z])
        center = np.mean(np.array(pts), axis=0)
        return puw.quantity(center, 'angstroms')

    def _get_projection_vector(self, mol, indices, feature_type):
        """
        Calculate the ideal projection vector for a feature.
        (Simplified for Gen 1: projects along atom-neighbor bonds).
        """
        conf = mol.GetConformer()
        
        if feature_type == 'aromatic ring':
            center = self._get_centroid(mol, indices)
            pts = []
            for idx in indices:
                pos = conf.GetAtomPosition(idx)
                pts.append([pos.x, pos.y, pos.z])
            coords = puw.quantity(np.array(pts), 'angstroms')
            vector = ring_normal(np.arange(len(indices)), coords, center)
            return center, vector
            
        atom_idx = indices[0]
        atom = mol.GetAtomWithIdx(atom_idx)
        pos = conf.GetAtomPosition(atom_idx)
        center = puw.quantity([pos.x, pos.y, pos.z], 'angstroms')
        
        # Projection logic: move away from neighbors
        neighbors = atom.GetNeighbors()
        if not neighbors:
            return center, np.array([0, 0, 1])
            
        n_pos = conf.GetAtomPosition(neighbors[0].GetIdx())
        n_center = puw.quantity([n_pos.x, n_pos.y, n_pos.z], 'angstroms')
        
        # Vector neighbor -> atom (points INTO the pocket)
        vector = puw.get_value(center - n_center)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm
            
        return center, vector

    @signal(tags=["modeler", "structure", "build"])
    def build(self, structure_indices=0, add_excluded_volumes=True):
        """Build the pharmacophore by projecting sites from the receptor.

        Parameters
        ----------
        structure_indices : int, optional
            Which structure (frame) to use from the molecular system (default 0).
        add_excluded_volumes : bool, optional
            If True, add ExcludedVolume spheres for all non-hydrogen pocket atoms
            to block inaccessible space (default True).
        """
        ph = Pharmacophore(name="Structure-based Model", molecular_system=self.system)

        # 1. Isolate the pocket/receptor
        if self.pocket_selection:
            indices = msm.select(self.system, selection=self.pocket_selection)
        elif self.pocket_center is not None and self.pocket_radius is not None:
            # Primary route: spherical pocket around a geometric centre
            center_nm = puw.get_value(self.pocket_center, to_unit='nm')
            radius_nm = float(puw.get_value(self.pocket_radius, to_unit='nm'))
            protein_indices = [int(i) for i in msm.select(self.system, selection=self.selection)]
            coords_q = msm.get(self.system, element='atom', selection=protein_indices,
                               structure_indices=structure_indices, coordinates=True)
            coords_nm = puw.get_value(coords_q, to_unit='nm')[0]  # (N,3)
            dists = np.linalg.norm(coords_nm - center_nm, axis=1)
            mask = dists <= radius_nm
            indices = [protein_indices[i] for i, m in enumerate(mask) if m]
        else:
            indices = msm.select(self.system, selection=self.selection)

        indices = [int(i) for i in indices]
        receptor_mol = msm.convert(
            self.system, selection=indices,
            structure_indices=structure_indices, to_form='rdkit.Mol'
        )
        receptor_mol.UpdatePropertyCache()
        Chem.FastFindRings(receptor_mol)

        # 2. Detect protein features
        features = self._detect_features(receptor_mol)

        # 3. Project InteractionSites
        for feature_name, matches in features.items():
            if feature_name not in self.params:
                continue
                
            dist = self.params[feature_name]
            
            for indices in matches:
                center, vector = self._get_projection_vector(receptor_mol, indices, feature_name)
                projected_center = center + vector * dist
                
                if feature_name == 'hb donor':
                    site = interaction_sites.HBAcceptorSphereAndVector(
                        center=projected_center, radius='0.1 nm', direction=-vector, skip_digestion=True)
                elif feature_name == 'hb acceptor':
                    site = interaction_sites.HBDonorSphereAndVector(
                        center=projected_center, radius='0.1 nm', direction=-vector, skip_digestion=True)
                elif feature_name == 'aromatic ring':
                    site = interaction_sites.AromaticRingSphereAndVector(
                        center=projected_center, radius='0.15 nm', direction=-vector, skip_digestion=True)
                elif feature_name == 'hydrophobicity':
                    site = interaction_sites.HydrophobicSphere(
                        center=projected_center, radius='0.15 nm', skip_digestion=True)
                elif feature_name == 'positive charge':
                    site = interaction_sites.NegativeChargeSphere(
                        center=projected_center, radius='0.15 nm', skip_digestion=True)
                elif feature_name == 'negative charge':
                    site = interaction_sites.PositiveChargeSphere(
                        center=projected_center, radius='0.15 nm', skip_digestion=True)
                else:
                    continue
                    
                ph.add_interaction_site(site)

        # 4. Excluded volumes — one per heavy atom of the pocket
        if add_excluded_volumes:
            conf = receptor_mol.GetConformer()
            ev_radius = puw.quantity(0.10, 'nm')  # 1 Å — tight steric exclusion
            for atom in receptor_mol.GetAtoms():
                if atom.GetSymbol() == 'H':
                    continue
                pos = conf.GetAtomPosition(atom.GetIdx())
                center = puw.quantity([pos.x, pos.y, pos.z], 'angstroms')
                site = interaction_sites.ExcludedVolumeSphere(
                    center, ev_radius, skip_digestion=True
                )
                ph.add_interaction_site(site)

        return ph
