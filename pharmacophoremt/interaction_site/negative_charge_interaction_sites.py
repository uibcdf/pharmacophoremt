from .interaction_site import InteractionSite
from .shape import Point, Sphere, GaussianKernel

class NegativeChargePoint(InteractionSite):

    def __init__(self, position):

        super().__init__(Point(position), "negative charge")

class NegativeChargeSphere(InteractionSite):

    def __init__(self, center, radius):

        super().__init__(Sphere(center, radius), "negative charge")

class NegativeChargeGaussianKernel(InteractionSite):

    def __init__(self, center, sigma):

        super().__init__(GaussianKernel(center, sigma), "negative charge")
