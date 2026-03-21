import numpy as np
import itertools
from collections import Counter, defaultdict
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler.modeler import Modeler
from pharmacophoremt.pharmacophore import Pharmacophore
from pharmacophoremt import interaction_site as interaction_sites
from pharmacophoremt.data.smarts import LIGAND_SMARTS
from pharmacophoremt.utils.alignment import align_pharmacophores
from pharmacophoremt.modeler.scoring import ScoringFunction
import molsysmt as msm
import networkx as nx
from rdkit import Chem
from argdigest import arg_digest
from smonitor import signal

class LigandBasedModeler(Modeler):
    """
    Modeler to find common pharmacophores (consensus) from a set of ligands.
    """

    @signal(tags=["modeler", "ligand", "init"])
    @arg_digest(type_check=True)
    def __init__(self, molecular_systems, n_points=3, min_actives=None, skip_digestion=False):
        self.systems = molecular_systems
        self.n_points = n_points
        self.min_actives = min_actives if min_actives is not None else len(molecular_systems)
        self.bin_size = puw.quantity(0.15, 'nm') # 1.5 Angstrom binning
        self.scorer = ScoringFunction()

    def _detect_features(self, mol, conf_id=0):
        """Detect chemical features and return their centroids."""
        found = defaultdict(list)
        conf = mol.GetConformer(conf_id)
        for feat_name, patterns in LIGAND_SMARTS.items():
            for pattern in patterns:
                p = Chem.MolFromSmarts(pattern)
                if p is None: continue
                matches = mol.GetSubstructMatches(p)
                for m in matches:
                    pts = [conf.GetAtomPosition(idx) for idx in m]
                    center = np.mean([[p.x, p.y, p.z] for p in pts], axis=0)
                    found[feat_name].append(puw.quantity(center, 'angstroms'))
        return found

    def _get_distance_vector(self, coords):
        """Compute the N*(N-1)/2 distance vector between coordinates."""
        n = coords.shape[0]
        if n < 2: return np.array([])
        diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
        dist_matrix = np.sqrt(np.sum(diff**2, axis=-1))
        iu = np.triu_indices(n, k=1)
        return dist_matrix[iu]

    def _recursive_partitioning(self, sublists, dim, n_dims, min_actives):
        """
        Recursive partitioning algorithm rescued and optimized.
        Groups candidates by similarity in their inter-site distances.
        """
        if dim >= n_dims:
            return [sublists]

        bins = defaultdict(list)
        bin_size_val = puw.get_value(self.bin_size, to_unit='nm')
        tolerance = 0.1 * bin_size_val

        for item in sublists:
            dist = item['distances'][dim]
            low_bin = np.floor(dist / bin_size_val) * bin_size_val
            bins[low_bin].append(item)

            remainder = dist % bin_size_val
            if remainder < tolerance:
                bins[low_bin - bin_size_val].append(item)
            elif remainder > (bin_size_val - tolerance):
                bins[low_bin + bin_size_val].append(item)

        results = []
        for b_coord in bins:
            box = bins[b_coord]
            # Check if this box contains enough unique ligands
            unique_ligands = {it['lig_idx'] for it in box}
            if len(unique_ligands) >= min_actives:
                results.extend(self._recursive_partitioning(box, dim + 1, n_dims, min_actives))
        
        return results

    @signal(tags=["modeler", "ligand", "build"])
    def build(self):
        """Execute the consensus algorithm using Recursive Partitioning."""
        
        # 1. Feature Extraction & Candidate Generation
        candidates = []
        for lig_idx, sys in enumerate(self.systems):
            if msm.get_form(sys) == 'rdkit.Mol':
                mol = sys
            else:
                mol = msm.convert(sys, to_form='rdkit.Mol')
            n_conformers = mol.GetNumConformers()
            
            for conf_idx in range(n_conformers):
                feats = self._detect_features(mol, conf_id=conf_idx)
                
                # Flatten features into a list of (type, coords)
                flat_feats = []
                for ftype, centers in feats.items():
                    for c in centers:
                        flat_feats.append({'type': ftype, 'coords': puw.get_value(c, to_unit='nm')})
                
                # Combinations of N points
                for combo in itertools.combinations(flat_feats, self.n_points):
                    coords = np.array([c['coords'] for c in combo])
                    dists = self._get_distance_vector(coords)
                    candidates.append({
                        'lig_idx': lig_idx,
                        'conf_idx': conf_idx,
                        'types': [c['type'] for c in combo],
                        'coords': coords,
                        'distances': dists
                    })

        # 2. Group by type-variant and Run Partitioning
        hypotheses = []
        by_variant = defaultdict(list)
        for cand in candidates:
            variant = tuple(sorted(cand['types']))
            by_variant[variant].append(cand)

        for variant, v_candidates in by_variant.items():
            if len({c['lig_idx'] for c in v_candidates}) < self.min_actives:
                continue
            
            n_dims = len(v_candidates[0]['distances'])
            surviving_boxes = self._recursive_partitioning(v_candidates, 0, n_dims, self.min_actives)
            
            # 3. Consolidate results from all boxes
            final_box_candidates = []
            for box in surviving_boxes:
                final_box_candidates.extend(box)
            
            if not final_box_candidates: continue

            # Build a graph of similarity between all surviving candidates
            consensus_graph = nx.Graph()
            for i in range(len(final_box_candidates)):
                consensus_graph.add_node(i)
                for j in range(i + 1, len(final_box_candidates)):
                    # Distance between distance-vectors (RMSD proxy)
                    d_rmsd = np.sqrt(np.mean((final_box_candidates[i]['distances'] - final_box_candidates[j]['distances'])**2))
                    if d_rmsd <= puw.get_value(self.bin_size, to_unit='nm'):
                        consensus_graph.add_edge(i, j)
            
            cliques = list(nx.find_cliques(consensus_graph))
            
            for clique in cliques:
                # Top representative of this clique
                seed = final_box_candidates[clique[0]]
                
                # Calculate score for the clique
                all_dists = np.array([final_box_candidates[i]['distances'] for i in clique])
                mean_dists = np.mean(all_dists, axis=0)
                rmsd = np.sqrt(np.mean((all_dists - mean_dists)**2))
                score = self.scorer(rmsd)

                ph = Pharmacophore(
                    name=f"Consensus {variant}",
                    score=float(score),
                    ref_mol=seed['lig_idx'],
                    ref_struct=seed['conf_idx']
                )
                for i in range(self.n_points):
                    ftype = seed['types'][i]
                    from pharmacophoremt.interaction_site.shape import Sphere
                    site = interaction_sites.InteractionSite(
                        Sphere(puw.quantity(seed['coords'][i], 'nm'), '0.15 nm'), 
                        ftype
                    )
                    ph.add_interaction_site(site)
                hypotheses.append(ph)

        # 4. Final Ranking
        hypotheses.sort(key=lambda x: x.score if x.score else 0, reverse=True)
        return hypotheses if hypotheses else [Pharmacophore(name="No Consensus Found")]
