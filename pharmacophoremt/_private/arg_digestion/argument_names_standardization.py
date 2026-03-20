def argument_names_standardization(name):

    if name in ['interaction_site', 'interaction_sites', 'site', 'sites']:
        return 'interaction_sites'
    
    if name in ['molecular_system', 'system', 'mol_sys']:
        return 'molecular_system'

    return name
