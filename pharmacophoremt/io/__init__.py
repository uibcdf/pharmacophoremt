from .ligandscout import from_ligandscout, to_ligandscout
from .pharmer import from_pharmer, to_pharmer
from .rdkit import load_rdkit, to_rdkit
from .sdf import load_sdf, to_sdf
from .phmt import load_json, load_yaml, to_json, to_yaml
import molsysmt as msm
import os

def load(file_name, **kwargs):
    """
    Polymorphic loader for molecular systems and pharmacophores.
    Rescued and refined from OpenPharmacophore.
    """
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string path.")

    extension = os.path.splitext(file_name)[1].lower()

    # 1. Pharmacophore Formats
    if extension == '.pml':
        return from_ligandscout(file_name)
    elif extension == '.json':
        # Check if it's our native JSON or a Pharmer JSON
        import json
        with open(file_name, 'r') as f:
            data = json.load(f)
        if data.get("software") == "pharmacophoremt":
            return load_json(file_name)
        else:
            return from_pharmer(file_name)
    elif extension in ['.yaml', '.yml']:
        return load_yaml(file_name)
    
    # 2. Molecular System Formats (via MolSysMT)
    # Most trajectory and structural formats
    try:
        return msm.convert(file_name, to_form='molsysmt.MolSys', **kwargs)
    except:
        raise ValueError(f"Format {extension} not recognized or failed to load via MolSysMT.")
