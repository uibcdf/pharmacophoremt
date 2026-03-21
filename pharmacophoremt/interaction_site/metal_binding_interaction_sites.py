from .interaction_site import InteractionSite
from .shape.sphere import Sphere

class MetalBindingSphere(InteractionSite):

    def __init__(self, center, radius, skip_digestion=False):

        super().__init__(Sphere(center, radius, skip_digestion=skip_digestion), "metal coordination", skip_digestion=skip_digestion)
