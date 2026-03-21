from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt import interaction_site as interaction_sites
import molsysmt as msm
import json

def from_pharmer(pharmacophore):

    from pharmacophoremt.pharmacophore import Pharmacophore
    tmp_pharmacophore = Pharmacophore()

    if isinstance(pharmacophore, str):
        if pharmacophore.endswith('.json'):
            print(f"Reading file: {pharmacophore}")
            with open(pharmacophore, "r") as fff:
                pharmacophore = json.load(fff)
        else:
            raise NotImplementedError

    print(f"Number of points in JSON: {len(pharmacophore['points'])}")

    def get_pharmer_interaction_site_properties(interaction_site, direction=False):
        center = puw.quantity([interaction_site['x'], interaction_site['y'], interaction_site['z']], 'angstroms')
        radius = puw.quantity(interaction_site['radius'], 'angstroms')
        if direction:
            direction = [interaction_site['svector']['x'], interaction_site['svector']['y'], interaction_site['svector']['z']]
            return center, radius, direction

        return center, radius

    for pharmer_interaction_site in pharmacophore['points']:
        pharmer_feature_name = pharmer_interaction_site['name']

        if pharmer_feature_name=='Aromatic':
            center, radius, direction = get_pharmer_interaction_site_properties(pharmer_interaction_site, direction=True)
            interaction_site = interaction_sites.AromaticRingSphereAndVector(center, radius, direction)
            tmp_pharmacophore.add_interaction_site(interaction_site)

        elif pharmer_feature_name=='Hydrophobic':
            center, radius = get_pharmer_interaction_site_properties(pharmer_interaction_site, direction=False)
            interaction_site = interaction_sites.HydrophobicSphere(center, radius)
            tmp_pharmacophore.add_interaction_site(interaction_site)

        elif pharmer_feature_name=='HydrogenAcceptor':
            center, radius, direction = get_pharmer_interaction_site_properties(pharmer_interaction_site, direction=True)
            interaction_site = interaction_sites.HBAcceptorSphereAndVector(center, radius, direction)
            tmp_pharmacophore.add_interaction_site(interaction_site)

        elif pharmer_feature_name=="HydrogenDonor":
            center, radius, direction = get_pharmer_interaction_site_properties(pharmer_interaction_site, direction=True)
            interaction_site = interaction_sites.HBDonorSphereAndVector(center, radius, direction)
            tmp_pharmacophore.add_interaction_site(interaction_site)

        elif pharmer_feature_name=="PositiveIon":
            center, radius = get_pharmer_interaction_site_properties(pharmer_interaction_site, direction=False)
            interaction_site = interaction_sites.PositiveChargeSphere(center, radius)
            tmp_pharmacophore.add_interaction_site(interaction_site)
        
        elif pharmer_feature_name=="NegativeIon":
            center, radius = get_pharmer_interaction_site_properties(pharmer_interaction_site, direction=False)
            interaction_site = interaction_sites.NegativeChargeSphere(center, radius)
            tmp_pharmacophore.add_interaction_site(interaction_site)

        elif pharmer_feature_name=="ExclusionSphere":
            center, radius = get_pharmer_interaction_site_properties(pharmer_interaction_site, direction=False)
            interaction_site = interaction_sites.ExcludedVolumeSphere(center, radius)
            tmp_pharmacophore.add_interaction_site(interaction_site)

        elif pharmer_feature_name=='InclusionSphere':
            center, radius = get_pharmer_interaction_site_properties(pharmer_interaction_site, direction=False)
            interaction_site = interaction_sites.IncludedVolumeSphere(center, radius)
            tmp_pharmacophore.add_interaction_site(interaction_site)

        else:
            raise NotImplementedError

    if "ligand" in pharmacophore:
        ligand = msm.convert(pharmacophore["ligand"], to_form="molsysmt.MolSys")
        tmp_pharmacophore.molecular_system = ligand

    return tmp_pharmacophore

def to_pharmer(pharmacophore, file_name):

    pharmer_interaction_site_name = { # dictionary to map pharmacophoremt feature names to pharmer feature names
        "aromatic ring": "Aromatic",
        "hydrophobicity": "Hydrophobic",
        "hb acceptor": "HydrogenAcceptor",
        "hb donor": "HydrogenDonor",
        "included volume": "InclusionSphere",
        "excluded volume": "ExclusionSphere",
        "positive charge": "PositiveIon",
        "negative charge": "NegativeIon",
    }
    points = []
    for interaction_site in pharmacophore.interaction_sites:
        point_dict = {}
        temp_center = puw.get_value(interaction_site.center, to_unit='angstroms')
        point_dict["name"] = pharmer_interaction_site_name[interaction_site.feature_name]
        point_dict["svector"] = {}
        if hasattr(interaction_site, "direction"): 
            point_dict["hasvec"] = True
            point_dict["svector"]["x"] = interaction_site.direction[0]
            point_dict["svector"]["y"] = interaction_site.direction[1] 
            point_dict["svector"]["z"] = interaction_site.direction[2]  
        else: 
            point_dict["hasvec"] = False
            point_dict["svector"]["x"] = 1
            point_dict["svector"]["y"] = 0
            point_dict["svector"]["z"] = 0 
        point_dict["x"] = temp_center[0]
        point_dict["y"] = temp_center[1]
        point_dict["z"] = temp_center[2]
        point_dict["radius"] = puw.get_value(interaction_site.radius, to_unit='angstroms')
        point_dict["enabled"] = True
        point_dict["vector_on"] = 0
        point_dict["minsize"] = ""
        point_dict["maxsize"] = ""
        point_dict["selected"] = False

        points.append(point_dict)

    pharmer_dict = {}
    pharmer_dict["points"] = points

    # TODO: add ligand and/or receptor
    
    with open(file_name, "w") as outfile:
        json.dump(pharmer_dict, outfile)
