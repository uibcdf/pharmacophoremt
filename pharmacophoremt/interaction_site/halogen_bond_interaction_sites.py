from .interaction_site import InteractionSite
from .shape import Sphere, SphereAndVector

class HalogenBondSphere(InteractionSite):

    def __init__(self, center, radius):

        super().__init__(Sphere(center, radius), "halogen bond")

class HalogenBondSphereAndVector(InteractionSite):

    def __init__(self, center, radius, direction):

        super().__init__(SphereAndVector(center, radius, direction), "halogen bond")
