from rdkit import Geometry
from rdkit.Chem import ChemicalFeatures
from rdkit.Chem.Pharm3D import Pharmacophore as RDKitPharmacophore
import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt import interaction_site as interaction_sites

# Mapping from pharmacophoremt feature names to RDKit Families
# RDKit Family standard: Donor, Acceptor, Aromatic, Hydrophobic, PosIonizable, NegIonizable
PHMT_TO_RDKIT = {
    'hb donor': 'Donor',
    'hb acceptor': 'Acceptor',
    'aromatic ring': 'Aromatic',
    'hydrophobicity': 'Hydrophobic',
    'positive charge': 'PosIonizable',
    'negative charge': 'NegIonizable',
    'excluded volume': 'ExcludedVolume', # Custom or RDKit-compatible
}

RDKIT_TO_PHMT = {v: k for k, v in PHMT_TO_RDKIT.items()}

def to_rdkit(pharmacophore):
    """Convert a PharmacophoreMT object to an RDKit Pharmacophore object.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        The pharmacophore object to convert.

    Returns
    -------
    rdkit.Chem.Pharm3D.Pharmacophore.Pharmacophore
        The RDKit pharmacophore object.
    """
    rd_feats = []
    for site in pharmacophore.interaction_sites:
        family = PHMT_TO_RDKIT.get(site.feature_name, 'Any')
        
        # RDKit expects coordinates in Angstroms
        center = puw.get_value(site.center, to_unit='angstroms')
        pos = Geometry.Point3D(float(center[0]), float(center[1]), float(center[2]))
        
        # Create a FreeChemicalFeature using positional arguments
        # Signature: family, type, loc
        feat = ChemicalFeatures.FreeChemicalFeature(family, 'any', pos)
        rd_feats.append(feat)

    return RDKitPharmacophore.Pharmacophore(rd_feats)

def load_rdkit(rd_pharmacophore):
    """Convert an RDKit Pharmacophore object to a PharmacophoreMT object.

    Parameters
    ----------
    rd_pharmacophore : rdkit.Chem.Pharm3D.Pharmacophore.Pharmacophore
        The RDKit pharmacophore object.

    Returns
    -------
    Pharmacophore
        The PharmacophoreMT object.
    """
    from pharmacophoremt.pharmacophore import Pharmacophore
    phmt = Pharmacophore()

    for feat in rd_pharmacophore.getFeatures():
        family = feat.GetFamily()
        phmt_feature = RDKIT_TO_PHMT.get(family, 'any')
        
        pos = feat.GetPos()
        center = puw.quantity([pos.x, pos.y, pos.z], 'angstroms')
        
        # For now, RDKit features don't have a built-in 'radius' or 'tolerance'
        # in the FreeChemicalFeature itself (it's usually in the bounds matrix).
        # We'll use a default radius of 1.0 Angstrom.
        radius = puw.quantity(1.0, 'angstroms')
        
        # Mapping to specialized classes if possible
        if phmt_feature == 'hb donor':
            site = interaction_sites.HBDonorSphere(center, radius)
        elif phmt_feature == 'hb acceptor':
            site = interaction_sites.HBAcceptorSphere(center, radius)
        elif phmt_feature == 'aromatic ring':
            site = interaction_sites.AromaticRingSphere(center, radius)
        elif phmt_feature == 'hydrophobicity':
            site = interaction_sites.HydrophobicSphere(center, radius)
        elif phmt_feature == 'positive charge':
            site = interaction_sites.PositiveChargeSphere(center, radius)
        elif phmt_feature == 'negative charge':
            site = interaction_sites.NegativeChargeSphere(center, radius)
        else:
            from pharmacophoremt.interaction_site.shape.sphere import Sphere
            site = interaction_sites.InteractionSite(Sphere(center, radius), phmt_feature)

        phmt.add_interaction_site(site)

    return phmt
