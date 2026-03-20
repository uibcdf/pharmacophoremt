from .interaction_site import InteractionSite
from .shape import Point, Sphere, GaussianKernel, Shapelet

class HydrophobicPoint(InteractionSite):

    def __init__(self, position):

        super().__init__(Point(position), "hydrophobicity")

class HydrophobicSphere(InteractionSite):

    def __init__(self, center, radius):

        super().__init__(Sphere(center, radius), "hydrophobicity")

class HydrophobicGaussianKernel(InteractionSite):

    def __init__(self, center, sigma):

        super().__init__(GaussianKernel(center, sigma), "hydrophobicity")

class HydrophobicShapelet(InteractionSite):

    def __init__(self):

        super().__init__(Shapelet(), "hydrophobicity")
