from .interaction_site import InteractionSite
from .shape import Sphere

class MetalBindingSphere(InteractionSite):

    def __init__(self, center, radius):

        super().__init__(Sphere(center, radius), "metal coordination")
