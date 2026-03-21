import xml.etree.ElementTree as ET
import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt import interaction_site as interaction_sites

# Mapping from LigandScout feature types to pharmacophoremt feature names
LS_TO_PHMT = {
    'HBD': 'hb donor',
    'HBA': 'hb acceptor',
    'PI': 'positive charge',
    'NI': 'negative charge',
    'H': 'hydrophobicity',
    'AR': 'aromatic ring',
    'EXCL': 'excluded volume',
}

# Mapping from pharmacophoremt feature names to LigandScout feature types
PHMT_TO_LS = {v: k for k, v in LS_TO_PHMT.items()}

def from_ligandscout(pharmacophore):
    """Import a pharmacophore from a LigandScout .pml file.

    Parameters
    ----------
    pharmacophore : str
        Path to the .pml file.

    Returns
    -------
    Pharmacophore
        The imported pharmacophore object.
    """
    from pharmacophoremt.pharmacophore import Pharmacophore
    tmp_ph = Pharmacophore()

    tree = ET.parse(pharmacophore)
    root = tree.getroot()

    # LigandScout PML usually has a <pharmacophore> root or similar
    # We iterate over features. Note: LS structure can vary slightly by version.
    for feature_xml in root.findall('.//feature'):
        ls_type = feature_xml.get('type')
        if ls_type not in LS_TO_PHMT:
            continue
        
        phmt_feature = LS_TO_PHMT[ls_type]
        
        # Position and Tolerance
        pos_xml = feature_xml.find('position')
        if pos_xml is None:
            continue
            
        center = puw.quantity([
            float(pos_xml.get('x')), 
            float(pos_xml.get('y')), 
            float(pos_xml.get('z'))
        ], 'angstroms')
        
        radius = puw.quantity(float(pos_xml.get('tolerance', 1.0)), 'angstroms')
        
        # Check for directionality (Vectorial features)
        dir_xml = feature_xml.find('direction')
        
        if dir_xml is not None and phmt_feature in ['hb donor', 'hb acceptor', 'aromatic ring']:
            direction = [
                float(dir_xml.get('x')),
                float(dir_xml.get('y')),
                float(dir_xml.get('z'))
            ]
            
            if phmt_feature == 'hb donor':
                site = interaction_sites.HBDonorSphereAndVector(center, radius, direction)
            elif phmt_feature == 'hb acceptor':
                site = interaction_sites.HBAcceptorSphereAndVector(center, radius, direction)
            elif phmt_feature == 'aromatic ring':
                site = interaction_sites.AromaticRingSphereAndVector(center, radius, direction)
        else:
            # Non-vectorial or fallback to Sphere
            if phmt_feature == 'hydrophobicity':
                site = interaction_sites.HydrophobicSphere(center, radius)
            elif phmt_feature == 'positive charge':
                site = interaction_sites.PositiveChargeSphere(center, radius)
            elif phmt_feature == 'negative charge':
                site = interaction_sites.NegativeChargeSphere(center, radius)
            elif phmt_feature == 'excluded volume':
                site = interaction_sites.ExcludedVolumeSphere(center, radius)
            elif phmt_feature == 'aromatic ring':
                site = interaction_sites.AromaticRingSphere(center, radius)
            elif phmt_feature == 'hb donor':
                site = interaction_sites.HBDonorSphere(center, radius)
            elif phmt_feature == 'hb acceptor':
                site = interaction_sites.HBAcceptorSphere(center, radius)
            else:
                # Default generic site if no specialized class matches
                from pharmacophoremt.interaction_site.shape.sphere import Sphere
                site = interaction_sites.InteractionSite(Sphere(center, radius), phmt_feature)

        tmp_ph.add_interaction_site(site)

    return tmp_ph

def to_ligandscout(pharmacophore, file_name=None):
    """Export a pharmacophore to a LigandScout .pml file.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        The pharmacophore object to export.
    file_name : str, optional
        Path to the output .pml file.
    """
    root = ET.Element('pharmacophore')
    root.set('name', pharmacophore.name if pharmacophore.name else 'PharmacophoreMT Export')

    for i, site in enumerate(pharmacophore.interaction_sites):
        ls_type = PHMT_TO_LS.get(site.feature_name, 'H') # Default to Hydrophobic if unknown
        
        feature_xml = ET.SubElement(root, 'feature')
        feature_xml.set('type', ls_type)
        feature_xml.set('id', str(i))
        
        # Position
        pos_xml = ET.SubElement(feature_xml, 'position')
        center = puw.get_value(site.center, to_unit='angstroms')
        pos_xml.set('x', f"{center[0]:.3f}")
        pos_xml.set('y', f"{center[1]:.3f}")
        pos_xml.set('z', f"{center[2]:.3f}")
        
        radius = puw.get_value(site.radius, to_unit='angstroms')
        pos_xml.set('tolerance', f"{radius:.3f}")
        
        # Direction (if applicable)
        if hasattr(site, 'direction') and site.direction is not None:
            dir_xml = ET.SubElement(feature_xml, 'direction')
            direction = puw.get_value(site.direction) # Direction is dimensionless
            dir_xml.set('x', f"{direction[0]:.3f}")
            dir_xml.set('y', f"{direction[1]:.3f}")
            dir_xml.set('z', f"{direction[2]:.3f}")

    tree = ET.ElementTree(root)
    if file_name:
        with open(file_name, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            tree.write(f, encoding='utf-8', xml_declaration=False)
