from .interaction_site import InteractionSite
from .shape import Sphere, SphereAndVector

class HalogenBondSphere(InteractionSite):

    def __init__(self, center, radius, skip_digestion=False):

        super().__init__(Sphere(center, radius), "halogen bond", skip_digestion=skip_digestion)

class HalogenBondSphereAndVector(InteractionSite):

    def __init__(self, center, radius, direction, skip_digestion=False):

        super().__init__(SphereAndVector(center, radius, direction), "halogen bond", skip_digestion=skip_digestion)
