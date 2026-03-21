def argument_names_standardization(caller, bound):

    new_bound = {}
    for name, value in bound.items():
        if name in ['interaction_site', 'interaction_sites', 'site', 'sites']:
            if 'interaction_site' in bound: # If already singular, keep it
                 new_bound['interaction_site'] = value
            elif 'interaction_sites' in bound: # If already plural, keep it
                 new_bound['interaction_sites'] = value
            else:
                # Default to singular for add_interaction_site, 
                # but this is still a bit brittle.
                # A better way is to check the caller or the function signature.
                new_bound['interaction_site'] = value
        elif name in ['molecular_system', 'system', 'mol_sys']:
            new_bound['molecular_system'] = value
        else:
            new_bound[name] = value

    return new_bound
