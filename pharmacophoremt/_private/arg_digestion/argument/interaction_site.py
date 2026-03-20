from pharmacophoremt.interaction_site.interaction_site import InteractionSite

def digest_interaction_site(interaction_site, ctx=None):
    if not isinstance(interaction_site, InteractionSite):
        raise TypeError(f"Expected InteractionSite, got {type(interaction_site)}")
    return interaction_site
