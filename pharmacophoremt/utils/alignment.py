import numpy as np
from rdkit.Numerics import rdAlignment
from rdkit.Chem.Pharm3D import EmbedLib
from rdkit.Chem import rdMolTransforms
from operator import itemgetter
from pharmacophoremt import pyunitwizard as puw

def align_pharmacophores(ref_coords, probe_coords):
    """
    Align two sets of coordinates using the Kabsch algorithm.
    
    Parameters
    ----------
    ref_coords : Quantity or ndarray
        Reference coordinates (N, 3).
    probe_coords : Quantity or ndarray
        Probe coordinates (N, 3).
        
    Returns
    -------
    rmsd : float
        RMSD of the alignment in Angstroms.
    trans_mat : ndarray
        4x4 transformation matrix.
    """
    ref = puw.get_value(ref_coords, to_unit='angstroms')
    probe = puw.get_value(probe_coords, to_unit='angstroms')
    
    ssd, trans_mat = rdAlignment.GetAlignmentTransform(ref, probe)
    rmsd = np.sqrt(ssd / ref.shape[0])
    
    return rmsd, trans_mat

def get_inertia_transform(coords, weights=None):
    """
    Calculate the transformation matrix to align the principal axes 
    of a set of points to the Cartesian axes.
    """
    pts = puw.get_value(coords, to_unit='angstroms')
    n_pts = pts.shape[0]
    
    if weights is None:
        weights = np.ones(n_pts)
    
    # 1. Center the points
    centroid = np.average(pts, axis=0, weights=weights)
    centered_pts = pts - centroid
    
    # 2. Compute principal axes using SVD
    weighted_pts = centered_pts * np.sqrt(weights)[:, np.newaxis]
    _, _, vh = np.linalg.svd(weighted_pts)
    
    # vh rows are the principal axes.
    rotation = vh
    
    # 3. Build 4x4 matrix: Rotate * Translate(-centroid)
    trans_mat = np.eye(4)
    trans_mat[:3, :3] = rotation
    trans_mat[:3, 3] = -rotation.dot(centroid)
    
    return trans_mat

def align_ligand_to_pharmacophore(ligand, atom_match, rdkit_pharmacophore):
    """
    Align an RDKit molecule to an RDKit Pharmacophore object.
    """
    try:
        _, embeddings, _ = EmbedLib.EmbedPharmacophore(ligand, atom_match, rdkit_pharmacophore, count=10)
    except:
        return None, None

    if not embeddings:
        return None, None

    # Scoring embeddings based on RMSD
    ref_pos = [f.GetPos() for f in rdkit_pharmacophore.getFeatures()]
    best_rmsd = float('inf')
    best_mol = None

    for mol in embeddings:
        conf = mol.GetConformer()
        # Calculate probe points from atom_match
        probe_pts = []
        for indices in atom_match:
            pts = [conf.GetAtomPosition(idx) for idx in indices]
            center = np.mean([[p.x, p.y, p.z] for p in pts], axis=0)
            from rdkit import Geometry
            probe_pts.append(Geometry.Point3D(float(center[0]), float(center[1]), float(center[2])))
        
        ssd, trans_mat = rdAlignment.GetAlignmentTransform(ref_pos, probe_pts)
        rmsd = np.sqrt(ssd / len(ref_pos))
        
        if rmsd < best_rmsd:
            best_rmsd = rmsd
            best_mol = mol
            rdMolTransforms.TransformConformer(best_mol.GetConformer(), trans_mat)

    return best_mol, best_rmsd
