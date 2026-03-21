import yaml
import json
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt import interaction_site as interaction_sites

def _to_dict(pharmacophore):
    """Internal helper to convert pharmacophore to a dictionary standard."""
    data = {
        "software": "pharmacophoremt",
        "version": "0.1.0",
        "name": pharmacophore.name,
        "description": pharmacophore.description,
        "interaction_sites": []
    }
    
    for site in pharmacophore.interaction_sites:
        site_dict = {
            "features": site.features,
            "shape": {
                "type": site.shape_name,
                "center": puw.get_value(site.center, to_unit='nm').tolist(),
                "radius": float(puw.get_value(site.radius, to_unit='nm'))
            }
        }
        if hasattr(site.shape, 'direction'):
            site_dict["shape"]["direction"] = puw.get_value(site.shape.direction).tolist()
        if hasattr(site.shape, 'normal'):
            site_dict["shape"]["normal"] = puw.get_value(site.shape.normal).tolist()
            
        data["interaction_sites"].append(site_dict)
    return data

def _from_dict(data):
    """Internal helper to create a pharmacophore from a dictionary standard."""
    from pharmacophoremt.pharmacophore import Pharmacophore
    
    if data.get("software") != "pharmacophoremt":
        raise ValueError("Not a valid PharmacophoreMT data structure")
        
    ph = Pharmacophore(name=data.get("name"), description=data.get("description"))
    
    for s_data in data["interaction_sites"]:
        features = s_data["features"]
        shape_data = s_data["shape"]
        stype = shape_data["type"]
        center = puw.quantity(shape_data["center"], 'nm')
        radius = puw.quantity(shape_data["radius"], 'nm')
        
        if stype == 'sphere':
            from pharmacophoremt.interaction_site.shape import Sphere
            site = interaction_sites.InteractionSite(Sphere(center, radius), features)
        elif stype == 'sphere and vector':
            from pharmacophoremt.interaction_site.shape import SphereAndVector
            direction = shape_data["direction"]
            site = interaction_sites.InteractionSite(SphereAndVector(center, radius, direction), features)
        else:
            raise NotImplementedError(f"Shape {stype} not yet supported")
            
        ph.add_interaction_site(site)
    return ph

def to_json(pharmacophore, file_name):
    """Export pharmacophore to a JSON file."""
    data = _to_dict(pharmacophore)
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

def load_json(file_name):
    """Load pharmacophore from a JSON file."""
    with open(file_name, 'r') as f:
        data = json.load(f)
    return _from_dict(data)

def to_yaml(pharmacophore, file_name):
    """Export pharmacophore to a YAML file."""
    data = _to_dict(pharmacophore)
    with open(file_name, 'w') as f:
        yaml.dump(data, f, sort_keys=False)

def load_yaml(file_name):
    """Load pharmacophore from a YAML file."""
    with open(file_name, 'r') as f:
        data = yaml.safe_load(f)
    return _from_dict(data)
