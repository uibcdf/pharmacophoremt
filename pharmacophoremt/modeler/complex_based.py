import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler.modeler import Modeler
from pharmacophoremt.pharmacophore import Pharmacophore
from pharmacophoremt import interaction_site as interaction_sites
from pharmacophoremt.data.smarts import LIGAND_SMARTS, PROTEIN_SMARTS, SOLVENT_AND_IONS
from pharmacophoremt.utils.maths import ring_normal, angle_between_normals, point_projection
from pharmacophoremt.utils.chemistry import fix_bond_orders
import molsysmt as msm
import networkx as nx
from rdkit import Chem
from argdigest import arg_digest
from smonitor import signal

class ComplexBasedModeler(Modeler):
    """
    Modeler to extract interaction sites from protein-ligand complexes.
    """

    RULES = {
        'hb_dist_max': puw.quantity(0.35, 'nm'),
        'hb_ang_min': puw.quantity(120, 'degree'),
        'hyd_dist_max': puw.quantity(0.50, 'nm'),
        'charge_dist_max': puw.quantity(0.56, 'nm'),
        'pi_stack_dist_max': puw.quantity(0.75, 'nm'),
        'pi_stack_ang_dev': 30.0, # degrees
        'pi_stack_offset_max': puw.quantity(0.20, 'nm'),
        'halogen_dist_max': puw.quantity(0.40, 'nm'),
        'metal_dist_max': puw.quantity(0.28, 'nm'),
    }

    @signal(tags=["modeler", "complex", "init"])
    @arg_digest(type_check=True)
    def __init__(self, molecular_system, ligand_selection='molecule_type == "small molecule"', 
                 receptor_selection='molecule_type == "protein"', skip_digestion=False):
        
        if isinstance(molecular_system, str):
            self.system = msm.convert(molecular_system, to_form='molsysmt.MolSys')
        else:
            self.system = molecular_system
            
        # Aggressive Unpack
        while isinstance(self.system, (list, tuple)) and len(self.system) == 1:
            self.system = self.system[0]

        self.ligand_selection = ligand_selection
        self.receptor_selection = receptor_selection
        self.params = self.RULES.copy()

    def _detect_features(self, mol, smarts_dict):
        found = {feat: [] for feat in smarts_dict}
        for feat_name, patterns in smarts_dict.items():
            for pattern in patterns:
                p = Chem.MolFromSmarts(pattern)
                if p is None: continue
                matches = mol.GetSubstructMatches(p)
                for m in matches:
                    if m not in found[feat_name]:
                        found[feat_name].append(m)
        return found

    def _get_coords(self, mol, indices):
        conf = mol.GetConformer()
        pts = []
        for idx in indices:
            pos = conf.GetAtomPosition(idx)
            pts.append([pos.x, pos.y, pos.z])
        return puw.quantity(np.array(pts), 'angstroms')

    def _get_centroid(self, mol, indices):
        coords = self._get_coords(mol, indices)
        center = np.mean(puw.get_value(coords), axis=0)
        return puw.quantity(center, 'angstroms')

    def _get_h_atom_pos(self, mol, donor_idx):
        conf = mol.GetConformer()
        donor_atom = mol.GetAtomWithIdx(donor_idx)
        for neighbor in donor_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'H':
                pos = conf.GetAtomPosition(neighbor.GetIdx())
                return puw.quantity([pos.x, pos.y, pos.z], 'angstroms')
        return None

    def _dist(self, q1, q2):
        v1 = puw.get_value(q1, to_unit='nm')
        v2 = puw.get_value(q2, to_unit='nm')
        return np.linalg.norm(v1 - v2)

    def _angle(self, q1, q2, q3):
        v1 = puw.get_value(q1, to_unit='nm')
        v2 = puw.get_value(q2, to_unit='nm')
        v3 = puw.get_value(q3, to_unit='nm')
        ba = v1 - v2
        bc = v3 - v2
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        return np.degrees(angle)

    @signal(tags=["modeler", "complex", "build"])
    def build(self, structure_indices=None):
        
        # Detect hydrogens using correct attribute 'atom_type'
        atom_types = msm.get(self.system, element='atom', atom_type=True)
        if 'H' not in atom_types:
            self.system = msm.build.add_missing_hydrogens(self.system)
            
        if structure_indices is None:
            indices = [0]
            return_list = False
        elif isinstance(structure_indices, (int, np.integer)):
            indices = [structure_indices]
            return_list = False
        else:
            indices = structure_indices
            return_list = len(indices) > 1

        phs = []
        for idx in indices:
            ph = Pharmacophore(name="Complex-based Model", molecular_system=self.system, ref_struct=idx)

            lig_indices = [int(i) for i in msm.select(self.system, selection=self.ligand_selection)]
            ligand_mol = msm.convert(self.system, selection=lig_indices, structure_indices=idx, to_form='rdkit.Mol')
            ligand_mol.UpdatePropertyCache()
            Chem.FastFindRings(ligand_mol)
            
            group_names = msm.get(self.system, element='atom', selection=lig_indices, group_name=True)
            if len(group_names) > 0:
                ligand_mol = fix_bond_orders(ligand_mol, group_names[0])
                ligand_mol.UpdatePropertyCache()
                Chem.FastFindRings(ligand_mol)

            rec_indices = [int(i) for i in msm.select(self.system, selection=self.receptor_selection)]
            bs_selection = f'(index in {rec_indices}) within 0.8 nm of (index in {lig_indices})'
            bs_indices = [int(i) for i in msm.select(self.system, selection=bs_selection)]
            
            bs_group_names = msm.get(self.system, element='atom', selection=bs_indices, group_name=True)
            mask = [g not in SOLVENT_AND_IONS for g in bs_group_names]
            bs_indices = [bs_indices[i] for i, m in enumerate(mask) if m]

            receptor_bs_mol = msm.convert(self.system, selection=bs_indices, structure_indices=idx, to_form='rdkit.Mol')
            receptor_bs_mol.UpdatePropertyCache()
            Chem.FastFindRings(receptor_bs_mol)

            lig_feats = self._detect_features(ligand_mol, LIGAND_SMARTS)
            rec_feats = self._detect_features(receptor_bs_mol, PROTEIN_SMARTS)

            # --- Rules ---
            max_h_dist = puw.get_value(self.params['hb_dist_max'], to_unit='nm')
            min_h_ang = puw.get_value(self.params['hb_ang_min'], to_unit='degree')
            max_hyd_dist = puw.get_value(self.params['hyd_dist_max'], to_unit='nm')
            max_charge_dist = puw.get_value(self.params['charge_dist_max'], to_unit='nm')

            for l_indices in lig_feats['hydrophobicity']:
                l_center = self._get_centroid(ligand_mol, l_indices)
                for r_indices in rec_feats['hydrophobicity']:
                    r_center = self._get_centroid(receptor_bs_mol, r_indices)
                    if self._dist(l_center, r_center) <= max_hyd_dist:
                        ph.add_interaction_site(interaction_sites.HydrophobicSphere(l_center, '0.15 nm', skip_digestion=True))
                        break

            for l_indices in lig_feats['hb donor']:
                l_center = self._get_centroid(ligand_mol, l_indices)
                l_h_pos = self._get_h_atom_pos(ligand_mol, l_indices[0])
                if l_h_pos is None: continue
                for r_indices in rec_feats['hb acceptor']:
                    r_center = self._get_centroid(receptor_bs_mol, r_indices)
                    if self._dist(l_center, r_center) <= max_h_dist:
                        if self._angle(l_center, l_h_pos, r_center) >= min_h_ang:
                            dir_vec = puw.get_value(r_center - l_h_pos)
                            ph.add_interaction_site(interaction_sites.HBDonorSphereAndVector(l_center, '0.1 nm', dir_vec, skip_digestion=True))
                            break

            for l_indices in lig_feats['hb acceptor']:
                l_center = self._get_centroid(ligand_mol, l_indices)
                for r_indices in rec_feats['hb donor']:
                    r_center = self._get_centroid(receptor_bs_mol, r_indices)
                    r_h_pos = self._get_h_atom_pos(receptor_bs_mol, r_indices[0])
                    if r_h_pos is None: continue
                    if self._dist(l_center, r_center) <= max_h_dist:
                        if self._angle(r_center, r_h_pos, l_center) >= min_h_ang:
                            dir_vec = puw.get_value(r_h_pos - l_center)
                            ph.add_interaction_site(interaction_sites.HBAcceptorSphereAndVector(l_center, '0.1 nm', dir_vec, skip_digestion=True))
                            break

            for l_feat, r_feat, site_class in [('positive charge', 'negative charge', interaction_sites.PositiveChargeSphere),
                                              ('negative charge', 'positive charge', interaction_sites.NegativeChargeSphere)]:
                for l_indices in lig_feats[l_feat]:
                    l_center = self._get_centroid(ligand_mol, l_indices)
                    for r_indices in rec_feats[r_feat]:
                        r_center = self._get_centroid(receptor_bs_mol, r_indices)
                        if self._dist(l_center, r_center) <= max_charge_dist:
                            ph.add_interaction_site(site_class(l_center, '0.15 nm', skip_digestion=True))
                            break

            self._merge_interaction_sites(ph, feature_name='hydrophobicity', threshold='0.2 nm')
            phs.append(ph)

        return phs if return_list else phs[0]

    def _merge_interaction_sites(self, ph, feature_name, threshold):
        sites = ph.get(feature_name=feature_name, skip_digestion=True)
        if len(sites) < 2: return
        threshold_val = puw.get_value(puw.convert(threshold, to_unit='nm'))
        graph = nx.Graph()
        for i in range(len(sites)):
            graph.add_node(i)
            for j in range(i + 1, len(sites)):
                dist = self._dist(sites[i].center, sites[j].center)
                if dist <= threshold_val:
                    graph.add_edge(i, j)
        cliques = list(nx.find_cliques(graph))
        if len(cliques) == len(sites): return
        other_sites = [s for s in ph.interaction_sites if feature_name not in s.features]
        ph.interaction_sites = other_sites
        ph.n_interaction_sites = len(other_sites)
        for clique in cliques:
            centers = [puw.get_value(puw.convert(sites[i].center, to_unit='nm')) for i in clique]
            avg_center = np.mean(centers, axis=0)
            avg_center_q = puw.quantity(avg_center, 'nm')
            site_class = sites[clique[0]].__class__
            ph.add_interaction_site(site_class(avg_center_q, radius=sites[clique[0]].radius, skip_digestion=True))
