from .interaction_site import InteractionSite
from .shape import Point, Sphere, GaussianKernel, Shapelet

class HydrophobicPoint(InteractionSite):

    def __init__(self, position, skip_digestion=False):

        super().__init__(Point(position), "hydrophobicity", skip_digestion=skip_digestion)

class HydrophobicSphere(InteractionSite):

    def __init__(self, center, radius, skip_digestion=False):

        super().__init__(Sphere(center, radius), "hydrophobicity", skip_digestion=skip_digestion)

class HydrophobicGaussianKernel(InteractionSite):

    def __init__(self, center, sigma, skip_digestion=False):

        super().__init__(GaussianKernel(center, sigma), "hydrophobicity", skip_digestion=skip_digestion)

class HydrophobicShapelet(InteractionSite):

    def __init__(self, skip_digestion=False):

        super().__init__(Shapelet(), "hydrophobicity", skip_digestion=skip_digestion)
